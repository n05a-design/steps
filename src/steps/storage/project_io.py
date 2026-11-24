"""
STEPS Storage Core: Project IO, Schema Validation, Locks & Crash Recovery.

Handles:
- Loading and saving of STEPS project files (.stepsproj / .json)
- Lock-based double-instance concurrency protection
- Schema version checks (forward-compatibility protection)
- Transparent crash/corruption recovery using backup files
"""

from __future__ import annotations

import json
import os
import time
import uuid
from copy import deepcopy
from dataclasses import asdict, dataclass, field
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional

from .atomic import atomic_write_json, list_backups, validate_path_safety
from .exceptions import (
    CorruptedProjectError,
    LockCollisionError,
    StorageError,
    StorageSecurityError,
    UnsupportedSchemaVersionError,
)

CURRENT_SCHEMA_VERSION: str = "1.0.0"
CURRENT_APP_VERSION: str = "0.6.0-dev"


@dataclass
class Project:
    """In-memory representation of a STEPS music project."""
    title: str = "Untitled Project"
    project_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    schema_version: str = CURRENT_SCHEMA_VERSION
    app_version: str = CURRENT_APP_VERSION
    notation_convention: Literal["INT", "DE"] = "INT"
    metadata: Dict[str, Any] = field(default_factory=lambda: {
        "created_at": datetime.now(timezone.utc).isoformat(),
        "modified_at": datetime.now(timezone.utc).isoformat(),
        "author": "",
        "description": ""
    })
    time_settings: Dict[str, Any] = field(default_factory=lambda: {
        "ppq": 480,
        "time_signature": {"numerator": 4, "denominator": 4},
        "tempo_bpm": 120.0,
        "tempo_points": [{"start_tick": 0, "bpm": 120.0}]
    })
    tracks: List[Dict[str, Any]] = field(default_factory=lambda: [
        {
            "track_id": "trk_chords",
            "track_type": "CHORDS",
            "name": "Chords Track",
            "channel": 0,
            "events": []
        }
    ])

    def to_dict(self) -> Dict[str, Any]:
        """Serializes project into dictionary conforming to project.schema.json."""
        d = asdict(self)
        d["metadata"]["modified_at"] = datetime.now(timezone.utc).isoformat()
        return d

    @classmethod
    def from_dict(cls, data: Dict[str, Any]) -> Project:
        """Constructs Project from dictionary, validating minimum required fields."""
        required = ("schema_version", "project_id", "title", "time_settings", "tracks")
        missing = [f for f in required if f not in data]
        if missing:
            raise CorruptedProjectError(f"Missing required project fields: {missing}")

        return cls(
            title=data.get("title", "Untitled Project"),
            project_id=data.get("project_id", str(uuid.uuid4())),
            schema_version=data.get("schema_version", CURRENT_SCHEMA_VERSION),
            app_version=data.get("app_version", CURRENT_APP_VERSION),
            notation_convention=data.get("notation_convention", "INT"),
            metadata=data.get("metadata", {}),
            time_settings=data.get("time_settings", {}),
            tracks=data.get("tracks", [])
        )


@dataclass(frozen=True)
class ProjectLoadResult:
    """Project load outcome, including whether crash recovery used a backup."""

    project: Project
    recovered_from_backup: bool = False
    backup_path: Optional[Path] = None
    migrations: tuple[str, ...] = ()

    @property
    def migrated(self) -> bool:
        return bool(self.migrations)


class ProjectLock:
    """
    Manages a lockfile (<path>.lock) to prevent concurrent writes from
    multiple running instances.
    """
    def __init__(self, project_path: Path | str, timeout_seconds: float = 3600.0):
        self.project_path = Path(project_path)
        self.lock_path = self.project_path.parent / f".{self.project_path.name}.lock"
        self.timeout_seconds = timeout_seconds
        self._acquired = False

    def acquire(self) -> None:
        """Acquires lock. Raises LockCollisionError if active lock exists."""
        if self.lock_path.exists():
            try:
                info = json.loads(self.lock_path.read_text(encoding="utf-8"))
                lock_time = info.get("timestamp", 0)
                pid = info.get("pid", 0)

                # Check if lock is stale (older than timeout)
                if (time.time() - lock_time) < self.timeout_seconds:
                    # Check if process is still running (on POSIX)
                    is_running = True
                    try:
                        os.kill(pid, 0)
                    except OSError:
                        is_running = False

                    if is_running:
                        raise LockCollisionError(
                            f"Project is locked by another running process (PID {pid}, locked at {info.get('time_iso')})."
                        )
            except (json.JSONDecodeError, OSError):
                pass  # Corrupted or unreadable lock is treated as stale

        # Write fresh lock
        self.lock_path.parent.mkdir(parents=True, exist_ok=True)
        lock_info = {
            "pid": os.getpid(),
            "timestamp": time.time(),
            "time_iso": datetime.now(timezone.utc).isoformat(),
            "project": str(self.project_path)
        }
        self.lock_path.write_text(json.dumps(lock_info, indent=2), encoding="utf-8")
        self._acquired = True

    def release(self) -> None:
        """Releases the lock file."""
        if self.lock_path.exists():
            try:
                self.lock_path.unlink()
            except OSError:
                pass
        self._acquired = False

    def __enter__(self) -> ProjectLock:
        self.acquire()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self.release()


def _check_schema_version_compatibility(file_version: str) -> None:
    """
    Validates schema version compatibility.
    Rejects versions with higher major version numbers (e.g. 2.x when current is 1.x).
    """
    parts = file_version.split(".")
    curr_parts = CURRENT_SCHEMA_VERSION.split(".")
    try:
        file_major = int(parts[0])
        curr_major = int(curr_parts[0])
    except (ValueError, IndexError):
        raise UnsupportedSchemaVersionError(f"Malformed schema version string: {file_version!r}")

    if file_major > curr_major:
        raise UnsupportedSchemaVersionError(
            f"Project schema version {file_version} is newer than current supported version {CURRENT_SCHEMA_VERSION}. "
            "Please update STEPS to open this project."
        )


def migrate_project_data(raw: Dict[str, Any]) -> tuple[Dict[str, Any], tuple[str, ...]]:
    """Apply only documented, reversible 1.x project compatibility migrations."""
    migrated = deepcopy(raw)
    migrations: List[str] = []
    if "title" not in migrated or not isinstance(migrated["title"], str) or not migrated["title"].strip():
        raise CorruptedProjectError("Project title must be a non-empty string.")
    schema_version = migrated.get("schema_version", "1.0.0")
    if not isinstance(schema_version, str):
        raise CorruptedProjectError("Project schema_version must be a string.")

    parts = schema_version.split(".")
    if len(parts) != 3:
        raise UnsupportedSchemaVersionError(
            f"Malformed project schema version string: {schema_version!r}"
        )
    try:
        major = int(parts[0])
    except ValueError as exc:
        raise UnsupportedSchemaVersionError(
            f"Malformed project schema version string: {schema_version!r}"
        ) from exc

    legacy_0_x = major == 0
    if legacy_0_x:
        migrations.append("MIG-001 0.x-to-1.0.0")

    if "project_id" not in migrated:
        migrated["project_id"] = str(uuid.uuid4())
        migrations.append("MIG-002 add-project-id")
    if "app_version" not in migrated:
        migrated["app_version"] = CURRENT_APP_VERSION
        migrations.append("MIG-003 add-app-version")
    if "notation_convention" not in migrated:
        migrated["notation_convention"] = "INT"
        migrations.append("MIG-004 add-notation-convention")
    if "metadata" not in migrated or not isinstance(migrated["metadata"], dict):
        migrated["metadata"] = {}
        migrations.append("MIG-005 normalize-metadata")

    time_settings = migrated.get("time_settings")
    if not isinstance(time_settings, dict):
        time_settings = {}

    ppq = time_settings.get("ppq", 480)
    if isinstance(ppq, bool) or not isinstance(ppq, int) or not 96 <= ppq <= 1920:
        ppq = 480

    time_signature = time_settings.get("time_signature")
    if not isinstance(time_signature, dict):
        time_signature = {}
    numerator = time_signature.get("numerator", 4)
    denominator = time_signature.get("denominator", 4)
    if (
        isinstance(numerator, bool)
        or not isinstance(numerator, int)
        or not 1 <= numerator <= 32
    ):
        numerator = 4
    if (
        isinstance(denominator, bool)
        or not isinstance(denominator, int)
        or denominator not in (1, 2, 4, 8, 16, 32)
    ):
        denominator = 4
    normalized_time_signature = {
        "numerator": numerator,
        "denominator": denominator,
    }

    tempo_bpm = time_settings.get("tempo_bpm", 120.0)
    if (
        isinstance(tempo_bpm, bool)
        or not isinstance(tempo_bpm, (int, float))
        or not 20.0 <= tempo_bpm <= 400.0
    ):
        tempo_bpm = 120.0
    tempo_bpm = float(tempo_bpm)

    tempo_points = time_settings.get("tempo_points")
    normalized_tempo_points: List[Dict[str, Any]]
    if isinstance(tempo_points, list):
        valid_tempo_points = True
        normalized_tempo_points = []
        for point in tempo_points:
            if not isinstance(point, dict):
                valid_tempo_points = False
                break
            start_tick = point.get("start_tick")
            bpm = point.get("bpm")
            if (
                isinstance(start_tick, bool)
                or not isinstance(start_tick, int)
                or start_tick < 0
                or isinstance(bpm, bool)
                or not isinstance(bpm, (int, float))
                or not 20.0 <= bpm <= 400.0
            ):
                valid_tempo_points = False
                break
            normalized_tempo_points.append({"start_tick": start_tick, "bpm": float(bpm)})
        if not valid_tempo_points:
            normalized_tempo_points = [{"start_tick": 0, "bpm": tempo_bpm}]
        elif normalized_tempo_points:
            normalized_tempo_points.sort(key=lambda point: point["start_tick"])
            if normalized_tempo_points[0]["start_tick"] != 0:
                normalized_tempo_points.insert(0, {"start_tick": 0, "bpm": tempo_bpm})
            deduplicated: List[Dict[str, Any]] = []
            for point in normalized_tempo_points:
                if deduplicated and deduplicated[-1]["start_tick"] == point["start_tick"]:
                    deduplicated[-1] = point
                else:
                    deduplicated.append(point)
            normalized_tempo_points = deduplicated
        else:
            normalized_tempo_points = [{"start_tick": 0, "bpm": tempo_bpm}]
    else:
        normalized_tempo_points = [{"start_tick": 0, "bpm": tempo_bpm}]

    normalized_time_settings = {
        "ppq": ppq,
        "time_signature": normalized_time_signature,
        "tempo_bpm": tempo_bpm,
        "tempo_points": normalized_tempo_points,
    }
    if normalized_time_settings != time_settings:
        migrations.append("MIG-006 normalize-time-settings")
    migrated["time_settings"] = normalized_time_settings

    if "tracks" not in migrated or not isinstance(migrated["tracks"], list):
        migrated["tracks"] = []
        migrations.append("MIG-007 normalize-tracks")

    migrated["schema_version"] = CURRENT_SCHEMA_VERSION
    return migrated, tuple(dict.fromkeys(migrations))


def save_project(
    project: Project,
    path: Path | str,
    max_backups: int = 5,
    base_dir: Optional[Path | str] = None
) -> Path:
    """
    Saves a Project object to disk atomically with automatic backup rotation.
    """
    data = project.to_dict()
    return atomic_write_json(path, data, max_backups=max_backups, base_dir=base_dir)


def load_project_with_status(
    path: Path | str,
    auto_recover_from_backup: bool = True,
    base_dir: Optional[Path | str] = None
) -> ProjectLoadResult:
    """
    Loads a Project object from disk.
    If the file is corrupted and auto_recover_from_backup is True,
    attempts recovery from the latest valid backup file.
    """
    resolved_path = validate_path_safety(path, base_dir=base_dir)

    def _try_parse_file(target: Path) -> tuple[Project, tuple[str, ...]]:
        text = target.read_text(encoding="utf-8")
        if not text.strip():
            raise CorruptedProjectError(f"Project file is empty: {target}")
        raw = json.loads(text)
        if not isinstance(raw, dict):
            raise CorruptedProjectError("Project file root must be a JSON object.")
        schema_version = raw.get("schema_version", "1.0.0")
        if not isinstance(schema_version, str):
            raise CorruptedProjectError("Project schema_version must be a string.")
        _check_schema_version_compatibility(schema_version)
        migrated_raw, migrations = migrate_project_data(raw)
        project = Project.from_dict(migrated_raw)
        return project, migrations

    try:
        project, migrations = _try_parse_file(resolved_path)
        return ProjectLoadResult(project=project, migrations=migrations)
    except (json.JSONDecodeError, UnicodeDecodeError, CorruptedProjectError) as exc:
        if not auto_recover_from_backup:
            raise CorruptedProjectError(f"Project file {resolved_path} is corrupted: {exc}") from exc

        # Search for backups
        backups = list_backups(resolved_path)
        for b in backups:
            try:
                recovered, migrations = _try_parse_file(b)
                # Successfully loaded from backup!
                return ProjectLoadResult(
                    project=recovered,
                    recovered_from_backup=True,
                    backup_path=b,
                    migrations=migrations,
                )
            except Exception:
                continue

        raise CorruptedProjectError(
            f"Project file {resolved_path} is corrupted and no valid backup could be recovered: {exc}"
        ) from exc


def load_project(
    path: Path | str,
    auto_recover_from_backup: bool = True,
    base_dir: Optional[Path | str] = None
) -> Project:
    """Loads a project while preserving the existing Project-only API."""
    return load_project_with_status(
        path,
        auto_recover_from_backup=auto_recover_from_backup,
        base_dir=base_dir,
    ).project

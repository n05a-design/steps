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
CURRENT_APP_VERSION: str = "0.1.0"


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


def load_project(
    path: Path | str,
    auto_recover_from_backup: bool = True,
    base_dir: Optional[Path | str] = None
) -> Project:
    """
    Loads a Project object from disk.
    If the file is corrupted and auto_recover_from_backup is True,
    attempts recovery from the latest valid backup file.
    """
    resolved_path = validate_path_safety(path, base_dir=base_dir)
    if not resolved_path.exists():
        raise FileNotFoundError(f"Project file not found: {resolved_path}")

    def _try_parse_file(target: Path) -> Project:
        text = target.read_text(encoding="utf-8")
        if not text.strip():
            raise CorruptedProjectError(f"Project file is empty: {target}")
        raw = json.loads(text)
        _check_schema_version_compatibility(raw.get("schema_version", "1.0.0"))
        return Project.from_dict(raw)

    try:
        return _try_parse_file(resolved_path)
    except (json.JSONDecodeError, CorruptedProjectError) as exc:
        if not auto_recover_from_backup:
            raise CorruptedProjectError(f"Project file {resolved_path} is corrupted: {exc}") from exc

        # Search for backups
        backups = list_backups(resolved_path)
        for b in backups:
            try:
                recovered = _try_parse_file(b)
                # Successfully loaded from backup!
                return recovered
            except Exception:
                continue

        raise CorruptedProjectError(
            f"Project file {resolved_path} is corrupted and no valid backup could be recovered: {exc}"
        ) from exc

"""
STEPS Storage Core: Atomic File Persistence & Backup Rotation.

Guarantees:
- Zero data loss during crash or sudden shutdown (write to temp file, fsync, atomic rename)
- Multi-generation backup rotation
- Path safety against directory traversal attacks
"""

from __future__ import annotations

import json
import os
import shutil
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Dict, List, Optional

from .exceptions import StorageError, StorageSecurityError


def validate_path_safety(path: Path | str, base_dir: Optional[Path | str] = None) -> Path:
    """
    Validates that a path does not escape into forbidden system directories
    via path traversal ('../') or malformed components.
    """
    p = Path(path)
    # Check for path traversal substrings
    parts = p.parts
    if any(part == ".." for part in parts):
        raise StorageSecurityError(f"Path traversal detected in path: {path!r}")

    resolved = p.resolve()
    if base_dir is not None:
        base_resolved = Path(base_dir).resolve()
        try:
            resolved.relative_to(base_resolved)
        except ValueError:
            raise StorageSecurityError(f"Path {resolved} escapes allowed base directory {base_resolved}")

    return resolved


def rotate_backups(backup_dir: Path, file_stem: str, max_backups: int = 5) -> None:
    """Removes oldest backups if count exceeds max_backups."""
    if not backup_dir.exists():
        return
    backups = sorted(backup_dir.glob(f"{file_stem}.*.bak"), key=lambda f: f.stat().st_mtime)
    while len(backups) > max_backups:
        oldest = backups.pop(0)
        try:
            oldest.unlink()
        except OSError:
            pass


def create_backup_copy(target_path: Path, max_backups: int = 5) -> Optional[Path]:
    """
    Creates a timestamped backup copy in the .steps_backups directory
    adjacent to target_path if target_path exists.
    """
    if not target_path.exists() or target_path.stat().st_size == 0:
        return None

    backup_dir = target_path.parent / ".steps_backups"
    backup_dir.mkdir(parents=True, exist_ok=True)

    timestamp = datetime.now(timezone.utc).strftime("%Y%m%d_%H%M%S_%f")
    backup_path = backup_dir / f"{target_path.stem}.{timestamp}.bak"
    shutil.copy2(target_path, backup_path)

    rotate_backups(backup_dir, target_path.stem, max_backups=max_backups)
    return backup_path


def list_backups(target_path: Path) -> List[Path]:
    """Returns list of existing backup files for target_path, newest first."""
    backup_dir = target_path.parent / ".steps_backups"
    if not backup_dir.exists():
        return []
    backups = sorted(
        backup_dir.glob(f"{target_path.stem}.*.bak"),
        key=lambda f: f.stat().st_mtime,
        reverse=True
    )
    return backups


def atomic_write_json(
    target_path: Path | str,
    data: Dict[str, Any],
    indent: int = 2,
    max_backups: int = 5,
    base_dir: Optional[Path | str] = None
) -> Path:
    """
    Atomically writes a JSON dictionary to target_path:
    1. Validates path safety
    2. Backs up existing file
    3. Writes to temp file in same directory
    4. fsync ensures physical disk write
    5. Atomic replace (os.replace)
    """
    resolved_target = validate_path_safety(target_path, base_dir=base_dir)
    resolved_target.parent.mkdir(parents=True, exist_ok=True)

    # 1. Create backup if file exists
    if resolved_target.exists():
        create_backup_copy(resolved_target, max_backups=max_backups)

    # 2. Write to temp file in same directory (guarantees same filesystem for atomic rename)
    tmp_fd, tmp_path_str = tempfile.mkstemp(
        prefix=f".{resolved_target.name}.",
        suffix=".tmp",
        dir=resolved_target.parent
    )
    tmp_path = Path(tmp_path_str)

    try:
        with open(tmp_fd, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=indent, ensure_ascii=False)
            f.flush()
            os.fsync(f.fileno())

        # 3. Atomic replace
        os.replace(tmp_path, resolved_target)
    except Exception as exc:
        if tmp_path.exists():
            try:
                tmp_path.unlink()
            except OSError:
                pass
        raise StorageError(f"Failed to atomically write {resolved_target}: {exc}") from exc

    return resolved_target

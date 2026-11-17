"""STEPS storage, persistence, atomic IO, and undo/redo subsystems."""
from __future__ import annotations

from .atomic import (
    atomic_write_json,
    create_backup_copy,
    list_backups,
    rotate_backups,
    validate_path_safety,
)
from .exceptions import (
    CorruptedProjectError,
    LockCollisionError,
    StorageError,
    StorageSecurityError,
    UndoRedoError,
    UnsupportedSchemaVersionError,
)
from .project_io import (
    CURRENT_APP_VERSION,
    CURRENT_SCHEMA_VERSION,
    Project,
    ProjectLock,
    load_project,
    save_project,
)
from .undo import UndoStack

__all__ = [
    "StorageError",
    "CorruptedProjectError",
    "UnsupportedSchemaVersionError",
    "StorageSecurityError",
    "LockCollisionError",
    "UndoRedoError",
    "atomic_write_json",
    "validate_path_safety",
    "create_backup_copy",
    "list_backups",
    "rotate_backups",
    "CURRENT_SCHEMA_VERSION",
    "CURRENT_APP_VERSION",
    "Project",
    "ProjectLock",
    "save_project",
    "load_project",
    "UndoStack",
]

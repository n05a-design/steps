"""
STEPS Storage & Persistence: Domain Exceptions.

Provides specific exceptions for atomic persistence, crash recovery, lock management,
and schema migration.
"""

from __future__ import annotations


class StorageError(Exception):
    """Base exception for all storage, persistence and undo/redo operations."""
    pass


class CorruptedProjectError(StorageError):
    """Raised when a project file cannot be parsed or contains invalid JSON."""
    pass


class UnsupportedSchemaVersionError(StorageError):
    """Raised when the project schema version is higher than supported or incompatible."""
    pass


class StorageSecurityError(StorageError):
    """Raised when an operation attempts directory traversal or touches forbidden paths."""
    pass


class LockCollisionError(StorageError):
    """Raised when an existing active lock prevents concurrent file access."""
    pass


class UndoRedoError(StorageError):
    """Raised when an illegal undo/redo operation is attempted (e.g. empty stack)."""
    pass

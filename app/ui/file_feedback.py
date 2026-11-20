"""Localized presentation of file-operation failures."""

from __future__ import annotations

import errno
from pathlib import Path
from typing import Literal

from app.i18n import LocaleManager
from src.steps.storage.exceptions import (
    CorruptedProjectError,
    StorageError,
    StorageSecurityError,
    UnsupportedSchemaVersionError,
)


_FILE_ERROR_REASONS = {
    errno.EACCES: "permission",
    errno.EPERM: "permission",
    errno.EROFS: "permission",
    errno.EBUSY: "locked",
    errno.ENOSPC: "space",
    getattr(errno, "EDQUOT", errno.ENOSPC): "space",
    errno.ENOENT: "folder",
    errno.ENOTDIR: "folder",
    errno.EISDIR: "directory",
}


def file_error_reason(error: OSError) -> str:
    if getattr(error, "winerror", None) in (32, 33):
        return "locked"
    return _FILE_ERROR_REASONS.get(error.errno, "file")


def format_project_file_error(
    error: Exception, path: Path | str, operation: Literal["open", "save"], i18n: LocaleManager,
) -> str:
    if isinstance(error, CorruptedProjectError):
        reason = "corrupt"
    elif isinstance(error, UnsupportedSchemaVersionError):
        reason = "schema"
    elif isinstance(error, StorageSecurityError):
        reason = "path"
    else:
        cause = error.__cause__ if isinstance(error, StorageError) else error
        if isinstance(cause, OSError):
            reason = file_error_reason(cause)
            if operation == "open":
                if isinstance(cause, FileNotFoundError):
                    reason = "missing"
                elif reason == "file":
                    reason = "read"
        else:
            reason = "read" if operation == "open" else "file"
    return i18n.translate(f"project.file.error.{reason}", path=path)

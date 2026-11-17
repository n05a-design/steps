"""
STEPS Architecture Ports: Storage & Project Repository Port.

Adheres to:
- ADR-006 (Datenhaltung: JSON + Schema + atomarer Writer)
- Prompt 07, Prompt 12
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, List, Optional, Protocol

from ..storage.project_io import Project


class ProjectStoragePort(Protocol):
    """Protocol defining persistence and crash recovery operations for STEPS projects."""

    def save(self, path: Path | str, project: Project, write_backup: bool = True) -> Path:
        """Atomically saves project to disk with schema validation and backup rotation."""
        ...

    def load(self, path: Path | str, recover_from_backup: bool = True) -> Project:
        """Loads and validates project document, transparently recovering from corruptions."""
        ...

    def list_backups(self, project_path: Path | str) -> List[Path]:
        """Lists available backup snapshots in descending chronological order."""
        ...

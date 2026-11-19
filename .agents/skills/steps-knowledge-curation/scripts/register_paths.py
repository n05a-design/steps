"""Resolve the repository's canonical work register."""

from __future__ import annotations

from pathlib import Path


MASTER_NAME = "OFFENE_ARBEITSAUFFORDERUNGEN.md"
REPOSITORY_ROOT = Path(__file__).resolve().parents[4]


def absolute_path(value: str | Path, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} requires an absolute path without '..': {value}")
    return path


def master_path(value: str | Path | None = None) -> Path:
    if value is not None:
        return absolute_path(value, "Register")
    return REPOSITORY_ROOT / "docs" / "operations" / MASTER_NAME

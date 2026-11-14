"""Resolve the configured canonical register at command execution time."""

from __future__ import annotations

import os
from pathlib import Path


MASTER_NAME = "OFFENE_ARBEITSAUFFORDERUNGEN.md"


def absolute_path(value: str | Path, label: str) -> Path:
    path = Path(value).expanduser()
    if not path.is_absolute() or ".." in path.parts:
        raise ValueError(f"{label} requires an absolute path without '..': {value}")
    return path


def master_path(value: str | Path | None = None) -> Path:
    if value is not None:
        return absolute_path(value, "Register")
    configured = os.environ.get("STEPS_KNOWLEDGE_REGISTER")
    if configured:
        return absolute_path(configured, "STEPS_KNOWLEDGE_REGISTER")
    local_app_data = os.environ.get("LOCALAPPDATA")
    if os.name == "nt" and local_app_data:
        return absolute_path(local_app_data, "LOCALAPPDATA") / "StepsKnowledge" / MASTER_NAME
    raise ValueError("Set STEPS_KNOWLEDGE_REGISTER to the absolute path of the existing register.")

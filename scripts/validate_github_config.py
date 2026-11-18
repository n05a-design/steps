#!/usr/bin/env python3
"""Syntax and basic structural checks for versioned GitHub YAML configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any
import re

ROOT = Path(__file__).resolve().parents[1]
ISSUE_TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ALLOWED_FORM_FIELDS = {"textarea", "input", "markdown", "dropdown", "checkboxes"}
DISCUSSION_TEMPLATE_DIR = ROOT / ".github" / "DISCUSSION_TEMPLATE"


def _load_yaml(path: Path) -> Any:
    return path.read_text(encoding="utf-8")


def _validate_issue_form(path: Path, data: Any) -> None:
    if not isinstance(data, str):
        raise ValueError(f"{path}: expected text")
    if path.name == "config.yml":
        return
    if not re.search(r"(?m)^name:\s*\S", data):
        raise ValueError(f"{path}: missing form name")
    if not re.search(r"(?m)^description:\s*\S", data) or not re.search(r"(?m)^body:\s*$", data):
        raise ValueError(f"{path}: missing description or body")

    field_ids: set[str] = set()
    field_blocks = re.split(r"(?m)^  - type:\s*", data)
    for block in field_blocks[1:]:
        field_type = block.splitlines()[0].strip()
        if field_type not in ALLOWED_FORM_FIELDS:
            raise ValueError(f"{path}: unsupported or malformed field type {field_type!r}")
        if field_type == "markdown":
            continue
        match = re.search(r"(?m)^    id:\s*([A-Za-z0-9_-]+)\s*$", block)
        if not match:
            raise ValueError(f"{path}: missing field id")
        field_id = match.group(1)
        if field_id in field_ids:
            raise ValueError(f"{path}: duplicate field id {field_id}")
        field_ids.add(field_id)
        if not re.search(r"(?m)^    attributes:\s*$", block):
            raise ValueError(f"{path}: field {field_id!r} has no attributes")


def main() -> int:
    paths = sorted((ROOT / ".github").rglob("*.yml"))
    if not paths:
        raise SystemExit("No GitHub YAML files found")

    for path in paths:
        data = _load_yaml(path)
        if path.parent == ISSUE_TEMPLATE_DIR:
            _validate_issue_form(path, data)
        elif DISCUSSION_TEMPLATE_DIR in path.parents:
            _validate_issue_form(path, data)
        elif path.name == "dependabot.yml":
            if not re.search(r"(?m)^version:\s*2\s*$", data) or not re.search(r"(?m)^updates:\s*$", data):
                raise ValueError(f"{path}: invalid Dependabot top-level structure")
        elif path.name == "release.yml":
            if not re.search(r"(?m)^changelog:\s*$", data):
                raise ValueError(f"{path}: invalid release notes structure")
    print(f"Validated YAML syntax and basic forms for {len(paths)} GitHub configuration files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

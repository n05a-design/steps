#!/usr/bin/env python3
"""Syntax and basic structural checks for versioned GitHub YAML configuration."""

from __future__ import annotations

from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parents[1]
ISSUE_TEMPLATE_DIR = ROOT / ".github" / "ISSUE_TEMPLATE"
ALLOWED_FORM_FIELDS = {"textarea", "input", "markdown", "dropdown", "checkboxes"}
DISCUSSION_TEMPLATE_DIR = ROOT / ".github" / "DISCUSSION_TEMPLATE"


def _load_yaml(path: Path) -> Any:
    with path.open(encoding="utf-8") as file:
        return yaml.safe_load(file)


def _validate_issue_form(path: Path, data: Any) -> None:
    if path.name == "config.yml":
        if not isinstance(data, dict):
            raise ValueError(f"{path}: expected a mapping")
        return
    if not isinstance(data, dict) or not isinstance(data.get("name"), str):
        raise ValueError(f"{path}: missing form name")
    if not isinstance(data.get("description"), str) or not isinstance(data.get("body"), list):
        raise ValueError(f"{path}: missing description or body")

    field_ids: set[str] = set()
    for field in data["body"]:
        if not isinstance(field, dict) or field.get("type") not in ALLOWED_FORM_FIELDS:
            raise ValueError(f"{path}: unsupported or malformed field {field!r}")
        if field["type"] == "markdown":
            continue
        field_id = field.get("id")
        if not isinstance(field_id, str) or field_id in field_ids:
            raise ValueError(f"{path}: missing or duplicate field id {field_id!r}")
        field_ids.add(field_id)
        if not isinstance(field.get("attributes"), dict):
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
            if not isinstance(data, dict) or data.get("version") != 2 or not isinstance(data.get("updates"), list):
                raise ValueError(f"{path}: invalid Dependabot top-level structure")
        elif path.name == "release.yml":
            if not isinstance(data, dict) or not isinstance(data.get("changelog"), dict):
                raise ValueError(f"{path}: invalid release notes structure")
    print(f"Validated YAML syntax and basic forms for {len(paths)} GitHub configuration files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

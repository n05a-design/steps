#!/usr/bin/env python3
"""Validate version axes and release evidence without creating tags or releases."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def check() -> int:
    findings: list[str] = []
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    init_file = (ROOT / "src/steps/__init__.py").read_text(encoding="utf-8")
    changelog = (ROOT / "CHANGELOG.md").read_text(encoding="utf-8")

    py_match = re.search(r'version\s*=\s*"([^"]+)"', pyproject)
    init_match = re.search(r'__version__\s*=\s*"([^"]+)"', init_file)
    py_version = py_match.group(1) if py_match else ""
    init_version = init_match.group(1) if init_match else ""

    if py_version != init_version:
        findings.append(
            f"package source mismatch: pyproject={py_version} src.steps={init_version}"
        )
    version_base = re.sub(r"(?:-|_).*$", "", version)
    py_base = re.sub(r"[^0-9.].*$", "", py_version).rstrip(".")
    if version_base != py_base:
        findings.append(
            f"development/version mismatch: VERSION={version} pyproject={py_version}"
        )
    if "Unreleased" not in changelog:
        findings.append("CHANGELOG.md lacks the Unreleased development section")

    tags = subprocess.run(
        ["git", "tag", "--list"],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.splitlines()
    if "v0.1.0" not in tags:
        findings.append("existing v0.1.0 published-release tag is missing locally")
    if "v1.0.0" in tags:
        findings.append("v1.0.0 must not be considered released without a future owner decision")

    if findings:
        print("RELEASE CONSISTENCY FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(
        "RELEASE CONSISTENCY PASS:"
        f" VERSION={version}"
        f" pyproject={py_version}"
        f" src.steps={init_version}"
        " published-tag=v0.1.0"
    )
    return 0


def main() -> int:
    if "--check" not in sys.argv:
        print("Usage: python -B scripts/check_release_consistency.py --check")
        return 2
    return check()


if __name__ == "__main__":
    raise SystemExit(main())

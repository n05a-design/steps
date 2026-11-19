#!/usr/bin/env python3
"""Check documentation status axes without forcing every merge SHA to become a snapshot."""

from __future__ import annotations

import re
import subprocess
import sys
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
STATUS_DOCUMENTS = (
    Path("docs/IMPLEMENTATION.md"),
    Path("docs/product/V1.0.0_PRODUCT_CONTRACT.md"),
    Path("docs/project/PROJECT_OVERVIEW.md"),
    Path("docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md"),
)
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b")


def git(*args: str) -> str:
    return subprocess.run(
        ["git", *args],
        cwd=ROOT,
        check=True,
        capture_output=True,
        text=True,
    ).stdout.strip()


def commit_exists(revision: str) -> bool:
    result = subprocess.run(
        ["git", "cat-file", "-e", f"{revision}^{{commit}}"],
        cwd=ROOT,
        capture_output=True,
        text=True,
    )
    return result.returncode == 0

def snapshot_revisions(text: str) -> set[str]:
    marker = re.compile(
        r"(?:immutable snapshot|repository baseline|main at|main-referenz|main-Referenz|main-stand|Aktuelle `main`-Referenz)",
        re.IGNORECASE,
    )
    revisions: set[str] = set()
    for line in text.splitlines():
        if marker.search(line):
            revisions.update(SHA_RE.findall(line))
    return revisions


def version_axes() -> dict[str, str]:
    version = (ROOT / "VERSION").read_text(encoding="utf-8").strip()
    pyproject = (ROOT / "pyproject.toml").read_text(encoding="utf-8")
    init_file = (ROOT / "src/steps/__init__.py").read_text(encoding="utf-8")

    pyproject_match = re.search(r'version\s*=\s*"([^"]+)"', pyproject)
    init_match = re.search(r'__version__\s*=\s*"([^"]+)"', init_file)
    return {
        "VERSION": version,
        "pyproject": pyproject_match.group(1) if pyproject_match else "",
        "src.steps": init_match.group(1) if init_match else "",
    }


def check() -> int:
    head = git("rev-parse", "HEAD")
    findings: list[str] = []

    seen: dict[str, list[str]] = {}
    for relative in STATUS_DOCUMENTS:
        path = ROOT / relative
        if not path.is_file():
            findings.append(f"missing active status document: {relative}")
            continue
        text = path.read_text(encoding="utf-8")
        for sha in sorted(snapshot_revisions(text)):
            seen.setdefault(sha, []).append(str(relative))
            if not commit_exists(sha):
                findings.append(f"{relative}: unknown commit snapshot {sha}")

    axes = version_axes()
    if axes["pyproject"] and axes["pyproject"] != axes["src.steps"]:
        findings.append(
            f"package version mismatch: pyproject={axes['pyproject']} src.steps={axes['src.steps']}"
        )
    version_base = re.sub(r"(?:-|_).*$", "", axes["VERSION"])
    pyproject_base = re.sub(r"[^0-9.].*$", "", axes["pyproject"]).rstrip(".")
    if axes["VERSION"] and axes["pyproject"] and pyproject_base != version_base:
        findings.append(
            f"development/version-axis mismatch: VERSION={axes['VERSION']} pyproject={axes['pyproject']}"
        )

    readme = (ROOT / "README.md").read_text(encoding="utf-8")
    readme_de = (ROOT / "README.de.md").read_text(encoding="utf-8")
    if "No complete English/German UI localization" in readme:
        findings.append("README.md contradicts the implemented i18n catalogs")
    if "keine vollständige englisch/deutsche" in readme_de.lower():
        findings.append("README.de.md contradicts the implemented i18n catalogs")

    if findings:
        print("DOCUMENTATION CONSISTENCY FAIL")
        for finding in findings:
            print(f"- {finding}")
        return 1

    print(f"DOCUMENTATION CONSISTENCY PASS at HEAD {head}")
    print(
        "Version axes:"
        f" VERSION={axes['VERSION']}"
        f" pyproject={axes['pyproject']}"
        f" src.steps={axes['src.steps']}"
    )
    print(
        "Immutable snapshot commits:"
        f" {len(seen)} references across {len(STATUS_DOCUMENTS)} active status documents"
    )
    return 0


def main() -> int:
    if "--check" not in sys.argv:
        print("Usage: python -B scripts/check_documentation_consistency.py --check")
        return 2
    return check()


if __name__ == "__main__":
    raise SystemExit(main())

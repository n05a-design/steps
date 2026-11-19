#!/usr/bin/env python3
"""Validate the required STEPS Gemini Knowledge Pack documents."""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path
from urllib.parse import urlparse


ROOT = Path(__file__).resolve().parents[1]
PACK = ROOT / "docs" / "gemini-knowledge"
BASELINE_COMMIT = "00f4d5b9079575260c9f26d6d0f3305ab15e241a"
AUDIT_DATE = "2026-11-19"
REQUIRED_FILES = (
    "00_KNOWLEDGE_INDEX.md",
    "01_PROJECT_OVERVIEW.md",
    "02_PRODUCT_STRATEGY.md",
    "03_SYSTEM_ARCHITECTURE.md",
    "04_MUSIC_THEORY_ENGINE.md",
    "05_FEATURE_INVENTORY.md",
    "06_DATA_MODELS_AND_INTERFACES.md",
    "07_USER_EXPERIENCE.md",
    "08_INTERNATIONALIZATION.md",
    "09_DEVELOPMENT_AND_BUILD.md",
    "10_TESTING_AND_QUALITY.md",
    "11_ROADMAP_AND_BACKLOG.md",
    "12_KNOWN_ISSUES_AND_RISKS.md",
    "13_DESIGN_AND_BRANDING.md",
    "14_SECURITY_LICENSE_GOVERNANCE.md",
    "15_HISTORY_AND_DECISIONS.md",
    "16_GLOSSARY.md",
    "17_SOURCE_EVIDENCE_REGISTER.md",
    "18_GEMINI_USAGE_GUIDE.md",
    "19_GEMINI_INSTRUCTIONS.md",
    "20_UPDATE_AND_CHANGE_MAP.md",
    "21_FINAL_AUDIT_REPORT.md",
    "ZUSAMMENFASSUNG_DE.md",
)
STATUS_MARKERS = (
    "IMPLEMENTED",
    "TESTED",
    "PARTIAL",
    "PLANNED",
    "BLOCKED",
    "HISTORICAL",
    "NOT_EVIDENCED",
)
PLACEHOLDER_RE = re.compile(
    r"\b(?:TODO|TBD|FIXME|INSERT_HERE|REPLACE_ME)\b|\[(?:INSERT|REPLACE|TODO|TBD)[^\]]*\]",
    re.IGNORECASE,
)
SHA_RE = re.compile(r"\b[0-9a-f]{40}\b", re.IGNORECASE)
MARKDOWN_LINK_RE = re.compile(r"!?\[[^\]]*\]\(([^)]+)\)")


def _strip_code_fences(text: str) -> str:
    """Keep authored Markdown checks independent from examples in code fences."""
    return re.sub(r"```.*?```", "", text, flags=re.DOTALL)


def _relative_link_target(raw_target: str) -> str | None:
    target = raw_target.strip()
    if target.startswith("<") and target.endswith(">"):
        target = target[1:-1]
    target = target.split(maxsplit=1)[0] if target else ""
    parsed = urlparse(target)
    if parsed.scheme or target.startswith(("/", "#")):
        return None
    path = target.split("#", maxsplit=1)[0].split("?", maxsplit=1)[0]
    return path or None


def validate_pack() -> list[str]:
    errors: list[str] = []
    missing = [name for name in REQUIRED_FILES if not (PACK / name).is_file()]
    errors.extend(f"missing mandatory file: docs/gemini-knowledge/{name}" for name in missing)

    documents = sorted(PACK.glob("*.md"))
    if not documents:
        return errors + ["no Markdown documents found in docs/gemini-knowledge"]

    for path in documents:
        relative = path.relative_to(ROOT).as_posix()
        text = path.read_text(encoding="utf-8")
        for marker, expected in (
            ("Baseline commit", BASELINE_COMMIT),
            ("Audit date", AUDIT_DATE),
        ):
            if not re.search(
                rf"^\*\*{re.escape(marker)}:\*\*\s+`?{re.escape(expected)}`?\s*$",
                text,
                flags=re.MULTILINE,
            ):
                errors.append(f"{relative}: missing or inconsistent {marker} metadata")

        status_match = re.search(
            r"^\*\*Status:\*\*\s+([A-Z_]+)\b", text, flags=re.MULTILINE
        )
        if status_match is None:
            errors.append(f"{relative}: missing **Status:** metadata")
        elif status_match.group(1) not in STATUS_MARKERS:
            errors.append(
                f"{relative}: unrecognized status metadata {status_match.group(1)}"
            )
        if not all(status in text for status in STATUS_MARKERS):
            errors.append(f"{relative}: incomplete status vocabulary")

        authored = _strip_code_fences(text)
        if PLACEHOLDER_RE.search(authored):
            errors.append(f"{relative}: stale placeholder marker found")

        for sha in SHA_RE.findall(text):
            if sha.lower() != BASELINE_COMMIT:
                errors.append(f"{relative}: evidence commit {sha} differs from pinned baseline")

        for match in MARKDOWN_LINK_RE.finditer(text):
            target = _relative_link_target(match.group(1))
            if target is None:
                continue
            destination = (path.parent / target).resolve()
            try:
                destination.relative_to(PACK.resolve())
            except ValueError:
                # Local links may intentionally point to repository source documents.
                try:
                    destination.relative_to(ROOT.resolve())
                except ValueError:
                    errors.append(f"{relative}: relative link escapes repository: {target}")
                    continue
            if not destination.exists():
                errors.append(f"{relative}: broken relative Markdown link: {target}")

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="check the pack without modifying files")
    parser.parse_args()
    errors = validate_pack()
    if errors:
        print("Gemini knowledge pack check failed:")
        for error in errors:
            print(f"- {error}")
        return 1
    print(
        f"Gemini knowledge pack check passed: {len(REQUIRED_FILES)} mandatory files, "
        f"baseline {BASELINE_COMMIT}, audit date {AUDIT_DATE}."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())

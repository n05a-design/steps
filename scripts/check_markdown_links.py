#!/usr/bin/env python3
"""Check that relative Markdown links in the active documentation resolve.

The check covers tracked Markdown files outside dated archives, raw research
material and preserved originals. It reports links whose target file or
directory does not exist in the checkout. External URLs and in-page anchors are
not fetched or validated.
"""

from __future__ import annotations

import re
import subprocess
import sys
import unicodedata
import urllib.parse
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

# Preserved or historical material keeps its original links unchanged.
EXCLUDED_PREFIXES = (
    "archive/",
    "source_archive/",
    "publish_overlay/",
    "docs/project/Archiv/",
    "docs/project/originals/",
    "docs/project/Technische Auswertung/",
    "docs/audits/",
)
# Research material is source-bound; only the curated gap register is active.
RESEARCH_ACTIVE_PREFIXES = ("research/gaps/", "research/README.md")

# Dated evidence that intentionally points at removed binaries. Each entry
# names the commit that explains the removal; the source document stays as is.
HISTORICAL_LINKS = {
    (
        "docs/audit/fable-5.2/PR22_QUELLENVOTUM_2026-11-13.md",
        "../../../research/STEPS_Bibliothek/MusicTheory.pdf",
    ): "PDF binary removed in 9a316c6 in favour of curated Markdown",
}

LINK_RE = re.compile(r"!?\[[^\]]*\]\(\s*<?([^)\s>]+)>?(?:\s+\"[^\"]*\")?\s*\)")
FENCE_RE = re.compile(r"^(```|~~~).*?^\1", re.MULTILINE | re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]*`")
SKIP_SCHEMES = ("http://", "https://", "mailto:", "tel:", "data:")


def tracked_markdown(root: Path) -> list[str]:
    output = subprocess.run(
        ["git", "-c", "core.quotePath=false", "ls-files", "-z", "--", "*.md"],
        cwd=root,
        check=True,
        capture_output=True,
    ).stdout.decode("utf-8")
    return [path for path in output.split("\0") if path]


def is_active(path: str) -> bool:
    path = unicodedata.normalize("NFC", path)
    if path.startswith(EXCLUDED_PREFIXES):
        return False
    if path.startswith("research/"):
        return path.startswith(RESEARCH_ACTIVE_PREFIXES)
    return True


def link_targets(text: str) -> list[str]:
    text = FENCE_RE.sub("", text)
    text = INLINE_CODE_RE.sub("", text)
    return [match.group(1) for match in LINK_RE.finditer(text)]


def _exists(path: Path) -> bool:
    if path.exists():
        return True
    # macOS and Git may store a decomposed spelling of the same file name.
    for form in ("NFC", "NFD"):
        if Path(unicodedata.normalize(form, str(path))).exists():
            return True
    return False


def broken_links(root: Path, relative: str) -> list[str]:
    source = root / relative
    try:
        text = source.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as error:
        return [f"{relative}: unreadable ({error.__class__.__name__})"]
    findings: list[str] = []
    for target in link_targets(text):
        if target.startswith(SKIP_SCHEMES) or target.startswith("#"):
            continue
        path_part = urllib.parse.unquote(target.split("#", 1)[0].split("?", 1)[0])
        if not path_part:
            continue
        if path_part.startswith("/"):
            resolved = root / path_part.lstrip("/")
        else:
            resolved = source.parent / path_part
        if (relative, target) in HISTORICAL_LINKS:
            continue
        if not _exists(resolved):
            findings.append(f"{relative}: {target}")
    return findings


def check(root: Path = ROOT) -> int:
    files = [path for path in tracked_markdown(root) if is_active(path)]
    findings: list[str] = []
    for relative in files:
        findings.extend(broken_links(root, relative))
    if findings:
        print(f"MARKDOWN LINK CHECK FAIL: {len(findings)} broken relative links in {len(files)} files")
        for finding in findings:
            print(f"- {finding}")
        return 1
    print(f"MARKDOWN LINK CHECK PASS: {len(files)} active Markdown files")
    return 0


def main() -> int:
    if "--check" not in sys.argv:
        print("Usage: python -B scripts/check_markdown_links.py --check")
        return 2
    return check()


if __name__ == "__main__":
    raise SystemExit(main())

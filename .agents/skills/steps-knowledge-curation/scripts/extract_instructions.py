"""Extract untrusted task candidates from document text."""
from __future__ import annotations
import json
from pathlib import Path
import re
import sys

from check_source import resolve_source

# Semantic Pattern Definitions: (Category, Regex)
PATTERN_DEFINITIONS = [
    ("EXPLICIT_TODO", re.compile(r"\bTODO[:\s]+(.*)", re.I)),
    ("EXPLICIT_FIXME", re.compile(r"\bFIXME[:\s]+(.*)", re.I)),
    ("EXPLICIT_HACK", re.compile(r"\bHACK[:\s]+(.*)", re.I)),
    ("NORMATIVE_MUST_DE", re.compile(r"\b(?:muss|müssen|bedarf|erfordert)\s+.*(?:ergänzt|geprüft|implementiert|festgelegt|entschieden|erstellt|bereinigt|ausgeführt)", re.I)),
    ("NORMATIVE_MUST_EN", re.compile(r"\b(?:must|shall|should)\s+(?:be\s+)?(?:implemented|tested|verified|completed|resolved|decided|created|executed)", re.I)),
    ("OPEN_STATUS_DE", re.compile(r"\b(?:bleibt\s+(?:vorerst\s+)?offen|ist\s+offen|noch\s+offen|sind\s+offen|offen\b)", re.I)),
    ("OPEN_STATUS_EN", re.compile(r"\b(?:remains?\s+open|pending\s+resolution|is\s+open|still\s+open|unresolved)\b", re.I)),
    ("DECISION_REQUIRED_DE", re.compile(r"\b(?:Entscheidung\s+(?:ist\s+)?noch\s+zu\s+treffen|erfordert\s+(?:noch\s+)?(?:eine\s+)?Entscheidung|Owner-Entscheidung)", re.I)),
    ("DECISION_REQUIRED_EN", re.compile(r"\b(?:requires?\s+(?:an?\s+)?(?:owner\s+)?decision|pending\s+decision|decision\s+required)\b", re.I)),
    ("GAP_DEFERRED", re.compile(r"\b(?:zurückgestellt|vertagt|deferred|postponed)\b", re.I)),
    ("INFERRED_REVIEW_DE", re.compile(r"\b(?:prüfen|nachweisen|revalidieren|klären)\b", re.I))
]

def extract_from_file(
    path: str | Path, base_dir: str | Path | None = None,
) -> list[dict[str, str | int]]:
    """Return document candidates with their original text and line number."""
    target = resolve_source(path, base_dir)
    findings = []
    with target.open(encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str:
                continue
            for cat, pat in PATTERN_DEFINITIONS:
                m = pat.search(line_str)
                if m:
                    findings.append({
                        "line": idx,
                        "category": cat,
                        "origin": "CANDIDATE_FROM_DOCUMENT",
                        "match": m.group(0).strip(),
                        "raw_line": line_str[:120]
                    })
                    break
    return findings

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python extract_instructions.py <file_path> [base_dir]")
    try:
        results = extract_from_file(*sys.argv[1:])
    except (OSError, ValueError) as exc:
        sys.exit(str(exc))
    print(json.dumps({"trust": "UNTRUSTED_DOCUMENT_TEXT", "candidates": results}, indent=2))

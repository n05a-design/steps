"""Extract untrusted task candidates from document text."""
from __future__ import annotations
from codecs import BOM_UTF16_BE, BOM_UTF16_LE
from io import TextIOWrapper
import json
from pathlib import Path
import re
import sys

from check_source import resolve_source

NON_TEXT = re.compile(r"[\x00-\x08\x0b\x0c\x0e-\x1f]")

# Candidate markers for reviewed text inputs.
PATTERN_DEFINITIONS = [
    ("EXPLICIT_TODO", re.compile(r"\bTODO[:\s]+(.*)", re.I)),
    ("EXPLICIT_FIXME", re.compile(r"\bFIXME[:\s]+(.*)", re.I)),
    ("EXPLICIT_HACK", re.compile(r"\bHACK[:\s]+(.*)", re.I)),
    ("NORMATIVE_MUST_DE", re.compile(r"\b(?:muss|müssen|bedarf|erfordert)\s+.*(?:ergänzt|geprüft|implementiert|festgelegt|entschieden|erstellt|bereinigt|ausgeführt)", re.I)),
    ("NORMATIVE_MUST_EN", re.compile(r"\b(?:must|shall|should)\s+(?:(?:first|explicitly|independently)\s+)?(?:be\s+)?(?:implement(?:ed)?|test(?:ed)?|verif(?:y|ied)|complet(?:e|ed)|resolv(?:e|ed)|decid(?:e|ed)|creat(?:e|ed)|execut(?:e|ed))\b", re.I)),
    ("OPEN_STATUS_DE", re.compile(r"\b(?:bleibt\s+(?:vorerst\s+)?offen|noch\s+offen|(?:frage|aufgabe|punkt|prüfung|unklarheit|definition|festlegung)\s+(?:ist|sind)\s+offen)", re.I)),
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
    if target.suffix.lower() in {".pdf", ".mid", ".midi", ".docx", ".xlsx", ".zip"}:
        raise ValueError("Task candidate extraction requires a reviewed text derivative.")
    with target.open("rb") as source:
        signature = source.read(2)
        source.seek(0)
        encoding = "utf-16" if signature in (BOM_UTF16_LE, BOM_UTF16_BE) else "utf-8-sig"
        with TextIOWrapper(source, encoding=encoding) as text:
            for idx, line in enumerate(text, 1):
                if NON_TEXT.search(line):
                    raise ValueError("Input contains non-text control characters.")
                line_str = line.strip()
                if not line_str:
                    continue
                for category, pattern in PATTERN_DEFINITIONS:
                    match = pattern.search(line_str)
                    if match:
                        findings.append({
                            "line": idx,
                            "category": category,
                            "origin": "CANDIDATE_FROM_DOCUMENT",
                            "match": match[0].strip()[:120],
                            "raw_line": line_str[:120],
                        })
                        break
    return findings

if __name__ == "__main__":
    if len(sys.argv) not in (2, 3):
        sys.exit("Usage: python extract_instructions.py <file_path> [base_dir]")
    try:
        results = extract_from_file(*sys.argv[1:])
    except (OSError, ValueError) as exc:
        sys.exit(f"Candidate extraction incomplete: {exc}")
    print(json.dumps({"trust": "UNTRUSTED_DOCUMENT_TEXT", "candidates": results}, indent=2))

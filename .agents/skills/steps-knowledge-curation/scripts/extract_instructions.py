"""Extract explicit TODOs and inferred instructions from text/markdown files with semantic categorization."""
from __future__ import annotations
import sys, os, re

# Semantic Pattern Definitions: (Category, Regex, Origin)
PATTERN_DEFINITIONS = [
    ("EXPLICIT_TODO", re.compile(r"\bTODO[:\s]+(.*)", re.I), "EXPLICIT"),
    ("EXPLICIT_FIXME", re.compile(r"\bFIXME[:\s]+(.*)", re.I), "EXPLICIT"),
    ("EXPLICIT_HACK", re.compile(r"\bHACK[:\s]+(.*)", re.I), "EXPLICIT"),
    ("NORMATIVE_MUST_DE", re.compile(r"\b(?:muss|müssen|bedarf|erfordert)\s+.*(?:ergänzt|geprüft|implementiert|festgelegt|entschieden|erstellt|bereinigt|ausgeführt)", re.I), "INFERRED"),
    ("NORMATIVE_MUST_EN", re.compile(r"\b(?:must|shall|should)\s+(?:be\s+)?(?:implemented|tested|verified|completed|resolved|decided|created|executed)", re.I), "INFERRED"),
    ("OPEN_STATUS_DE", re.compile(r"\b(?:bleibt\s+(?:vorerst\s+)?offen|ist\s+offen|noch\s+offen|sind\s+offen|offen\b)", re.I), "INFERRED"),
    ("OPEN_STATUS_EN", re.compile(r"\b(?:remains?\s+open|pending\s+resolution|is\s+open|still\s+open|unresolved)\b", re.I), "INFERRED"),
    ("DECISION_REQUIRED_DE", re.compile(r"\b(?:Entscheidung\s+(?:ist\s+)?noch\s+zu\s+treffen|erfordert\s+(?:noch\s+)?(?:eine\s+)?Entscheidung|Owner-Entscheidung)", re.I), "OWNER_DECISION_REQUIRED"),
    ("DECISION_REQUIRED_EN", re.compile(r"\b(?:requires?\s+(?:an?\s+)?(?:owner\s+)?decision|pending\s+decision|decision\s+required)\b", re.I), "OWNER_DECISION_REQUIRED"),
    ("GAP_DEFERRED", re.compile(r"\b(?:zurückgestellt|vertagt|deferred|postponed)\b", re.I), "INFERRED"),
    ("INFERRED_REVIEW_DE", re.compile(r"\b(?:prüfen|nachweisen|revalidieren|klären)\b", re.I), "INFERRED")
]

def extract_from_file(path: str) -> list[dict[str, str | int]]:
    """Extract instruction markers with line number, context and semantic category."""
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    findings = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str or line_str.startswith("#"):
                continue
            for cat, pat, origin in PATTERN_DEFINITIONS:
                m = pat.search(line_str)
                if m:
                    findings.append({
                        "line": idx,
                        "category": cat,
                        "origin": origin,
                        "match": m.group(0).strip(),
                        "raw_line": line_str[:120]
                    })
                    break
    return findings

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python extract_instructions.py <file_path>")
        sys.exit(1)
    results = extract_from_file(sys.argv[1])
    print(f"Extracted {len(results)} potential instruction(s):")
    for r in results:
        print(f"  Line {r['line']} [{r['category']} - {r['origin']}]: {r['match']}")

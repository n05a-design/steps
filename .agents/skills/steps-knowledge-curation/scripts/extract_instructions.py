"""Extract explicit TODOs and inferred instructions from text/markdown files."""
from __future__ import annotations
import sys, os, re

INSTRUCTION_PATTERNS = [
    re.compile(r"\bTODO[:\s]+(.*)", re.I),
    re.compile(r"\bFIXME[:\s]+(.*)", re.I),
    re.compile(r"(muss\s+(?:noch\s+)?(?:ergänzt|geprüft|implementiert|festgelegt)\s+werden.*)", re.I),
    re.compile(r"(bleibt\s+(?:vorerst\s+)?offen.*)", re.I),
    re.compile(r"(Entscheidung\s+(?:ist\s+)?noch\s+zu\s+treffen.*)", re.I),
    re.compile(r"(erfordert\s+(?:noch\s+)?(?:eine\s+)?Entscheidung.*)", re.I)
]

def extract_from_file(path: str) -> list[dict[str, str | int]]:
    if not os.path.exists(path):
        raise FileNotFoundError(f"Path not found: {path}")
    findings = []
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        for idx, line in enumerate(f, 1):
            line_str = line.strip()
            for pat in INSTRUCTION_PATTERNS:
                m = pat.search(line_str)
                if m:
                    findings.append({
                        "line": idx,
                        "match": m.group(1).strip(),
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
        print(f"  Line {r['line']}: {r['match']}")

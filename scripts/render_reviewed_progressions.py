"""Render the reviewed STEPS catalog as Markdown and verify its source links."""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md"
REGISTRY = ROOT / "knowledge/sources/registry.yaml"

if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.steps.progression.engine import list_reviewed_progressions


def render() -> str:
    registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
    if registry["schema_version"] != 1:
        raise ValueError("Unsupported source registry version.")
    sources = {source["id"]: source for source in registry["sources"]}
    if len(sources) != len(registry["sources"]):
        raise ValueError("Duplicate source ID in the product registry.")
    lines = [
        "# Einzeln geprüfte STEPS-Progressionen", "",
        "Dieses Lernmaterial wird aus dem Datensatz für die App erzeugt.",
        "Zur Aktualisierung dient `python scripts/render_reviewed_progressions.py`.", "",
    ]
    for example in list_reviewed_progressions():
        progression = example.progression
        references = [sources[ident] for ident in example.source_ids]
        if any(source["rights_status"] != "approved" for source in references):
            raise ValueError(f"Unapproved reference for {progression.prog_id}.")
        links = " · ".join(f"[{source['title']}]({source['url']})" for source in references)
        lines.extend([
            f"## {progression.prog_id} – {progression.name}", "",
            f"- **Tonart** `{progression.default_key}`",
            f"- **Stufen** `{progression.roman_numerals}`",
            f"- **Akkorde** `{progression.chords_str}`", "",
            example.lesson, "",
            f"Fachlich geprüft am {example.reviewed_on}. {links}", "",
        ])
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    content = render()
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Reviewed learning material is out of date. Run the renderer.")
    else:
        OUTPUT.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()

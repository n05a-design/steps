"""Publish Markdown from the same approved pilot catalog used by the app."""

from __future__ import annotations

import argparse
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.knowledge import list_reviewed_progressions
from src.steps.progression.reviewed import ApprovedClaim, PublicationError

LABELS = {
    "fact": "Nachprüfbare Aussage",
    "convention": "Konvention",
    "style_interpretation": "Stilabhängige Interpretation",
}


def render_claim(approval: ApprovedClaim) -> list[str]:
    claim = approval.claim
    return [
        f"**{claim.claim_id} · {LABELS[claim.kind]}**", "",
        claim.text, "",
        f"- Gültigkeitsbereich — {claim.scope}",
        f"- Fachlicher Gegencheck — {claim.countercheck}",
        *(
            f"- Quelle — [{ref.title}](<{ref.url}>) · {ref.locator}"
            for ref in claim.citations
        ),
        f"- Freigabe — [{approval.reviewer}]({approval.evidence_url}) am {approval.reviewed_on}",
        f"- Fassungsfingerabdruck — `{claim.fingerprint}`", "",
    ]


def render() -> str:
    examples = list_reviewed_progressions()
    lines = [
        "# Freigegebene STEPS-Pilotprogressionen", "",
        "Dieses Lernmaterial wird aus demselben geprüften Datensatz wie der App-Katalog erzeugt.",
        f"Datenversion `{examples[0].catalog_version}`.", "",
        "## Schreibkonvention", "",
        *render_claim(examples[0].claims[0]),
    ]
    for example in examples:
        progression = example.progression
        lines.extend([
            f"## {progression.prog_id} – {progression.name}", "",
            f"- **Tonart** `{progression.default_key}`",
            f"- **Stufen** `{progression.roman_numerals}`",
            f"- **Akkorde** `{progression.chords_str}`", "",
        ])
        for approval in example.claims[1:]:
            lines.extend(render_claim(approval))
    return "\n".join(lines)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    try:
        content = render()
    except PublicationError as exc:
        raise SystemExit(f"Pilot publication blocked: {exc}") from None
    if args.check:
        if not OUTPUT.exists() or OUTPUT.read_text(encoding="utf-8") != content:
            raise SystemExit("Reviewed learning material is out of date. Run the renderer.")
    else:
        OUTPUT.write_text(content, encoding="utf-8")


if __name__ == "__main__":
    main()

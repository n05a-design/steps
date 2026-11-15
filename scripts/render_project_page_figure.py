"""Draw the project page figure from the reviewed pilot progressions.

The figure shows the MIDI notes that ``generate_progression_voicings`` returns
for the three approved examples. It is rendered from the current code, so the
picture on the project page cannot drift from what the core computes.
"""

from __future__ import annotations

import argparse
from html import escape
from pathlib import Path
import sys

ROOT = Path(__file__).resolve().parents[1]
OUTPUT = ROOT / "design/assets/project-page-pilot-voicings.svg"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from app.knowledge import list_reviewed_progressions
from src.steps.progression import generate_progression_voicings

# Colours of the logo masters in design/brand.
DARK, TEAL, LIGHT = "#15243c", "#209f95", "#4ee4cd"
WIDTH, HEIGHT = 1200, 482
PANEL_WIDTH, PANEL_GAP, MARGIN = 352, 32, 40
ROLL_TOP, ROW = 128, 9
FONT = "font-family=\"system-ui, 'Segoe UI', Helvetica, Arial, sans-serif\""


def render() -> str:
    examples = [(example.progression, generate_progression_voicings(example.progression))
                for example in list_reviewed_progressions()]
    notes = [note for _, voicings in examples for voicing in voicings for note in voicing.midi_notes]
    lowest, highest = min(notes) // 12 * 12, max(notes)
    roll_height = (highest - lowest + 1) * ROW

    def note_y(note: int) -> int:
        return ROLL_TOP + (highest - note) * ROW

    lines = [
        f'<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 {WIDTH} {HEIGHT}" role="img" '
        'aria-label="MIDI-Noten der drei freigegebenen Pilotbeispiele als Notenrolle">',
        f'  <rect width="{WIDTH}" height="{HEIGHT}" rx="28" fill="{DARK}"/>',
    ]
    for index, (progression, voicings) in enumerate(examples):
        left = MARGIN + index * (PANEL_WIDTH + PANEL_GAP)
        chords = progression.chords_str.split(" - ")
        column = PANEL_WIDTH / len(chords)
        lines += [
            f'  <text x="{left}" y="62" {FONT} font-size="24" font-weight="700" fill="#ffffff">'
            f"{escape(progression.name)}</text>",
            f'  <text x="{left}" y="92" {FONT} font-size="17" fill="{LIGHT}">'
            f'{escape(progression.prog_id)} · {escape(progression.roman_numerals.replace(" - ", " – "))}</text>',
            f'  <rect x="{left}" y="{ROLL_TOP - 8}" width="{PANEL_WIDTH}" height="{roll_height + 16}" '
            'rx="14" fill="#ffffff" fill-opacity="0.05"/>',
        ]
        for note in range(lowest, highest + 1, 12):
            y = note_y(note) + ROW / 2
            lines += [
                f'  <line x1="{left + 34}" y1="{y:g}" x2="{left + PANEL_WIDTH - 10}" y2="{y:g}" '
                'stroke="#ffffff" stroke-opacity="0.16"/>',
                f'  <text x="{left + 10}" y="{y + 4:g}" {FONT} font-size="11" fill="#ffffff" '
                f'fill-opacity="0.6">C{note // 12 - 1}</text>',
            ]
        for position, (chord, voicing) in enumerate(zip(chords, voicings)):
            x = left + 40 + position * (column - 12)
            width = column - 26
            for note in voicing.midi_notes:
                fill = TEAL if note == voicing.bass_note else LIGHT
                lines.append(f'  <rect x="{x:g}" y="{note_y(note) + 1}" width="{width:g}" '
                             f'height="{ROW - 2}" rx="3.5" fill="{fill}"/>')
            lines.append(f'  <text x="{x + width / 2:g}" y="{ROLL_TOP + roll_height + 36}" {FONT} '
                         f'font-size="18" font-weight="600" text-anchor="middle" fill="#ffffff">'
                         f"{escape(chord)}</text>")
    lines += [
        f'  <text x="{MARGIN}" y="{HEIGHT - 22}" {FONT} font-size="13" fill="#ffffff" fill-opacity="0.6">'
        "Ausgabe von generate_progression_voicings für die freigegebenen Pilotbeispiele · "
        "dunkler Balken = Basston</text>",
        "</svg>",
    ]
    return "\n".join(lines) + "\n"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="compare the stored figure without writing")
    args = parser.parse_args()
    figure = render()
    if args.check:
        stored = OUTPUT.read_text(encoding="utf-8").replace("\r\n", "\n") if OUTPUT.is_file() else None
        if stored != figure:
            print(f"outdated: {OUTPUT.relative_to(ROOT).as_posix()}", file=sys.stderr)
            return 1
        print("OK: project page figure matches the pilot voicings.")
        return 0
    OUTPUT.write_text(figure, encoding="utf-8", newline="\n")
    print(f"{OUTPUT.relative_to(ROOT).as_posix()}: {len(figure.encode('utf-8'))} bytes")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())

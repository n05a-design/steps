"""Localized presentation of chord analysis and keyboard voicings."""

from __future__ import annotations

from collections.abc import Callable
from typing import Literal

from src.steps.theory.chord import parse_chord
from src.steps.theory.pitch import NoteSpelling
from src.steps.theory.scale import SCALE_TEMPLATES, construct_scale


def _note_name(note: NoteSpelling, convention: Literal["INT", "DE"]) -> str:
    return note.render(convention).removesuffix(str(note.octave))


def format_chord_analysis(
    chord_name: str,
    convention: Literal["INT", "DE"],
    translate: Callable[..., str],
) -> str:
    chord = parse_chord(chord_name, convention=convention)
    voicing = chord.to_voicing(bass_octave=3, voicing_type="CLOSE")

    required = chord.pitch_class_set
    if chord.bass is not None:
        required.add(int(chord.bass.pitch_class))
    root = int(chord.root.pitch_class)
    candidates = [
        template for template in SCALE_TEMPLATES.values()
        if required <= {(root + interval) % 12 for interval in template.intervals}
    ]

    quality = chord.quality or translate("chord.quality.major")
    lines = [
        translate("chord.analysis.title", chord=chord_name),
        "=" * 50,
        f"{translate('chord.root')}: {_note_name(chord.root, convention)} "
        f"({translate('chord.pitch_class')} {int(chord.root.pitch_class)})",
        f"{translate('chord.quality')}: {quality}",
        f"{translate('chord.intervals')}: {chord.theoretical_intervals}",
        f"{translate('chord.voicing')}: {voicing.midi_notes}",
        "",
        translate("scales.heading"),
        "-" * 50,
    ]
    if not candidates:
        lines.append(translate("scales.none"))
    for candidate in candidates:
        scale = construct_scale(chord.root, candidate)
        notes = " - ".join(_note_name(note, convention) for note in scale.spellings)
        lines.append(f"• {scale.template.name.upper():16s} {notes}")
    lines.extend(("", translate("diagnosis.heading"), "-" * 50, translate("diagnosis.voicing")))
    return "\n".join(lines)


def format_beginner_voicings(beginner: dict, translate: Callable[..., str]) -> str:
    if not beginner:
        return ""
    lines = [
        translate("beginner.heading"),
        "-" * 50,
        translate(
            "beginner.summary",
            smoothness=f'{beginner["smoothness_score"]:.1f}',
            distance=beginner["total_l1_distance"],
        ),
    ]
    for voicing in beginner["voicings"]:
        lines.append(translate(
            "beginner.voicing",
            chord=voicing["chord_symbol"],
            bass=voicing["lh_spelling"],
            lh_finger=voicing["lh_fingering"],
            notes=" ".join(voicing["rh_spellings"]),
        ))
    for transition in beginner["transitions"]:
        lines.append(translate(
            "beginner.transition.measurements",
            from_chord=transition["from_chord"],
            to_chord=transition["to_chord"],
            common=len(transition["common_tones"]),
            distance=transition["total_l1_distance"],
            leap=transition["max_single_leap"],
        ))
        lines.append("  " + translate(
            "beginner.transition.original", guidance=transition["pedagogical_guidance"],
        ))
    return "\n".join(lines)

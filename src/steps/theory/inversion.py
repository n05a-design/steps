"""
STEPS Theory Core: Chord Inversion & Figured Bass Engine (M04 / OA-0025).

Adheres to:
- M04 (Akkordumkehrungen, Bezifferter Bass, Hand-Voicing vs. Gesamtinversion)
- Aldwell & Schachter (1989): Harmony and Voice Leading, Chapters 4–5
- de la Motte, Diether (1976): Harmonielehre
- Golden Reference Cases: REF-0031, REF-0032
- Fixes ERR-006 (Strict distinction between root deduction and bass-driven inversion)
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import Enum
from typing import Any, List, Optional, Tuple, Union

from .exceptions import ChordConstructionError, VoiceLeadingError
from .chord import Voicing


class ChordInversion(str, Enum):
    """
    Classical inversion state determined by the lowest sounding pitch (bass).
    """
    ROOT_POSITION = "ROOT_POSITION"      # Grundstellung
    FIRST_INVERSION = "FIRST_INVERSION"  # 1. Umkehrung (Terz im Bass)
    SECOND_INVERSION = "SECOND_INVERSION"# 2. Umkehrung (Quinte im Bass)
    THIRD_INVERSION = "THIRD_INVERSION"  # 3. Umkehrung (Septime im Bass, nur Vierklänge)


class FiguredBassSymbol(str, Enum):
    """
    Standard figured bass notation (Generalbass-Ziffern).
    """
    TRIAD_ROOT = "5/3"
    TRIAD_FIRST = "6"
    TRIAD_SECOND = "6/4"
    SEVENTH_ROOT = "7"
    SEVENTH_FIRST = "6/5"
    SEVENTH_SECOND = "4/3"
    SEVENTH_THIRD = "4/2"


@dataclass(frozen=True)
class InversionAnalysis:
    """
    Detailed result of chord inversion analysis.
    """
    inversion: ChordInversion
    figured_bass: str
    bass_factor: str  # 'ROOT', 'THIRD', 'FIFTH', 'SEVENTH'
    root_pc: int
    bass_pc: int
    german_name: str
    is_seventh_chord: bool


def _deduce_triad_or_seventh_root(pcs: set[int]) -> tuple[int, bool]:
    """
    Deduces the harmonic root pitch class and whether the set represents a seventh chord.
    Returns:
        (root_pitch_class, is_seventh_chord)
    """
    # 1. Check seventh chords (4 pitch classes)
    if len(pcs) >= 4:
        for root in pcs:
            # Major 7th, Dominant 7th, Minor 7th, Half-diminished, Diminished 7th
            triad_thirds = {3, 4}
            fifths = {6, 7, 8}
            sevenths = {9, 10, 11}
            rel = {(p - root) % 12 for p in pcs}
            has_3 = bool(rel & triad_thirds)
            has_5 = bool(rel & fifths)
            has_7 = bool(rel & sevenths)
            if has_3 and has_7:
                return root, True

    # 2. Check triads (3 pitch classes)
    for root in pcs:
        # Major (0, 4, 7), Minor (0, 3, 7), Diminished (0, 3, 6), Augmented (0, 4, 8)
        rel = {(p - root) % 12 for p in pcs}
        if rel in (
            {0, 4, 7},  # Major
            {0, 3, 7},  # Minor
            {0, 3, 6},  # Diminished
            {0, 4, 8},  # Augmented
            {0, 2, 7},  # Sus2
            {0, 5, 7},  # Sus4
        ):
            return root, False

    # 3. Fallback: Check if 3 tones form a subset of standard triad
    for root in pcs:
        rel = {(p - root) % 12 for p in pcs}
        if {0, 4, 7}.issubset(rel) or {0, 3, 7}.issubset(rel):
            return root, len(pcs) >= 4

    # If ambiguous or modal, pick the lowest pitch class as default root
    return min(pcs), len(pcs) >= 4


def detect_chord_inversion(
    notes: Union[List[int], Tuple[int, ...], Voicing],
    root_pitch_class: Optional[int] = None,
    is_seventh: Optional[bool] = None
) -> InversionAnalysis:
    """
    Determines the formal chord inversion and figured bass notation based on the lowest sounding pitch.
    
    Adheres strictly to Aldwell & Schachter (1989) and fixes ERR-006:
    The inversion is governed solely by which chord factor is in the bass,
    independent of the spacing or permutation of the upper voices.
    """
    if isinstance(notes, Voicing):
        midi_list = notes.midi_notes
    elif isinstance(notes, (list, tuple)):
        midi_list = list(notes)
    else:
        raise ChordConstructionError("Notes must be a list, tuple, or Voicing instance.")

    if not midi_list:
        raise ChordConstructionError("Cannot analyze inversion of an empty chord.")
    if any(type(n) is not int or isinstance(n, bool) or not 0 <= n <= 127 for n in midi_list):
        raise VoiceLeadingError("Notes must be valid MIDI integers in 0..127.")

    pcs = {n % 12 for n in midi_list}
    bass_note = min(midi_list)
    bass_pc = bass_note % 12

    if root_pitch_class is None:
        deduced_root, deduced_seventh = _deduce_triad_or_seventh_root(pcs)
        root_pc = deduced_root
        if is_seventh is None:
            is_seventh = deduced_seventh
    else:
        if type(root_pitch_class) is not int or isinstance(root_pitch_class, bool) or not 0 <= root_pitch_class <= 11:
            raise ChordConstructionError("root_pitch_class must be an integer in 0..11.")
        root_pc = root_pitch_class
        if is_seventh is None:
            is_seventh = len(pcs) >= 4

    # Distance from root to bass in semitones (0 = Root, 3/4 = Third, 6/7/8 = Fifth, 9/10/11 = Seventh)
    dist = (bass_pc - root_pc) % 12

    if dist == 0:
        inversion = ChordInversion.ROOT_POSITION
        bass_factor = "ROOT"
        if is_seventh:
            figured_bass = FiguredBassSymbol.SEVENTH_ROOT.value
            german_name = "Grundstellung (7)"
        else:
            figured_bass = FiguredBassSymbol.TRIAD_ROOT.value
            german_name = "Grundstellung (5/3)"
    elif dist in (3, 4):
        inversion = ChordInversion.FIRST_INVERSION
        bass_factor = "THIRD"
        if is_seventh:
            figured_bass = FiguredBassSymbol.SEVENTH_FIRST.value
            german_name = "1. Umkehrung (Quintsextakkord 6/5)"
        else:
            figured_bass = FiguredBassSymbol.TRIAD_FIRST.value
            german_name = "1. Umkehrung (Sextakkord 6)"
    elif dist in (6, 7, 8):
        inversion = ChordInversion.SECOND_INVERSION
        bass_factor = "FIFTH"
        if is_seventh:
            figured_bass = FiguredBassSymbol.SEVENTH_SECOND.value
            german_name = "2. Umkehrung (Terzquartakkord 4/3)"
        else:
            figured_bass = FiguredBassSymbol.TRIAD_SECOND.value
            german_name = "2. Umkehrung (Quartsextakkord 6/4)"
    elif dist in (9, 10, 11):
        inversion = ChordInversion.THIRD_INVERSION
        bass_factor = "SEVENTH"
        figured_bass = FiguredBassSymbol.SEVENTH_THIRD.value
        german_name = "3. Umkehrung (Sekundakkord 4/2)"
    else:
        # Non-chord tone / pedal point in bass
        inversion = ChordInversion.ROOT_POSITION
        bass_factor = "NON_CHORD_TONE"
        figured_bass = "slash"
        german_name = f"Orgelpunkt / Fremdbass ({dist})"

    return InversionAnalysis(
        inversion=inversion,
        figured_bass=figured_bass,
        bass_factor=bass_factor,
        root_pc=root_pc,
        bass_pc=bass_pc,
        german_name=german_name,
        is_seventh_chord=bool(is_seventh)
    )


def detect_hand_voicing(
    hand_notes: Union[List[int], Tuple[int, ...], Voicing],
    separate_bass_note: Optional[int] = None,
    root_pitch_class: Optional[int] = None
) -> dict[str, Any]:
    """
    Distinguishes the upper-hand voicing configuration from the overall global chord inversion.
    
    Crucial pedagogical distinction (M10/M12):
    A pianist playing C4-E4-G4 in the right hand over C2 in the left has a root-position hand voicing.
    Playing E4-G4-C5 over C2 has a 1st-inversion hand voicing (Sextakkord-Lage) within an overall root-position chord.
    """
    if isinstance(hand_notes, Voicing):
        hand_midi = hand_notes.midi_notes
    else:
        hand_midi = list(hand_notes)

    hand_analysis = detect_chord_inversion(hand_midi, root_pitch_class=root_pitch_class)

    if separate_bass_note is not None:
        total_notes = [separate_bass_note] + hand_midi
        overall_analysis = detect_chord_inversion(total_notes, root_pitch_class=root_pitch_class)
    else:
        overall_analysis = hand_analysis

    return {
        "hand_analysis": hand_analysis,
        "overall_analysis": overall_analysis,
        "is_hand_inverted": hand_analysis.inversion != ChordInversion.ROOT_POSITION,
        "is_overall_inverted": overall_analysis.inversion != ChordInversion.ROOT_POSITION,
        "hand_figured_bass": hand_analysis.figured_bass,
        "overall_figured_bass": overall_analysis.figured_bass
    }

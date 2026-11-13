"""
STEPS Music Theory Core: Seventh Chords, Extensions, Drop-2 & Shell Voicings.

Adheres to:
- M04 (Vierklänge, Alterationen, Drop-2, Shell Voicings, Rootless Voicings)
- Golden Reference Cases: REF-0013..0016, REF-0021, REF-0035, REF-0043, REF-0050, REF-0143..0147
- Mark Levine (1995): The Jazz Piano Book (Chapter on Drop-2 and Shell Voicings)
"""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple
from .pitch import PitchClass
from .chord import Voicing
from .exceptions import ChordConstructionError

class SeventhQuality(Enum):
    DOMINANT_SEVENTH = 'DOMINANT_SEVENTH'      # 7: [0, 4, 7, 10]
    MAJOR_SEVENTH = 'MAJOR_SEVENTH'              # maj7: [0, 4, 7, 11]
    MINOR_SEVENTH = 'MINOR_SEVENTH'              # m7: [0, 3, 7, 10]
    HALF_DIMINISHED = 'HALF_DIMINISHED'          # m7b5: [0, 3, 6, 10]
    DIMINISHED_SEVENTH = 'DIMINISHED_SEVENTH'    # dim7: [0, 3, 6, 9]
    MINOR_MAJOR_SEVENTH = 'MINOR_MAJOR_SEVENTH'  # m(maj7): [0, 3, 7, 11]
    LYDIAN_DOMINANT = 'LYDIAN_DOMINANT'          # 7(#11): theoretical [0, 4, 7, 10, 18] or voiced [0, 4, 6, 10]


# Canonical 4-voice interval structures from root in semitones
SEVENTH_INTERVALS: dict[SeventhQuality, list[int]] = {
    SeventhQuality.DOMINANT_SEVENTH: [0, 4, 7, 10],
    SeventhQuality.MAJOR_SEVENTH: [0, 4, 7, 11],
    SeventhQuality.MINOR_SEVENTH: [0, 3, 7, 10],
    SeventhQuality.HALF_DIMINISHED: [0, 3, 6, 10],
    SeventhQuality.DIMINISHED_SEVENTH: [0, 3, 6, 9],
    SeventhQuality.MINOR_MAJOR_SEVENTH: [0, 3, 7, 11],
    SeventhQuality.LYDIAN_DOMINANT: [0, 4, 6, 10]  # Standard 4-voice performance voicing (5th omitted)
}

# Complete theoretical pitch class intervals including all extensions
THEORETICAL_INTERVALS: dict[SeventhQuality, list[int]] = {
    SeventhQuality.DOMINANT_SEVENTH: [0, 4, 7, 10],
    SeventhQuality.MAJOR_SEVENTH: [0, 4, 7, 11],
    SeventhQuality.MINOR_SEVENTH: [0, 3, 7, 10],
    SeventhQuality.HALF_DIMINISHED: [0, 3, 6, 10],
    SeventhQuality.DIMINISHED_SEVENTH: [0, 3, 6, 9],
    SeventhQuality.MINOR_MAJOR_SEVENTH: [0, 3, 7, 11],
    SeventhQuality.LYDIAN_DOMINANT: [0, 4, 7, 10, 18]  # 1, 3, 5, b7, #11
}


def construct_seventh(
    root: int | PitchClass,
    quality: SeventhQuality,
    full_theoretical: bool = False
) -> list[PitchClass]:
    """
    Constructs pitch class list for a seventh chord.
    
    If full_theoretical is True, includes optional unvoiced scale degrees
    (e.g. natural 5th in Lydian Dominant 7#11).
    """
    if quality not in SEVENTH_INTERVALS:
        raise ChordConstructionError(f"Unknown seventh chord quality: {quality}")
    r = int(root) % 12
    intervals = THEORETICAL_INTERVALS[quality] if full_theoretical else SEVENTH_INTERVALS[quality]
    return [PitchClass(r + semi) for semi in intervals]


def invert_seventh_voicing(voicing_midi: list[int], inversion: int) -> list[int]:
    """
    Permutes a 4-note seventh chord voicing:
    inversion 0: Root position (7)
    inversion 1: 1st inversion (6/5, 3rd in bass)
    inversion 2: 2nd inversion (4/3, 5th in bass)
    inversion 3: 3rd inversion (4/2, 7th in bass)
    """
    if len(voicing_midi) != 4 or type(inversion) is not int or not 0 <= inversion <= 3:
        raise ChordConstructionError("Seventh chord inversion requires four voices and an inversion in 0..3.")
    return Voicing(tuple(voicing_midi)).invert(inversion).midi_notes


def make_drop2_voicing(close_voicing_midi: list[int]) -> list[int]:
    """
    Transforms a 4-voice close position voicing into Drop-2:
    The second voice from the top drops by an octave (-12 semitones).
    
    Example:
        Close Dm7 [F4, A4, C5, D5] -> voice 2 from top is C5 (index 2).
        Drop-2 -> [C4, F4, A4, D5].
    """
    if len(close_voicing_midi) != 4:
        raise ChordConstructionError("Drop-2 voicing transformation requires exactly 4 voices.")
    v0, v1, v2, v3 = Voicing(tuple(close_voicing_midi)).midi_notes
    if len({v0, v1, v2, v3}) != 4 or v3 - v0 >= 12:
        raise ChordConstructionError("Drop-2 requires four distinct notes in close position.")
    return Voicing((v0, v1, v2 - 12, v3), "DROP2").midi_notes


def make_shell_voicing(root_midi: int, quality: SeventhQuality) -> tuple[int, tuple[int, int]]:
    """
    Creates a standard two-handed shell voicing:
    Left hand: Root note (bass).
    Right hand: Guide tones (3rd & 7th).
    
    Returns:
        (lh_root_midi, (rh_third_midi, rh_seventh_midi))
    """
    if quality not in SEVENTH_INTERVALS:
        raise ChordConstructionError(f"Unknown seventh chord quality: {quality}")
    Voicing((root_midi,))
    r_pc = root_midi % 12
    intervals = SEVENTH_INTERVALS[quality]
    third_pc = intervals[1]
    seventh_pc = intervals[3]
    
    floor = max(60, root_midi + 1)
    rh_third = floor + (r_pc + third_pc - floor) % 12
    rh_seventh = floor + (r_pc + seventh_pc - floor) % 12
    Voicing((root_midi, rh_third, rh_seventh))
    
    return (root_midi, (rh_third, rh_seventh))


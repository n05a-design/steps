"""
STEPS Music Theory Core: Seventh Chords, Extensions, Drop-2 & Shell Voicings.

Adheres to:
- M04 (Vierklänge, Alterationen, Drop-2, Shell Voicings, Rootless Voicings)
- Golden Reference Cases: REF-0013..0016, REF-0021, REF-0035, REF-0043, REF-0050, REF-0143..0147
"""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple
from .pitch import PitchClass

class SeventhQuality(Enum):
    DOMINANT_SEVENTH = 'DOMINANT_SEVENTH'      # 7: [0, 4, 7, 10]
    MAJOR_SEVENTH = 'MAJOR_SEVENTH'              # maj7: [0, 4, 7, 11]
    MINOR_SEVENTH = 'MINOR_SEVENTH'              # m7: [0, 3, 7, 10]
    HALF_DIMINISHED = 'HALF_DIMINISHED'          # m7b5: [0, 3, 6, 10]
    DIMINISHED_SEVENTH = 'DIMINISHED_SEVENTH'    # dim7: [0, 3, 6, 9]
    MINOR_MAJOR_SEVENTH = 'MINOR_MAJOR_SEVENTH'  # m(maj7): [0, 3, 7, 11]
    LYDIAN_DOMINANT = 'LYDIAN_DOMINANT'          # 7(#11): [0, 4, 6, 10]


SEVENTH_INTERVALS: dict[SeventhQuality, list[int]] = {
    SeventhQuality.DOMINANT_SEVENTH: [0, 4, 7, 10],
    SeventhQuality.MAJOR_SEVENTH: [0, 4, 7, 11],
    SeventhQuality.MINOR_SEVENTH: [0, 3, 7, 10],
    SeventhQuality.HALF_DIMINISHED: [0, 3, 6, 10],
    SeventhQuality.DIMINISHED_SEVENTH: [0, 3, 6, 9],
    SeventhQuality.MINOR_MAJOR_SEVENTH: [0, 3, 7, 11],
    SeventhQuality.LYDIAN_DOMINANT: [0, 4, 6, 10]  # Tritone #11 (6 semitones) replaces or extends 5th
}


def construct_seventh(root: int | PitchClass, quality: SeventhQuality) -> list[PitchClass]:
    """Constructs pitch class list for a seventh chord."""
    r = int(root) % 12
    intervals = SEVENTH_INTERVALS[quality]
    return [PitchClass(r + semi) for semi in intervals]


def invert_seventh_voicing(voicing_midi: list[int], inversion: int) -> list[int]:
    """
    Permutes a 4-note seventh chord voicing:
    inversion 0: Root position (7)
    inversion 1: 1st inversion (6/5, 3rd in bass)
    inversion 2: 2nd inversion (4/3, 5th in bass)
    inversion 3: 3rd inversion (4/2, 7th in bass)
    """
    if len(voicing_midi) < 4:
        raise ValueError("Seventh chord voicing must have at least 4 voices.")
    inv = inversion % len(voicing_midi)
    if inv == 0:
        return sorted(voicing_midi)
    
    sorted_v = sorted(voicing_midi)
    return sorted_v[inv:] + [pitch + 12 for pitch in sorted_v[:inv]]


def make_drop2_voicing(close_voicing_midi: list[int]) -> list[int]:
    """
    Transforms a 4-voice close position voicing into Drop-2:
    The second voice from the top drops by an octave (-12 semitones).
    
    Example:
        Close Dm7 [F4, A4, C5, D5] -> voice 2 from top is C5 (index 2).
        Drop-2 -> [C4, F4, A4, D5].
    """
    if len(close_voicing_midi) != 4:
        raise ValueError("Drop-2 voicing transformation requires exactly 4 voices.")
    sorted_v = sorted(close_voicing_midi)
    # Voices from bottom to top: v0 (lowest), v1, v2 (second from top), v3 (highest)
    v0, v1, v2, v3 = sorted_v
    dropped_v2 = v2 - 12
    return sorted([v0, v1, dropped_v2, v3])


def make_shell_voicing(root_midi: int, quality: SeventhQuality) -> tuple[int, tuple[int, int]]:
    """
    Creates a standard two-handed shell voicing:
    Left hand: Root note (bass).
    Right hand: Guide tones (3rd & 7th).
    
    Returns:
        (lh_root_midi, (rh_third_midi, rh_seventh_midi))
    """
    r_pc = root_midi % 12
    intervals = SEVENTH_INTERVALS[quality]
    third_pc = intervals[1]
    seventh_pc = intervals[3]
    
    # Place guide tones in octave 4 (around middle C)
    rh_third = 60 + ((r_pc + third_pc) % 12)
    rh_seventh = 60 + ((r_pc + seventh_pc) % 12)
    
    return (root_midi, (rh_third, rh_seventh))

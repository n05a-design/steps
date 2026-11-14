"""
STEPS Music Theory Core: Triad Construction, Qualities & Inversions.

Adheres to:
- M04 (Dreiklänge, Terzschichtung, Sus- und Add-Akkorde)
- Golden Reference Cases: REF-0012, REF-0039, REF-0040, REF-0049, REF-0138..0142
"""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple
from .pitch import PitchClass
from .chord import Voicing
from .exceptions import ChordConstructionError

class TriadQuality(Enum):
    MAJOR = 'MAJOR'
    MINOR = 'MINOR'
    DIMINISHED = 'DIMINISHED'
    AUGMENTED = 'AUGMENTED'
    SUS4 = 'SUS4'
    SUS2 = 'SUS2'
    ADD9 = 'ADD9'


# Canonical interval structures from root in semitones
TRIAD_INTERVALS: dict[TriadQuality, list[int]] = {
    TriadQuality.MAJOR: [0, 4, 7],
    TriadQuality.MINOR: [0, 3, 7],
    TriadQuality.DIMINISHED: [0, 3, 6],
    TriadQuality.AUGMENTED: [0, 4, 8],
    TriadQuality.SUS4: [0, 5, 7],
    TriadQuality.SUS2: [0, 2, 7],
    TriadQuality.ADD9: [0, 2, 4, 7]
}


def construct_triad(root: int | PitchClass, quality: TriadQuality) -> list[PitchClass]:
    """
    Constructs the pitch class list for a triad of given root and quality.
    
    Example:
        construct_triad(0, TriadQuality.MAJOR) -> [PitchClass(0), PitchClass(4), PitchClass(7)]
        construct_triad(0, TriadQuality.SUS4) -> [PitchClass(0), PitchClass(5), PitchClass(7)]
    """
    if quality not in TRIAD_INTERVALS:
        raise ChordConstructionError(f"Unknown triad quality: {quality}")
    r = int(root) % 12
    intervals = TRIAD_INTERVALS[quality]
    return [PitchClass(r + semi) for semi in intervals]


def invert_triad_voicing(voicing_midi: list[int], inversion: int) -> list[int]:
    """
    Permutes a concrete triad voicing into its designated inversion.
    
    inversion 0: Root position (e.g. [C4, E4, G4] = [60, 64, 67])
    inversion 1: 1st inversion (6/3, bass note is 3rd, e.g. [E4, G4, C5] = [64, 67, 72])
    inversion 2: 2nd inversion (6/4, bass note is 5th, e.g. [G4, C5, E5] = [67, 72, 76])
    """
    if len(voicing_midi) != 3 or type(inversion) is not int or not 0 <= inversion <= 2:
        raise ChordConstructionError("Triad inversion requires three voices and an inversion in 0..2.")
    return Voicing(tuple(voicing_midi)).invert(inversion).midi_notes


def get_triad_pitch_class_set(root: int | PitchClass, quality: TriadQuality) -> set[int]:
    """Returns the set of integers in Z12 belonging to the triad."""
    return {int(pc) for pc in construct_triad(root, quality)}


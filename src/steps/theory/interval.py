"""
STEPS Music Theory Core: Interval Arithmetics & Inversions.

Adheres to:
- M01 (Intervalldistanzen & Inversionen), M03 (Skalen-Schritte)
- Mathematical Invariant: interval + invert(interval) == 0 mod 12
- Separation of Chromatic Semitone Distance from Diatonic Interval Quality
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Literal, Tuple

class ChromaticInterval(IntEnum):
    """Standard chromatic intervals in semitones within the octave."""
    PERFECT_UNISON = 0
    MINOR_SECOND = 1
    MAJOR_SECOND = 2
    MINOR_THIRD = 3
    MAJOR_THIRD = 4
    PERFECT_FOURTH = 5
    TRITONE = 6
    PERFECT_FIFTH = 7
    MINOR_SIXTH = 8
    MAJOR_SIXTH = 9
    MINOR_SEVENTH = 10
    MAJOR_SEVENTH = 11
    PERFECT_OCTAVE = 12


IntervalQuality = Literal['P', 'M', 'm', 'd', 'A']


@dataclass(frozen=True)
class DiatonicInterval:
    """
    Represents a diatonic interval with scale-step degree and quality.
    
    Attributes:
        number: Diatonic span (1=Unison, 2=Second, 3=Third, 4=Fourth, 5=Fifth, 6=Sixth, 7=Seventh, 8=Octave).
        quality: 'P' (Perfect), 'M' (Major), 'm' (Minor), 'd' (Diminished), 'A' (Augmented).
    """
    number: int
    quality: IntervalQuality

    def __post_init__(self):
        if self.number < 1:
            raise ValueError("Interval number must be >= 1.")
        # Perfect intervals can only be 1, 4, 5, 8, 11, 12, etc.
        simple_num = (self.number - 1) % 7 + 1
        if simple_num in (1, 4, 5):
            if self.quality in ('M', 'm'):
                raise ValueError(f"Interval {self.number} is perfect-type and cannot be Major ('M') or Minor ('m').")
        else:
            if self.quality == 'P':
                raise ValueError(f"Interval {self.number} is imperfect-type and cannot be Perfect ('P').")

    @property
    def semitones(self) -> int:
        """Calculates semitones for the diatonic interval."""
        simple_num = (self.number - 1) % 7 + 1
        octaves = (self.number - 1) // 7
        
        # Base diatonic major/perfect sizes in semitones
        base_semitones = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
        base = base_semitones[simple_num]
        
        if simple_num in (1, 4, 5):
            if self.quality == 'P':
                delta = 0
            elif self.quality == 'A':
                delta = 1
            elif self.quality == 'd':
                delta = -1
            else:
                raise ValueError(f"Invalid quality {self.quality} for perfect interval.")
        else:
            if self.quality == 'M':
                delta = 0
            elif self.quality == 'm':
                delta = -1
            elif self.quality == 'A':
                delta = 1
            elif self.quality == 'd':
                delta = -2
            else:
                raise ValueError(f"Invalid quality {self.quality} for major/minor interval.")
                
        return octaves * 12 + base + delta

    def invert(self) -> DiatonicInterval:
        """Inverts a simple diatonic interval (within octave)."""
        if self.number > 8:
            raise ValueError("Direct diatonic inversion is defined for simple intervals <= 8.")
        inv_num = 9 - self.number
        quality_map: dict[IntervalQuality, IntervalQuality] = {
            'P': 'P',
            'M': 'm',
            'm': 'M',
            'A': 'd',
            'd': 'A'
        }
        return DiatonicInterval(number=inv_num, quality=quality_map[self.quality])


def semitones_between(note_a: int, note_b: int) -> int:
    """Computes absolute semitone distance between two pitches: |note_b - note_a|."""
    return abs(note_b - note_a)


def directed_semitones(note_from: int, note_to: int) -> int:
    """Computes directed semitone difference: note_to - note_from."""
    return note_to - note_from


def invert_semitones_modulo12(semitones: int) -> int:
    """
    Computes modular interval inversion in Z12.
    Formula: (12 - (s mod 12)) mod 12.
    """
    return (12 - (semitones % 12)) % 12

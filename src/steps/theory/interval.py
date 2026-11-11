"""
STEPS Music Theory Core: Interval Arithmetics, Transpositions & Inversions.

Adheres to:
- M01 (Intervalldistanzen & Inversionen), M03 (Skalen-Schritte)
- Mathematical Invariant: interval + invert(interval) == 0 mod 12
- Separation of Chromatic Semitone Distance from Diatonic Interval Quality
"""

from __future__ import annotations
from dataclasses import dataclass
from enum import IntEnum
from typing import Literal, Tuple

from .exceptions import InvalidIntervalError, MusicTheoryError
from .pitch import NoteSpelling, DIATONIC_STEPS, DIATONIC_BASE_PC


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
    # Compound extensions
    MINOR_NINTH = 13
    MAJOR_NINTH = 14
    AUGMENTED_NINTH = 15
    PERFECT_ELEVENTH = 17
    AUGMENTED_ELEVENTH = 18
    MINOR_THIRTEENTH = 20
    MAJOR_THIRTEENTH = 21


IntervalQuality = Literal['P', 'M', 'm', 'd', 'A']


@dataclass(frozen=True)
class DiatonicInterval:
    """
    Represents a diatonic interval with scale-step degree, quality, and direction.
    
    Attributes:
        number: Diatonic span (1=Unison, 2=Second, 3=Third, 4=Fourth, 5=Fifth, 6=Sixth, 7=Seventh, 8=Octave,
                9=Ninth, 11=Eleventh, 13=Thirteenth, etc.).
        quality: 'P' (Perfect), 'M' (Major), 'm' (Minor), 'd' (Diminished), 'A' (Augmented).
        direction: 1 for ascending (default), -1 for descending.
    """
    number: int
    quality: IntervalQuality
    direction: Literal[1, -1] = 1

    def __post_init__(self):
        if self.number < 1:
            raise InvalidIntervalError("Interval number must be >= 1.")
        if self.direction not in (1, -1):
            raise InvalidIntervalError("Interval direction must be +1 (ascending) or -1 (descending).")
            
        # Perfect intervals: 1, 4, 5 and their compound octaves (8, 11, 12, 15, etc.)
        simple_num = (self.number - 1) % 7 + 1
        if simple_num in (1, 4, 5):
            if self.quality in ('M', 'm'):
                raise InvalidIntervalError(
                    f"Interval {self.number} is perfect-type and cannot be Major ('M') or Minor ('m')."
                )
        else:
            if self.quality == 'P':
                raise InvalidIntervalError(
                    f"Interval {self.number} is imperfect-type and cannot be Perfect ('P')."
                )

    @property
    def is_compound(self) -> bool:
        """Returns True if interval spans more than an octave (> 8)."""
        return self.number > 8

    @property
    def octaves(self) -> int:
        """Returns the number of whole octaves spanned."""
        return (self.number - 1) // 7

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
                raise InvalidIntervalError(f"Invalid quality {self.quality} for perfect interval.")
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
                raise InvalidIntervalError(f"Invalid quality {self.quality} for major/minor interval.")
                
        return octaves * 12 + base + delta

    @property
    def signed_semitones(self) -> int:
        """Returns signed semitones (+ for ascending, - for descending)."""
        return self.direction * self.semitones

    def invert(self) -> DiatonicInterval:
        """
        Inverts a simple diatonic interval (within octave).
        Rule: 9 - number, opposite quality (M <-> m, A <-> d, P <-> P).
        """
        if self.number > 8:
            raise InvalidIntervalError("Direct diatonic inversion is defined for simple intervals <= 8.")
        inv_num = 9 - self.number
        quality_map: dict[IntervalQuality, IntervalQuality] = {
            'P': 'P',
            'M': 'm',
            'm': 'M',
            'A': 'd',
            'd': 'A'
        }
        return DiatonicInterval(number=inv_num, quality=quality_map[self.quality], direction=self.direction)


def transpose_spelling(
    spelling: NoteSpelling,
    interval: DiatonicInterval,
    direction: Literal[1, -1] = 1
) -> NoteSpelling:
    """
    Transposes a NoteSpelling by a DiatonicInterval, preserving strict orthography and accidentals.
    
    Examples:
        C4 + DiatonicInterval(5, 'P') -> G4
        C4 + DiatonicInterval(4, 'A') -> F#4
        C4 + DiatonicInterval(5, 'd') -> Gb4
        C4 + DiatonicInterval(5, 'P', direction=-1) -> F3
    """
    effective_dir = interval.direction * direction
    step_delta = effective_dir * (interval.number - 1)
    semi_delta = effective_dir * interval.semitones
    return spelling.transpose_diatonic(step_delta=step_delta, semitone_delta=semi_delta)


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


def interval_between_spellings(spelling_a: NoteSpelling, spelling_b: NoteSpelling) -> DiatonicInterval:
    """
    Calculates the exact DiatonicInterval from spelling_a to spelling_b.
    """
    idx_a = DIATONIC_STEPS.index(spelling_a.step)
    idx_b = DIATONIC_STEPS.index(spelling_b.step)
    
    midi_diff = spelling_b.midi_number - spelling_a.midi_number
    direction: Literal[1, -1] = 1 if midi_diff >= 0 else -1
    
    if direction == 1:
        step_diff = (idx_b - idx_a) + (spelling_b.octave - spelling_a.octave) * 7
        semi_diff = midi_diff
    else:
        step_diff = (idx_a - idx_b) + (spelling_a.octave - spelling_b.octave) * 7
        semi_diff = -midi_diff
        
    number = step_diff + 1
    if number < 1:
        raise InvalidIntervalError("Unable to calculate diatonic interval for negative diatonic span.")
        
    simple_num = (number - 1) % 7 + 1
    octaves = (number - 1) // 7
    base_semitones = {1: 0, 2: 2, 3: 4, 4: 5, 5: 7, 6: 9, 7: 11}
    base = octaves * 12 + base_semitones[simple_num]
    delta = semi_diff - base
    
    if simple_num in (1, 4, 5):
        if delta == 0:
            quality: IntervalQuality = 'P'
        elif delta == 1:
            quality = 'A'
        elif delta == -1:
            quality = 'd'
        else:
            raise InvalidIntervalError(f"Unsupported alteration delta {delta} for perfect interval.")
    else:
        if delta == 0:
            quality = 'M'
        elif delta == -1:
            quality = 'm'
        elif delta == 1:
            quality = 'A'
        elif delta == -2:
            quality = 'd'
        else:
            raise InvalidIntervalError(f"Unsupported alteration delta {delta} for major/minor interval.")
            
    return DiatonicInterval(number=number, quality=quality, direction=direction)


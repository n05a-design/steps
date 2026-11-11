"""
STEPS Music Theory Core: Pitch, PitchClass & NoteSpelling.

Adheres to:
- M01 (Akustik & Frequenzen), M02 (Enharmonik & Notationskonventionen)
- ISO 16:1975 standard tuning (A4 = 440 Hz)
- MIDI 1.0 detailed specification (Middle C = C4 = MIDI 60)
- ADR-005: Separation of Chromatic PitchClass (Z12) from Diatonic NoteSpelling
"""

from __future__ import annotations
from dataclasses import dataclass
from typing import Literal, Optional, Tuple, Dict

# Standard frequency reference for A4
A4_STANDARD_FREQ: float = 440.0
A4_MIDI_NOTE: int = 69
MIDDLE_C_MIDI_NOTE: int = 60

# Base diatonic pitch classes (C-major scale basis)
DIATONIC_BASE_PC: Dict[str, int] = {
    'C': 0,
    'D': 2,
    'E': 4,
    'F': 5,
    'G': 7,
    'A': 9,
    'B': 11,
}

# Diatonic steps order
DIATONIC_STEPS = ('C', 'D', 'E', 'F', 'G', 'A', 'B')

# Alteration semitone mappings
ALTERATION_SEMITONES: Dict[str, int] = {
    'bb': -2,
    'b': -1,
    'n': 0,
    '': 0,
    '#': 1,
    'x': 2,
    '##': 2
}

# Unicode symbols
UNICODE_ACCIDENTALS: Dict[int, str] = {
    -2: '𝄫',
    -1: '♭',
    0: '♮',
    1: '♯',
    2: '𝄪'
}

ASCII_ACCIDENTALS: Dict[int, str] = {
    -2: 'bb',
    -1: 'b',
    0: '',
    1: '#',
    2: 'x'
}


class PitchClass(int):
    """
    Represents an integer in Z_12 (0..11) corresponding to chromatic pitch class modulo 12.
    0 = C, 1 = C#/Db, 2 = D, ..., 11 = B/H.
    """
    def __new__(cls, val: int):
        return super().__new__(cls, val % 12)

    def __repr__(self) -> str:
        return f"PitchClass({int(self)})"

    def __add__(self, other: int) -> PitchClass:
        return PitchClass(super().__add__(other))

    def __sub__(self, other: int) -> PitchClass:
        return PitchClass(super().__sub__(other))


@dataclass(frozen=True)
class NoteSpelling:
    """
    Orthographic diatonic spelling of a pitch, preserving enharmonic distinction.
    
    Attributes:
        step: Diatonic letter name ('C', 'D', 'E', 'F', 'G', 'A', 'B').
        alteration: Semitone shift (-2 for double flat, -1 for flat, 0 for natural, +1 for sharp, +2 for double sharp).
        octave: Integer octave number in Scientific Pitch Notation (e.g. 4 for Middle C).
    """
    step: Literal['C', 'D', 'E', 'F', 'G', 'A', 'B']
    alteration: int = 0
    octave: int = 4

    def __post_init__(self):
        if self.step not in DIATONIC_BASE_PC:
            raise ValueError(f"Invalid diatonic step: '{self.step}'. Must be one of {DIATONIC_STEPS}.")
        if self.alteration not in (-2, -1, 0, 1, 2):
            raise ValueError(f"Alteration must be between -2 and +2, got {self.alteration}.")

    @property
    def pitch_class(self) -> PitchClass:
        """Returns the modulo-12 chromatic pitch class."""
        base = DIATONIC_BASE_PC[self.step]
        return PitchClass(base + self.alteration)

    @property
    def midi_number(self) -> int:
        """
        Calculates the standard MIDI note number (C4 = 60).
        midi = (octave + 1) * 12 + base_pc + alteration
        """
        base = DIATONIC_BASE_PC[self.step]
        midi = (self.octave + 1) * 12 + base + self.alteration
        if not (0 <= midi <= 127):
            raise ValueError(f"Calculated MIDI note {midi} out of standard range [0..127].")
        return midi

    @property
    def frequency(self) -> float:
        """Calculates frequency in Hz according to ISO 16 (A4 = 440 Hz)."""
        return midi_to_frequency(self.midi_number)

    def render(self, convention: Literal['INT', 'DE'] = 'INT', unicode_accidental: bool = False) -> str:
        """
        Renders the note spelling as a string under International or German convention.
        
        International:
          B natural -> B
          B flat    -> Bb
        German:
          B natural -> H
          B flat    -> B
          E flat    -> Es
          A flat    -> As
          F sharp   -> Fis
          F double sharp -> Fisis
        """
        if convention == 'DE':
            return self._render_german()
        else:
            return self._render_international(unicode_accidental)

    def _render_international(self, unicode_acc: bool = False) -> str:
        acc = UNICODE_ACCIDENTALS[self.alteration] if unicode_acc else ASCII_ACCIDENTALS[self.alteration]
        return f"{self.step}{acc}{self.octave}"

    def _render_german(self) -> str:
        # German special cases for B / H
        if self.step == 'B':
            if self.alteration == 0:
                base_str = 'H'
            elif self.alteration == -1:
                base_str = 'B'
            elif self.alteration == -2:
                base_str = 'Heses'
            elif self.alteration == 1:
                base_str = 'His'
            elif self.alteration == 2:
                base_str = 'Hisis'
            return f"{base_str}{self.octave}"
        
        # General German suffixes: -is for sharp, -es for flat (with contraction for Es, As)
        s = self.step
        if self.alteration == 0:
            return f"{s}{self.octave}"
        elif self.alteration == 1:
            return f"{s}is{self.octave}"
        elif self.alteration == 2:
            return f"{s}isis{self.octave}"
        elif self.alteration == -1:
            if s in ('E', 'A'):
                return f"{s}s{self.octave}"
            return f"{s}es{self.octave}"
        elif self.alteration == -2:
            if s in ('E', 'A'):
                return f"{s}ses{self.octave}"
            return f"{s}eses{self.octave}"
        return f"{s}{self.octave}"


def midi_to_pitch_class(midi_note: int) -> PitchClass:
    """Computes pitch class p = m mod 12."""
    if not (0 <= midi_note <= 127):
        raise ValueError(f"MIDI note {midi_note} out of standard range [0..127].")
    return PitchClass(midi_note % 12)


def midi_to_frequency(midi_note: int, a4_ref: float = A4_STANDARD_FREQ) -> float:
    """Computes exact ISO 16 frequency: f = a4_ref * 2^((m - 69) / 12)."""
    return a4_ref * (2.0 ** ((midi_note - A4_MIDI_NOTE) / 12.0))


def frequency_to_midi(freq: float, a4_ref: float = A4_STANDARD_FREQ) -> float:
    """Computes fractional MIDI note from frequency: m = 69 + 12 * log2(f / a4_ref)."""
    import math
    if freq <= 0:
        raise ValueError("Frequency must be positive.")
    return 69.0 + 12.0 * math.log2(freq / a4_ref)


def parse_spelling(note_str: str) -> NoteSpelling:
    """
    Parses a scientific pitch notation string (e.g. 'C4', 'C#4', 'Db3', 'F##5', 'Bb2', 'Fx4').
    """
    import re
    m = re.match(r"^([A-Ga-g])(bb|b|##|#|x|n)?(-?\d+)?$", note_str.strip())
    if not m:
        raise ValueError(f"Cannot parse note string: '{note_str}'")
    step = m.group(1).upper()
    acc_str = m.group(2) or ''
    oct_str = m.group(3)
    octave = int(oct_str) if oct_str is not None else 4
    alteration = ALTERATION_SEMITONES.get(acc_str.lower(), 0)
    return NoteSpelling(step=step, alteration=alteration, octave=octave)  # type: ignore

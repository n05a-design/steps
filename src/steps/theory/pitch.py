"""
STEPS Music Theory Core: Pitch, PitchClass & NoteSpelling.

Adheres to:
- M01 (Akustik & Frequenzen), M02 (Enharmonik & Notationskonventionen)
- ISO 16:1975 standard tuning (A4 = 440 Hz)
- MIDI 1.0 detailed specification (Middle C = C4 = MIDI 60)
- ADR-005: Separation of Chromatic PitchClass (Z12) from Diatonic NoteSpelling
"""

from __future__ import annotations
import math
import re
from dataclasses import dataclass
from typing import Literal, Optional, Tuple, Dict

from .exceptions import (
    MusicTheoryError,
    InvalidPitchClassError,
    InvalidDiatonicStepError,
    InvalidAlterationError,
    PitchRangeError,
)

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

# German alteration suffixes mappings
GERMAN_SUFFIX_SEMITONES: Dict[str, int] = {
    'eses': -2,
    'ses': -2,
    'es': -1,
    's': -1,
    '': 0,
    'is': 1,
    'isis': 2
}

# Unicode symbols
UNICODE_ACCIDENTALS: Dict[int, str] = {
    -2: '𝄫',
    -1: '♭',
    0: '',
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
        if isinstance(val, bool) or not isinstance(val, int):
            raise InvalidPitchClassError(f"PitchClass value must be integer, got {type(val).__name__}")
        return super().__new__(cls, int(val) % 12)

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
        if not isinstance(self.step, str) or self.step not in DIATONIC_BASE_PC:
            raise InvalidDiatonicStepError(
                f"Invalid diatonic step: '{self.step}'. Must be one of {DIATONIC_STEPS}."
            )
        if type(self.alteration) is not int or not -2 <= self.alteration <= 2:
            raise InvalidAlterationError(
                f"Alteration must be an integer between -2 and +2, got {self.alteration}."
            )

        if type(self.octave) is not int:
            raise PitchRangeError("Octave must be an integer.")

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
            raise PitchRangeError(f"Calculated MIDI note {midi} out of standard range [0..127].")
        return midi

    @property
    def frequency(self) -> float:
        """Calculates frequency in Hz according to ISO 16 (A4 = 440 Hz)."""
        return midi_to_frequency(self.midi_number)

    def is_enharmonic_with(self, other: NoteSpelling, ignore_octave: bool = False) -> bool:
        """
        Tests if this spelling represents the exact same sounding pitch as other.
        If ignore_octave is True, compares pitch classes (modulo 12).
        Otherwise, compares exact MIDI note numbers.
        """
        if ignore_octave:
            return self.pitch_class == other.pitch_class
        return self.midi_number == other.midi_number

    def transpose_diatonic(self, step_delta: int, semitone_delta: int) -> NoteSpelling:
        """
        Transposes this note spelling by a diatonic step offset and semitone offset.
        Calculates the correct resulting diatonic step, alteration, and octave.
        
        Example:
            C4.transpose_diatonic(step_delta=4, semitone_delta=7) -> G4 (Perfect 5th)
            C4.transpose_diatonic(step_delta=3, semitone_delta=6) -> F#4 (Augmented 4th)
            C4.transpose_diatonic(step_delta=4, semitone_delta=6) -> Gb4 (Diminished 5th)
        """
        if type(step_delta) is not int or type(semitone_delta) is not int:
            raise MusicTheoryError("Diatonic transposition requires whole steps and semitones.")
        current_idx = DIATONIC_STEPS.index(self.step)
        target_idx_unbounded = current_idx + step_delta
        target_step = DIATONIC_STEPS[target_idx_unbounded % 7]
        
        # Diatonic octave shift based on scale-step wrapping (C-based)
        diatonic_octave_shift = target_idx_unbounded // 7
        target_octave = self.octave + diatonic_octave_shift
        
        target_midi = self.midi_number + semitone_delta
        target_base_midi = (target_octave + 1) * 12 + DIATONIC_BASE_PC[target_step]
        
        needed_alteration = target_midi - target_base_midi
        
        # If alteration exceeds -2..+2, adjust octave by +/-1 if possible
        if needed_alteration < -2:
            target_octave -= 1
            target_base_midi = (target_octave + 1) * 12 + DIATONIC_BASE_PC[target_step]
            needed_alteration = target_midi - target_base_midi
        elif needed_alteration > 2:
            target_octave += 1
            target_base_midi = (target_octave + 1) * 12 + DIATONIC_BASE_PC[target_step]
            needed_alteration = target_midi - target_base_midi
            
        if needed_alteration not in (-2, -1, 0, 1, 2):
            raise InvalidAlterationError(
                f"Diatonic transposition resulting alteration {needed_alteration} exceeds valid range [-2, 2]."
            )
            
        return NoteSpelling(step=target_step, alteration=needed_alteration, octave=target_octave)  # type: ignore

    def transpose_chromatic(self, semitones: int) -> NoteSpelling:
        """
        Transposes chromatically by the specified number of semitones.
        Prefers standard circle-of-fifths spellings with simple alterations.
        """
        if type(semitones) is not int:
            raise MusicTheoryError("Chromatic transposition requires whole semitones.")
        new_midi = self.midi_number + semitones
        if not (0 <= new_midi <= 127):
            raise PitchRangeError(f"Transposed MIDI note {new_midi} out of range [0..127].")
            
        target_pc = new_midi % 12
        target_oct = (new_midi // 12) - 1
        
        # Standard preferred spelling for each pitch class
        preferred: Dict[int, Tuple[str, int]] = {
            0: ('C', 0),
            1: ('C', 1) if self.alteration >= 0 else ('D', -1),
            2: ('D', 0),
            3: ('E', -1) if self.alteration <= 0 else ('D', 1),
            4: ('E', 0),
            5: ('F', 0),
            6: ('F', 1) if self.alteration >= 0 else ('G', -1),
            7: ('G', 0),
            8: ('A', -1) if self.alteration <= 0 else ('G', 1),
            9: ('A', 0),
            10: ('B', -1) if self.alteration <= 0 else ('A', 1),
            11: ('B', 0)
        }
        step, alt = preferred[target_pc]
        # Re-verify exact octave
        calc_midi = (target_oct + 1) * 12 + DIATONIC_BASE_PC[step] + alt
        if calc_midi < new_midi:
            target_oct += 1
        elif calc_midi > new_midi:
            target_oct -= 1
        return NoteSpelling(step=step, alteration=alt, octave=target_oct)  # type: ignore

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
        if convention == 'INT':
            return self._render_international(unicode_accidental)
        raise MusicTheoryError(f"Unknown notation convention: {convention!r}.")

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
    if isinstance(midi_note, bool) or not isinstance(midi_note, int) or not 0 <= midi_note <= 127:
        raise PitchRangeError(f"MIDI note {midi_note} out of standard range [0..127].")
    return PitchClass(midi_note % 12)


def midi_to_frequency(midi_note: int | float, a4_ref: float = A4_STANDARD_FREQ) -> float:
    """Convert a MIDI position, including a fractional position, to frequency."""
    if isinstance(midi_note, bool) or not isinstance(midi_note, (int, float)) or not 0 <= midi_note <= 127:
        raise PitchRangeError("MIDI note must be in 0..127.")
    if not _positive_frequency(a4_ref):
        raise MusicTheoryError("Reference frequency must be finite and positive.")
    return a4_ref * (2.0 ** ((midi_note - A4_MIDI_NOTE) / 12.0))


def _positive_frequency(value: float) -> bool:
    if isinstance(value, bool) or not isinstance(value, (int, float)):
        return False
    try:
        return math.isfinite(value) and value > 0
    except OverflowError:
        return False


def frequency_to_midi(freq: float, a4_ref: float = A4_STANDARD_FREQ) -> float:
    """Computes fractional MIDI note from frequency: m = 69 + 12 * log2(f / a4_ref)."""
    if not all(_positive_frequency(value) for value in (freq, a4_ref)):
        raise MusicTheoryError("Frequencies must be finite and positive.")
    return 69.0 + 12.0 * (math.log2(freq) - math.log2(a4_ref))


_UNICODE_TO_ASCII = str.maketrans({"♯": "#", "♭": "b", "𝄪": "x", "𝄫": "bb", "♮": "n"})
_INT_NAME = re.compile(r"[A-Ga-g](?:bb|b|##|#|x|n)?")
_DE_NAMES = {
    NoteSpelling(step, alteration, 4).render("DE")[:-1].lower(): (step, alteration)
    for step in DIATONIC_STEPS
    for alteration in range(-2, 3)
}


def _parse_note_name(name: str, convention: str, octave: int) -> NoteSpelling:
    if convention == "DE":
        german = _DE_NAMES.get(name.lower())
        if german is not None:
            return NoteSpelling(*german, octave)
    elif convention == "INT":
        if _INT_NAME.fullmatch(name):
            return NoteSpelling(name[0].upper(), ALTERATION_SEMITONES[name[1:]], octave)
    else:
        raise MusicTheoryError(f"Unknown notation convention: {convention!r}.")
    raise MusicTheoryError(f"Invalid {convention} note name: {name!r}.")


def parse_spelling(note_str: str, convention: Literal['INT', 'DE', 'AUTO'] = 'AUTO') -> NoteSpelling:
    """Parse a written pitch. AUTO requires explicit DE or INT for a bare B."""
    if not isinstance(note_str, str):
        raise MusicTheoryError("Note spelling must be text.")
    cleaned = note_str.strip().translate(_UNICODE_TO_ASCII)
    match = re.fullmatch(r"([^0-9-]+)(-?[0-9]+)?", cleaned)
    if not match:
        raise MusicTheoryError(f"Cannot parse note spelling: {note_str!r}.")
    name, raw_octave = match.groups()
    try:
        octave = int(raw_octave) if raw_octave is not None else 4
    except ValueError as exc:
        raise MusicTheoryError("Invalid octave.") from exc
    if convention == "AUTO":
        if name.lower() == "b":
            raise MusicTheoryError("Ambiguous B: select DE (B-flat) or INT (B-natural).")
        convention = "DE" if name.lower() in _DE_NAMES else "INT"
    return _parse_note_name(name, convention, octave)

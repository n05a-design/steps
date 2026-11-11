"""
STEPS Music Theory Core: Domain Exceptions.

Provides unambiguous, domain-specific exception classes for the music theory core.
"""

from __future__ import annotations


class MusicTheoryError(Exception):
    """Base exception for all music theory domain errors in STEPS."""
    pass


class InvalidPitchClassError(MusicTheoryError):
    """Raised when a pitch class integer is invalid or out of range."""
    pass


class InvalidDiatonicStepError(MusicTheoryError):
    """Raised when a diatonic note name is not in {'C', 'D', 'E', 'F', 'G', 'A', 'B'}."""
    pass


class InvalidAlterationError(MusicTheoryError):
    """Raised when an alteration semitone offset is not supported (e.g. outside -2..+2)."""
    pass


class PitchRangeError(MusicTheoryError):
    """Raised when a calculated MIDI note falls outside standard MIDI range [0..127]."""
    pass


class InvalidIntervalError(MusicTheoryError):
    """Raised when an interval number or quality combination is theoretically invalid."""
    pass


class ChordConstructionError(MusicTheoryError):
    """Raised when chord construction parameters are contradictory or unresolvable."""
    pass


class VoiceLeadingError(MusicTheoryError):
    """Raised when a voice leading vector is malformed or invalid."""
    pass


class ProgressionParsingError(MusicTheoryError):
    """Raised when a Roman numeral degree or progression string cannot be parsed."""
    pass

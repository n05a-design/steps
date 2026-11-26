"""Physical piano keyboard model: 88 keys, MIDI identity and visible ranges.

The physical layer only knows key identity, MIDI number, octave, pitch class and
white/black colour. It deliberately does not choose a note spelling: one black
key can be C-sharp or D-flat, and a white key can be B-sharp, C or D-double-flat.
Spelling comes from musical context (chord, scale, key) in ``chord_tones``.

Conventions follow ``theory.pitch``: Scientific Pitch Notation with C4 = MIDI 60
and A4 = MIDI 69 = 440 Hz (ISO 16).
"""

from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from typing import Iterable, Iterator

from ..theory.exceptions import PitchRangeError
from ..theory.pitch import A4_MIDI_NOTE, MIDDLE_C_MIDI_NOTE, NoteSpelling, midi_to_frequency

MIDI_MIN = 0
MIDI_MAX = 127
PIANO_LOWEST_MIDI = 21  # A0
PIANO_HIGHEST_MIDI = 108  # C8
PIANO_KEY_COUNT = 88

_BLACK_PITCH_CLASSES = frozenset({1, 3, 6, 8, 10})


def _require_midi(note: object) -> int:
    if isinstance(note, bool) or not isinstance(note, int) or not MIDI_MIN <= note <= MIDI_MAX:
        raise PitchRangeError(f"MIDI note must be an integer in {MIDI_MIN}..{MIDI_MAX}, got {note!r}.")
    return note


def is_black_key(midi: int) -> bool:
    """True for the five raised keys of each octave (pitch classes 1, 3, 6, 8, 10)."""
    return _require_midi(midi) % 12 in _BLACK_PITCH_CLASSES


def is_on_piano(midi: int) -> bool:
    """True when a valid MIDI note lies on the standard 88-key piano (A0..C8)."""
    return PIANO_LOWEST_MIDI <= _require_midi(midi) <= PIANO_HIGHEST_MIDI


def octave_of(midi: int) -> int:
    """Scientific-pitch octave of the key's C-based octave block (C4 = 60)."""
    return _require_midi(midi) // 12 - 1


@dataclass(frozen=True)
class PianoKey:
    """Physical key identity. ``number`` counts 1..88 from A0 on a standard piano."""

    midi: int
    number: int | None
    octave: int
    pitch_class: int
    is_black: bool

    @property
    def is_white(self) -> bool:
        return not self.is_black

    @property
    def frequency(self) -> float:
        """Equal-tempered frequency relative to A4 = 440 Hz."""
        return midi_to_frequency(self.midi)

    def enharmonic_spellings(self) -> tuple[NoteSpelling, ...]:
        """All single/double-accidental spellings that sound at this exact MIDI pitch.

        Ordered by absolute alteration, then letter order; the caller still has to
        choose from context. Returned spellings carry the octave that keeps the
        sounding pitch, so B-sharp of MIDI 60 is B#3 and C-flat of MIDI 59 is Cb4.
        """
        return _enharmonic_spellings(self.midi)


@lru_cache(maxsize=None)
def _enharmonic_spellings(midi: int) -> tuple[NoteSpelling, ...]:
    found: list[NoteSpelling] = []
    for step in ("C", "D", "E", "F", "G", "A", "B"):
        for alteration in (0, -1, 1, -2, 2):
            base = NoteSpelling(step, 0, 4).midi_number  # octave 4 base
            octave_delta, remainder = divmod(midi - (base + alteration), 12)
            if remainder:
                continue
            octave = 4 + octave_delta
            try:
                spelling = NoteSpelling(step, alteration, octave)
                if spelling.midi_number == midi:
                    found.append(spelling)
            except PitchRangeError:
                continue
    return tuple(sorted(found, key=lambda item: (abs(item.alteration), "CDEFGAB".index(item.step))))


@lru_cache(maxsize=None)
def piano_key(midi: int) -> PianoKey:
    """Return the physical key for any MIDI note 0..127 (``number`` is None off-piano)."""
    _require_midi(midi)
    number = midi - PIANO_LOWEST_MIDI + 1 if is_on_piano(midi) else None
    return PianoKey(midi, number, octave_of(midi), midi % 12, midi % 12 in _BLACK_PITCH_CLASSES)


def piano_keys(descending: bool = False) -> tuple[PianoKey, ...]:
    """All 88 keys in ascending (default) or descending pitch order."""
    keys = tuple(piano_key(m) for m in range(PIANO_LOWEST_MIDI, PIANO_HIGHEST_MIDI + 1))
    return tuple(reversed(keys)) if descending else keys


def sorted_unique_notes(notes: Iterable[int]) -> tuple[int, ...]:
    """Validate, deduplicate and sort MIDI notes ascending (deterministic order)."""
    return tuple(sorted({_require_midi(note) for note in notes}))


def _snap_down_to_white(midi: int) -> int:
    return midi - 1 if midi % 12 in _BLACK_PITCH_CLASSES else midi


def _snap_up_to_white(midi: int) -> int:
    return midi + 1 if midi % 12 in _BLACK_PITCH_CLASSES else midi


@dataclass(frozen=True)
class KeyboardViewport:
    """Visible key range. Both edges are white keys inside the 88-key piano.

    The viewport is purely presentational: musical content outside it is kept and
    reported by the view model, never removed or transposed.
    """

    low: int = 48  # C3
    high: int = 84  # C6

    def __post_init__(self) -> None:
        for edge in (self.low, self.high):
            if not is_on_piano(edge):
                raise PitchRangeError(f"Viewport edge {edge} is outside the 88-key piano (21..108).")
            if is_black_key(edge):
                raise PitchRangeError(f"Viewport edge {edge} must be a white key.")
        if self.high - self.low < 11:
            raise PitchRangeError("Viewport must show at least one octave.")

    @classmethod
    def full_piano(cls) -> KeyboardViewport:
        return cls(PIANO_LOWEST_MIDI, PIANO_HIGHEST_MIDI)

    @property
    def span(self) -> int:
        return self.high - self.low

    def contains(self, midi: int) -> bool:
        return self.low <= _require_midi(midi) <= self.high

    def keys(self) -> tuple[PianoKey, ...]:
        return tuple(piano_key(m) for m in range(self.low, self.high + 1))

    def white_keys(self) -> tuple[PianoKey, ...]:
        return tuple(key for key in self.keys() if key.is_white)

    def shifted(self, semitones: int) -> KeyboardViewport:
        """Move by whole semitones, clamped to the piano and re-snapped to white keys."""
        if isinstance(semitones, bool) or not isinstance(semitones, int):
            raise PitchRangeError("Viewport shift must be whole semitones.")
        span = self.span
        low = max(PIANO_LOWEST_MIDI, min(self.low + semitones, PIANO_HIGHEST_MIDI - span))
        low = _snap_down_to_white(low) if low > PIANO_LOWEST_MIDI else PIANO_LOWEST_MIDI
        high = _snap_up_to_white(min(PIANO_HIGHEST_MIDI, low + span))
        return KeyboardViewport(low, high)

    def with_octaves(self, octaves: int) -> KeyboardViewport:
        """Resize around the current low edge to ``octaves`` octaves (1..7)."""
        if isinstance(octaves, bool) or not isinstance(octaves, int) or not 1 <= octaves <= 7:
            raise PitchRangeError("Visible octaves must be an integer in 1..7.")
        span = 12 * octaves
        low = max(PIANO_LOWEST_MIDI, min(self.low, PIANO_HIGHEST_MIDI - span))
        low = _snap_down_to_white(low) if low > PIANO_LOWEST_MIDI else low
        high = _snap_up_to_white(min(PIANO_HIGHEST_MIDI, low + span))
        return KeyboardViewport(low, high)

    def fitted_to(self, notes: Iterable[int], margin: int = 2) -> KeyboardViewport:
        """Smallest move (and growth if needed) that shows every on-piano note.

        Notes outside the piano stay outside; the caller reports them separately.
        """
        playable = [note for note in sorted_unique_notes(notes) if is_on_piano(note)]
        if not playable:
            return self
        lowest, highest = playable[0], playable[-1]
        if self.low <= lowest and highest <= self.high:
            return self
        span = max(self.span, highest - lowest + 2 * margin)
        low = lowest - margin if lowest < self.low else highest + margin - span
        low = max(PIANO_LOWEST_MIDI, min(low, PIANO_HIGHEST_MIDI - span))
        low = _snap_down_to_white(max(PIANO_LOWEST_MIDI, low))
        high = _snap_up_to_white(min(PIANO_HIGHEST_MIDI, max(low + span, highest)))
        if low < PIANO_LOWEST_MIDI:
            low = PIANO_LOWEST_MIDI
        return KeyboardViewport(low, high)

    def partition(self, notes: Iterable[int]) -> tuple[tuple[int, ...], tuple[int, ...], tuple[int, ...]]:
        """Split notes into (below, visible, above); nothing is dropped."""
        ordered = sorted_unique_notes(notes)
        below = tuple(n for n in ordered if n < self.low)
        visible = tuple(n for n in ordered if self.low <= n <= self.high)
        above = tuple(n for n in ordered if n > self.high)
        return below, visible, above


def iter_white_index(viewport: KeyboardViewport) -> Iterator[tuple[int, PianoKey]]:
    """Yield (white-key column, key) pairs; black keys share the column to their left."""
    column = -1
    for key in viewport.keys():
        if key.is_white:
            column += 1
        yield column, key


__all__ = [
    "A4_MIDI_NOTE",
    "MIDDLE_C_MIDI_NOTE",
    "MIDI_MAX",
    "MIDI_MIN",
    "PIANO_HIGHEST_MIDI",
    "PIANO_KEY_COUNT",
    "PIANO_LOWEST_MIDI",
    "KeyboardViewport",
    "PianoKey",
    "is_black_key",
    "is_on_piano",
    "iter_white_index",
    "octave_of",
    "piano_key",
    "piano_keys",
    "sorted_unique_notes",
]

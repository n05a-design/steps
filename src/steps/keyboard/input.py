"""Note input state shared by mouse, computer keyboard and (later) MIDI devices.

Two sets are kept strictly apart:

* ``pressed`` – keys physically held right now (temporary; cleared on release,
  focus loss or device disconnect),
* ``selected`` – latched chord-input notes the user built up deliberately.

A physical MIDI keyboard is meant to feed the same ``apply`` entry point via
``ports.live.LiveNoteEvent`` so virtual and physical input share one code path.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum

from ..ports.live import LiveEventKind, LiveNoteEvent
from .model import _require_midi


class InputSource(str, Enum):
    MOUSE = "MOUSE"
    COMPUTER_KEYBOARD = "COMPUTER_KEYBOARD"
    MIDI_DEVICE = "MIDI_DEVICE"
    PROGRAM = "PROGRAM"


@dataclass
class KeyboardInputState:
    """Mutable, UI-free input state. All methods are idempotent for repeated events."""

    pressed: dict[int, tuple[InputSource, int]] = field(default_factory=dict)  # midi -> (source, velocity)
    selected: set[int] = field(default_factory=set)
    sustained: set[int] = field(default_factory=set)
    sustain_down: bool = False

    # -- temporary key presses -------------------------------------------------
    def press(self, midi: int, source: InputSource = InputSource.MOUSE, velocity: int = 100) -> bool:
        """Mark ``midi`` as held. Returns False for an auto-repeat of an already held key."""
        _require_midi(midi)
        if isinstance(velocity, bool) or not isinstance(velocity, int) or not 1 <= velocity <= 127:
            raise ValueError("Velocity must be an integer in 1..127 (0 means note off).")
        if midi in self.pressed:
            return False
        self.pressed[midi] = (source, velocity)
        self.sustained.discard(midi)
        return True

    def release(self, midi: int) -> bool:
        """Release ``midi``. With sustain held the note keeps sounding until pedal up."""
        _require_midi(midi)
        if midi not in self.pressed:
            return False
        del self.pressed[midi]
        if self.sustain_down:
            self.sustained.add(midi)
        return True

    def set_sustain(self, down: bool) -> None:
        self.sustain_down = bool(down)
        if not self.sustain_down:
            self.sustained.clear()

    def release_all(self) -> tuple[int, ...]:
        """Panic/focus-loss reset of every temporary note. Selection stays."""
        released = tuple(sorted(set(self.pressed) | self.sustained))
        self.pressed.clear()
        self.sustained.clear()
        self.sustain_down = False
        return released

    @property
    def sounding(self) -> tuple[int, ...]:
        return tuple(sorted(set(self.pressed) | self.sustained))

    # -- latched chord input ---------------------------------------------------
    def toggle_selected(self, midi: int) -> bool:
        """Toggle a latched note; returns True if it is now selected."""
        _require_midi(midi)
        if midi in self.selected:
            self.selected.discard(midi)
            return False
        self.selected.add(midi)
        return True

    def set_selected(self, notes) -> None:
        self.selected = {_require_midi(n) for n in notes}

    def clear_selected(self) -> None:
        self.selected.clear()

    @property
    def active_notes(self) -> tuple[int, ...]:
        """Notes that count as input for recognition/practice: selection plus sounding keys."""
        return tuple(sorted(self.selected | set(self.pressed) | self.sustained))

    # -- unified event path ----------------------------------------------------
    def apply(self, event: LiveNoteEvent, source: InputSource = InputSource.MIDI_DEVICE) -> None:
        if event.kind is LiveEventKind.NOTE_ON:
            self.press(event.note, source, event.velocity)
        elif event.kind is LiveEventKind.NOTE_OFF:
            self.release(event.note)
        elif event.kind is LiveEventKind.SUSTAIN:
            self.set_sustain(event.value >= 64)
        elif event.kind is LiveEventKind.ALL_NOTES_OFF:
            self.release_all()


__all__ = ["InputSource", "KeyboardInputState"]

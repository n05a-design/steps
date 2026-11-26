"""STEPS Architecture Ports: live note input and note preview (proposed, ADR-019).

Status: interface specification with deterministic test adapters only.
ADR-007 keeps v0.1 to file export; no device driver, synthesizer or soundfont is
shipped or imported here. Real adapters need an owner decision (ADR-019).

* ``normalize_midi_message`` turns raw MIDI 1.0 channel messages into
  ``LiveNoteEvent`` values (note-on velocity 0 is note-off, CC64 is sustain,
  CC120/CC123 are all-sound/all-notes-off).
* ``MidiInputPort`` describes a future device adapter. Its callback may run on a
  driver thread; GUI code must marshal events with ``ui_dispatcher`` (e.g.
  ``root.after_idle``) and must call ``release_all`` on disconnect.
* ``NotePreviewService`` wraps the existing ``AudioBackendPort`` so any preview
  tracks its sounding notes and can always silence them (T14: no hung notes).
"""

from __future__ import annotations

import threading
import time
from dataclasses import dataclass, field
from enum import Enum
from typing import Callable, Iterable, Optional, Protocol

from .audio import AudioBackendPort, PlaybackEvent


class LiveEventKind(str, Enum):
    NOTE_ON = "NOTE_ON"
    NOTE_OFF = "NOTE_OFF"
    SUSTAIN = "SUSTAIN"
    ALL_NOTES_OFF = "ALL_NOTES_OFF"


@dataclass(frozen=True)
class LiveNoteEvent:
    kind: LiveEventKind
    note: int = 0
    velocity: int = 0
    channel: int = 0
    value: int = 0  # controller value for SUSTAIN
    timestamp: float = field(default_factory=time.monotonic)

    def __post_init__(self) -> None:
        for name, value, high in (("note", self.note, 127), ("velocity", self.velocity, 127),
                                  ("channel", self.channel, 15), ("value", self.value, 127)):
            if isinstance(value, bool) or not isinstance(value, int) or not 0 <= value <= high:
                raise ValueError(f"{name} must be an integer in 0..{high}, got {value!r}.")
        if self.kind is LiveEventKind.NOTE_ON and self.velocity == 0:
            raise ValueError("NOTE_ON needs velocity 1..127; velocity 0 is a NOTE_OFF.")


def normalize_midi_message(status: int, data1: int = 0, data2: int = 0) -> Optional[LiveNoteEvent]:
    """Map one MIDI 1.0 channel-voice message to a live event, or None if irrelevant."""
    for value in (status, data1, data2):
        if isinstance(value, bool) or not isinstance(value, int):
            raise ValueError("MIDI bytes must be integers.")
    if not 0x80 <= status <= 0xEF or not 0 <= data1 <= 127 or not 0 <= data2 <= 127:
        return None
    kind, channel = status & 0xF0, status & 0x0F
    if kind == 0x90 and data2 > 0:
        return LiveNoteEvent(LiveEventKind.NOTE_ON, data1, data2, channel)
    if kind == 0x80 or (kind == 0x90 and data2 == 0):
        return LiveNoteEvent(LiveEventKind.NOTE_OFF, data1, 0, channel)
    if kind == 0xB0 and data1 == 64:
        return LiveNoteEvent(LiveEventKind.SUSTAIN, channel=channel, value=data2)
    if kind == 0xB0 and data1 in (120, 123):
        return LiveNoteEvent(LiveEventKind.ALL_NOTES_OFF, channel=channel)
    return None


@dataclass(frozen=True)
class MidiInputDevice:
    device_id: str
    name: str


class MidiInputPort(Protocol):
    """Future physical MIDI input (not implemented; see ADR-019)."""

    def list_devices(self) -> tuple[MidiInputDevice, ...]: ...

    def open(self, device_id: str, on_event: Callable[[LiveNoteEvent], None]) -> None: ...

    def close(self) -> None: ...


class ScriptedMidiInput:
    """Deterministic MidiInputPort for tests: replays raw MIDI bytes on demand."""

    def __init__(self, devices: Iterable[MidiInputDevice] = ()) -> None:
        self._devices = tuple(devices)
        self._callback: Optional[Callable[[LiveNoteEvent], None]] = None
        self.opened: Optional[str] = None

    def list_devices(self) -> tuple[MidiInputDevice, ...]:
        return self._devices

    def open(self, device_id: str, on_event: Callable[[LiveNoteEvent], None]) -> None:
        if device_id not in {d.device_id for d in self._devices}:
            raise LookupError(f"Unknown MIDI input device: {device_id!r}")
        self.opened, self._callback = device_id, on_event

    def close(self) -> None:
        callback, self._callback, self.opened = self._callback, None, None
        if callback is not None:
            callback(LiveNoteEvent(LiveEventKind.ALL_NOTES_OFF))

    def feed(self, status: int, data1: int = 0, data2: int = 0) -> None:
        event = normalize_midi_message(status, data1, data2)
        if event is not None and self._callback is not None:
            self._callback(event)


class NotePreviewService:
    """Note on/off/all-off over an ``AudioBackendPort`` with hung-note protection.

    With ``NullAudioBackend`` nothing is audible; this is the only backend
    permitted by ADR-007 for v0.1.
    """

    def __init__(self, backend: AudioBackendPort, channel: int = 0) -> None:
        self._backend = backend
        self._channel = channel
        self._lock = threading.RLock()
        self._sounding: set[int] = set()

    @property
    def sounding(self) -> tuple[int, ...]:
        with self._lock:
            return tuple(sorted(self._sounding))

    def note_on(self, note: int, velocity: int = 90) -> None:
        with self._lock:
            if note in self._sounding:
                self._backend.send_event(PlaybackEvent(0, "note_off", note, 0, self._channel, "preview"))
            self._backend.send_event(PlaybackEvent(0, "note_on", note, velocity, self._channel, "preview"))
            self._sounding.add(note)

    def note_off(self, note: int) -> None:
        with self._lock:
            if note in self._sounding:
                self._backend.send_event(PlaybackEvent(0, "note_off", note, 0, self._channel, "preview"))
                self._sounding.discard(note)

    def preview_chord(self, notes: Iterable[int], velocity: int = 90) -> None:
        with self._lock:
            self.all_notes_off()
            for note in sorted(set(notes)):
                self.note_on(note, velocity)

    def all_notes_off(self) -> None:
        with self._lock:
            for note in sorted(self._sounding):
                self._backend.send_event(PlaybackEvent(0, "note_off", note, 0, self._channel, "preview"))
            self._sounding.clear()
            self._backend.all_notes_off(self._channel)


__all__ = [
    "LiveEventKind",
    "LiveNoteEvent",
    "MidiInputDevice",
    "MidiInputPort",
    "NotePreviewService",
    "ScriptedMidiInput",
    "normalize_midi_message",
]

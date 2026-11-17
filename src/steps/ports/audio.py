"""
STEPS Architecture Ports: Audio Transport, Playback Backend & Monotonic Scheduler.

Adheres to:
- ADR-007 (Audio/MIDI Architecture: Ports first, NullBackend for headless/CI)
- Prompt 07 & Prompt 11 (Non-blocking transport, MonotonicScheduler, Loop/Cancel/Stop, No Tk-callbacks with audio sleep)
- Golden Invariants: T14 (No hung notes via guaranteed all_notes_off), T15 (Multi-tempo map support)
"""

from __future__ import annotations

import logging
import threading
import time
from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Callable, Dict, List, Optional, Tuple

from ..models.timeline import DEFAULT_PPQ, TempoMap, Timeline, TimelineEvent
from ..theory.chord import ChordDefinition, Voicing, parse_chord

logger = logging.getLogger(__name__)


class PlaybackState(str, Enum):
    """Transport lifecycle states."""
    STOPPED = "STOPPED"
    PLAYING = "PLAYING"
    PAUSED = "PAUSED"


@dataclass(frozen=True)
class PlaybackEvent:
    """Atomic playback event scheduled at a specific musical tick."""
    tick: int
    event_type: str  # 'note_on', 'note_off', 'all_notes_off'
    pitch: int = 60  # MIDI note number [0..127]
    velocity: int = 80  # MIDI velocity [0..127]
    channel: int = 0  # MIDI channel [0..15]
    track_id: str = "main"

    def __post_init__(self):
        if not isinstance(self.tick, int) or self.tick < 0:
            raise ValueError(f"tick must be a non-negative integer, got {self.tick}")
        if self.event_type not in ("note_on", "note_off", "all_notes_off"):
            raise ValueError(f"Unknown event_type: {self.event_type}")
        if not (0 <= self.pitch <= 127):
            raise ValueError(f"pitch must be in [0..127], got {self.pitch}")
        if not (0 <= self.velocity <= 127):
            raise ValueError(f"velocity must be in [0..127], got {self.velocity}")
        if not (0 <= self.channel <= 15):
            raise ValueError(f"channel must be in [0..15], got {self.channel}")


class AudioBackendPort(ABC):
    """Abstract port for physical, virtual or synthetic audio/MIDI backends."""

    @abstractmethod
    def is_available(self) -> bool:
        """Returns True if the audio device/subsystem is ready for output."""
        ...

    @abstractmethod
    def open(self) -> None:
        """Initializes and opens audio/MIDI connections."""
        ...

    @abstractmethod
    def close(self) -> None:
        """Closes audio backend and releases hardware/software resources."""
        ...

    @abstractmethod
    def send_event(self, event: PlaybackEvent) -> None:
        """Sends a single playback event directly to output."""
        ...

    @abstractmethod
    def all_notes_off(self, channel: Optional[int] = None) -> None:
        """Silences all active sounding voices to prevent hanging notes (T14)."""
        ...

    @abstractmethod
    def get_device_info(self) -> Dict[str, Any]:
        """Returns diagnostics and device descriptor."""
        ...


class NullAudioBackend(AudioBackendPort):
    """
    Deterministic in-memory test backend.
    
    Used for headless CI, unit tests, and system fallback when no physical
    MIDI or audio devices are present. Thread-safe and recording all events.
    """

    def __init__(self) -> None:
        self._lock = threading.RLock()
        self._is_open: bool = False
        self.events_recorded: List[Tuple[float, PlaybackEvent]] = []
        self.all_notes_off_count: int = 0

    def is_available(self) -> bool:
        return True

    def open(self) -> None:
        with self._lock:
            self._is_open = True

    def close(self) -> None:
        with self._lock:
            self._is_open = False
            self.all_notes_off()

    def send_event(self, event: PlaybackEvent) -> None:
        with self._lock:
            self.events_recorded.append((time.monotonic(), event))

    def all_notes_off(self, channel: Optional[int] = None) -> None:
        with self._lock:
            self.all_notes_off_count += 1
            self.events_recorded.append(
                (time.monotonic(), PlaybackEvent(tick=0, event_type="all_notes_off", channel=channel or 0))
            )

    def get_device_info(self) -> Dict[str, Any]:
        with self._lock:
            return {
                "driver": "null",
                "name": "Null Headless Audio Backend",
                "available": True,
                "is_open": self._is_open,
                "recorded_count": len(self.events_recorded),
                "all_notes_off_count": self.all_notes_off_count,
            }

    def clear(self) -> None:
        with self._lock:
            self.events_recorded.clear()
            self.all_notes_off_count = 0


class MonotonicPlaybackScheduler:
    """
    Real-time transport scheduler driven by time.monotonic().

    Runs event dispatch in a dedicated background worker thread to ensure:
    - GUI thread is never blocked (no audio sleep in Tk event loop).
    - Jitter-free scheduling using high-resolution monotonic clock.
    - Safe loop, pause, seek, stop and close without deadlocks.
    - Safe UI notification using optional ui_dispatcher (e.g. root.after_idle).
    - Absolute prevention of hanging notes (T14 invariant) on stop/loop/close.
    """

    def __init__(
        self,
        backend: AudioBackendPort,
        events: Optional[List[PlaybackEvent]] = None,
        tempo_bpm: float = 120.0,
        tempo_map: Optional[TempoMap] = None,
        ppq: int = DEFAULT_PPQ,
        loop: bool = False,
        loop_start_tick: int = 0,
        loop_end_tick: Optional[int] = None,
        on_tick: Optional[Callable[[int, float], None]] = None,
        on_state_change: Optional[Callable[[PlaybackState], None]] = None,
        ui_dispatcher: Optional[Callable[[Callable[[], None]], None]] = None,
    ) -> None:
        self.backend = backend
        self.ppq = ppq
        self.tempo_map = tempo_map or TempoMap(points=[], ppq=ppq)
        if not tempo_map:
            self.tempo_map.points[0] = self.tempo_map.points[0].__class__(0, tempo_bpm)

        self.loop = loop
        self.loop_start_tick = max(0, loop_start_tick)
        self.loop_end_tick = loop_end_tick
        self.on_tick = on_tick
        self.on_state_change = on_state_change
        self.ui_dispatcher = ui_dispatcher

        self._lock = threading.RLock()
        self._state: PlaybackState = PlaybackState.STOPPED
        self._current_tick: int = self.loop_start_tick
        self._events: List[PlaybackEvent] = []
        if events:
            self.set_events(events)

        self._worker_thread: Optional[threading.Thread] = None
        self._stop_event = threading.Event()
        self._pause_event = threading.Event()
        self._pause_event.set()  # Unpaused initially

    @property
    def state(self) -> PlaybackState:
        with self._lock:
            return self._state

    @property
    def current_tick(self) -> int:
        with self._lock:
            return self._current_tick

    def set_events(self, events: List[PlaybackEvent]) -> None:
        """Sets and sorts the scheduled event list."""
        with self._lock:
            self._events = sorted(events, key=lambda e: (e.tick, 0 if e.event_type == "note_off" else 1))
            if self.loop_end_tick is None and self._events:
                self.loop_end_tick = max(e.tick for e in self._events)

    def set_loop(self, start_tick: int, end_tick: Optional[int], loop: bool = True) -> None:
        with self._lock:
            self.loop_start_tick = max(0, start_tick)
            self.loop_end_tick = end_tick
            self.loop = loop

    def _notify_state_change(self, new_state: PlaybackState) -> None:
        if not self.on_state_change:
            return
        cb = self.on_state_change
        if self.ui_dispatcher:
            self.ui_dispatcher(lambda: cb(new_state))
        else:
            try:
                cb(new_state)
            except Exception as e:
                logger.error("Error in on_state_change callback: %s", e)

    def _notify_tick(self, tick: int, seconds: float) -> None:
        if not self.on_tick:
            return
        cb = self.on_tick
        if self.ui_dispatcher:
            self.ui_dispatcher(lambda: cb(tick, seconds))
        else:
            try:
                cb(tick, seconds)
            except Exception as e:
                logger.error("Error in on_tick callback: %s", e)

    def play(self) -> None:
        """Starts or restarts playback."""
        with self._lock:
            if self._state == PlaybackState.PLAYING:
                return

            if not self.backend.is_available():
                logger.warning("Audio backend is unavailable, skipping playback.")
                return

            self.backend.open()
            self._stop_event.clear()
            self._pause_event.set()
            self._state = PlaybackState.PLAYING
            self._notify_state_change(PlaybackState.PLAYING)

            if self._worker_thread is None or not self._worker_thread.is_alive():
                self._worker_thread = threading.Thread(target=self._run_loop, daemon=True, name="StepsAudioScheduler")
                self._worker_thread.start()

    def pause(self) -> None:
        """Pauses transport and silences active voices."""
        with self._lock:
            if self._state != PlaybackState.PLAYING:
                return
            self._pause_event.clear()
            self._state = PlaybackState.PAUSED
            self.backend.all_notes_off()
            self._notify_state_change(PlaybackState.PAUSED)

    def resume(self) -> None:
        """Resumes transport from paused position."""
        with self._lock:
            if self._state != PlaybackState.PAUSED:
                return
            self._pause_event.set()
            self._state = PlaybackState.PLAYING
            self._notify_state_change(PlaybackState.PLAYING)

    def stop(self) -> None:
        """Stops transport, rewinds to start, and silences all notes."""
        with self._lock:
            self._stop_event.set()
            self._pause_event.set()
            self._state = PlaybackState.STOPPED
            self._current_tick = self.loop_start_tick
            self.backend.all_notes_off()
            self._notify_state_change(PlaybackState.STOPPED)

    def seek(self, tick: int) -> None:
        """Seeks transport to target tick, silencing active notes to prevent hanging."""
        with self._lock:
            self._current_tick = max(0, tick)
            self.backend.all_notes_off()
            elapsed_sec = self.tempo_map.tick_to_seconds(self._current_tick)
            self._notify_tick(self._current_tick, elapsed_sec)

    def close(self) -> None:
        """Shuts down scheduler and worker thread safely."""
        self.stop()
        if self._worker_thread and self._worker_thread.is_alive():
            self._worker_thread.join(timeout=1.0)
        self.backend.close()

    def _run_loop(self) -> None:
        """High-resolution background playback loop."""
        with self._lock:
            events_to_play = list(self._events)
            idx = 0
            while idx < len(events_to_play) and events_to_play[idx].tick < self._current_tick:
                idx += 1

        last_mono = time.monotonic()

        while not self._stop_event.is_set():
            if not self._pause_event.is_set():
                self._pause_event.wait(timeout=0.05)
                last_mono = time.monotonic()
                continue

            with self._lock:
                end_tick = self.loop_end_tick if self.loop_end_tick is not None else (
                    events_to_play[-1].tick if events_to_play else 0
                )

                if self._current_tick >= end_tick:
                    self.backend.all_notes_off()
                    if self.loop:
                        self._current_tick = self.loop_start_tick
                        idx = 0
                        while idx < len(events_to_play) and events_to_play[idx].tick < self._current_tick:
                            idx += 1
                        last_mono = time.monotonic()
                    else:
                        self._state = PlaybackState.STOPPED
                        self._current_tick = self.loop_start_tick
                        self._notify_state_change(PlaybackState.STOPPED)
                        break

                while idx < len(events_to_play) and events_to_play[idx].tick <= self._current_tick:
                    ev = events_to_play[idx]
                    self.backend.send_event(ev)
                    idx += 1

                curr_t = self._current_tick
                elapsed_sec = self.tempo_map.tick_to_seconds(curr_t)

            self._notify_tick(curr_t, elapsed_sec)

            time.sleep(0.005)
            now_mono = time.monotonic()
            dt_sec = now_mono - last_mono
            last_mono = now_mono

            # Advance ticks only if still playing (not paused or stopped)
            with self._lock:
                if not self._pause_event.is_set() or self._stop_event.is_set() or self._state != PlaybackState.PLAYING:
                    continue
                active_bpm = self.tempo_map.get_tempo_at_tick(self._current_tick)
                ticks_per_sec = (active_bpm * self.ppq) / 60.0
                delta_ticks = int(round(dt_sec * ticks_per_sec))
                if delta_ticks < 1 and dt_sec > 0.003:
                    delta_ticks = 1
                self._current_tick += delta_ticks


def events_from_voicings(
    voicings: List[Voicing],
    duration_ticks: int = 1920,
    channel: int = 0
) -> List[PlaybackEvent]:
    """Converts a list of Voicings into sorted PlaybackEvents."""
    events: List[PlaybackEvent] = []
    current_tick = 0

    for v in voicings:
        for note in v.midi_notes:
            events.append(PlaybackEvent(
                tick=current_tick,
                event_type="note_on",
                pitch=note,
                velocity=80,
                channel=channel,
                track_id="chords"
            ))
            events.append(PlaybackEvent(
                tick=current_tick + duration_ticks,
                event_type="note_off",
                pitch=note,
                velocity=0,
                channel=channel,
                track_id="chords"
            ))
        current_tick += duration_ticks

    events.sort(key=lambda e: (e.tick, 0 if e.event_type == "note_off" else 1))
    return events


def events_from_timeline(timeline: Timeline, channel: int = 0) -> List[PlaybackEvent]:
    """Converts a Timeline object into a sorted list of PlaybackEvents."""
    events: List[PlaybackEvent] = []

    for ev in timeline.events:
        if ev.event_type in ("NOTE", "CHORD"):
            pitches = []
            if isinstance(ev.payload, dict) and "pitches" in ev.payload:
                pitches = ev.payload["pitches"]
            elif isinstance(ev.payload, (int, float)):
                pitches = [int(ev.payload)]
            elif isinstance(ev.payload, (list, tuple)):
                pitches = list(ev.payload)

            for p in pitches:
                if 0 <= p <= 127:
                    events.append(PlaybackEvent(
                        tick=ev.start_tick,
                        event_type="note_on",
                        pitch=p,
                        velocity=80,
                        channel=channel,
                        track_id=ev.track_id
                    ))
                    events.append(PlaybackEvent(
                        tick=ev.start_tick + ev.duration_ticks,
                        event_type="note_off",
                        pitch=p,
                        velocity=0,
                        channel=channel,
                        track_id=ev.track_id
                    ))

    events.sort(key=lambda e: (e.tick, 0 if e.event_type == "note_off" else 1))
    return events

"""
STEPS Music Domain: Drum Patterns, Grooves & Beat Grid Model.

Adheres to:
- Prompt 10 (Drum Progressions, Groove und Beatmaking)
- ADR-002, ADR-007
- General MIDI (GM 1.0) Channel 10 percussion standard
- Shared 480 PPQ timeline integration (no separate timing formats)
- Non-destructive swing and microtiming transformations
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from enum import IntEnum
from typing import Any, Dict, List, Optional

from ..midi.smf import MidiTrack
from .timeline import (
    DEFAULT_PPQ,
    TimeSignature,
    TimelineEvent,
    apply_humanize,
    apply_swing,
)


class GeneralMidiPercussion(IntEnum):
    """Standard General MIDI 1.0 Channel 10 Key Map."""
    ACOUSTIC_BASS_DRUM = 35
    BASS_DRUM_1 = 36
    SIDE_STICK = 37
    ACOUSTIC_SNARE = 38
    HAND_CLAP = 39
    ELECTRIC_SNARE = 40
    LOW_FLOOR_TOM = 41
    CLOSED_HI_HAT = 42
    HIGH_FLOOR_TOM = 43
    PEDAL_HI_HAT = 44
    LOW_TOM = 45
    OPEN_HI_HAT = 46
    LOW_MID_TOM = 47
    HI_MID_TOM = 48
    CRASH_CYMBAL_1 = 49
    HIGH_TOM = 50
    RIDE_CYMBAL_1 = 51
    CHINESE_CYMBAL = 52
    RIDE_BELL = 53
    TAMBOURINE = 54
    SPLASH_CYMBAL = 55
    COWBELL = 56
    CRASH_CYMBAL_2 = 57
    VIBRASLAP = 58
    RIDE_CYMBAL_2 = 59


@dataclass(frozen=True)
class DrumPad:
    """A drum instrument pad mapped to a General MIDI pitch."""
    pad_id: str
    name: str
    midi_pitch: int

    def __post_init__(self):
        if not (0 <= self.midi_pitch <= 127):
            raise ValueError(f"midi_pitch must be in [0..127], got {self.midi_pitch}")


@dataclass
class DrumStep:
    """An individual step on a drum track grid."""
    step_index: int
    active: bool = False
    velocity: int = 100
    probability: float = 1.0
    microtiming_offset: int = 0  # Off-grid nudge in ticks

    def __post_init__(self):
        if self.step_index < 0:
            raise ValueError(f"step_index must be >= 0, got {self.step_index}")
        if not (0 <= self.velocity <= 127):
            raise ValueError(f"velocity must be in [0..127], got {self.velocity}")
        if not (0.0 <= self.probability <= 1.0):
            raise ValueError(f"probability must be in [0.0..1.0], got {self.probability}")
        if not (-120 <= self.microtiming_offset <= 120):
            raise ValueError(f"microtiming_offset must be in [-120..120], got {self.microtiming_offset}")


@dataclass
class DrumTrack:
    """A sequence of steps triggering a specific DrumPad."""
    pad: DrumPad
    steps: List[DrumStep] = field(default_factory=list)

    def set_step(
        self,
        step_index: int,
        active: bool = True,
        velocity: int = 100,
        probability: float = 1.0,
        microtiming_offset: int = 0
    ) -> None:
        """Sets or replaces a step configuration."""
        self.steps = [s for s in self.steps if s.step_index != step_index]
        self.steps.append(
            DrumStep(
                step_index=step_index,
                active=active,
                velocity=velocity,
                probability=probability,
                microtiming_offset=microtiming_offset
            )
        )
        self.steps.sort(key=lambda s: s.step_index)


@dataclass
class DrumPattern:
    """
    Complete rhythm pattern container.
    
    Operates on a step grid (e.g. 16 or 32 steps) with configurable step resolution
    (default 120 ticks = 16th note at 480 PPQ), swing, and humanization.
    """
    pattern_id: str
    name: str
    meter: TimeSignature = field(default_factory=lambda: TimeSignature(4, 4))
    step_count: int = 16
    step_resolution_ticks: int = 120  # 480 / 4 = 16th notes
    swing_amount: float = 0.0
    humanize_ticks: int = 0
    tracks: List[DrumTrack] = field(default_factory=list)

    def __post_init__(self):
        if self.step_count not in (8, 16, 24, 32, 64):
            raise ValueError(f"step_count must be in (8, 16, 24, 32, 64), got {self.step_count}")
        if self.step_resolution_ticks <= 0:
            raise ValueError(f"step_resolution_ticks must be > 0, got {self.step_resolution_ticks}")
        if not (0.0 <= self.swing_amount <= 1.0):
            raise ValueError(f"swing_amount must be in [0.0..1.0], got {self.swing_amount}")
        if self.humanize_ticks < 0:
            raise ValueError(f"humanize_ticks must be >= 0, got {self.humanize_ticks}")

    def add_track(self, pad: DrumPad) -> DrumTrack:
        """Adds a new drum instrument track initialized with inactive steps."""
        track = DrumTrack(
            pad=pad,
            steps=[DrumStep(step_index=i, active=False) for i in range(self.step_count)]
        )
        self.tracks.append(track)
        return track

    def get_track(self, pad_id: str) -> Optional[DrumTrack]:
        for trk in self.tracks:
            if trk.pad.pad_id == pad_id:
                return trk
        return None

    def to_timeline_events(
        self,
        start_tick: int = 0,
        ppq: int = DEFAULT_PPQ,
        seed: int = 42,
        hit_duration_ticks: int = 60
    ) -> List[TimelineEvent]:
        """
        Renders pattern to TimelineEvents on the shared PPQ timeline.
        Applies swing, probability, and microtiming without altering the pattern.
        """
        rng = random.Random(seed)
        events: List[TimelineEvent] = []

        for track in self.tracks:
            for step in track.steps:
                if not step.active:
                    continue
                # Probability check
                if step.probability < 1.0 and rng.random() > step.probability:
                    continue

                base_tick = start_tick + (step.step_index * self.step_resolution_ticks)

                # Apply swing to off-beat 16th or 8th notes
                swung_tick = base_tick
                if self.swing_amount > 0.0:
                    swung_tick = apply_swing(base_tick, self.swing_amount, ppq=ppq)

                # Apply microtiming offset and humanize
                final_tick = swung_tick + step.microtiming_offset
                if self.humanize_ticks > 0:
                    final_tick = apply_humanize(final_tick, self.humanize_ticks, seed=seed + step.step_index)

                final_tick = max(0, final_tick)

                events.append(
                    TimelineEvent(
                        event_id=f"{self.pattern_id}_{track.pad.pad_id}_{step.step_index}",
                        track_id=f"drum_{track.pad.pad_id}",
                        event_type="NOTE",
                        start_tick=final_tick,
                        duration_ticks=hit_duration_ticks,
                        payload={
                            "pitch": track.pad.midi_pitch,
                            "velocity": step.velocity,
                            "channel": 9,  # GM Drum Channel (0-indexed)
                            "pad_id": track.pad.pad_id,
                        },
                        source_id=self.pattern_id
                    )
                )

        events.sort(key=lambda e: e.start_tick)
        return events

    def to_midi_track(
        self,
        name: str = "Drums",
        channel: int = 9,
        ppq: int = DEFAULT_PPQ,
        start_tick: int = 0,
        seed: int = 42,
        hit_duration_ticks: int = 60
    ) -> MidiTrack:
        """Renders pattern directly to a Standard MIDI File Track."""
        midi_track = MidiTrack(name=name)
        tl_events = self.to_timeline_events(start_tick=start_tick, ppq=ppq, seed=seed, hit_duration_ticks=hit_duration_ticks)

        for ev in tl_events:
            pitch = ev.payload.get("pitch", 36)
            velocity = ev.payload.get("velocity", 100)
            midi_track.add_note(
                start_tick=ev.start_tick,
                duration_ticks=ev.duration_ticks,
                pitch=pitch,
                velocity=velocity,
                channel=channel
            )

        return midi_track

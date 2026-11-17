"""
STEPS Common Domain Models: Timeline, Musical Time & Event Scheduling.

Adheres to:
- ADR-005, ADR-007
- M05 (Timeline, PPQ-Auflösung, Takt-/Metrenmodelle)
- 480 PPQ integer tick resolution
- Deterministic multi-tempo conversions and swing/humanize transforms
"""

from __future__ import annotations

import random
from dataclasses import dataclass, field
from typing import Any, Dict, List, Optional, Tuple

DEFAULT_PPQ: int = 480


@dataclass(frozen=True)
class TimeSignature:
    """Musical meter definition (e.g. 4/4, 3/4, 6/8, 7/8)."""
    numerator: int = 4
    denominator: int = 4

    def __post_init__(self):
        if not isinstance(self.numerator, int) or self.numerator < 1:
            raise ValueError(f"Time signature numerator must be >= 1, got {self.numerator}")
        if self.denominator not in (1, 2, 4, 8, 16, 32):
            raise ValueError(f"Time signature denominator must be a power of two in [1..32], got {self.denominator}")

    def ticks_per_bar(self, ppq: int = DEFAULT_PPQ) -> int:
        """Computes exact tick length of one measure."""
        # 1 quarter note = ppq ticks. Whole note = ppq * 4 ticks.
        # Beat unit tick length = (ppq * 4) // denominator
        return self.numerator * ((ppq * 4) // self.denominator)

    def ticks_per_beat(self, ppq: int = DEFAULT_PPQ) -> int:
        """Computes exact tick length of one beat."""
        return (ppq * 4) // self.denominator


@dataclass(frozen=True)
class TempoPoint:
    """A tempo marker on the timeline at a specific tick."""
    start_tick: int
    bpm: float

    def __post_init__(self):
        if not isinstance(self.start_tick, int) or self.start_tick < 0:
            raise ValueError(f"start_tick must be non-negative integer, got {self.start_tick}")
        if not isinstance(self.bpm, (int, float)) or self.bpm <= 0.0:
            raise ValueError(f"bpm must be positive float, got {self.bpm}")

    @property
    def microseconds_per_quarter(self) -> int:
        """Standard SMF tempo meta event value: microseconds per quarter note."""
        return int(round(60_000_000.0 / self.bpm))


@dataclass
class TempoMap:
    """
    Continuous tempo map supporting multiple tempo changes along integer ticks.
    Converts between musical ticks and elapsed wall-clock seconds.
    """
    points: List[TempoPoint] = field(default_factory=lambda: [TempoPoint(0, 120.0)])
    ppq: int = DEFAULT_PPQ

    def __post_init__(self):
        if not self.points:
            self.points = [TempoPoint(0, 120.0)]
        self.points.sort(key=lambda p: p.start_tick)
        if self.points[0].start_tick != 0:
            # Guarantee a base tempo at tick 0
            self.points.insert(0, TempoPoint(0, self.points[0].bpm))

    def add_tempo_point(self, start_tick: int, bpm: float) -> None:
        """Inserts or updates a tempo point."""
        point = TempoPoint(start_tick, bpm)
        self.points = [p for p in self.points if p.start_tick != start_tick]
        self.points.append(point)
        self.points.sort(key=lambda p: p.start_tick)

    def get_tempo_at_tick(self, tick: int) -> float:
        """Returns the active BPM at the given tick."""
        active = self.points[0].bpm
        for p in self.points:
            if p.start_tick <= tick:
                active = p.bpm
            else:
                break
        return active

    def tick_to_seconds(self, target_tick: int) -> float:
        """Converts integer tick to wall-clock seconds respecting all tempo segments."""
        if target_tick <= 0:
            return 0.0

        elapsed_sec = 0.0
        for i, point in enumerate(self.points):
            segment_start = point.start_tick
            next_start = self.points[i + 1].start_tick if i + 1 < len(self.points) else None

            if next_start is not None and target_tick >= next_start:
                # Full segment
                ticks_in_seg = next_start - segment_start
                seconds_per_tick = 60.0 / (point.bpm * self.ppq)
                elapsed_sec += ticks_in_seg * seconds_per_tick
            else:
                # Partial segment reaching target_tick
                ticks_in_seg = target_tick - segment_start
                seconds_per_tick = 60.0 / (point.bpm * self.ppq)
                elapsed_sec += ticks_in_seg * seconds_per_tick
                break

        return elapsed_sec

    def seconds_to_tick(self, target_seconds: float) -> int:
        """Converts wall-clock seconds to integer ticks respecting all tempo segments."""
        if target_seconds <= 0.0:
            return 0

        accum_sec = 0.0
        current_tick = 0

        for i, point in enumerate(self.points):
            next_start = self.points[i + 1].start_tick if i + 1 < len(self.points) else None
            seconds_per_tick = 60.0 / (point.bpm * self.ppq)

            if next_start is not None:
                ticks_in_seg = next_start - point.start_tick
                seg_duration = ticks_in_seg * seconds_per_tick
                if accum_sec + seg_duration < target_seconds:
                    accum_sec += seg_duration
                    current_tick = next_start
                    continue

            # Within this segment
            rem_seconds = target_seconds - accum_sec
            ticks_rem = int(round(rem_seconds / seconds_per_tick))
            return point.start_tick + ticks_rem

        return current_tick


@dataclass(frozen=True)
class TimelineEvent:
    """
    Atomic musical event on the timeline.
    Separates onset start_tick from duration_ticks (no implicit zero-durations).
    """
    event_id: str
    track_id: str
    event_type: str  # e.g. 'CHORD', 'NOTE', 'REST', 'DRUM_HIT'
    start_tick: int
    duration_ticks: int
    payload: Any = None
    source_id: Optional[str] = None

    def __post_init__(self):
        if not isinstance(self.start_tick, int) or self.start_tick < 0:
            raise ValueError(f"start_tick must be >= 0 integer, got {self.start_tick}")
        if not isinstance(self.duration_ticks, int) or self.duration_ticks <= 0:
            raise ValueError(f"duration_ticks must be > 0 integer, got {self.duration_ticks}")

    @property
    def end_tick(self) -> int:
        return self.start_tick + self.duration_ticks


@dataclass
class Timeline:
    """Timeline container holding a sequence of TimelineEvents."""
    events: List[TimelineEvent] = field(default_factory=list)
    ppq: int = DEFAULT_PPQ
    tempo_map: TempoMap = field(default_factory=TempoMap)
    time_signature: TimeSignature = field(default_factory=TimeSignature)

    def add_event(self, event: TimelineEvent) -> None:
        self.events.append(event)
        self.events.sort(key=lambda e: e.start_tick)

    @property
    def total_ticks(self) -> int:
        if not self.events:
            return 0
        return max(e.end_tick for e in self.events)


def apply_swing(tick: int, amount: float, ppq: int = DEFAULT_PPQ) -> int:
    """
    Applies deterministic swing transformation to off-beat 8th notes.
    
    amount: float between 0.0 (straight) and 1.0 (maximum triplet swing).
    0.5 represents standard jazz swing (shifting the 2nd eighth note to triplet position).
    """
    if not (0.0 <= amount <= 1.0):
        raise ValueError(f"Swing amount must be in range [0.0..1.0], got {amount}")
    if amount == 0.0:
        return tick

    beat_ticks = ppq  # 1 quarter note
    eighth_ticks = ppq // 2  # 240 ticks for 480 PPQ

    # Determine position within the beat
    pos_in_beat = tick % beat_ticks
    beat_start = tick - pos_in_beat

    # Off-beat eighth note occurs at pos_in_beat == eighth_ticks
    # Allow a small tolerance window of ±10 ticks around the exact 8th note grid
    if abs(pos_in_beat - eighth_ticks) <= 10:
        # Triplet off-beat is at 2/3 of beat = beat_ticks * 2 // 3 (320 ticks)
        # Shift delta: from 240 towards 320
        max_shift = (beat_ticks * 2 // 3) - eighth_ticks  # 80 ticks
        shift = int(round(amount * max_shift))
        return beat_start + eighth_ticks + shift

    return tick


def apply_humanize(tick: int, max_delta_ticks: int, seed: int) -> int:
    """
    Applies bounded, deterministic pseudo-random humanization to a tick onset.
    Guarantees non-negative ticks.
    """
    if max_delta_ticks < 0:
        raise ValueError("max_delta_ticks must be non-negative.")
    if max_delta_ticks == 0:
        return tick

    rng = random.Random(seed ^ (tick * 1337))
    offset = rng.randint(-max_delta_ticks, max_delta_ticks)
    return max(0, tick + offset)


def validate_midi_note_on_off_pairing(
    events: List[Tuple[str, int, int, int]]
) -> List[str]:
    """
    Validates that every MIDI note_on has an exact corresponding note_off,
    even when notes overlap or repeat on the exact same pitch.
    
    events: list of tuples (event_type, tick, channel, pitch)
      where event_type in ('note_on', 'note_off')
    
    Returns list of validation error descriptions (empty if 100% valid).
    """
    errors: List[str] = []
    # Active note tracker: (channel, pitch) -> list of start_ticks
    active: Dict[Tuple[int, int], List[int]] = {}

    sorted_events = sorted(events, key=lambda e: (e[1], 0 if e[0] == 'note_off' else 1))

    for ev_type, tick, channel, pitch in sorted_events:
        key = (channel, pitch)
        if ev_type == 'note_on':
            active.setdefault(key, []).append(tick)
        elif ev_type == 'note_off':
            if key not in active or not active[key]:
                errors.append(f"Unmatched note_off at tick {tick} for pitch {pitch} on channel {channel}")
            else:
                active[key].pop(0)

    for (channel, pitch), remaining in active.items():
        if remaining:
            errors.append(
                f"Hanging note_on (missing note_off) for pitch {pitch} on channel {channel} starting at ticks {remaining}"
            )

    return errors

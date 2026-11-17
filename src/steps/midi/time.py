"""
STEPS MIDI Core: Rational MIDI Time Engine & Variable PPQ Conversion (OA-0029, M11).

Adheres to:
- MMA Standard MIDI File 1.0 Specification (Dave Oppenheim / MMA)
- Mathematical exactness using Python's fractions.Fraction to eliminate floating-point drift
- Lossless conversion across variable PPQ resolutions (96 to 1920 PPQ)
- Tuplet timing distribution (triplets 1/3, quintuplets 1/5, septuplets 1/7) without rounding drift
- Musical Bar.Beat.Tick metric coordinate representation
"""

from __future__ import annotations

import math
from dataclasses import dataclass
from fractions import Fraction
from typing import List, Optional, Tuple, Union


@dataclass(frozen=True)
class BarBeatPosition:
    """
    Musical bar, beat, and fractional subdivision coordinate.
    
    Attributes:
        bar: 1-based bar (measure) number.
        beat: 1-based beat within the bar (1..numerator).
        sub_beat: Exact rational fraction [0, 1) of the beat elapsed.
    """
    bar: int
    beat: int
    sub_beat: Fraction = Fraction(0, 1)

    def __post_init__(self) -> None:
        if self.bar < 1:
            raise ValueError(f"Bar must be >= 1, got {self.bar}")
        if self.beat < 1:
            raise ValueError(f"Beat must be >= 1, got {self.beat}")
        if not (0 <= self.sub_beat < 1):
            raise ValueError(f"sub_beat must be in [0, 1), got {self.sub_beat}")

    def format_daw(self, ppq: int = 480) -> str:
        """
        Formats position as standard DAW notation: Bar.Beat.Tick (e.g. '1.1.000' or '4.3.240').
        """
        tick_in_beat = int(round(float(self.sub_beat * ppq)))
        return f"{self.bar}.{self.beat}.{tick_in_beat:03d}"


class RationalMidiTime:
    """
    Exact rational time engine for MIDI tick calculation and multi-PPQ scaling.
    Eliminates all cumulative floating-point errors across long song timelines.
    """

    @staticmethod
    def ticks_per_beat(ppq: int, denominator: int = 4) -> int:
        """
        Calculates the number of MIDI ticks per metric beat.
        For quarter-note beat (denominator=4), beat_ticks == ppq.
        For eighth-note beat (denominator=8), beat_ticks == ppq // 2.
        """
        if ppq <= 0:
            raise ValueError(f"PPQ must be positive, got {ppq}")
        if denominator <= 0 or (denominator & (denominator - 1)) != 0:
            raise ValueError(f"Denominator must be a power of 2, got {denominator}")
        # standard SMF defines PPQ as ticks per quarter note
        # a beat has duration (4 / denominator) quarter notes
        return int(ppq * Fraction(4, denominator))

    @staticmethod
    def ticks_per_bar(ppq: int, numerator: int = 4, denominator: int = 4) -> int:
        """Calculates exact ticks in one complete musical bar."""
        return numerator * RationalMidiTime.ticks_per_beat(ppq, denominator)

    @classmethod
    def ticks_to_position(
        cls,
        abs_tick: int,
        ppq: int = 480,
        numerator: int = 4,
        denominator: int = 4,
    ) -> BarBeatPosition:
        """
        Converts absolute MIDI ticks to an exact rational BarBeatPosition.
        """
        if abs_tick < 0:
            raise ValueError(f"abs_tick must be non-negative, got {abs_tick}")

        bar_ticks = cls.ticks_per_bar(ppq, numerator, denominator)
        beat_ticks = cls.ticks_per_beat(ppq, denominator)

        bar_index = abs_tick // bar_ticks
        bar = bar_index + 1
        rem_ticks = abs_tick % bar_ticks

        beat_index = rem_ticks // beat_ticks
        beat = beat_index + 1
        sub_ticks = rem_ticks % beat_ticks

        sub_beat = Fraction(sub_ticks, beat_ticks)
        return BarBeatPosition(bar=bar, beat=beat, sub_beat=sub_beat)

    @classmethod
    def position_to_ticks(
        cls,
        pos: BarBeatPosition,
        ppq: int = 480,
        numerator: int = 4,
        denominator: int = 4,
    ) -> int:
        """
        Converts a BarBeatPosition back to absolute MIDI ticks with exact rounding.
        """
        bar_ticks = cls.ticks_per_bar(ppq, numerator, denominator)
        beat_ticks = cls.ticks_per_beat(ppq, denominator)

        total_fractional_beats = (pos.bar - 1) * numerator + (pos.beat - 1) + pos.sub_beat
        total_ticks = total_fractional_beats * beat_ticks
        return int(round(float(total_ticks)))

    @staticmethod
    def convert_ppq(ticks: int, source_ppq: int, target_ppq: int) -> int:
        """
        Converts an absolute tick count or duration from source_ppq to target_ppq
        using exact rational arithmetic with half-up rounding.
        """
        if source_ppq <= 0 or target_ppq <= 0:
            raise ValueError("PPQ values must be positive integers.")
        if ticks < 0:
            raise ValueError("Ticks must be non-negative.")
        if source_ppq == target_ppq:
            return ticks

        exact = Fraction(ticks * target_ppq, source_ppq)
        # Standard symmetric half-up rounding
        return int(math.floor(exact + Fraction(1, 2)))

    @staticmethod
    def distribute_tuplet_ticks(
        total_ticks: int,
        tuplet_count: int,
    ) -> List[Tuple[int, int]]:
        """
        Distributes total_ticks evenly across tuplet_count subdivisions
        (e.g. triplets: count=3, quintuplets: count=5, septuplets: count=7)
        using rational Bresenham accumulator to guarantee 0 cumulative drift.
        
        Returns:
            List of (start_tick_offset, duration_ticks) for each division.
        """
        if total_ticks <= 0:
            raise ValueError(f"total_ticks must be positive, got {total_ticks}")
        if tuplet_count <= 0:
            raise ValueError(f"tuplet_count must be positive, got {tuplet_count}")

        step = Fraction(total_ticks, tuplet_count)
        result: List[Tuple[int, int]] = []
        last_boundary = 0

        for i in range(1, tuplet_count + 1):
            next_boundary = int(round(float(step * i)))
            dur = next_boundary - last_boundary
            result.append((last_boundary, dur))
            last_boundary = next_boundary

        # Invariant check: sum of durations must equal total_ticks exactly
        assert sum(dur for _, dur in result) == total_ticks, "Tuplet division drift detected"
        return result

    @staticmethod
    def ticks_to_seconds(
        ticks: int,
        ppq: int = 480,
        tempo_points: Optional[List[Tuple[int, float]]] = None,
    ) -> float:
        """
        Converts MIDI ticks to absolute time in seconds, accounting for mid-sequence tempo changes.
        
        tempo_points: List of (start_tick, bpm) sorted by start_tick. Defaults to [(0, 120.0)].
        """
        if ticks < 0:
            raise ValueError(f"ticks must be non-negative, got {ticks}")
        if ppq <= 0:
            raise ValueError(f"ppq must be positive, got {ppq}")

        points = tempo_points if tempo_points else [(0, 120.0)]
        sorted_points = sorted(points, key=lambda p: p[0])

        total_seconds = Fraction(0, 1)
        cur_tick = 0

        for i, (p_tick, bpm) in enumerate(sorted_points):
            if bpm <= 0.0:
                raise ValueError(f"BPM must be positive, got {bpm}")

            next_tick = sorted_points[i + 1][0] if i + 1 < len(sorted_points) else ticks
            seg_start = max(cur_tick, p_tick)
            seg_end = min(ticks, next_tick)

            if seg_end > seg_start:
                seg_ticks = seg_end - seg_start
                # seconds per tick = 60 / (bpm * ppq)
                us_per_beat = int(round(60_000_000.0 / bpm))
                sec_fraction = Fraction(seg_ticks * us_per_beat, ppq * 1_000_000)
                total_seconds += sec_fraction
                cur_tick = seg_end

            if cur_tick >= ticks:
                break

        return float(total_seconds)


__all__ = [
    "BarBeatPosition",
    "RationalMidiTime",
]

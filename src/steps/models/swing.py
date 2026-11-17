"""
STEPS Music Domain: Swing Ratio, Micro-Timing Engine & MPC Groove Quantization (M07, OA-0022).

Adheres to:
- Prompt 10 & M07 (Rhythmik, Metrik & Micro-Timing)
- ADR-002, ADR-007
- Rule CR-027: In each binary pair (index 0, 1), the second onset (index 1) is delayed
- Golden References: REF-0020, REF-0021, REF-0177..REF-0186
- Roger Linn MPC 50%–75% Swing Model (ERR-034: 61% = Tick 146 @ 480 PPQ)
- Friberg & Sundström (2002) tempo-dependent swing decay model
- Variable PPQ resolution support (240, 480, 960 PPQ)
"""

from __future__ import annotations

import math
import random
from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .timeline import (
    DEFAULT_PPQ,
    TimelineEvent,
    apply_humanize,
)


class SwingSubdivision(str, Enum):
    """Grid resolution for binary pair subdivision."""
    EIGHTH = "8th"        # Swung 8th notes (pair span = 1 quarter note = PPQ ticks)
    SIXTEENTH = "16th"    # Swung 16th notes (pair span = 1 eighth note = PPQ // 2 ticks)


class SwingProfileType(str, Enum):
    """Canonical swing profile presets across genres."""
    STRAIGHT = "STRAIGHT"         # 50% (straight subdivision, rho = 1.0)
    MPC_54 = "MPC_54"             # 54% (subtle laid-back groove)
    MPC_57 = "MPC_57"             # 57% (Neo-Soul / Phrygian Halftime Shuffle, PAT-030)
    MPC_58 = "MPC_58"             # 58% (UK Garage 2-Step, PAT-020, PAT-023)
    MPC_61 = "MPC_61"             # 61% (Golden Era Boom-Bap MPC 3000, PAT-024)
    MPC_64 = "MPC_64"             # 64% (UK Garage Heavy Swing, PAT-026)
    TRIPLET = "TRIPLET"           # 66.67% (exact triplet swing, rho = 2.0)
    HARD_BOP = "HARD_BOP"         # Dynamic Friberg tempo-decay model (rho up to 3.5)
    CUSTOM = "CUSTOM"             # User-specified percentage or ratio


def swing_ratio_to_percentage(rho: float) -> float:
    """
    Convert swing ratio rho (t_long / t_short) into percentage (e.g. 1.0 -> 50.0%, 2.0 -> 66.67%).
    Formula: percentage = (rho / (1.0 + rho)) * 100.0.
    """
    if rho <= 0.0:
        raise ValueError(f"Swing ratio rho must be positive, got {rho}")
    return round((rho / (1.0 + rho)) * 100.0, 4)


def percentage_to_swing_ratio(percentage: float) -> float:
    """
    Convert swing percentage into swing ratio rho = t_long / t_short.
    Formula: rho = percentage / (100.0 - percentage).
    Examples:
    - 50.0% -> 1.0 (Straight, REF-0020)
    - 66.6667% -> 2.0 (Triplet, REF-0021)
    - 61.0% -> 1.5641 (Boom-Bap, PAT-024)
    """
    if not (0.0 < percentage < 100.0):
        raise ValueError(f"Swing percentage must be in range (0.0..100.0), got {percentage}")
    return round(percentage / (100.0 - percentage), 4)


def calculate_swing_quant_tick(
    ppq: int,
    ratio_or_pct: float,
    subdivision: SwingSubdivision = SwingSubdivision.SIXTEENTH
) -> int:
    """
    Computes the quantized tick position of the second onset in a binary subdivision span.
    
    Adheres strictly to Golden Reference Cases:
    - REF-0177: 480 PPQ, 0.50 -> 120 (Offset 0)
    - REF-0178: 480 PPQ, 0.61 -> 146 (ERR-034: round(240 * 0.61) = 146)
    - REF-0181: 960 PPQ, 0.61 -> 293 (round(480 * 0.61) = 293)
    - REF-0183: 240 PPQ, 0.61 -> 73 (round(120 * 0.61) = 73)
    - REF-0185: 480 PPQ, 0.57 -> 137 (round(240 * 0.57) = 137)
    - REF-0186: 480 PPQ, 2/3 -> 160 (round(240 * 2/3) = 160)
    """
    if ppq <= 0:
        raise ValueError(f"ppq must be positive, got {ppq}")

    span = ppq if subdivision == SwingSubdivision.EIGHTH else ppq // 2

    factor = ratio_or_pct
    if factor > 1.0:
        if factor > 3.5:
            # Interpreted as percentage (e.g. 61.0)
            factor = factor / 100.0
        else:
            # Interpreted as swing ratio rho (e.g. 2.0 or 1.0)
            factor = factor / (1.0 + factor)

    return round(span * factor)


def calculate_swing_offset_ticks(
    ppq: int,
    ratio_or_pct: float,
    subdivision: SwingSubdivision = SwingSubdivision.SIXTEENTH
) -> int:
    """
    Computes the signed tick displacement relative to straight binary timing.
    
    Adheres to Golden Reference Cases:
    - REF-0179: 480 PPQ, 61% -> +26 ticks (146 - 120 = 26)
    - REF-0182: 960 PPQ, 61% -> +53 ticks (293 - 240 = 53)
    - REF-0184: 240 PPQ, 61% -> +13 ticks (73 - 60 = 13)
    """
    quant_tick = calculate_swing_quant_tick(ppq, ratio_or_pct, subdivision)
    span = ppq if subdivision == SwingSubdivision.EIGHTH else ppq // 2
    straight_tick = span // 2
    return quant_tick - straight_tick


def ticks_to_milliseconds(offset_ticks: int, bpm: float, ppq: int = DEFAULT_PPQ) -> float:
    """
    Converts tick displacement into wall-clock milliseconds.
    
    Adheres to:
    - REF-0180: offset=26 ticks @ 90 BPM & 480 PPQ -> 36.11 ms
    """
    if bpm <= 0.0 or ppq <= 0:
        raise ValueError(f"bpm and ppq must be positive, got bpm={bpm}, ppq={ppq}")
    # 1 quarter note = 60_000 ms / bpm. 1 tick = (60_000 ms / bpm) / ppq.
    return round(offset_ticks * 60_000.0 / (bpm * ppq), 2)


def milliseconds_to_ticks(ms: float, bpm: float, ppq: int = DEFAULT_PPQ) -> int:
    """Converts milliseconds delay into the closest integer tick offset."""
    if bpm <= 0.0 or ppq <= 0:
        raise ValueError(f"bpm and ppq must be positive, got bpm={bpm}, ppq={ppq}")
    return int(round(ms * bpm * ppq / 60_000.0))


def friberg_swing_ratio(bpm: float) -> float:
    """
    Calculates tempo-dependent jazz swing ratio according to Friberg & Sundström (2002).
    Swing ratio rho is high at relaxed tempos (up to 3.5:1 at 90-100 BPM) and
    decreases linearly towards 1.0:1 (straight) at high bebop tempos (240+ BPM).
    """
    if bpm <= 0.0:
        raise ValueError(f"BPM must be positive, got {bpm}")
    # Empirical regression: rho = 4.0 - 0.0125 * BPM, bounded to [1.0..3.5]
    rho = 4.0 - (0.0125 * bpm)
    return round(max(1.0, min(3.5, rho)), 2)


@dataclass(frozen=True)
class SwingProfile:
    """Complete specification of a genre swing profile."""
    name: str
    profile_type: SwingProfileType
    subdivision: SwingSubdivision
    percentage: float
    ratio: float
    description: str

    def get_offset_ticks(self, ppq: int = DEFAULT_PPQ) -> int:
        """Calculate signed tick offset at the given PPQ resolution."""
        return calculate_swing_offset_ticks(ppq, self.percentage, self.subdivision)

    def get_quant_tick(self, ppq: int = DEFAULT_PPQ) -> int:
        """Calculate absolute onset tick within the pair span."""
        return calculate_swing_quant_tick(ppq, self.percentage, self.subdivision)

    def get_delay_ms(self, bpm: float, ppq: int = DEFAULT_PPQ) -> float:
        """Calculate delay in milliseconds for a specific tempo."""
        return ticks_to_milliseconds(self.get_offset_ticks(ppq), bpm, ppq)


# Canonical Swing Presets
SWING_PRESETS: Dict[SwingProfileType, SwingProfile] = {
    SwingProfileType.STRAIGHT: SwingProfile(
        name="Straight (1:1)",
        profile_type=SwingProfileType.STRAIGHT,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=50.0,
        ratio=1.0,
        description="Even subdivision with zero timing displacement (REF-0020, REF-0177)."
    ),
    SwingProfileType.MPC_54: SwingProfile(
        name="MPC 54% Subtle Swing",
        profile_type=SwingProfileType.MPC_54,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=54.0,
        ratio=percentage_to_swing_ratio(54.0),
        description="Subtle humanized laid-back groove common in contemporary R&B and house."
    ),
    SwingProfileType.MPC_57: SwingProfile(
        name="Neo-Soul 57% Halftime Shuffle",
        profile_type=SwingProfileType.MPC_57,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=57.0,
        ratio=percentage_to_swing_ratio(57.0),
        description="57% swing quantizing tick 137 at 480 PPQ (PAT-030, REF-0185)."
    ),
    SwingProfileType.MPC_58: SwingProfile(
        name="UK Garage 58% 2-Step",
        profile_type=SwingProfileType.MPC_58,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=58.0,
        ratio=percentage_to_swing_ratio(58.0),
        description="58% swing quantizing tick 139 at 480 PPQ (PAT-020, PAT-023, CDR-016)."
    ),
    SwingProfileType.MPC_61: SwingProfile(
        name="Golden Era 61% Boom-Bap",
        profile_type=SwingProfileType.MPC_61,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=61.0,
        ratio=percentage_to_swing_ratio(61.0),
        description="Classic Roger Linn 61% swing quantizing tick 146 (+26 ticks @ 480 PPQ, PAT-024, REF-0178)."
    ),
    SwingProfileType.MPC_64: SwingProfile(
        name="UK Garage 64% Heavy Shuffle",
        profile_type=SwingProfileType.MPC_64,
        subdivision=SwingSubdivision.SIXTEENTH,
        percentage=64.0,
        ratio=percentage_to_swing_ratio(64.0),
        description="64% swing quantizing tick 154 (+34 ticks @ 480 PPQ, PAT-026)."
    ),
    SwingProfileType.TRIPLET: SwingProfile(
        name="Triplet Swing (2:1)",
        profile_type=SwingProfileType.TRIPLET,
        subdivision=SwingSubdivision.EIGHTH,
        percentage=66.6667,
        ratio=2.0,
        description="Traditional jazz triplet swing with 2:1 duration ratio (REF-0021, REF-0186)."
    ),
}


class SwingEngine:
    """
    Deterministic swing and micro-timing engine for MIDI events and drum grids.
    
    Implements rule CR-027: In each binary pair, the second onset (odd index)
    is delayed by the swing offset, while the first onset (downbeat) remains anchored.
    """

    def __init__(
        self,
        ppq: int = DEFAULT_PPQ,
        subdivision: SwingSubdivision = SwingSubdivision.SIXTEENTH,
        swing_ratio: float = 1.0,
        percentage: Optional[float] = None,
        humanize_max_ticks: int = 0,
        seed: Optional[int] = None,
    ) -> None:
        self.ppq = ppq
        self.subdivision = subdivision

        if percentage is not None:
            self.percentage = float(percentage)
            self.swing_ratio = percentage_to_swing_ratio(self.percentage)
        else:
            self.swing_ratio = float(swing_ratio)
            self.percentage = swing_ratio_to_percentage(self.swing_ratio)

        self.humanize_max_ticks = humanize_max_ticks
        self.seed = seed

    @property
    def span_ticks(self) -> int:
        """Total duration of one binary pair in ticks."""
        return self.ppq if self.subdivision == SwingSubdivision.EIGHTH else self.ppq // 2

    @property
    def straight_step_ticks(self) -> int:
        """Straight duration of an individual subdivision step."""
        return self.span_ticks // 2

    @property
    def offset_ticks(self) -> int:
        """Signed displacement for the swung second onset."""
        return calculate_swing_offset_ticks(self.ppq, self.percentage, self.subdivision)

    @property
    def quant_tick(self) -> int:
        """Position of second onset within its pair span."""
        return calculate_swing_quant_tick(self.ppq, self.percentage, self.subdivision)

    def apply_to_tick(self, tick: int) -> int:
        """
        Applies swing displacement to an individual onset tick.
        If the tick lies on a second onset (odd subdivision position), it is shifted by offset_ticks.
        """
        span = self.span_ticks
        straight = self.straight_step_ticks
        pos_in_span = tick % span
        base_tick = tick - pos_in_span

        # Toleranzfenster ±10 Ticks um die ungeswingte Position
        if abs(pos_in_span - straight) <= 10:
            swung_tick = base_tick + self.quant_tick
        else:
            swung_tick = tick

        if self.humanize_max_ticks > 0 and self.seed is not None:
            swung_tick = apply_humanize(swung_tick, self.humanize_max_ticks, self.seed + tick)

        return max(0, swung_tick)

    def apply_to_events(self, events: List[TimelineEvent]) -> List[TimelineEvent]:
        """
        Applies swing to a sequence of TimelineEvents non-destructively.
        Returns a newly allocated list of shifted TimelineEvents.
        """
        result: List[TimelineEvent] = []
        for ev in events:
            new_start = self.apply_to_tick(ev.start_tick)
            result.append(
                TimelineEvent(
                    event_id=ev.event_id,
                    track_id=ev.track_id,
                    event_type=ev.event_type,
                    start_tick=new_start,
                    duration_ticks=ev.duration_ticks,
                    payload=ev.payload,
                    source_id=ev.source_id,
                )
            )
        result.sort(key=lambda e: e.start_tick)
        return result

    def get_grid_ticks(self, num_steps: int = 16) -> List[int]:
        """Returns the complete sequence of tick positions for a swung step grid."""
        straight_step = self.straight_step_ticks
        grid = [i * straight_step for i in range(num_steps)]
        return [self.apply_to_tick(t) for t in grid]

    def to_profile(self, name: str = "Custom Swing") -> SwingProfile:
        """Export current settings as a SwingProfile."""
        return SwingProfile(
            name=name,
            profile_type=SwingProfileType.CUSTOM,
            subdivision=self.subdivision,
            percentage=self.percentage,
            ratio=self.swing_ratio,
            description=f"Swing {self.percentage:.1f}% (rho={self.swing_ratio:.2f}) on {self.subdivision.value}",
        )

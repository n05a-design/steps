"""Compare two concrete voicings for keyboard display.

Voice pairing follows the existing core contract used by
``ProgressionSession.analyze_progression`` and the Voice Leading Lab: voices are
paired by register order (bass to soprano) and only when both voicings have the
same number of voices. With different voice counts no one-to-one mapping is
forced; only held pitches, added and removed pitches are reported.

Per-voice motion size uses the signed distance from ``theory.interval``;
contrapuntal motion classes come from ``theory.voice_leading``.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Iterable, Optional

from ..progression.voice_leading import absolute_semitone_distance
from ..theory.interval import directed_semitones
from ..theory.voice_leading import classify_voice_motion
from .model import sorted_unique_notes


class MotionKind(str, Enum):
    HELD = "HELD"  # same MIDI pitch
    SEMITONE = "SEMITONE"
    WHOLE_TONE = "WHOLE_TONE"
    LEAP = "LEAP"  # three or more semitones


class Direction(str, Enum):
    UP = "UP"
    DOWN = "DOWN"
    NONE = "NONE"


@dataclass(frozen=True)
class VoiceMotion:
    voice: int  # 0 = bass
    start: int
    end: int
    semitones: int  # signed
    direction: Direction
    kind: MotionKind


@dataclass(frozen=True)
class VoicingComparison:
    start: tuple[int, ...]
    end: tuple[int, ...]
    paired: bool  # True when voices were paired one-to-one by register
    motions: tuple[VoiceMotion, ...]
    held_pitches: tuple[int, ...]  # identical MIDI pitch in both chords
    common_pitch_classes_moved: tuple[int, ...]  # pitch class shared but sounding in another octave
    added_pitches: tuple[int, ...]
    removed_pitches: tuple[int, ...]
    total_movement: Optional[int]  # L1 distance, only for paired voicings
    outer_voice_motion: Optional[str]  # ContrapuntalMotion value for bass/soprano


def _kind(semitones: int) -> MotionKind:
    size = abs(semitones)
    if size == 0:
        return MotionKind.HELD
    if size == 1:
        return MotionKind.SEMITONE
    if size == 2:
        return MotionKind.WHOLE_TONE
    return MotionKind.LEAP


def compare_voicings(start: Iterable[int], end: Iterable[int]) -> VoicingComparison:
    a = sorted_unique_notes(start)
    b = sorted_unique_notes(end)
    held = tuple(sorted(set(a) & set(b)))
    added = tuple(n for n in b if n not in a)
    removed = tuple(n for n in a if n not in b)
    moved_common = tuple(sorted(
        {n % 12 for n in removed} & {n % 12 for n in added}
    ))
    paired = bool(a) and len(a) == len(b)
    motions: list[VoiceMotion] = []
    total = None
    outer = None
    if paired:
        for voice, (x, y) in enumerate(zip(a, b, strict=True)):
            step = directed_semitones(x, y)
            direction = Direction.UP if step > 0 else Direction.DOWN if step < 0 else Direction.NONE
            motions.append(VoiceMotion(voice, x, y, step, direction, _kind(step)))
        total = absolute_semitone_distance(list(a), list(b))
        if len(a) >= 2:
            outer = classify_voice_motion(a[0], b[0], a[-1], b[-1]).value
    return VoicingComparison(a, b, paired, tuple(motions), held, moved_common, added, removed, total, outer)


__all__ = ["Direction", "MotionKind", "VoiceMotion", "VoicingComparison", "compare_voicings"]

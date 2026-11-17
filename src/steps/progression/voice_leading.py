"""
STEPS Progression Core: Voice Leading Metrics, Invariants, Styles & Optimizers.

Adheres to:
- M06 (Stimmführung, Kontrapunkt, Parallelen-Prüfung, Tymoczko L1-Distanz)
- Golden Reference Cases: REF-0019, REF-0023..0026, REF-0065, REF-0095..0097
- Tymoczko, Dmitri (2011): A Geometry of Music (Harmonic & Voice-Leading Spaces)
"""

from __future__ import annotations
from enum import Enum
from typing import Any, Dict, List, Optional, Tuple, Union

from ..theory.exceptions import VoiceLeadingError
from ..theory.voice_leading import (
    ContrapuntalMotion,
    VoiceLeadingEvaluation,
    VoiceLeadingStyle,
    VoiceLeadingViolation,
    analyze_contrapuntal_motions,
    classify_voice_motion,
    detect_parallel_fifths_octaves,
    detect_voice_crossing,
    detect_voice_overlap,
    evaluate_voice_leading_transition,
)


def absolute_semitone_distance(voicing_a: list[int], voicing_b: list[int]) -> int:
    """
    Computes absolute L1 semitone distance between two voice-leading vectors:
    dist = sum(|v_b[i] - v_a[i]|) for all voices i.
    """
    if len(voicing_a) != len(voicing_b):
        raise VoiceLeadingError(f"Voice count mismatch: {len(voicing_a)} != {len(voicing_b)}")
    return sum(abs(b - a) for a, b in zip(voicing_a, voicing_b))


def circular_pc_distance(voicing_a: list[int], voicing_b: list[int]) -> int:
    """
    Computes Tymoczko's circular pitch-class distance on the Z12 circle:
    dist = sum(min(|pc_b - pc_a|, 12 - |pc_b - pc_a|))
    """
    if len(voicing_a) != len(voicing_b):
        raise VoiceLeadingError(f"Voice count mismatch: {len(voicing_a)} != {len(voicing_b)}")
    
    total = 0
    for a, b in zip(voicing_a, voicing_b):
        diff = abs((b % 12) - (a % 12))
        total += min(diff, 12 - diff)
    return total


def guide_tone_resolution(seventh_midi: int, target_third_midi: int) -> int:
    """
    Computes semitone displacement for standard jazz guide-tone resolution:
    The 7th of a dominant chord resolves step-wise (typically down by half step)
    to the 3rd of the target tonic chord.
    
    Returns:
        Signed semitone difference (target - source).
    """
    return target_third_midi - seventh_midi


def optimize_smooth_voice_leading(
    source_voicing: list[int],
    target_pcs: set[int] | list[int],
    bass_pc: Optional[int] = None,
    style: VoiceLeadingStyle = VoiceLeadingStyle.JAZZ_POP
) -> list[int]:
    """Minimize L1 movement within one octave per voice and MIDI range.

    Returns strictly ascending voices covering all target pitch classes.
    Raises VoiceLeadingError when the requested constraints cannot be met.
    """
    if not source_voicing or any(not isinstance(note, int) or isinstance(note, bool) or not 0 <= note <= 127 for note in source_voicing):
        raise VoiceLeadingError("Source voicing must contain MIDI notes in 0..127.")
    if any(a >= b for a, b in zip(source_voicing, source_voicing[1:])):
        raise VoiceLeadingError("Source voicing must be strictly ascending.")
    if not target_pcs or any(not isinstance(pc, int) or isinstance(pc, bool) or not 0 <= pc <= 11 for pc in target_pcs):
        raise VoiceLeadingError("Target voicing requires integer pitch classes in 0..11.")
    if bass_pc is not None and (not isinstance(bass_pc, int) or isinstance(bass_pc, bool) or not 0 <= bass_pc <= 11):
        raise VoiceLeadingError("Bass pitch class must be an integer in 0..11.")

    target = set(target_pcs)
    bass = bass_pc
    if len(target) > len(source_voicing):
        raise VoiceLeadingError(f"{len(target)} target pitch classes exceed the voice count.")
    if bass is not None and bass not in target:
        raise VoiceLeadingError("Bass pitch class is absent from the target voicing.")

    candidates = [
        [
            note for note in range(max(0, center - 12), min(127, center + 12) + 1)
            if note % 12 in target and (index != 0 or bass is None or note % 12 == bass)
        ]
        for index, center in enumerate(source_voicing)
    ]
    best: tuple[int, ...] | None = None
    best_distance = float("inf")

    # Prune partial assignments that already cross voices or exceed the best cost.
    def search(notes: tuple[int, ...], remaining: set[int], distance: int) -> None:
        nonlocal best, best_distance
        index = len(notes)
        if distance >= best_distance or len(remaining) > len(candidates) - index:
            return
        if index == len(candidates):
            if not detect_parallel_fifths_octaves(source_voicing, list(notes), style):
                best, best_distance = notes, distance
            return
        for note in candidates[index]:
            if not notes or note > notes[-1]:
                search(notes + (note,), remaining - {note % 12}, distance + abs(note - source_voicing[index]))

    search((), target, 0)
    if best is None:
        raise VoiceLeadingError("No voicing satisfies the constraints within one octave per voice.")
    return list(best)


__all__ = [
    "VoiceLeadingStyle",
    "ContrapuntalMotion",
    "VoiceLeadingViolation",
    "VoiceLeadingEvaluation",
    "classify_voice_motion",
    "analyze_contrapuntal_motions",
    "detect_voice_crossing",
    "detect_voice_overlap",
    "detect_parallel_fifths_octaves",
    "evaluate_voice_leading_transition",
    "absolute_semitone_distance",
    "circular_pc_distance",
    "guide_tone_resolution",
    "optimize_smooth_voice_leading",
]

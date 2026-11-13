"""
STEPS Progression Core: Voice Leading Metrics, Invariants, Styles & Optimizers.

Adheres to:
- M06 (Stimmführung, Kontrapunkt, Parallelen-Prüfung, Tymoczko L1-Distanz)
- Golden Reference Cases: REF-0019, REF-0023..0026, REF-0065, REF-0095..0097
- Tymoczko, Dmitri (2011): A Geometry of Music (Harmonic & Voice-Leading Spaces)
"""

from __future__ import annotations
from enum import Enum
from typing import Optional

from ..theory.exceptions import VoiceLeadingError


class VoiceLeadingStyle(Enum):
    STRICT_COUNTERPOINT = 'STRICT_COUNTERPOINT'  # Strict classical 4-part rules (no parallel 5ths/8ths)
    JAZZ_POP = 'JAZZ_POP'                        # Smooth minimal movement, guide-tones, planing permitted


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


def detect_voice_crossing(voicing: list[int]) -> bool:
    """Detect crossing in voice order. A unison is not a crossing."""
    return any(lower > upper for lower, upper in zip(voicing, voicing[1:]))


def detect_voice_overlap(voicing_a: list[int], voicing_b: list[int]) -> bool:
    """
    Checks for voice overlap between two consecutive voicings:
    A lower voice moves higher than the previous pitch of a higher voice,
    or a higher voice moves lower than the previous pitch of a lower voice.
    """
    if len(voicing_a) != len(voicing_b):
        raise VoiceLeadingError("Voicings must have equal voice count.")
    n = len(voicing_a)
    for i in range(n):
        for j in range(i + 1, n):
            # Voice i is lower than Voice j in chord A
            if voicing_b[i] > voicing_a[j] or voicing_b[j] < voicing_a[i]:
                return True
    return False


def detect_parallel_fifths_octaves(
    chord_a: list[int],
    chord_b: list[int],
    style: VoiceLeadingStyle = VoiceLeadingStyle.STRICT_COUNTERPOINT
) -> list[str]:
    """Report perfect parallels and contrary outer-voice intervals in strict style.

    JAZZ_POP permits both forms of movement. Input order assigns voice identity.
    """
    if len(chord_a) != len(chord_b):
        raise VoiceLeadingError("Chords must have identical voice count.")
    if style != VoiceLeadingStyle.STRICT_COUNTERPOINT:
        return []
    violations = []
    for low in range(len(chord_a)):
        for high in range(low + 1, len(chord_a)):
            before = abs(chord_a[high] - chord_a[low]) % 12
            after = abs(chord_b[high] - chord_b[low]) % 12
            if before != after or before not in (0, 7):
                continue
            motion = (chord_b[low] - chord_a[low]) * (chord_b[high] - chord_a[high])
            label = "octave/unison" if before == 0 else "fifth"
            if motion > 0:
                violations.append(f"Parallel {label} between voice {low} and {high}")
            elif motion < 0 and low == 0 and high == len(chord_a) - 1:
                violations.append(f"Contrary {label} between outer voices {low} and {high}")
    return violations


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

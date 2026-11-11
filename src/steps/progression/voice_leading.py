"""
STEPS Progression Core: Voice Leading Metrics, Invariants, Styles & Optimizers.

Adheres to:
- M06 (Stimmführung, Kontrapunkt, Parallelen-Prüfung, Tymoczko L1-Distanz)
- Golden Reference Cases: REF-0019, REF-0023..0026, REF-0065, REF-0095..0097
- Tymoczko, Dmitri (2011): A Geometry of Music (Harmonic & Voice-Leading Spaces)
"""

from __future__ import annotations
from enum import Enum
from typing import List, Tuple, Dict, Optional, Set
import itertools

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
    """
    Checks if a voicing contains voice crossing:
    Returns True if any lower voice i has pitch >= voice i+1 (strict ascending order violated).
    """
    for i in range(len(voicing) - 1):
        if voicing[i] >= voicing[i + 1]:
            return True
    return False


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
    """
    Detects parallel fifths (7 semitones) and octaves (0/12 semitones) between
    any two voices moving in the same direction.
    
    In JAZZ_POP style, parallel movement (planing) is acknowledged but marked as non-violating.
    """
    if len(chord_a) != len(chord_b):
        raise VoiceLeadingError("Chords must have identical voice count.")
    
    violations = []
    n_voices = len(chord_a)
    
    for i in range(n_voices):
        for j in range(i + 1, n_voices):
            # Interval in chord_a
            int_a = abs(chord_a[j] - chord_a[i]) % 12
            # Interval in chord_b
            int_b = abs(chord_b[j] - chord_b[i]) % 12
            
            # Motion of both voices
            delta_i = chord_b[i] - chord_a[i]
            delta_j = chord_b[j] - chord_a[j]
            
            # Parallel motion in same direction
            if delta_i != 0 and delta_j != 0 and (delta_i * delta_j > 0):
                # Parallel octaves / unisons
                if int_a == 0 and int_b == 0:
                    msg = f"Parallel octave/unison between voice {i} and {j}"
                    if style == VoiceLeadingStyle.STRICT_COUNTERPOINT:
                        violations.append(msg)
                # Parallel fifths
                elif int_a == 7 and int_b == 7:
                    msg = f"Parallel fifth between voice {i} and {j}"
                    if style == VoiceLeadingStyle.STRICT_COUNTERPOINT:
                        violations.append(msg)
                        
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
    """
    Deterministically finds the optimal voicing permutation for target_pcs that:
    1. Minimizes total L1 semitone distance from source_voicing.
    2. Strictly avoids voice crossing (v0 < v1 < v2 < ...).
    3. If style is STRICT_COUNTERPOINT, rejects parallel 5ths and octaves.
    4. If bass_pc is given, constrains the lowest voice to bass_pc.
    """
    n_voices = len(source_voicing)
    unique_target_pcs = list({pc % 12 for pc in target_pcs})
    
    if len(unique_target_pcs) > n_voices:
        raise VoiceLeadingError(
            f"Target pitch class set has {len(unique_target_pcs)} elements, exceeding voice count {n_voices}."
        )

    # Candidate pitches for each voice: search around source_voicing[i] +/- 12 semitones
    possible_pitches_per_voice: list[list[int]] = []
    for base_pitch in source_voicing:
        candidates = []
        for semi_offset in range(-12, 13):
            candidate = base_pitch + semi_offset
            if (candidate % 12) in unique_target_pcs:
                candidates.append(candidate)
        possible_pitches_per_voice.append(candidates)

    best_voicing: Optional[list[int]] = None
    best_distance = float('inf')

    # Carthesian product of candidate assignments
    for combo in itertools.product(*possible_pitches_per_voice):
        voicing = list(combo)
        
        # 1. No voice crossing
        if detect_voice_crossing(voicing):
            continue
            
        # 2. Check if all target PCs are covered
        voicing_pcs = {p % 12 for p in voicing}
        if not set(unique_target_pcs).issubset(voicing_pcs):
            continue
            
        # 3. Check bass note constraint if specified
        if bass_pc is not None and (voicing[0] % 12) != (bass_pc % 12):
            continue
            
        # 4. Strict counterpoint rules
        if style == VoiceLeadingStyle.STRICT_COUNTERPOINT:
            if detect_parallel_fifths_octaves(source_voicing, voicing, style):
                continue
                
        # 5. Measure L1 distance
        dist = absolute_semitone_distance(source_voicing, voicing)
        if dist < best_distance:
            best_distance = dist
            best_voicing = voicing

    if best_voicing is None:
        # Fallback: construct standard close voicing matching target_pcs
        sorted_pcs = sorted(list(unique_target_pcs))
        base_octave = source_voicing[0] // 12
        fallback = [base_octave * 12 + pc for pc in sorted_pcs]
        # Pad if n_voices > len(pcs) with octave doubling of bass
        while len(fallback) < n_voices:
            fallback.append(fallback[0] + 12)
        return sorted(fallback)

    return best_voicing


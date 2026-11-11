"""
STEPS Progression Core: Voice Leading Metrics, Invariants & Constraint Checkers.

Adheres to:
- M06 (Stimmführung, Kontrapunkt, Parallelen-Prüfung, Tymoczko L1-Distanz)
- Golden Reference Cases: REF-0019, REF-0023..0026, REF-0065, REF-0095..0097
- Tymoczko, Dmitri (2011): A Geometry of Music
"""

from __future__ import annotations
from typing import List, Tuple, Dict

def absolute_semitone_distance(voicing_a: list[int], voicing_b: list[int]) -> int:
    """
    Computes absolute L1 semitone distance between two voice-leading vectors:
    dist = sum(|v_b[i] - v_a[i]|) for all voices i.
    """
    if len(voicing_a) != len(voicing_b):
        raise ValueError(f"Voice count mismatch: {len(voicing_a)} != {len(voicing_b)}")
    return sum(abs(b - a) for a, b in zip(voicing_a, voicing_b))


def circular_pc_distance(voicing_a: list[int], voicing_b: list[int]) -> int:
    """
    Computes Tymoczko's circular pitch-class distance on the Z12 circle:
    dist = sum(min(|pc_b - pc_a|, 12 - |pc_b - pc_a|))
    """
    if len(voicing_a) != len(voicing_b):
        raise ValueError(f"Voice count mismatch: {len(voicing_a)} != {len(voicing_b)}")
    
    total = 0
    for a, b in zip(voicing_a, voicing_b):
        diff = abs((b % 12) - (a % 12))
        total += min(diff, 12 - diff)
    return total


def detect_voice_crossing(voicing: list[int]) -> bool:
    """
    Checks if a voicing contains voice crossing:
    Returns True if any lower voice i has pitch > voice i+1.
    """
    for i in range(len(voicing) - 1):
        if voicing[i] > voicing[i + 1]:
            return True
    return False


def detect_parallel_fifths_octaves(chord_a: list[int], chord_b: list[int]) -> list[str]:
    """
    Detects parallel fifths (7 semitones) and octaves (0/12 semitones) between
    any two voices moving in the same direction in strict 4-part contrapuntal writing.
    
    Returns:
        List of violation descriptions, e.g. ["Parallel fifth between voice 0 and 2"].
    """
    if len(chord_a) != len(chord_b):
        raise ValueError("Chords must have identical voice count.")
    
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
                    violations.append(f"Parallel octave/unison between voice {i} and {j}")
                # Parallel fifths
                elif int_a == 7 and int_b == 7:
                    violations.append(f"Parallel fifth between voice {i} and {j}")
                    
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

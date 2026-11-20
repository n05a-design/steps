"""
STEPS Theory Core: Voice Leading Rules, Contrapuntal Motions & Stylistic Frameworks (M06 / OA-0026).

Adheres to:
- M06 (Stimmführung, Kontrapunkt, Parallelen-Prüfung, Tymoczko L1-Distanz)
- Fux, Johann Joseph (1725): Gradus ad Parnassum (Strict Species Counterpoint)
- Aldwell, Edward & Schachter, Carl (1989): Harmony and Voice Leading (Chapters 4–5)
- Everett, Walter (2008/2009): The Foundations of Rock (Oxford University Press) – Parallel Planing & Power Chords
- Tymoczko, Dmitri (2011): A Geometry of Music (Harmonic & Voice-Leading Spaces)
- Fixes ERR-009: Stylistic differentiation between strict classical rules and contemporary pop/rock idioms.
"""

from __future__ import annotations

from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .exceptions import VoiceLeadingError


class VoiceLeadingStyle(str, Enum):
    """
    Stylistic framework governing voice-leading rules and constraints.
    
    Differentiates strict classical counterpoint from contemporary pop, rock power-chords,
    and modern jazz quartal harmony (OA-0026).
    """
    STRICT_CLASSICAL = "STRICT_CLASSICAL"        # Strict classical counterpoint (parallel 5ths/8ths forbidden)
    STRICT_COUNTERPOINT = "STRICT_COUNTERPOINT"  # Canonical alias for STRICT_CLASSICAL
    CONTEMPORARY_POP = "CONTEMPORARY_POP"        # Modern pop/rock/jazz: parallel 5ths permitted, minimal L1 favored
    JAZZ_POP = "JAZZ_POP"                        # Canonical alias for CONTEMPORARY_POP
    POWER_CHORDS = "POWER_CHORDS"                # Rock/Metal: parallel 5ths and octaves are defining stylistic idioms (Everett)
    QUARTAL_JAZZ = "QUARTAL_JAZZ"                # Modern jazz: quartal harmony, 4th intervals and planing permitted

    @property
    def is_strict_counterpoint(self) -> bool:
        """True if the style enforces strict prohibition of parallel fifths and octaves."""
        return self in (VoiceLeadingStyle.STRICT_CLASSICAL, VoiceLeadingStyle.STRICT_COUNTERPOINT)

    @property
    def allows_parallel_fifths(self) -> bool:
        """True if the style permits parallel fifth progressions."""
        return self in (
            VoiceLeadingStyle.CONTEMPORARY_POP,
            VoiceLeadingStyle.JAZZ_POP,
            VoiceLeadingStyle.POWER_CHORDS,
            VoiceLeadingStyle.QUARTAL_JAZZ
        )

    @property
    def allows_parallel_octaves(self) -> bool:
        """True if the style permits parallel octave progressions."""
        return self in (
            VoiceLeadingStyle.CONTEMPORARY_POP,
            VoiceLeadingStyle.JAZZ_POP,
            VoiceLeadingStyle.POWER_CHORDS,
            VoiceLeadingStyle.QUARTAL_JAZZ
        )

    @property
    def is_power_chord_style(self) -> bool:
        """True if the style treats parallel fifths/octaves as primary structural sonorities (planing)."""
        return self == VoiceLeadingStyle.POWER_CHORDS

    @property
    def reference_framework(self) -> str:
        """Authoritative musicological and theoretical reference for this style."""
        if self.is_strict_counterpoint:
            return "Fux (1725) Gradus ad Parnassum; Aldwell & Schachter (1989) Harmony and Voice Leading"
        elif self == VoiceLeadingStyle.POWER_CHORDS:
            return "Walter Everett (2008/2009) The Foundations of Rock (Parallel Planing)"
        elif self == VoiceLeadingStyle.QUARTAL_JAZZ:
            return "Modern Jazz Harmony; Quartal Planing (McCoy Tyner)"
        else:
            return "Contemporary Popular Harmony; Walter Everett (2008/2009) The Foundations of Rock; Tymoczko (2011) Minimal L1 Distance"

    @property
    def description(self) -> str:
        """Concise pedagogical description of the stylistic framework."""
        if self.is_strict_counterpoint:
            return "Strenger historischer Kontrapunkt: Parallele reine Quinten und Oktaven sind strikt verboten."
        elif self == VoiceLeadingStyle.POWER_CHORDS:
            return "Rock / Power-Chords: Parallele Verschiebung von reinen Quinten und Oktaven ist ein definierendes Stilmerkmal."
        elif self == VoiceLeadingStyle.QUARTAL_JAZZ:
            return "Modern Jazz / Quartenharmonik: Quarten-Schichtung und Quarten-Planing sind stilistisch legitim."
        else:
            return "Zeitgenössischer Pop / Jazz: Sanfte Stimmführung mit minimalem Handweg; parallele Fortschreitungen sind erlaubt."


class ContrapuntalMotion(str, Enum):
    """
    Relative contrapuntal motion classification between two voices.
    Adheres to Fux (1725), Aldwell & Schachter (1989), and CLM-0051 (OA-0021).
    """
    PARALLEL = "PARALLEL"  # Both voices move in the same direction by the exact same interval
    SIMILAR = "SIMILAR"    # Both voices move in the same direction by different intervals
    CONTRARY = "CONTRARY"  # Voices move in opposite directions (one up, one down)
    OBLIQUE = "OBLIQUE"    # Exactly one voice moves while the other remains on the same pitch
    STATIC = "STATIC"      # Both voices remain on the same pitch


@dataclass(frozen=True)
class VoiceLeadingViolation:
    """
    Detailed violation report of a voice-leading rule within a specific stylistic context.
    """
    rule_name: str
    voice_indices: Tuple[int, int]
    motion_type: str
    pitch_interval: int
    from_pitches: Tuple[int, int]
    to_pitches: Tuple[int, int]
    severity: Literal["ERROR", "WARNING", "INFO"]
    explanation: str
    stylistic_context: str

    @property
    def violation_type(self) -> str:
        """Alias for rule_name."""
        return self.rule_name

    @property
    def rule_source(self) -> str:
        """Alias for stylistic_context."""
        return self.stylistic_context

    def to_dict(self) -> Dict[str, Any]:
        return {
            "rule_name": self.rule_name,
            "voice_indices": list(self.voice_indices),
            "motion_type": self.motion_type,
            "pitch_interval": self.pitch_interval,
            "from_pitches": list(self.from_pitches),
            "to_pitches": list(self.to_pitches),
            "severity": self.severity,
            "explanation": self.explanation,
            "stylistic_context": self.stylistic_context,
        }


@dataclass(frozen=True)
class VoiceLeadingEvaluation:
    """
    Comprehensive stylistic evaluation of the transition between two chord voicings.
    """
    from_voicing: Tuple[int, ...]
    to_voicing: Tuple[int, ...]
    style: VoiceLeadingStyle
    is_valid: bool
    violations: List[VoiceLeadingViolation]
    l1_distance: int
    max_voice_leap: int
    contrapuntal_motion: Dict[str, Any]
    stylistic_notes: List[str]

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_voicing": list(self.from_voicing),
            "to_voicing": list(self.to_voicing),
            "style": self.style.value,
            "is_valid": self.is_valid,
            "violations": [v.to_dict() for v in self.violations],
            "l1_distance": self.l1_distance,
            "max_voice_leap": self.max_voice_leap,
            "contrapuntal_motion": self.contrapuntal_motion,
            "stylistic_notes": list(self.stylistic_notes),
        }


def classify_voice_motion(
    v1_start: int,
    v1_end: int,
    v2_start: int,
    v2_end: int
) -> ContrapuntalMotion:
    """
    Classifies the relative contrapuntal motion between two voices moving from start to end MIDI pitches.
    
    Adheres to:
    - CLM-0051 / Fux (1725) Gradus ad Parnassum
    - Aldwell & Schachter (1989) Harmony and Voice Leading
    """
    if any(type(x) is not int or isinstance(x, bool) or not 0 <= x <= 127 for x in (v1_start, v1_end, v2_start, v2_end)):
        raise VoiceLeadingError("Voice pitches must be integer MIDI values in 0..127.")

    d1 = v1_end - v1_start
    d2 = v2_end - v2_start

    if d1 == 0 and d2 == 0:
        return ContrapuntalMotion.STATIC
    if d1 == 0 or d2 == 0:
        return ContrapuntalMotion.OBLIQUE
    if d1 * d2 < 0:
        return ContrapuntalMotion.CONTRARY
    if d1 == d2:
        return ContrapuntalMotion.PARALLEL
    return ContrapuntalMotion.SIMILAR


def analyze_contrapuntal_motions(
    voicing_a: Union[List[int], Tuple[int, ...]],
    voicing_b: Union[List[int], Tuple[int, ...]]
) -> Dict[str, Any]:
    """
    Analyzes relative contrapuntal motion across all voice pairs in two consecutive voicings.
    """
    if len(voicing_a) != len(voicing_b):
        raise VoiceLeadingError("Voicings must have identical voice counts.")
    if len(voicing_a) < 2:
        raise VoiceLeadingError("Contrapuntal motion analysis requires at least two voices.")

    pairwise_motions: Dict[Tuple[int, int], str] = {}
    counts: Dict[str, int] = {m.value: 0 for m in ContrapuntalMotion}

    n = len(voicing_a)
    total_pairs = 0
    for low in range(n):
        for high in range(low + 1, n):
            motion = classify_voice_motion(
                voicing_a[low], voicing_b[low],
                voicing_a[high], voicing_b[high]
            )
            pairwise_motions[(low, high)] = motion.value
            counts[motion.value] += 1
            total_pairs += 1

    outer_motion = classify_voice_motion(
        voicing_a[0], voicing_b[0],
        voicing_a[-1], voicing_b[-1]
    )

    contrary_ratio = counts[ContrapuntalMotion.CONTRARY.value] / total_pairs if total_pairs > 0 else 0.0

    return {
        "pairwise_motions": pairwise_motions,
        "motion_counts": counts,
        "outer_voice_motion": outer_motion.value,
        "contrary_motion_ratio": round(contrary_ratio, 3),
        "total_voice_pairs": total_pairs,
    }


def detect_voice_crossing(notes: Union[List[int], Tuple[int, ...]]) -> bool:
    """
    Detects if any higher-index voice is pitched strictly lower than a lower-index voice.
    Input must be strictly non-descending (voices indexed from bass=0 to soprano=n-1).
    """
    if not notes:
        return False
    return any(notes[i] > notes[i + 1] for i in range(len(notes) - 1))


def detect_voice_overlap(
    voicing_a: Union[List[int], Tuple[int, ...]],
    voicing_b: Union[List[int], Tuple[int, ...]]
) -> bool:
    """
    Detects voice overlap: A voice moves to a pitch higher than the preceding pitch
    of a higher voice, or lower than the preceding pitch of a lower voice.
    """
    if len(voicing_a) != len(voicing_b):
        raise VoiceLeadingError("Voicings must have equal voice count.")
    n = len(voicing_a)
    for i in range(n):
        for j in range(i + 1, n):
            if voicing_b[i] > voicing_a[j] or voicing_b[j] < voicing_a[i]:
                return True
    return False


def _resolve_style(style_input: Union[str, VoiceLeadingStyle]) -> VoiceLeadingStyle:
    """Normalize string or enum into canonical VoiceLeadingStyle."""
    if isinstance(style_input, VoiceLeadingStyle):
        return style_input
    if isinstance(style_input, str):
        key = style_input.strip().upper()
        # Direct lookup
        try:
            return VoiceLeadingStyle(key)
        except ValueError:
            pass
        # Common aliases
        alias_map = {
            "STRICT": VoiceLeadingStyle.STRICT_CLASSICAL,
            "CLASSICAL": VoiceLeadingStyle.STRICT_CLASSICAL,
            "STRICT_CLASSICAL": VoiceLeadingStyle.STRICT_CLASSICAL,
            "STRICT_COUNTERPOINT": VoiceLeadingStyle.STRICT_COUNTERPOINT,
            "POP": VoiceLeadingStyle.CONTEMPORARY_POP,
            "JAZZ": VoiceLeadingStyle.JAZZ_POP,
            "POP_ROCK": VoiceLeadingStyle.CONTEMPORARY_POP,
            "CONTEMPORARY_POP": VoiceLeadingStyle.CONTEMPORARY_POP,
            "ROCK": VoiceLeadingStyle.POWER_CHORDS,
            "METAL": VoiceLeadingStyle.POWER_CHORDS,
            "POWER_CHORD": VoiceLeadingStyle.POWER_CHORDS,
            "POWER_CHORDS": VoiceLeadingStyle.POWER_CHORDS,
            "QUARTAL": VoiceLeadingStyle.QUARTAL_JAZZ,
            "QUARTAL_JAZZ": VoiceLeadingStyle.QUARTAL_JAZZ,
            # Backwards compatibility / tolerant aliases
            "CLOSE": VoiceLeadingStyle.JAZZ_POP,
            "DROP2": VoiceLeadingStyle.JAZZ_POP,
            "SHELL": VoiceLeadingStyle.JAZZ_POP,
            "ROOTLESS": VoiceLeadingStyle.JAZZ_POP,
        }
        if key in alias_map:
            return alias_map[key]
        raise VoiceLeadingError(f"Unknown voice leading style: {style_input!r}")
    raise VoiceLeadingError(f"Invalid voice leading style type: {type(style_input)}")


@dataclass(frozen=True)
class VoiceLeadingDiagnostic:
    """Style-dependent finding with zero-based voice indices."""

    motion: Literal["parallel", "contrary"]
    interval: Literal["fifth", "octave_or_unison"]
    lower_voice: int
    upper_voice: int

    def describe(self) -> str:
        """Return the historical diagnostic text for existing API consumers."""
        label = "octave/unison" if self.interval == "octave_or_unison" else "fifth"
        if self.motion == "parallel":
            return f"Parallel {label} between voice {self.lower_voice} and {self.upper_voice}"
        return f"Contrary {label} between outer voices {self.lower_voice} and {self.upper_voice}"


def detect_parallel_fifths_octaves(
    chord_a: Union[List[int], Tuple[int, ...]],
    chord_b: Union[List[int], Tuple[int, ...]],
    style: Union[str, VoiceLeadingStyle] = VoiceLeadingStyle.STRICT_COUNTERPOINT
) -> List[str]:
    """
    Report perfect parallels and contrary outer-voice intervals in strict style.
    
    Adheres strictly to OA-0026 / M06:
    - CONTEMPORARY_POP, JAZZ_POP, POWER_CHORDS and QUARTAL_JAZZ permit parallel fifths and octaves.
    - STRICT_CLASSICAL and STRICT_COUNTERPOINT report parallel fifths and octaves as violations.
    """
    return [
        diagnostic.describe()
        for diagnostic in find_perfect_interval_motion(chord_a, chord_b, style)
    ]


def find_perfect_interval_motion(
    chord_a: Union[List[int], Tuple[int, ...]],
    chord_b: Union[List[int], Tuple[int, ...]],
    style: Union[str, VoiceLeadingStyle] = VoiceLeadingStyle.STRICT_COUNTERPOINT,
) -> List[VoiceLeadingDiagnostic]:
    """Find perfect parallels and contrary outer-voice intervals in strict style."""
    if len(chord_a) != len(chord_b):
        raise VoiceLeadingError("Chords must have identical voice count.")

    resolved_style = _resolve_style(style)
    if not resolved_style.is_strict_counterpoint:
        return []

    violations: List[VoiceLeadingDiagnostic] = []
    n = len(chord_a)
    for low in range(n):
        for high in range(low + 1, n):
            before = abs(chord_a[high] - chord_a[low]) % 12
            after = abs(chord_b[high] - chord_b[low]) % 12
            if before != after or before not in (0, 7):
                continue
            motion = (chord_b[low] - chord_a[low]) * (chord_b[high] - chord_a[high])
            interval = "octave_or_unison" if before == 0 else "fifth"
            if motion > 0:
                violations.append(VoiceLeadingDiagnostic("parallel", interval, low, high))
            elif motion < 0 and low == 0 and high == n - 1:
                violations.append(VoiceLeadingDiagnostic("contrary", interval, low, high))
    return violations


def evaluate_voice_leading_transition(
    chord_a: Union[List[int], Tuple[int, ...]],
    chord_b: Union[List[int], Tuple[int, ...]],
    style: Union[str, VoiceLeadingStyle] = VoiceLeadingStyle.CONTEMPORARY_POP
) -> VoiceLeadingEvaluation:
    """
    Perform a complete stylistic evaluation of the voice-leading transition between two voicings.
    
    Generates structured VoiceLeadingViolation entries and stylistic annotations
    adhering to Fux (1725), Aldwell & Schachter (1989), Everett (2009), or Tymoczko (2011).
    """
    if len(chord_a) != len(chord_b):
        raise VoiceLeadingError("Chords must have identical voice count.")
    if len(chord_a) < 2:
        raise VoiceLeadingError("Voice leading evaluation requires at least two voices.")

    resolved_style = _resolve_style(style)
    n = len(chord_a)

    # 1. Contrapuntal motion analysis
    cm_analysis = analyze_contrapuntal_motions(chord_a, chord_b)

    # 2. L1 distance and max leap
    deltas = [abs(chord_b[i] - chord_a[i]) for i in range(n)]
    total_l1 = sum(deltas)
    max_leap = max(deltas)

    # 3. Detect violations and stylistic notes
    violations: List[VoiceLeadingViolation] = []
    stylistic_notes: List[str] = []

    for low in range(n):
        for high in range(low + 1, n):
            before_int = abs(chord_a[high] - chord_a[low]) % 12
            after_int = abs(chord_b[high] - chord_b[low]) % 12

            if before_int == after_int and before_int in (0, 7):
                d_low = chord_b[low] - chord_a[low]
                d_high = chord_b[high] - chord_a[high]
                motion_mult = d_low * d_high
                int_name = "Quinte" if before_int == 7 else "Oktave/Prime"
                rule_tag = "PARALLEL_FIFTH" if before_int == 7 else "PARALLEL_OCTAVE"

                if motion_mult > 0:
                    # Parallel motion
                    if resolved_style.is_strict_counterpoint:
                        violations.append(VoiceLeadingViolation(
                            rule_name=rule_tag,
                            voice_indices=(low, high),
                            motion_type=ContrapuntalMotion.PARALLEL.value,
                            pitch_interval=before_int,
                            from_pitches=(chord_a[low], chord_a[high]),
                            to_pitches=(chord_b[low], chord_b[high]),
                            severity="ERROR",
                            explanation=(
                                f"Parallele {int_name} zwischen Stimme {low} und {high}. "
                                "Nach klassischem Kontrapunkt (Fux 1725) unzulässig, da Eigenständigkeit der Stimmen verloren geht."
                            ),
                            stylistic_context=resolved_style.reference_framework
                        ))
                    elif resolved_style.is_power_chord_style:
                        stylistic_notes.append(
                            f"Parallele {int_name} zwischen Stimme {low} und {high} als Power-Chord-Planing legitimiert (Everett 2009)."
                        )
                    else:
                        stylistic_notes.append(
                            f"Parallele {int_name} zwischen Stimme {low} und {high} im Pop/Jazz-Kontext zulässig (Everett 2008, Tymoczko 2011)."
                        )

                elif motion_mult < 0 and low == 0 and high == n - 1:
                    # Contrary motion into perfect interval in outer voices
                    if resolved_style.is_strict_counterpoint:
                        violations.append(VoiceLeadingViolation(
                            rule_name="CONTRARY_OUTER_" + ("FIFTH" if before_int == 7 else "OCTAVE"),
                            voice_indices=(low, high),
                            motion_type=ContrapuntalMotion.CONTRARY.value,
                            pitch_interval=before_int,
                            from_pitches=(chord_a[low], chord_a[high]),
                            to_pitches=(chord_b[low], chord_b[high]),
                            severity="WARNING",
                            explanation=(
                                f"Antiparallele {int_name} in den Außenstimmen (Bass {low} und Sopran {high}). "
                                "In strengem Satz verpönt (Aldwell & Schachter 1989)."
                            ),
                            stylistic_context=resolved_style.reference_framework
                        ))

    # Voice crossing check
    if detect_voice_crossing(chord_b):
        violations.append(VoiceLeadingViolation(
            rule_name="VOICE_CROSSING",
            voice_indices=(0, n - 1),
            motion_type="CROSSING",
            pitch_interval=0,
            from_pitches=(chord_a[0], chord_a[-1]),
            to_pitches=(chord_b[0], chord_b[-1]),
            severity="ERROR" if resolved_style.is_strict_counterpoint else "WARNING",
            explanation="Stimmkreuzung im Zielakkord: Höhere Stimme liegt unterhalb einer tieferen Stimme.",
            stylistic_context=resolved_style.reference_framework
        ))

    is_valid = len([v for v in violations if v.severity == "ERROR"]) == 0

    return VoiceLeadingEvaluation(
        from_voicing=tuple(chord_a),
        to_voicing=tuple(chord_b),
        style=resolved_style,
        is_valid=is_valid,
        violations=violations,
        l1_distance=total_l1,
        max_voice_leap=max_leap,
        contrapuntal_motion=cm_analysis,
        stylistic_notes=stylistic_notes,
    )

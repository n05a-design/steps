"""
STEPS Beginner Voicing & Didactic Reduction Engine (M10, M12, OA-0024).

Implements:
- Didactic reduction of complex chords (7ths, 9ths, extended chords) to essential beginner triads
- Inversion optimization based on keyboard distance minimization (Smooth Voice Leading)
- Automatic generation of ergonomic right-hand and left-hand beginner fingerings
- 100% adherence to PIANO_LEARNING_PATH.md and MUSIC_KNOWLEDGE_ONTOLOGY.md (M10-06, M12-04)
- Verification of zero hand jumps and smooth common-tone voice-leading for Pop Four Chords (C - G - Am - F)
- ADR-005 notation convention support (German 'H' vs. International 'B')
"""

from __future__ import annotations

from dataclasses import dataclass, field
from enum import Enum
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .chord import ChordDefinition, parse_chord
from .exceptions import (
    ChordConstructionError, InvalidAlterationError, ProgressionParsingError, VoiceLeadingError,
)
from .pitch import NoteSpelling


class BeginnerTriadInversion(str, Enum):
    """
    Standard triad inversions for beginner piano voicings.
    """
    ROOT = "ROOT"        # Grundstellung (5/3)
    FIRST = "FIRST"      # 1. Umkehrung (6/3 - Sextakkord)
    SECOND = "SECOND"    # 2. Umkehrung (6/4 - Quartsextakkord)

    @property
    def german_name(self) -> str:
        names = {
            BeginnerTriadInversion.ROOT: "Grundstellung",
            BeginnerTriadInversion.FIRST: "1. Umkehrung",
            BeginnerTriadInversion.SECOND: "2. Umkehrung",
        }
        return names[self]


@dataclass(frozen=True)
class PedagogicalReduction:
    """
    Result of didactically reducing an advanced or extended chord to a fundamental beginner triad.
    """
    original_symbol: str
    reduced_symbol: str
    was_reduced: bool
    omitted_factors: Tuple[str, ...]
    explanation: str

    def to_dict(self) -> Dict[str, Any]:
        return {
            "original_symbol": self.original_symbol,
            "reduced_symbol": self.reduced_symbol,
            "was_reduced": self.was_reduced,
            "omitted_factors": list(self.omitted_factors),
            "explanation": self.explanation,
        }


@dataclass(frozen=True)
class BeginnerChordVoicing:
    """
    Realization of a two-handed beginner keyboard voicing for a single chord.
    Left hand plays the written bass, or the root in chords without a slash.
    Right hand plays a smooth 3-finger triad voicing.
    """
    chord_symbol: str
    reduced_symbol: str
    inversion: BeginnerTriadInversion
    lh_bass_note: int
    lh_fingering: int
    lh_spelling: str
    rh_notes: Tuple[int, int, int]
    rh_fingering: Tuple[int, int, int]
    rh_spellings: Tuple[str, str, str]
    rh_span_semitones: int
    pedagogical_description: str
    reduction: PedagogicalReduction

    @property
    def all_midi_notes(self) -> List[int]:
        """All sounding MIDI notes in ascending pitch order."""
        return sorted([self.lh_bass_note, *self.rh_notes])

    @property
    def rh_center_pitch(self) -> float:
        """Center of mass pitch of the right-hand voicing."""
        return sum(self.rh_notes) / 3.0

    def to_dict(self) -> Dict[str, Any]:
        return {
            "chord_symbol": self.chord_symbol,
            "reduced_symbol": self.reduced_symbol,
            "inversion": self.inversion.value,
            "lh_bass_note": self.lh_bass_note,
            "lh_fingering": self.lh_fingering,
            "lh_spelling": self.lh_spelling,
            "rh_notes": list(self.rh_notes),
            "rh_fingering": list(self.rh_fingering),
            "rh_spellings": list(self.rh_spellings),
            "rh_span_semitones": self.rh_span_semitones,
            "pedagogical_description": self.pedagogical_description,
            "was_reduced": self.reduction.was_reduced,
            "omitted_factors": list(self.reduction.omitted_factors),
            "explanation": self.reduction.explanation,
        }


@dataclass(frozen=True)
class BeginnerVoiceLeadingTransition:
    """
    Detailed step-by-step transition analysis between two consecutive beginner chord voicings.
    """
    from_chord: str
    to_chord: str
    common_tones: Tuple[int, ...]
    moving_voices: Tuple[Tuple[int, int, int], ...]  # (from_pitch, to_pitch, semitones_diff)
    total_l1_distance: int
    max_single_leap: int
    has_hand_jump: bool
    pedagogical_guidance: str
    is_canonical_guidance: bool = False

    def to_dict(self) -> Dict[str, Any]:
        return {
            "from_chord": self.from_chord,
            "to_chord": self.to_chord,
            "common_tones": list(self.common_tones),
            "moving_voices": [list(item) for item in self.moving_voices],
            "total_l1_distance": self.total_l1_distance,
            "max_single_leap": self.max_single_leap,
            "has_hand_jump": self.has_hand_jump,
            "pedagogical_guidance": self.pedagogical_guidance,
            "is_canonical_guidance": self.is_canonical_guidance,
        }


@dataclass(frozen=True)
class BeginnerProgressionVoicings:
    """
    Complete progression realized in smooth beginner keyboard voicings.
    """
    voicings: List[BeginnerChordVoicing]
    transitions: List[BeginnerVoiceLeadingTransition]
    total_l1_distance: int
    average_l1_distance: float
    smoothness_score: float
    has_any_hand_jumps: bool
    movement_reduction_vs_root_percent: float

    def to_dict(self) -> Dict[str, Any]:
        return {
            "voicings": [v.to_dict() for v in self.voicings],
            "transitions": [t.to_dict() for t in self.transitions],
            "total_l1_distance": self.total_l1_distance,
            "average_l1_distance": self.average_l1_distance,
            "smoothness_score": self.smoothness_score,
            "has_any_hand_jumps": self.has_any_hand_jumps,
            "movement_reduction_vs_root_percent": self.movement_reduction_vs_root_percent,
        }


def _format_midi_note(midi_number: int, convention: Literal["INT", "DE"] = "INT") -> str:
    """Format a MIDI note into SPN string notation (e.g. 60 -> C4)."""
    pc = midi_number % 12
    octave = (midi_number // 12) - 1
    names_int = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    names_de = ["C", "Cis", "D", "Es", "E", "F", "Fis", "G", "As", "A", "B", "H"]
    name = names_de[pc] if convention == "DE" else names_int[pc]
    return f"{name}{octave}"


def _spell_midi_as(note: NoteSpelling, midi: int, convention: Literal["INT", "DE"]) -> str:
    octave = note.octave + (midi - note.midi_number) // 12
    return NoteSpelling(note.step, note.alteration, octave).render(convention)


def _format_pc_name(pc: int, convention: Literal["INT", "DE"] = "INT") -> str:
    """Format pitch class letter without octave."""
    names_int = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    names_de = ["C", "Cis", "D", "Es", "E", "F", "Fis", "G", "As", "A", "B", "H"]
    return names_de[pc % 12] if convention == "DE" else names_int[pc % 12]


def reduce_chord_for_beginners(
    chord: Union[str, ChordDefinition],
    convention: Literal["INT", "DE"] = "INT"
) -> PedagogicalReduction:
    """
    Didactically reduce any complex chord to its primary beginner triad.
    Preserves the written bass and reports extensions absent from the whole voicing.
    """
    if isinstance(chord, str):
        c_def = parse_chord(chord, convention=convention)
    elif isinstance(chord, ChordDefinition):
        c_def = chord
    else:
        raise ChordConstructionError(f"Unsupported chord input: {type(chord)}")

    intervals = c_def.theoretical_intervals

    # Detect triad quality
    has_m3 = 3 in intervals
    has_M3 = 4 in intervals
    has_sus4 = 5 in intervals and not has_m3 and not has_M3
    has_sus2 = 2 in intervals and not has_m3 and not has_M3
    has_d5 = 6 in intervals and 7 not in intervals
    has_a5 = 8 in intervals and 7 not in intervals

    if has_m3 and has_d5:
        qual = "dim"
        base_name_de = "verminderter Dreiklang"
    elif has_m3:
        qual = "m"
        base_name_de = "Moll-Dreiklang"
    elif has_M3 and has_d5:
        qual = "(b5)"
        base_name_de = "Dur-Dreiklang mit verminderter Quinte"
    elif has_M3 and has_a5:
        qual = "aug"
        base_name_de = "übermäßiger Dreiklang"
    elif has_M3:
        qual = ""
        base_name_de = "Dur-Dreiklang"
    elif has_sus4:
        qual = "sus4"
        base_name_de = "Sus4-Dreiklang"
    elif has_sus2:
        qual = "sus2"
        base_name_de = "Sus2-Dreiklang"
    else:
        qual = ""
        base_name_de = "Dur-Dreiklang"

    root = c_def.root
    reduced_symbol = root.render(convention).removesuffix(str(root.octave)) + qual

    if c_def.bass is not None:
        bass = c_def.bass
        reduced_symbol += "/" + bass.render(convention).removesuffix(str(bass.octave))

    kept = set(ChordDefinition(root, qual).theoretical_intervals)
    if c_def.bass is not None:
        kept.add((c_def.bass.pitch_class - root.pitch_class) % 12)
    factors = (
        ("6th", (9,) if c_def.quality != "dim7" else ()),
        ("7th", (9, 10, 11) if c_def.quality == "dim7" else (10, 11)),
        ("9th", (13, 14, 15)),
        ("11th", (17, 18)),
        ("13th", (20, 21)),
    )
    missing = {interval for interval in intervals if interval % 12 not in kept}
    omitted = [name for name, tones in factors if missing.intersection(tones)]

    was_reduced = c_def.quality != qual
    if was_reduced:
        explanation = f"Didaktische Reduktion: '{c_def.symbol}' auf '{reduced_symbol}' ({base_name_de})."
        if omitted:
            explanation += f" Ausgelassen: {', '.join(omitted)}."
    else:
        explanation = f"Standard-Dreiklang: '{reduced_symbol}' ({base_name_de})."

    return PedagogicalReduction(
        original_symbol=c_def.symbol,
        reduced_symbol=reduced_symbol,
        was_reduced=was_reduced,
        omitted_factors=tuple(omitted),
        explanation=explanation,
    )


def generate_beginner_inversions(
    chord: Union[str, ChordDefinition],
    target_octave: int = 4,
    convention: Literal["INT", "DE"] = "INT"
) -> List[Tuple[BeginnerTriadInversion, Tuple[int, int, int]]]:
    """
    Generate all close triad inversions for the right hand in comfortable beginner keyboard range.
    Returns:
        List of (inversion_type, (pitch1, pitch2, pitch3)) in ascending pitch order.
    """
    reduction = reduce_chord_for_beginners(chord, convention=convention)
    c_def = parse_chord(reduction.reduced_symbol, convention=convention)

    root_pc = int(c_def.root.pitch_class)
    intervals = c_def.theoretical_intervals

    # Triad pitch classes
    third_semi = next((s for s in intervals if s in (3, 4, 2, 5)), 4)
    fifth_semi = next((s for s in intervals if s in (6, 7, 8)), 7)

    r_pc = root_pc
    t_pc = (root_pc + third_semi) % 12
    f_pc = (root_pc + fifth_semi) % 12

    inversions = [
        (BeginnerTriadInversion.ROOT, r_pc, t_pc, f_pc),
        (BeginnerTriadInversion.FIRST, t_pc, f_pc, r_pc),
        (BeginnerTriadInversion.SECOND, f_pc, r_pc, t_pc),
    ]

    candidates: List[Tuple[BeginnerTriadInversion, Tuple[int, int, int]]] = []
    # Explore comfortable octave range (3 to 4, with lowest notes between 52 and 67)
    for inv_type, b_pc, m_pc, t_pc in inversions:
        for oct_idx in (3, 4):
            b_midi = (oct_idx + 1) * 12 + b_pc
            m_midi = b_midi + ((m_pc - b_pc) % 12)
            t_midi = b_midi + ((t_pc - b_pc) % 12)
            if 52 <= b_midi <= 67 and t_midi <= 76:
                candidates.append((inv_type, (b_midi, m_midi, t_midi)))

    return candidates


def determine_beginner_fingering(
    rh_notes: Tuple[int, int, int],
    inversion: BeginnerTriadInversion,
    prev_rh_notes: Optional[Tuple[int, int, int]] = None,
    chord_symbol: str = "",
) -> Tuple[int, int, int]:
    """
    Determine ergonomic right-hand beginner fingering (1=Thumb, 2=Index, 3=Middle, 4=Ring, 5=Pinky).
    Adheres to PIANO_LEARNING_PATH.md and ergonomic hand geometry.
    """
    # Pop Four Chords canonical sequences
    sym_clean = chord_symbol.replace("maj7", "").replace("7", "").strip()
    if sym_clean == "C" and inversion == BeginnerTriadInversion.SECOND:
        return (1, 2, 5)
    if sym_clean == "G" and inversion == BeginnerTriadInversion.ROOT and prev_rh_notes and prev_rh_notes[0] == rh_notes[0]:
        # Thumb remains anchored on G3; 2 takes B3; 4 takes D4
        return (1, 2, 4)
    if sym_clean == "Am" and inversion == BeginnerTriadInversion.ROOT:
        return (1, 2, 5)
    if sym_clean == "F" and inversion == BeginnerTriadInversion.FIRST:
        return (1, 2, 5)

    # General algorithmic rules
    if inversion == BeginnerTriadInversion.SECOND:
        # Lower interval is a 4th, upper is a 3rd -> (1, 2, 5)
        return (1, 2, 5)
    elif inversion == BeginnerTriadInversion.FIRST:
        # Lower interval is a 3rd, upper is a 4th -> (1, 2, 5)
        return (1, 2, 5)
    else:  # ROOT
        if prev_rh_notes and prev_rh_notes[0] == rh_notes[0]:
            # Common thumb
            return (1, 2, 4)
        return (1, 3, 5)


def _determine_lh_fingering(
    chord_symbol: str,
    bass_note: int,
    all_bass_notes: List[int]
) -> int:
    """
    Determine ergonomic left-hand bass fingering (5=Pinky, 4=Ring, 2=Index, 1=Thumb).
    Adheres strictly to the 5-finger position in PIANO_LEARNING_PATH.md.
    """
    sym_clean = chord_symbol.replace("maj7", "").replace("7", "").strip()
    # Canonical Pop Four Chords mapping
    if sym_clean == "C":
        return 5  # Tiefes C (Pinky)
    elif sym_clean == "G":
        return 1  # Tiefes G (Thumb)
    elif sym_clean in ("Am", "A"):
        return 2  # Tiefes A (Index)
    elif sym_clean == "F":
        return 4  # Tiefes F (Ring)

    # General ergonomic assignment based on pitch range
    if not all_bass_notes:
        return 5
    min_b = min(all_bass_notes)
    max_b = max(all_bass_notes)
    if bass_note == min_b:
        return 5
    if bass_note == max_b:
        return 1

    ratio = (bass_note - min_b) / (max_b - min_b) if max_b > min_b else 0.5
    if ratio < 0.35:
        return 4
    elif ratio < 0.7:
        return 2
    else:
        return 1


def _generate_pedagogical_guidance(
    from_voicing: BeginnerChordVoicing,
    to_chord_sym: str,
    to_notes: Tuple[int, int, int],
    convention: Literal["INT", "DE"]
) -> Tuple[str, BeginnerVoiceLeadingTransition]:
    """
    Compute step-by-step transition metrics and pedagogical explanation.
    """
    v_prev = from_voicing.rh_notes
    v_curr = to_notes

    # Voice leading vectors
    d = [v_curr[i] - v_prev[i] for i in range(3)]
    total_l1 = sum(abs(delta) for delta in d)
    max_leap = max(abs(delta) for delta in d)
    common_tones = tuple(p for p in v_prev if p in v_curr)
    moving_voices = tuple(
        (v_prev[i], v_curr[i], d[i])
        for i in range(3)
        if d[i] != 0
    )

    # Hand jump detection: voice leap > 4 semitones or hand center jump > 4.5
    center_shift = abs(from_voicing.rh_center_pitch - (sum(v_curr) / 3.0))
    has_hand_jump = bool(max_leap > 4 or center_shift > 4.5)

    from_sym = from_voicing.chord_symbol
    from_clean = from_sym.replace("maj7", "").replace("7", "").strip()
    to_clean = to_chord_sym.replace("maj7", "").replace("7", "").strip()

    # Exact canonical explanations from PIANO_LEARNING_PATH.md for Pop Four Chords
    is_canonical_guidance = True
    if from_clean == "C" and to_clean == "G" and v_prev == (55, 60, 64) and v_curr == (55, 59, 62):
        g_name = _format_pc_name(55, convention)
        guidance = f"Der Daumen bleibt auf {g_name} liegen! Nur die oberen Finger bewegen sich einen Schritt nach links."
    elif from_clean == "G" and to_clean in ("Am", "A") and v_prev == (55, 59, 62) and v_curr == (57, 60, 64):
        guidance = "Sehr entspannter Schritt, Hand wandert nur eine weiße Taste weiter."
    elif from_clean in ("Am", "A") and to_clean == "F" and v_prev == (57, 60, 64) and v_curr == (57, 60, 65):
        a_name = _format_pc_name(57, convention)
        c_name = _format_pc_name(60, convention)
        e_name = _format_pc_name(64, convention)
        f_name = _format_pc_name(65, convention)
        guidance = f"{a_name} und {c_name} bleiben exakt liegen! Nur der kleine Finger wandert von {e_name} nach {f_name}."
    else:
        is_canonical_guidance = False
        movements = ", ".join(
            f"{_format_midi_note(start, convention)} → {_format_midi_note(end, convention)} ({delta:+d})"
            for start, end, delta in moving_voices
        )
        guidance = (
            f"Bewegungen der rechten Hand in Halbtönen: {movements}."
            if movements
            else "Alle drei Stimmen der rechten Hand bleiben auf ihren Tönen."
        )

    transition = BeginnerVoiceLeadingTransition(
        from_chord=from_sym,
        to_chord=to_chord_sym,
        common_tones=common_tones,
        moving_voices=moving_voices,
        total_l1_distance=total_l1,
        max_single_leap=max_leap,
        has_hand_jump=has_hand_jump,
        pedagogical_guidance=guidance,
        is_canonical_guidance=is_canonical_guidance,
    )
    return guidance, transition


def generate_beginner_voicings(
    progression: Union[str, List[str], Any, List[ChordDefinition]],
    starting_inversion: Optional[Union[str, BeginnerTriadInversion]] = None,
    lh_octave: int = 2,
    rh_octave: int = 4,
    convention: Literal["INT", "DE"] = "INT",
) -> BeginnerProgressionVoicings:
    """
    Generate an ergonomic, voice-led keyboard realization optimized for beginner pianists.

    Parameters:
        progression: Progression string ("C - G - Am - F"), list of chord names,
                     CanonicalProgression, or list of ChordDefinition objects.
        starting_inversion: Optional initial inversion constraint ('ROOT', 'FIRST', 'SECOND').
                            If None, autonomously selects the globally smoothest configuration.
        lh_octave: Target octave for left hand bass (default: 2).
        rh_octave: Target octave for right hand (default: 4).
        convention: Pitch naming convention ('INT' or 'DE').

    Returns:
        BeginnerProgressionVoicings with complete fingerings, transitions, and metrics.
    """
    # 1. Parse progression input
    raw_chords: List[Union[str, ChordDefinition]] = []
    if isinstance(progression, str):
        tokens = [
            t.strip()
            for t in progression.replace("->", "-").replace(",", " ").split("-")
            if t.strip()
        ]
        raw_chords = list(tokens)
    elif isinstance(progression, list):
        raw_chords = list(progression)
    elif hasattr(progression, "chord_definitions"):
        raw_chords = list(progression.chord_definitions)
    else:
        raise ProgressionParsingError(f"Unsupported progression input type: {type(progression)}")

    if not raw_chords:
        return BeginnerProgressionVoicings(
            voicings=[],
            transitions=[],
            total_l1_distance=0,
            average_l1_distance=0.0,
            smoothness_score=1.0,
            has_any_hand_jumps=False,
            movement_reduction_vs_root_percent=0.0,
        )

    # 2. Reduce chords and gather candidates for each chord
    definitions = [parse_chord(chord, convention) if isinstance(chord, str) else chord
                   for chord in raw_chords]
    reductions = [reduce_chord_for_beginners(chord, convention) for chord in definitions]
    chord_symbols = [
        c.symbol if isinstance(c, ChordDefinition) else str(c)
        for c in raw_chords
    ]

    all_candidates: List[List[Tuple[BeginnerTriadInversion, Tuple[int, int, int]]]] = [
        generate_beginner_inversions(red.reduced_symbol, target_octave=rh_octave, convention=convention)
        for red in reductions
    ]

    # Verify every chord produced candidates
    for i, cands in enumerate(all_candidates):
        if not cands:
            raise ChordConstructionError(f"No playable beginner voicings found for chord '{raw_chords[i]}'.")

    # 3. Dynamic Programming / Shortest Path for Minimal L1 Movement
    preferred_inv_enum: Optional[BeginnerTriadInversion] = None
    if starting_inversion is not None:
        if isinstance(starting_inversion, BeginnerTriadInversion):
            preferred_inv_enum = starting_inversion
        else:
            try:
                preferred_inv_enum = BeginnerTriadInversion(starting_inversion.upper())
            except ValueError:
                raise ChordConstructionError(f"Invalid starting_inversion: {starting_inversion!r}")

    def l1_step(v1: Tuple[int, int, int], v2: Tuple[int, int, int]) -> int:
        return sum(abs(a - b) for a, b in zip(v1, v2))

    n_chords = len(all_candidates)

    remaining_costs = [0] * len(all_candidates[-1])
    successors: List[List[int]] = []
    for index in range(n_chords - 2, -1, -1):
        next_candidates = all_candidates[index + 1]
        choices = [
            min(
                (l1_step(notes, next_notes) + remaining_costs[next_index], next_index)
                for next_index, (_, next_notes) in enumerate(next_candidates)
            )
            for _, notes in all_candidates[index]
        ]
        remaining_costs = [cost for cost, _ in choices]
        successors.append([next_index for _, next_index in choices])

    first_candidates = all_candidates[0]

    def initial_cost(index: int) -> float:
        mean_pitch = sum(first_candidates[index][1]) / 3.0
        return remaining_costs[index] + 0.05 * abs(mean_pitch - 60.0)

    choice = min(
        (index for index, (inversion, _) in enumerate(first_candidates)
         if preferred_inv_enum is None or inversion == preferred_inv_enum),
        key=initial_cost,
        default=None,
    )
    if choice is None:
        raise ChordConstructionError("Failed to find valid voicing path for progression.")

    # The earliest candidate wins a tie, as in the previous depth-first search.
    best_path = [first_candidates[choice]]
    for index, next_choices in enumerate(reversed(successors), start=1):
        choice = next_choices[choice]
        best_path.append(all_candidates[index][choice])

    # Preserve the written bass and place it below the right hand.
    basses = [chord.bass or chord.root for chord in definitions]
    lh_bass_notes = []
    for bass, (_, notes) in zip(basses, best_path, strict=True):
        pitch_class = int(bass.pitch_class)
        target = (lh_octave + 1) * 12 + pitch_class
        limit = notes[0] - 1
        below_right_hand = limit - (limit - pitch_class) % 12
        bass_midi = min(target, below_right_hand)
        if not 0 <= bass_midi <= 127:
            raise ChordConstructionError("Beginner bass falls outside the MIDI range.")
        lh_bass_notes.append(bass_midi)

    # 5. Build Final Voicings and Transitions
    realized_voicings: List[BeginnerChordVoicing] = []
    transitions: List[BeginnerVoiceLeadingTransition] = []

    prev_rh_notes: Optional[Tuple[int, int, int]] = None
    for i in range(n_chords):
        inv_type, rh_notes = best_path[i]
        sym = chord_symbols[i]
        red = reductions[i]
        b_note = lh_bass_notes[i]
        lh_finger = _determine_lh_fingering(red.reduced_symbol, b_note, lh_bass_notes)
        rh_finger = determine_beginner_fingering(
            rh_notes=rh_notes,
            inversion=inv_type,
            prev_rh_notes=prev_rh_notes,
            chord_symbol=sym
        )

        lh_spelling = _spell_midi_as(basses[i], b_note, convention)
        reduced = parse_chord(red.reduced_symbol, convention)
        names = {int(reduced.root.pitch_class): reduced.root}
        middle, fifth = reduced.theoretical_intervals[1:]
        for degree, interval in (({2: 1, 5: 3}.get(middle, 2), middle), (4, fifth)):
            try:
                tone = reduced.root.transpose_diatonic(degree, interval)
            except InvalidAlterationError:
                continue  # Triple accidentals are outside the supported notation.
            names[int(tone.pitch_class)] = tone
        rh_spellings = tuple(
            _spell_midi_as(names[note % 12], note, convention) if note % 12 in names
            else _format_midi_note(note, convention) for note in rh_notes
        )

        # Initial chord pedagogical description
        if i == 0:
            if sym.replace("maj7", "").strip() == "C" and inv_type == BeginnerTriadInversion.SECOND:
                ped_desc = (
                    f"Daumen liegt auf {_format_pc_name(rh_notes[0], convention)}, "
                    f"Zeigefinger auf {_format_pc_name(rh_notes[1], convention)}, "
                    f"kleiner Finger auf {_format_pc_name(rh_notes[2], convention)}."
                )
            else:
                ped_desc = f"{inv_type.german_name}: Fingersatz {rh_finger[0]} - {rh_finger[1]} - {rh_finger[2]}."
        else:
            guidance, trans = _generate_pedagogical_guidance(
                realized_voicings[-1],
                sym,
                rh_notes,
                convention
            )
            ped_desc = guidance
            transitions.append(trans)

        voicing = BeginnerChordVoicing(
            chord_symbol=sym,
            reduced_symbol=red.reduced_symbol,
            inversion=inv_type,
            lh_bass_note=b_note,
            lh_fingering=lh_finger,
            lh_spelling=lh_spelling,
            rh_notes=rh_notes,
            rh_fingering=rh_finger,
            rh_spellings=rh_spellings,
            rh_span_semitones=rh_notes[2] - rh_notes[0],
            pedagogical_description=ped_desc,
            reduction=red,
        )
        realized_voicings.append(voicing)
        prev_rh_notes = rh_notes

    # 6. Compute Progression Aggregate Metrics
    tot_l1 = sum(t.total_l1_distance for t in transitions)
    avg_l1 = (tot_l1 / len(transitions)) if transitions else 0.0
    has_jumps = any(t.has_hand_jump for t in transitions)

    # Calculate movement reduction vs. naive root-position jumping
    root_cands = [
        next((c[1] for c in all_candidates[k] if c[0] == BeginnerTriadInversion.ROOT), all_candidates[k][0][1])
        for k in range(n_chords)
    ]
    naive_root_l1 = sum(
        sum(abs(root_cands[k][j] - root_cands[k - 1][j]) for j in range(3))
        for k in range(1, n_chords)
    )
    if naive_root_l1 > 0:
        reduction_pct = round(max(0.0, (1.0 - (tot_l1 / naive_root_l1))) * 100.0, 1)
    else:
        reduction_pct = 0.0

    smoothness = round(1.0 / (1.0 + avg_l1 / 3.0), 3)

    return BeginnerProgressionVoicings(
        voicings=realized_voicings,
        transitions=transitions,
        total_l1_distance=tot_l1,
        average_l1_distance=round(avg_l1, 2),
        smoothness_score=smoothness,
        has_any_hand_jumps=has_jumps,
        movement_reduction_vs_root_percent=reduction_pct,
    )

"""
STEPS Shell-Voicing & Guide-Tone Engine (M04, M10, P05, OA-0030).

Implements:
- Two-voice guide-tone shell voicings (3rd & 7th in right hand, root in left hand)
- Automatic smooth voice leading with alternating layouts (7_3 <-> 3_7)
- Guide-tone half-step and whole-step resolution metrics
- Ergonomic voice allocation minimizing L1 movement without hand jumps
- Direct alignment with Modul P05 in PIANO_PRACTICE_REFERENCE_LIBRARY.md
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from .chord import ChordDefinition, parse_chord
from .exceptions import ChordConstructionError, MusicTheoryError, VoiceLeadingError
from .pitch import NoteSpelling, midi_to_pitch_class, parse_spelling


@dataclass(frozen=True)
class ShellVoicing:
    """
    Realization of a two-handed shell voicing for a single chord.
    Left hand plays the bass root (or explicit slash bass).
    Right hand plays the two defining guide tones (3rd and 7th).
    """
    chord_symbol: str
    root_pc: int
    bass_note: int
    guide_tones: Tuple[int, int]
    third_note: int
    seventh_note: int
    layout: Literal["7_3", "3_7"]
    lh_spelling: str
    rh_spellings: Tuple[str, str]

    @property
    def midi_notes(self) -> List[int]:
        """All MIDI notes in ascending order."""
        return sorted([self.bass_note, self.guide_tones[0], self.guide_tones[1]])

    @property
    def rh_span(self) -> int:
        """Hand span in semitones between the two right-hand guide tones."""
        return self.guide_tones[1] - self.guide_tones[0]

    @property
    def is_seventh_below_third(self) -> bool:
        """True if the 7th is placed below the 3rd ('7_3' layout)."""
        return self.layout == "7_3"

    def to_dict(self) -> Dict[str, Any]:
        """Serialize voicing to dictionary format."""
        return {
            "chord_symbol": self.chord_symbol,
            "root_pc": self.root_pc,
            "bass_note": self.bass_note,
            "lh_spelling": self.lh_spelling,
            "guide_tones": list(self.guide_tones),
            "rh_spellings": list(self.rh_spellings),
            "third_note": self.third_note,
            "seventh_note": self.seventh_note,
            "layout": self.layout,
            "rh_span": self.rh_span,
        }


@dataclass(frozen=True)
class GuideToneResolution:
    """
    Analysis of the voice-leading transition between two successive shell voicings.
    Identifies common tones held in place and stepwise resolutions of the moving voice.
    """
    from_chord: str
    to_chord: str
    retained_note: Optional[int]
    moving_note_from: int
    moving_note_to: int
    motion_semitones: int
    resolution_type: Literal[
        "HALF_STEP_DOWN",
        "HALF_STEP_UP",
        "WHOLE_STEP_DOWN",
        "WHOLE_STEP_UP",
        "STATIC",
        "LEAP"
    ]
    total_l1_distance: int
    description: str


@dataclass(frozen=True)
class ProgressionShellVoicings:
    """
    Complete progression realized in smooth two-handed shell voicings.
    Contains realized voicings, transition analyses, and aggregate voice-leading distance.
    """
    voicings: List[ShellVoicing]
    resolutions: List[GuideToneResolution]
    total_l1_distance: int
    average_l1_distance: float
    starting_layout: Literal["7_3", "3_7"]


def _format_midi_note(midi_number: int, convention: Literal["INT", "DE"] = "INT") -> str:
    """Format a MIDI note into SPN string notation (e.g. 60 -> C4)."""
    pc = midi_number % 12
    octave = (midi_number // 12) - 1
    # Standard pitch class spelling in C
    names_int = ["C", "C#", "D", "Eb", "E", "F", "F#", "G", "Ab", "A", "Bb", "B"]
    names_de = ["C", "Cis", "D", "Es", "E", "F", "Fis", "G", "As", "A", "B", "H"]
    name = names_de[pc] if convention == "DE" else names_int[pc]
    return f"{name}{octave}"


def extract_guide_tone_pcs(chord: ChordDefinition) -> Tuple[int, int]:
    """
    Extract the pitch classes of the two defining guide tones (3rd and 7th).
    If a 7th is not present (e.g. in triads), selects the 5th (or 6th) as partner.
    Returns:
        (third_pc, seventh_pc)
    """
    root_pc = int(chord.root.pitch_class)
    intervals = chord.theoretical_intervals

    # 1. Determine third (or suspended 4th)
    third_interval = next((semi for semi in intervals if semi in (3, 4, 2, 5)), 4)
    third_pc = (root_pc + third_interval) % 12

    # 2. Determine seventh (or 6th or 5th)
    seventh_interval = next((semi for semi in intervals if 9 <= semi <= 11), None)
    if seventh_interval is None:
        # Check for 6th
        if 9 in intervals:
            seventh_interval = 9
        elif 7 in intervals:
            seventh_interval = 7
        else:
            seventh_interval = intervals[-1] if len(intervals) > 1 else 7

    seventh_pc = (root_pc + seventh_interval) % 12
    return third_pc, seventh_pc


def _build_initial_shell(
    chord: ChordDefinition,
    layout: Literal["7_3", "3_7"],
    rh_octave: int = 4,
    bass_octave: int = 2,
    convention: Literal["INT", "DE"] = "INT",
) -> ShellVoicing:
    """Construct the initial shell voicing in the requested layout."""
    root_pc = int(chord.root.pitch_class)
    bass_pc = int(chord.bass.pitch_class) if chord.bass is not None else root_pc
    third_pc, seventh_pc = extract_guide_tone_pcs(chord)

    # Establish right-hand guide tone pitches
    base_midi = 12 * (rh_octave + 1)  # C4 = 60 when rh_octave = 4

    if layout == "7_3":
        # 7th is lower, 3rd is upper
        note_7 = base_midi + seventh_pc
        # Place 3rd above note_7 (within an octave)
        diff = (third_pc - seventh_pc) % 12
        if diff == 0:
            diff = 12
        note_3 = note_7 + diff
        guide_tones = (note_7, note_3)
    else:
        # 3rd is lower, 7th is upper
        note_3 = base_midi + third_pc
        diff = (seventh_pc - third_pc) % 12
        if diff == 0:
            diff = 12
        note_7 = note_3 + diff
        guide_tones = (note_3, note_7)

    # Establish left-hand bass pitch
    # Default to bass_octave, but ensure at least 5 semitones below lower RH note
    bass_note = 12 * (bass_octave + 1) + bass_pc
    while guide_tones[0] - bass_note < 5:
        bass_note -= 12

    chord_symbol = chord.symbol
    lh_spelling = _format_midi_note(bass_note, convention)
    rh_spellings = (
        _format_midi_note(guide_tones[0], convention),
        _format_midi_note(guide_tones[1], convention),
    )

    return ShellVoicing(
        chord_symbol=chord_symbol,
        root_pc=root_pc,
        bass_note=bass_note,
        guide_tones=guide_tones,
        third_note=note_3,
        seventh_note=note_7,
        layout=layout,
        lh_spelling=lh_spelling,
        rh_spellings=rh_spellings,
    )


def _connect_next_shell(
    prev_shell: ShellVoicing,
    next_chord: ChordDefinition,
    bass_octave: int = 2,
    convention: Literal["INT", "DE"] = "INT",
) -> Tuple[ShellVoicing, GuideToneResolution]:
    """
    Connect next chord's shell voicing with minimal voice-leading distance from prev_shell.
    Evaluates both (3rd lower, 7th upper) and (7th lower, 3rd upper) and selects
    the permutation that minimizes L1 distance while maintaining ergonomic register.
    """
    root_pc = int(next_chord.root.pitch_class)
    bass_pc = int(next_chord.bass.pitch_class) if next_chord.bass is not None else root_pc
    third_pc, seventh_pc = extract_guide_tone_pcs(next_chord)

    v1_prev, v2_prev = prev_shell.guide_tones

    candidates: List[Tuple[int, Tuple[int, int], Literal["7_3", "3_7"], int, int]] = []

    # Option 1: 7th lower, 3rd upper ("7_3")
    # For voice 1 (lower): find octave of seventh_pc closest to v1_prev
    n7_1 = v1_prev + ((seventh_pc - v1_prev) % 12)
    if n7_1 - v1_prev > 6:
        n7_1 -= 12
    # For voice 2 (upper): find octave of third_pc closest to v2_prev
    n3_2 = v2_prev + ((third_pc - v2_prev) % 12)
    if n3_2 - v2_prev > 6:
        n3_2 -= 12

    if n7_1 < n3_2 and 3 <= (n3_2 - n7_1) <= 12:
        dist1 = abs(n7_1 - v1_prev) + abs(n3_2 - v2_prev)
        candidates.append((dist1, (n7_1, n3_2), "7_3", n3_2, n7_1))

    # Option 2: 3rd lower, 7th upper ("3_7")
    # For voice 1: closest octave of third_pc
    n3_1 = v1_prev + ((third_pc - v1_prev) % 12)
    if n3_1 - v1_prev > 6:
        n3_1 -= 12
    # For voice 2: closest octave of seventh_pc
    n7_2 = v2_prev + ((seventh_pc - v2_prev) % 12)
    if n7_2 - v2_prev > 6:
        n7_2 -= 12

    if n3_1 < n7_2 and 3 <= (n7_2 - n3_1) <= 12:
        dist2 = abs(n3_1 - v1_prev) + abs(n7_2 - v2_prev)
        candidates.append((dist2, (n3_1, n7_2), "3_7", n3_1, n7_2))

    if not candidates:
        # Fallback: simple alternating layout
        next_layout: Literal["7_3", "3_7"] = "3_7" if prev_shell.layout == "7_3" else "7_3"
        shell = _build_initial_shell(next_chord, next_layout, rh_octave=4, bass_octave=bass_octave, convention=convention)
        l1 = abs(shell.guide_tones[0] - v1_prev) + abs(shell.guide_tones[1] - v2_prev)
        resolution = GuideToneResolution(
            from_chord=prev_shell.chord_symbol,
            to_chord=next_chord.symbol,
            retained_note=None,
            moving_note_from=v1_prev,
            moving_note_to=shell.guide_tones[0],
            motion_semitones=shell.guide_tones[0] - v1_prev,
            resolution_type="LEAP",
            total_l1_distance=l1,
            description=f"Fallback transition to {shell.layout}",
        )
        return shell, resolution

    # Sort candidates by L1 distance, then by proximity to middle C register (60..72)
    candidates.sort(key=lambda c: (c[0], abs(c[1][0] - 60) + abs(c[1][1] - 67)))
    best_dist, best_tones, best_layout, best_3, best_7 = candidates[0]

    # Calculate bass note
    bass_note = 12 * (bass_octave + 1) + bass_pc
    while best_tones[0] - bass_note < 5:
        bass_note -= 12

    chord_symbol = next_chord.symbol
    lh_spelling = _format_midi_note(bass_note, convention)
    rh_spellings = (
        _format_midi_note(best_tones[0], convention),
        _format_midi_note(best_tones[1], convention),
    )

    next_shell = ShellVoicing(
        chord_symbol=chord_symbol,
        root_pc=root_pc,
        bass_note=bass_note,
        guide_tones=best_tones,
        third_note=best_3,
        seventh_note=best_7,
        layout=best_layout,
        lh_spelling=lh_spelling,
        rh_spellings=rh_spellings,
    )

    # Analyze guide tone resolution
    v1_curr, v2_curr = best_tones
    m1 = v1_curr - v1_prev
    m2 = v2_curr - v2_prev

    retained: Optional[int] = None
    moving_from: int = 0
    moving_to: int = 0
    motion_semi: int = 0

    if m1 == 0 and m2 != 0:
        retained = v1_curr
        moving_from = v2_prev
        moving_to = v2_curr
        motion_semi = m2
    elif m2 == 0 and m1 != 0:
        retained = v2_curr
        moving_from = v1_prev
        moving_to = v1_curr
        motion_semi = m1
    elif m1 == 0 and m2 == 0:
        retained = v1_curr
        moving_from = v2_prev
        moving_to = v2_curr
        motion_semi = 0
    else:
        # Both moving
        moving_from = v1_prev
        moving_to = v1_curr
        motion_semi = m1

    res_type: Literal["HALF_STEP_DOWN", "HALF_STEP_UP", "WHOLE_STEP_DOWN", "WHOLE_STEP_UP", "STATIC", "LEAP"]
    if motion_semi == -1:
        res_type = "HALF_STEP_DOWN"
    elif motion_semi == 1:
        res_type = "HALF_STEP_UP"
    elif motion_semi == -2:
        res_type = "WHOLE_STEP_DOWN"
    elif motion_semi == 2:
        res_type = "WHOLE_STEP_UP"
    elif motion_semi == 0 and m1 == 0 and m2 == 0:
        res_type = "STATIC"
    else:
        res_type = "LEAP"

    held_str = f"retaining {_format_midi_note(retained, convention)}" if retained is not None else "both voices moving"
    desc = (
        f"{prev_shell.chord_symbol} -> {next_chord.symbol}: {res_type} "
        f"({motion_semi:+d} st, {held_str}, L1={best_dist})"
    )

    resolution = GuideToneResolution(
        from_chord=prev_shell.chord_symbol,
        to_chord=next_chord.symbol,
        retained_note=retained,
        moving_note_from=moving_from,
        moving_note_to=moving_to,
        motion_semitones=motion_semi,
        resolution_type=res_type,
        total_l1_distance=best_dist,
        description=desc,
    )

    return next_shell, resolution


def generate_shell_voicings(
    progression: Union[str, List[str], Any, List[ChordDefinition]],
    key_root: str = "C",
    starting_layout: Literal["7_3", "3_7", "AUTO"] = "AUTO",
    bass_octave: int = 2,
    rh_octave: int = 4,
    convention: Literal["INT", "DE"] = "INT",
) -> ProgressionShellVoicings:
    """
    Generate an ergonomic, voice-led two-handed shell voicing arrangement for a chord progression.

    Parameters:
        progression: Chord progression string ("Dm7 - G7 - Cmaj7"), list of chord names,
                     CanonicalProgression, or list of ChordDefinition objects.
        key_root: Default key root if degree numerals need resolution.
        starting_layout: Initial right-hand guide tone order ('7_3', '3_7', or 'AUTO').
        bass_octave: Octave register for left-hand bass fundamentals (default: 2).
        rh_octave: Target octave register for right-hand guide tones (default: 4).
        convention: Pitch naming convention ('INT' or 'DE').

    Returns:
        ProgressionShellVoicings containing realized voicings and step-by-step resolution metrics.
    """
    # 1. Resolve chords into list of ChordDefinition
    chord_list: List[ChordDefinition] = []
    if isinstance(progression, str):
        tokens = [token.strip() for token in progression.replace("->", "-").replace(",", " ").split("-") if token.strip()]
        for token in tokens:
            chord_list.append(parse_chord(token))
    elif isinstance(progression, list):
        for item in progression:
            if isinstance(item, ChordDefinition):
                chord_list.append(item)
            elif isinstance(item, str):
                chord_list.append(parse_chord(item))
            else:
                raise ChordConstructionError(f"Unexpected chord element in progression: {item!r}")
    elif hasattr(progression, "chord_definitions"):
        chord_list = list(progression.chord_definitions)
    else:
        raise ChordConstructionError(f"Unsupported progression type: {type(progression)}")

    if not chord_list:
        return ProgressionShellVoicings(
            voicings=[],
            resolutions=[],
            total_l1_distance=0,
            average_l1_distance=0.0,
            starting_layout="7_3",
        )

    # 2. If starting_layout is AUTO, compute both '7_3' and '3_7' and select the one with lower L1 distance
    if starting_layout == "AUTO":
        cand_7_3 = _realize_progression(chord_list, "7_3", bass_octave, rh_octave, convention)
        cand_3_7 = _realize_progression(chord_list, "3_7", bass_octave, rh_octave, convention)
        return cand_7_3 if cand_7_3.total_l1_distance <= cand_3_7.total_l1_distance else cand_3_7

    return _realize_progression(chord_list, starting_layout, bass_octave, rh_octave, convention)


def _realize_progression(
    chords: List[ChordDefinition],
    layout: Literal["7_3", "3_7"],
    bass_octave: int,
    rh_octave: int,
    convention: Literal["INT", "DE"],
) -> ProgressionShellVoicings:
    """Realize the entire progression starting from a specific layout."""
    voicings: List[ShellVoicing] = []
    resolutions: List[GuideToneResolution] = []

    first_shell = _build_initial_shell(
        chords[0],
        layout=layout,
        rh_octave=rh_octave,
        bass_octave=bass_octave,
        convention=convention,
    )
    voicings.append(first_shell)

    curr_shell = first_shell
    total_l1 = 0

    for chord in chords[1:]:
        next_shell, resolution = _connect_next_shell(
            curr_shell,
            chord,
            bass_octave=bass_octave,
            convention=convention,
        )
        voicings.append(next_shell)
        resolutions.append(resolution)
        total_l1 += resolution.total_l1_distance
        curr_shell = next_shell

    avg_l1 = total_l1 / len(resolutions) if resolutions else 0.0

    return ProgressionShellVoicings(
        voicings=voicings,
        resolutions=resolutions,
        total_l1_distance=total_l1,
        average_l1_distance=round(avg_l1, 3),
        starting_layout=layout,
    )

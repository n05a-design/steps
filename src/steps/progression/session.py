"""
STEPS Progression Core: Interactive Session, Harmony Explorer & Vertical Slice.

Adheres to:
- M04 (Harmonielehre), M05 (Progressionsanalyse)
- ADR-005 (Explicit notation conventions DE/INT)
- ADR-006 (JSON storage & atomic persistence)
- ADR-007 (MIDI export service integration)
- 4-chord workflow (Edit -> Transpose -> Explore -> Save/Load -> MIDI Export)
"""

from __future__ import annotations

import copy
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from ..midi.export_service import Adr017NoteDuration, Adr017Voicing, MidiExportService
from ..models.timeline import TimeSignature
from ..storage.exceptions import CorruptedProjectError
from ..storage.project_io import Project, load_project_with_status, save_project
from ..storage.undo import UndoStack
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from ..theory.exceptions import ChordConstructionError, MusicTheoryError, PitchRangeError, ProgressionParsingError
from ..theory.pitch import NoteSpelling, parse_spelling
from ..theory.voice_leading import VoiceLeadingDiagnostic, find_perfect_interval_motion
from .engine import (
    _transpose_with_key,
    analyze_progression_voice_leading,
    detect_progression_archetypes,
    generate_progression_voicings,
    resolve_roman_degree,
)
from .harmony_analysis import format_harmonic_degree, has_dominant_quality, written_root_interval
from .voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
)


@dataclass(frozen=True)
class ChordRecommendation:
    """A suggested continuation chord with harmonic relation and proof."""
    candidate_symbol: str
    relation_type: Literal[
        "DOMINANT_OF", "RESOLVES_TO", "BORROWED_FROM",
        "VOICE_LEADING_NEAR", "SUBSTITUTES_FOR", "ROOT_MOTION", "SCHEMA_CONTINUATION"
    ]
    explanation: str
    framework: str
    source_id: str


@dataclass(frozen=True)
class DegreeAnalysis:
    """Analysis of a chord position in relation to key context."""
    index: int
    symbol: str
    roman_numeral: str
    semitone_distance_to_next: Optional[int] = None
    voice_leading_warnings: tuple[str, ...] = ()
    voice_leading_diagnostics: tuple[VoiceLeadingDiagnostic, ...] = field(
        default=(), compare=False, repr=False,
    )


@dataclass
class SessionState:
    """Serializable snapshot of progression session state."""
    title: str = "My Progression"
    chords: List[str] = field(default_factory=lambda: ["C", "G", "Am", "F"])
    key_root: str = "C"
    is_minor: bool = False
    convention: Literal["INT", "DE"] = "INT"
    bpm: float = 120.0
    ppq: int = 480
    chord_duration_ticks: int = 1920
    voice_leading_style: str = "CONTEMPORARY_POP"
    time_signature: Tuple[int, int] = (4, 4)
    chord_event_timings: List[Tuple[int, int]] = field(default_factory=list)


class ProgressionSession:
    """
    Stateful editor for chord progressions with full undo/redo, transposition,
    harmonic exploration, atomic persistence, and MIDI export.
    """

    def __init__(
        self,
        initial_chords: Optional[List[str]] = None,
        key_root: str = "C",
        is_minor: bool = False,
        convention: Literal["INT", "DE"] = "INT",
        bpm: float = 120.0,
        voice_leading_style: Union[str, VoiceLeadingStyle] = VoiceLeadingStyle.CONTEMPORARY_POP,
        title: Optional[str] = None,
    ):
        chords = initial_chords if initial_chords is not None else ["C", "G", "Am", "F"]
        # Verify initial chords can be parsed
        for sym in chords:
            parse_chord(sym, convention=convention)

        style_val = (
            voice_leading_style.value
            if isinstance(voice_leading_style, VoiceLeadingStyle)
            else str(voice_leading_style).upper()
        )

        init_state = SessionState(
            title=title.strip() if title is not None and title.strip() else "My Progression",
            chords=list(chords),
            key_root=key_root,
            is_minor=is_minor,
            convention=convention,
            bpm=bpm,
            voice_leading_style=style_val,
        )
        init_state.chord_event_timings = [
            (index * init_state.chord_duration_ticks, init_state.chord_duration_ticks)
            for index in range(len(chords))
        ]
        self._undo_stack = UndoStack[SessionState](init_state, max_depth=50)
        self.last_load_recovered_from_backup = False
        self.last_loaded_backup_path: Optional[Path] = None
        self.last_load_migrations: tuple[str, ...] = ()

    @property
    def state(self) -> SessionState:
        return self._undo_stack.current_state

    @staticmethod
    def _render_note_name(note: NoteSpelling, convention: Literal["INT", "DE"]) -> str:
        rendered = note.render(convention=convention, unicode_accidental=False)
        return re.sub(r"-?\d+$", "", rendered)

    def set_notation_convention(self, convention: Literal["INT", "DE"]) -> bool:
        """Explicitly converts project note spellings when the notation convention changes."""
        if convention not in ("INT", "DE"):
            raise ValueError("Notation convention must be INT or DE.")
        if convention == self.convention:
            return False

        try:
            key = parse_spelling(self.state.key_root, convention=self.convention)
            converted_key = self._render_note_name(key, convention)

            converted_chords: List[str] = []
            for symbol in self.chords:
                chord = parse_chord(symbol, convention=self.convention)
                root = self._render_note_name(chord.root, convention)
                quality = chord.quality
                converted = f"{root}{quality}"
                if chord.bass is not None:
                    converted += f"/{self._render_note_name(chord.bass, convention)}"
                parse_chord(converted, convention=convention)
                converted_chords.append(converted)
        except (MusicTheoryError, ChordConstructionError, ValueError) as exc:
            raise ValueError(
                f"Notation convention {convention} could not be applied safely: {exc}"
            ) from exc

        new_state = copy.deepcopy(self.state)
        new_state.convention = convention
        new_state.key_root = converted_key
        new_state.chords = converted_chords
        self._push_mutation(new_state)
        return True

    def reset_to_defaults(self) -> None:
        """Replaces the active session with a clean default project."""
        init_state = SessionState()
        init_state.chord_event_timings = [
            (index * init_state.chord_duration_ticks, init_state.chord_duration_ticks)
            for index in range(len(init_state.chords))
        ]
        self._undo_stack = UndoStack[SessionState](init_state, max_depth=50)
        self.last_load_recovered_from_backup = False
        self.last_loaded_backup_path = None
        self.last_load_migrations = ()

    @property
    def chords(self) -> List[str]:
        return list(self.state.chords)

    @property
    def key_root(self) -> str:
        return self.state.key_root

    @property
    def is_minor(self) -> bool:
        return self.state.is_minor

    @property
    def convention(self) -> Literal["INT", "DE"]:
        return self.state.convention

    @property
    def bpm(self) -> float:
        return self.state.bpm

    @property
    def time_signature(self) -> Tuple[int, int]:
        return self.state.time_signature

    def get_chord_event_timing(self, index: int) -> Tuple[int, int]:
        if not 0 <= index < len(self.state.chord_event_timings):
            raise IndexError(f"Chord index {index} out of range")
        return self.state.chord_event_timings[index]

    @property
    def voice_leading_style(self) -> VoiceLeadingStyle:
        try:
            return VoiceLeadingStyle(self.state.voice_leading_style)
        except ValueError:
            return VoiceLeadingStyle.CONTEMPORARY_POP

    def set_voice_leading_style(self, style: Union[str, VoiceLeadingStyle]) -> None:
        """Sets the active voice-leading style (e.g. CONTEMPORARY_POP vs. STRICT_CLASSICAL)."""
        resolved = (
            style
            if isinstance(style, VoiceLeadingStyle)
            else VoiceLeadingStyle(str(style).upper())
        )
        if resolved.value != self.state.voice_leading_style:
            new_state = copy.deepcopy(self.state)
            new_state.voice_leading_style = resolved.value
            self._push_mutation(new_state)

    @property
    def is_dirty(self) -> bool:
        return self._undo_stack.is_dirty

    @property
    def can_undo(self) -> bool:
        return self._undo_stack.can_undo

    @property
    def can_redo(self) -> bool:
        return self._undo_stack.can_redo

    def undo(self) -> None:
        self._undo_stack.undo()

    def redo(self) -> None:
        self._undo_stack.redo()

    def _push_mutation(self, new_state: SessionState) -> None:
        self._undo_stack.push(new_state)

    def set_chord(self, index: int, symbol: str) -> None:
        """Updates chord at index with parsing validation."""
        if not (0 <= index < len(self.chords)):
            raise IndexError(f"Chord index {index} out of range [0..{len(self.chords) - 1}]")
        parse_chord(symbol, convention=self.convention)

        new_chords = list(self.chords)
        new_chords[index] = symbol
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
        self._push_mutation(new_state)

    def add_chord(self, symbol: str, position: Optional[int] = None) -> None:
        """Appends or inserts a chord."""
        parse_chord(symbol, convention=self.convention)
        new_chords = list(self.chords)
        old_count = len(new_chords)
        if position is None:
            new_chords.append(symbol)
            insert_index = len(new_chords) - 1
        else:
            normalized_position = position if position >= 0 else old_count + position
            insert_index = max(0, min(normalized_position, old_count))
            new_chords.insert(insert_index, symbol)
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
        duration_ticks = new_state.chord_duration_ticks
        if position is None:
            previous_start, previous_duration = new_state.chord_event_timings[insert_index - 1]
            start_tick = previous_start + previous_duration
        elif insert_index < len(new_state.chord_event_timings):
            start_tick = new_state.chord_event_timings[insert_index][0]
            new_state.chord_event_timings = [
                (start + duration_ticks, duration)
                if index >= insert_index
                else (start, duration)
                for index, (start, duration) in enumerate(new_state.chord_event_timings)
            ]
        else:
            previous_start, previous_duration = new_state.chord_event_timings[insert_index - 1]
            start_tick = previous_start + previous_duration
        new_state.chord_event_timings.insert(insert_index, (start_tick, duration_ticks))
        self._push_mutation(new_state)

    def duplicate_chord_event(self, index: int) -> int:
        """Insert a copy starting at the source end, preserving other event timings."""
        start, duration = self.get_chord_event_timing(index)
        return self._insert_chord_copy(index, (start, duration), (start + duration, duration))

    def split_chord_event(self, index: int) -> int:
        """Split at the midpoint, assigning an odd remaining tick to the second part."""
        start, duration = self.get_chord_event_timing(index)
        if duration < 2:
            raise ValueError("A chord event needs at least two ticks to split.")
        first_duration = duration // 2
        return self._insert_chord_copy(
            index, (start, first_duration), (start + first_duration, duration - first_duration),
        )

    def _insert_chord_copy(
        self, index: int, first: tuple[int, int], second: tuple[int, int],
    ) -> int:
        new_state = copy.deepcopy(self.state)
        new_index = index + 1
        new_state.chords.insert(new_index, new_state.chords[index])
        new_state.chord_event_timings[index:new_index] = [first, second]
        self._push_mutation(new_state)
        return new_index

    def remove_chord(self, index: int) -> None:
        """Removes chord at index. Requires at least one chord to remain."""
        if len(self.chords) <= 1:
            raise ValueError("Progression must contain at least one chord.")
        if not (0 <= index < len(self.chords)):
            raise IndexError(f"Chord index {index} out of range")
        new_chords = list(self.chords)
        new_chords.pop(index)
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
        new_state.chord_event_timings.pop(index)
        self._push_mutation(new_state)

    def move_chord(self, index: int, direction: Literal[-1, 1]) -> None:
        """Moves a chord one position up (-1) or down (1) in the progression."""
        if direction not in (-1, 1):
            raise ValueError("Chord move direction must be -1 or 1.")
        if not (0 <= index < len(self.chords)):
            raise IndexError(f"Chord index {index} out of range")
        target = index + direction
        if not 0 <= target < len(self.chords):
            return

        new_chords = list(self.chords)
        new_chords[index], new_chords[target] = new_chords[target], new_chords[index]
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
        timings = list(new_state.chord_event_timings)
        timings[index], timings[target] = timings[target], timings[index]
        new_state.chord_event_timings = timings
        self._push_mutation(new_state)

    def set_chord_event_timing(self, index: int, start_tick: int, duration_ticks: int) -> None:
        """Sets one chord event's absolute tick position and positive tick duration."""
        if not 0 <= index < len(self.chords):
            raise IndexError(f"Chord index {index} out of range")
        if not isinstance(start_tick, int) or isinstance(start_tick, bool) or start_tick < 0:
            raise ValueError("Event start tick must be a non-negative integer.")
        if (
            not isinstance(duration_ticks, int)
            or isinstance(duration_ticks, bool)
            or duration_ticks <= 0
        ):
            raise ValueError("Event duration must be a positive integer.")
        if self.state.chord_event_timings[index] == (start_tick, duration_ticks):
            return

        new_state = copy.deepcopy(self.state)
        new_state.chord_event_timings[index] = (start_tick, duration_ticks)
        self._push_mutation(new_state)

    def transpose(self, semitones: int) -> None:
        """Transpose the progression and its tonal context together."""
        if type(semitones) is not int:
            raise MusicTheoryError("Transposition requires whole semitones.")
        if semitones == 0:
            return

        key = parse_spelling(self.key_root, convention=self.convention)
        chords = [parse_chord(symbol, convention=self.convention) for symbol in self.chords]
        for chord in chords:
            for note in (chord.root, chord.bass):
                if note is not None and not 0 <= note.midi_number + semitones <= 127:
                    raise PitchRangeError("Transposed chord note falls outside the MIDI range.")
        new_key, transposed = _transpose_with_key(key, chords, semitones)
        transposed_symbols = []
        for chord in transposed:
            root = self._render_note_name(chord.root, self.convention)
            symbol = root + chord.quality
            if chord.bass is not None:
                symbol += "/" + self._render_note_name(chord.bass, self.convention)
            # Only save symbols representable in the active notation.
            parse_chord(symbol, convention=self.convention)
            transposed_symbols.append(symbol)

        new_state = copy.deepcopy(self.state)
        new_state.chords = transposed_symbols
        new_state.key_root = self._render_note_name(new_key, self.convention)
        self._push_mutation(new_state)

    def set_key(self, new_key_root: str, is_minor: bool = False) -> None:
        """Updates tonal center key context."""
        parse_spelling(new_key_root, convention=self.convention)
        new_state = copy.deepcopy(self.state)
        new_state.key_root = new_key_root
        new_state.is_minor = is_minor
        self._push_mutation(new_state)

    def set_context(
        self,
        key_root: str,
        is_minor: bool,
        bpm: float,
        time_signature: Optional[Tuple[int, int]] = None,
        title: Optional[str] = None,
    ) -> None:
        """Atomically updates project title, tonal, tempo, and optional meter context."""
        if title is not None:
            if not isinstance(title, str) or not title.strip():
                raise ValueError("Project title must be a non-empty string.")
            normalized_title = title.strip()
        else:
            normalized_title = self.state.title
        if not isinstance(is_minor, bool):
            raise ValueError("Minor-mode selection must be a boolean.")
        parse_spelling(key_root, convention=self.convention)
        if isinstance(bpm, bool) or not isinstance(bpm, (int, float)):
            raise ValueError("Tempo must be a number between 20 and 400 BPM.")
        if not 20 <= bpm <= 400:
            raise ValueError("Tempo must be between 20 and 400 BPM.")
        meter = self.state.time_signature if time_signature is None else time_signature
        if (
            not isinstance(meter, tuple)
            or len(meter) != 2
            or any(not isinstance(value, int) or isinstance(value, bool) for value in meter)
        ):
            raise ValueError("Time signature must contain integer numerator and denominator.")
        if not 1 <= meter[0] <= 32:
            raise ValueError("Time signature numerator must be between 1 and 32.")
        try:
            TimeSignature(*meter)
        except ValueError as exc:
            raise ValueError(f"Invalid time signature: {exc}") from exc
        if (
            key_root == self.state.key_root
            and is_minor == self.state.is_minor
            and float(bpm) == self.state.bpm
            and meter == self.state.time_signature
            and normalized_title == self.state.title
        ):
            return

        new_state = copy.deepcopy(self.state)
        new_state.title = normalized_title
        new_state.key_root = key_root
        new_state.is_minor = is_minor
        new_state.bpm = float(bpm)
        new_state.time_signature = meter
        self._push_mutation(new_state)

    def get_voicings(
        self,
        voicing_type: Literal["CLOSE", "DROP2", "SHELL", "ROOTLESS"] = "CLOSE",
        style: Optional[Union[str, VoiceLeadingStyle]] = None,
    ) -> List[Voicing]:
        """Generates voice-led Voicing instances for all chords in session."""
        defs = [parse_chord(sym, convention=self.convention) for sym in self.chords]
        actual_voicing_type = voicing_type
        actual_vl_style = self.voice_leading_style if style is None else style
        if isinstance(actual_vl_style, str) and actual_vl_style.upper() in {"CLOSE", "DROP2", "SHELL", "ROOTLESS"}:
            actual_voicing_type = actual_vl_style.upper()  # type: ignore
            actual_vl_style = self.voice_leading_style
        return generate_progression_voicings(
            defs,
            style=actual_vl_style,
            initial_voicing_type=actual_voicing_type,
        )

    def get_beginner_voicings(
        self,
        starting_inversion: Optional[str] = None,
        lh_octave: int = 2,
        rh_octave: int = 4,
    ) -> Any:
        """
        Generates didactic beginner voicings, fingerings and smooth voice-leading guidance (OA-0024).
        """
        from ..theory.beginner_voicing import generate_beginner_voicings
        return generate_beginner_voicings(
            progression=self.chords,
            starting_inversion=starting_inversion,
            lh_octave=lh_octave,
            rh_octave=rh_octave,
            convention=self.convention,
        )

    def analyze_progression(
        self,
        style: Optional[Union[str, VoiceLeadingStyle]] = None,
        voicing_style: Optional[Union[str, VoiceLeadingStyle]] = None,
    ) -> List[DegreeAnalysis]:
        """
        Performs Roman numeral analysis and calculates adjacent voice-leading
        distances and parallel motion warnings according to the configured
        or specified diagnostic style. A separate voicing style can be supplied
        when comparing generated candidates.
        """
        analyses, _voicings = self.analyze_progression_with_voicings(style, voicing_style)
        return analyses

    def analyze_progression_with_voicings(
        self,
        style: Optional[Union[str, VoiceLeadingStyle]] = None,
        voicing_style: Optional[Union[str, VoiceLeadingStyle]] = None,
    ) -> Tuple[List[DegreeAnalysis], List[Voicing]]:
        """Return the analyses together with the exact voicings used to calculate them."""
        active_style = self.voice_leading_style if style is None else (
            style if isinstance(style, VoiceLeadingStyle) else VoiceLeadingStyle(str(style).upper())
        )
        generation_style = self.voice_leading_style if voicing_style is None else (
            voicing_style
            if isinstance(voicing_style, VoiceLeadingStyle)
            else VoiceLeadingStyle(str(voicing_style).upper())
        )
        voicings = self.get_voicings("CLOSE", style=generation_style)
        analyses: List[DegreeAnalysis] = []
        
        key_spelling = parse_spelling(self.key_root, convention=self.convention)
        chords = [parse_chord(symbol, convention=self.convention) for symbol in self.chords]

        for i, (sym, chord) in enumerate(zip(self.chords, chords, strict=True)):
            following = chords[i + 1] if i + 1 < len(chords) else None
            roman = format_harmonic_degree(
                chord, key_spelling, self.is_minor, self.convention, following,
            )

            dist: Optional[int] = None
            diagnostics: List[VoiceLeadingDiagnostic] = []
            if i + 1 < len(voicings):
                v_curr = voicings[i].midi_notes
                v_next = voicings[i + 1].midi_notes
                if len(v_curr) == len(v_next):
                    dist = absolute_semitone_distance(v_curr, v_next)
                    diagnostics = find_perfect_interval_motion(v_curr, v_next, style=active_style)

            analyses.append(DegreeAnalysis(
                index=i,
                symbol=sym,
                roman_numeral=roman,
                semitone_distance_to_next=dist,
                voice_leading_warnings=tuple(item.describe() for item in diagnostics),
                voice_leading_diagnostics=tuple(diagnostics),
            ))

        return analyses, voicings

    def harmonic_degree_at(self, index: int) -> str:
        """Analyze the selected event in its project key and immediate chord context."""
        chords = self.state.chords
        if not 0 <= index < len(chords):
            raise IndexError(f"Index {index} out of range")
        current = parse_chord(chords[index], convention=self.convention)
        following = (
            parse_chord(chords[index + 1], convention=self.convention)
            if index + 1 < len(chords) else None
        )
        key = parse_spelling(self.key_root, convention=self.convention)
        return format_harmonic_degree(current, key, self.is_minor, self.convention, following)

    def explore_next_chords(self, from_index: int) -> List[ChordRecommendation]:
        """
        Recommends typologically categorized continuation chords from from_index
        with clear theoretical justification and framework references.
        """
        if not (0 <= from_index < len(self.chords)):
            raise IndexError(f"Index {from_index} out of range")

        curr_sym = self.chords[from_index]
        curr_chord = parse_chord(curr_sym, convention=self.convention)
        recommendations: List[ChordRecommendation] = []

        key_spelling = parse_spelling(self.key_root, convention=self.convention)
        degree = written_root_interval(curr_chord.root, key_spelling)
        quality = curr_chord.quality
        tonic = key_spelling.render(self.convention)[:-1]
        dominant = has_dominant_quality(curr_chord)

        # A descending fifth establishes a root relation; a dominant quality supports a resolution.
        res_root = curr_chord.root.transpose_diatonic(step_delta=3, semitone_delta=5)
        res_sym = res_root.render(self.convention)[:-1]
        minor_targets = {(0, 0), (3, 5)} if self.is_minor else {(1, 2), (2, 4), (5, 9)}
        if dominant and written_root_interval(res_root, key_spelling) in minor_targets:
            res_sym += "m"
        recommendations.append(ChordRecommendation(
            candidate_symbol=res_sym,
            relation_type="RESOLVES_TO" if dominant else "ROOT_MOTION",
            explanation=(
                f"Mögliche Dominantauflösung von {curr_sym} nach {res_sym}; "
                "die Grundtöne liegen eine fallende Quinte auseinander."
                if dominant else
                f"Die Grundtöne von {curr_sym} und {res_sym} bilden einen Quintfall."
            ),
            framework="Dominant Resolution" if dominant else "Root Motion",
            source_id="Open Music Theory · Tonicization" if dominant else "STEPS interval model",
        ))

        # 2. Dominant Preparation (Secondary Dominant: V7 of next degree)
        sec_dom_root = curr_chord.root.transpose_diatonic(step_delta=4, semitone_delta=7)
        sec_dom_sym = f"{sec_dom_root.render(self.convention)[:-1]}7"
        recommendations.append(ChordRecommendation(
            candidate_symbol=sec_dom_sym,
            relation_type="DOMINANT_OF",
            explanation=f"{sec_dom_sym} kann als Dominante zu {curr_sym} zurückführen.",
            framework="Functional Harmony",
            source_id="Open Music Theory · Tonicization"
        ))

        # 3. Modal Interchange / Borrowed Chord (e.g. bVII or iv)
        if not self.is_minor:
            bvii_root = key_spelling.transpose_diatonic(step_delta=6, semitone_delta=10)
            bvii_sym = f"{bvii_root.render(self.convention)[:-1]}"
            recommendations.append(ChordRecommendation(
                candidate_symbol=bvii_sym,
                relation_type="BORROWED_FROM",
                explanation=f"Modal Interchange: Entlehnung der Subtonika {bvii_sym} aus dem parallelen Moll.",
                framework="Modal Mixture (Aldwell/Schachter)",
                source_id="omt-chromatic-subdominants"
            ))

        # 4. Root motion by a whole step
        near_root = curr_chord.root.transpose_diatonic(step_delta=1, semitone_delta=2)
        near_sym = f"{near_root.render(self.convention)[:-1]}m"
        recommendations.append(ChordRecommendation(
            candidate_symbol=near_sym,
            relation_type="ROOT_MOTION",
            explanation=f"Der Grundton von {near_sym} liegt einen Ganzton über dem Grundton von {curr_sym}.",
            framework="Root Motion",
            source_id="STEPS interval model"
        ))

        # 5. Andalusian Cadence / Phrygian Step (bVI -> V in minor)
        if self.is_minor:
            # bVI is 8 semitones above tonic
            if degree == (5, 8) and quality in ("", "maj7"):
                v_root = key_spelling.transpose_diatonic(step_delta=4, semitone_delta=7)
                v_sym = f"{v_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=v_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Andalusische Kadenz als mögliches Muster: Die Grundtöne von {curr_sym} und {v_sym} bilden einen absteigenden Halbtonschritt.",
                    framework="Andalusian Cadence / Phrygian Schema",
                    source_id="Gauldin (2004)"
                ))
                # Minor Jazz Blues Turnaround (bVImaj7 -> V7(#11))
                if quality == "maj7":
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=f"{v_root.render(self.convention)[:-1]}7(#11)",
                        relation_type="RESOLVES_TO",
                        explanation=f"Minor Jazz Blues Turnaround: Submediante {curr_sym} (bVImaj7) kann mit einem Halbtonschritt der Grundtöne zur alterierten Dominante führen: {v_root.render(self.convention)[:-1]}7(#11).",
                        framework="Minor Jazz Blues Submediant Turnaround",
                        source_id="Levine (1995)"
                    ))
            # Minor Jazz Blues Subdominant (iv7 -> bVImaj7)
            elif degree == (3, 5) and quality == "m7":
                bvi_root = key_spelling.transpose_diatonic(step_delta=5, semitone_delta=8)
                bvi_sym = f"{bvi_root.render(self.convention)[:-1]}maj7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=bvi_sym,
                    relation_type="VOICE_LEADING_NEAR",
                    explanation=f"Minor Jazz Blues Turnaround: Subdominante {curr_sym} (iv7) leitet zur Submediante {bvi_sym} (bVImaj7) über.",
                    framework="Minor Jazz Blues Submediant Turnaround",
                    source_id="Levine (1995)"
                ))
            # Minor Dominant Resolution (V7(#11) -> i7 or Afro-Cuban Rebound -> iv)
            elif degree == (4, 7) and dominant:
                if quality == "7#11":
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=f"{tonic}m7",
                        relation_type="RESOLVES_TO",
                        explanation=f"Minor Jazz Blues: {curr_sym} mit erhöhter Undezime kann nach {tonic}m7 führen.",
                        framework="Minor Jazz Blues Submediant Turnaround",
                        source_id="Terefenko (2014)",
                    ))
                if quality == "7":
                    iv_root = key_spelling.transpose_diatonic(step_delta=3, semitone_delta=5)
                    iv_sym = f"{iv_root.render(self.convention)[:-1]}m"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=iv_sym,
                        relation_type="SCHEMA_CONTINUATION",
                        explanation=f"Afro-Cuban Montuno Vamp als Stilidee: {curr_sym} kann zur Mollsubdominante {iv_sym} zurückführen.",
                        framework="Afro-Cuban Ostinato Vamp",
                        source_id="Mauleón (1993)",
                    ))
            # Subtonic in Minor (bVII -> I Picardy Third, i Liquid D&B, or IIImaj9 Soul Circle)
            elif degree == (6, 10) and quality in ("", "7"):
                i_major_sym = f"{key_spelling.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_major_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Picardy Third als Option am Phrasenende: {i_major_sym} ist die Durtonika im Mollkontext.",
                    framework="Picardy Third Resolution",
                    source_id="Aldwell/Schachter (1989)"
                ))
                i_minor_sym = f"{key_spelling.render(self.convention)[:-1]}m"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_minor_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Liquid D&B Sub-Pulse Cadence: Mögliche modale Fortsetzung im Ganztonschritt {curr_sym} (bVII) in die Moll-Tonika {i_minor_sym}.",
                    framework="Liquid D&B Sub-Pulse Cadence",
                    source_id="Butterfield (2010)"
                ))
                iii_root = key_spelling.transpose_diatonic(step_delta=2, semitone_delta=3)
                iii_sym = f"{iii_root.render(self.convention)[:-1]}maj9"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=iii_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Soul Circle of Fifths: Quintfall {curr_sym} (bVII) zur Durparallele {iii_sym} (IIImaj9).",
                    framework="Soul Circle of Fifths",
                    source_id="Mulholland (2013)"
                ))
            # Minor Line Cliché (tonic minor root)
            elif degree == (0, 0):
                root_prefix = curr_chord.root.render(self.convention)[:-1]
                if curr_chord.quality == "m":
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=f"{root_prefix}m(maj7)",
                        relation_type="VOICE_LEADING_NEAR",
                        explanation=f"Minor Line Cliché: Chromatische Innenstimme 8 -> 7 ({curr_sym} -> {root_prefix}m(maj7)).",
                        framework="Minor Line Cliché",
                        source_id="Levine (1995)"
                    ))
                elif curr_chord.quality in ("m(maj7)", "mmaj7"):
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=f"{root_prefix}m7",
                        relation_type="VOICE_LEADING_NEAR",
                        explanation=f"Minor Line Cliché: Chromatische Innenstimme 7 -> b7 ({curr_sym} -> {root_prefix}m7).",
                        framework="Minor Line Cliché",
                        source_id="Levine (1995)"
                    ))
                elif curr_chord.quality == "m7":
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=f"{root_prefix}m6",
                        relation_type="VOICE_LEADING_NEAR",
                        explanation=f"Minor Line Cliché: Chromatische Innenstimme b7 -> 6 ({curr_sym} -> {root_prefix}m6).",
                        framework="Minor Line Cliché",
                        source_id="Levine (1995)"
                    ))

        # 6. 50s Doo-Wop Turnaround Steps
        if not self.is_minor:
            # vi is 9 semitones above tonic
            if degree == (5, 9) and quality in ("m", "m7"):
                iv_root = key_spelling.transpose_diatonic(step_delta=3, semitone_delta=5)
                iv_sym = f"{iv_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=iv_sym,
                    relation_type="SCHEMA_CONTINUATION",
                    explanation=f"50s Doo-Wop als mögliches Muster: {iv_sym} übernimmt nach {curr_sym} die Stufe IV.",
                    framework="Doo-Wop Turnaround",
                    source_id="omt-four-chord-schemas"
                ))
            # The chromatic form and the minor forms of ii support different options.
            elif degree == (1, 2) and quality == "7":
                ii_symbol = f"{curr_chord.root.render(self.convention)[:-1]}m7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=ii_symbol,
                    relation_type="VOICE_LEADING_NEAR",
                    explanation=f"Bossa Nova Stimmführung als Stilidee: {curr_sym} und {ii_symbol} unterscheiden sich durch die um einen Halbton tiefere Terz.",
                    framework="Bossa Nova Applied Dominant",
                    source_id="Mauleón (1993)",
                ))
            elif degree == (1, 2) and quality in ("m", "m7"):
                bii_root = key_spelling.transpose_diatonic(step_delta=1, semitone_delta=1)
                bii_sym = f"{bii_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=bii_sym,
                    relation_type="SUBSTITUTES_FOR",
                    explanation=f"Tritonussubstitution: {bii_sym} kann in dieser Tonart V7 ersetzen und einen chromatischen Grundtonschritt zur Tonika bilden.",
                    framework="Tritone Substitution",
                    source_id="Open Music Theory · Substitutions",
                ))
                if quality == "m7":
                    bvii_root = key_spelling.transpose_diatonic(step_delta=6, semitone_delta=10)
                    bvii_sym = f"{bvii_root.render(self.convention)[:-1]}7"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=bvii_sym,
                        relation_type="SCHEMA_CONTINUATION",
                        explanation=f"Substitute Backdoor ii–V als Stilidee: Nach {curr_sym} lässt sich {bvii_sym} als Alternative zu V7 ausprobieren.",
                        framework="Substitute Backdoor ii-V",
                        source_id="Rawlins/Bahha (2005)",
                    ))
            # bII is 1 semitone above tonic (Extended Tritone Sub Altered)
            elif degree == (1, 1) and quality == "7#11":
                i_root = key_spelling
                i_sym = f"{i_root.render(self.convention)[:-1]}maj9"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Extended Tritone Sub (Altered): {curr_sym} mit erhöhter Undezime kann als Tritonussubstitution nach {i_sym} führen.",
                    framework="Extended Tritone Sub (Altered)",
                    source_id="Pease (2003)"
                ))
            # IV is 5 semitones above tonic (iv7 Backdoor or IVdom7 Blues)
            elif degree == (3, 5):
                if quality == "m7":
                    bvii_root = key_spelling.transpose_diatonic(step_delta=6, semitone_delta=10)
                    bvii_sym = f"{bvii_root.render(self.convention)[:-1]}7"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=bvii_sym,
                        relation_type="RESOLVES_TO",
                        explanation=f"Classical Jazz Backdoor ii-V: Moll-Subdominante {curr_sym} (iv7) leitet zur Backdoor-Dominante {bvii_sym} (bVII7) über.",
                        framework="Classical Jazz Backdoor ii-V",
                        source_id="Levine (1995)"
                    ))
                elif curr_chord.quality in ("7", "dom7"):
                    i_root = key_spelling
                    i_sym = f"{i_root.render(self.convention)[:-1]}7"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=i_sym,
                        relation_type="RESOLVES_TO",
                        explanation=f"12-Bar Blues: Subdominante {curr_sym} (IVdom7) kehrt zur Tonika {i_sym} (Idom7) zurück.",
                        framework="12-Bar Blues",
                        source_id="Rawlins/Bahha (2005)"
                    ))
            # bVII is 10 semitones above tonic (Backdoor resolution)
            elif degree == (6, 10) and quality == "7":
                i_root = key_spelling
                i_sym = f"{i_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Backdoor-Auflösung: Subtonika {curr_sym} (bVII7) löst sich subdominantisch in die Tonika {i_sym} auf.",
                    framework="Backdoor Progression",
                    source_id="Terefenko (2014)"
                ))
            # I is tonic (Secondary dominant lift to vi or Blues shift to IV7)
            elif degree == (0, 0):
                if curr_chord.quality in ("7", "dom7"):
                    iv_root = key_spelling.transpose_diatonic(step_delta=3, semitone_delta=5)
                    iv_sym = f"{iv_root.render(self.convention)[:-1]}7"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=iv_sym,
                        relation_type="RESOLVES_TO",
                        explanation=f"12-Bar Blues: Tonika-Dominantseptakkord {curr_sym} (Idom7) wechselt zur Subdominante {iv_sym} (IVdom7).",
                        framework="12-Bar Blues",
                        source_id="Rawlins/Bahha (2005)"
                    ))
                v_vi_root = key_spelling.transpose_diatonic(step_delta=2, semitone_delta=4)
                v_vi_sym = f"{v_vi_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=v_vi_sym,
                    relation_type="DOMINANT_OF",
                    explanation=f"Zwischendominante: {v_vi_sym} (V7/vi) bereitet leittönig die Tonikaparallele vi vor.",
                    framework="Zwischendominanten",
                    source_id="Kostka/Payne (2013)"
                ))
                v_v_root = key_spelling.transpose_diatonic(step_delta=1, semitone_delta=2)
                v_v_sym = f"{v_v_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=v_v_sym,
                    relation_type="DOMINANT_OF",
                    explanation=f"Bossa Nova Doppeldominante: {v_v_sym} (V7/V) kann als Dominante der Dominante zur Stufe V führen.",
                    framework="Bossa Nova Applied Dominant",
                    source_id="Mauleón (1993)"
                ))
            # iii is 4 semitones above tonic (Royal Road mediant -> submediant)
            elif degree == (2, 4) and quality in ("m", "m7"):
                vi_root = key_spelling.transpose_diatonic(step_delta=5, semitone_delta=9)
                vi_sym = f"{vi_root.render(self.convention)[:-1]}m"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=vi_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Royal Road (Ōdō shinkō): Möglicher Quintfall von {curr_sym} (iii) in die Tonikaparallele {vi_sym} (vi).",
                    framework="Royal Road (Ōdō shinkō)",
                    source_id="Jaffe (1996)"
                ))

        # Conventional jazz qualities are offered as choices, without inferring a genre or phrase.
        if degree == (1, 2) and quality == ("m7b5" if self.is_minor else "m7"):
            v_root = key_spelling.transpose_diatonic(step_delta=4, semitone_delta=7)
            v_symbol = f"{v_root.render(self.convention)[:-1]}7"
            recommendations.append(ChordRecommendation(
                candidate_symbol=v_symbol,
                relation_type="SCHEMA_CONTINUATION",
                explanation=f"{curr_sym} → {v_symbol} entspricht den ersten beiden Akkorden einer Jazz-ii–V–I-Folge in dieser Tonart.",
                framework="Jazz ii–V–I",
                source_id="omt-ii-v-i",
            ))
        elif degree == (4, 7) and dominant and quality != "":
            suffix = "m7" if self.is_minor else "maj7"
            recommendations.append(ChordRecommendation(
                candidate_symbol=tonic + suffix,
                relation_type="RESOLVES_TO",
                explanation=f"{curr_sym} kann sich im Jazz zur Tonika {tonic}{suffix} auflösen.",
                framework="Jazz ii–V–I",
                source_id="omt-ii-v-i",
            ))

        return recommendations

    def identify_archetypes(self, allow_rotations: bool = True) -> list[dict[str, Any]]:
        """
        Identifies canonical progression archetypes matching the current session chords,
        including exact matches, rotations (e.g. Pop 4-Chord rotations) and transpositions.
        """
        return detect_progression_archetypes(
            self.chords,
            key_root=self.key_root,
            is_minor_key=self.is_minor,
            allow_rotations=allow_rotations,
            convention=self.convention,
        )

    def save_to_file(self, file_path: Path | str) -> Path:
        """Saves current session state to a STEPS project file."""
        events = []
        for sym, (start_tick, duration_ticks) in zip(
            self.chords, self.state.chord_event_timings
        ):
            events.append({
                "start_tick": start_tick,
                "duration_ticks": duration_ticks,
                "payload": sym
            })

        proj = Project(
            title=self.state.title,
            notation_convention=self.convention,
            metadata={
                "voice_leading_style": self.voice_leading_style.value,
                "key_root": self.key_root,
                "is_minor": self.is_minor,
            },
            time_settings={
                "ppq": self.state.ppq,
                "time_signature": {
                    "numerator": self.state.time_signature[0],
                    "denominator": self.state.time_signature[1],
                },
                "tempo_bpm": self.bpm,
                "tempo_points": [{"start_tick": 0, "bpm": self.bpm}]
            },
            tracks=[
                {
                    "track_id": "trk_chords",
                    "track_type": "CHORDS",
                    "name": "Chords Progression",
                    "channel": 0,
                    "events": events
                }
            ]
        )
        saved = save_project(proj, file_path)
        self._undo_stack.mark_clean()
        return saved

    def load_from_file(self, file_path: Path | str) -> None:
        """Loads session state from a STEPS project file."""
        load_result = load_project_with_status(file_path)
        proj = load_result.project
        if not isinstance(proj.title, str) or not proj.title.strip():
            raise CorruptedProjectError("Project title must be a non-empty string.")
        if proj.notation_convention not in ("INT", "DE"):
            raise CorruptedProjectError(
                f"Unsupported notation convention: {proj.notation_convention!r}"
            )
        if not isinstance(proj.metadata, dict):
            raise CorruptedProjectError("Project metadata must be an object.")
        if not isinstance(proj.time_settings, dict) or not isinstance(proj.tracks, list):
            raise CorruptedProjectError("Project time settings and tracks have invalid types.")

        chords: List[str] = []
        chord_event_timings: List[Tuple[int, int]] = []
        for trk in proj.tracks:
            if not isinstance(trk, dict):
                raise CorruptedProjectError("Project track entries must be objects.")
            if trk.get("track_type") == "CHORDS":
                events = trk.get("events", [])
                if not isinstance(events, list):
                    raise CorruptedProjectError("Chord track events must be an array.")
                default_duration = proj.time_settings.get("ppq", 480) * 4
                for event_index, ev in enumerate(events):
                    if not isinstance(ev, dict):
                        raise CorruptedProjectError("Chord track event entries must be objects.")
                    payload = ev.get("payload")
                    if isinstance(payload, str):
                        symbol = payload
                    elif isinstance(payload, dict) and "symbol" in payload:
                        symbol = payload["symbol"]
                        if not isinstance(symbol, str):
                            raise CorruptedProjectError("Chord event symbols must be strings.")
                    else:
                        raise CorruptedProjectError("Chord events must contain a chord symbol.")
                    try:
                        parse_chord(symbol, convention=proj.notation_convention)
                    except MusicTheoryError as exc:
                        raise CorruptedProjectError(
                            f"Invalid chord symbol in project: {symbol!r}"
                        ) from exc
                    chords.append(symbol)
                    start_tick = ev.get("start_tick", event_index * default_duration)
                    duration_ticks = ev.get("duration_ticks", default_duration)
                    if (
                        not isinstance(start_tick, int)
                        or isinstance(start_tick, bool)
                        or start_tick < 0
                        or not isinstance(duration_ticks, int)
                        or isinstance(duration_ticks, bool)
                        or duration_ticks <= 0
                    ):
                        raise CorruptedProjectError(
                            "Chord event timing must use a non-negative start and positive integer duration."
                        )
                    chord_event_timings.append((start_tick, duration_ticks))
                break

        bpm = proj.time_settings.get("tempo_bpm", 120.0)
        ppq = proj.time_settings.get("ppq", 480)
        meter_data = proj.time_settings.get(
            "time_signature", {"numerator": 4, "denominator": 4}
        )
        dur = ppq * 4
        key_root = proj.metadata.get("key_root", "C")
        is_minor = proj.metadata.get("is_minor", False)
        style_val = proj.metadata.get("voice_leading_style", "CONTEMPORARY_POP")
        if not isinstance(key_root, str) or not isinstance(is_minor, bool):
            raise CorruptedProjectError("Project key context has invalid types.")
        try:
            parse_spelling(key_root, convention=proj.notation_convention)
            resolved_style = VoiceLeadingStyle(str(style_val).upper())
        except (MusicTheoryError, ValueError) as exc:
            raise CorruptedProjectError(f"Invalid project key or voice-leading style: {exc}") from exc
        if not isinstance(bpm, (int, float)) or not 20 <= bpm <= 400:
            raise CorruptedProjectError(f"Invalid project tempo: {bpm!r}")
        if not isinstance(ppq, int) or isinstance(ppq, bool) or not 96 <= ppq <= 1920:
            raise CorruptedProjectError(f"Invalid project PPQ: {ppq!r}")
        if not isinstance(meter_data, dict):
            raise CorruptedProjectError("Project time signature must be an object.")
        numerator = meter_data.get("numerator")
        denominator = meter_data.get("denominator")
        if (
            not isinstance(numerator, int)
            or isinstance(numerator, bool)
            or not 1 <= numerator <= 32
            or not isinstance(denominator, int)
            or isinstance(denominator, bool)
        ):
            raise CorruptedProjectError("Project time signature has invalid values.")
        try:
            TimeSignature(numerator, denominator)
        except ValueError as exc:
            raise CorruptedProjectError(f"Invalid project time signature: {exc}") from exc

        new_state = SessionState(
            title=proj.title,
            chords=chords,
            key_root=key_root,
            is_minor=is_minor,
            convention=proj.notation_convention,
            bpm=bpm,
            time_signature=(numerator, denominator),
            ppq=ppq,
            chord_duration_ticks=dur,
            voice_leading_style=resolved_style.value,
            chord_event_timings=chord_event_timings,
        )
        self._undo_stack = UndoStack[SessionState](new_state, max_depth=50)
        self.last_load_recovered_from_backup = load_result.recovered_from_backup
        self.last_loaded_backup_path = load_result.backup_path
        self.last_load_migrations = load_result.migrations

    def midi_voicing_failures(self) -> dict[Adr017Voicing, str]:
        """Identify which export modes cannot voice the current progression."""
        return MidiExportService.adr017_voicing_failures(self.chords, self.convention)

    def midi_overlap_summary(
        self, voicing_type: Adr017Voicing, note_duration_mode: Adr017NoteDuration,
    ) -> tuple[int, int | None]:
        """Preview overlapping attacks under the current project timing."""
        return MidiExportService.adr017_overlap_summary(
            self.chords,
            self.state.chord_event_timings,
            convention=self.convention,
            voicing_type=voicing_type,
            note_duration_mode=note_duration_mode,
        )

    def export_midi_file(
        self,
        file_path: Path | str,
        *,
        voicing_type: Literal["CLOSE", "DROP2", "ROOTLESS"] = "CLOSE",
        note_duration_mode: Literal["FIXED_GAP", "PERCENT_95"] = "FIXED_GAP",
        smf_format: Literal[0, 1] = 1,
    ) -> Path:
        """Exports the active progression using the ADR-017 v0.1 MIDI contract."""
        key_spelling = parse_spelling(self.key_root, convention=self.convention)
        fifths_by_step = {"C": 0, "D": 2, "E": 4, "F": -1, "G": 1, "A": 3, "B": 5}
        key_accidentals = (
            fifths_by_step[key_spelling.step]
            + 7 * key_spelling.alteration
            - (3 if self.is_minor else 0)
        )
        if not -7 <= key_accidentals <= 7:
            key_accidentals = None

        return MidiExportService.export_progression_adr017(
            chords=self.chords,
            output_path=file_path,
            bpm=self.bpm,
            ppq=self.state.ppq,
            chord_duration_quarters=self.state.chord_duration_ticks / self.state.ppq,
            time_signature=self.state.time_signature,
            key_accidentals=key_accidentals,
            is_minor_key=self.is_minor,
            convention=self.convention,
            event_timings=self.state.chord_event_timings,
            voicing_type=voicing_type,
            note_duration_mode=note_duration_mode,
            smf_format=smf_format,
        )

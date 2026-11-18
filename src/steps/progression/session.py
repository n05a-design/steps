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
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Dict, List, Literal, Optional, Tuple, Union

from ..midi.export_service import MidiExportService
from ..models.timeline import TimeSignature
from ..storage.exceptions import CorruptedProjectError
from ..storage.project_io import Project, load_project_with_status, save_project
from ..storage.undo import UndoStack
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from ..theory.exceptions import ChordConstructionError, MusicTheoryError, ProgressionParsingError
from ..theory.pitch import NoteSpelling, parse_spelling
from .engine import (
    analyze_progression_voice_leading,
    detect_progression_archetypes,
    generate_progression_voicings,
    resolve_roman_degree,
)
from .voice_leading import (
    VoiceLeadingStyle,
    absolute_semitone_distance,
    detect_parallel_fifths_octaves,
)


@dataclass(frozen=True)
class ChordRecommendation:
    """A suggested continuation chord with harmonic relation and proof."""
    candidate_symbol: str
    relation_type: Literal[
        "DOMINANT_OF", "RESOLVES_TO", "BORROWED_FROM",
        "VOICE_LEADING_NEAR", "SUBSTITUTES_FOR"
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
            new_chords.insert(position, symbol)
            normalized_position = position if position >= 0 else old_count + position
            insert_index = max(0, min(normalized_position, old_count))
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
        if insert_index == 0:
            start_tick = 0
        else:
            previous_start, previous_duration = new_state.chord_event_timings[insert_index - 1]
            start_tick = previous_start + previous_duration
        duration_ticks = new_state.chord_duration_ticks
        if position is not None:
            new_state.chord_event_timings = [
                (start + duration_ticks, duration)
                if index >= insert_index
                else (start, duration)
                for index, (start, duration) in enumerate(new_state.chord_event_timings)
            ]
        new_state.chord_event_timings.insert(insert_index, (start_tick, duration_ticks))
        self._push_mutation(new_state)

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
        """
        Transposes all chords and key root by semitones, preserving
        orthographic spelling.
        """
        if semitones == 0:
            return

        transposed_chords: List[str] = []
        for sym in self.chords:
            ch = parse_chord(sym, convention=self.convention)
            new_root = ch.root.transpose_chromatic(semitones)
            new_sym = f"{new_root.render(self.convention)[:-1]}{ch.quality}"
            if ch.bass is not None:
                new_bass = ch.bass.transpose_chromatic(semitones)
                new_sym += f"/{new_bass.render(self.convention)[:-1]}"
            transposed_chords.append(new_sym)

        # Transpose key root
        old_key_spelling = parse_spelling(self.key_root, convention=self.convention)
        new_key_spelling = old_key_spelling.transpose_chromatic(semitones)
        new_key_root = new_key_spelling.render(self.convention)[:-1]

        new_state = copy.deepcopy(self.state)
        new_state.chords = transposed_chords
        new_state.key_root = new_key_root
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
    ) -> List[DegreeAnalysis]:
        """
        Performs Roman numeral analysis and calculates adjacent voice-leading
        distances and parallel motion warnings according to the configured
        or specified voice leading style.
        """
        active_style = self.voice_leading_style if style is None else (
            style if isinstance(style, VoiceLeadingStyle) else VoiceLeadingStyle(str(style).upper())
        )
        voicings = self.get_voicings("CLOSE")
        analyses: List[DegreeAnalysis] = []
        
        # Roman numeral mapping map (common degrees)
        key_spelling = parse_spelling(self.key_root, convention=self.convention)
        key_pc = int(key_spelling.pitch_class)

        major_scale_degrees = {0: "I", 2: "ii", 4: "iii", 5: "IV", 7: "V", 9: "vi", 11: "vii°", 10: "bVII"}
        minor_scale_degrees = {0: "i", 2: "ii°", 3: "III", 5: "iv", 7: "V", 8: "VI", 10: "VII", 11: "vii°"}
        deg_map = minor_scale_degrees if self.is_minor else major_scale_degrees

        for i, sym in enumerate(self.chords):
            ch = parse_chord(sym, convention=self.convention)
            root_pc = int(ch.root.pitch_class)
            interval_from_tonic = (root_pc - key_pc) % 12
            
            roman = deg_map.get(interval_from_tonic, "?")
            # Refine quality case
            if "m" in ch.quality and not roman.islower() and roman != "?":
                roman = roman.lower()
            if ch.quality in ("7", "maj7", "m7"):
                roman += ch.quality

            dist: Optional[int] = None
            warnings: List[str] = []
            if i + 1 < len(voicings):
                v_curr = voicings[i].midi_notes
                v_next = voicings[i + 1].midi_notes
                if len(v_curr) == len(v_next):
                    dist = absolute_semitone_distance(v_curr, v_next)
                    warnings = detect_parallel_fifths_octaves(v_curr, v_next, style=active_style)

            analyses.append(DegreeAnalysis(
                index=i,
                symbol=sym,
                roman_numeral=roman,
                semitone_distance_to_next=dist,
                voice_leading_warnings=tuple(warnings)
            ))

        return analyses

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

        # 1. Circle of Fifths / Dominant Resolution (V7 -> I, or Secondary Dominant)
        # Target: down 7 semitones (up 5 semitones)
        res_root = curr_chord.root.transpose_diatonic(step_delta=3, semitone_delta=5)
        res_sym = f"{res_root.render(self.convention)[:-1]}"
        recommendations.append(ChordRecommendation(
            candidate_symbol=res_sym,
            relation_type="RESOLVES_TO",
            explanation=f"Quintauflösung (Quintfall): {curr_sym} löst sich nach {res_sym} auf.",
            framework="Stufentheorie / Functional Harmony",
            source_id="omt-roman-numerals"
        ))

        # 2. Dominant Preparation (Secondary Dominant: V7 of next degree)
        sec_dom_root = curr_chord.root.transpose_diatonic(step_delta=4, semitone_delta=7)
        sec_dom_sym = f"{sec_dom_root.render(self.convention)[:-1]}7"
        recommendations.append(ChordRecommendation(
            candidate_symbol=sec_dom_sym,
            relation_type="DOMINANT_OF",
            explanation=f"Zwischendominante: {sec_dom_sym} bereitet {curr_sym} mit Leitton vor.",
            framework="Funktionstheorie (Riemann / Schönberg)",
            source_id="omt-chromatic-subdominants"
        ))

        # 3. Modal Interchange / Borrowed Chord (e.g. bVII or iv)
        if not self.is_minor:
            key_spelling = parse_spelling(self.key_root, convention=self.convention)
            bvii_root = key_spelling.transpose_diatonic(step_delta=6, semitone_delta=10)
            bvii_sym = f"{bvii_root.render(self.convention)[:-1]}"
            recommendations.append(ChordRecommendation(
                candidate_symbol=bvii_sym,
                relation_type="BORROWED_FROM",
                explanation=f"Modal Interchange: Entlehnung der Subtonika {bvii_sym} aus dem parallelen Moll.",
                framework="Modal Mixture (Aldwell/Schachter)",
                source_id="omt-chromatic-subdominants"
            ))

        # 4. Voice-Leading Near (Stepwise bass motion)
        near_root = curr_chord.root.transpose_diatonic(step_delta=1, semitone_delta=2)
        near_sym = f"{near_root.render(self.convention)[:-1]}m"
        recommendations.append(ChordRecommendation(
            candidate_symbol=near_sym,
            relation_type="VOICE_LEADING_NEAR",
            explanation=f"Schrittweise Bass- und Stimmfortschreitung (+2 Halbtöne) zu {near_sym}.",
            framework="Tymoczko L1 Geometry",
            source_id="REF-0019"
        ))

        # 5. Andalusian Cadence / Phrygian Step (bVI -> V in minor)
        if self.is_minor:
            key_spelling = parse_spelling(self.key_root, convention=self.convention)
            key_pc = int(key_spelling.pitch_class)
            curr_pc = int(curr_chord.root.pitch_class)
            # bVI is 8 semitones above tonic
            if (curr_pc - key_pc) % 12 == 8:
                v_root = key_spelling.transpose_diatonic(step_delta=4, semitone_delta=7)
                v_sym = f"{v_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=v_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Andalusische Kadenz / Phrygischer Halbschluss: Leittönige Auflösung {curr_sym} -> {v_sym} mit charakteristischem Halbtonschritt im Bass.",
                    framework="Andalusian Cadence / Phrygian Schema",
                    source_id="Gauldin (2004)"
                ))
                # Minor Jazz Blues Turnaround (bVImaj7 -> V7(#11))
                recommendations.append(ChordRecommendation(
                    candidate_symbol=f"{v_root.render(self.convention)[:-1]}7(#11)",
                    relation_type="RESOLVES_TO",
                    explanation=f"Minor Jazz Blues Turnaround: Submediante {curr_sym} (bVImaj7) leitet über Halbtonschritt zur alterierten Dominante {v_root.render(self.convention)[:-1]}7(#11).",
                    framework="Minor Jazz Blues Submediant Turnaround",
                    source_id="Levine (1995)"
                ))
            # Minor Jazz Blues Subdominant (iv7 -> bVImaj7)
            elif (curr_pc - key_pc) % 12 == 5:
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
            elif (curr_pc - key_pc) % 12 == 7:
                i_root = key_spelling
                i_sym = f"{i_root.render(self.convention)[:-1]}m7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Minor Jazz Blues: Alterierte Dominante {curr_sym} löst sich in die Tonika {i_sym} (i7) auf.",
                    framework="Minor Jazz Blues Submediant Turnaround",
                    source_id="Terefenko (2014)"
                ))
                iv_root = key_spelling.transpose_diatonic(step_delta=3, semitone_delta=5)
                iv_sym = f"{iv_root.render(self.convention)[:-1]}m"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=iv_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Afro-Cuban Montuno Vamp: Rebound von Dominante {curr_sym} (V7) über die Subdominante {iv_sym} (iv).",
                    framework="Afro-Cuban Ostinato Vamp",
                    source_id="Mauleón (1993)"
                ))
            # Subtonic in Minor (bVII -> I Picardy Third, i Liquid D&B, or IIImaj9 Soul Circle)
            elif (curr_pc - key_pc) % 12 == 10:
                i_major_sym = f"{key_spelling.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_major_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Picardy Third (Tierce de Picardie): Unerwartete modale Aufhellung von Moll nach Dur ({curr_sym} -> {i_major_sym}).",
                    framework="Picardy Third Resolution",
                    source_id="Aldwell/Schachter (1989)"
                ))
                i_minor_sym = f"{key_spelling.render(self.convention)[:-1]}m"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_minor_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Liquid D&B Sub-Pulse Cadence: Modaler Ganzton-Schluss {curr_sym} (bVII) in die Moll-Tonika {i_minor_sym}.",
                    framework="Liquid D&B Sub-Pulse Cadence",
                    source_id="Butterfield (2010)"
                ))
                iii_root = key_spelling.transpose_diatonic(step_delta=2, semitone_delta=3)
                iii_sym = f"{iii_root.render(self.convention)[:-1]}maj9"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=iii_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Soul Circle of Fifths: Quintfall {curr_sym} (bVII) in die Dur-Parallele {iii_sym} (IIImaj9).",
                    framework="Soul Circle of Fifths",
                    source_id="Mulholland (2013)"
                ))
            # Minor Line Cliché (tonic minor root)
            elif (curr_pc - key_pc) % 12 == 0:
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
            key_spelling = parse_spelling(self.key_root, convention=self.convention)
            key_pc = int(key_spelling.pitch_class)
            curr_pc = int(curr_chord.root.pitch_class)
            # vi is 9 semitones above tonic
            if (curr_pc - key_pc) % 12 == 9:
                iv_root = key_spelling.transpose_diatonic(step_delta=3, semitone_delta=5)
                iv_sym = f"{iv_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=iv_sym,
                    relation_type="VOICE_LEADING_NEAR",
                    explanation=f"50s Doo-Wop Kadenz: Subdominante {iv_sym} folgt auf Tonikaparallele {curr_sym} und bereitet Dominante vor.",
                    framework="Doo-Wop Turnaround",
                    source_id="Aldwell/Schachter (1989)"
                ))
            # V is 7 semitones above tonic
            elif (curr_pc - key_pc) % 12 == 7:
                i_root = key_spelling
                i_sym = f"{i_root.render(self.convention)[:-1]}"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Authentischer Ganzschluss: Dominante {curr_sym} löst sich in die Tonika {i_sym} auf.",
                    framework="Stufentheorie / Functional Harmony",
                    source_id="Kostka/Payne (2013)"
                ))
            # ii is 2 semitones above tonic (Tritone substitution candidate or Bossa Nova V7/V)
            elif (curr_pc - key_pc) % 12 == 2:
                if curr_chord.quality in ("7", "dom7"):
                    ii_root = key_spelling.transpose_diatonic(step_delta=1, semitone_delta=2)
                    ii_sym = f"{ii_root.render(self.convention)[:-1]}m7"
                    recommendations.append(ChordRecommendation(
                        candidate_symbol=ii_sym,
                        relation_type="VOICE_LEADING_NEAR",
                        explanation=f"Bossa Nova Stimmführung: Terzabsenkung von {curr_sym} (V7/V) in die Moll-Subdominantparallele {ii_sym} (ii7).",
                        framework="Bossa Nova Applied Dominant",
                        source_id="Mauleón (1993)"
                    ))
                bii_root = key_spelling.transpose_diatonic(step_delta=1, semitone_delta=1)
                bii_sym = f"{bii_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=bii_sym,
                    relation_type="SUBSTITUTES_FOR",
                    explanation=f"Tritonussubstitution: {bii_sym} (bII7) ersetzt die Quintfall-Dominante V7 durch chromatischen Bassabstieg.",
                    framework="Tritone Substitution",
                    source_id="Levine (1995)"
                ))
                bvii_root = key_spelling.transpose_diatonic(step_delta=6, semitone_delta=10)
                bvii_sym = f"{bvii_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=bvii_sym,
                    relation_type="SUBSTITUTES_FOR",
                    explanation=f"Substitute Backdoor ii-V: {bvii_sym} (bVII7) ersetzt V7 nach {curr_sym} (ii7) in einer Backdoor-Kadenz.",
                    framework="Substitute Backdoor ii-V",
                    source_id="Rawlins/Bahha (2005)"
                ))
            # bII is 1 semitone above tonic (Extended Tritone Sub Altered)
            elif (curr_pc - key_pc) % 12 == 1:
                i_root = key_spelling
                i_sym = f"{i_root.render(self.convention)[:-1]}maj9"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=i_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Extended Tritone Sub (Altered): Alterierte Tritonussubstitution {curr_sym} (bII7) löst sich mit Antizipation der #11 in die Tonika {i_sym} auf.",
                    framework="Extended Tritone Sub (Altered)",
                    source_id="Pease (2003)"
                ))
            # IV is 5 semitones above tonic (iv7 Backdoor or IVdom7 Blues)
            elif (curr_pc - key_pc) % 12 == 5:
                if curr_chord.quality in ("m", "m7"):
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
            elif (curr_pc - key_pc) % 12 == 10:
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
            elif (curr_pc - key_pc) % 12 == 0:
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
                    explanation=f"Bossa Nova Doppeldominante: {v_v_sym} (V7/V) bereitet als Zwischendominante die Subdominantparallele ii vor.",
                    framework="Bossa Nova Applied Dominant",
                    source_id="Mauleón (1993)"
                ))
            # iii is 4 semitones above tonic (Royal Road mediant -> submediant)
            elif (curr_pc - key_pc) % 12 == 4:
                vi_root = key_spelling.transpose_diatonic(step_delta=5, semitone_delta=9)
                vi_sym = f"{vi_root.render(self.convention)[:-1]}m"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=vi_sym,
                    relation_type="RESOLVES_TO",
                    explanation=f"Royal Road (Ōdō shinkō): Quintfall von mediantischem {curr_sym} (iii) in die Tonikaparallele {vi_sym} (vi).",
                    framework="Royal Road (Ōdō shinkō)",
                    source_id="Jaffe (1996)"
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
        self.last_load_recovered_from_backup = False
        self.last_loaded_backup_path = None
        self.last_load_migrations = ()
        load_result = load_project_with_status(file_path)
        proj = load_result.project
        self.last_load_recovered_from_backup = load_result.recovered_from_backup
        self.last_loaded_backup_path = load_result.backup_path
        self.last_load_migrations = load_result.migrations
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

    def export_midi_file(self, file_path: Path | str) -> Path:
        """Exports the active progression session as an SMF Format 1 MIDI file."""
        voicings = self.get_voicings("CLOSE")
        return MidiExportService.export_voicings_to_smf(
            voicings=voicings,
            output_path=file_path,
            bpm=self.bpm,
            ppq=self.state.ppq,
            chord_duration_ticks=self.state.chord_duration_ticks,
            time_signature=self.state.time_signature,
            event_timings=self.state.chord_event_timings,
            smf_format=1
        )

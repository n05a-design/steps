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
from typing import Any, Dict, List, Literal, Optional, Tuple

from ..midi.export_service import MidiExportService
from ..storage.project_io import Project, load_project, save_project
from ..storage.undo import UndoStack
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from ..theory.exceptions import ChordConstructionError, ProgressionParsingError
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
        bpm: float = 120.0
    ):
        chords = initial_chords if initial_chords is not None else ["C", "G", "Am", "F"]
        # Verify initial chords can be parsed
        for sym in chords:
            parse_chord(sym, convention=convention)

        init_state = SessionState(
            chords=list(chords),
            key_root=key_root,
            is_minor=is_minor,
            convention=convention,
            bpm=bpm
        )
        self._undo_stack = UndoStack[SessionState](init_state, max_depth=50)

    @property
    def state(self) -> SessionState:
        return self._undo_stack.current_state

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
        if position is None:
            new_chords.append(symbol)
        else:
            new_chords.insert(position, symbol)
        new_state = copy.deepcopy(self.state)
        new_state.chords = new_chords
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

    def get_voicings(self, style: Literal["CLOSE", "DROP2", "SHELL", "ROOTLESS"] = "CLOSE") -> List[Voicing]:
        """Generates voice-led Voicing instances for all chords in session."""
        defs = [parse_chord(sym, convention=self.convention) for sym in self.chords]
        return generate_progression_voicings(defs, style=style)

    def analyze_progression(self) -> List[DegreeAnalysis]:
        """
        Performs Roman numeral analysis and calculates adjacent voice-leading
        distances and parallel motion warnings.
        """
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
                    warnings = detect_parallel_fifths_octaves(v_curr, v_next, VoiceLeadingStyle.STRICT_COUNTERPOINT)

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
            # ii is 2 semitones above tonic (Tritone substitution candidate)
            elif (curr_pc - key_pc) % 12 == 2:
                bii_root = key_spelling.transpose_diatonic(step_delta=1, semitone_delta=1)
                bii_sym = f"{bii_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=bii_sym,
                    relation_type="SUBSTITUTES_FOR",
                    explanation=f"Tritonussubstitution: {bii_sym} (bII7) ersetzt die Quintfall-Dominante V7 durch chromatischen Bassabstieg.",
                    framework="Tritone Substitution",
                    source_id="Levine (1995)"
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
            # I is tonic (Secondary dominant lift to vi)
            elif (curr_pc - key_pc) % 12 == 0:
                v_vi_root = key_spelling.transpose_diatonic(step_delta=2, semitone_delta=4)
                v_vi_sym = f"{v_vi_root.render(self.convention)[:-1]}7"
                recommendations.append(ChordRecommendation(
                    candidate_symbol=v_vi_sym,
                    relation_type="DOMINANT_OF",
                    explanation=f"Zwischendominante: {v_vi_sym} (V7/vi) bereitet leittönig die Tonikaparallele vi vor.",
                    framework="Zwischendominanten",
                    source_id="Kostka/Payne (2013)"
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
        cur_tick = 0
        for sym in self.chords:
            events.append({
                "start_tick": cur_tick,
                "duration_ticks": self.state.chord_duration_ticks,
                "payload": sym
            })
            cur_tick += self.state.chord_duration_ticks

        proj = Project(
            title=self.state.title,
            notation_convention=self.convention,
            time_settings={
                "ppq": self.state.ppq,
                "time_signature": {"numerator": 4, "denominator": 4},
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
        proj = load_project(file_path)
        chords: List[str] = []
        for trk in proj.tracks:
            if trk.get("track_type") == "CHORDS":
                for ev in trk.get("events", []):
                    payload = ev.get("payload")
                    if isinstance(payload, str):
                        chords.append(payload)
                break

        if not chords:
            chords = ["C", "G", "Am", "F"]

        bpm = proj.time_settings.get("tempo_bpm", 120.0)
        ppq = proj.time_settings.get("ppq", 480)
        dur = ppq * 4

        new_state = SessionState(
            title=proj.title,
            chords=chords,
            key_root="C",
            is_minor=False,
            convention=proj.notation_convention,
            bpm=bpm,
            ppq=ppq,
            chord_duration_ticks=dur
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
            smf_format=1
        )

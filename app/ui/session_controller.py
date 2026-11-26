"""
STEPS UI Presenter: Progression Session Controller.

Decouples UI views (Tkinter/Desktop) from pure music logic in src/steps/progression/session.py.
Follows AGENTS.md Rule 4 (Domain boundary separation).
"""

from __future__ import annotations

import logging
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from src.steps.midi.export_service import Adr017ExportPreview, Adr017NoteDuration, Adr017Voicing
from src.steps.progression.session import (
    ChordRecommendation,
    DegreeAnalysis,
    ProgressionSession,
    VoiceLeadingStyle,
)
from src.steps.progression.engine import ReviewedProgression

logger = logging.getLogger(__name__)


def reviewed_practice_session(
    reviewed: ReviewedProgression, semitones: int = 0, convention: Literal["INT", "DE"] = "INT",
) -> ProgressionSession:
    """Create a clean practice copy with the catalog's original harmonic spelling."""
    progression = reviewed.progression
    original = ProgressionSession(
        initial_chords=[symbol.strip() for symbol in progression.chords_str.split(" - ")],
        key_root=progression.default_key.removesuffix("m"),
        is_minor=progression.default_key.endswith("m"), convention="INT", title=progression.name,
    )
    if type(semitones) is not int or not -6 <= semitones <= 6:
        raise ValueError("Practice transposition must be between -6 and +6 semitones.")
    if semitones == 0 and convention == "INT":
        return original
    original.transpose(semitones)
    original.set_notation_convention(convention)
    return ProgressionSession(
        initial_chords=original.chords, key_root=original.key_root, is_minor=original.is_minor,
        convention=original.convention, title=original.state.title,
    )


@dataclass(frozen=True)
class VoiceLeadingStyleProfile:
    """Non-mutating summary of one style's progression analysis."""

    style: VoiceLeadingStyle
    transitions: Tuple[DegreeAnalysis, ...]
    total_movement: int
    midi_notes: Tuple[Tuple[int, ...], ...]


class ProgressionSessionController:
    """
    Observable controller mediating between desktop views and progression session.
    Headless-testable without graphical display server.
    """

    def __init__(self, session: Optional[ProgressionSession] = None):
        self._session = session or ProgressionSession()
        self._listeners: List[Callable[[], None]] = []
        self._revision = 0

    @property
    def session(self) -> ProgressionSession:
        return self._session

    @property
    def revision(self) -> int:
        """Version of the last project notification."""
        return self._revision

    def add_listener(self, callback: Callable[[], None]) -> None:
        """Subscribes view listener for state changes."""
        self._listeners.append(callback)

    def remove_listener(self, callback: Callable[[], None]) -> None:
        """Unsubscribes a view listener (no-op if it was not registered)."""
        if callback in self._listeners:
            self._listeners.remove(callback)

    def _notify(self) -> None:
        """Notifies registered listeners."""
        self._revision += 1
        for cb in list(self._listeners):
            try:
                cb()
            except Exception:
                logger.exception("Progression session listener callback failed")

    def get_view_model(self) -> Dict[str, Any]:
        """Produces a structured view-model dictionary ready for GUI rendering."""
        analysis = self._session.analyze_progression()
        beginner_data = self._session.get_beginner_voicings().to_dict()
        return {
            "title": self._session.state.title,
            "chords": self._session.chords,
            "key_root": self._session.key_root,
            "is_minor": self._session.is_minor,
            "convention": self._session.convention,
            "bpm": self._session.bpm,
            "voice_leading_style": self._session.voice_leading_style.value,
            "is_dirty": self._session.is_dirty,
            "can_undo": self._session.can_undo,
            "can_redo": self._session.can_redo,
            "beginner_voicings": beginner_data,
            "analysis": [
                {
                    "index": a.index,
                    "symbol": a.symbol,
                    "roman": a.roman_numeral,
                    "distance_to_next": a.semitone_distance_to_next,
                    "warnings": list(a.voice_leading_warnings)
                }
                for a in analysis
            ]
        }

    def harmonic_degree_at(self, index: int) -> str:
        return self._session.harmonic_degree_at(index)

    def analyze_voice_leading_style(
        self,
        style: Union[str, VoiceLeadingStyle],
    ) -> VoiceLeadingStyleProfile:
        """Analyze a style without changing the project's selected style."""
        resolved = (
            style
            if isinstance(style, VoiceLeadingStyle)
            else VoiceLeadingStyle(str(style).upper())
        )
        transitions, voicings = self._session.analyze_progression_with_voicings(
            style=resolved,
            voicing_style=resolved,
        )
        total_movement = sum(
            item.semitone_distance_to_next or 0 for item in transitions
        )
        return VoiceLeadingStyleProfile(
            style=resolved,
            transitions=tuple(transitions),
            total_movement=total_movement,
            midi_notes=tuple(tuple(voicing.midi_notes) for voicing in voicings),
        )

    def get_state_summary(self) -> Dict[str, Any]:
        """Summary dictionary for status bars, logs and headless runners."""
        return {
            "title": self._session.state.title,
            "chords": list(self._session.chords),
            "key": f"{self._session.key_root} {'m' if self._session.is_minor else ''}".strip(),
            "key_root": self._session.key_root,
            "is_minor": self._session.is_minor,
            "bpm": self._session.bpm,
            "time_signature": self._session.time_signature,
            "voice_leading_style": self._session.voice_leading_style.value,
            "can_undo": self._session.can_undo,
            "can_redo": self._session.can_redo,
        }

    def get_beginner_voicings(self, starting_inversion: Optional[str] = None) -> Dict[str, Any]:
        """Provides beginner keyboard voicings and pedagogical guidance for UI rendering (OA-0024)."""
        return self._session.get_beginner_voicings(starting_inversion).to_dict()

    def set_chord(self, index: int, symbol: str) -> None:
        self._session.set_chord(index, symbol)
        self._notify()

    def add_chord(self, symbol: str) -> None:
        self._session.add_chord(symbol)
        self._notify()

    def duplicate_chord_event(self, index: int) -> int:
        new_index = self._session.duplicate_chord_event(index)
        self._notify()
        return new_index

    def split_chord_event(self, index: int) -> int:
        new_index = self._session.split_chord_event(index)
        self._notify()
        return new_index

    def remove_chord(self, index: int) -> None:
        self._session.remove_chord(index)
        self._notify()

    def move_chord(self, index: int, direction: Literal[-1, 1]) -> None:
        self._session.move_chord(index, direction)
        self._notify()

    def set_context(
        self,
        key_root: str,
        is_minor: bool,
        bpm: float,
        time_signature: Optional[Tuple[int, int]] = None,
        title: Optional[str] = None,
    ) -> None:
        self._session.set_context(key_root, is_minor, bpm, time_signature, title)
        self._notify()

    def set_chord_event_timing(self, index: int, start_tick: int, duration_ticks: int) -> None:
        self._session.set_chord_event_timing(index, start_tick, duration_ticks)
        self._notify()

    def transpose(self, semitones: int) -> None:
        self._session.transpose(semitones)
        self._notify()

    def set_voice_leading_style(self, style: Union[str, VoiceLeadingStyle]) -> None:
        """Sets the voice leading evaluation style (e.g. CONTEMPORARY_POP vs STRICT_CLASSICAL)."""
        self._session.set_voice_leading_style(style)
        self._notify()

    def set_notation_convention(self, convention: Literal["INT", "DE"]) -> bool:
        """Explicitly converts and notifies views when musical notation convention changes."""
        changed = self._session.set_notation_convention(convention)
        if changed:
            self._notify()
        return changed

    def undo(self) -> None:
        self._session.undo()
        self._notify()

    def redo(self) -> None:
        self._session.redo()
        self._notify()

    def save(self, file_path: Path | str) -> Path:
        out = self._session.save_to_file(file_path)
        self._notify()
        return out

    def load(self, file_path: Path | str) -> None:
        self._session.load_from_file(file_path)
        self._notify()

    def new_project(self) -> None:
        self._session.reset_to_defaults()
        self._notify()

    def new_reviewed_project(
        self, reviewed: ReviewedProgression, semitones: int = 0, convention: Literal["INT", "DE"] = "INT",
    ) -> None:
        """Replaces the active session with an independent copy of a published example."""
        self._session = reviewed_practice_session(reviewed, semitones, convention)
        self._notify()

    def midi_voicing_failures(self) -> dict[Adr017Voicing, str]:
        return self._session.midi_voicing_failures()

    def midi_export_preview(
        self, voicing_type: Adr017Voicing, note_duration_mode: Adr017NoteDuration,
    ) -> Adr017ExportPreview:
        return self._session.midi_export_preview(voicing_type, note_duration_mode)

    def midi_overlap_summary(
        self, voicing_type: Adr017Voicing, note_duration_mode: Adr017NoteDuration,
    ) -> tuple[int, int | None]:
        return self._session.midi_overlap_summary(voicing_type, note_duration_mode)

    def export_midi(
        self,
        file_path: Path | str,
        *,
        voicing_type: Literal["CLOSE", "DROP2", "ROOTLESS"] = "CLOSE",
        note_duration_mode: Literal["FIXED_GAP", "PERCENT_95"] = "FIXED_GAP",
        smf_format: Literal[0, 1] = 1,
    ) -> Path:
        return self._session.export_midi_file(
            file_path,
            voicing_type=voicing_type,
            note_duration_mode=note_duration_mode,
            smf_format=smf_format,
        )

    def explore_next(self, index: int) -> List[ChordRecommendation]:
        return self._session.explore_next_chords(index)

    def apply_next_recommendation(
        self,
        index: int,
        candidate_symbol: str,
        *,
        selected: ChordRecommendation | None = None,
        expected_revision: int | None = None,
    ) -> ChordRecommendation:
        """Validates and inserts one recommendation after the selected chord."""
        if not isinstance(candidate_symbol, str) or not candidate_symbol.strip():
            raise ValueError("A valid recommendation symbol is required.")
        if expected_revision is not None and expected_revision != self.revision:
            raise ValueError("The progression has changed since the recommendation was generated.")
        recommendations = self._session.explore_next_chords(index)
        candidate = next(
            (
                recommendation
                for recommendation in recommendations
                if recommendation.candidate_symbol == candidate_symbol
                and (selected is None or selected == recommendation)
            ),
            None,
        )
        if candidate is None:
            raise ValueError("The selected chord is not a valid recommendation for this context.")
        if not (0 <= index < len(self._session.chords)):
            raise IndexError(f"Index {index} out of range")
        self._session.add_chord(candidate.candidate_symbol, position=index + 1)
        self._notify()
        return candidate

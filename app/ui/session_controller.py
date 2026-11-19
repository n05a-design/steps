"""
STEPS UI Presenter: Progression Session Controller.

Decouples UI views (Tkinter/Desktop) from pure music logic in src/steps/progression/session.py.
Follows AGENTS.md Rule 4 (Domain boundary separation).
"""

from __future__ import annotations

from pathlib import Path
from typing import Any, Callable, Dict, List, Literal, Optional, Tuple, Union

from src.steps.progression.session import (
    ChordRecommendation,
    DegreeAnalysis,
    ProgressionSession,
    VoiceLeadingStyle,
)


class ProgressionSessionController:
    """
    Observable controller mediating between desktop views and progression session.
    Headless-testable without graphical display server.
    """

    def __init__(self, session: Optional[ProgressionSession] = None):
        self._session = session or ProgressionSession()
        self._listeners: List[Callable[[], None]] = []

    @property
    def session(self) -> ProgressionSession:
        return self._session

    def add_listener(self, callback: Callable[[], None]) -> None:
        """Subscribes view listener for state changes."""
        self._listeners.append(callback)

    def _notify(self) -> None:
        """Notifies registered listeners."""
        for cb in self._listeners:
            try:
                cb()
            except Exception:
                pass

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

    def export_midi(self, file_path: Path | str) -> Path:
        return self._session.export_midi_file(file_path)

    def explore_next(self, index: int) -> List[ChordRecommendation]:
        return self._session.explore_next_chords(index)

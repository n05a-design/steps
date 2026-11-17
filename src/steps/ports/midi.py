"""
STEPS Architecture Ports: MIDI Export Port.

Adheres to:
- ADR-007 (Audio/MIDI Architecture)
- Prompt 07, Prompt 11
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional, Protocol

from ..storage.project_io import Project
from ..theory.chord import Voicing


class MidiExportPort(Protocol):
    """Protocol for rendering domain voicings and projects to Standard MIDI Files."""

    def export_project_to_smf(
        self,
        project: Project,
        output_path: Path | str,
        smf_format: int = 1
    ) -> Path:
        """Renders an entire multi-track STEPS project to SMF Format 0 or 1 file."""
        ...

    def export_voicings_to_smf(
        self,
        voicings: List[Voicing],
        output_path: Path | str,
        bpm: float = 120.0,
        ppq: int = 480,
        chord_duration_ticks: int = 1920,
        smf_format: int = 1
    ) -> Path:
        """Renders a sequence of voicings to SMF Format 0 or 1 file."""
        ...

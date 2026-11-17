"""
STEPS MIDI Core: Export Service.

Translates high-level music structures (STEPS Project, Voicings, Progressions)
into Standard MIDI Files (SMF) Format 0 and Format 1.
"""

from __future__ import annotations

from pathlib import Path
from typing import List, Optional

from ..storage.project_io import Project
from ..theory.chord import Voicing, parse_chord
from .smf import MidiFile, MidiTrack


class MidiExportService:
    """Service for exporting STEPS projects and progressions to Standard MIDI Files."""

    @staticmethod
    def export_project_to_smf(
        project: Project,
        output_path: Path | str,
        smf_format: int = 1
    ) -> Path:
        """
        Exports a STEPS Project into a Standard MIDI File.
        
        Format 1 creates a dedicated Conductor track (Track 0) for tempo and meter,
        followed by individual tracks for Chords, Melody, Drums, etc.
        """
        ppq = project.time_settings.get("ppq", 480)
        midi_file = MidiFile(smf_format=smf_format, division=ppq)

        # 1. Conductor Track (Tempo & Meter)
        if smf_format == 1:
            conductor = midi_file.add_track(MidiTrack(name=f"{project.title} - Conductor"))
            # Time Signature
            ts = project.time_settings.get("time_signature", {"numerator": 4, "denominator": 4})
            conductor.add_time_signature(0, ts.get("numerator", 4), ts.get("denominator", 4))
            # Tempo Points
            tempo_points = project.time_settings.get("tempo_points", [])
            if not tempo_points:
                bpm = project.time_settings.get("tempo_bpm", 120.0)
                conductor.add_tempo(0, bpm)
            else:
                for tp in tempo_points:
                    conductor.add_tempo(tp.get("start_tick", 0), tp.get("bpm", 120.0))

        # 2. Content Tracks
        for trk_data in project.tracks:
            trk_name = trk_data.get("name", "Track")
            channel = trk_data.get("channel", 0)
            t_type = trk_data.get("track_type", "CHORDS")

            if smf_format == 1:
                midi_track = midi_file.add_track(MidiTrack(name=trk_name))
            else:
                # Format 0 uses single track
                midi_track = midi_file.tracks[0] if midi_file.tracks else midi_file.add_track(MidiTrack(name=project.title))

            events = trk_data.get("events", [])
            for ev in events:
                start_tick = ev.get("start_tick", 0)
                dur_ticks = ev.get("duration_ticks", ppq)
                payload = ev.get("payload")

                if payload is None:
                    continue

                # If payload is a string chord symbol (e.g. 'Cmaj7')
                if isinstance(payload, str):
                    try:
                        chord = parse_chord(payload, convention=project.notation_convention)
                        voicing = chord.to_voicing(bass_octave=3, voicing_type="CLOSE")
                        for note in voicing.midi_notes:
                            midi_track.add_note(start_tick, dur_ticks, note, velocity=75, channel=channel)
                    except Exception:
                        pass
                # If payload is a list of MIDI integers
                elif isinstance(payload, (list, tuple)):
                    for note in payload:
                        if isinstance(note, int) and 0 <= note <= 127:
                            midi_track.add_note(start_tick, dur_ticks, note, velocity=80, channel=channel)
                # If payload is an integer (single note)
                elif isinstance(payload, int) and 0 <= payload <= 127:
                    midi_track.add_note(start_tick, dur_ticks, payload, velocity=80, channel=channel)

        return midi_file.save(output_path)

    @staticmethod
    def export_voicings_to_smf(
        voicings: List[Voicing],
        output_path: Path | str,
        bpm: float = 120.0,
        ppq: int = 480,
        chord_duration_ticks: int = 1920,
        smf_format: int = 1
    ) -> Path:
        """
        Exports a sequence of Voicings into an SMF file.
        Each chord is placed at consecutive bars (chord_duration_ticks, default 1 bar of 4/4).
        """
        midi_file = MidiFile(smf_format=smf_format, division=ppq)

        # Track 0 / Conductor
        if smf_format == 1:
            conductor = midi_file.add_track(MidiTrack(name="Conductor"))
            conductor.add_time_signature(0, 4, 4)
            conductor.add_tempo(0, bpm)
            chords_track = midi_file.add_track(MidiTrack(name="Chords"))
        else:
            chords_track = midi_file.add_track(MidiTrack(name="Chords"))
            chords_track.add_time_signature(0, 4, 4)
            chords_track.add_tempo(0, bpm)

        current_tick = 0
        for v in voicings:
            for note in v.midi_notes:
                chords_track.add_note(
                    start_tick=current_tick,
                    duration_ticks=chord_duration_ticks,
                    pitch=note,
                    velocity=75,
                    channel=0
                )
            current_tick += chord_duration_ticks

        return midi_file.save(output_path)

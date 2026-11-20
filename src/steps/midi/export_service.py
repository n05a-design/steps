"""
STEPS MIDI Core: Export Service.

Translates high-level music structures (STEPS Project, Voicings, Progressions)
into Standard MIDI Files (SMF) Format 0 and Format 1.
"""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import List, Literal, Optional, Tuple

from ..storage.project_io import Project
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from .smf import MidiFile, MidiTrack


def _adr017_close_notes(chord: ChordDefinition) -> list[int]:
    intervals = chord.default_voiced_intervals
    if len(intervals) < 4:
        selected = list(intervals)
        root = next((interval for interval in intervals if interval % 12 == 0), 0)
        while len(selected) < 4:
            root += 12
            selected.append(root)
    elif len(intervals) > 4:
        root = next((interval for interval in intervals if interval % 12 == 0), None)
        third = next(
            (interval for interval in intervals if interval % 12 in (3, 4, 5)),
            None,
        )
        seventh = next(
            (interval for interval in intervals if interval % 12 in (9, 10, 11)),
            None,
        )
        extension = max((interval for interval in intervals if interval > 12), default=None)
        if root is None or third is None or seventh is None or extension is None:
            raise ValueError(
                f"ADR-017 cannot select four chord voices for {chord.symbol}."
            )
        selected = [root, third, seventh, extension]
    else:
        selected = list(intervals)

    root_note = 48 + int(chord.root.pitch_class)
    notes = []
    for interval in selected:
        note = root_note + interval
        while note > 72:
            note -= 12
        while note < 48:
            note += 12
        notes.append(note)
    notes.sort()
    if len(set(notes)) != 4:
        raise ValueError(f"ADR-017 requires four distinct chord voices for {chord.symbol}.")
    return notes


def _adr017_alternative_notes(
    chord: ChordDefinition,
    voicing_type: Literal["DROP2", "ROOTLESS"],
) -> list[int]:
    chord_without_slash_bass = replace(chord, bass=None)
    notes = chord_without_slash_bass.to_voicing(
        bass_octave=3,
        voicing_type=voicing_type,
    ).midi_notes
    if len(notes) != 4:
        raise ValueError(
            f"ADR-017 {voicing_type} requires four chord voices for {chord.symbol}."
        )

    normalized = []
    for note in notes:
        while note < 48:
            note += 12
        while note > 72:
            note -= 12
        normalized.append(note)
    normalized.sort()
    if len(set(normalized)) != 4:
        raise ValueError(
            f"ADR-017 {voicing_type} requires four distinct chord voices for {chord.symbol}."
        )
    return normalized


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
                    if t_type == "CHORDS":
                        chord = parse_chord(payload, convention=project.notation_convention)
                        voicing = chord.to_voicing(bass_octave=3, voicing_type="CLOSE")
                        for note in voicing.midi_notes:
                            midi_track.add_note(start_tick, dur_ticks, note, velocity=75, channel=channel)
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
        smf_format: int = 1,
        time_signature: tuple[int, int] = (4, 4),
        event_timings: list[tuple[int, int]] | None = None,
    ) -> Path:
        """
        Exports a sequence of Voicings into an SMF file.
        Optional event timing supplies absolute tick positions and durations; otherwise
        chords use consecutive tick offsets and the supplied fixed duration.
        """
        if event_timings is not None and len(event_timings) != len(voicings):
            raise ValueError("Event timing count must match the voicing count.")
        if event_timings is None:
            event_timings = [
                (index * chord_duration_ticks, chord_duration_ticks)
                for index in range(len(voicings))
            ]
        if any(
            not isinstance(timing, tuple)
            or len(timing) != 2
            or not isinstance(timing[0], int)
            or isinstance(timing[0], bool)
            or timing[0] < 0
            or not isinstance(timing[1], int)
            or isinstance(timing[1], bool)
            or timing[1] <= 0
            for timing in event_timings
        ):
            raise ValueError("Event timings require non-negative starts and positive durations.")

        midi_file = MidiFile(smf_format=smf_format, division=ppq)

        # Track 0 / Conductor
        if smf_format == 1:
            conductor = midi_file.add_track(MidiTrack(name="Conductor"))
            conductor.add_time_signature(0, time_signature[0], time_signature[1])
            conductor.add_tempo(0, bpm)
            chords_track = midi_file.add_track(MidiTrack(name="Chords"))
        else:
            chords_track = midi_file.add_track(MidiTrack(name="Chords"))
            chords_track.add_time_signature(0, time_signature[0], time_signature[1])
            chords_track.add_tempo(0, bpm)

        for v, (start_tick, duration_ticks) in zip(voicings, event_timings):
            for note in v.midi_notes:
                chords_track.add_note(
                    start_tick=start_tick,
                    duration_ticks=duration_ticks,
                    pitch=note,
                    velocity=75,
                    channel=0
                )

        return midi_file.save(output_path)

    @staticmethod
    def export_progression_adr017(
        chords: List[str | ChordDefinition],
        output_path: Path | str,
        bpm: float = 120.0,
        ppq: int = 480,
        chord_duration_quarters: float = 4.0,
        time_signature: tuple[int, int] = (4, 4),
        key_accidentals: Optional[int] = None,
        is_minor_key: bool = False,
        separate_bass_track: bool = True,
        lead_gap_ticks: int = 10,
        chords_velocity: int = 90,
        bass_velocity: int = 100,
        convention: str = "INT",
        event_timings: Optional[List[Tuple[int, int]]] = None,
        voicing_type: Literal["CLOSE", "DROP2", "ROOTLESS"] = "CLOSE",
        note_duration_mode: Literal["FIXED_GAP", "PERCENT_95"] = "FIXED_GAP",
        smf_format: Literal[0, 1] = 1,
    ) -> Path:
        """
        Exports a chord progression following the ADR-017 MIDI specification.
        Default output is SMF Type 1 with Conductor, Chords, and Bass tracks;
        SMF Type 0 combines them into one STEPS track.
        Chords use four voices in MIDI 48..72; bass uses MIDI 36..47.
        Effective note length defaults to duration_ticks minus lead_gap_ticks.
        No program change messages (0xC0) are added.
        Event timing overrides sequential positions and fixed chord durations.
        Optional output modes support DROP2/ROOTLESS and 95%-length notes.
        """
        if voicing_type not in ("CLOSE", "DROP2", "ROOTLESS"):
            raise ValueError(f"Unsupported ADR-017 voicing type: {voicing_type!r}.")
        if note_duration_mode not in ("FIXED_GAP", "PERCENT_95"):
            raise ValueError(f"Unsupported ADR-017 note duration mode: {note_duration_mode!r}.")

        midi_file = MidiFile(smf_format=smf_format, division=ppq)

        if smf_format == 0:
            conductor = midi_file.add_track(MidiTrack(name="STEPS"))
            chords_track = conductor
            bass_track = conductor if separate_bass_track else None
        else:
            conductor = midi_file.add_track(MidiTrack(name="Conductor"))
            chords_track = midi_file.add_track(MidiTrack(name="Chords"))
            bass_track = (
                midi_file.add_track(MidiTrack(name="Bass"))
                if separate_bass_track
                else None
            )

        conductor.add_time_signature(0, time_signature[0], time_signature[1])
        conductor.add_tempo(0, bpm)
        if key_accidentals is not None and -7 <= key_accidentals <= 7:
            conductor.add_key_signature(0, accidentals=key_accidentals, is_minor=is_minor_key)

        chord_dur_ticks = int(round(chord_duration_quarters * ppq))
        if event_timings is None:
            event_timings = [
                (index * chord_dur_ticks, chord_dur_ticks)
                for index in range(len(chords))
            ]
        if len(event_timings) != len(chords):
            raise ValueError("Event timing count must match the chord count.")
        if (
            not isinstance(lead_gap_ticks, int)
            or isinstance(lead_gap_ticks, bool)
            or lead_gap_ticks < 0
        ):
            raise ValueError("Lead gap must be a non-negative whole number of ticks.")
        if any(
            not isinstance(timing, tuple)
            or len(timing) != 2
            or not isinstance(timing[0], int)
            or isinstance(timing[0], bool)
            or timing[0] < 0
            or not isinstance(timing[1], int)
            or isinstance(timing[1], bool)
            or timing[1] <= 0
            for timing in event_timings
        ):
            raise ValueError("Event timings require non-negative starts and positive durations.")

        def note_duration(duration_ticks: int) -> int:
            if note_duration_mode == "PERCENT_95":
                return max(1, int(round(duration_ticks * 0.95)))
            return max(1, duration_ticks - lead_gap_ticks)

        for item, (start_tick, duration_ticks) in zip(chords, event_timings):
            if isinstance(item, str):
                chord_def = parse_chord(item, convention=convention)
            else:
                chord_def = item

            if voicing_type == "CLOSE":
                chord_notes = _adr017_close_notes(chord_def)
            else:
                chord_notes = _adr017_alternative_notes(chord_def, voicing_type)

            for note in chord_notes:
                chords_track.add_note(
                    start_tick=start_tick,
                    duration_ticks=note_duration(duration_ticks),
                    pitch=note,
                    velocity=chords_velocity,
                    channel=0
                )

            # Bass: Grundton bzw. notierter Bass in MIDI 36..47 (C2..B2)
            if bass_track is not None:
                bass_spelling = chord_def.bass if chord_def.bass else chord_def.root
                bass_pitch = int(bass_spelling.pitch_class) + 36
                bass_track.add_note(
                    start_tick=start_tick,
                    duration_ticks=note_duration(duration_ticks),
                    pitch=bass_pitch,
                    velocity=bass_velocity,
                    channel=1
                )

        return midi_file.save(output_path)






"""
STEPS MIDI Core: Export Service.

Translates high-level music structures (STEPS Project, Voicings, Progressions)
into Standard MIDI Files (SMF) Format 0 and Format 1.
"""

from __future__ import annotations

from collections.abc import Iterator
from dataclasses import dataclass, replace
from pathlib import Path
from typing import List, Literal, Optional, Sequence, Tuple

from ..storage.project_io import Project
from ..theory.chord import ChordDefinition, Voicing, parse_chord
from ..theory.exceptions import MusicTheoryError
from ..theory.seventh import make_drop2_voicing
from .smf import MidiFile, MidiTrack


Adr017Voicing = Literal["CLOSE", "DROP2", "ROOTLESS"]
Adr017NoteDuration = Literal["FIXED_GAP", "PERCENT_95"]
ADR017_VOICINGS: tuple[Adr017Voicing, ...] = ("CLOSE", "DROP2", "ROOTLESS")


@dataclass(frozen=True)
class Adr017ExportPreview:
    """Descriptive statistics of the actual note events prepared for export."""

    first_tick: int | None
    end_tick: int | None
    chord_notes: int
    bass_notes: int
    chord_range: tuple[int, int] | None
    bass_range: tuple[int, int] | None
    overlaps: int
    first_overlap_tick: int | None


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
    if notes[-1] - notes[0] > 12:
        # Rebuild the selected pitch classes within the octave above the root.
        notes = sorted({root_note + interval % 12 for interval in selected})
        if len(intervals) < 4:
            notes.append(root_note + 12)
    if len(set(notes)) != 4:
        raise ValueError(f"ADR-017 requires four distinct chord voices for {chord.symbol}.")
    return notes


def _adr017_drop2_notes(chord: ChordDefinition) -> list[int]:
    close = _adr017_close_notes(chord)
    if len({note % 12 for note in close}) != 4:
        raise ValueError(f"ADR-017 DROP2 requires four different chord tones for {chord.symbol}.")
    notes = make_drop2_voicing(close)
    if notes[0] < 48:
        notes = [note + 12 for note in notes]
    if notes[-1] > 72:
        raise ValueError(f"ADR-017 DROP2 does not fit MIDI 48–72 for {chord.symbol}.")
    return notes


def _adr017_rootless_notes(chord: ChordDefinition) -> list[int]:
    chord_without_slash_bass = replace(chord, bass=None)
    notes = chord_without_slash_bass.to_voicing(
        bass_octave=3,
        voicing_type="ROOTLESS",
    ).midi_notes
    if len(notes) != 4:
        raise ValueError(
            f"ADR-017 ROOTLESS requires four chord voices for {chord.symbol}."
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
            f"ADR-017 ROOTLESS requires four distinct chord voices for {chord.symbol}."
        )
    return normalized


def _adr017_notes(chord: ChordDefinition, mode: Adr017Voicing) -> list[int]:
    if mode == "CLOSE":
        return _adr017_close_notes(chord)
    if mode == "DROP2":
        return _adr017_drop2_notes(chord)
    return _adr017_rootless_notes(chord)


def _adr017_note_events(
    chords: Sequence[str | ChordDefinition],
    event_timings: Sequence[tuple[int, int]],
    *,
    convention: str,
    voicing_type: Adr017Voicing,
    note_duration_mode: Adr017NoteDuration,
    lead_gap_ticks: int = 10,
    include_bass: bool = True,
) -> Iterator[tuple[int, int, int, int]]:
    """Yield (start, length, channel, pitch) in export order."""
    if voicing_type not in ADR017_VOICINGS:
        raise ValueError(f"Unsupported ADR-017 voicing type: {voicing_type!r}.")
    if note_duration_mode not in ("FIXED_GAP", "PERCENT_95"):
        raise ValueError(f"Unsupported ADR-017 note duration mode: {note_duration_mode!r}.")
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

    for item, (start, duration) in zip(chords, event_timings, strict=True):
        chord = parse_chord(item, convention=convention) if isinstance(item, str) else item
        length = (
            max(1, int(round(duration * 0.95)))
            if note_duration_mode == "PERCENT_95"
            else max(1, duration - lead_gap_ticks)
        )
        for pitch in _adr017_notes(chord, voicing_type):
            yield start, length, 0, pitch
        if include_bass:
            bass = chord.bass if chord.bass else chord.root
            yield start, length, 1, int(bass.pitch_class) + 36


class MidiExportService:
    """Service for exporting STEPS projects and progressions to Standard MIDI Files."""

    @staticmethod
    def adr017_voicing_failures(
        chords: Sequence[str], convention: str = "INT",
    ) -> dict[Adr017Voicing, str]:
        """Return the first blocking chord for each incompatible export voicing."""
        failures: dict[Adr017Voicing, str] = {}
        for symbol in dict.fromkeys(chords):
            try:
                chord = parse_chord(symbol, convention=convention)
            except MusicTheoryError:
                return {mode: failures.get(mode, symbol) for mode in ADR017_VOICINGS}

            for mode in ADR017_VOICINGS:
                if mode not in failures:
                    try:
                        _adr017_notes(chord, mode)
                    except (MusicTheoryError, ValueError):
                        failures[mode] = symbol
            if len(failures) == len(ADR017_VOICINGS):
                break
        return failures

    @staticmethod
    def adr017_overlap_summary(
        chords: Sequence[str | ChordDefinition],
        event_timings: Sequence[tuple[int, int]],
        *,
        convention: str = "INT",
        voicing_type: Adr017Voicing = "CLOSE",
        note_duration_mode: Adr017NoteDuration = "FIXED_GAP",
    ) -> tuple[int, int | None]:
        """Count overlapping attacks by channel and pitch and return their earliest tick."""
        preview = MidiExportService.adr017_export_preview(
            chords, event_timings, convention=convention, voicing_type=voicing_type,
            note_duration_mode=note_duration_mode,
        )
        return preview.overlaps, preview.first_overlap_tick

    @staticmethod
    def adr017_export_preview(
        chords: Sequence[str | ChordDefinition],
        event_timings: Sequence[tuple[int, int]],
        *,
        convention: str = "INT",
        voicing_type: Adr017Voicing = "CLOSE",
        note_duration_mode: Adr017NoteDuration = "FIXED_GAP",
    ) -> Adr017ExportPreview:
        """Summarize the same note stream used by the standard project exporter."""
        events = _adr017_note_events(
            chords, event_timings, convention=convention, voicing_type=voicing_type,
            note_duration_mode=note_duration_mode,
        )
        sounding_until: dict[tuple[int, int], int] = {}
        count = 0
        first_tick = None
        chord_pitches: list[int] = []
        bass_pitches: list[int] = []
        first_event = end_tick = None
        for start, duration, channel, pitch in sorted(events, key=lambda event: event[0]):
            if first_event is None:
                first_event = start
            end_tick = max(end_tick or 0, start + duration)
            (bass_pitches if channel == 1 else chord_pitches).append(pitch)
            key = channel, pitch
            end = sounding_until.get(key, 0)
            if start < end:
                count += 1
                if first_tick is None:
                    first_tick = start
            sounding_until[key] = max(end, start + duration)
        return Adr017ExportPreview(
            first_event, end_tick, len(chord_pitches), len(bass_pitches),
            (min(chord_pitches), max(chord_pitches)) if chord_pitches else None,
            (min(bass_pitches), max(bass_pitches)) if bass_pitches else None,
            count, first_tick,
        )

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

        # Format 0 stores metadata and content on the same track. Format 1
        # keeps the tempo map and time signature on a dedicated conductor.
        track_name = f"{project.title} - Conductor" if smf_format == 1 else project.title
        conductor = midi_file.add_track(MidiTrack(name=track_name))
        time_signature = project.time_settings.get("time_signature", {"numerator": 4, "denominator": 4})
        conductor.add_time_signature(0, time_signature.get("numerator", 4), time_signature.get("denominator", 4))
        tempo_points = project.time_settings.get("tempo_points", [])
        if not tempo_points:
            conductor.add_tempo(0, project.time_settings.get("tempo_bpm", 120.0))
        else:
            for point in tempo_points:
                conductor.add_tempo(point.get("start_tick", 0), point.get("bpm", 120.0))

        # 2. Content Tracks
        for trk_data in project.tracks:
            trk_name = trk_data.get("name", "Track")
            channel = trk_data.get("channel", 0)
            t_type = trk_data.get("track_type", "CHORDS")

            if smf_format == 1:
                midi_track = midi_file.add_track(MidiTrack(name=trk_name))
            else:
                # Format 0 uses single track
                midi_track = conductor

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
                    if any(type(note) is not int or not 0 <= note <= 127 for note in payload):
                        raise ValueError(
                            f"Invalid MIDI note payload for track {trk_name!r}: {payload!r}."
                        )
                    for note in payload:
                        midi_track.add_note(start_tick, dur_ticks, note, velocity=80, channel=channel)
                # If payload is an integer (single note)
                elif isinstance(payload, int):
                    if type(payload) is not int or not 0 <= payload <= 127:
                        raise ValueError(
                            f"Invalid MIDI note payload for track {trk_name!r}: {payload!r}."
                        )
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
        for start, duration, channel, pitch in _adr017_note_events(
            chords, event_timings, convention=convention, voicing_type=voicing_type,
            note_duration_mode=note_duration_mode, lead_gap_ticks=lead_gap_ticks,
            include_bass=bass_track is not None,
        ):
            track = bass_track if channel == 1 and bass_track is not None else chords_track
            track.add_note(
                start_tick=start, duration_ticks=duration, pitch=pitch,
                velocity=bass_velocity if channel == 1 else chords_velocity, channel=channel,
            )

        return midi_file.save(output_path)






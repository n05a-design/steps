"""
STEPS MIDI Core & Export Service Verification Test Suite (Phase P1.4 / Prompt 11).

Validates:
- Variable-Length Quantity (VLQ) encoding and decoding accuracy
- SMF Format 0 and Format 1 header (MThd) and track (MTrk) structures
- Compatibility with independent envelope reader (scripts.audit_midi_files.envelope)
- Note On / Note Off event generation with exact duration ticks
- Tempo and Time Signature meta events
- Project export to multi-track SMF
- Voicings sequence export to SMF
- Full binary round-trip: MidiFile.to_bytes() -> MidiFile.from_bytes()
"""

import errno
import os
import shutil
import stat
import tempfile
import unittest

from pathlib import Path
from unittest.mock import patch

from scripts.audit_midi_files import envelope
from src.steps.midi import (
    MidiExportService,
    MidiFile,
    MidiTrack,
    SMFParser,
    decode_vlq,
    encode_vlq,
)
from src.steps.models.swing import SwingEngine, SwingSubdivision
from src.steps.storage.project_io import Project
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import ChordConstructionError, MusicTheoryError


class TestVLQEncodingDecoding(unittest.TestCase):
    def test_smf_four_byte_limit_and_invalid_offsets(self):
        self.assertEqual(encode_vlq(0x0FFFFFFF), bytes.fromhex("ff ff ff 7f"))
        self.assertEqual(decode_vlq(bytes.fromhex("00 ff ff ff 7f 00"), 1), (0x0FFFFFFF, 4))
        for invalid in (bytes.fromhex("81 80 80 80 00"), bytes.fromhex("80 80 80 80"), b"\x80"):
            with self.subTest(data=invalid), self.assertRaises(ValueError):
                decode_vlq(invalid)
        for invalid in (0x10000000, True):
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                encode_vlq(invalid)
        for invalid in (-1, True, 1.5):
            with self.subTest(offset=invalid), self.assertRaises(ValueError):
                decode_vlq(b"\x00", invalid)

    def test_vlq_roundtrips(self):
        cases = [0, 1, 64, 127, 128, 255, 480, 1920, 8192, 16383, 16384, 2097151]
        for val in cases:
            with self.subTest(value=val):
                encoded = encode_vlq(val)
                decoded, consumed = decode_vlq(encoded)
                self.assertEqual(decoded, val)
                self.assertEqual(consumed, len(encoded))

    def test_vlq_specific_byte_values(self):
        self.assertEqual(encode_vlq(0), b"\x00")
        self.assertEqual(encode_vlq(127), b"\x7F")
        self.assertEqual(encode_vlq(128), b"\x81\x00")
        self.assertEqual(encode_vlq(8192), b"\xC0\x00")

    def test_vlq_negative_fails(self):
        with self.assertRaises(ValueError):
            encode_vlq(-1)


class TestSMFGenerationAndEnvelope(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_midi_test_")
        self.midi_path = Path(self.temp_dir) / "test_out.mid"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_failed_midi_write_or_publish_preserves_existing_target(self):
        midi = MidiFile()
        midi.add_track().add_note(0, 480, 60)
        self.midi_path.write_bytes(b"previous MIDI data")

        for operation in ("fsync", "replace"):
            with self.subTest(operation=operation):
                with patch(
                    f"src.steps.midi.smf.os.{operation}",
                    side_effect=OSError(errno.ENOSPC, "injected failure"),
                ), self.assertRaises(OSError):
                    midi.save(self.midi_path)

                self.assertEqual(self.midi_path.read_bytes(), b"previous MIDI data")
                self.assertEqual(list(self.midi_path.parent.iterdir()), [self.midi_path])

        self.assertEqual(midi.save(self.midi_path), self.midi_path)
        self.assertEqual(self.midi_path.read_bytes(), midi.to_bytes())
        self.assertEqual(len(SMFParser.parse(self.midi_path.read_bytes()).all_notes), 1)

    @unittest.skipIf(os.name == "nt", "POSIX mode and symlink behavior")
    def test_midi_export_follows_existing_symlink_and_keeps_target_mode(self):
        midi = MidiFile()
        self.midi_path.write_bytes(b"previous MIDI data")
        self.midi_path.chmod(0o640)
        link = self.midi_path.with_name("alias.mid")
        link.symlink_to(self.midi_path.name)

        self.assertEqual(midi.save(link), link)

        self.assertTrue(link.is_symlink())
        self.assertEqual(link.read_bytes(), midi.to_bytes())
        self.assertEqual(stat.S_IMODE(self.midi_path.stat().st_mode), 0o640)

    def test_adr017_overlap_summary_uses_effective_note_lengths(self):
        summary = MidiExportService.adr017_overlap_summary
        self.assertEqual(summary(["C", "C"], [(0, 20), (10, 20)]), (0, None))
        self.assertEqual(summary(["C", "C"], [(0, 20), (12, 20)]), (0, None))
        self.assertEqual(
            summary(["C", "C"], [(0, 20), (12, 20)], note_duration_mode="PERCENT_95"),
            (5, 12),
        )
        self.assertEqual(summary(["C", "Db"], [(0, 20), (0, 20)]), (0, None))
        self.assertEqual(summary(["C", "C/E"], [(0, 20), (0, 20)]), (4, 0))

    def test_adr017_overlap_summary_retains_longest_note_across_unsorted_events(self):
        self.assertEqual(
            MidiExportService.adr017_overlap_summary(
                ["C", "C", "C", "C"], [(40, 20), (30, 20), (30, 60), (45, 20)],
            ),
            (15, 30),
        )

    def test_adr017_preview_matches_written_note_spans_counts_and_pitch_ranges(self):
        chords = ["C13/E", "C13"]
        timings = [(120, 180), (0, 100)]
        for voicing in ("CLOSE", "DROP2", "ROOTLESS"):
            for duration in ("FIXED_GAP", "PERCENT_95"):
                preview = MidiExportService.adr017_export_preview(
                    chords, timings, voicing_type=voicing, note_duration_mode=duration,
                )
                for smf_format in (0, 1):
                    with self.subTest(voicing=voicing, duration=duration, smf_format=smf_format):
                        path = MidiExportService.export_progression_adr017(
                            chords, self.midi_path, event_timings=timings, voicing_type=voicing,
                            note_duration_mode=duration, smf_format=smf_format,
                        )
                        parsed = SMFParser.parse(path.read_bytes())
                        notes = parsed.all_notes
                        chord_pitches = [note.pitch for note in notes if note.channel == 0]
                        bass_pitches = [note.pitch for note in notes if note.channel == 1]
                        self.assertEqual((preview.chord_notes, preview.bass_notes), (8, 2))
                        self.assertEqual((len(chord_pitches), len(bass_pitches)), (8, 2))
                        self.assertEqual(preview.chord_range, (min(chord_pitches), max(chord_pitches)))
                        self.assertEqual(preview.bass_range, (36, 40))
                        self.assertEqual(preview.bass_range, (min(bass_pitches), max(bass_pitches)))
                        self.assertEqual(preview.first_tick, min(note.start_tick for note in notes))
                        self.assertEqual(preview.end_tick, max(note.end_tick for note in notes))
                        self.assertEqual(preview.overlaps, 0)

    def test_adr017_preflight_matches_actual_exports_in_german_notation(self):
        chords = ["Hmaj7", "Fis"]
        self.assertEqual(
            MidiExportService.adr017_voicing_failures(chords, "DE"),
            {"DROP2": "Fis", "ROOTLESS": "Hmaj7"},
        )
        self.assertEqual(
            MidiExportService.adr017_voicing_failures(["Hmaj7", "?"], "DE"),
            {"CLOSE": "?", "DROP2": "?", "ROOTLESS": "Hmaj7"},
        )
        for mode in ("CLOSE", "DROP2", "ROOTLESS"):
            with self.subTest(mode=mode):
                target = self.midi_path.with_name(f"preflight-{mode}.mid")
                if mode == "CLOSE":
                    MidiExportService.export_progression_adr017(
                        chords, target, convention="DE", voicing_type=mode,
                    )
                    self.assertTrue(target.is_file())
                else:
                    with self.assertRaises((MusicTheoryError, ValueError)):
                        MidiExportService.export_progression_adr017(
                            chords, target, convention="DE", voicing_type=mode,
                        )
                    self.assertFalse(target.exists())

    def test_minimal_format0_smf(self):
        midi = MidiFile(smf_format=0, division=480)
        track = midi.add_track(MidiTrack(name="Solo"))
        track.add_tempo(0, 120.0)
        track.add_note(0, 480, 60, velocity=80)

        data = midi.to_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 0)
        self.assertEqual(env["tracks"], 1)
        self.assertEqual(env["division"], 480)

    def test_format1_multi_track_smf(self):
        midi = MidiFile(smf_format=1, division=480)
        conductor = midi.add_track(MidiTrack(name="Conductor"))
        conductor.add_time_signature(0, 4, 4)
        conductor.add_tempo(0, 130.0)

        chords = midi.add_track(MidiTrack(name="Chords"))
        chords.add_note(0, 960, 60, velocity=75)
        chords.add_note(0, 960, 64, velocity=75)
        chords.add_note(0, 960, 67, velocity=75)

        data = midi.to_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)
        self.assertEqual(env["division"], 480)

    def test_binary_roundtrip(self):
        midi = MidiFile(smf_format=1, division=480)
        t1 = midi.add_track(MidiTrack(name="Track A"))
        t1.add_tempo(0, 120.0)
        t1.add_note(0, 480, 60, 80)
        t1.add_note(480, 480, 62, 80)

        data = midi.to_bytes()
        parsed = MidiFile.from_bytes(data)

        self.assertEqual(parsed.format, 1)
        self.assertEqual(parsed.division, 480)
        self.assertEqual(len(parsed.tracks), 1)

    def test_project_export_to_smf(self):
        project = Project(
            title="Autumn Leaves Study",
            time_settings={
                "ppq": 480,
                "time_signature": {"numerator": 4, "denominator": 4},
                "tempo_bpm": 120.0,
                "tempo_points": [
                    {"start_tick": 0, "bpm": 120.0},
                    {"start_tick": 1920, "bpm": 140.0}
                ]
            },
            tracks=[
                {
                    "track_id": "trk_1",
                    "track_type": "CHORDS",
                    "name": "Chords Track",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 1920, "payload": "Cm7"},
                        {"start_tick": 1920, "duration_ticks": 1920, "payload": "F7"},
                        {"start_tick": 3840, "duration_ticks": 1920, "payload": "Bbmaj7"},
                    ]
                }
            ]
        )

        out = MidiExportService.export_project_to_smf(project, self.midi_path, smf_format=1)
        self.assertTrue(out.exists())
        self.assertGreater(out.stat().st_size, 50)

        data = out.read_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)  # Conductor + Chords track
        self.assertEqual(env["division"], 480)

    def test_project_export_preserves_swing_melody_drums_and_timing_in_both_formats(self):
        swing = SwingEngine(ppq=480, subdivision=SwingSubdivision.EIGHTH, swing_ratio=2)

        def note(tick, pitch, duration):
            return {"start_tick": tick, "duration_ticks": duration, "payload": pitch}

        project = Project(
            title="Synthetic arrangement",
            time_settings={
                "ppq": 480, "time_signature": {"numerator": 3, "denominator": 4},
                "tempo_points": [{"start_tick": 0, "bpm": 120}, {"start_tick": 960, "bpm": 100}],
            },
            tracks=[
                {"name": "Harmony", "track_type": "CHORDS", "channel": 0,
                 "events": [note(0, "C", 960)]},
                {"name": "Melody", "track_type": "MELODY", "channel": 2,
                 "events": [note(0, 72, 120), note(swing.apply_to_tick(240), 74, 120),
                            note(480, 76, 120)]},
                {"name": "Drums", "track_type": "DRUMS", "channel": 9,
                 "events": [note(0, 36, 60), note(swing.apply_to_tick(240), 42, 60),
                            note(480, 38, 60)]},
            ],
        )
        for smf_format in (0, 1):
            with self.subTest(smf_format=smf_format):
                path = MidiExportService.export_project_to_smf(project, self.midi_path, smf_format)
                result = SMFParser.parse(path.read_bytes())
                self.assertEqual((result.format, result.division, result.num_tracks),
                                 (smf_format, 480, 1 if smf_format == 0 else 4))
                self.assertEqual([(n.start_tick, n.pitch, n.duration_ticks)
                                  for n in result.all_notes if n.channel == 2],
                                 [(0, 72, 120), (320, 74, 120), (480, 76, 120)])
                self.assertEqual([(n.start_tick, n.pitch, n.duration_ticks)
                                  for n in result.all_notes if n.channel == 9],
                                 [(0, 36, 60), (320, 42, 60), (480, 38, 60)])
                self.assertEqual({n.pitch % 12 for n in result.all_notes if n.channel == 0}, {0, 4, 7})
                self.assertEqual(result.time_signatures, [(0, 3, 4)])
                self.assertEqual(result.tempos, [(0, 120.0), (960, 100.0)])

    def test_invalid_chord_payload_fails_project_export(self):
        project = Project(
            tracks=[
                {
                    "track_id": "trk_chords",
                    "track_type": "CHORDS",
                    "name": "Chords Track",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 480, "payload": "not-a-chord"}
                    ],
                }
            ]
        )

        with self.assertRaises(ChordConstructionError):
            MidiExportService.export_project_to_smf(project, self.midi_path)

        self.assertFalse(self.midi_path.exists())

    def test_annotation_text_is_not_parsed_as_a_chord(self):
        project = Project(
            tracks=[
                {
                    "track_id": "trk_annotations",
                    "track_type": "ANNOTATIONS",
                    "name": "Annotations",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 480, "payload": "Section A"}
                    ],
                }
            ]
        )

        with patch("src.steps.midi.export_service.parse_chord") as parse_chord_mock:
            MidiExportService.export_project_to_smf(project, self.midi_path)

        parse_chord_mock.assert_not_called()
        self.assertTrue(self.midi_path.exists())

    def test_invalid_midi_note_payloads_fail_project_export(self):
        for payload in ([60, 128], [60, True], 128, True):
            with self.subTest(payload=payload):
                self.midi_path.unlink(missing_ok=True)
                project = Project(
                    tracks=[
                        {
                            "track_id": "trk_notes",
                            "track_type": "MELODY",
                            "name": "Melody Track",
                            "channel": 0,
                            "events": [
                                {"start_tick": 0, "duration_ticks": 480, "payload": payload}
                            ],
                        }
                    ]
                )

                with self.assertRaises(ValueError):
                    MidiExportService.export_project_to_smf(project, self.midi_path)

                self.assertFalse(self.midi_path.exists())

    def test_integer_note_payloads_export_every_valid_note(self):
        project = Project(
            tracks=[
                {
                    "track_id": "trk_notes",
                    "track_type": "MELODY",
                    "name": "Melody Track",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 480, "payload": [60, 64]},
                        {"start_tick": 480, "duration_ticks": 480, "payload": 67},
                    ],
                }
            ]
        )

        MidiExportService.export_project_to_smf(project, self.midi_path)
        parsed = MidiFile.from_bytes(self.midi_path.read_bytes())
        note_ons = [
            event
            for event in parsed.tracks[1].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x90 and event.msg_bytes[2] > 0
        ]

        self.assertEqual([event.msg_bytes[1] for event in note_ons], [60, 64, 67])

    def test_voicings_export_to_smf(self):
        c1 = parse_chord("Dm7", "INT").to_voicing(3, "CLOSE")
        c2 = parse_chord("G7", "INT").to_voicing(3, "CLOSE")
        c3 = parse_chord("Cmaj7", "INT").to_voicing(3, "CLOSE")

        out = MidiExportService.export_voicings_to_smf(
            [c1, c2, c3],
            self.midi_path,
            bpm=110.0,
            ppq=480,
            chord_duration_ticks=1920,
            time_signature=(6, 8),
            event_timings=[(120, 480), (2000, 240), (3000, 960)],
            smf_format=1
        )
        self.assertTrue(out.exists())
        data = out.read_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)
        parsed = MidiFile.from_bytes(data)
        time_signature_events = [
            event.msg_bytes
            for event in parsed.tracks[0].raw_events
            if event.msg_bytes.startswith(b"\xff\x58")
        ]
        self.assertEqual(time_signature_events, [b"\xff\x58\x04\x06\x03\x18\x08"])
        chord_events = parsed.tracks[1].raw_events
        note_ons = [event for event in chord_events if event.msg_bytes[0] & 0xF0 == 0x90]
        note_offs = [event for event in chord_events if event.msg_bytes[0] & 0xF0 == 0x80]
        self.assertEqual({event.abs_tick for event in note_ons}, {120, 2000, 3000})
        self.assertEqual(
            {event.abs_tick for event in note_offs},
            {600, 2240, 3960},
        )

    def test_export_progression_adr017(self):
        out = MidiExportService.export_progression_adr017(
            chords=["Dm7", "G7", "Cmaj7"],
            output_path=self.midi_path,
            bpm=120.0,
            ppq=480,
            chord_duration_quarters=4.0,
            time_signature=(4, 4),
            key_accidentals=0,
            is_minor_key=False,
            separate_bass_track=True,
            lead_gap_ticks=10,
            chords_velocity=90,
            bass_velocity=100,
            convention="INT"
        )
        self.assertTrue(out.exists())
        data = out.read_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 3)  # Conductor, Chords, Bass
        self.assertEqual(env["division"], 480)

        # Parse back
        parsed = MidiFile.from_bytes(data)
        self.assertEqual(len(parsed.tracks), 3)
        self.assertEqual(parsed.tracks[0].name, "Conductor")
        self.assertEqual(parsed.tracks[1].name, "Chords")
        self.assertEqual(parsed.tracks[2].name, "Bass")

        # Verify key signature meta event in conductor track
        has_key_sig = any(e.msg_bytes.startswith(b"\xFF\x59") for e in parsed.tracks[0].raw_events)
        self.assertTrue(has_key_sig)

        # Verify chords track note-on events have velocity 90 and note-offs are at eff_dur
        chord_note_ons = [e for e in parsed.tracks[1].raw_events if (e.msg_bytes[0] & 0xF0) == 0x90]
        chord_note_offs = [e for e in parsed.tracks[1].raw_events if (e.msg_bytes[0] & 0xF0) == 0x80]
        self.assertGreater(len(chord_note_ons), 0)
        self.assertEqual(len(chord_note_ons), len(chord_note_offs))
        for on, off in zip(chord_note_ons, chord_note_offs):
            self.assertEqual(on.msg_bytes[2], 90)  # velocity
            self.assertEqual(on.msg_bytes[0] & 0x0F, 0)  # channel 0 (MIDI 1)
            self.assertTrue(48 <= on.msg_bytes[1] <= 72)  # pitch
            self.assertEqual(off.abs_tick - on.abs_tick, 1910)  # 1920 - 10 ticks

        # Verify bass track notes have velocity 100 and channel 1 (MIDI 2), pitch in octave 2 (36..47)
        bass_note_ons = [e for e in parsed.tracks[2].raw_events if (e.msg_bytes[0] & 0xF0) == 0x90]
        bass_note_offs = [e for e in parsed.tracks[2].raw_events if (e.msg_bytes[0] & 0xF0) == 0x80]
        self.assertEqual(len(bass_note_ons), 3)
        self.assertEqual(len(bass_note_offs), 3)
        for on, off in zip(bass_note_ons, bass_note_offs):
            self.assertEqual(on.msg_bytes[2], 100)  # velocity
            self.assertEqual(on.msg_bytes[0] & 0x0F, 1)  # channel 1 (MIDI 2)
            self.assertTrue(36 <= on.msg_bytes[1] <= 47)  # bass octave 2
            self.assertEqual(off.abs_tick - on.abs_tick, 1910)

    def test_export_progression_adr017_uses_four_chord_voices_in_range(self):
        out = MidiExportService.export_progression_adr017(
            chords=["C", "C13", "C/E", "B13"],
            output_path=self.midi_path,
        )
        parsed = MidiFile.from_bytes(out.read_bytes())

        chord_notes = {}
        for event in parsed.tracks[1].raw_events:
            message = event.msg_bytes
            if message[0] & 0xF0 == 0x90 and message[2] > 0:
                chord_notes.setdefault(event.abs_tick, []).append(message[1])

        self.assertEqual(
            {tick: sorted(notes) for tick, notes in chord_notes.items()},
            {
                0: [48, 52, 55, 60],
                1920: [48, 52, 57, 58],
                3840: [48, 52, 55, 60],
                5760: [59, 63, 68, 69],
            },
        )
        self.assertTrue(
            all(48 <= note <= 72 for notes in chord_notes.values() for note in notes)
        )
        bass_notes = [
            (event.abs_tick, event.msg_bytes[1])
            for event in parsed.tracks[2].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x90 and event.msg_bytes[2] > 0
        ]
        self.assertEqual(
            bass_notes,
            [(0, 36), (1920, 36), (3840, 40), (5760, 47)],
        )

    def test_export_progression_adr017_optional_voicings(self):
        expected = {
            "CLOSE": [48, 52, 57, 58],
            "DROP2": [57, 60, 64, 70],
            "ROOTLESS": [62, 64, 69, 70],
        }
        for voicing_type, expected_notes in expected.items():
            with self.subTest(voicing_type=voicing_type):
                out = MidiExportService.export_progression_adr017(
                    chords=["C13"],
                    output_path=self.midi_path,
                    voicing_type=voicing_type,
                )
                parsed = MidiFile.from_bytes(out.read_bytes())
                actual_notes = sorted(
                    event.msg_bytes[1]
                    for event in parsed.tracks[1].raw_events
                    if event.msg_bytes[0] & 0xF0 == 0x90 and event.msg_bytes[2] > 0
                )
                self.assertEqual(actual_notes, expected_notes)
                self.assertTrue(all(48 <= note <= 72 for note in actual_notes))

    def test_adr017_drop2_moves_the_whole_shape_and_preserves_separate_bass(self):
        out = MidiExportService.export_progression_adr017(
            chords=["Cmaj7/E", "G7"], output_path=self.midi_path, voicing_type="DROP2", smf_format=0,
        )
        notes = SMFParser.parse(out.read_bytes()).tracks[0].notes
        for tick, chord_pitches, bass in ((0, [55, 60, 64, 71], 40), (1920, [50, 55, 59, 65], 43)):
            self.assertEqual(sorted(note.pitch for note in notes if note.channel == 0 and note.start_tick == tick),
                             chord_pitches)
            self.assertEqual([note.pitch for note in notes if note.channel == 1 and note.start_tick == tick],
                             [bass])

    def test_adr017_rejects_drop2_when_closed_shape_cannot_fit(self):
        chords = ["Cmaj7", "Emaj7"]
        self.assertEqual(MidiExportService.adr017_voicing_failures(chords)["DROP2"], "Emaj7")
        self.midi_path.write_bytes(b"existing file")
        with self.assertRaisesRegex(ValueError, "does not fit"):
            MidiExportService.export_progression_adr017(
                chords, self.midi_path, voicing_type="DROP2",
            )
        self.assertEqual(self.midi_path.read_bytes(), b"existing file")
        with self.assertRaisesRegex(ValueError, "does not fit"):
            MidiExportService.adr017_overlap_summary(
                chords, [(0, 1920), (1910, 1920)], voicing_type="DROP2",
            )

    def test_export_progression_adr017_percentage_length_and_single_track(self):
        out = MidiExportService.export_progression_adr017(
            chords=["C7"],
            output_path=self.midi_path,
            key_accidentals=0,
            note_duration_mode="PERCENT_95",
            smf_format=0,
        )
        self.assertEqual(envelope(out.read_bytes())["tracks"], 1)
        parsed = MidiFile.from_bytes(out.read_bytes())
        self.assertEqual(parsed.format, 0)
        self.assertEqual(len(parsed.tracks), 1)
        self.assertEqual(parsed.tracks[0].name, "STEPS")

        note_ons = [
            event for event in parsed.tracks[0].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x90 and event.msg_bytes[2] > 0
        ]
        note_offs = [
            event for event in parsed.tracks[0].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x80
        ]
        self.assertEqual(len(note_ons), 5)
        self.assertEqual(len(note_offs), 5)
        self.assertEqual(
            {off.abs_tick - on.abs_tick for on, off in zip(note_ons, note_offs)},
            {1824},
        )
        self.assertEqual({event.msg_bytes[0] & 0x0F for event in note_ons}, {0, 1})
        self.assertTrue(
            any(event.msg_bytes.startswith(b"\xff\x59") for event in parsed.tracks[0].raw_events)
        )
        independent = SMFParser.parse(out.read_bytes())
        self.assertEqual(independent.format, 0)
        self.assertEqual(independent.num_tracks, 1)
        self.assertEqual(len(independent.tracks[0].notes), 5)
        self.assertEqual(
            {note.duration_ticks for note in independent.tracks[0].notes},
            {1824},
        )
        self.assertEqual(
            {note.channel for note in independent.tracks[0].notes},
            {0, 1},
        )

    def test_export_progression_adr017_rejects_non_four_note_alternatives(self):
        with self.assertRaisesRegex(ValueError, "ROOTLESS requires four chord voices"):
            MidiExportService.export_progression_adr017(
                chords=["C"],
                output_path=self.midi_path,
                voicing_type="ROOTLESS",
            )


if __name__ == "__main__":
    unittest.main()

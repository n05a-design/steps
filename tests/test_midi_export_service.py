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

import shutil
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
from src.steps.storage.project_io import Project
from src.steps.theory.chord import parse_chord
from src.steps.theory.exceptions import ChordConstructionError


class TestVLQEncodingDecoding(unittest.TestCase):
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
                1920: [48, 52, 58, 69],
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
            "CLOSE": [48, 52, 58, 69],
            "DROP2": [48, 52, 57, 58],
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

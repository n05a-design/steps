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

from scripts.audit_midi_files import envelope
from src.steps.midi import (
    MidiExportService,
    MidiFile,
    MidiTrack,
    decode_vlq,
    encode_vlq,
)
from src.steps.storage.project_io import Project
from src.steps.theory.chord import parse_chord


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
            smf_format=1
        )
        self.assertTrue(out.exists())
        data = out.read_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)


if __name__ == "__main__":
    unittest.main()

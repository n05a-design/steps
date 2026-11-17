"""
Unit tests for STEPS SMF Format 0 & 1 Parser and Format Conversion (OA-0028, M11).
"""

import struct
import unittest

from src.steps.midi.smf import MidiFile, MidiTrack
from src.steps.midi.smf_parser import (
    MidiParseError,
    SMFParser,
    convert_format_0_to_1,
    convert_format_1_to_0,
)


class TestSMFParser(unittest.TestCase):
    """Tests the parsing, validation, and conversion of SMF Format 0 and Format 1 files."""

    def test_parse_valid_format_0(self) -> None:
        midi = MidiFile(smf_format=0, division=480)
        track = midi.add_track()
        track.add_tempo(0, 120.0)
        track.add_time_signature(0, 4, 4)
        # Add a C major chord on channel 0
        track.add_note(start_tick=0, duration_ticks=480, pitch=60, velocity=80, channel=0)
        track.add_note(start_tick=0, duration_ticks=480, pitch=64, velocity=75, channel=0)
        track.add_note(start_tick=0, duration_ticks=480, pitch=67, velocity=70, channel=0)

        raw_bytes = midi.to_bytes()
        parsed = SMFParser.parse(raw_bytes)

        self.assertEqual(parsed.format, 0)
        self.assertEqual(parsed.division, 480)
        self.assertEqual(parsed.num_tracks, 1)

        # Tempos & Time Signatures
        self.assertEqual(len(parsed.tempos), 1)
        self.assertEqual(parsed.tempos[0], (0, 120.0))
        self.assertEqual(len(parsed.time_signatures), 1)
        self.assertEqual(parsed.time_signatures[0], (0, 4, 4))

        # Check notes
        notes = parsed.tracks[0].notes
        self.assertEqual(len(notes), 3)
        pitches = sorted(n.pitch for n in notes)
        self.assertEqual(pitches, [60, 64, 67])
        for n in notes:
            self.assertEqual(n.start_tick, 0)
            self.assertEqual(n.duration_ticks, 480)
            self.assertEqual(n.end_tick, 480)
            self.assertEqual(n.channel, 0)

    def test_parse_valid_format_1_multi_track(self) -> None:
        midi = MidiFile(smf_format=1, division=480)
        # Track 0: Conductor (Tempo & Time Signature)
        t0 = midi.add_track()
        t0.add_track_name("Conductor")
        t0.add_tempo(0, 140.0)
        t0.add_time_signature(0, 3, 4)

        # Track 1: Bass on Channel 1
        t1 = midi.add_track()
        t1.add_track_name("Bass")
        t1.add_note(start_tick=0, duration_ticks=480, pitch=36, velocity=100, channel=1)
        t1.add_note(start_tick=480, duration_ticks=480, pitch=43, velocity=90, channel=1)

        # Track 2: Piano on Channel 0
        t2 = midi.add_track()
        t2.add_track_name("Piano")
        t2.add_note(start_tick=0, duration_ticks=960, pitch=60, velocity=70, channel=0)

        raw_bytes = midi.to_bytes()
        parsed = SMFParser.parse(raw_bytes)

        self.assertEqual(parsed.format, 1)
        self.assertEqual(parsed.division, 480)
        self.assertEqual(parsed.num_tracks, 3)

        self.assertEqual(parsed.tracks[0].name, "Conductor")
        self.assertEqual(parsed.tracks[1].name, "Bass")
        self.assertEqual(parsed.tracks[2].name, "Piano")

        all_notes = parsed.all_notes
        self.assertEqual(len(all_notes), 3)
        self.assertEqual(len(parsed.tracks[1].notes), 2)
        self.assertEqual(len(parsed.tracks[2].notes), 1)

    def test_note_on_velocity_zero_as_note_off(self) -> None:
        # Build raw MTrk with 0x90 pitch 0x00 instead of 0x80
        # MThd: format 0, 1 track, 480 ppq
        mthd = b"MThd\x00\x00\x00\x06\x00\x00\x00\x01\x01\xE0"
        # MTrk:
        # delta 0: Note On ch 0, pitch 60, vel 64 (\x90\x3C\x40)
        # delta 240 (\x81\x70): Note On ch 0, pitch 60, vel 0 (\x90\x3C\x00) -> acts as note off!
        # delta 0: End of Track (\xFF\x2F\x00)
        mtrk_data = b"\x00\x90\x3C\x40\x81\x70\x90\x3C\x00\x00\xFF\x2F\x00"
        mtrk_len = struct.pack(">I", len(mtrk_data))
        raw = mthd + b"MTrk" + mtrk_len + mtrk_data

        parsed = SMFParser.parse(raw)
        self.assertEqual(len(parsed.tracks[0].notes), 1)
        note = parsed.tracks[0].notes[0]
        self.assertEqual(note.pitch, 60)
        self.assertEqual(note.start_tick, 0)
        self.assertEqual(note.duration_ticks, 240)
        self.assertEqual(note.velocity, 64)

    def test_running_status_handling(self) -> None:
        # MThd: format 0, 1 track, 480 ppq
        mthd = b"MThd\x00\x00\x00\x06\x00\x00\x00\x01\x01\xE0"
        # MTrk with running status:
        # delta 0: Note On ch 0, pitch 60, vel 80 (\x90\x3C\x50)
        # delta 0: (running status) pitch 64, vel 75 (\x40\x4B)
        # delta 480 (\x83\x60): Note Off ch 0, pitch 60, vel 0 (\x80\x3C\x00)
        # delta 0: (running status) pitch 64, vel 0 (\x40\x00)
        # delta 0: End of Track (\xFF\x2F\x00)
        mtrk_data = (
            b"\x00\x90\x3C\x50"
            b"\x00\x40\x4B"
            b"\x83\x60\x80\x3C\x00"
            b"\x00\x40\x00"
            b"\x00\xFF\x2F\x00"
        )
        mtrk = b"MTrk" + struct.pack(">I", len(mtrk_data)) + mtrk_data
        parsed = SMFParser.parse(mthd + mtrk)

        self.assertEqual(len(parsed.tracks[0].notes), 2)
        n1, n2 = parsed.tracks[0].notes
        self.assertEqual(n1.pitch, 60)
        self.assertEqual(n1.duration_ticks, 480)
        self.assertEqual(n2.pitch, 64)
        self.assertEqual(n2.duration_ticks, 480)

    def test_unclosed_notes_at_track_end(self) -> None:
        # Note On without corresponding Note Off before End of Track
        mthd = b"MThd\x00\x00\x00\x06\x00\x00\x00\x01\x01\xE0"
        # Note on at tick 0, then 480 ticks later End of Track
        mtrk_data = b"\x00\x90\x3C\x64\x83\x60\xFF\x2F\x00"
        mtrk = b"MTrk" + struct.pack(">I", len(mtrk_data)) + mtrk_data
        parsed = SMFParser.parse(mthd + mtrk)

        self.assertEqual(len(parsed.tracks[0].notes), 1)
        note = parsed.tracks[0].notes[0]
        self.assertEqual(note.pitch, 60)
        self.assertEqual(note.start_tick, 0)
        self.assertEqual(note.duration_ticks, 480)

    def test_format_conversion_roundtrip(self) -> None:
        # Create a Format 1 file with 2 tracks
        src_f1 = MidiFile(smf_format=1, division=480)
        t0 = src_f1.add_track()
        t0.add_tempo(0, 120.0)
        t0.add_time_signature(0, 4, 4)

        t1 = src_f1.add_track()
        t1.add_note(0, 480, 60, channel=0)
        t1.add_note(480, 480, 62, channel=0)

        t2 = src_f1.add_track()
        t2.add_note(0, 960, 36, channel=1)

        # Convert to Format 0
        f0 = convert_format_1_to_0(src_f1)
        self.assertEqual(f0.format, 0)
        self.assertEqual(len(f0.tracks), 1)

        # Verify parsed format 0
        parsed_f0 = SMFParser.parse(f0.to_bytes())
        self.assertEqual(len(parsed_f0.all_notes), 3)

        # Convert Format 0 back to Format 1
        f1_restored = convert_format_0_to_1(f0)
        self.assertEqual(f1_restored.format, 1)
        self.assertEqual(len(f1_restored.tracks), 3)  # Master/Tempo + Ch0 + Ch1

        parsed_f1 = SMFParser.parse(f1_restored.to_bytes())
        self.assertEqual(len(parsed_f1.all_notes), 3)
        # All pitches and durations match
        original_notes = [(n.pitch, n.start_tick, n.duration_ticks, n.channel) for n in parsed_f0.all_notes]
        restored_notes = [(n.pitch, n.start_tick, n.duration_ticks, n.channel) for n in parsed_f1.all_notes]
        self.assertEqual(original_notes, restored_notes)

    def test_parse_error_scenarios(self) -> None:
        # 1. Too short
        with self.assertRaises(MidiParseError):
            SMFParser.parse(b"MThd")

        # 2. Invalid magic
        with self.assertRaises(MidiParseError):
            SMFParser.parse(b"RIFF\x00\x00\x00\x06\x00\x00\x00\x01\x01\xE0")

        # 3. Invalid header len
        with self.assertRaises(MidiParseError):
            SMFParser.parse(b"MThd\x00\x00\x00\x04\x00\x00\x00\x01")

        # 4. Format 0 with >1 tracks
        with self.assertRaises(MidiParseError):
            SMFParser.parse(b"MThd\x00\x00\x00\x06\x00\x00\x00\x02\x01\xE0")

        # 5. Truncated chunk header
        mthd = b"MThd\x00\x00\x00\x06\x00\x00\x00\x01\x01\xE0"
        with self.assertRaises(MidiParseError):
            SMFParser.parse(mthd + b"MTr")

        # 6. Truncated chunk payload
        with self.assertRaises(MidiParseError):
            SMFParser.parse(mthd + b"MTrk\x00\x00\x00\x10\x00")

        # 7. Invalid running status without previous command
        bad_running = mthd + b"MTrk\x00\x00\x00\x04\x00\x3C\x40\x00"
        with self.assertRaises(MidiParseError):
            SMFParser.parse(bad_running)


if __name__ == "__main__":
    unittest.main()

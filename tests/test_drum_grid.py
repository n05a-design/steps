"""
Unit & Integration Tests for STEPS Drum Grid, Rhythm Patterns & MIDI GM Mapping.

Adheres to:
- Prompt 10 (Drum Progressions, Groove und Beatmaking)
- ADR-002, ADR-007
- General MIDI (GM 1.0) Channel 10 percussion standard
- 480 PPQ integer tick resolution
- Non-destructive swing and microtiming transformations
"""

import unittest
from pathlib import Path

from scripts.audit_midi_files import envelope
from src.steps.midi.smf import MidiFile
from src.steps.models.drums import (
    DrumPad,
    DrumPattern,
    DrumStep,
    DrumTrack,
    GeneralMidiPercussion,
)
from src.steps.models.timeline import TimeSignature, validate_midi_note_on_off_pairing


class DrumGridTests(unittest.TestCase):

    def setUp(self):
        self.kick_pad = DrumPad("kick", "Acoustic Kick", GeneralMidiPercussion.BASS_DRUM_1)
        self.snare_pad = DrumPad("snare", "Acoustic Snare", GeneralMidiPercussion.ACOUSTIC_SNARE)
        self.hihat_pad = DrumPad("hihat", "Closed Hi-Hat", GeneralMidiPercussion.CLOSED_HI_HAT)

    def test_drum_pad_validation(self):
        """Validates GM pitch range [0..127]."""
        pad = DrumPad("kick", "Kick", 36)
        self.assertEqual(pad.midi_pitch, 36)
        with self.assertRaises(ValueError):
            DrumPad("invalid", "Invalid", 128)
        with self.assertRaises(ValueError):
            DrumPad("invalid", "Invalid", -1)

    def test_drum_step_validation(self):
        """Validates step index, velocity, probability, and microtiming bounds."""
        step = DrumStep(step_index=0, active=True, velocity=100, probability=0.8, microtiming_offset=15)
        self.assertEqual(step.velocity, 100)
        self.assertEqual(step.probability, 0.8)

        with self.assertRaises(ValueError):
            DrumStep(step_index=-1)
        with self.assertRaises(ValueError):
            DrumStep(step_index=0, velocity=128)
        with self.assertRaises(ValueError):
            DrumStep(step_index=0, probability=1.5)
        with self.assertRaises(ValueError):
            DrumStep(step_index=0, microtiming_offset=200)

    def test_drum_pattern_setup_and_track_manipulation(self):
        """Creates a standard 16-step 4/4 Pop/Rock straight groove (PAT-001 equivalent)."""
        pattern = DrumPattern(
            pattern_id="PAT-001",
            name="Pop / Rock Straight",
            meter=TimeSignature(4, 4),
            step_count=16,
            step_resolution_ticks=120  # 16th notes at 480 PPQ
        )

        kick_trk = pattern.add_track(self.kick_pad)
        snare_trk = pattern.add_track(self.snare_pad)
        hihat_trk = pattern.add_track(self.hihat_pad)

        # Kick on 1 and 3 (steps 0 and 8 in 16-step grid)
        kick_trk.set_step(0, active=True, velocity=105)
        kick_trk.set_step(8, active=True, velocity=100)

        # Snare on 2 and 4 (steps 4 and 12)
        snare_trk.set_step(4, active=True, velocity=100)
        snare_trk.set_step(12, active=True, velocity=100)

        # Hi-Hat on 8th notes (steps 0, 2, 4, 6, 8, 10, 12, 14)
        for s in range(0, 16, 2):
            hihat_trk.set_step(s, active=True, velocity=85)

        self.assertEqual(len(pattern.tracks), 3)
        self.assertEqual(pattern.get_track("kick"), kick_trk)
        self.assertIsNone(pattern.get_track("cowbell"))

        # Render to timeline events
        events = pattern.to_timeline_events(start_tick=0, ppq=480)
        # Expected hits: 2 kicks + 2 snares + 8 hi-hats = 12 hits
        self.assertEqual(len(events), 12)

        # Verify GM pitches on channel 9 (Channel 10)
        kick_evs = [e for e in events if e.payload["pitch"] == GeneralMidiPercussion.BASS_DRUM_1]
        snare_evs = [e for e in events if e.payload["pitch"] == GeneralMidiPercussion.ACOUSTIC_SNARE]
        hihat_evs = [e for e in events if e.payload["pitch"] == GeneralMidiPercussion.CLOSED_HI_HAT]

        self.assertEqual(len(kick_evs), 2)
        self.assertEqual(len(snare_evs), 2)
        self.assertEqual(len(hihat_evs), 8)

        # Kick 1 at tick 0, Kick 2 at tick 8 * 120 = 960 (Beat 3)
        self.assertEqual(kick_evs[0].start_tick, 0)
        self.assertEqual(kick_evs[1].start_tick, 960)

        # Snare 1 at tick 4 * 120 = 480 (Beat 2), Snare 2 at tick 12 * 120 = 1440 (Beat 4)
        self.assertEqual(snare_evs[0].start_tick, 480)
        self.assertEqual(snare_evs[1].start_tick, 1440)

    def test_swing_and_microtiming_rendering(self):
        """Verifies swing and microtiming transformations without altering original step definitions."""
        pattern = DrumPattern(
            pattern_id="PAT-SWING",
            name="Swing Groove",
            step_count=16,
            step_resolution_ticks=120,
            swing_amount=0.5  # Triplet swing
        )
        hihat_trk = pattern.add_track(self.hihat_pad)
        # Step 0 (on-beat), Step 2 (off-beat 8th note, tick 240)
        hihat_trk.set_step(0, active=True, velocity=80)
        hihat_trk.set_step(2, active=True, velocity=80, microtiming_offset=10)

        events = pattern.to_timeline_events(start_tick=0, ppq=480)
        self.assertEqual(len(events), 2)

        # Step 0 is on-beat: tick 0
        self.assertEqual(events[0].start_tick, 0)
        # Step 2 base tick is 240 (8th note). With swing (0.5 * 80 = 40 shift -> 280) + microtiming 10 = 290
        self.assertEqual(events[1].start_tick, 290)

        # Original pattern step definitions remain intact
        self.assertEqual(hihat_trk.steps[0].microtiming_offset, 0)
        self.assertEqual(hihat_trk.steps[2].microtiming_offset, 10)

    def test_drum_pattern_to_midi_track_and_smf_export(self):
        """Verifies direct export of DrumPattern to SMF Track and binary roundtrip."""
        pattern = DrumPattern(
            pattern_id="PAT-001",
            name="Rock Beat",
            step_count=16,
            step_resolution_ticks=120
        )
        kick_trk = pattern.add_track(self.kick_pad)
        snare_trk = pattern.add_track(self.snare_pad)

        kick_trk.set_step(0, active=True)
        snare_trk.set_step(4, active=True)

        midi_trk = pattern.to_midi_track(name="Drum Kit", channel=9, ppq=480)

        # Create MidiFile with Conductor + Drums track
        midi_file = MidiFile(smf_format=1, division=480)
        cond = midi_file.add_track()
        cond.add_time_signature(0, 4, 4)
        cond.add_tempo(0, 120.0)
        midi_file.add_track(midi_trk)

        data = midi_file.to_bytes()
        env = envelope(data)
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)
        self.assertEqual(env["division"], 480)

        # Re-parse file and verify note pairing (T14)
        parsed = MidiFile.from_bytes(data)
        drum_track_parsed = parsed.tracks[1]

        note_events = []
        for rev in drum_track_parsed.raw_events:
            mb = rev.msg_bytes
            if len(mb) >= 3 and (mb[0] & 0xF0) in (0x80, 0x90):
                status = mb[0] & 0xF0
                channel = mb[0] & 0x0F
                pitch = mb[1]
                vel = mb[2]
                ev_name = "note_off" if (status == 0x80 or vel == 0) else "note_on"
                note_events.append((ev_name, rev.abs_tick, channel, pitch))

        self.assertEqual(len(note_events), 4)  # 2 note-ons, 2 note-offs
        pairing_errors = validate_midi_note_on_off_pairing(note_events)
        self.assertEqual(pairing_errors, [])


if __name__ == "__main__":
    unittest.main()

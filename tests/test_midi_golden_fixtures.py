"""
STEPS 10 Deterministic Golden MIDI Fixtures & Verification Suite.

Adheres to:
- Prompt 11 (MIDI, Audiowiedergabe und Export/Import, Ergänzender Auditauftrag)
- REQ-026 (MIDI/Interchange prüfen)
- 10 canonical golden progressions:
  1. Classical Authentic Cadence (I - IV - V - I in C major)
  2. Jazz Major 2-5-1 (Dm7 - G7 - Cmaj7 in C major)
  3. Jazz Minor 2-5-1 (Dm7b5 - G7 - Cm7 in C minor)
  4. Pop 4-Chord Axis (C - G - Am - F in C major)
  5. Modal Dorian Vamp (Dm7 - G7)
  6. 12-Bar Blues in F (F7, Bb7, C7)
  7. Andalusian Cadence (Am - G - F - E7)
  8. Secondary Dominants Cycle (C - A7 - D7 - G7 - C)
  9. Multi-Tempo & Meter Transition (120 BPM 4/4 -> 90 BPM 3/4 -> 120 BPM 4/4)
  10. Chromatic Mediants (C - Ab - E - C)

Validates:
- SMF Format 0 & Format 1 export
- Envelope compliance (MThd, MTrk, PPQ 480) via scripts.audit_midi_files.envelope
- Binary roundtrip fidelity (MidiFile.to_bytes -> MidiFile.from_bytes)
- Golden Invariant T14 (1:1 NoteOn/NoteOff pairing, zero hung notes)
- Golden Invariant T15 (Multi-tempo map tick transitions)
"""

import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Tuple

from scripts.audit_midi_files import envelope
from src.steps.midi.export_service import MidiExportService
from src.steps.midi.smf import MidiFile, MidiTrack
from src.steps.models.timeline import validate_midi_note_on_off_pairing
from src.steps.storage.project_io import Project
from src.steps.theory.chord import Voicing, parse_chord

# The 10 Canonical Golden Definitions
GOLDEN_PROGRESSIONS: List[Dict[str, Any]] = [
    {
        "id": "GOLD_01_CLASSICAL_CADENCE",
        "name": "Classical Authentic Cadence",
        "tempo_bpm": 120.0,
        "meter": (4, 4),
        "chords": ["C", "F", "G", "C"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_02_JAZZ_MAJOR_251",
        "name": "Jazz Major 2-5-1",
        "tempo_bpm": 130.0,
        "meter": (4, 4),
        "chords": ["Dm7", "G7", "Cmaj7"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_03_JAZZ_MINOR_251",
        "name": "Jazz Minor 2-5-1",
        "tempo_bpm": 110.0,
        "meter": (4, 4),
        "chords": ["Dm7b5", "G7", "Cm7"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_04_POP_AXIS",
        "name": "Pop 4-Chord Axis",
        "tempo_bpm": 128.0,
        "meter": (4, 4),
        "chords": ["C", "G", "Am", "F"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_05_MODAL_DORIAN",
        "name": "Modal Dorian Vamp",
        "tempo_bpm": 105.0,
        "meter": (4, 4),
        "chords": ["Dm7", "G7", "Dm7", "G7"],
        "chord_duration_quarters": 2.0,
    },
    {
        "id": "GOLD_06_BLUES_12BAR",
        "name": "12-Bar Blues in F",
        "tempo_bpm": 115.0,
        "meter": (4, 4),
        "chords": ["F7", "Bb7", "F7", "F7", "Bb7", "Bb7", "F7", "F7", "C7", "Bb7", "F7", "C7"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_07_ANDALUSIAN_CADENCE",
        "name": "Andalusian Cadence",
        "tempo_bpm": 120.0,
        "meter": (4, 4),
        "chords": ["Am", "G", "F", "E7"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_08_SECONDARY_DOMINANTS",
        "name": "Secondary Dominants Cycle",
        "tempo_bpm": 135.0,
        "meter": (4, 4),
        "chords": ["C", "A7", "D7", "G7", "C"],
        "chord_duration_quarters": 4.0,
    },
    {
        "id": "GOLD_09_MULTI_TEMPO_METER",
        "name": "Multi-Tempo and Meter Progression",
        "tempo_points": [
            {"start_tick": 0, "bpm": 120.0},
            {"start_tick": 1920, "bpm": 90.0},
            {"start_tick": 3360, "bpm": 120.0},
        ],
        "meter": (4, 4),
        "events": [
            {"start_tick": 0, "duration_ticks": 1920, "payload": "Cmaj7"},       # 1 bar of 4/4 at 120 bpm
            {"start_tick": 1920, "duration_ticks": 1440, "payload": "Fmaj7"},    # 1 bar of 3/4 at 90 bpm
            {"start_tick": 3360, "duration_ticks": 1920, "payload": "Cmaj7"},    # 1 bar of 4/4 at 120 bpm
        ],
    },
    {
        "id": "GOLD_10_CHROMATIC_MEDIANTS",
        "name": "Chromatic Mediants",
        "tempo_bpm": 100.0,
        "meter": (4, 4),
        "chords": ["C", "Ab", "E", "C"],
        "chord_duration_quarters": 4.0,
    },
]


class TestMidiGoldenFixtures(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_golden_midi_")
        self.out_dir = Path(self.temp_dir)

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def _build_project_from_golden(self, gold_def: Dict[str, Any]) -> Project:
        ppq = 480
        time_sig = gold_def.get("meter", (4, 4))
        tempo_points = gold_def.get("tempo_points")
        tempo_bpm = gold_def.get("tempo_bpm", 120.0)

        if not tempo_points:
            tempo_points = [{"start_tick": 0, "bpm": tempo_bpm}]

        events = []
        if "events" in gold_def:
            events = gold_def["events"]
        else:
            chords = gold_def["chords"]
            dur_quarters = gold_def.get("chord_duration_quarters", 4.0)
            dur_ticks = int(round(dur_quarters * ppq))
            curr_tick = 0
            for sym in chords:
                events.append({
                    "start_tick": curr_tick,
                    "duration_ticks": dur_ticks,
                    "payload": sym,
                })
                curr_tick += dur_ticks

        return Project(
            title=gold_def["name"],
            notation_convention="INT",
            time_settings={
                "ppq": ppq,
                "time_signature": {"numerator": time_sig[0], "denominator": time_sig[1]},
                "tempo_bpm": tempo_bpm,
                "tempo_points": tempo_points,
            },
            tracks=[
                {
                    "track_id": "trk_chords",
                    "track_type": "CHORDS",
                    "name": "Chords Track",
                    "channel": 0,
                    "events": events,
                }
            ]
        )

    def test_all_10_golden_progressions_format_1_and_format_0(self):
        """Generates, exports and verifies both Format 0 and Format 1 for all 10 Golden files."""
        for gold in GOLDEN_PROGRESSIONS:
            gold_id = gold["id"]
            project = self._build_project_from_golden(gold)

            for smf_format in (0, 1):
                with self.subTest(gold_id=gold_id, smf_format=smf_format):
                    out_path = self.out_dir / f"{gold_id}_fmt{smf_format}.mid"
                    MidiExportService.export_project_to_smf(project, out_path, smf_format=smf_format)

                    self.assertTrue(out_path.exists())
                    raw_data = out_path.read_bytes()

                    # 1. Check Envelope with independent envelope reader
                    env = envelope(raw_data)
                    self.assertEqual(env["format"], smf_format)
                    self.assertEqual(env["division"], 480)
                    if smf_format == 1:
                        # Conductor track + Chords track = 2 tracks
                        self.assertEqual(env["tracks"], 2)
                    else:
                        # Format 0 = 1 track
                        self.assertEqual(env["tracks"], 1)

                    # 2. Binary Round-trip via parser
                    parsed_file = MidiFile.from_bytes(raw_data)
                    self.assertEqual(parsed_file.format, smf_format)
                    self.assertEqual(parsed_file.division, 480)
                    self.assertEqual(len(parsed_file.tracks), env["tracks"])

                    # 3. Collect Note Events and verify 1:1 Note-On/Note-Off pairing (T14)
                    note_events: List[Tuple[str, int, int, int]] = []
                    for trk in parsed_file.tracks:
                        for rev in trk.raw_events:
                            mb = rev.msg_bytes
                            if len(mb) >= 3 and (mb[0] & 0xF0) in (0x80, 0x90):
                                status = mb[0] & 0xF0
                                channel = mb[0] & 0x0F
                                pitch = mb[1]
                                vel = mb[2]
                                ev_name = "note_off" if (status == 0x80 or vel == 0) else "note_on"
                                note_events.append((ev_name, rev.abs_tick, channel, pitch))

                    self.assertGreater(len(note_events), 0)
                    pairing_errors = validate_midi_note_on_off_pairing(note_events)
                    self.assertEqual(pairing_errors, [], f"Hanging note detected in {gold_id} fmt{smf_format}: {pairing_errors}")

    def test_multi_tempo_golden_progression_invariants(self):
        """GOLD_09 verifies multi-tempo points and timing transitions (T15)."""
        gold_09 = next(g for g in GOLDEN_PROGRESSIONS if g["id"] == "GOLD_09_MULTI_TEMPO_METER")
        project = self._build_project_from_golden(gold_09)

        out_path = self.out_dir / "GOLD_09_tempo_test.mid"
        MidiExportService.export_project_to_smf(project, out_path, smf_format=1)

        raw = out_path.read_bytes()
        parsed = MidiFile.from_bytes(raw)
        conductor = parsed.tracks[0]

        tempo_events = [rev for rev in conductor.raw_events if rev.msg_bytes.startswith(b"\xFF\x51\x03")]
        self.assertEqual(len(tempo_events), 3)
        self.assertEqual(tempo_events[0].abs_tick, 0)
        self.assertEqual(tempo_events[1].abs_tick, 1920)
        self.assertEqual(tempo_events[2].abs_tick, 3360)


if __name__ == "__main__":
    unittest.main()

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

import hashlib
import shutil
import tempfile
import unittest
from pathlib import Path
from typing import Any, Dict, List, Tuple

from scripts.audit_midi_files import envelope
from scripts.generate_midi_daw_fixtures import generate_fixtures
from src.steps.midi.export_service import MidiExportService
from src.steps.midi.smf import MidiFile, MidiTrack
from src.steps.midi.smf_parser import SMFParser
from src.steps.models.timeline import validate_midi_note_on_off_pairing
from src.steps.progression.session import ProgressionSession
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

ADR017_GOLDEN_EXPORTS: list[dict[str, Any]] = [
    {
        "id": "GOLD_01_CLASSICAL_CADENCE",
        "chords": ["C", "F", "G", "C"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 120.0,
        "sha256": "ea9332015d9aeec4950b7dc80cac37620331736304fd728811f7aed461c5e53b",
    },
    {
        "id": "GOLD_02_JAZZ_MAJOR_251",
        "chords": ["Dm7", "G7", "Cmaj7"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 130.0,
        "sha256": "f1e2954e71ff8d8adf765464d2ea42a67ca3183c3e3e85811dd4d6533fd2209e",
    },
    {
        "id": "GOLD_03_JAZZ_MINOR_251",
        "chords": ["Dm7b5", "G7", "Cm7"],
        "key_root": "C",
        "is_minor": True,
        "tempo_bpm": 110.0,
        "sha256": "cb3a1bbcebd24b9149d4c5a6468f3609d365967260b2d33a52564d567d0c2775",
    },
    {
        "id": "GOLD_04_POP_AXIS",
        "chords": ["C", "G", "Am", "F"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 128.0,
        "sha256": "e7eb0d49f05c93d43567697fa5b8cb46debc3463b5c0c6c264b84bc8d6e77bd2",
    },
    {
        "id": "GOLD_05_SLASH_BASS",
        "chords": ["Dm7/C", "G7/B", "Cmaj7"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 116.0,
        "sha256": "2c95201ce1abfb8f47cf1a3194bf3a7df20a87f583be7bbba21cf82a22ef1e4c",
    },
    {
        "id": "GOLD_06_BLUES_12BAR",
        "chords": ["F7", "Bb7", "F7", "F7", "Bb7", "Bb7", "F7", "F7", "C7", "Bb7", "F7", "C7"],
        "key_root": "F",
        "is_minor": False,
        "tempo_bpm": 115.0,
        "sha256": "7af5d7d848a3cdf81bfbfd6d2efc8d206b69a5d8af4dcd0c5122ef2b25b8cb63",
    },
    {
        "id": "GOLD_07_ANDALUSIAN_CADENCE",
        "chords": ["Am", "G", "F", "E7"],
        "key_root": "A",
        "is_minor": True,
        "tempo_bpm": 120.0,
        "sha256": "724108d5c223bba43c75082d6adfc4b9819481ce1fa087db68b403684ce15889",
    },
    {
        "id": "GOLD_08_SECONDARY_DOMINANTS",
        "chords": ["C", "A7", "D7", "G7", "C"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 135.0,
        "sha256": "e5c5800f0e322c6e99947dbad231aee9c280927bb2429adc99f49e7a8365c058",
    },
    {
        "id": "GOLD_09_EVENT_TIMING",
        "chords": ["Cmaj7", "Fmaj7", "Cmaj7"],
        "key_root": "C",
        "is_minor": False,
        "tempo_bpm": 120.0,
        "event_timings": [(0, 1920), (1920, 1440), (3360, 1920)],
        "sha256": "6d25ffe59f8612716117c68772656889ea7fa6750bf7a4adcee51c0e6fdf4379",
    },
    {
        "id": "GOLD_10_GERMAN_H_NOTATION",
        "chords": ["H", "E", "Fis", "H"],
        "key_root": "H",
        "is_minor": False,
        "convention": "DE",
        "tempo_bpm": 100.0,
        "sha256": "511b7fd3cf953b07c9c7ae48eeb7d2b174ec71fd6071e0526b698d872ded540f",
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

    def test_daw_fixtures_are_reproducible_and_preserve_reference_exports(self):
        manifest = generate_fixtures(self.out_dir / "daw")
        other_manifest = generate_fixtures(self.out_dir / "repeat")
        self.assertEqual(manifest.read_bytes(), other_manifest.read_bytes())
        rows = [line.split("  ", 1) for line in manifest.read_text().splitlines()]
        self.assertEqual(len(rows), 6)
        for digest, filename in rows:
            with self.subTest(filename=filename):
                self.assertEqual(
                    hashlib.sha256((manifest.parent / filename).read_bytes()).hexdigest(),
                    digest,
                )

        cadence_path = manifest.parent / "GOLD_01_ADR017_Format1.mid"
        self.assertEqual(
            hashlib.sha256(cadence_path.read_bytes()).hexdigest(),
            ADR017_GOLDEN_EXPORTS[0]["sha256"],
        )
        timeline_path = manifest.parent / "GOLD_09_Project_Format1.mid"
        reference = self._build_project_from_golden(
            next(item for item in GOLDEN_PROGRESSIONS if item["id"].startswith("GOLD_09_"))
        )
        expected = MidiExportService.export_project_to_smf(reference, self.out_dir / "reference.mid")
        self.assertEqual(timeline_path.read_bytes(), expected.read_bytes())

        timeline = SMFParser.parse(timeline_path.read_bytes())
        meter = SMFParser.parse((manifest.parent / "GOLD_09_Meter_Import_Probe.mid").read_bytes())
        self.assertEqual(timeline.tempos, [(0, 120.0), (1920, 90.0), (3360, 120.0)])
        self.assertEqual(meter.tempos, timeline.tempos)
        self.assertEqual(meter.all_notes, timeline.all_notes)
        self.assertEqual(timeline.time_signatures, [(0, 4, 4)])
        self.assertEqual(meter.time_signatures, [(0, 4, 4), (1920, 3, 4), (3360, 4, 4)])

    def test_daw_overlap_probes_encode_two_starts_before_first_note_off(self):
        folder = generate_fixtures(self.out_dir / "overlap").parent
        pitches = [(0, pitch) for pitch in (48, 52, 55, 60)] + [(1, 36)]
        for smf_format, names in ((0, ["STEPS"]), (1, ["Conductor", "Chords", "Bass"])):
            with self.subTest(smf_format=smf_format):
                raw = (folder / f"ADR017_Overlap_Format{smf_format}.mid").read_bytes()
                parsed = SMFParser.parse(raw)
                self.assertEqual((parsed.format, parsed.division), (smf_format, 480))
                self.assertEqual([track.name for track in parsed.tracks], names)
                actual = [
                    (event.event_type, event.abs_tick, event.channel, event.data1)
                    for track in parsed.tracks
                    for event in track.events
                    if event.event_type in {"note_on", "note_off"}
                ]
                expected = [
                    (kind, tick, channel, pitch)
                    for kind, tick in (
                        ("note_on", 0), ("note_on", 960), ("note_off", 1910), ("note_off", 2870),
                    )
                    for channel, pitch in pitches
                ]
                self.assertCountEqual(actual, expected)

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
                    note_events: list[tuple[str, int, int, int]] = []
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

    def test_adr017_session_exports_match_10_golden_hashes(self):
        for golden in ADR017_GOLDEN_EXPORTS:
            with self.subTest(golden=golden["id"]):
                convention = golden.get("convention", "INT")
                session = ProgressionSession(
                    initial_chords=golden["chords"],
                    key_root=golden["key_root"],
                    is_minor=golden["is_minor"],
                    convention=convention,
                    bpm=golden["tempo_bpm"],
                    title=golden["id"],
                )
                session.set_context(
                    golden["key_root"],
                    golden["is_minor"],
                    golden["tempo_bpm"],
                    golden.get("meter", (4, 4)),
                    title=golden["id"],
                )
                for index, (start_tick, duration_ticks) in enumerate(
                    golden.get("event_timings", ())
                ):
                    session.set_chord_event_timing(index, start_tick, duration_ticks)

                output_path = self.out_dir / f'{golden["id"]}.mid'
                session.export_midi_file(output_path)
                raw_data = output_path.read_bytes()
                self.assertEqual(
                    hashlib.sha256(raw_data).hexdigest(),
                    golden["sha256"],
                )

                parsed = MidiFile.from_bytes(raw_data)
                self.assertEqual((parsed.format, parsed.division), (1, 480))
                self.assertEqual(
                    [track.name for track in parsed.tracks],
                    ["Conductor", "Chords", "Bass"],
                )
                independent = SMFParser.parse(raw_data)
                self.assertEqual((independent.format, independent.division), (1, 480))
                self.assertEqual(
                    [track.name for track in independent.tracks],
                    ["Conductor", "Chords", "Bass"],
                )
                self.assertEqual(independent.tempos, [(0, golden["tempo_bpm"])])
                self.assertEqual(
                    independent.time_signatures,
                    [(0, *golden.get("meter", (4, 4)))],
                )
                chord_note_ons = [
                    event
                    for event in parsed.tracks[1].raw_events
                    if event.msg_bytes[0] & 0xF0 == 0x90 and event.msg_bytes[2] > 0
                ]
                notes_by_start = {}
                for event in chord_note_ons:
                    notes_by_start.setdefault(event.abs_tick, []).append(event.msg_bytes[1])
                self.assertTrue(all(len(notes) == 4 for notes in notes_by_start.values()))
                self.assertTrue(
                    all(48 <= note <= 72 for notes in notes_by_start.values() for note in notes)
                )
                self.assertEqual(
                    len(independent.tracks[1].notes),
                    4 * len(golden["chords"]),
                )
                self.assertEqual(
                    len(independent.tracks[2].notes),
                    len(golden["chords"]),
                )
                self.assertEqual(
                    {note.channel for note in independent.tracks[1].notes},
                    {0},
                )
                self.assertEqual(
                    {note.channel for note in independent.tracks[2].notes},
                    {1},
                )
                self.assertTrue(
                    all(48 <= note.pitch <= 72 for note in independent.tracks[1].notes)
                )
                self.assertTrue(
                    all(36 <= note.pitch <= 47 for note in independent.tracks[2].notes)
                )
                note_events: List[Tuple[str, int, int, int]] = []
                for track in parsed.tracks:
                    self.assertFalse(
                        any(
                            event.msg_bytes[0] & 0xF0 == 0xC0
                            for event in track.raw_events
                        ),
                        "ADR-017 exports must not contain program changes.",
                    )
                    for event in track.raw_events:
                        message = event.msg_bytes
                        if (message[0] & 0xF0) in (0x80, 0x90):
                            status, velocity = message[0] & 0xF0, message[2]
                            name = "note_off" if status == 0x80 or velocity == 0 else "note_on"
                            note_events.append(
                                (name, event.abs_tick, message[0] & 0x0F, message[1])
                            )
                self.assertEqual(validate_midi_note_on_off_pairing(note_events), [])


if __name__ == "__main__":
    unittest.main()

"""
STEPS Vertical Slice End-to-End Verification Test Suite (Phase P1.3 / Prompt 09).

Validates the complete 4-chord user vertical slice across:
  Core (src/steps/theory, src/steps/progression)
  UI Presenter (app/ui/session_controller)
  Storage (src/steps/storage)
  MIDI (src/steps/midi)

User Workflow Tested:
  1. Initialize progression with 4 chords (C - G - Am - F) in C-Major
  2. Analyze Roman numerals (I - V - vi - IV) and adjacent voice leading
  3. Edit chord 4 to Fm (modal interchange)
  4. Transpose progression by +2 semitones to D-Major (D - A - Bm - Gm)
  5. Explore next harmonic continuations from dominant A
  6. Save project atomically to .stepsproj file
  7. Mutate and test Undo/Redo with dirty flag tracking
  8. Reload project from file and verify round-trip identity
  9. Export progression to SMF Format 1 MIDI file and verify SMF envelope
  10. UI Controller observable event listeners triggered on actions
"""

import shutil
import tempfile
import unittest
from pathlib import Path

from app.ui.session_controller import ProgressionSessionController
from scripts.audit_midi_files import envelope
from src.steps.progression.session import ProgressionSession
from src.steps.storage import CorruptedProjectError, Project, save_project


class TestVerticalSliceProgression(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_vertikalschnitt_test_")
        self.project_file = Path(self.temp_dir) / "test_progression.stepsproj"
        self.midi_file = Path(self.temp_dir) / "test_progression.mid"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_next_chord_controller_accepts_apply_rejects_invalid_and_undoes(self):
        session = ProgressionSession(
            initial_chords=["C", "G", "Am", "F"],
            key_root="C",
            is_minor=False,
            convention="INT",
        )
        controller = ProgressionSessionController(session)

        recommendations = controller.explore_next(1)
        candidate = next(r for r in recommendations if r.candidate_symbol == "C")

        applied = controller.apply_next_recommendation(1, candidate.candidate_symbol)

        self.assertEqual(applied.candidate_symbol, "C")
        self.assertEqual(session.chords, ["C", "G", "C", "Am", "F"])
        for index, (start, duration) in enumerate(session.state.chord_event_timings):
            self.assertGreaterEqual(start, 0)
            self.assertGreater(duration, 0)
            if index:
                previous_start, previous_duration = session.state.chord_event_timings[index - 1]
                self.assertGreaterEqual(start, previous_start + previous_duration)

        controller.undo()
        self.assertEqual(session.chords, ["C", "G", "Am", "F"])
        controller.redo()
        self.assertEqual(session.chords, ["C", "G", "C", "Am", "F"])

        with self.assertRaises(IndexError):
            controller.explore_next(-1)
        with self.assertRaises(IndexError):
            controller.explore_next(len(session.chords))
        with self.assertRaises(ValueError):
            controller.apply_next_recommendation(1, "NotARecommendation")

    def test_e2e_four_chord_vertical_slice(self):
        # 1. Initialize session with 4 chords (C - G - Am - F) in C-Major
        session = ProgressionSession(
            initial_chords=["C", "G", "Am", "F"],
            key_root="C",
            is_minor=False,
            convention="INT",
            bpm=120.0
        )
        controller = ProgressionSessionController(session)
        
        # Setup listener to verify observable UI notifications
        notifications = []
        controller.add_listener(lambda: notifications.append(1))

        vm0 = controller.get_view_model()
        self.assertEqual(vm0["chords"], ["C", "G", "Am", "F"])
        self.assertEqual(vm0["key_root"], "C")
        self.assertFalse(vm0["is_dirty"])

        # 2. Analyze Roman numerals (I - V - vi - IV) and adjacent voice leading
        analysis0 = vm0["analysis"]
        self.assertEqual(len(analysis0), 4)
        self.assertEqual(analysis0[0]["roman"], "I")
        self.assertEqual(analysis0[1]["roman"], "V")
        self.assertEqual(analysis0[2]["roman"], "vi")
        self.assertEqual(analysis0[3]["roman"], "IV")
        
        # Verify voice leading semitone distances are populated
        self.assertIsNotNone(analysis0[0]["distance_to_next"])
        self.assertIsNotNone(analysis0[1]["distance_to_next"])
        self.assertIsNotNone(analysis0[2]["distance_to_next"])

        # 3. Edit chord 4 to Fm (modal interchange iv in C)
        controller.set_chord(3, "Fm")
        self.assertEqual(len(notifications), 1)
        self.assertEqual(controller.session.chords[3], "Fm")
        self.assertTrue(controller.session.is_dirty)

        analysis1 = controller.get_view_model()["analysis"]
        self.assertEqual(analysis1[3]["roman"], "iv")  # Minor iv

        # 4. Transpose progression by +2 semitones to D-Major (D - A - Bm - Gm)
        controller.transpose(2)
        self.assertEqual(len(notifications), 2)
        self.assertEqual(controller.session.key_root, "D")
        self.assertEqual(controller.session.chords, ["D", "A", "Bm", "Gm"])

        analysis2 = controller.get_view_model()["analysis"]
        self.assertEqual(analysis2[0]["roman"], "I")   # D is now I
        self.assertEqual(analysis2[1]["roman"], "V")   # A is now V
        self.assertEqual(analysis2[2]["roman"], "vi")  # Bm is now vi
        self.assertEqual(analysis2[3]["roman"], "iv")  # Gm is now iv

        # 5. Explore next harmonic continuations from chord index 1 (Dominant A)
        recs = controller.explore_next(1)
        rec_symbols = [r.candidate_symbol for r in recs]
        # Must recommend dominant resolution to D
        self.assertIn("D", rec_symbols)
        # Verify relation types
        relations = {r.relation_type for r in recs}
        self.assertIn("RESOLVES_TO", relations)
        self.assertIn("DOMINANT_OF", relations)

        # 6. Save project atomically to .stepsproj file
        saved_path = controller.save(self.project_file)
        self.assertTrue(saved_path.exists())
        self.assertFalse(controller.session.is_dirty)  # Saved state is clean

        # 7. Mutate state, verify dirty, then Undo back to saved state
        controller.add_chord("Em")
        self.assertEqual(len(controller.session.chords), 5)
        self.assertTrue(controller.session.is_dirty)

        controller.undo()
        self.assertEqual(len(controller.session.chords), 4)
        self.assertFalse(controller.session.is_dirty)  # Restored to clean save point!

        # 8. Reload project from file and verify round-trip identity
        fresh_session = ProgressionSession()
        fresh_controller = ProgressionSessionController(fresh_session)
        fresh_controller.load(self.project_file)

        self.assertEqual(fresh_controller.session.chords, ["D", "A", "Bm", "Gm"])
        self.assertFalse(fresh_controller.session.is_dirty)

        # 9. Export progression to SMF Format 1 MIDI file and verify SMF envelope
        midi_path = fresh_controller.export_midi(self.midi_file)
        self.assertTrue(midi_path.exists())
        self.assertGreater(midi_path.stat().st_size, 100)

        # Verify SMF envelope with independent audit function
        env = envelope(midi_path.read_bytes())
        self.assertEqual(env["format"], 1)
        self.assertEqual(env["tracks"], 2)  # Conductor + Chords
        self.assertEqual(env["division"], 480)

        # 10. Notifications check
        self.assertGreaterEqual(len(notifications), 5)

    def test_project_roundtrip_preserves_key_notation_and_mode(self):
        session = ProgressionSession(
            initial_chords=["H7", "Em"],
            key_root="E",
            is_minor=True,
            convention="DE",
            bpm=96.0,
            voice_leading_style="POWER_CHORDS",
        )
        session.save_to_file(self.project_file)

        reopened = ProgressionSession()
        reopened.load_from_file(self.project_file)

        self.assertEqual(reopened.chords, ["H7", "Em"])
        self.assertEqual(reopened.key_root, "E")
        self.assertTrue(reopened.is_minor)
        self.assertEqual(reopened.convention, "DE")
        self.assertEqual(reopened.bpm, 96.0)
        self.assertEqual(reopened.voice_leading_style, "POWER_CHORDS")
        self.assertFalse(reopened.is_dirty)

    def test_project_without_new_key_metadata_uses_legacy_defaults(self):
        project = Project(metadata={})
        save_project(project, self.project_file)

        reopened = ProgressionSession()
        reopened.load_from_file(self.project_file)

        self.assertEqual(reopened.key_root, "C")
        self.assertFalse(reopened.is_minor)
        self.assertEqual(reopened.voice_leading_style, "CONTEMPORARY_POP")

    def test_invalid_project_chord_does_not_replace_current_session(self):
        invalid_project = Project(
            tracks=[
                {
                    "track_id": "trk_chords",
                    "track_type": "CHORDS",
                    "name": "Invalid Chords",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 480, "payload": "not-a-chord"}
                    ],
                }
            ]
        )
        save_project(invalid_project, self.project_file)
        session = ProgressionSession(initial_chords=["Am", "F"], key_root="A", is_minor=True)

        with self.assertRaises(CorruptedProjectError):
            session.load_from_file(self.project_file)

        self.assertEqual(session.chords, ["Am", "F"])
        self.assertEqual(session.key_root, "A")
        self.assertTrue(session.is_minor)


if __name__ == "__main__":
    unittest.main()

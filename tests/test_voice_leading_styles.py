"""
STEPS Music Theory Core: Stylistic Voice-Leading Rules Unit Tests (OA-0026).

Validates:
- M06 (Voice-leading constraints) & ERR-009 (Differentiating classical vs. contemporary pop/rock rules)
- Strict classical counterpoint (Fux 1725, Aldwell & Schachter 1989)
- Contemporary pop/rock & power chords (Walter Everett 2008/2009 "The Foundations of Rock", Tymoczko 2011)
- ProgressionSession and ProgressionSessionController integration
- Project save/load persistence of voice-leading style settings
"""

import unittest
from pathlib import Path
import tempfile

from src.steps.theory.voice_leading import (
    VoiceLeadingStyle,
    ContrapuntalMotion,
    VoiceLeadingViolation,
    VoiceLeadingEvaluation,
    classify_voice_motion,
    analyze_contrapuntal_motions,
    detect_parallel_fifths_octaves,
    detect_voice_crossing,
    detect_voice_overlap,
    evaluate_voice_leading_transition,
)
from src.steps.progression.session import ProgressionSession
from app.ui.session_controller import ProgressionSessionController
from src.steps.theory.exceptions import VoiceLeadingError


class TestVoiceLeadingStylesTheory(unittest.TestCase):
    """Verifies pure music theory rules across stylistic frameworks."""

    def test_voice_leading_style_attributes(self):
        """Verifies stylistic flags and reference frameworks for each style."""
        strict = VoiceLeadingStyle.STRICT_CLASSICAL
        self.assertTrue(strict.is_strict_counterpoint)
        self.assertFalse(strict.allows_parallel_fifths)
        self.assertFalse(strict.allows_parallel_octaves)
        self.assertFalse(strict.is_power_chord_style)
        self.assertIn("Fux", strict.reference_framework)

        pop = VoiceLeadingStyle.CONTEMPORARY_POP
        self.assertFalse(pop.is_strict_counterpoint)
        self.assertTrue(pop.allows_parallel_fifths)
        self.assertTrue(pop.allows_parallel_octaves)
        self.assertFalse(pop.is_power_chord_style)
        self.assertIn("Everett", pop.reference_framework)

        power = VoiceLeadingStyle.POWER_CHORDS
        self.assertFalse(power.is_strict_counterpoint)
        self.assertTrue(power.allows_parallel_fifths)
        self.assertTrue(power.is_power_chord_style)

    def test_pop_progression_parallel_fifths_differentiation(self):
        """
        Acceptance Criteria for OA-0026:
        Transition G -> Am with root position parallel fifths:
        G major: G2 (43), D3 (50), B3 (59)
        A minor: A2 (45), E3 (52), C4 (60)
        Voices 0 and 1 move:
          Voice 0 (Bass): 43 -> 45 (+2)
          Voice 1 (Tenor): 50 -> 52 (+2)
          Both start at interval 7 (perfect fifth) and move by +2 to interval 7 (perfect fifth).
        """
        g_notes = [43, 50, 59]
        am_notes = [45, 52, 60]

        # 1. Strict classical / counterpoint: MUST report parallel fifth violation
        strict_warnings = detect_parallel_fifths_octaves(
            g_notes, am_notes, style=VoiceLeadingStyle.STRICT_CLASSICAL
        )
        self.assertEqual(len(strict_warnings), 1)
        self.assertIn("Parallel fifth between voice 0 and 1", strict_warnings[0])

        strict_counterpoint_warnings = detect_parallel_fifths_octaves(
            g_notes, am_notes, style=VoiceLeadingStyle.STRICT_COUNTERPOINT
        )
        self.assertEqual(len(strict_counterpoint_warnings), 1)

        # 2. Contemporary pop / rock: MUST allow parallel fifths without error
        pop_warnings = detect_parallel_fifths_octaves(
            g_notes, am_notes, style=VoiceLeadingStyle.CONTEMPORARY_POP
        )
        self.assertEqual(pop_warnings, [])

        jazz_warnings = detect_parallel_fifths_octaves(
            g_notes, am_notes, style=VoiceLeadingStyle.JAZZ_POP
        )
        self.assertEqual(jazz_warnings, [])

        power_chord_warnings = detect_parallel_fifths_octaves(
            g_notes, am_notes, style=VoiceLeadingStyle.POWER_CHORDS
        )
        self.assertEqual(power_chord_warnings, [])

    def test_rock_power_chord_planing(self):
        """
        Rock power chords (E5 -> G5 -> A5):
        E5: E2 (40), B2 (47), E3 (52)
        G5: G2 (43), D3 (50), G3 (55)
        All voices parallel (+3 semitones).
        """
        e5 = [40, 47, 52]
        g5 = [43, 50, 55]

        # Strict classical: Both parallel fifth (0-1) and parallel octave (0-2)
        strict_warnings = detect_parallel_fifths_octaves(e5, g5, style="STRICT_CLASSICAL")
        self.assertEqual(len(strict_warnings), 2)

        # Power chords / Pop: Completely valid, no warnings
        power_warnings = detect_parallel_fifths_octaves(e5, g5, style="POWER_CHORDS")
        self.assertEqual(power_warnings, [])

    def test_voice_crossing_and_overlap(self):
        """Verifies voice crossing and overlap detection."""
        # Normal ascending: no crossing
        self.assertFalse(detect_voice_crossing([48, 55, 60, 64]))
        # Crossed: voice 1 is higher than voice 2
        self.assertTrue(detect_voice_crossing([48, 62, 60, 64]))

        # No overlap
        v_a = [48, 55, 60, 64]
        v_b = [45, 57, 59, 62]
        self.assertFalse(detect_voice_overlap(v_a, v_b))

        # Overlap: bass v_b[0] rises to 56, higher than previous tenor v_a[1] (55)
        v_c = [56, 58, 60, 64]
        self.assertTrue(detect_voice_overlap(v_a, v_c))

    def test_evaluate_voice_leading_transition_comprehensive(self):
        """Verifies comprehensive evaluation including violations and stylistic annotations."""
        g_notes = [43, 50, 59]
        am_notes = [45, 52, 60]

        eval_strict = evaluate_voice_leading_transition(
            g_notes, am_notes, style=VoiceLeadingStyle.STRICT_CLASSICAL
        )
        self.assertFalse(eval_strict.is_valid)
        self.assertEqual(len(eval_strict.violations), 1)
        self.assertEqual(eval_strict.violations[0].violation_type, "PARALLEL_FIFTH")
        self.assertIn("Fux", eval_strict.violations[0].rule_source)

        eval_pop = evaluate_voice_leading_transition(
            g_notes, am_notes, style=VoiceLeadingStyle.CONTEMPORARY_POP
        )
        self.assertTrue(eval_pop.is_valid)
        self.assertEqual(len(eval_pop.violations), 0)
        self.assertGreater(len(eval_pop.stylistic_notes), 0)
        self.assertIn("Everett", eval_pop.stylistic_notes[0])


class TestVoiceLeadingStylesSessionIntegration(unittest.TestCase):
    """Verifies integration into ProgressionSession and ProgressionSessionController."""

    def test_progression_session_style_switching(self):
        """Verifies ProgressionSession analyzes according to active voice-leading style."""
        # Progression with natural pop parallel fifths in close position: G -> Am
        session = ProgressionSession(
            initial_chords=["G", "Am"],
            voice_leading_style=VoiceLeadingStyle.CONTEMPORARY_POP,
        )
        self.assertEqual(session.voice_leading_style, VoiceLeadingStyle.CONTEMPORARY_POP)

        # 1. Under CONTEMPORARY_POP: no warnings for parallel fifths
        analysis_pop = session.analyze_progression()
        has_warnings_pop = any(len(a.voice_leading_warnings) > 0 for a in analysis_pop)
        self.assertFalse(has_warnings_pop)

        # 2. When evaluated under STRICT_CLASSICAL: reports parallel fifth violation
        analysis_strict = session.analyze_progression(style=VoiceLeadingStyle.STRICT_CLASSICAL)
        has_warnings_strict = any(len(a.voice_leading_warnings) > 0 for a in analysis_strict)
        self.assertTrue(has_warnings_strict)
        self.assertIn("Parallel fifth between voice 0 and 2", analysis_strict[0].voice_leading_warnings)

        # 3. Switching session style mutates state and is reversible via undo
        session.set_voice_leading_style(VoiceLeadingStyle.STRICT_CLASSICAL)
        self.assertEqual(session.voice_leading_style, VoiceLeadingStyle.STRICT_CLASSICAL)
        session.undo()
        self.assertEqual(session.voice_leading_style, VoiceLeadingStyle.CONTEMPORARY_POP)

    def test_controller_view_model_and_notifications(self):
        """Verifies ProgressionSessionController exposes voice_leading_style and notifies views."""
        controller = ProgressionSessionController()
        vm = controller.get_view_model()
        self.assertIn("voice_leading_style", vm)
        self.assertEqual(vm["voice_leading_style"], "CONTEMPORARY_POP")

        notified = []
        controller.add_listener(lambda: notified.append(True))

        controller.set_voice_leading_style(VoiceLeadingStyle.STRICT_CLASSICAL)
        self.assertEqual(controller.session.voice_leading_style, VoiceLeadingStyle.STRICT_CLASSICAL)
        self.assertEqual(len(notified), 1)

        vm_updated = controller.get_view_model()
        self.assertEqual(vm_updated["voice_leading_style"], "STRICT_CLASSICAL")

    def test_project_persistence_roundtrip(self):
        """Verifies voice_leading_style is persisted and restored via project file save/load."""
        with tempfile.TemporaryDirectory() as tmp_dir:
            file_path = Path(tmp_dir) / "test_vl_style.steps.json"
            session = ProgressionSession(
                initial_chords=["C", "F", "G", "C"],
                voice_leading_style=VoiceLeadingStyle.STRICT_CLASSICAL,
            )
            session.save_to_file(file_path)

            new_session = ProgressionSession()
            new_session.load_from_file(file_path)
            self.assertEqual(
                new_session.voice_leading_style,
                VoiceLeadingStyle.STRICT_CLASSICAL
            )


if __name__ == "__main__":
    unittest.main()

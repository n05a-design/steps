"""Tests for non-mutating style comparisons and explicit style application."""

import unittest
from unittest.mock import Mock

from app.i18n import LocaleManager
from app.ui.session_controller import ProgressionSessionController, VoiceLeadingStyleProfile
from app.ui.voice_leading_lab_dialog import (
    VoiceLeadingLabDialog,
    format_voice_leading_profile,
)
from src.steps.progression.session import DegreeAnalysis, ProgressionSession
from src.steps.progression.voice_leading import VoiceLeadingStyle
from src.steps.theory.voice_leading import detect_parallel_fifths_octaves, find_perfect_interval_motion


class TestVoiceLeadingLab(unittest.TestCase):
    def setUp(self):
        self.session = ProgressionSession(
            initial_chords=["C", "G", "Am", "F"],
            key_root="C",
        )
        self.controller = ProgressionSessionController(self.session)

    def test_style_profiles_use_requested_style_without_mutating_project(self):
        pop = self.controller.analyze_voice_leading_style(
            VoiceLeadingStyle.CONTEMPORARY_POP
        )
        strict = self.controller.analyze_voice_leading_style(
            VoiceLeadingStyle.STRICT_CLASSICAL
        )

        self.assertNotEqual(pop.total_movement, strict.total_movement)
        self.assertEqual(self.session.voice_leading_style, VoiceLeadingStyle.CONTEMPORARY_POP)
        self.assertFalse(self.session.is_dirty)
        self.assertEqual(len(strict.transitions), len(self.session.chords))
        self.assertEqual(strict.midi_notes, tuple(
            tuple(voicing.midi_notes)
            for voicing in self.session.get_voicings(style=VoiceLeadingStyle.STRICT_CLASSICAL)
        ))

    def test_profile_summary_labels_movement_as_descriptive(self):
        profile = self.controller.analyze_voice_leading_style(
            VoiceLeadingStyle.STRICT_CLASSICAL
        )

        rendered = format_voice_leading_profile(
            profile,
            tuple(self.session.chords),
            self.session.voice_leading_style,
            LocaleManager(preference="en").translate,
        )

        self.assertIn("Cumulative absolute MIDI-note movement", rendered)
        self.assertIn("not a universal ranking", rendered)
        self.assertIn("C → G", rendered)

    def test_profile_localizes_detected_parallel_and_contrary_motion(self):
        style = VoiceLeadingStyle.STRICT_CLASSICAL
        for start, end, en, de in (
            ([60, 67], [62, 69], "Parallel fifth", "Quintparallele"),
            ([60, 67], [59, 78], "Fifth in contrary motion", "Quinte in Gegenbewegung"),
            ([60, 72], [61, 73], "Parallel octave or unison", "Oktav- oder Primparallele"),
            ([60, 72], [61, 61], "Octave or unison in contrary motion", "Oktave oder Prime in Gegenbewegung"),
        ):
            with self.subTest(start=start, end=end):
                diagnostics = find_perfect_interval_motion(start, end, style)
                self.assertEqual(len(diagnostics), 1)
                legacy = detect_parallel_fifths_octaves(start, end, style)
                self.assertEqual(legacy, [diagnostics[0].describe()])
                transition = DegreeAnalysis(
                    0, "C", "I", semitone_distance_to_next=2,
                    voice_leading_warnings=tuple(legacy),
                    voice_leading_diagnostics=tuple(diagnostics),
                )
                profile = VoiceLeadingStyleProfile(
                    style, (transition, DegreeAnalysis(1, "D", "II")), 2,
                    (tuple(start), tuple(end)),
                )
                for language, expected in (("en", en), ("de", de)):
                    text = format_voice_leading_profile(
                        profile, ("C", "D"), style, LocaleManager(preference=language).translate,
                    )
                    self.assertIn(expected, text)
                    self.assertRegex(text, r"1 (?:and|und) 2")

    def test_dialog_stays_open_when_style_application_is_rejected(self):
        dialog = object.__new__(VoiceLeadingLabDialog)
        dialog._profiles = [Mock(style=VoiceLeadingStyle.STRICT_CLASSICAL), None]
        dialog._refresh_changed_project = Mock(return_value=False)
        dialog._on_apply = Mock(return_value=False)
        dialog._close = Mock()

        dialog._apply_profile(0)

        dialog._on_apply.assert_called_once_with("STRICT_CLASSICAL")
        dialog._close.assert_not_called()

    def test_dialog_closes_after_style_application(self):
        dialog = object.__new__(VoiceLeadingLabDialog)
        dialog._profiles = [Mock(style=VoiceLeadingStyle.STRICT_CLASSICAL), None]
        dialog._refresh_changed_project = Mock(return_value=False)
        dialog._on_apply = Mock(return_value=True)
        dialog._close = Mock()

        dialog._apply_profile(0)

        dialog._close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

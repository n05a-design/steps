"""Tests for non-mutating style comparisons and explicit style application."""

import unittest
from unittest.mock import Mock

from app.i18n import LocaleManager
from app.ui.session_controller import ProgressionSessionController
from app.ui.voice_leading_lab_dialog import (
    VoiceLeadingLabDialog,
    format_voice_leading_profile,
)
from src.steps.progression.session import ProgressionSession
from src.steps.progression.voice_leading import VoiceLeadingStyle


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

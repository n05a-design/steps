"""Tests for ADR-017 MIDI export option handling."""

import errno
import unittest
from unittest.mock import Mock

from app.i18n import LocaleManager
from app.ui.midi_export_dialog import (
    MidiExportOptions, MidiExportOptionsDialog, format_midi_file_error,
)


class TestMidiExportOptions(unittest.TestCase):
    def test_defaults_match_adr017_compatibility_contract(self):
        self.assertEqual(
            MidiExportOptions(),
            MidiExportOptions(
                voicing_type="CLOSE",
                note_duration_mode="FIXED_GAP",
                smf_format=1,
            ),
        )

    def test_rejects_unsupported_options(self):
        invalid_options = (
            {"voicing_type": "SHELL"},
            {"note_duration_mode": "LEGATO"},
            {"smf_format": 2},
            {"smf_format": True},
        )
        for kwargs in invalid_options:
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                MidiExportOptions(**kwargs)

    def test_windows_sharing_violation_has_specific_recovery_message(self):
        error = PermissionError(errno.EACCES, "file in use")
        error.winerror = 32
        for language in ("en", "de"):
            locale = LocaleManager(preference=language)
            self.assertEqual(
                format_midi_file_error(error, "demo.mid", locale),
                locale.translate("midi.export.error.locked", path="demo.mid"),
            )

    def test_dialog_closes_only_after_successful_export(self):
        dialog = object.__new__(MidiExportOptionsDialog)
        dialog._voicing_var = Mock(get=Mock(return_value="DROP2"))
        dialog._duration_var = Mock(get=Mock(return_value="PERCENT_95"))
        dialog._format_var = Mock(get=Mock(return_value="0"))
        dialog._on_export = Mock(return_value=False)
        dialog._close = Mock()

        dialog._export()

        dialog._on_export.assert_called_once_with(
            MidiExportOptions(
                voicing_type="DROP2",
                note_duration_mode="PERCENT_95",
                smf_format=0,
            )
        )
        dialog._close.assert_not_called()

        dialog._on_export.return_value = True
        dialog._export()
        dialog._close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

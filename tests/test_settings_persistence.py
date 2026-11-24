"""
Unit Tests for STEPS Settings & Preferences Persistence (Glide parity).
"""

import os
import tempfile
import unittest
from pathlib import Path

from app.settings import (
    DEFAULT_SETTINGS,
    get_settings_file,
    load_settings,
    normalize_settings,
    save_settings,
)


class TestSettingsPersistence(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.TemporaryDirectory()
        self.base_dir = Path(self.temp_dir.name)

    def tearDown(self):
        self.temp_dir.cleanup()

    def test_default_settings_when_file_missing(self):
        loaded = load_settings(self.base_dir)
        self.assertEqual(loaded, DEFAULT_SETTINGS)

    def test_save_and_reload_settings(self):
        custom = {
            "theme_preference": "glass-dark",
            "background_color": "due_action",
            "accent_color": "export",
            "corner_radius": "large",
            "font_scale": "large",
            "font_weight": "bold",
            "animations_enabled": False,
            "hints_visible": False,
            "language": "de",
            "window_geometry": "1024x720+100+100",
            "saved_compact_geometry": "520x720+604+100",
        }
        ok = save_settings(custom, self.base_dir)
        self.assertTrue(ok)

        filepath = get_settings_file(self.base_dir)
        self.assertTrue(filepath.is_file())

        loaded = load_settings(self.base_dir)
        self.assertEqual(loaded, custom)

    def test_normalize_invalid_values(self):
        corrupt = {
            "theme_preference": "invalid_mode",
            "background_color": "not_a_bg",
            "accent_color": "bad_accent",
            "corner_radius": "huge",
            "font_scale": "tiny",
            "font_weight": "heavy",
            "animations_enabled": "not_a_bool",
            "hints_visible": 1,
            "language": "es",
        }
        normalized = normalize_settings(corrupt)
        self.assertEqual(normalized["theme_preference"], DEFAULT_SETTINGS["theme_preference"])
        self.assertEqual(normalized["background_color"], DEFAULT_SETTINGS["background_color"])
        self.assertEqual(normalized["accent_color"], DEFAULT_SETTINGS["accent_color"])
        self.assertEqual(normalized["corner_radius"], DEFAULT_SETTINGS["corner_radius"])
        self.assertEqual(normalized["font_scale"], DEFAULT_SETTINGS["font_scale"])
        self.assertEqual(normalized["font_weight"], DEFAULT_SETTINGS["font_weight"])
        self.assertTrue(normalized["animations_enabled"])
        self.assertTrue(normalized["hints_visible"])
        self.assertEqual(normalized["language"], DEFAULT_SETTINGS["language"])


if __name__ == "__main__":
    unittest.main()

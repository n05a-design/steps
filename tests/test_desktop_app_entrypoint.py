"""
Unit Tests for STEPS Desktop Application Entrypoint & 2-Pane UI (ADR-001 / Prompt 01).

Validates:
- Headless execution mode for CI pipelines
- CLI argument parsing (--export-midi, --theme, --headless)
- Integration of StepsMainWindow with ProgressionSessionController
- Verification of 2-Pane UI hierarchy (Working Area & Information Area)
"""

import os
import shutil
import tempfile
import unittest
from pathlib import Path

from app.main import main
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager


class TestDesktopAppEntrypoint(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_app_test_")
        self.midi_path = str(Path(self.temp_dir) / "test_out.mid")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_headless_mode_returns_zero(self):
        exit_code = main(["--headless"])
        self.assertEqual(exit_code, 0)

    def test_export_midi_cli_arg(self):
        exit_code = main(["--export-midi", self.midi_path])
        self.assertEqual(exit_code, 0)
        self.assertTrue(Path(self.midi_path).exists())
        self.assertGreater(Path(self.midi_path).stat().st_size, 50)

    def test_main_window_instantiation_and_wiring(self):
        """Tests UI creation and controller wiring without triggering Tk mainloop."""
        try:
            import tkinter as tk
            from app.ui.main_window import StepsMainWindow
        except ImportError:
            self.skipTest("tkinter not available in environment")

        try:
            root = tk.Tk()
        except tk.TclError:
            self.skipTest("Tk initialization failed (no graphics display)")

        try:
            root.withdraw()  # Do not display window on screen
            ctrl = ProgressionSessionController()
            theme = ThemeManager(mode="dark")
            window = StepsMainWindow(root, controller=ctrl, theme=theme)

            # Area 1 checks
            self.assertIsNotNone(window.work_area)
            self.assertIsNotNone(window.chord_listbox)
            self.assertGreater(window.chord_listbox.size(), 0)

            # Area 2 checks
            self.assertIsNotNone(window.info_area)
            self.assertIsNotNone(window.detail_text)
            content = window.detail_text.get("1.0", tk.END)
            self.assertIn("AKKORD-ANALYSE", content)

            # Test UI add chord action
            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "F#m7b5")
            window._on_add_chord()
            self.assertIn("F#m7b5", ctrl.session.chords)

            # Test Transpose action
            prev_first = ctrl.session.chords[0]
            window._on_transpose(2)
            self.assertNotEqual(ctrl.session.chords[0], prev_first)

            root.destroy()
        except Exception as e:
            root.destroy()
            raise e


if __name__ == "__main__":
    unittest.main()

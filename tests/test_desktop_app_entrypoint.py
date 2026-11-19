"""
Unit Tests for STEPS Desktop Application Entrypoint & 2-Pane UI (ADR-001 / Prompt 01).

Validates:
- Headless execution mode for CI pipelines
- CLI argument parsing (--export-midi, --theme, --headless)
- Integration of StepsMainWindow with ProgressionSessionController
- Verification of 2-Pane UI hierarchy (Working Area & Information Area)
- Platform keyboard accelerators and the real UI save/open/export workflow
"""

import os
import shutil
import sys
import tempfile
import unittest
from contextlib import redirect_stdout
from io import StringIO
from pathlib import Path
from unittest.mock import patch

from app.main import main
from app.i18n import LocaleManager
from app.ui.session_controller import ProgressionSessionController
from app.ui.theme import ThemeManager
from src.steps.midi import MidiFile


class TestDesktopAppEntrypoint(unittest.TestCase):
    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_app_test_")
        self.midi_path = str(Path(self.temp_dir) / "test_out.mid")

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_headless_mode_returns_zero(self):
        exit_code = main(["--headless"])
        self.assertEqual(exit_code, 0)

    def test_cli_language_override_localizes_output_without_persisting_preference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = Path(temp_dir) / "preferences.json"
            manager = LocaleManager(settings_file=settings, system_locale="en_US")
            output = StringIO()
            with patch("app.main.LocaleManager", return_value=manager), redirect_stdout(output):
                exit_code = main(["--language", "de", "--headless"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Headless-Modus aktiv", output.getvalue())
            self.assertFalse(settings.exists())

            output = StringIO()
            with patch("app.main.LocaleManager", return_value=manager), redirect_stdout(output):
                exit_code = main(["--language", "en", "--headless"])

            self.assertEqual(exit_code, 0)
            self.assertIn("Headless mode active", output.getvalue())

    def test_cli_language_override_localizes_help_without_persisting_preference(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = Path(temp_dir) / "preferences.json"
            manager = LocaleManager(settings_file=settings, system_locale="en_US")
            output = StringIO()
            with patch("app.main.LocaleManager", return_value=manager), redirect_stdout(output):
                with self.assertRaises(SystemExit) as result:
                    main(["--language", "de", "--help"])

            self.assertEqual(result.exception.code, 0)
            self.assertIn("Desktop-Anwendung für Musiktheorie", output.getvalue())
            self.assertFalse(settings.exists())

    def test_export_midi_cli_arg(self):
        exit_code = main(["--export-midi", self.midi_path])
        self.assertEqual(exit_code, 0)
        self.assertTrue(Path(self.midi_path).exists())
        self.assertGreater(Path(self.midi_path).stat().st_size, 50)

    def test_main_window_instantiation_and_wiring(self):
        """Tests UI creation and controller wiring without triggering Tk mainloop."""
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        try:
            import tkinter as tk
            from app.ui.main_window import StepsMainWindow
        except ImportError as exc:
            if require_tk:
                self.fail(f"Tk is required for this platform smoke test: {exc}")
            self.skipTest("tkinter not available in environment")

        try:
            root = tk.Tk()
        except tk.TclError as exc:
            if require_tk:
                self.fail(f"Tk could not initialize for this platform smoke test: {exc}")
            self.skipTest("Tk initialization failed (no graphics display)")

        try:
            root.withdraw()  # Do not display window on screen
            ctrl = ProgressionSessionController()
            theme = ThemeManager(mode="dark")
            window = StepsMainWindow(
                root, controller=ctrl, theme=theme, locale_manager=LocaleManager(preference="de")
            )

            shortcut_prefix = "⌘" if sys.platform == "darwin" else "Ctrl+"
            for index, key in enumerate(("N", "O", "S")):
                self.assertEqual(
                    window.file_menu.entrycget(index, "accelerator"),
                    f"{shortcut_prefix}{key}",
                )
            for sequence in (
                "<Control-n>",
                "<Control-o>",
                "<Control-s>",
                "<Control-z>",
                "<Control-Shift-z>",
                "<Command-n>",
                "<Command-o>",
                "<Command-s>",
                "<Command-z>",
                "<Command-Shift-z>",
            ):
                self.assertTrue(root.bind_all(sequence), f"Missing keyboard binding: {sequence}")

            # Area 1 checks
            self.assertIsNotNone(window.work_area)
            self.assertIsNotNone(window.chord_listbox)
            self.assertGreater(window.chord_listbox.size(), 0)

            # Area 2 checks
            self.assertIsNotNone(window.info_area)
            self.assertIsNotNone(window.detail_text)
            content = window.detail_text.get("1.0", tk.END)
            self.assertIn(window.i18n.translate("chord.analysis.title", chord="C"), content)

            window.key_entry.delete(0, tk.END)
            window.key_entry.insert(0, "D")
            window.mode_var.set(True)
            window.tempo_entry.delete(0, tk.END)
            window.tempo_entry.insert(0, "96")
            window.context_btn.invoke()
            self.assertEqual(
                (ctrl.session.key_root, ctrl.session.is_minor, ctrl.session.bpm),
                ("D", True, 96.0),
            )
            window.undo_btn.invoke()
            self.assertEqual(
                (ctrl.session.key_root, ctrl.session.is_minor, ctrl.session.bpm),
                ("C", False, 120.0),
            )

            # Test UI add chord action
            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "F#m7b5")
            window.add_btn.invoke()
            self.assertIn("F#m7b5", ctrl.session.chords)
            self.assertEqual(window.chord_listbox.curselection(), (4,))

            window.move_up_btn.invoke()
            self.assertEqual(ctrl.session.chords[-2:], ["F#m7b5", "F"])
            self.assertEqual(window.chord_listbox.curselection(), (3,))
            window.move_down_btn.invoke()
            self.assertEqual(ctrl.session.chords[-2:], ["F", "F#m7b5"])

            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "Fm7")
            window.update_btn.invoke()
            self.assertEqual(ctrl.session.chords[-1], "Fm7")

            window.remove_btn.invoke()
            self.assertNotIn("Fm7", ctrl.session.chords)
            window.undo_btn.invoke()
            self.assertIn("Fm7", ctrl.session.chords)
            window.redo_btn.invoke()
            self.assertNotIn("Fm7", ctrl.session.chords)
            window.undo_btn.invoke()

            # Test Transpose action
            prev_first = ctrl.session.chords[0]
            window._on_transpose(2)
            self.assertNotEqual(ctrl.session.chords[0], prev_first)

            project_path = Path(self.temp_dir) / "ui_workflow.stepsproj"
            with patch(
                "app.ui.main_window.filedialog.asksaveasfilename",
                return_value=str(project_path),
            ):
                window.file_menu.invoke(3)
            self.assertTrue(project_path.is_file())
            saved_chords = ctrl.session.chords

            window._on_transpose(1)
            with (
                patch(
                    "app.ui.main_window.filedialog.askopenfilename",
                    return_value=str(project_path),
                ),
                patch("app.ui.main_window.messagebox.askyesnocancel", return_value=False),
            ):
                window.file_menu.invoke(1)
            self.assertEqual(ctrl.session.chords, saved_chords)
            self.assertFalse(ctrl.session.is_dirty)

            with patch(
                "app.ui.main_window.filedialog.asksaveasfilename",
                return_value=self.midi_path,
            ):
                window.export_btn.invoke()
            midi_path = Path(self.midi_path)
            self.assertTrue(midi_path.is_file())
            parsed_midi = MidiFile.from_bytes(midi_path.read_bytes())
            self.assertEqual(
                [track.name for track in parsed_midi.tracks],
                ["Conductor", "Chords", "Bass"],
            )

            root.destroy()
        except Exception as e:
            root.destroy()
            raise e


if __name__ == "__main__":
    unittest.main()

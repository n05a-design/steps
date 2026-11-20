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
from app.ui.midi_export_dialog import MidiExportOptions
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
            ), patch("app.ui.main_window.MidiExportOptionsDialog") as export_dialog:
                window.export_btn.invoke()
                export_dialog.call_args.kwargs["on_export"](MidiExportOptions())
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


    def test_native_dialog_workflow(self):
        """Drive real widgets on the platform; inject OS file chooser responses."""
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        try:
            import tkinter as tk
            from tkinter import ttk
            from app.ui.main_window import StepsMainWindow
        except ImportError as exc:
            if require_tk:
                self.fail(f"Tk is required for the desktop smoke test: {exc}")
            self.skipTest("tkinter not available")
        try:
            root = tk.Tk()
        except tk.TclError as exc:
            if require_tk:
                self.fail(f"Tk could not initialize: {exc}")
            self.skipTest("No Tk graphics display")
        def destroy_root():
            try:
                root.destroy()
            except tk.TclError:
                pass

        self.addCleanup(destroy_root)
        callback_errors = []
        root.report_callback_exception = lambda *error: callback_errors.append(error)
        i18n = LocaleManager(preference="en")
        window = StepsMainWindow(root, locale_manager=i18n)
        controller = window.controller
        root.update()

        def widgets(parent, kind):
            for child in parent.winfo_children():
                if isinstance(child, kind):
                    yield child
                yield from widgets(child, kind)

        def button(parent, key):
            return next(
                widget for widget in widgets(parent, (tk.Button, ttk.Button))
                if widget.cget("text") == i18n.translate(key)
            )

        def modal():
            root.update()
            dialog = root.grab_current()
            self.assertIsInstance(dialog, tk.Toplevel)
            self.assertTrue(dialog.winfo_ismapped())
            return dialog

        with (
            patch("app.ui.main_window.messagebox.showerror") as errors,
            patch("app.ui.main_window.messagebox.askyesnocancel", return_value=None) as prompt,
        ):
            window.file_menu.invoke(0)
            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "!")
            window.update_btn.invoke()
            errors.assert_called_once()
            self.assertFalse(controller.session.is_dirty)
            errors.reset_mock()

            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "Dm7")
            window.update_btn.invoke()
            self.assertTrue(controller.session.is_dirty)
            window.file_menu.invoke(4)
            library = modal()
            search = next(widgets(library, tk.Entry))
            preview = next(widgets(library, tk.Text))
            search.insert(0, "no-matching-example")
            self.assertIn(i18n.translate("library.no_results"), preview.get("1.0", tk.END))
            search.delete(0, tk.END)
            search.insert(0, "PROG-003")
            self.assertIn("G7", preview.get("1.0", tk.END))
            button(library, "library.load").invoke()
            self.assertTrue(library.winfo_exists())
            self.assertEqual(controller.session.chords[0], "Dm7")
            prompt.return_value = False
            button(library, "library.load").invoke()
            self.assertFalse(library.winfo_exists())
            self.assertEqual(controller.session.chords, ["Dm7", "G7", "Cmaj7"])
            window.file_menu.invoke(4)
            button(modal(), "library.close").invoke()

            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "Dm")
            window.update_btn.invoke()
            before = tuple(controller.session.state.chord_event_timings)
            window.explore_next_btn.invoke()
            self.assertGreater(window.next_candidates_list.size(), 0)
            window.next_candidates_list.selection_set(0)
            window.next_candidates_list.event_generate("<<ListboxSelect>>")
            root.update()
            self.assertIn(i18n.translate("next_chord.original"), window.detail_text.get("1.0", tk.END))
            window.apply_next_btn.invoke()
            self.assertEqual(len(controller.session.chords), 4)
            window.undo_btn.invoke()
            self.assertEqual(tuple(controller.session.state.chord_event_timings), before)
            window.redo_btn.invoke()

            active_style = controller.session.voice_leading_style
            window.voice_lab_btn.invoke()
            lab = modal()
            rolls = list(widgets(lab, tk.Canvas))
            self.assertEqual(len(rolls), 2)
            self.assertTrue(all(roll.find_withtag("note") for roll in rolls))
            selector = list(widgets(lab, ttk.Combobox))[1]
            selector.current(1 if active_style.value != "STRICT_CLASSICAL" else 0)
            selector.event_generate("<<ComboboxSelected>>")
            root.update()
            self.assertEqual(controller.session.voice_leading_style, active_style)
            button(lab, "voice.lab.apply_b").invoke()
            self.assertFalse(lab.winfo_exists())
            self.assertNotEqual(controller.session.voice_leading_style, active_style)
            window.undo_btn.invoke()
            self.assertEqual(controller.session.voice_leading_style, active_style)
            window.redo_btn.invoke()

            window.export_btn.invoke()
            export = modal()
            for key in ("midi.options.duration.percent_95", "midi.options.format.type0"):
                radio = next(
                    widget for widget in widgets(export, tk.Radiobutton)
                    if widget.cget("text") == i18n.translate(key)
                )
                radio.invoke()
            with patch("app.ui.main_window.filedialog.asksaveasfilename", return_value=""):
                button(export, "midi.options.export").invoke()
            self.assertTrue(export.winfo_exists())
            with patch("app.ui.main_window.filedialog.asksaveasfilename", return_value=self.midi_path):
                button(export, "midi.options.export").invoke()
            self.assertFalse(export.winfo_exists())
            midi = MidiFile.from_bytes(Path(self.midi_path).read_bytes())
            self.assertEqual(len(midi.tracks), 1)

            path = Path(self.temp_dir) / "native.stepsproj"
            expected_state = controller.session.state
            with patch("app.ui.main_window.filedialog.asksaveasfilename", return_value=str(path)):
                window.file_menu.invoke(2)
            self.assertTrue(path.is_file())
            self.assertFalse(controller.session.is_dirty)
            window._on_close()

            reopened_root = tk.Tk()
            self.addCleanup(reopened_root.destroy)
            reopened = StepsMainWindow(reopened_root, locale_manager=i18n)
            with patch("app.ui.main_window.filedialog.askopenfilename", return_value=str(path)):
                reopened.file_menu.invoke(1)
            self.assertEqual(reopened.controller.session.state, expected_state)
            errors.assert_not_called()
            self.assertFalse(callback_errors)


if __name__ == "__main__":
    unittest.main()

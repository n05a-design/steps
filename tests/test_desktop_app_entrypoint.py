"""
Unit Tests for STEPS Desktop Application Entrypoint & 2-Pane UI (ADR-001 / Prompt 01).

Validates:
- Headless execution mode for CI pipelines
- CLI argument parsing (--export-midi, --theme, --headless)
- Integration of StepsMainWindow with ProgressionSessionController
- Verification of 2-Pane UI hierarchy (Working Area & Information Area)
- Platform keyboard accelerators and the real UI save/open/export workflow
"""

import errno
import json
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
from app.knowledge import get_reviewed_progression
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
                self.assertTrue(root.bind(sequence), f"Missing window keyboard binding: {sequence}")

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
            current_state = ctrl.session.state
            with patch("app.ui.main_window.messagebox.showerror") as showerror:
                window._on_transpose(-200)
            showerror.assert_called_once()
            self.assertEqual(ctrl.session.state, current_state)

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
        self.assertIn(
            i18n.translate("chord.degree", degree="I"),
            window.detail_text.get("1.0", tk.END),
        )

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
            patch("app.ui.reviewed_library_dialog.webbrowser.open", return_value=True) as browser,
        ):
            for _ in range(30):
                controller.add_chord("C")
            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "G7")
            window.add_btn.invoke()
            root.update()
            rows = window.chord_listbox
            last = rows.size() - 1
            self.assertEqual(rows.curselection(), (last,))
            self.assertEqual(rows.index(tk.ACTIVE), last)
            self.assertEqual(rows.yview()[1], 1.0)
            self.assertIsNotNone(rows.bbox(last))
            modifier = "Option" if sys.platform == "darwin" else "Alt"
            rows.focus_force()
            root.update()
            revision = controller.revision
            rows.event_generate(f"<{modifier}-Down>")
            root.update()
            self.assertEqual(controller.revision, revision)
            last_timing = controller.session.get_chord_event_timing(last)
            rows.event_generate(f"<{modifier}-Up>")
            root.update()
            self.assertEqual(rows.curselection(), (last - 1,))
            self.assertEqual(controller.session.chords[last - 1], "G7")
            self.assertEqual(controller.session.get_chord_event_timing(last - 1), last_timing)
            self.assertIsNotNone(rows.bbox(last - 1))
            window.undo_btn.invoke()
            self.assertEqual(controller.session.chords[last], "G7")

            window.project_title_entry.delete(0, tk.END)
            window.project_title_entry.insert(0, "Draft")
            window.event_start_entry.delete(0, tk.END)
            window.event_start_entry.insert(0, "15:2:")
            view = rows.yview()[0]
            state_before_language = controller.session.state
            preference_path = Path(self.temp_dir) / "preferences.json"
            with patch.object(i18n, "settings_file", preference_path):
                window.language_menu.invoke(2)
                root.update()
                self.assertEqual(rows.yview()[0], view)
                self.assertEqual(rows.curselection(), (last - 1,))
                self.assertEqual(window.project_title_entry.get(), "Draft")
                self.assertEqual(window.event_start_entry.get(), "15:2:")
                self.assertIn(" Ticks", rows.get(last - 1))
                self.assertEqual(controller.session.state, state_before_language)
                window.language_menu.invoke(1)
                root.update()

            start_entry = window.event_start_entry
            duration_entry = window.event_duration_entry
            start_entry.focus_force()
            root.update()
            start_entry.event_generate("<Escape>")
            root.update()
            self.assertNotEqual(start_entry.get(), "15:2:")
            self.assertEqual(controller.session.state, state_before_language)
            start_entry.delete(0, tk.END)
            start_entry.insert(0, "1320")
            duration_entry.delete(0, tk.END)
            duration_entry.insert(0, "0")
            start_entry.event_generate("<Return>")
            root.update()
            errors.assert_called_once()
            self.assertEqual(errors.call_args.args[1], i18n.translate("event.duration.invalid"))
            self.assertEqual(root.focus_lastfor(), duration_entry)
            self.assertTrue(duration_entry.selection_present())
            self.assertEqual(start_entry.get(), "1320")
            self.assertEqual(controller.session.state, state_before_language)
            errors.reset_mock()
            duration_entry.delete(0, tk.END)
            duration_entry.insert(0, "240")
            duration_entry.event_generate("<Return>")
            root.update()
            self.assertEqual(controller.session.get_chord_event_timing(last - 1), (1320, 240))
            self.assertEqual(start_entry.get(), "1:3:360")
            self.assertIn("1:3:360 · 240 ticks", rows.get(last - 1))
            window.undo_btn.invoke()
            self.assertEqual(controller.session.state, state_before_language)

            event_index = last - 1
            original_start, original_duration = controller.session.get_chord_event_timing(event_index)
            original_count = rows.size()
            rows.focus_force()
            editor_modifier = "Command" if sys.platform == "darwin" else "Control"
            rows.event_generate(f"<{editor_modifier}-d>")
            root.update()
            self.assertEqual(rows.size(), original_count + 1)
            self.assertEqual(rows.curselection(), (event_index + 1,))
            self.assertEqual(
                controller.session.get_chord_event_timing(event_index + 1),
                (original_start + original_duration, original_duration),
            )
            window.chord_menu.invoke(1)
            self.assertEqual(rows.size(), original_count + 2)
            self.assertEqual(rows.curselection(), (event_index + 2,))
            self.assertEqual(root.focus_lastfor(), rows)
            window.undo_btn.invoke()
            window.undo_btn.invoke()
            self.assertEqual(controller.session.state, state_before_language)

            window.event_duration_entry.delete(0, tk.END)
            window.event_duration_entry.insert(0, "1")
            window.event_timing_btn.invoke()
            self.assertEqual(window.chord_menu.entrycget(1, "state"), tk.DISABLED)
            self.assertEqual(window.chord_menu.entrycget(0, "state"), tk.NORMAL)
            revision = controller.revision
            rows.event_generate(f"<{editor_modifier}-t>")
            root.update()
            self.assertEqual(controller.revision, revision)
            self.assertEqual(rows.size(), original_count)
            window.undo_btn.invoke()
            self.assertEqual(controller.session.state, state_before_language)

            prompt.return_value = False
            window.file_menu.invoke(0)
            prompt.reset_mock()
            prompt.return_value = None
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
            window.chord_entry.focus_force()
            root.update()
            window.file_menu.invoke(4)
            library = modal()
            library.geometry("760x500")
            root.update()
            search = next(widgets(library, tk.Entry))
            preview = next(widgets(library, tk.Text))
            evidence = next(widgets(library, ttk.Menubutton))
            menu = library.nametowidget(evidence.cget("menu"))

            def visible_labels():
                return [
                    label.cget("text") for label in widgets(library, tk.Label)
                    if label.winfo_ismapped()
                ]
            self.assertEqual(library.focus_lastfor(), search)
            search.event_generate("<Control-n>")
            root.update()
            prompt.assert_not_called()
            search.insert(0, "no-matching-example")
            self.assertIn(i18n.translate("library.no_results"), preview.get("1.0", tk.END))
            self.assertTrue(evidence.instate(["disabled"]))
            self.assertIsNone(menu.index(tk.END))
            search.delete(0, tk.END)
            search.insert(0, "jazz G7")
            self.assertIn("G7", preview.get("1.0", tk.END))
            root.update()
            self.assertEqual(
                visible_labels()[-7:],
                [
                    i18n.translate("library.detail.key", value="C"),
                    "Dm7", "ii^7", "G7", "V^7", "Cmaj7", "I^maj7",
                ],
            )
            preview.focus_force()
            preview.event_generate("<Next>")
            root.update()
            preview_offset = preview.yview()[0]
            self.assertGreater(preview_offset, 0.0)
            search.insert(tk.END, " omt-ii-v-i")
            root.update()
            self.assertEqual(preview.yview()[0], preview_offset)
            self.assertEqual(preview.cget("state"), tk.DISABLED)
            before_tab = preview.tk_focusNext()
            preview.event_generate("<Tab>")
            root.update()
            self.assertEqual(before_tab, evidence)
            self.assertEqual(library.focus_lastfor(), evidence)
            jazz = get_reviewed_progression("PROG-003")
            expected_links = list(dict.fromkeys(
                citation.url for approved in jazz.claims for citation in approved.claim.citations
            ))
            expected_links += list(dict.fromkeys(approved.evidence_url for approved in jazz.claims))
            before_browser = controller.session.state
            browser.assert_not_called()
            for index in range(menu.index(tk.END) + 1):
                if menu.type(index) == "command":
                    menu.invoke(index)
            self.assertEqual(
                [call.args[0] for call in browser.call_args_list], expected_links,
            )
            self.assertEqual(controller.session.state, before_browser)
            self.assertEqual(root.grab_current(), library)
            before_shift_tab = preview.tk_focusPrev()
            preview.focus_force()
            preview.event_generate("<Shift-Tab>")
            root.update()
            self.assertNotEqual(before_shift_tab, preview)
            self.assertEqual(library.focus_lastfor(), before_shift_tab)
            search.delete(0, tk.END)
            self.assertIn("PROG-003", preview.get("1.0", tk.END))
            search.insert(0, "Pop Four Chords")
            root.update()
            self.assertEqual(preview.yview()[0], 0.0)
            self.assertEqual(visible_labels()[-8:], ["C", "I", "G", "V", "Am", "vi", "F", "IV"])
            pop = get_reviewed_progression("PROG-001")
            first_pop_source = pop.claims[0].claim.citations[0]
            self.assertEqual(menu.entrycget(0, "label"), first_pop_source.title)
            menu.invoke(0)
            browser.assert_called_with(first_pop_source.url, new=2)
            search.insert(tk.END, " no-match")
            root.update()
            self.assertNotIn("Am", visible_labels())
            self.assertTrue(evidence.instate(["disabled"]))
            self.assertIsNone(menu.index(tk.END))
            search.delete(0, tk.END)
            search.insert(0, "jazz")
            button(library, "library.load").invoke()
            self.assertTrue(library.winfo_exists())
            self.assertEqual(controller.session.chords[0], "Dm7")
            prompt.return_value = False
            button(library, "library.load").invoke()
            self.assertFalse(library.winfo_exists())
            self.assertEqual(controller.session.chords, ["Dm7", "G7", "Cmaj7"])
            self.assertIn(
                i18n.translate("chord.degree", degree="ii7"),
                window.detail_text.get("1.0", tk.END),
            )
            window.file_menu.invoke(4)
            library = modal()
            search = next(widgets(library, tk.Entry))
            search.focus_force()
            search.event_generate("<Escape>")
            root.update()
            self.assertFalse(library.winfo_exists())
            self.assertIsNone(root.grab_current())
            self.assertEqual(root.focus_lastfor(), window.chord_entry)

            window.chord_entry.delete(0, tk.END)
            window.chord_entry.insert(0, "Dm")
            window.update_btn.invoke()
            before = tuple(controller.session.state.chord_event_timings)
            panel = window.next_chord_panel
            root.geometry("860x600")
            root.update()
            window.chord_listbox.focus_force()
            window.tools_menu.invoke(0)
            root.update()
            candidates = panel.candidates
            self.assertGreater(candidates.size(), 1)
            self.assertEqual(root.focus_lastfor(), candidates)
            self.assertEqual(candidates.curselection(), (0,))
            reference = controller.explore_next(0)[0]
            initial_comparison_state = controller.session.state
            detail = window.detail_text
            candidates.event_generate("<Tab>")
            root.update()
            panel.apply_button.event_generate("<Tab>")
            root.update()
            self.assertEqual(root.focus_lastfor(), panel.comparison_button)
            self.assertTrue(panel.comparison_button.winfo_ismapped())
            panel.comparison_button.invoke()
            root.update()
            self.assertEqual(root.focus_lastfor(), candidates)
            self.assertIn(i18n.translate("next_chord.compare.choose"), detail.get("1.0", tk.END))
            self.assertEqual(controller.session.state, initial_comparison_state)
            candidates.event_generate("<Down>")
            root.update()
            self.assertEqual(candidates.curselection(), (1,))
            selected = controller.explore_next(0)[1]
            before_language = controller.session.state
            preference_file = Path(self.temp_dir) / "preferences.json"
            with patch.object(i18n, "settings_file", preference_file):
                window.language_menu.invoke(2)
                root.update()
                self.assertEqual(candidates.curselection(), (1,))
                self.assertEqual(controller.session.state, before_language)
                self.assertIn(selected.candidate_symbol, candidates.get(1))
                localized_relation = i18n.translate(f"next_chord.relation.{selected.relation_type}")
                self.assertIn(localized_relation, candidates.get(1))
                detail = window.detail_text
                self.assertIn(i18n.translate("next_chord.original"), detail.get("1.0", tk.END))
                comparison = detail.get("1.0", tk.END)
                self.assertIn(i18n.translate("next_chord.compare.reference"), comparison)
                self.assertIn(i18n.translate("next_chord.compare.selected"), comparison)
                self.assertIn(reference.explanation, comparison)
                for item in (reference, selected):
                    self.assertIn(i18n.translate(f"next_chord.evidence.{item.evidence_kind}"), comparison)
                self.assertIn(selected.explanation, detail.get("1.0", tk.END))
                self.assertEqual(detail.cget("state"), tk.DISABLED)
                candidates.event_generate("<Shift-Tab>")
                root.update()
                self.assertEqual(root.focus_lastfor(), detail)
                detail.event_generate("<Tab>")
                root.update()
                self.assertEqual(root.focus_lastfor(), candidates)
                candidates.event_generate("<Tab>")
                root.update()
                self.assertEqual(root.focus_lastfor(), panel.apply_button)
                self.assertTrue(panel.apply_button.winfo_ismapped())
                panel.apply_button.event_generate("<Shift-Tab>")
                root.update()
                self.assertEqual(root.focus_lastfor(), candidates)
                window.language_menu.invoke(1)
            candidates.event_generate("<Return>")
            root.update()
            self.assertEqual(controller.session.chords[1], selected.candidate_symbol)
            self.assertEqual(window.chord_listbox.curselection(), (1,))
            self.assertEqual(root.focus_lastfor(), window.chord_listbox)
            self.assertEqual(candidates.size(), 0)
            self.assertEqual(str(panel.comparison_button.cget("state")), tk.DISABLED)
            detail.focus_set()
            root.update()
            detail.event_generate("<Control-z>")
            root.update()
            self.assertEqual(tuple(controller.session.state.chord_event_timings), before)
            window.redo_btn.invoke()

            active_style = controller.session.voice_leading_style
            before_comparison = controller.session.state
            window.voice_lab_btn.invoke()
            lab = modal()
            lab.geometry("720x490")
            root.update()
            for key in ("voice.lab.close", "voice.lab.apply_a", "voice.lab.apply_b"):
                self.assertTrue(button(lab, key).winfo_ismapped())
            for text in widgets(lab, tk.Text):
                self.assertEqual(str(text.cget("takefocus")), "1")
                rendered = text.get("1.0", tk.END)
                self.assertRegex(rendered, r"MIDI note range: [0-9]+–[0-9]+\.")
                self.assertIn(i18n.translate("voice.lab.transition.voices", steps="").rstrip(), rendered)
            nested_export = window._on_export_midi()
            self.assertEqual(modal(), nested_export.window)
            nested_export._close()
            nested_export._close()
            self.assertEqual(root.grab_current(), lab)
            rolls = list(widgets(lab, tk.Canvas))
            self.assertEqual(len(rolls), 2)
            self.assertTrue(all(roll.find_withtag("note") for roll in rolls))
            event_selector, zoom_selector, _, selector = widgets(lab, ttk.Combobox)
            self.assertEqual(event_selector.current(), window.chord_listbox.curselection()[0])
            first_highlights = [roll.coords("selected-event") for roll in rolls]
            self.assertTrue(all(coords for coords in first_highlights))
            self.assertTrue(all(roll.find_withtag("following-event") for roll in rolls))
            event_selector.current(3)
            event_selector.event_generate("<<ComboboxSelected>>")
            root.update()
            self.assertTrue(all(roll.coords("selected-event") for roll in rolls))
            self.assertTrue(all(
                roll.coords("selected-event")[0] > previous[0]
                for roll, previous in zip(rolls, first_highlights, strict=True)
            ))
            self.assertIn(controller.session.chords[3], event_selector.get())
            self.assertFalse(any(roll.find_withtag("following-event") for roll in rolls))
            self.assertTrue(all(
                i18n.translate("voice.lab.focus.last") in preview.get("1.0", tk.END)
                for preview in widgets(lab, tk.Text)
            ))

            def visible_ticks(roll):
                return [int(roll.itemcget(item, "text")) for item in roll.find_withtag("tick-label")]

            overview = visible_ticks(rolls[0])
            self.assertEqual(overview, visible_ticks(rolls[1]))
            zoom_selector.focus_force()
            for _ in range(2):
                zoom_selector.event_generate("<Right>")
            root.update()
            self.assertEqual(zoom_selector.get(), "4×")
            zoomed = visible_ticks(rolls[0])
            self.assertEqual(zoomed, visible_ticks(rolls[1]))
            self.assertGreater(zoomed[0], overview[0])
            self.assertEqual(zoomed[-1], overview[-1])
            self.assertTrue(all(roll.coords("selected-event") for roll in rolls))
            self.assertTrue(all(
                28 <= roll.coords(item)[0] <= roll.coords(item)[2] <= roll.winfo_width() - 10
                for roll in rolls for item in roll.find_withtag("note")
            ))

            event_selector.current(0)
            event_selector.event_generate("<<ComboboxSelected>>")
            root.update()
            first_zoomed = visible_ticks(rolls[0])
            self.assertEqual(first_zoomed, visible_ticks(rolls[1]))
            self.assertEqual(first_zoomed[0], overview[0])
            self.assertLess(first_zoomed[-1], overview[-1])
            self.assertEqual(controller.session.state, before_comparison)

            selector.current(1 if active_style.value != "STRICT_CLASSICAL" else 0)
            selector.event_generate("<<ComboboxSelected>>")
            root.update()
            self.assertEqual(controller.session.state, before_comparison)
            self.assertEqual(first_zoomed, visible_ticks(rolls[1]))
            zoom_selector.current(0)
            zoom_selector.event_generate("<<ComboboxSelected>>")
            root.update()
            self.assertTrue(all(visible_ticks(roll) == overview for roll in rolls))
            target_roll = rolls[1]
            note = target_roll.find_withtag("event:2")[0]
            x_start, y_note, x_end, _ = target_roll.coords(note)
            target_roll.event_generate("<Button-1>", x=round((x_start + x_end) / 2), y=round(y_note))
            root.update()
            self.assertEqual(event_selector.current(), 2)
            self.assertTrue(all(roll.coords("selected-event")[0] >= 28 for roll in rolls))
            self.assertTrue(all(roll.find_withtag("following-event") for roll in rolls))
            self.assertTrue(all(
                preview.get("1.0", tk.END).startswith(
                    i18n.translate("voice.lab.focus.event", number=3, chord=controller.session.chords[2])
                )
                for preview in widgets(lab, tk.Text)
            ))
            target_roll.event_generate("<Button-1>", x=1, y=1)
            root.update()
            self.assertEqual(event_selector.current(), 2)
            event_selector.focus_force()
            event_selector.event_generate("<Right>")
            root.update()
            self.assertEqual(event_selector.current(), 3)
            event_selector.event_generate("<Right>")
            event_selector.event_generate("<Left>")
            root.update()
            self.assertEqual(event_selector.current(), 2)
            self.assertEqual(lab.focus_lastfor(), event_selector)
            self.assertEqual(controller.session.state, before_comparison)
            button(lab, "voice.lab.apply_b").invoke()
            self.assertFalse(lab.winfo_exists())
            self.assertNotEqual(controller.session.voice_leading_style, active_style)
            window.undo_btn.focus_force()
            window.undo_btn.event_generate("<Control-z>")
            root.update()
            self.assertEqual(controller.session.voice_leading_style, active_style)
            window.redo_btn.invoke()

            controller.set_chord(1, "Dm")
            controller.set_chord_event_timing(0, 0, 20)
            controller.set_chord_event_timing(1, 12, 20)
            state_before_export = controller.session.state

            window.export_btn.invoke()
            export = modal()
            voicing_radios = {
                widget.cget("value"): widget
                for widget in widgets(export, tk.Radiobutton)
            }
            self.assertEqual(voicing_radios["CLOSE"].cget("state"), tk.NORMAL)
            self.assertEqual(voicing_radios["DROP2"].cget("state"), tk.DISABLED)
            self.assertEqual(voicing_radios["ROOTLESS"].cget("state"), tk.DISABLED)
            descriptions = [label.cget("text") for label in widgets(export, tk.Label)]
            self.assertTrue(any(
                i18n.translate("midi.options.voicing.unavailable", mode="DROP2", chord="Dm") in text
                for text in descriptions
            ))
            self.assertIn(i18n.translate("midi.options.overlap.none"), descriptions)
            def export_preview_text(tracks, duration):
                result = controller.midi_export_preview("CLOSE", duration)
                return i18n.translate(
                    "midi.options.preview.events", tracks=tracks, first=result.first_tick, end=result.end_tick,
                    chords=result.chord_notes, bass=result.bass_notes,
                    chord_low=result.chord_range[0], chord_high=result.chord_range[1],
                    bass_low=result.bass_range[0], bass_high=result.bass_range[1],
                )

            self.assertIn(export_preview_text(3, "FIXED_GAP"), descriptions)
            for key in ("midi.options.duration.percent_95", "midi.options.format.type0"):
                radio = next(
                    widget for widget in widgets(export, tk.Radiobutton)
                    if widget.cget("text") == i18n.translate(key)
                )
                radio.invoke()
            descriptions = [label.cget("text") for label in widgets(export, tk.Label)]
            self.assertIn(
                i18n.translate("midi.options.overlap.detected", count=5, tick=12),
                descriptions,
            )
            self.assertIn(export_preview_text(1, "PERCENT_95"), descriptions)
            self.assertEqual(controller.session.state, state_before_export)
            with patch(
                "app.ui.main_window.filedialog.asksaveasfilename", return_value="",
            ) as chooser:
                button(export, "midi.options.export").invoke()
            self.assertEqual(chooser.call_args.kwargs["initialfile"], "Jazz Two-Five-One.mid")
            self.assertNotIn("initialdir", chooser.call_args.kwargs)
            self.assertTrue(export.winfo_exists())
            target = Path(self.midi_path)
            target.write_bytes(b"previous MIDI data")
            with (
                patch("app.ui.main_window.filedialog.asksaveasfilename", return_value=self.midi_path),
                patch("src.steps.midi.smf.os.replace", side_effect=PermissionError(errno.EACCES, "locked")),
                self.assertLogs("app.ui.main_window", level="WARNING"),
            ):
                button(export, "midi.options.export").invoke()
            errors.assert_called_once()
            self.assertIn(i18n.translate("midi.export.error.permission", path=self.midi_path), errors.call_args.args)
            self.assertTrue(export.winfo_exists())
            self.assertEqual(target.read_bytes(), b"previous MIDI data")
            errors.reset_mock()
            with patch("app.ui.main_window.filedialog.asksaveasfilename", return_value=self.midi_path):
                button(export, "midi.options.export").invoke()
            self.assertFalse(export.winfo_exists())
            exported_bytes = target.read_bytes()
            midi = MidiFile.from_bytes(exported_bytes)
            self.assertEqual(len(midi.tracks), 1)

            window.export_btn.invoke()
            again = modal()
            with patch(
                "app.ui.main_window.filedialog.asksaveasfilename", return_value="",
            ) as chooser:
                button(again, "midi.options.export").invoke()
            self.assertEqual(chooser.call_args.kwargs["initialdir"], str(target.parent))
            self.assertTrue(again.winfo_exists())
            button(again, "midi.options.cancel").invoke()
            self.assertEqual(target.read_bytes(), exported_bytes)

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

            reopened.controller.save(path)
            future_data = json.loads(path.read_text(encoding="utf-8"))
            future_data["schema_version"] = "99.0.0"
            future_path = path.with_name("future.stepsproj")
            future_path.write_text(json.dumps(future_data), encoding="utf-8")
            damaged_bytes = bytes((255, 254, 253))
            path.write_bytes(damaged_bytes)

            with (
                patch("app.ui.main_window.filedialog.askopenfilename", return_value=str(path)),
                patch("app.ui.main_window.messagebox.showinfo") as recovery_notice,
            ):
                reopened.file_menu.invoke(1)
            session = reopened.controller.session
            backup = session.last_loaded_backup_path
            self.assertTrue(session.last_load_recovered_from_backup)
            self.assertIsNotNone(backup)
            recovery_notice.assert_called_once()
            self.assertIn(backup.name, recovery_notice.call_args.args[1])
            self.assertEqual(session.state, expected_state)
            self.assertEqual(path.read_bytes(), damaged_bytes)

            reopened.controller.set_chord(0, "Cm")
            dirty_state = session.state
            with (
                patch("app.ui.main_window.filedialog.askopenfilename", return_value=str(future_path)),
                self.assertLogs("app.ui.main_window", level="WARNING"),
            ):
                reopened.file_menu.invoke(1)
            self.assertEqual(
                errors.call_args.args[1],
                i18n.translate("project.file.error.schema", path=str(future_path)),
            )
            self.assertEqual(reopened._project_path, path)
            self.assertEqual(session.state, dirty_state)
            self.assertTrue(session.is_dirty)
            self.assertTrue(session.can_undo)
            self.assertEqual(session.last_loaded_backup_path, backup)
            self.assertFalse(callback_errors)


if __name__ == "__main__":
    unittest.main()

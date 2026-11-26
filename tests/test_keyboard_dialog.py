"""Real Tk tests for the keyboard dialog opened from the production main window.

Skipped (not passed) when Tk or a display is unavailable, unless
STEPS_REQUIRE_DESKTOP_TK=1 makes the missing display a failure.
"""

import ast
import os
import unittest
from pathlib import Path

from app.i18n import LocaleManager
from app.ui.keyboard_dialog import describe_workbench
from app.ui.keyboard_view import readable_text
from app.ui.session_controller import ProgressionSessionController
from src.steps.keyboard import KeyboardMode, KeyboardWorkbench, KeyState
from src.steps.progression.session import ProgressionSession

ROOT = Path(__file__).resolve().parents[1]


class TestKeyboardPresentationContracts(unittest.TestCase):
    def test_view_module_does_not_compute_music(self):
        tree = ast.parse((ROOT / "app" / "ui" / "keyboard_view.py").read_text(encoding="utf-8"))
        imported = {node.module for node in ast.walk(tree) if isinstance(node, ast.ImportFrom) and node.module}
        music = {name for name in imported if name.startswith("src.steps")}
        self.assertEqual(music, {"src.steps.keyboard.model", "src.steps.keyboard.state"})

    def test_button_labels_fit_the_glide_button_budget(self):
        from app.ui.layout_policy import BUTTON_TEXT_MAX_CHARS
        keys = (
            "keyboard.previous", "keyboard.next", "keyboard.inversion.down", "keyboard.inversion.up",
            "keyboard.octave.down", "keyboard.octave.up", "keyboard.fit", "keyboard.clear",
            "keyboard.add_to_progression", "keyboard.practice.check", "keyboard.practice.solution",
            "keyboard.practice.next", "keyboard.close",
        )
        for language in ("en", "de"):
            t = LocaleManager(preference=language).translate
            for key in keys:
                with self.subTest(language=language, key=key):
                    self.assertLessEqual(len(t(key)), BUTTON_TEXT_MAX_CHARS)

    def test_readable_text_picks_contrasting_colour(self):
        self.assertEqual(readable_text("#FFFFFF"), "#000000")
        self.assertEqual(readable_text("#000000"), "#FFFFFF")
        self.assertEqual(readable_text("#22252B"), "#FFFFFF")

    def test_description_is_localized_and_marks_preview_and_pilot(self):
        controller = ProgressionSessionController(ProgressionSession(["C/E", "G7"], key_root="C"))
        workbench = KeyboardWorkbench(lambda: controller.session)
        for language in ("en", "de"):
            with self.subTest(language=language):
                t = LocaleManager(preference=language).translate
                workbench.mode = KeyboardMode.PROGRESSION
                text = describe_workbench(workbench, t)
                self.assertIn(t("keyboard.info.preview_only"), text)
                self.assertIn(t("keyboard.inversion.FIRST_INVERSION"), text)
                workbench.mode = KeyboardMode.PRACTICE
                self.assertIn(t("keyboard.practice.pilot_status"), describe_workbench(workbench, t))
                workbench.mode = KeyboardMode.FREE_INPUT
                workbench.input.set_selected([60, 64, 67, 69])
                text = describe_workbench(workbench, t)
                self.assertIn(t("keyboard.recognition.AMBIGUOUS"), text)
                self.assertIn("C6", text)
                self.assertIn("Am7/C", text)
                workbench.input.clear_selected()

    def test_description_uses_german_note_names_after_notation_switch(self):
        controller = ProgressionSessionController(ProgressionSession(["G7"], key_root="C"))
        controller.set_notation_convention("DE")
        workbench = KeyboardWorkbench(lambda: controller.session)
        text = describe_workbench(workbench, LocaleManager(preference="en").translate)
        self.assertIn("H (3)", text)  # B natural is H in German notation, independent of UI language


class TestKeyboardDialogTk(unittest.TestCase):
    def setUp(self):
        require_tk = os.environ.get("STEPS_REQUIRE_DESKTOP_TK") == "1"
        try:
            import tkinter as tk
            from app.ui.main_window import StepsMainWindow
        except ImportError as exc:
            if require_tk:
                self.fail(f"Tk is required: {exc}")
            self.skipTest("tkinter not available")
        try:
            self.root = tk.Tk()
        except tk.TclError as exc:
            if require_tk:
                self.fail(f"Tk could not initialize: {exc}")
            self.skipTest("No Tk graphics display")
        self.tk = tk
        self.errors = []
        self.root.report_callback_exception = lambda *error: self.errors.append(error)
        self.addCleanup(self._destroy)
        self.i18n = LocaleManager(preference="en")
        self.window = StepsMainWindow(self.root, locale_manager=self.i18n)
        self.controller = self.window.controller
        self.root.update()

    def _destroy(self):
        try:
            self.root.destroy()
        except self.tk.TclError:
            pass

    def test_menu_and_sidebar_open_the_keyboard_and_close_cleanly(self):
        from app.ui.keyboard_dialog import KeyboardDialog
        opened = []
        original = KeyboardDialog.__init__

        def tracking_init(dialog, *args, **kwargs):
            original(dialog, *args, **kwargs)
            opened.append(dialog)

        KeyboardDialog.__init__ = tracking_init
        self.addCleanup(setattr, KeyboardDialog, "__init__", original)
        listeners = len(self.controller._listeners)
        for _ in range(3):  # repeated open/close
            self.window.tools_menu.invoke(3)
            self.root.update()
            dialog = opened[-1]
            self.assertEqual(self.root.grab_current(), dialog.window)
            self.assertEqual(len(self.controller._listeners), listeners + 1)
            dialog._close()
            self.root.update()
            self.assertFalse(dialog.window.winfo_exists())
            self.assertEqual(len(self.controller._listeners), listeners)
        self.assertEqual(self.i18n.translate("keyboard.open"), self.window.tools_menu.entrycget(3, "label"))
        self.assertIn("keyboard", self.window._rail_button_map)
        self.window._rail_button_map["keyboard"].invoke()
        self.root.update()
        opened[-1]._close()
        self.assertEqual(self.errors, [])

    def make_dialog(self, chords=("C", "G/B", "Am", "F")):
        from app.ui.keyboard_dialog import KeyboardDialog
        self.controller.new_project()
        for index, symbol in enumerate(chords):
            if index < len(self.controller.session.chords):
                self.controller.set_chord(index, symbol)
            else:
                self.controller.add_chord(symbol)
        self.window._refresh_all(selected_index=1)
        self.root.update()
        dialog = KeyboardDialog(
            self.root, self.controller, self.i18n, self.window.theme,
            on_project_change=lambda index: self.window._refresh_all(selected_index=index),
            selected_index=self.window._selected_chord_index(),
        )
        self.addCleanup(lambda: dialog.window.winfo_exists() and dialog._close())
        self.root.update()
        return dialog

    def click(self, dialog, midi):
        x, y = dialog.keyboard.key_center(midi)
        self.assertEqual(dialog.keyboard.key_at(x, y), midi)
        dialog.keyboard.event_generate("<ButtonPress-1>", x=x, y=y)
        dialog.keyboard.event_generate("<ButtonRelease-1>", x=x, y=y)
        self.root.update()

    def test_progression_preview_draws_selected_voicing_with_root_and_bass(self):
        dialog = self.make_dialog()
        self.assertEqual(dialog.workbench.selected_index, 1)  # follows the main-window selection
        model = dialog.keyboard.model
        keys_in_view = len(model.viewport.keys())
        self.assertEqual(len(dialog.keyboard.find_withtag("key")), keys_in_view)
        info = dialog.workbench.chord_info()
        bass = model.visual(info.voicing.bass.midi)
        self.assertIn("B", bass.badges)
        self.assertNotIn(KeyState.CHORD_ROOT, bass.states)  # G/B: bass is the third
        marker = dialog.keyboard.item_ids(info.voicing.bass.midi)["marker"]
        self.assertNotEqual(dialog.keyboard.itemcget(marker, "fill"), "")
        text = dialog.info_text.get("1.0", "end")
        self.assertIn("G/B", text)
        self.assertIn(self.i18n.translate("keyboard.inversion.FIRST_INVERSION"), text)
        dialog.next_btn.invoke()
        self.root.update()
        self.assertEqual(dialog.workbench.selected_index, 2)
        self.assertEqual(self.errors, [])

    def test_preview_controls_do_not_mutate_project(self):
        dialog = self.make_dialog()
        state = repr(self.controller.session.state)
        revision = self.controller.revision
        dialog.voicing_selector.current(1)
        dialog._on_voicing()
        dialog.rotate_up_btn.invoke()
        dialog._vars["scale"].set(True)
        dialog._vars["compare"].set(True)
        dialog._on_toggles()
        dialog.octave_up_btn.invoke()
        dialog.fit_btn.invoke()
        self.click(dialog, 60)
        self.root.update()
        self.assertEqual(repr(self.controller.session.state), state)
        self.assertEqual(self.controller.revision, revision)
        self.assertEqual(self.errors, [])

    def test_free_input_white_and_black_keys_recognition_and_undoable_insert(self):
        dialog = self.make_dialog()
        dialog.mode_selector.current(1)
        dialog._on_mode()
        dialog.workbench.viewport = dialog.workbench.viewport.__class__(48, 84)
        dialog.workbench.auto_fit = False
        dialog.refresh()
        self.root.update()
        for midi in (58, 62, 65):  # Bb (black), D, F (white)
            self.click(dialog, midi)
        self.assertEqual(dialog.workbench.input.selected, {58, 62, 65})
        self.assertEqual(dialog.workbench.input.sounding, ())  # released after click
        self.assertIn(KeyState.SELECTED, dialog.keyboard.model.visual(58).states)
        self.assertEqual(dialog.candidate_selector.get(), "Bb")
        chords_before = list(self.controller.session.chords)
        dialog.add_btn.invoke()
        self.root.update()
        self.assertEqual(self.controller.session.chords, chords_before + ["Bb"])
        self.assertEqual(self.window.chord_listbox.size(), len(chords_before) + 1)
        self.controller.undo()
        self.assertEqual(self.controller.session.chords, chords_before)
        self.click(dialog, 58)  # toggle off
        self.assertNotIn(58, dialog.workbench.input.selected)
        dialog.clear_btn.invoke()
        self.assertEqual(dialog.workbench.input.selected, set())
        self.assertEqual(self.errors, [])

    def test_computer_keyboard_input_repeat_release_and_focus_loss(self):
        dialog = self.make_dialog()
        dialog.mode_selector.current(1)
        dialog._on_mode()
        canvas = dialog.keyboard
        canvas.focus_force()
        self.root.update()
        base = dialog.computer_key_note("a")
        self.assertIsNotNone(base)
        self.assertEqual(base % 12, 0)
        self.assertEqual(dialog.computer_key_note("w"), base + 1)
        self.assertEqual(dialog.computer_key_note("z"), dialog.computer_key_note("y"))
        self.assertIsNone(dialog.computer_key_note("q"))
        canvas.event_generate("<KeyPress-a>")
        canvas.event_generate("<KeyPress-a>")  # auto-repeat must not toggle twice
        self.root.update()
        self.assertIn(base, dialog.workbench.input.selected)
        self.assertIn(base, dialog.workbench.input.sounding)
        canvas.event_generate("<KeyRelease-a>")
        self.root.update()
        self.assertNotIn(base, dialog.workbench.input.sounding)
        canvas.event_generate("<KeyPress-s>")
        self.root.update()
        held = dialog.computer_key_note("s")
        dialog._shift(12)  # viewport moves while the key is held
        canvas.event_generate("<KeyRelease-s>")
        self.root.update()
        self.assertNotIn(held, dialog.workbench.input.sounding)  # the pressed note is released
        canvas.event_generate("<KeyPress-d>")
        self.root.update()
        dialog._on_focus_out(None)
        self.assertEqual(dialog.workbench.input.sounding, ())
        self.assertEqual(dialog._held_computer_keys, {})
        self.assertEqual(self.errors, [])

    def test_practice_pilot_check_and_solution(self):
        dialog = self.make_dialog()
        state = repr(self.controller.session.state)
        dialog.mode_selector.current(2)
        dialog._on_mode()
        dialog.exercise_selector.current(1)  # C major triad
        dialog._on_exercise()
        dialog.workbench.viewport = dialog.workbench.viewport.__class__(48, 84)
        dialog.workbench.auto_fit = False
        dialog.refresh()
        self.root.update()
        for midi in (60, 64, 67):
            self.click(dialog, midi)
        dialog.check_btn.invoke()
        self.root.update()
        self.assertTrue(dialog.workbench.feedback.is_correct)
        self.assertIn(self.i18n.translate("practice.feedback.correct"), dialog.info_text.get("1.0", "end"))
        self.assertIn(self.i18n.translate("keyboard.practice.pilot_status"), dialog.info_text.get("1.0", "end"))
        dialog.next_exercise_btn.invoke()
        dialog.solution_btn.invoke()
        self.root.update()
        self.assertTrue(any(KeyState.PRACTICE_MISSING in k.states for k in dialog.keyboard.model.keys))
        self.assertEqual(repr(self.controller.session.state), state)
        self.assertEqual(self.errors, [])

    def test_resize_relayouts_only_on_real_size_change_and_repaint_reuses_items(self):
        dialog = self.make_dialog()
        canvas = dialog.keyboard
        self.root.update()
        layouts = canvas.layout_count
        items = canvas.find_all()
        for _ in range(5):
            dialog.refresh()
        self.root.update()
        self.assertEqual(canvas.layout_count, layouts)  # note changes repaint, do not rebuild
        self.assertEqual(canvas.find_all(), items)
        dialog.window.geometry("1200x700")
        self.root.update()
        self.assertGreaterEqual(canvas.layout_count, layouts)
        settled = canvas.layout_count
        for _ in range(3):
            self.root.update()
        self.assertEqual(canvas.layout_count, settled)  # no Configure feedback loop
        self.assertEqual(self.errors, [])

    def test_controller_changes_refresh_open_dialog(self):
        dialog = self.make_dialog()
        self.controller.transpose(2)
        self.root.update()
        self.assertIn("A/C#", dialog.info_text.get("1.0", "end"))
        self.controller.set_notation_convention("DE")
        self.root.update()
        self.assertIn("A/Cis", dialog.info_text.get("1.0", "end"))
        self.assertEqual(self.errors, [])

    def test_dialog_builds_under_every_theme(self):
        from app.ui.keyboard_dialog import KeyboardDialog
        for mode in ("dark", "light", "contrast-dark", "contrast-light"):
            with self.subTest(theme=mode):
                self.window.apply_theme(mode)
                self.root.update()
                dialog = KeyboardDialog(self.root, self.controller, self.i18n, self.window.theme,
                                        on_project_change=lambda index: None)
                self.root.update()
                self.assertTrue(dialog.keyboard.find_withtag("key"))
                dialog._close()
        self.assertEqual(self.errors, [])


if __name__ == "__main__":
    unittest.main()

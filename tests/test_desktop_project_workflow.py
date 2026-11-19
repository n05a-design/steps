"""Headless tests for the desktop project's save/open interaction."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.i18n import LocaleManager
from app.ui.session_controller import ProgressionSessionController

try:
    from app.ui.main_window import StepsMainWindow
except ImportError:
    StepsMainWindow = None

from src.steps.storage import CorruptedProjectError, StorageError
from src.steps.progression.session import ProgressionSession


class FakeRoot:
    def __init__(self):
        self.window_title = ""
        self.destroyed = False

    def title(self, value):
        self.window_title = value

    def destroy(self):
        self.destroyed = True


class FakeSession:
    def __init__(self, is_dirty=False):
        self.is_dirty = is_dirty
        self.key_root = "C"
        self.is_minor = False
        self.bpm = 120.0
        self.time_signature = (4, 4)
        self.convention = "INT"
        self.voice_leading_style = SimpleNamespace(value="CONTEMPORARY_POP")
        self.state = SimpleNamespace(
            ppq=480,
            title="My Progression",
            chords=["C", "G", "Am", "F"],
        )
        self.last_load_recovered_from_backup = False
        self.last_load_migrations = ()


class FakeController:
    def __init__(self, is_dirty=False):
        self.session = FakeSession(is_dirty)
        self.saved_paths = []
        self.loaded_paths = []
        self.exported_paths = []
        self.new_project_calls = 0
        self.save_error = None
        self.load_error = None
        self.export_error = None
        self.voice_style_calls = []
        self.reviewed_calls = []

    def get_state_summary(self):
        return {"title": "My Progression"}

    def get_view_model(self):
        return {}

    def save(self, path):
        if self.save_error:
            raise self.save_error
        saved_path = Path(path)
        self.saved_paths.append(saved_path)
        self.session.is_dirty = False
        return saved_path

    def load(self, path):
        if self.load_error:
            raise self.load_error
        self.loaded_paths.append(Path(path))
        self.session.is_dirty = False

    def new_project(self):
        self.new_project_calls += 1
        self.session = FakeSession(is_dirty=False)

    def new_reviewed_project(self, reviewed):
        self.reviewed_calls.append(reviewed)
        progression = reviewed.progression
        self.session = FakeSession(is_dirty=True)
        self.session.state.title = progression.name
        self.session.state.chords = progression.chords_str.replace(" ", "").split("-")
        self.session.key_root = progression.default_key.removesuffix("m")
        self.session.is_minor = progression.default_key.endswith("m")

    def set_notation_convention(self, convention):
        self.session.convention = convention
        if convention == "DE":
            self.session.key_root = "H" if self.session.key_root == "B" else self.session.key_root
        return True

    def set_voice_leading_style(self, style):
        self.voice_style_calls.append(style)
        self.session.voice_leading_style = SimpleNamespace(value=str(style).upper())

    def export_midi(self, path):
        if self.export_error:
            raise self.export_error
        output_path = Path(path)
        self.exported_paths.append(output_path)
        return output_path


@unittest.skipIf(StepsMainWindow is None, "tkinter is not available")
class TestDesktopProjectWorkflow(unittest.TestCase):
    def setUp(self):
        self.window = StepsMainWindow.__new__(StepsMainWindow)
        self.window.root = FakeRoot()
        self.window.controller = FakeController()
        self.window.i18n = LocaleManager(preference="en")
        self.window._project_path = None
        self.window._refresh_all = Mock()
        self.window.detail_text = Mock()
        self.window.project_title_entry = Mock()
        self.window.key_entry = Mock()
        self.window.mode_var = Mock()
        self.window.tempo_entry = Mock()
        self.window.meter_entry = Mock()
        self.window.event_start_entry = Mock()
        self.window.event_duration_entry = Mock()
        self.window.event_start_lbl = Mock()
        self.window.event_duration_lbl = Mock()
        self.window._load_context_controls = Mock()

    def test_window_icon_failure_is_logged_without_blocking_startup(self):
        root = Mock()
        with (
            patch(
                "app.ui.main_window.apply_window_icon",
                side_effect=OSError("missing icon"),
            ) as apply_icon,
            patch.object(StepsMainWindow, "_init_file_menu") as init_file_menu,
            patch.object(StepsMainWindow, "_init_ui") as init_ui,
            patch.object(StepsMainWindow, "_localize_widgets") as localize_widgets,
            patch.object(StepsMainWindow, "_refresh_all") as refresh_all,
        ):
            with self.assertLogs("app.ui.main_window", level="ERROR") as logged:
                window = StepsMainWindow(
                    root,
                    controller=FakeController(),
                    locale_manager=LocaleManager(preference="en"),
                )

        apply_icon.assert_called_once_with(root)
        init_file_menu.assert_called_once_with()
        init_ui.assert_called_once_with()
        localize_widgets.assert_called_once_with()
        refresh_all.assert_called_once_with()
        self.assertIn("Could not apply the STEPS window icon", logged.output[0])
        self.assertIs(window.root, root)

    def test_save_shortcut_delegates_to_save_and_stops_event(self):
        self.window._on_save_project = Mock()

        result = self.window._on_save_shortcut(SimpleNamespace())

        self.assertEqual(result, "break")
        self.window._on_save_project.assert_called_once_with()

    def test_new_from_reviewed_example_replaces_project_and_clears_path(self):
        reviewed = SimpleNamespace(
            progression=SimpleNamespace(
                prog_id="PROG-001",
                name="Pop Four Chords",
                default_key="C",
                chords_str="C - G - Am - F",
            )
        )
        self.window._project_path = Path("/tmp/old.stepsproj")

        with patch(
            "app.ui.main_window.get_reviewed_progression",
            return_value=reviewed,
        ):
            self.assertTrue(self.window._on_new_from_example("PROG-001"))

        self.assertIsNone(self.window._project_path)
        self.assertEqual(
            self.window.controller.session.state.chords,
            ["C", "G", "Am", "F"],
        )
        self.assertEqual(self.window.controller.reviewed_calls, [reviewed])
        self.window._load_context_controls.assert_called_once_with()
        self.window._refresh_all.assert_called_once_with()

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=False)
    def test_new_from_reviewed_example_confirms_before_replacing_dirty_project(self, prompt):
        reviewed = SimpleNamespace(
            progression=SimpleNamespace(
                prog_id="PROG-003",
                name="Jazz Two-Five-One",
                default_key="C",
                chords_str="Dm7 - G7 - Cmaj7",
            )
        )
        self.window.controller.session.is_dirty = True

        with patch(
            "app.ui.main_window.get_reviewed_progression",
            return_value=reviewed,
        ):
            self.assertTrue(self.window._on_new_from_example("PROG-003"))

        prompt.assert_called_once()
        self.assertEqual(len(self.window.controller.reviewed_calls), 1)

    def test_new_from_reviewed_example_cancel_keeps_current_project(self):
        self.window._project_path = Path("/tmp/current.stepsproj")
        self.window.controller.session.is_dirty = True

        with patch(
            "app.ui.main_window.messagebox.askyesnocancel",
            return_value=None,
        ):
            self.assertFalse(self.window._on_new_from_example("PROG-001"))

        self.assertEqual(self.window._project_path, Path("/tmp/current.stepsproj"))
        self.assertEqual(self.window.controller.reviewed_calls, [])

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/new.stepsproj")
    def test_save_as_updates_current_path_and_window_title(self, choose_path):
        self.window.controller.session.is_dirty = True

        self.assertTrue(self.window._on_save_project_as())

        self.assertEqual(self.window.controller.saved_paths, [Path("/tmp/new.stepsproj")])
        self.assertEqual(self.window._project_path, Path("/tmp/new.stepsproj"))
        self.assertEqual(self.window.root.window_title, "new.stepsproj — STEPS")

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/new.stepsproj")
    def test_save_as_uses_portable_default_filename(self, choose_path):
        cases = (
            ("Bad:Name?*", "Bad_Name__.stepsproj"),
            ("CON", "_CON.stepsproj"),
            ("...", "progression.stepsproj"),
        )
        for title, expected in cases:
            with self.subTest(title=title):
                self.window.controller.get_state_summary = Mock(return_value={"title": title})

                self.assertTrue(self.window._on_save_project_as())

                self.assertEqual(choose_path.call_args.kwargs["initialfile"], expected)

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="")
    def test_cancel_save_as_does_not_mark_session_clean(self, choose_path):
        self.window.controller.session.is_dirty = True

        self.assertFalse(self.window._on_save_project_as())

        self.assertTrue(self.window.controller.session.is_dirty)
        self.assertEqual(self.window.controller.saved_paths, [])

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=False)
    def test_new_project_discards_and_resets_session(self, prompt):
        self.window.controller.session.is_dirty = True
        self.window._project_path = Path("/tmp/old.stepsproj")

        self.assertTrue(self.window._on_new_project())

        self.assertIsNone(self.window._project_path)
        self.assertEqual(self.window.controller.new_project_calls, 1)
        self.assertEqual(
            self.window.controller.session.state.chords,
            ["C", "G", "Am", "F"],
        )
        self.window._refresh_all.assert_called_once_with()

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=True)
    def test_new_project_saves_current_file_before_reset(self, prompt):
        old_path = Path("/tmp/current.stepsproj")
        self.window.controller.session.is_dirty = True
        self.window._project_path = old_path

        self.assertTrue(self.window._on_new_project())

        self.assertEqual(self.window.controller.saved_paths, [old_path])
        self.assertEqual(self.window.controller.new_project_calls, 1)
        self.assertIsNone(self.window._project_path)
        self.assertFalse(self.window.controller.session.is_dirty)
        self.window._refresh_all.assert_called_once_with()

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="")
    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=True)
    def test_cancel_save_as_prevents_new_project(self, prompt, choose_path):
        self.window.controller.session.is_dirty = True

        self.assertFalse(self.window._on_new_project())

        self.assertTrue(self.window.controller.session.is_dirty)
        self.assertEqual(self.window.controller.saved_paths, [])
        self.assertEqual(self.window.controller.new_project_calls, 0)
        self.assertIsNone(self.window._project_path)
        self.window._refresh_all.assert_not_called()

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=None)
    def test_cancel_unsaved_prompt_prevents_new_project(self, prompt):
        self.window.controller.session.is_dirty = True
        old_path = Path("/tmp/old.stepsproj")
        self.window._project_path = old_path

        self.assertFalse(self.window._on_new_project())

        self.assertEqual(self.window.controller.new_project_calls, 0)
        self.assertEqual(self.window._project_path, old_path)
        self.window._refresh_all.assert_not_called()

    @patch("app.ui.main_window.messagebox.askyesno", return_value=True)
    def test_explicit_notation_change_converts_session_and_refreshes(self, prompt):
        convention = SimpleNamespace(value="INT")
        def get_convention(): return convention.value
        def set_convention(value): convention.value = value
        self.window.notation_var = SimpleNamespace(get=get_convention, set=set_convention)

        changed = getattr(self.window.controller.session, "convention", "INT")
        self.window.controller.session.convention = "INT"
        convention.value = "DE"

        self.window._on_notation_change()

        self.assertEqual(convention.value, "DE")
        self.window._refresh_all.assert_called_once_with(preserve_selection=True)

    def test_voice_leading_style_change_updates_controller_and_refreshes(self):
        self.window.voice_style_var = SimpleNamespace(
            get=lambda: "CONTEMPORARY_POP",
            set=Mock(),
        )
        self.window.voice_style_menu = {
            "menu": Mock(),
        }
        self.window._localize_voice_style_menu = Mock()

        self.window._on_voice_style_change("STRICT_CLASSICAL")

        self.assertEqual(
            self.window.controller.voice_style_calls,
            ["STRICT_CLASSICAL"],
        )
        self.window._refresh_all.assert_called_once_with(preserve_selection=True)

    def test_chord_details_include_beginner_voicing_data(self):
        self.window.controller = ProgressionSessionController(ProgressionSession())
        self.window.detail_text = Mock()

        self.window._display_chord_details("C")

        rendered = self.window.detail_text.insert.call_args.args[1]
        self.assertIn("BEGINNER KEYBOARD VOICINGS:", rendered)
        self.assertIn("C:", rendered)
        self.assertIn("Smoothness", rendered)

    def test_beginner_view_model_failure_is_logged_without_hiding_chord_details(self):
        self.window.controller.get_view_model = Mock(
            return_value={"beginner_voicings": {"smoothness_score": 0.9}}
        )

        with self.assertLogs("app.ui.main_window", level="ERROR") as logged:
            self.window._display_chord_details("C")

        self.assertIn("optional beginner voicing details", logged.output[0])
        rendered = self.window.detail_text.insert.call_args.args[1]
        self.assertIn(
            self.window.i18n.translate("chord.analysis.title", chord="C"),
            rendered,
        )

    def test_next_chord_explore_apply_undo_redo(self):
        self.window.controller = ProgressionSessionController(
            ProgressionSession(initial_chords=["C", "G", "Am", "F"], key_root="C")
        )
        self.window._next_recommendations = []
        self.window.chord_listbox = Mock()
        self.window.chord_listbox.curselection.return_value = (1,)
        self.window.next_candidates_list = Mock()
        self.window.next_candidates_list.curselection.return_value = (0,)
        self.window.apply_next_btn = Mock()
        self.window.detail_text = Mock()

        self.window._on_explore_next()
        recommendations = self.window._next_recommendations
        self.assertTrue(recommendations)
        candidate_index = next(
            index
            for index, recommendation in enumerate(recommendations)
            if recommendation.candidate_symbol == "C"
        )
        self.window.next_candidates_list.curselection.return_value = (candidate_index,)

        self.window._on_apply_next_recommendation()

        self.assertEqual(
            self.window.controller.session.chords,
            ["C", "G", "C", "Am", "F"],
        )
        self.window.controller.undo()
        self.assertEqual(
            self.window.controller.session.chords,
            ["C", "G", "Am", "F"],
        )
        self.window.controller.redo()
        self.assertEqual(
            self.window.controller.session.chords,
            ["C", "G", "C", "Am", "F"],
        )

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/fail.stepsproj")
    @patch("app.ui.main_window.messagebox.showerror")
    def test_save_error_is_visible_and_keeps_session_dirty(self, show_error, choose_path):
        self.window.controller.session.is_dirty = True
        self.window.controller.save_error = StorageError("disk full")

        self.assertFalse(self.window._on_save_project_as())

        self.assertTrue(self.window.controller.session.is_dirty)
        self.assertIsNone(self.window._project_path)
        show_error.assert_called_once()

    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/source.stepsproj")
    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=None)
    def test_cancel_unsaved_prompt_prevents_open(self, prompt, choose_path):
        self.window.controller.session.is_dirty = True

        self.assertFalse(self.window._on_open_project())

        self.assertEqual(self.window.controller.loaded_paths, [])
        self.window._refresh_all.assert_not_called()

    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/source.stepsproj")
    def test_open_loads_project_and_refreshes_view(self, choose_path):
        self.assertTrue(self.window._on_open_project())

        self.assertEqual(self.window.controller.loaded_paths, [Path("/tmp/source.stepsproj")])
        self.assertEqual(self.window._project_path, Path("/tmp/source.stepsproj"))
        self.window._refresh_all.assert_called_once_with()

    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/recovered.stepsproj")
    @patch("app.ui.main_window.messagebox.showinfo")
    def test_open_recovered_project_shows_localized_notice(self, show_info, choose_path):
        self.window.controller.session.last_load_recovered_from_backup = True

        self.assertTrue(self.window._on_open_project())

        show_info.assert_called_once()
        self.assertEqual(show_info.call_args.args[0], "Project recovered")

    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/legacy.stepsproj")
    @patch("app.ui.main_window.messagebox.showinfo")
    def test_open_migrated_project_shows_migration_notice(self, show_info, choose_path):
        self.window.controller.session.last_load_migrations = (
            "MIG-001 0.x-to-1.0.0",
            "MIG-004 add-notation-convention",
        )

        self.assertTrue(self.window._on_open_project())

        show_info.assert_called_once()
        self.assertEqual(show_info.call_args.args[0], "Project format updated")
        self.assertIn("MIG-001 0.x-to-1.0.0", show_info.call_args.args[1])

    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/broken.stepsproj")
    @patch("app.ui.main_window.messagebox.showerror")
    def test_failed_open_reports_error_and_keeps_current_path(self, show_error, choose_path):
        old_path = Path("/tmp/current.stepsproj")
        self.window._project_path = old_path
        self.window.controller.load_error = CorruptedProjectError("invalid project")

        self.assertFalse(self.window._on_open_project())

        self.assertEqual(self.window._project_path, old_path)
        self.assertEqual(self.window.controller.loaded_paths, [])
        show_error.assert_called_once()
        self.window._refresh_all.assert_not_called()

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=False)
    def test_close_can_discard_changes(self, prompt):
        self.window.controller.session.is_dirty = True

        self.window._on_close()

        self.assertTrue(self.window.root.destroyed)
        self.assertEqual(self.window.controller.saved_paths, [])

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/saved.stepsproj")
    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/source.stepsproj")
    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=True)
    def test_open_saves_dirty_session_before_loading(self, prompt, choose_open, choose_save):
        self.window.controller.session.is_dirty = True

        self.assertTrue(self.window._on_open_project())

        self.assertEqual(self.window.controller.saved_paths, [Path("/tmp/saved.stepsproj")])
        self.assertEqual(self.window.controller.loaded_paths, [Path("/tmp/source.stepsproj")])

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/fail-close.stepsproj")
    @patch("app.ui.main_window.messagebox.showerror")
    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=True)
    def test_close_save_error_keeps_window_and_dirty_session(
        self, prompt, show_error, choose_path
    ):
        self.window.controller.session.is_dirty = True
        self.window.controller.save_error = StorageError("disk full")

        self.window._on_close()

        self.assertFalse(self.window.root.destroyed)
        self.assertTrue(self.window.controller.session.is_dirty)
        show_error.assert_called_once()

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/fail-open.stepsproj")
    @patch("app.ui.main_window.messagebox.showerror")
    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=True)
    @patch("app.ui.main_window.filedialog.askopenfilename", return_value="/tmp/source.stepsproj")
    def test_open_save_error_prevents_loading(
        self, choose_open, prompt, show_error, choose_save
    ):
        self.window.controller.session.is_dirty = True
        self.window.controller.save_error = StorageError("disk full")

        self.assertFalse(self.window._on_open_project())

        self.assertTrue(self.window.controller.session.is_dirty)
        self.assertEqual(self.window.controller.loaded_paths, [])
        show_error.assert_called_once()
        self.window._refresh_all.assert_not_called()

    def test_dominant_chord_suggests_only_supported_scales(self):
        from src.steps.theory.scale import construct_scale

        with patch(
            "src.steps.theory.scale.construct_scale",
            wraps=construct_scale,
        ) as build_scale:
            self.window._display_chord_details("G7")

        self.assertEqual(
            [call.args[1] for call in build_scale.call_args_list],
            ["MIXOLYDIAN"],
        )
        details = self.window.detail_text.insert.call_args.args[1]
        self.assertIn("MIXOLYDIAN", details)
        self.assertNotIn("ALTERED", details)

    @patch(
        "src.steps.theory.scale.construct_scale",
        side_effect=RuntimeError("scale calculation failed"),
    )
    def test_scale_analysis_failure_is_visible(self, build_scale):
        self.window._display_chord_details("G7")

        build_scale.assert_called_once()
        details = self.window.detail_text.insert.call_args.args[1]
        self.assertIn("scale calculation failed", details)

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="")
    def test_cancel_midi_export_does_not_call_controller(self, choose_path):
        self.window._on_export_midi()

        self.assertEqual(self.window.controller.exported_paths, [])
        self.window.detail_text.insert.assert_not_called()

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/output.mid")
    def test_midi_export_uses_selected_path_and_confirms_success(self, choose_path):
        self.window._on_export_midi()

        self.assertEqual(self.window.controller.exported_paths, [Path("/tmp/output.mid")])
        self.window.detail_text.insert.assert_called_once()

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/output.mid")
    @patch("app.ui.main_window.messagebox.showerror")
    def test_midi_export_error_is_visible(self, show_error, choose_path):
        self.window.controller.export_error = OSError("disk full")

        self.window._on_export_midi()

        show_error.assert_called_once()
        self.window.detail_text.insert.assert_not_called()

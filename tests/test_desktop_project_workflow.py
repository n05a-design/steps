"""Headless tests for the desktop project's save/open interaction."""

import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.i18n import LocaleManager

try:
    from app.ui.main_window import StepsMainWindow
except ImportError:
    StepsMainWindow = None

from src.steps.storage import CorruptedProjectError, StorageError


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

    def get_state_summary(self):
        return {"title": "My Progression"}

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

    @patch("app.ui.main_window.filedialog.asksaveasfilename", return_value="/tmp/new.stepsproj")
    def test_save_as_updates_current_path_and_window_title(self, choose_path):
        self.window.controller.session.is_dirty = True

        self.assertTrue(self.window._on_save_project_as())

        self.assertEqual(self.window.controller.saved_paths, [Path("/tmp/new.stepsproj")])
        self.assertEqual(self.window._project_path, Path("/tmp/new.stepsproj"))
        self.assertEqual(self.window.root.window_title, "new.stepsproj — STEPS")

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

    @patch("app.ui.main_window.messagebox.askyesnocancel", return_value=None)
    def test_cancel_unsaved_prompt_prevents_new_project(self, prompt):
        self.window.controller.session.is_dirty = True
        old_path = Path("/tmp/old.stepsproj")
        self.window._project_path = old_path

        self.assertFalse(self.window._on_new_project())

        self.assertEqual(self.window.controller.new_project_calls, 0)
        self.assertEqual(self.window._project_path, old_path)
        self.window._refresh_all.assert_not_called()

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

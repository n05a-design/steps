"""Tests for localized catalogs and independent UI-language preferences."""

import ast
import json
from pathlib import Path
from string import Formatter
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import Mock, patch

from app.i18n import LocaleManager, detect_system_locale, preference_path
from app.ui.main_window import StepsMainWindow
from app.ui.session_controller import ProgressionSessionController
from src.steps.midi import MidiFile
from src.steps.progression.session import ProgressionSession
from src.steps.storage.exceptions import CorruptedProjectError


ROOT = Path(__file__).resolve().parents[1]
CATALOG_DIR = ROOT / "app" / "locales"


class FakeMenu:
    def __init__(self, size):
        self.entries = [{} for _ in range(size)]

    def entryconfigure(self, index, **options):
        self.entries[index].update(options)


class FakeWidget:
    def __init__(self):
        self.options = {}

    def configure(self, **options):
        self.options.update(options)


class FakeRoot:
    def __init__(self):
        self.title_text = ""

    def title(self, value):
        self.title_text = value


class FakeListbox:
    def __init__(self, selection=()):
        self.items = []
        self.selection = tuple(selection)

    def curselection(self):
        return self.selection

    def delete(self, start, end):
        self.items.clear()
        self.selection = ()

    def insert(self, index, value):
        self.items.append(value)

    def select_set(self, index):
        self.selection = (index,)


class FakeEntry:
    def __init__(self, value=""):
        self.value = value

    def get(self):
        return self.value

    def delete(self, start, end):
        self.value = ""

    def insert(self, index, value):
        self.value = str(value)


class FakeVariable:
    def __init__(self, value=None):
        self.value = value

    def get(self):
        return self.value

    def set(self, value):
        self.value = value


class TestLocaleManager(unittest.TestCase):
    def test_catalogs_have_identical_keys_and_placeholders(self):
        english = json.loads((CATALOG_DIR / "en.json").read_text(encoding="utf-8"))
        german = json.loads((CATALOG_DIR / "de.json").read_text(encoding="utf-8"))
        english_manager = LocaleManager(preference="en")
        german_manager = LocaleManager(preference="de")
        self.assertEqual(english.keys(), german.keys())
        self.assertTrue(all(value.strip() for value in english.values()))
        app_sources = [ROOT / "app/main.py", ROOT / "app/ui/main_window.py"]
        referenced_keys = set()
        for source in app_sources:
            tree = ast.parse(source.read_text(encoding="utf-8"))
            for node in ast.walk(tree):
                if (
                    isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)
                    and node.func.attr == "translate"
                    and node.args
                    and isinstance(node.args[0], ast.Constant)
                    and isinstance(node.args[0].value, str)
                ):
                    referenced_keys.add(node.args[0].value)
        referenced_keys.update(("language.system", "language.en", "language.de"))
        self.assertTrue(referenced_keys <= english.keys())
        for key in english:
            with self.subTest(key=key):
                en_fields = {field for _, field, _, _ in Formatter().parse(english[key]) if field}
                de_fields = {field for _, field, _, _ in Formatter().parse(german[key]) if field}
                self.assertEqual(en_fields, de_fields)
                values = {field: "value" for field in en_fields}
                self.assertEqual(
                    english_manager.translate(key, **values),
                    english[key].format(**values),
                )
                self.assertEqual(
                    german_manager.translate(key, **values),
                    german[key].format(**values),
                )

    def test_system_and_invalid_preferences_resolve_deterministically(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = Path(temp_dir) / "preferences.json"
            manager = LocaleManager(settings_file=settings, system_locale="de_AT")
            self.assertEqual(manager.language, "de")
            self.assertEqual(manager.set_preference("system", persist=False), "de")
            self.assertEqual(manager.set_preference("xx", persist=False), "de")

            english = LocaleManager(
                preference="system", settings_file=settings, system_locale="fr_FR"
            )
            self.assertEqual(english.language, "en")
            settings.write_text('{"language":"invalid"}', encoding="utf-8")
            invalid_saved = LocaleManager(settings_file=settings, system_locale="de_AT")
            self.assertEqual(invalid_saved.preference, "system")
            self.assertEqual(invalid_saved.language, "de")

    def test_system_locale_environment_precedence_and_unsupported_fallback(self):
        self.assertEqual(
            detect_system_locale(
                {"LANGUAGE": "fr_FR:de_DE", "LC_ALL": "en_US", "LANG": "en_US"}
            ),
            "de_DE",
        )
        self.assertEqual(
            detect_system_locale({"LC_ALL": "de_DE", "LC_MESSAGES": "en_US", "LANG": "en_US"}),
            "de_DE",
        )
        manager = LocaleManager(
            preference="system", settings_file=Path("/nonexistent/preferences.json"),
            environ={"LC_ALL": "fr_FR"},
        )
        self.assertEqual(manager.language, "en")

    def test_preference_persists_and_runtime_language_switch_does_not_change_music_state(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            settings = Path(temp_dir) / "preferences.json"
            manager = LocaleManager(settings_file=settings, system_locale="en_US")
            session = ProgressionSession(initial_chords=["H7", "Em"], convention="DE")

            self.assertEqual(manager.set_preference("de"), "de")
            self.assertEqual(json.loads(settings.read_text(encoding="utf-8")), {"language": "de"})
            self.assertEqual(manager.set_preference("en"), "en")
            reopened = LocaleManager(settings_file=settings, system_locale="en_US")

            self.assertEqual(reopened.preference, "en")
            self.assertEqual(session.convention, "DE")
            self.assertEqual(session.chords, ["H7", "Em"])
            midi_a = Path(temp_dir) / "german-ui.mid"
            midi_b = Path(temp_dir) / "english-ui.mid"
            manager.set_preference("de", persist=False)
            session.export_midi_file(midi_a)
            manager.set_preference("en", persist=False)
            session.export_midi_file(midi_b)
            self.assertEqual(midi_a.read_bytes(), midi_b.read_bytes())

    def test_unknown_translation_key_is_an_explicit_error(self):
        manager = LocaleManager(preference="en", system_locale="en_US")
        with self.assertRaisesRegex(KeyError, "Missing translation key"):
            manager.translate("missing.key")
        self.assertEqual(
            manager.translate("midi.export.success", path="/tmp/result.mid"),
            "MIDI file exported to:\n/tmp/result.mid",
        )

    def test_language_preference_paths_follow_platform_conventions(self):
        home = Path("/home/tester")
        self.assertEqual(
            preference_path(platform="darwin", home=home),
            home / "Library/Application Support/STEPS/preferences.json",
        )
        self.assertEqual(
            preference_path(
                platform="win32", environ={"APPDATA": "C:/Users/test/AppData/Roaming"}, home=home
            ),
            Path("C:/Users/test/AppData/Roaming/STEPS/preferences.json"),
        )
        self.assertEqual(
            preference_path(
                platform="linux", environ={"XDG_CONFIG_HOME": "/tmp/config"}, home=home
            ),
            Path("/tmp/config/steps/preferences.json"),
        )

    def test_desktop_language_switch_relocalizes_widgets_and_persists(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            window = StepsMainWindow.__new__(StepsMainWindow)
            window.i18n = LocaleManager(
                preference="en",
                settings_file=Path(temp_dir) / "preferences.json",
                system_locale="en_US",
            )
            window.controller = ProgressionSessionController(ProgressionSession())
            window.root = FakeRoot()
            window.file_menu = FakeMenu(3)
            window.menu_bar = FakeMenu(2)
            window.settings_menu = FakeMenu(1)
            window.language_menu = FakeMenu(3)
            window.title_lbl = FakeWidget()
            window.key_lbl = FakeWidget()
            window.mode_lbl = FakeWidget()
            window.major_btn = FakeWidget()
            window.minor_btn = FakeWidget()
            window.tempo_lbl = FakeWidget()
            window.meter_lbl = FakeWidget()
            window.context_btn = FakeWidget()
            window.event_start_lbl = FakeWidget()
            window.event_duration_lbl = FakeWidget()
            window.event_timing_btn = FakeWidget()
            window.add_btn = FakeWidget()
            window.update_btn = FakeWidget()
            window.remove_btn = FakeWidget()
            window.move_up_btn = FakeWidget()
            window.move_down_btn = FakeWidget()
            window.undo_btn = FakeWidget()
            window.redo_btn = FakeWidget()
            window.trans_down_btn = FakeWidget()
            window.trans_up_btn = FakeWidget()
            window.export_btn = FakeWidget()
            window.info_lbl = FakeWidget()
            window._refresh_all = Mock()

            window._localize_widgets()
            self.assertEqual(window.title_lbl.options["text"], "WORKSPACE")
            window._on_language_change("de")

            self.assertEqual(window.title_lbl.options["text"], "ARBEITSBEREICH")
            self.assertEqual(window.key_lbl.options["text"], "Tonart")
            self.assertEqual(window.major_btn.options["text"], "Dur")
            self.assertEqual(window.minor_btn.options["text"], "Moll")
            self.assertEqual(window.meter_lbl.options["text"], "Taktart")
            self.assertEqual(
                window.event_start_lbl.options["text"],
                "Start (Takt:Zählzeit:Tick, PPQ 480)",
            )
            self.assertEqual(window.event_duration_lbl.options["text"], "Dauer in Ticks (PPQ 480)")
            self.assertEqual(window.event_timing_btn.options["text"], "Timing setzen")
            self.assertEqual(window.update_btn.options["text"], "Auswahl ändern")
            self.assertEqual(window.remove_btn.options["text"], "Entfernen")
            self.assertEqual(window.move_up_btn.options["text"], "Nach oben")
            self.assertEqual(window.move_down_btn.options["text"], "Nach unten")
            self.assertEqual(window.undo_btn.options["text"], "Rückgängig")
            self.assertEqual(window.redo_btn.options["text"], "Wiederholen")
            self.assertEqual(window.file_menu.entries[0]["label"], "Öffnen…")
            self.assertEqual(window.root.title_text, "STEPS — Harmonielehre & Musiktheorie")
            self.assertEqual(
                json.loads((Path(temp_dir) / "preferences.json").read_text(encoding="utf-8")),
                {"language": "de"},
            )
            window._refresh_all.assert_called_once_with(preserve_selection=True)

    def test_refresh_after_language_switch_preserves_selected_chord(self):
        window = StepsMainWindow.__new__(StepsMainWindow)
        window.controller = SimpleNamespace(
            get_state_summary=lambda: {
                "title": "Progression",
                "chords": ["C", "G", "Am"],
                "can_undo": False,
                "can_redo": False,
            },
            session=SimpleNamespace(
                state=SimpleNamespace(ppq=480),
                time_signature=(4, 4),
                is_dirty=False,
                get_chord_event_timing=lambda index: (index * 1920, 1920),
            ),
        )
        window.i18n = LocaleManager(preference="en")
        window._project_path = None
        window.chord_listbox = FakeListbox(selection=(2,))
        window.update_btn = FakeWidget()
        window.remove_btn = FakeWidget()
        window.move_up_btn = FakeWidget()
        window.move_down_btn = FakeWidget()
        window.undo_btn = FakeWidget()
        window.redo_btn = FakeWidget()
        window.event_start_entry = FakeEntry()
        window.event_duration_entry = FakeEntry()
        window.event_timing_btn = FakeWidget()
        window._update_window_title = Mock()
        window._display_chord_details = Mock()
        window._display_empty_info = Mock()

        window._refresh_all(preserve_selection=True)

        self.assertEqual(window.chord_listbox.selection, (2,))
        window._display_chord_details.assert_called_once_with("Am")
        self.assertEqual(window.undo_btn.options["state"], "disabled")
        self.assertEqual(window.redo_btn.options["state"], "disabled")


class TestDesktopChordEditing(unittest.TestCase):
    def make_window(self, chords):
        window = StepsMainWindow.__new__(StepsMainWindow)
        window.controller = ProgressionSessionController(ProgressionSession(initial_chords=chords))
        window.i18n = LocaleManager(preference="en")
        window.root = FakeRoot()
        window._project_path = None
        window.chord_listbox = FakeListbox()
        window.chord_entry = FakeEntry()
        window.key_entry = FakeEntry(window.controller.session.key_root)
        window.mode_var = FakeVariable(window.controller.session.is_minor)
        window.tempo_entry = FakeEntry(f"{window.controller.session.bpm:g}")
        window.meter_entry = FakeEntry("4/4")
        window.event_start_entry = FakeEntry()
        window.event_duration_entry = FakeEntry()
        window.event_start_lbl = FakeWidget()
        window.event_duration_lbl = FakeWidget()
        window.event_timing_btn = FakeWidget()
        window.context_btn = FakeWidget()
        window.update_btn = FakeWidget()
        window.remove_btn = FakeWidget()
        window.move_up_btn = FakeWidget()
        window.move_down_btn = FakeWidget()
        window.undo_btn = FakeWidget()
        window.redo_btn = FakeWidget()
        window._display_chord_details = Mock()
        window._display_empty_info = Mock()
        window._refresh_all()
        return window

    def test_edit_remove_undo_redo_and_selection_follow_session(self):
        window = self.make_window(["C", "G", "Am"])
        window.chord_listbox.selection = (1,)
        window.chord_entry.value = "F#m7b5"

        window._on_update_chord()

        self.assertEqual(window.controller.session.chords, ["C", "F#m7b5", "Am"])
        self.assertEqual(window.chord_listbox.selection, (1,))
        self.assertEqual(window.undo_btn.options["state"], "normal")

        window.chord_listbox.selection = (2,)
        window._on_remove_chord()

        self.assertEqual(window.controller.session.chords, ["C", "F#m7b5"])
        self.assertEqual(window.chord_listbox.selection, (1,))

        window._on_undo()
        self.assertEqual(window.controller.session.chords, ["C", "F#m7b5", "Am"])
        self.assertEqual(window.redo_btn.options["state"], "normal")

        window._on_redo()
        self.assertEqual(window.controller.session.chords, ["C", "F#m7b5"])

    @patch("app.ui.main_window.messagebox.showerror")
    def test_invalid_chord_keeps_state_and_shows_localized_error(self, show_error):
        window = self.make_window(["C", "G"])
        window.chord_listbox.selection = (1,)
        window.chord_entry.value = "not-a-chord"

        window._on_update_chord()

        self.assertEqual(window.controller.session.chords, ["C", "G"])
        show_error.assert_called_once()
        self.assertEqual(show_error.call_args.args[0], "Chord could not be changed")

    @patch("app.ui.main_window.messagebox.showerror")
    def test_remove_last_chord_is_rejected_without_state_change(self, show_error):
        window = self.make_window(["C"])
        window.chord_listbox.selection = (0,)

        window._on_remove_chord()

        self.assertEqual(window.controller.session.chords, ["C"])
        self.assertIn("at least one chord", show_error.call_args.args[1])

    def test_move_chord_preserves_selection_and_is_one_undoable_change(self):
        window = self.make_window(["C", "G", "Am"])
        window.controller.session.set_chord_event_timing(1, 2000, 960)
        window.chord_listbox.selection = (1,)

        window._on_move_chord(-1)

        self.assertEqual(window.controller.session.chords, ["G", "C", "Am"])
        self.assertEqual(window.chord_listbox.selection, (0,))
        self.assertEqual(window.move_up_btn.options["state"], "disabled")
        self.assertEqual(window.move_down_btn.options["state"], "normal")
        self.assertEqual(window.controller.session.get_chord_event_timing(0), (2000, 960))

        window._on_undo()
        self.assertEqual(window.controller.session.chords, ["C", "G", "Am"])
        self.assertEqual(window.controller.session.get_chord_event_timing(1), (2000, 960))

    def test_move_at_progression_boundary_does_not_create_history(self):
        window = self.make_window(["C", "G"])
        window.chord_listbox.selection = (0,)
        undo_available = window.controller.session.can_undo

        window._on_move_chord(-1)

        self.assertEqual(window.controller.session.chords, ["C", "G"])
        self.assertEqual(window.controller.session.can_undo, undo_available)
        self.assertEqual(window.chord_listbox.selection, (0,))
        self.assertEqual(window.move_up_btn.options["state"], "disabled")

    def test_inserted_chord_gets_a_slot_and_shifts_later_events(self):
        session = ProgressionSession(initial_chords=["C", "G"])

        session.add_chord("F", position=1)

        self.assertEqual(session.chords, ["C", "F", "G"])
        self.assertEqual(
            [session.get_chord_event_timing(index) for index in range(3)],
            [(0, 1920), (1920, 1920), (3840, 1920)],
        )
        session.remove_chord(1)
        self.assertEqual(session.get_chord_event_timing(1), (3840, 1920))

    def test_event_timing_edit_updates_selected_chord_and_undoes(self):
        window = self.make_window(["C", "G"])
        window.chord_listbox.selection = (1,)
        window.event_start_entry.value = "2:1:180"
        window.event_duration_entry.value = "720"

        window._on_apply_event_timing()

        session = window.controller.session
        self.assertEqual(session.get_chord_event_timing(1), (2100, 720))
        self.assertEqual(window.event_start_entry.value, "2:1:180")
        window._on_undo()
        self.assertEqual(session.get_chord_event_timing(1), (1920, 1920))

    def test_session_midi_export_uses_event_specific_timing(self):
        session = ProgressionSession(initial_chords=["C", "G"])
        session.set_chord_event_timing(0, 240, 960)
        session.set_chord_event_timing(1, 1500, 480)

        with tempfile.TemporaryDirectory() as temp_dir:
            output_path = session.export_midi_file(Path(temp_dir) / "timing.mid")
            parsed = MidiFile.from_bytes(output_path.read_bytes())

        note_ons = [
            event for event in parsed.tracks[1].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x90
        ]
        note_offs = [
            event for event in parsed.tracks[1].raw_events
            if event.msg_bytes[0] & 0xF0 == 0x80
        ]
        self.assertEqual({event.abs_tick for event in note_ons}, {240, 1500})
        self.assertEqual({event.abs_tick for event in note_offs}, {1200, 1980})

    @patch("app.ui.main_window.messagebox.showerror")
    def test_invalid_event_timing_does_not_change_session(self, show_error):
        window = self.make_window(["C", "G"])
        window.chord_listbox.selection = (1,)
        window.event_start_entry.value = "1:5:0"
        window.event_duration_entry.value = "0"

        window._on_apply_event_timing()

        self.assertEqual(window.controller.session.get_chord_event_timing(1), (1920, 1920))
        self.assertEqual(
            show_error.call_args.args[1],
            "Enter a valid bar:beat:tick position (tick is within the metric beat) and a positive whole-number duration in ticks.",
        )

    def test_meter_change_reprojects_position_without_changing_absolute_tick(self):
        window = self.make_window(["C", "G"])
        session = window.controller.session
        session.set_chord_event_timing(0, 480, 960)
        window.chord_listbox.selection = (0,)
        window.meter_entry.value = "6/8"

        window._on_apply_context()

        self.assertEqual(session.get_chord_event_timing(0), (480, 960))
        self.assertEqual(window.event_start_entry.value, "1:3:0")

    def test_context_controls_apply_and_undo_key_mode_and_tempo_atomically(self):
        window = self.make_window(["C", "G"])
        window.key_entry.value = "D"
        window.mode_var.set(True)
        window.tempo_entry.value = "96.5"
        window.meter_entry.value = "3/4"

        window._on_apply_context()

        session = window.controller.session
        self.assertEqual(
            (session.key_root, session.is_minor, session.bpm, session.time_signature),
            ("D", True, 96.5, (3, 4)),
        )
        self.assertEqual(session.state.chord_duration_ticks, 1920)
        window._on_undo()
        self.assertEqual(
            (session.key_root, session.is_minor, session.bpm, session.time_signature),
            ("C", False, 120.0, (4, 4)),
        )

    def test_context_updates_respect_the_existing_german_notation(self):
        session = ProgressionSession(initial_chords=["H7"], convention="DE")

        session.set_context("H", True, 110)

        self.assertEqual(session.convention, "DE")
        self.assertEqual(session.chords, ["H7"])
        self.assertEqual((session.key_root, session.is_minor, session.bpm), ("H", True, 110.0))

    def test_invalid_meter_is_rejected_without_creating_history(self):
        session = ProgressionSession()

        with self.assertRaises(ValueError):
            session.set_context("D", True, 96, (33, 4))

        self.assertEqual(
            (session.key_root, session.is_minor, session.bpm, session.time_signature),
            ("C", False, 120.0, (4, 4)),
        )
        self.assertFalse(session.can_undo)

    def test_context_roundtrips_through_the_existing_project_schema(self):
        session = ProgressionSession(initial_chords=["H7", "Em"], convention="DE")

        session.set_context("H", True, 96.5, (6, 8))
        session.set_chord_event_timing(0, 120, 720)
        session.set_chord_event_timing(1, 1080, 360)

        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = session.save_to_file(Path(temp_dir) / "context.stepsproj")
            reopened = ProgressionSession()
            reopened.load_from_file(project_path)

        self.assertEqual(reopened.convention, "DE")
        self.assertEqual(reopened.chords, ["H7", "Em"])
        self.assertEqual(reopened.get_chord_event_timing(0), (120, 720))
        self.assertEqual(reopened.get_chord_event_timing(1), (1080, 360))
        self.assertEqual(
            (reopened.key_root, reopened.is_minor, reopened.bpm, reopened.time_signature),
            ("H", True, 96.5, (6, 8)),
        )

    def test_invalid_project_event_timing_does_not_replace_session(self):
        source = ProgressionSession(initial_chords=["C"])
        target = ProgressionSession(initial_chords=["Am"])
        with tempfile.TemporaryDirectory() as temp_dir:
            project_path = source.save_to_file(Path(temp_dir) / "invalid-timing.stepsproj")
            project_data = json.loads(project_path.read_text(encoding="utf-8"))
            project_data["tracks"][0]["events"][0]["start_tick"] = -1
            project_path.write_text(json.dumps(project_data), encoding="utf-8")

            with self.assertRaises(CorruptedProjectError):
                target.load_from_file(project_path)

        self.assertEqual(target.chords, ["Am"])

    @patch("app.ui.main_window.messagebox.showerror")
    def test_invalid_key_or_tempo_does_not_partially_update_context(self, show_error):
        window = self.make_window(["C", "G"])
        window.key_entry.value = "not-a-note"
        window.mode_var.set(True)
        window.tempo_entry.value = "96"

        window._on_apply_context()

        session = window.controller.session
        self.assertEqual((session.key_root, session.is_minor, session.bpm), ("C", False, 120.0))
        self.assertEqual(
            show_error.call_args.args[1],
            "Enter a valid key spelling for the current notation convention.",
        )

        window.key_entry.value = "D"
        window.tempo_entry.value = "401"
        window._on_apply_context()
        self.assertEqual((session.key_root, session.is_minor, session.bpm), ("C", False, 120.0))
        self.assertEqual(show_error.call_args.args[1], "Tempo must be a number between 20 and 400 BPM.")

        window.tempo_entry.value = "96"
        window.meter_entry.value = "4/5"
        window._on_apply_context()
        self.assertEqual(
            (session.key_root, session.is_minor, session.bpm, session.time_signature),
            ("C", False, 120.0, (4, 4)),
        )
        self.assertEqual(
            show_error.call_args.args[1],
            "Enter a valid time signature (numerator 1-32; denominator 1, 2, 4, 8, 16, or 32), e.g. 4/4 or 6/8.",
        )

    def test_undo_shortcut_does_not_intercept_text_entry(self):
        window = StepsMainWindow.__new__(StepsMainWindow)
        window._on_undo = Mock()
        text_entry = SimpleNamespace(winfo_class=lambda: "Entry")
        listbox = SimpleNamespace(winfo_class=lambda: "Listbox")

        self.assertIsNone(window._on_undo_shortcut(SimpleNamespace(widget=text_entry)))
        self.assertEqual(window._on_undo_shortcut(SimpleNamespace(widget=listbox)), "break")
        window._on_undo.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

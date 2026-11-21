"""Tests for reviewed progression search and provenance-preserving previews."""

import unittest
from unittest.mock import Mock, patch

from app.i18n import LocaleManager
from app.knowledge import list_reviewed_progressions
from app.ui.session_controller import ProgressionSessionController, reviewed_practice_session
from app.ui.reviewed_library_dialog import (
    ReviewedProgressionLibraryDialog,
    format_reviewed_progression,
    reviewed_progression_matches,
)


class TestReviewedProgressionLibrary(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.examples = list_reviewed_progressions()

    def test_search_includes_claim_text_and_sources(self):
        example = self.examples[0]
        source_id = example.claims[0].claim.citations[0].source_id

        self.assertTrue(reviewed_progression_matches(example, "tonales Zentrum"))
        self.assertTrue(reviewed_progression_matches(example, source_id))
        self.assertFalse(reviewed_progression_matches(example, "no matching content"))
        self.assertTrue(reviewed_progression_matches(example, ""))

    def test_search_combines_chord_name_and_provenance_terms(self):
        jazz = next(item for item in self.examples if item.progression.prog_id == "PROG-003")
        self.assertTrue(reviewed_progression_matches(jazz, "  G7    JAZZ  omt-ii-v-i "))
        self.assertFalse(reviewed_progression_matches(jazz, "jazz nowhere-in-the-catalog"))

    def test_preview_preserves_reviewed_text_and_evidence(self):
        example = self.examples[0]
        approved = example.claims[0]
        citation = approved.claim.citations[0]

        preview = format_reviewed_progression(
            example,
            LocaleManager(preference="en").translate,
        )

        for value in (
            approved.claim.text,
            approved.claim.scope,
            approved.claim.countercheck,
            citation.title,
            citation.locator,
            citation.url,
            approved.reviewer,
            approved.reviewed_on,
            approved.evidence_url,
            "source text shown as published",
        ):
            self.assertIn(value, preview)

    def test_practice_copy_preserves_stages_and_catalog_evidence(self):
        controller = ProgressionSessionController()
        before = controller.session.state
        for example in self.examples:
            original = reviewed_practice_session(example)
            degrees = [original.harmonic_degree_at(index) for index in range(len(original.chords))]
            for convention in ("INT", "DE"):
                for steps in range(-6, 7):
                    with self.subTest(example=example.progression.prog_id, convention=convention, steps=steps):
                        copy = reviewed_practice_session(example, steps, convention)
                        self.assertEqual(copy.convention, convention)
                        self.assertEqual([copy.harmonic_degree_at(index) for index in range(len(copy.chords))], degrees)
                        self.assertEqual(copy.state.chord_event_timings, original.state.chord_event_timings)
                        self.assertFalse(copy.is_dirty or copy.can_undo)
        self.assertEqual(controller.session.state, before)
        jazz = self.examples[1]
        controller.new_reviewed_project(jazz, -1, "DE")
        self.assertEqual(controller.session.key_root, "H")
        self.assertEqual(controller.session.chords, ["Cism7", "Fis7", "Hmaj7"])
        self.assertIn("Cmaj7", jazz.progression.chords_str)

    @patch("app.ui.reviewed_library_dialog.messagebox.showerror")
    @patch("app.ui.reviewed_library_dialog.webbrowser.open")
    def test_evidence_browser_failure_shows_address_in_current_language(self, browser, error):
        dialog = object.__new__(ReviewedProgressionLibraryDialog)
        dialog.window = Mock()
        url = self.examples[0].claims[0].claim.citations[0].url

        for language, failed_to_open in (("en", False), ("de", OSError("no browser"))):
            with self.subTest(language=language):
                dialog._i18n = LocaleManager(preference=language)
                browser.reset_mock(side_effect=True, return_value=True)
                error.reset_mock()
                if isinstance(failed_to_open, OSError):
                    browser.side_effect = failed_to_open
                else:
                    browser.return_value = failed_to_open

                dialog._open_evidence(url)

                browser.assert_called_once_with(url, new=2)
                error.assert_called_once_with(
                    dialog._i18n.translate("library.evidence.error.title"),
                    dialog._i18n.translate("library.evidence.error.message", url=url),
                    parent=dialog.window,
                )

    def test_dialog_stays_open_when_dirty_state_confirmation_is_cancelled(self):
        dialog = object.__new__(ReviewedProgressionLibraryDialog)
        dialog._selected = self.examples[0]
        dialog._on_load = Mock(return_value=False)
        dialog._close = Mock()
        dialog._practice_options = Mock(return_value=(1, "DE"))
        dialog._load_button = Mock()
        dialog._load_button.cget.return_value = "normal"

        dialog._load_selected()

        dialog._on_load.assert_called_once_with(
            self.examples[0].progression.prog_id, 1, "DE"
        )
        dialog._close.assert_not_called()

    def test_dialog_closes_after_project_is_loaded(self):
        dialog = object.__new__(ReviewedProgressionLibraryDialog)
        dialog._selected = self.examples[0]
        dialog._on_load = Mock(return_value=True)
        dialog._close = Mock()
        dialog._practice_options = Mock(return_value=(1, "DE"))
        dialog._load_button = Mock()
        dialog._load_button.cget.return_value = "normal"

        dialog._load_selected()

        dialog._close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

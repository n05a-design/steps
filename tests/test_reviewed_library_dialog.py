"""Tests for reviewed progression search and provenance-preserving previews."""

import unittest
from unittest.mock import Mock

from app.i18n import LocaleManager
from app.knowledge import list_reviewed_progressions
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

    def test_dialog_stays_open_when_dirty_state_confirmation_is_cancelled(self):
        dialog = object.__new__(ReviewedProgressionLibraryDialog)
        dialog._selected = self.examples[0]
        dialog._on_load = Mock(return_value=False)
        dialog._close = Mock()

        dialog._load_selected()

        dialog._on_load.assert_called_once_with(
            self.examples[0].progression.prog_id
        )
        dialog._close.assert_not_called()

    def test_dialog_closes_after_project_is_loaded(self):
        dialog = object.__new__(ReviewedProgressionLibraryDialog)
        dialog._selected = self.examples[0]
        dialog._on_load = Mock(return_value=True)
        dialog._close = Mock()

        dialog._load_selected()

        dialog._close.assert_called_once_with()


if __name__ == "__main__":
    unittest.main()

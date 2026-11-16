"""Bindet die menschliche Graph-Abnahme an die unveränderte, erzeugte Audit-Matrix."""

import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "knowledge" / "relations" / "GRAPH_AUDIT_MATRIX.csv"
REVIEW = ROOT / "knowledge" / "relations" / "GRAPH_HUMAN_REVIEW_v1.csv"
DECISIONS = {
    "APPROVED_WITH_PATCH": ("APPROVED_SCOPED", "True"),
    "REJECTED_DEPRECATED": ("DEPRECATED", "False"),
    "REJECTED_REPLACED": ("DEPRECATED", "False"),
}


def read(path):
    with path.open(encoding="utf-8", newline="") as source:
        return list(csv.DictReader(source))


class GraphHumanReviewTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.matrix = {row["relation_id"]: row for row in read(MATRIX)}
        cls.review = read(REVIEW)

    def test_each_decision_binds_to_an_unchanged_matrix_row(self):
        self.assertEqual(len(self.review), 25)
        self.assertEqual(len({row["relation_id"] for row in self.review}), 25)
        for row in self.review:
            with self.subTest(relation=row["relation_id"]):
                original = self.matrix[row["relation_id"]]
                for key in ("original_row_sha256", "source_id", "relation_type", "target_id"):
                    self.assertEqual(row[key], original[key])

    def test_decision_fields_are_consistent(self):
        for row in self.review:
            with self.subTest(relation=row["relation_id"]):
                status, production = DECISIONS[row["human_review"]]
                self.assertEqual(row["review_status"], status)
                self.assertEqual(row["production_use_allowed"], production)
                self.assertTrue(row["proposed_relation_type"].strip())
                self.assertTrue(row["decision_note"].strip())
                self.assertEqual((row["reviewer"], row["review_date"]), ("Inhaber", "2026-11-17"))

    def test_generated_matrix_still_awaits_review(self):
        # Die Abnahme ist eine eigene Schicht; der Generator weist Freigaben in der Matrix ab.
        self.assertTrue(all(row["human_review"] == "AUSSTEHEND" for row in self.matrix.values()))
        self.assertTrue(all(row["production_use_allowed"] == "False" for row in self.matrix.values()))


if __name__ == "__main__":
    unittest.main()

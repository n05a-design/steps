"""Bindet die menschliche Graph-Abnahme an die unveränderte, erzeugte Audit-Matrix."""

import csv
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MATRIX = ROOT / "knowledge" / "relations" / "GRAPH_AUDIT_MATRIX.csv"
REVIEW = ROOT / "knowledge" / "relations" / "GRAPH_HUMAN_REVIEW_v1.csv"
REVIEW_V2 = ROOT / "knowledge" / "relations" / "GRAPH_HUMAN_REVIEW_v2.csv"
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


class GraphHumanReviewV2Test(unittest.TestCase):
    STATES = {
        "APPROVED_SCOPED": ("APPROVED_SCOPED", "True"),
        "APPROVED_WITH_PATCH": ("APPROVED_SCOPED", "True"),
        "DEFERRED_CORPUS_REQUIRED": ("PENDING_EMPIRICAL_CORPUS_EVAL", "False"),
        "REJECTED_DEPRECATED": ("DEPRECATED", "False"),
        "REJECTED_REPLACED": ("DEPRECATED", "False"),
    }

    @classmethod
    def setUpClass(cls):
        cls.matrix = read(MATRIX)
        cls.v1 = {row["relation_id"]: row for row in read(REVIEW)}
        cls.v2 = read(REVIEW_V2)

    def test_covers_every_matrix_row_in_order_and_binds_to_it(self):
        self.assertEqual([r["relation_id"] for r in self.v2], [r["relation_id"] for r in self.matrix])
        for row, original in zip(self.v2, self.matrix):
            with self.subTest(relation=row["relation_id"]):
                for key in ("original_row_sha256", "source_id", "relation_type", "target_id"):
                    self.assertEqual(row[key], original[key])

    def test_counts_match_owner_specification(self):
        from collections import Counter
        self.assertEqual(Counter(r["human_review"] for r in self.v2), Counter({
            "APPROVED_SCOPED": 41, "APPROVED_WITH_PATCH": 40, "DEFERRED_CORPUS_REQUIRED": 14,
            "REJECTED_DEPRECATED": 1, "REJECTED_REPLACED": 1}))

    def test_states_scopes_and_round_one_carry_over(self):
        for row in self.v2:
            with self.subTest(relation=row["relation_id"]):
                status, production = self.STATES[row["human_review"]]
                self.assertEqual((row["review_status"], row["production_use_allowed"]), (status, production))
                self.assertTrue(row["decision_note"].strip())
                if production == "True":
                    self.assertTrue(row["scope"].strip())
                if row["relation_id"] in self.v1:
                    old = self.v1[row["relation_id"]]
                    self.assertEqual(row["review_round"], "v1")
                    for key in ("proposed_relation_type", "review_status", "human_review", "production_use_allowed"):
                        self.assertEqual(row[key], old[key])
                    self.assertEqual(row["decision_note"], old["decision_note"])

    def test_sample_supported_edges_keep_their_review_note_as_scope(self):
        for row, original in zip(self.v2, self.matrix):
            if row["human_review"] == "APPROVED_SCOPED":
                self.assertEqual(original["relation_status"], "SAMPLE_SUPPORTED")
                self.assertEqual(original["technical_status"], "PASS")
                self.assertEqual(row["scope"], original["review_note"])

    def test_attribution_is_not_a_historical_origin(self):
        cdr019 = next(r for r in self.v2 if r["relation_id"] == "CDR-019")
        self.assertEqual(cdr019["proposed_relation_type"], "ATTRIBUTED_INTERPRETATION")


if __name__ == "__main__":
    unittest.main()

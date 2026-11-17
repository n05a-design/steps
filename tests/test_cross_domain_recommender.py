"""
Tests for the STEPS Cross-Domain Recommendation Engine (OA-0032).

Verifies:
- Relational mapping between Harmony (M05), Drums (M08), Piano (M10), Bass, and Theory (M07).
- Explicit reference relationships REL-001 through REL-013, REL-014..REL-036, and CR-038.
- 100% full coverage for all 28 canonical archetypes (PROG-001 through PROG-028).
- Reverse lookups: recommend_for_drum_pattern and recommend_for_piano_module.
- Authentic genre bassline models and exception handling.
"""

from __future__ import annotations

import unittest
from pathlib import Path

from src.steps.progression import (
    CANONICAL_BASSLINE_MODELS,
    CANONICAL_DRUM_PATTERNS,
    CANONICAL_PIANO_MODULES,
    CANONICAL_PROGRESSIONS,
    BasslineModel,
    CrossDomainRecommendation,
    CrossDomainRecommender,
    CrossDomainRelation,
    RecommendationItem,
    get_concept_relations,
    get_recommender,
    recommend_for_drum_pattern,
    recommend_for_piano_module,
    recommend_for_progression,
)


class TestCrossDomainRecommender(unittest.TestCase):
    def setUp(self) -> None:
        self.recommender = get_recommender()

    def test_recommender_initialization_and_relation_count(self) -> None:
        """Verify recommender loads the canonical CSV and has 90+ relations."""
        self.assertGreaterEqual(len(self.recommender.relations), 94)
        self.assertIsInstance(self.recommender.relations[0], CrossDomainRelation)

    def test_explicit_relations_rel_001_through_rel_013(self) -> None:
        """Test specific explicit relations REL-001 to REL-013 required by OA-0032."""
        rel_map = {r.relation_id: r for r in self.recommender.relations}

        # REL-001: PROG-001 COMMONLY_PAIRED_WITH PAT-001
        self.assertIn("REL-001", rel_map)
        r1 = rel_map["REL-001"]
        self.assertEqual(r1.source_id, "PROG-001")
        self.assertEqual(r1.target_id, "PAT-001")
        self.assertEqual(r1.relation_type, "COMMONLY_PAIRED_WITH")
        self.assertEqual(r1.formal_rule_or_strength, "STRONG")

        # REL-002: PROG-001 TAUGHT_VIA P07
        self.assertIn("REL-002", rel_map)
        r2 = rel_map["REL-002"]
        self.assertEqual(r2.source_id, "PROG-001")
        self.assertEqual(r2.target_id, "P07")
        self.assertEqual(r2.relation_type, "TAUGHT_VIA")

        # REL-003: PROG-003 VOICED_BY P05
        self.assertIn("REL-003", rel_map)
        r3 = rel_map["REL-003"]
        self.assertEqual(r3.source_id, "PROG-003")
        self.assertEqual(r3.target_id, "P05")
        self.assertEqual(r3.formal_rule_or_strength, "MANDATORY_JAZZ")

        # REL-004: PROG-003 VOICED_BY P08
        self.assertIn("REL-004", rel_map)
        r4 = rel_map["REL-004"]
        self.assertEqual(r4.source_id, "PROG-003")
        self.assertEqual(r4.target_id, "P08")
        self.assertEqual(r4.formal_rule_or_strength, "ADVANCED_JAZZ")

        # REL-005: PROG-003 COMMONLY_PAIRED_WITH PAT-012
        self.assertIn("REL-005", rel_map)
        r5 = rel_map["REL-005"]
        self.assertEqual(r5.source_id, "PROG-003")
        self.assertEqual(r5.target_id, "PAT-012")

        # REL-006: PROG-007 COMMONLY_PAIRED_WITH PAT-007
        self.assertIn("REL-006", rel_map)
        r6 = rel_map["REL-006"]
        self.assertEqual(r6.source_id, "PROG-007")
        self.assertEqual(r6.target_id, "PAT-007")

        # REL-007: PROG-017 COMMONLY_PAIRED_WITH PAT-013
        self.assertIn("REL-007", rel_map)
        r7 = rel_map["REL-007"]
        self.assertEqual(r7.source_id, "PROG-017")
        self.assertEqual(r7.target_id, "PAT-013")

        # REL-008: PROG-017 VOICED_BY P08
        self.assertIn("REL-008", rel_map)
        r8 = rel_map["REL-008"]
        self.assertEqual(r8.source_id, "PROG-017")
        self.assertEqual(r8.target_id, "P08")

        # REL-009: PAT-010 REQUIRES_TECHNIQUE P09
        self.assertIn("REL-009", rel_map)
        r9 = rel_map["REL-009"]
        self.assertEqual(r9.source_id, "PAT-010")
        self.assertEqual(r9.target_id, "P09")
        self.assertEqual(r9.formal_rule_or_strength, "MANDATORY_REGGAE")

        # REL-010: PAT-018 EXEMPLIFIES_METRIC_DUALITY M07
        self.assertIn("REL-010", rel_map)
        r10 = rel_map["REL-010"]
        self.assertEqual(r10.source_id, "PAT-018")
        self.assertEqual(r10.target_id, "M07")

        # REL-011: PAT-020 UTILIZES_SWING_PROFILE M07
        self.assertIn("REL-011", rel_map)
        r11 = rel_map["REL-011"]
        self.assertEqual(r11.source_id, "PAT-020")
        self.assertEqual(r11.target_id, "M07")

        # REL-012: P09 TRAINS_RHYTHMIC_INTERACTION PAT-012
        self.assertIn("REL-012", rel_map)
        r12 = rel_map["REL-012"]
        self.assertEqual(r12.source_id, "P09")
        self.assertEqual(r12.target_id, "PAT-012")

        # REL-013: P10 FOUNDATIONAL_FOR PROG-001
        self.assertIn("REL-013", rel_map)
        r13 = rel_map["REL-013"]
        self.assertEqual(r13.source_id, "P10")
        self.assertEqual(r13.target_id, "PROG-001")

    def test_additional_relations_and_cr038(self) -> None:
        """Verify CR-038 and relations from Phase 4.10..4.18."""
        rel_map = {r.relation_id: r for r in self.recommender.relations}

        # CR-038: PROG-028 VOICED_BY P12
        self.assertIn("CR-038", rel_map)
        cr38 = rel_map["CR-038"]
        self.assertEqual(cr38.source_id, "PROG-028")
        self.assertEqual(cr38.target_id, "P12")

        # REL-021 & REL-022: PROG-021
        self.assertEqual(rel_map["REL-021"].target_id, "PAT-024")
        self.assertEqual(rel_map["REL-022"].target_id, "P12")

        # REL-026: PROG-023 with PAT-018
        self.assertEqual(rel_map["REL-026"].source_id, "PROG-023")
        self.assertEqual(rel_map["REL-026"].target_id, "PAT-018")

        # REL-029 & REL-030: PROG-024 with PAT-027 and P14
        self.assertEqual(rel_map["REL-029"].target_id, "PAT-027")
        self.assertEqual(rel_map["REL-030"].target_id, "P14")

        # REL-032 & REL-036: PROG-025 with PAT-028 and PAT-031
        self.assertEqual(rel_map["REL-032"].target_id, "PAT-028")
        self.assertEqual(rel_map["REL-036"].source_id, "PAT-031")
        self.assertEqual(rel_map["REL-036"].target_id, "PROG-025")

        # REL-035: PROG-028 with PAT-030
        self.assertEqual(rel_map["REL-035"].source_id, "PROG-028")
        self.assertEqual(rel_map["REL-035"].target_id, "PAT-030")

    def test_all_28_canonical_progressions_coverage(self) -> None:
        """Every canonical progression PROG-001..PROG-028 must yield a valid, non-empty recommendation."""
        for i in range(1, 29):
            prog_id = f"PROG-{i:03d}"
            rec = recommend_for_progression(prog_id)
            self.assertIsInstance(rec, CrossDomainRecommendation)
            self.assertEqual(rec.prog_id, prog_id)
            self.assertGreaterEqual(len(rec.drum_grooves), 1, f"Missing drum groove for {prog_id}")
            self.assertGreaterEqual(len(rec.piano_voicings), 1, f"Missing piano voicing for {prog_id}")
            self.assertIsInstance(rec.bassline_model, BasslineModel)
            self.assertTrue(rec.bassline_model.name)
            self.assertTrue(rec.bassline_model.pattern_description)
            self.assertEqual(rec.overall_compatibility, "HIGH")

            # Check recommendation items integrity
            for drum in rec.drum_grooves:
                self.assertIsInstance(drum, RecommendationItem)
                self.assertEqual(drum.domain, "DRUM")
                self.assertTrue(drum.target_id.startswith("PAT-"))
                self.assertGreaterEqual(drum.confidence, 0.7)
            for piano in rec.piano_voicings:
                self.assertIsInstance(piano, RecommendationItem)
                self.assertEqual(piano.domain, "PIANO")
                self.assertTrue(piano.target_id.startswith("P"))
                self.assertGreaterEqual(piano.confidence, 0.7)

    def test_recommendation_vectors_for_case_studies(self) -> None:
        """Test specific case study progressions: PROG-017 and PROG-023."""
        # Case Study 1: Midnight Solace (PROG-017 Backdoor)
        rec17 = recommend_for_progression("PROG-017")
        drum_ids17 = [d.target_id for d in rec17.drum_grooves]
        piano_ids17 = [p.target_id for p in rec17.piano_voicings]
        self.assertIn("PAT-013", drum_ids17)
        self.assertIn("P08", piano_ids17)
        self.assertIn("P18", piano_ids17)
        self.assertEqual(rec17.bassline_model.name, "Electric Fingerstyle Bass with Chromatic Passing Tones")
        self.assertIn("Fm7", rec17.bassline_model.pattern_description)

        # Case Study 2: Horizon Drift (PROG-023 Liquid D&B)
        rec23 = recommend_for_progression("PROG-023")
        drum_ids23 = [d.target_id for d in rec23.drum_grooves]
        piano_ids23 = [p.target_id for p in rec23.piano_voicings]
        self.assertIn("PAT-018", drum_ids23)
        self.assertIn("P09", piano_ids23)
        self.assertIn("Reese Sub-Bass", rec23.bassline_model.name)

    def test_reverse_lookup_recommend_for_drum_pattern(self) -> None:
        """Test reverse recommendations starting from a drum groove."""
        # PAT-013 (Linear Funk / Neo-Soul)
        matches13 = recommend_for_drum_pattern("PAT-013")
        target_ids13 = [m.target_id for m in matches13]
        self.assertIn("PROG-017", target_ids13)

        # PAT-018 (Liquid D&B Break)
        matches18 = recommend_for_drum_pattern("PAT-018")
        target_ids18 = [m.target_id for m in matches18]
        self.assertIn("PROG-002", target_ids18)
        self.assertIn("PROG-023", target_ids18)

        # PAT-027 (Bossa Nova Brush)
        matches27 = recommend_for_drum_pattern("PAT-027")
        target_ids27 = [m.target_id for m in matches27]
        self.assertIn("PROG-024", target_ids27)

        # PAT-028 (Afro-Cuban Cha-Cha)
        matches28 = recommend_for_drum_pattern("PAT-028")
        target_ids28 = [m.target_id for m in matches28]
        self.assertIn("PROG-025", target_ids28)

        # PAT-030 (Phrygian Neo-Soul Halftime Shuffle)
        matches30 = recommend_for_drum_pattern("PAT-030")
        target_ids30 = [m.target_id for m in matches30]
        self.assertIn("PROG-028", target_ids30)

    def test_reverse_lookup_recommend_for_piano_module(self) -> None:
        """Test reverse recommendations starting from a piano practice module."""
        # P08 (Drop-2 Voicings)
        matches_p08 = recommend_for_piano_module("P08")
        target_ids_p08 = [m.target_id for m in matches_p08]
        self.assertIn("PROG-003", target_ids_p08)
        self.assertIn("PROG-017", target_ids_p08)

        # P12 (Two-Handed Rootless Voicings)
        matches_p12 = recommend_for_piano_module("P12")
        target_ids_p12 = [m.target_id for m in matches_p12]
        self.assertIn("PROG-021", target_ids_p12)
        self.assertIn("PROG-028", target_ids_p12)

        # P14 (Bossa Nova / Latin Piano)
        matches_p14 = recommend_for_piano_module("P14")
        target_ids_p14 = [m.target_id for m in matches_p14]
        self.assertIn("PROG-024", target_ids_p14)
        self.assertIn("PROG-025", target_ids_p14)

        # P19 (Chromatic Bassline for Secondary Dominants)
        matches_p19 = recommend_for_piano_module("P19")
        target_ids_p19 = [m.target_id for m in matches_p19]
        self.assertIn("PROG-026", target_ids_p19)

    def test_get_concept_relations(self) -> None:
        """Verify entity querying returns all associated explicit relations."""
        rels = get_concept_relations("PROG-017")
        rel_ids = [r.relation_id for r in rels]
        self.assertIn("REL-007", rel_ids)
        self.assertIn("REL-008", rel_ids)

        rels_p09 = get_concept_relations("P09")
        p09_ids = [r.relation_id for r in rels_p09]
        self.assertIn("REL-009", p09_ids)
        self.assertIn("REL-012", p09_ids)
        self.assertIn("REL-018", p09_ids)

    def test_invalid_identifiers_raise_key_error(self) -> None:
        """Ensure invalid IDs trigger appropriate KeyError exceptions."""
        with self.assertRaises(KeyError):
            recommend_for_progression("PROG-999")

        with self.assertRaises(KeyError):
            recommend_for_progression("INVALID")

        with self.assertRaises(KeyError):
            recommend_for_drum_pattern("PAT-999")

        with self.assertRaises(KeyError):
            recommend_for_piano_module("P99")


if __name__ == "__main__":
    unittest.main()

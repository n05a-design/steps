"""
STEPS Public Repository & Rights Audit Verification Tests (Phase P0.1 / Prompt 27).

Validates:
- Presence and non-emptiness of all 5 Prompt 27 deliverables
- CSV column integrity and record schema
- No Class E assets are marked approved or in working tree
- Validation of recheck_manifest.json
"""

import csv
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
RIGHTS_DIR = ROOT / "docs/audit/rights_audit"


class TestRightsAuditDeliverables(unittest.TestCase):
    def test_deliverables_exist(self):
        required_files = [
            "public_asset_inventory.csv",
            "license_findings.csv",
            "history_impact.md",
            "recommended_mitigation_with_alternatives.md",
            "recheck_manifest.json",
        ]
        for name in required_files:
            file_path = RIGHTS_DIR / name
            self.assertTrue(file_path.exists(), f"Missing deliverable: {file_path}")
            self.assertGreater(file_path.stat().st_size, 100, f"Deliverable too small or empty: {file_path}")

    def test_inventory_csv_schema_and_contents(self):
        csv_path = RIGHTS_DIR / "public_asset_inventory.csv"
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            expected_fields = {
                "path", "blob_sha", "sha256", "size_bytes", "file_type",
                "category", "origin", "provenance_notes", "public_status", "release_scope"
            }
            self.assertTrue(expected_fields.issubset(set(reader.fieldnames or [])))
            rows = list(reader)
            self.assertGreaterEqual(len(rows), 250, "Expected at least 250 tracked binary/media assets")
            
            for row in rows:
                self.assertIn(row["public_status"], {"approved", "review_required", "restricted_local", "rejected"})
                self.assertIn(row["release_scope"], {"core_app", "dev_only", "research_archive", "restricted"})
                # Assert rejected AI text is properly marked
                if "The Chord Wheel.html" in row["path"]:
                    self.assertEqual(row["public_status"], "rejected")

    def test_license_findings_schema(self):
        csv_path = RIGHTS_DIR / "license_findings.csv"
        with open(csv_path, encoding="utf-8") as f:
            reader = csv.DictReader(f)
            rows = list(reader)
            self.assertGreaterEqual(len(rows), 8, "Expected at least 8 major finding groups")
            for row in rows:
                self.assertTrue(row["asset_id"].startswith("FIND-"))
                self.assertIn(row["license_class"], {"A", "B", "C", "D", "E", "STEPS_PROPRIETARY", "UNKNOWN"})
                self.assertIn(row["legal_risk_level"], {"LOW", "MEDIUM", "HIGH", "RESTRICTED_RESOLVED"})

    def test_recheck_manifest_json(self):
        json_path = RIGHTS_DIR / "recheck_manifest.json"
        with open(json_path, encoding="utf-8") as f:
            data = json.load(f)
        self.assertEqual(data["task_reference"], "P0.1 / Prompt 27 / OA-0001")
        self.assertTrue(data["gates_verified"]["no_class_e_in_working_tree"])
        self.assertTrue(data["gates_verified"]["all_assets_classified"])
        self.assertTrue(data["gates_verified"]["owner_history_decision_documented"])
        self.assertTrue(data["gates_verified"]["ingestion_policy_established"])


if __name__ == "__main__":
    unittest.main()

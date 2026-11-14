"""Check the external evidence boundary with synthetic GitHub responses."""

from datetime import datetime, timezone
from hashlib import sha256
import json
from pathlib import Path
import subprocess
from tempfile import TemporaryDirectory
from types import SimpleNamespace
import unittest
from unittest.mock import patch

from scripts import verify_pilot_review_evidence as evidence
from src.steps.progression import reviewed


class TestReviewEvidence(unittest.TestCase):
    def setUp(self):
        claim = reviewed.Claim(
            claim_id="TEST-CLAIM", kind="fact", text="Synthetic evidence test.",
            scope="Isolated unit test.", countercheck="Independent test data.",
            citations=(), fingerprint=sha256(b"synthetic evidence claim").hexdigest(),
            voice_path=(),
        )
        self.approval = reviewed.ApprovedClaim(
            claim=claim, reviewer="n05a-design", reviewed_on="2026-11-12",
            evidence_url="https://github.com/n05a-design/steps/pull/42#issuecomment-1234",
        )
        self.now = datetime(2026, 11, 13, tzinfo=timezone.utc)
        self.comment = {
            "id": 1234, "html_url": self.approval.evidence_url,
            "issue_url": "https://api.github.com/repos/n05a-design/steps/issues/42",
            "user": {"id": 333259995, "login": self.approval.reviewer, "type": "User"},
            "author_association": "OWNER",
            "created_at": "2026-11-12T19:28:13Z", "updated_at": "2026-11-12T19:28:13Z",
            "body": f"STEPS-APPROVED {claim.claim_id} {claim.fingerprint}",
        }

    def test_approved_pair(self):
        evidence.verify_approval(self.approval, self.comment, now=self.now)

    def test_mismatching_or_edited_evidence_blocks(self):
        claim = self.approval.claim
        for change in (
            {"id": 1235},
            {"issue_url": "https://api.github.com/repos/n05a-design/steps/issues/41"},
            {"html_url": self.approval.evidence_url.replace("n05a-design", "other")},
            {"user": {**self.comment["user"], "id": 1}},
            {"user": {**self.comment["user"], "type": "Bot"}},
            {"user": {**self.comment["user"], "login": "someone-else"}},
            {"author_association": "NONE"},
            {"body": f"STEPS-APPROVED OTHER-CLAIM {claim.fingerprint}"},
            {"body": f"STEPS-APPROVED {claim.claim_id} " + "a" * 64},
            {"body": f"Rejected: {claim.claim_id} {claim.fingerprint}"},
            {"updated_at": "2026-11-12T20:00:00Z"},
            {"created_at": "2026-11-14T00:00:00Z", "updated_at": "2026-11-14T00:00:00Z"},
        ):
            with self.subTest(change=change), self.assertRaises(reviewed.PublicationError):
                evidence.verify_approval(self.approval, {**self.comment, **change}, now=self.now)

    def test_legacy_rejection_is_not_an_approval(self):
        fingerprint = self.approval.claim.fingerprint
        body = f"| `PROG-001-TONAL-CENTER` | `{fingerprint}` | **Korrektur erforderlich.** Bitte neu prüfen. |"
        self.assertEqual(evidence.approvals_in_body(body, evidence.LEGACY_TABLE), set())

    def test_deleted_comment_and_api_outage_cannot_pass(self):
        example = SimpleNamespace(claims=(self.approval,))

        def fail(_):
            raise reviewed.PublicationError("GitHub comment unavailable")

        with self.assertRaisesRegex(reviewed.PublicationError, "unavailable"):
            evidence.verify_catalog((example,), fetch=fail, now=self.now)

    def test_local_revision_reads_the_committed_catalog(self):
        with TemporaryDirectory() as temporary:
            root = Path(temporary)
            files = self.write_revision_fixture(root)
            subprocess.run(["git", "init", "--quiet", str(root)], check=True)
            subprocess.run(["git", "add", "."], cwd=root, check=True)
            subprocess.run(
                ["git", "-c", "user.name=STEPS Test", "-c", "user.email=fixture@example.invalid",
                 "-c", "commit.gpgsign=false", "commit", "--quiet", "-m", "Synthetic catalog"],
                cwd=root, check=True,
            )
            revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=root, text=True).strip()
            with patch.object(evidence, "ROOT", root), patch.multiple(reviewed, **files):
                expected = reviewed.load_reviewed_catalog()
                self.assertEqual(len(expected), 3)
                self.assertEqual(evidence.catalog_from_revision(revision), expected)

                # A dirty worktree must not substitute its catalog data for the commit's blobs.
                files["APPROVALS"].write_text(
                    json.dumps({"schema_version": 1, "approvals": {}}), encoding="utf-8",
                )
                with self.assertRaisesRegex(reviewed.PublicationError, "Missing human approval"):
                    reviewed.load_reviewed_catalog()
                self.assertEqual(evidence.catalog_from_revision(revision), expected)

                # Invalid committed data must still be rejected by the production loader.
                subprocess.run(["git", "add", "."], cwd=root, check=True)
                invalid_tree = subprocess.check_output(["git", "write-tree"], cwd=root, text=True).strip()
                invalid_revision = subprocess.check_output(
                    ["git", "-c", "user.name=STEPS Test", "-c", "user.email=fixture@example.invalid",
                     "commit-tree", invalid_tree, "-p", revision, "-m", "Missing fixture approvals"],
                    cwd=root, text=True,
                ).strip()
                with self.assertRaisesRegex(reviewed.PublicationError, "Missing human approval"):
                    evidence.catalog_from_revision(invalid_revision)
        with self.assertRaises(ValueError):
            evidence.catalog_from_revision("HEAD")

    @staticmethod
    def write_revision_fixture(root):
        """Build all three data blobs without reading the product's review state."""
        files = {
            "CATALOG": root / "src/steps/progression/reviewed_progressions.json",
            "APPROVALS": root / "src/steps/progression/reviewed_progression_approvals.json",
            "REGISTRY": root / "knowledge/sources/registry.yaml",
        }
        for path in files.values():
            path.parent.mkdir(parents=True, exist_ok=True)

        def claim(ident, *, kind="fact", voice_path=None):
            result = {
                "id": ident, "kind": kind, "text": f"Synthetic claim {ident}.",
                "scope": "Isolated revision test.", "countercheck": "Independent fixture data.",
                "references": [{"source_id": "fixture-source", "locator": "Synthetic section 1"}],
            }
            if voice_path is not None:
                result["voice_path"] = [
                    {"chord_index": index, "note": note} for index, note in voice_path
                ]
            return result

        rows = (
            ("PROG-001", "I - V - vi - IV", "C - G - Am - F", [
                claim("PROG-001-HARMONY"), claim("PROG-001-TONAL-CENTER"),
            ]),
            ("PROG-003", "ii^7 - V^7 - I^maj7", "Dm7 - G7 - Cmaj7", [
                claim("PROG-003-HARMONY"),
                claim("PROG-003-VOICE-II-V", voice_path=((0, "C4"), (1, "H3"))),
                claim("PROG-003-VOICE-V-I", voice_path=((1, "F4"), (2, "E4"))),
            ]),
            ("PROG-009", "I - IV - iv - I", "C - F - Fm - C", [
                claim("PROG-009-HARMONY"),
                claim("PROG-009-VOICE-LEADING", voice_path=((1, "A4"), (2, "As4"), (3, "G4"))),
            ]),
        )
        catalog = {
            "schema_version": 2, "notation": claim("PILOT-NOTATION-001", kind="convention"),
            "examples": [
                {"id": ident, "name": f"Synthetic {ident}", "default_key": "C", "roman": roman,
                 "chords": chords, "context": "Synthetic C-major example.", "claims": claims}
                for ident, roman, chords, claims in rows
            ],
        }
        registry = {"schema_version": 1, "sources": [{
            "id": "fixture-source", "title": "Synthetic source",
            "url": "https://example.invalid/synthetic-source", "rights_status": "approved",
        }]}
        files["CATALOG"].write_text(json.dumps(catalog), encoding="utf-8")
        files["REGISTRY"].write_text(json.dumps(registry), encoding="utf-8")
        with patch.multiple(reviewed, **files):
            _, claims = reviewed._candidates()
        approvals = {ident: {
            "fingerprint": value.fingerprint, "reviewer": "fixture-reviewer",
            "reviewed_on": "2026-11-12",
            "evidence_url": "https://github.com/n05a-design/steps/pull/42#issuecomment-1234",
        } for ident, value in claims.items()}
        files["APPROVALS"].write_text(
            json.dumps({"schema_version": 1, "approvals": approvals}), encoding="utf-8",
        )
        return files

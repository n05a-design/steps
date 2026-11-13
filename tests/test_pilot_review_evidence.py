"""Check the external evidence boundary with synthetic GitHub responses."""

from dataclasses import replace
from datetime import datetime, timezone
import unittest

from scripts import verify_pilot_review_evidence as evidence
from src.steps.progression import reviewed


class TestReviewEvidence(unittest.TestCase):
    def setUp(self):
        example = reviewed.load_reviewed_catalog()[0]
        self.approval = replace(
            example.claims[0],
            evidence_url="https://github.com/n05a-design/steps/pull/42#issuecomment-1234",
        )
        claim = self.approval.claim
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
        example = reviewed.load_reviewed_catalog()[0]

        def fail(_):
            raise reviewed.PublicationError("GitHub comment unavailable")

        with self.assertRaisesRegex(reviewed.PublicationError, "unavailable"):
            evidence.verify_catalog((example,), fetch=fail, now=self.now)

    def test_local_revision_reads_the_committed_catalog(self):
        import subprocess
        revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=evidence.ROOT, text=True).strip()
        self.assertEqual(evidence.catalog_from_revision(revision), reviewed.load_reviewed_catalog())
        with self.assertRaises(ValueError):
            evidence.catalog_from_revision("HEAD")

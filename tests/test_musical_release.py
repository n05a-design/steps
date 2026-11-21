"""Missing, stale and self-approved evidence must block musical acceptance."""

from contextlib import redirect_stderr
from datetime import datetime, timezone
from io import StringIO
import json
import os
from subprocess import CompletedProcess
import unittest
from unittest.mock import patch

from scripts import verify_musical_release as gate


class MusicalReleaseTest(unittest.TestCase):
    revision = "a" * 40
    url = "https://github.com/n05a-design/steps/pull/30#issuecomment-40"

    def setUp(self):
        self.cases = gate.benchmark.load_cases()
        self.entry = {
            "criteria": {"Musical criterion": True},
            "observations": "The resolution was heard and checked in the score.",
            "sources": [{"url": "https://example.org/score", "locator": "Measure 14",
                         "supports": "Resolution of the leading tone"}],
            "evidence_url": "https://example.org/assessment",
        }

    def check(self, area, cases=(), automatic=(), acceptance=None, probes=None):
        return gate.check_area(area, cases, automatic, acceptance or {},
                               run_suites=lambda modules: [], probes=probes or {})

    def submission(self, *, self_review=False, edited=False, revision=None):
        record = {"area": "desktop-voicing", "revision": revision or self.revision,
                  "independent": True, "reviews": {"AREA": self.entry}}
        timestamp = datetime(2020, 1, 1, tzinfo=timezone.utc).isoformat()
        author = next(iter(gate.pilot.REVIEWERS))
        comment = {
            "id": 40, "html_url": self.url,
            "issue_url": f"https://api.github.com/repos/{gate.pilot.REPOSITORY}/issues/30",
            "user": {"id": author, "login": "reviewer", "type": "User"},
            "author_association": "MEMBER", "created_at": timestamp,
            "updated_at": "2020-01-02T00:00:00+00:00" if edited else timestamp,
            "body": "```steps-musical-review\n" + json.dumps(record) + "\n```",
        }
        pull = {"number": 30, "base": {"repo": {"full_name": gate.pilot.REPOSITORY}},
                "head": {"sha": "b" * 40}, "merged": True, "merge_commit_sha": self.revision,
                "user": {"id": author if self_review else 1}}
        return comment, pull

    def verify(self, comment, pull):
        return gate.verified_submission(self.url, self.revision, fetch_comment=lambda ident: comment,
                                        fetch_pr=lambda number: pull)

    def test_all_benchmark_cases_have_an_area(self):
        self.assertTrue(all(gate.case_area(case) in gate.AREAS for case in self.cases))
        self.assertEqual(sum(bool(gate.requirements("harmony-coach", [case])) for case in self.cases
                             if gate.case_area(case) == "harmony-coach"), 12)

    def test_pending_manual_case_blocks_only_its_area(self):
        cases = [case for case in self.cases if gate.case_area(case) == "desktop-voicing"]
        self.assertEqual("READY", self.check("theory-core")["status"])
        result = self.check("desktop-voicing", cases)
        self.assertEqual("BLOCKED", result["status"])
        self.assertTrue(any("KB-M12-PLAYABILITY" in blocker for blocker in result["blockers"]))

    def test_failed_calculation_cannot_be_overridden_by_optional_result(self):
        results = [
            {"id": "deterministic", "mandatory": True, "status": "FAIL", "observed": "incorrect bass"},
            {"id": "optional", "mandatory": False, "status": "PENDING", "observed": "open"},
        ]
        report = self.check("midi-export", automatic=results)
        self.assertEqual("BLOCKED", report["status"])
        self.assertEqual(["deterministic: FAIL (incorrect bass)"], report["blockers"])

    def test_runtime_probe_can_block_an_otherwise_green_area(self):
        report = self.check("midi-export", probes={"midi-export": lambda: ["DROP2 produced CLOSE"]})
        self.assertEqual(["DROP2 produced CLOSE"], report["blockers"])

    def test_research_release_blocks_when_curation_evidence_changes(self):
        error = "Curation evidence changed: review [CR-001]"
        command = CompletedProcess([], 1, json.dumps({"errors": [error]}), "")
        with patch.object(gate.subprocess, "run", return_value=command):
            report = self.check("research-library", probes=gate.AUTO_PROBES)
        self.assertEqual("BLOCKED", report["status"])
        self.assertIn(f"Curation evidence: {error}", report["blockers"])

    def test_concrete_evidence_and_exact_criteria_required(self):
        self.assertTrue(gate.reviewed_criteria(("Musical criterion",), self.entry))
        for change in ({"sources": []}, {"sources": [{"url": "https://example.org", "locator": "",
                                                       "supports": "A cadence"}]},
                       {"criteria": {"Musical criterion": 1}}, {"observations": ""}):
            with self.subTest(change=change):
                self.assertFalse(gate.reviewed_criteria(("Musical criterion",), {**self.entry, **change}))
        self.assertFalse(gate.reviewed_criteria(("Musical criterion",), self.entry, coach=True))

    def test_github_provenance_is_tied_to_revision_and_independent_reviewer(self):
        area, evidence = self.verify(*self.submission())
        self.assertEqual("desktop-voicing", area)
        self.assertEqual("reviewer", evidence["reviewer"])
        for kwargs in ({"self_review": True}, {"edited": True}, {"revision": "b" * 40}):
            with self.subTest(kwargs=kwargs), self.assertRaises(ValueError):
                self.verify(*self.submission(**kwargs))
        comment, pull = self.submission()
        comment["user"]["id"] = 2
        with self.assertRaises(ValueError):
            self.verify(comment, pull)

    def test_review_cannot_clear_an_unrelated_area_or_technical_failure(self):
        criteria = gate.requirements("recommendations", ())["AREA"]
        approval = {"reviews": {"AREA": {**self.entry, "criteria": dict.fromkeys(criteria, True)}}}
        self.assertEqual("READY", self.check("recommendations", acceptance=approval)["status"])
        self.assertEqual("BLOCKED", self.check("research-library", acceptance=approval)["status"])
        self.assertEqual("BLOCKED", self.check("recommendations", acceptance=approval,
                                               probes={"recommendations": lambda: ["broken"]})["status"])

    def test_release_checkout_state_ignores_inherited_git_context(self):
        with patch.dict(os.environ, {"GIT_DIR": "elsewhere/.git", "GIT_WORK_TREE": "elsewhere"}):
            with patch.object(gate.subprocess, "check_output", side_effect=[str(gate.ROOT), self.revision, b""]) as git:
                self.assertEqual(gate.checkout_state(), (self.revision, False))
        for call in git.call_args_list:
            self.assertEqual(call.kwargs["cwd"], gate.ROOT)
            self.assertNotIn("GIT_DIR", call.kwargs["env"])
            self.assertNotIn("GIT_WORK_TREE", call.kwargs["env"])

    def test_release_checkout_state_rejects_an_enclosing_git_repository(self):
        with patch.object(gate.subprocess, "check_output", return_value=str(gate.ROOT.parent)):
            with self.assertRaisesRegex(ValueError, "own STEPS Git checkout"):
                gate.checkout_state()

    def test_dirty_checkout_cannot_issue_release_verdict(self):
        with (patch.object(gate.sys, "argv", ["verify_musical_release"]),
              patch.object(gate, "checkout_state", return_value=(self.revision, True)),
              redirect_stderr(StringIO())):
            with self.assertRaises(SystemExit) as aborted:
                gate.main()
        self.assertEqual(2, aborted.exception.code)

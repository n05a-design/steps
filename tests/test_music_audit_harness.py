"""Negative tests for the audit gate itself."""

import json
from pathlib import Path
import subprocess
import sys
from tempfile import TemporaryDirectory
import unittest
from unittest.mock import patch

from scripts import audit_randomized_music as audit


class MusicAuditHarnessTest(unittest.TestCase):
    def test_reference_profiles_exercise_the_product(self):
        report = audit.run(1, 1, ("pitch", "chord-reference", "scale-reference", "harmonization"),
                           profile="smoke")
        self.assertEqual(report["gate"], "PASS", report["failures"][:3])
        self.assertEqual([area["passed"] for area in report["areas"].values()], [128, 372, 180, 1512])

    def test_generator_failure_preserves_progress_and_other_areas(self):
        broken = iter((ValueError("path that must not enter the report"), audit.Trial({}, 0, lambda: 0)))

        def generate(*args):
            result = next(broken)
            if isinstance(result, Exception):
                raise result
            return result

        with patch.dict(audit.PROBES, chords=generate):
            report = audit.run(1, 2, ("chords", "pitch"), profile="smoke")
        self.assertEqual(report["gate"], "ERROR")
        self.assertEqual(report["failures"][0]["classification"], "GENERATOR_DEFECT")
        self.assertEqual(report["areas"]["chords"]["passed"], 1)
        self.assertEqual(report["areas"]["pitch"]["passed"], 128)
        self.assertNotIn("path that must not enter", json.dumps(report))

    def test_parallel_areas_preserve_order_and_counts(self):
        areas = ("chords", "pitch", "transposition", "midi")
        serial = audit.run(7, 12, areas, profile="smoke")
        parallel = audit.run(7, 12, areas, profile="smoke", workers=3)
        self.assertEqual(serial["areas"], parallel["areas"])
        self.assertEqual(list(parallel["areas"]), list(areas))
        self.assertEqual(serial["gate"], parallel["gate"])

    def test_import_error_and_incomplete_timeout_cannot_pass(self):
        with patch.object(audit, "observe_reference", side_effect=ImportError("missing")):
            missing = audit.run(1, 1, ("pitch",), case="PITCH-060")
        self.assertEqual(missing["failures"][0]["classification"], "SETUP_ERROR")
        self.assertEqual(missing["gate"], "ERROR")
        timeout = audit.run(1, 1, ("pitch",), timeout=0)
        self.assertEqual(timeout["areas"]["pitch"]["timeout"], 1)
        self.assertEqual(timeout["areas"]["pitch"]["not_run"], 127)
        self.assertEqual(timeout["gate"], "ERROR")

    def test_final_case_cannot_pass_after_the_deadline(self):
        with patch.object(audit, "monotonic", side_effect=(0, 0, 2, 2)):
            report = audit.run(1, 1, ("pitch",), case="PITCH-060", timeout=1)
        row = report["failures"][0]
        self.assertEqual(row["status"], "timeout")
        self.assertEqual(report["gate"], "ERROR")
        self.assertEqual(row["replay"]["payload"]["input"], {"midi": 60})

    def test_hard_deadline_terminates_replay_and_preserves_input(self):
        case_id, question, expected = next(audit.references.cases("pitch", "smoke", 1))
        payload = audit.case_payload("pitch", case_id, question, expected)
        stopped = audit.replay_with_deadline(payload, 1, 0.000001)
        self.assertEqual(stopped["gate"], "ERROR")
        self.assertEqual(stopped["areas"]["pitch"]["timeout"], 1)
        self.assertEqual(stopped["failures"][0]["replay"]["payload"], payload)
        completed = audit.replay_with_deadline(payload, 1, 15)
        self.assertEqual(completed["gate"], "PASS")
        self.assertEqual(completed["deadline_mode"], "subprocess")

    def test_multiple_case_flags_do_not_discard_unknown_selector(self):
        result = subprocess.run([sys.executable, "-B", str(Path(audit.__file__)),
                                 "--case", "UNKNOWN", "--case", "PITCH-060"],
                                cwd=audit.ROOT, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 2)
        self.assertIn(b"--case must be supplied once", result.stderr)

    def test_replay_uses_saved_payload_and_rejects_tampering(self):
        with patch.object(audit, "observe_reference", return_value=[]):
            report = audit.run(1, 1, ("pitch",), case="PITCH-060")
        self.assertEqual(report["gate"], "FAIL")
        replay = report["failures"][0]["replay"]
        with TemporaryDirectory() as folder:
            source = Path(folder) / "replay.json"
            target = Path(folder) / "report.json"
            args = [sys.executable, "-B", str(Path(audit.__file__)), "--replay", str(source),
                    "--json-out", str(target)]
            audit.write_report(source, replay)
            result = subprocess.run(args, capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertEqual(json.loads(target.read_text(encoding="utf-8"))["areas"]["pitch"]["passed"], 1)
            replay["payload"]["expected"] = []
            audit.write_report(source, replay)
            result = subprocess.run(args, capture_output=True, timeout=15)
            self.assertEqual(result.returncode, 2, result.stderr)

    def test_each_random_area_replays_its_serialized_input(self):
        with patch.object(audit, "observe_random", return_value=[]):
            failed = audit.run(27, 1)
        self.assertEqual(len(failed["failures"]), len(audit.PROBES))
        for failure in failed["failures"]:
            area = failure["area"]
            payload = json.loads(json.dumps(failure["replay"]["payload"]))
            with self.subTest(area=area):
                with patch.dict(audit.PROBES, {area: lambda *_: self.fail("Replay regenerated the question")}):
                    report = audit.run(0, 1, (area,), replay=payload)
                self.assertEqual(report["gate"], "PASS", report["failures"])
                self.assertEqual(report["areas"][area]["passed"], 1)

    def test_optimized_self_test_rejects_mutated_fixture(self):
        code = (
            "import sys; "
            "from scripts import audit_randomized_music as audit; "
            "audit.references.FORMULAS[''] = '1 b3 5'; "
            "sys.argv = ['audit', '--self-test']; "
            "raise SystemExit(audit.main())"
        )
        result = subprocess.run([sys.executable, "-B", "-O", "-c", code],
                                cwd=audit.ROOT, capture_output=True, timeout=15)
        self.assertEqual(result.returncode, 3, result.stderr)
        self.assertEqual(json.loads(result.stdout)["classification"], "ORACLE_DEFECT")

    def test_unknown_case_has_an_explicit_result(self):
        report = audit.run(1, 1, ("pitch",), case="PITCH-128")
        self.assertEqual(report["gate"], "ERROR")
        self.assertEqual(report["failures"][0]["classification"], "UNKNOWN_CASE")



class MusicAuditFreshnessTest(unittest.TestCase):
    def test_time_revision_and_job_coverage_are_independent(self):
        from datetime import datetime, timedelta, timezone
        from unittest.mock import patch
        from scripts import check_music_audit_freshness as freshness

        now = datetime(2026, 11, 28, tzinfo=timezone.utc)
        revision = "a" * 40
        good = {"headSha": revision, "startedAt": (now - timedelta(hours=1)).isoformat(),
                "databaseId": 1, "conclusion": "success"}
        jobs = {"jobs": [{"name": name, "conclusion": "success"} for name in freshness.JOBS]}
        for run, details, expected in (
            (good, jobs, ("PASS", "PASS", "PASS")),
            ({**good, "headSha": "b" * 40}, jobs, ("REVISION_MISMATCH", "PASS", "REVISION_MISMATCH")),
            ({**good, "startedAt": (now - timedelta(hours=37)).isoformat()}, jobs, ("STALE", "STALE", "PASS")),
            (good, {"jobs": jobs["jobs"][:1]}, ("BLOCKED", "PASS", "PASS")),
        ):
            with self.subTest(expected=expected), patch.object(freshness, "github_json", side_effect=[[run], details]):
                report = freshness.check(36, now, revision)
                self.assertEqual(tuple(report[key] for key in ("status", "time_status", "revision_status")), expected)
        with patch.object(freshness, "github_json", return_value=[]):
            self.assertEqual(freshness.check(36, now, revision)["status"], "NOT_RUN")

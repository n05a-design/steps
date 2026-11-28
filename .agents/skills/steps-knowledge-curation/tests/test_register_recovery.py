"""Regression tests for register recovery using isolated fixtures."""

from hashlib import sha256
import json
import os
from pathlib import Path
import stat
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

SCRIPTS = Path(__file__).resolve().parents[1] / "scripts"
sys.path.insert(0, str(SCRIPTS))

import backup_knowledge
import check_source
import detect_duplicates
import extract_instructions
import register_paths
import validate_register


ORIGINAL = b"### OA-0001: Task\n* **Status:** `OPEN`\n"
CURRENT = b"### OA-0001: Task\n* **Status:** `IN_PROGRESS`\n"


class TestRegisterRecovery(unittest.TestCase):
    def setUp(self):
        tmp = tempfile.TemporaryDirectory()
        self.addCleanup(tmp.cleanup)
        self.base = Path(tmp.name).resolve()
        self.target = self.base / "register.md"
        self.target.write_bytes(ORIGINAL)
        self.backup = Path(backup_knowledge.backup_master(self.target)["backup"])
        self.target.write_bytes(CURRENT)

    def test_default_register_is_repository_canonical_and_ignores_legacy_env(self):
        canonical = Path(__file__).resolve().parents[4] / "docs" / "operations" / "OFFENE_ARBEITSAUFFORDERUNGEN.md"
        # Use a replacement mapping so Windows does not lose inherited empty Git values.
        with patch.object(os, "environ", {
            **os.environ,
            "LOCALAPPDATA": str(self.base),
            "STEPS_KNOWLEDGE_REGISTER": str(self.target),
        }):
            self.assertEqual(register_paths.master_path(), canonical)
        self.assertTrue(canonical.is_file())

    def test_cli_uses_explicit_register_override(self):
        env = os.environ.copy()
        env.pop("STEPS_KNOWLEDGE_REGISTER", None)
        result = subprocess.run(
            [
                sys.executable, "-B", str(SCRIPTS / "backup_knowledge.py"),
                "restore", str(self.backup), "--register", str(self.target),
            ],
            cwd=self.base, env=env, capture_output=True, text=True,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        restored = json.loads(result.stdout)
        self.assertEqual(self.target.read_bytes(), ORIGINAL)
        self.assertEqual(Path(restored["previous_backup"]).read_bytes(), CURRENT)

    def test_tampered_backup_leaves_current_register_intact(self):
        self.backup.write_bytes(ORIGINAL + b"\nExtra bytes\n")
        with self.assertRaisesRegex(ValueError, "does not match its manifest"):
            backup_knowledge.restore_master(self.backup, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)
        self.assertEqual(backup_knowledge.list_backups(self.backup.parent)[0]["integrity"], "INVALID")

    def test_arbitrary_and_legacy_files_are_not_restored(self):
        arbitrary = self.backup.parent / "random.md"
        arbitrary.write_bytes(ORIGINAL)
        with self.assertRaisesRegex(ValueError, "Unsupported backup name"):
            backup_knowledge.restore_master(arbitrary, self.target)
        legacy = self.backup.parent / "OFFENE_ARBEITSAUFFORDERUNGEN_20261112_100000.md"
        legacy.write_bytes(ORIGINAL)
        with self.assertRaises(ValueError):
            backup_knowledge.restore_master(legacy, self.target)
        inventory = {row["filename"]: row["integrity"] for row in backup_knowledge.list_backups(self.backup.parent)}
        self.assertEqual(inventory[legacy.name], "UNVERIFIED")
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_backup_from_other_directory_requires_explicit_selection(self):
        outside = self.base / "outside"
        copy = Path(backup_knowledge.backup_master(self.target, outside)["backup"])
        with self.assertRaisesRegex(ValueError, "selected backup directory"):
            backup_knowledge.restore_master(copy, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_invalid_register_rejected_even_with_matching_hash(self):
        self.target.write_bytes(b"# Notes without tasks\n")
        invalid = backup_knowledge.backup_master(self.target)["backup"]
        self.target.write_bytes(CURRENT)
        with self.assertRaisesRegex(ValueError, "Invalid register"):
            backup_knowledge.restore_master(invalid, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_restore_rejects_malformed_task_even_when_snapshot_hash_matches(self):
        self.target.write_bytes(ORIGINAL + b"\n### OA-10000: Malformed\n* **Status:** `UNKNOWN`\n")
        invalid = backup_knowledge.backup_master(self.target)["backup"]
        self.target.write_bytes(CURRENT)
        with self.assertRaisesRegex(ValueError, "Malformed OA task heading"):
            backup_knowledge.restore_master(invalid, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_restore_rejects_formatted_task_id(self):
        self.target.write_bytes(ORIGINAL + b"\n### `OA-0001`: Duplicate\n* **Status:** `INVALID`\n")
        invalid = backup_knowledge.backup_master(self.target)["backup"]
        self.target.write_bytes(CURRENT)
        with self.assertRaisesRegex(ValueError, "Malformed OA task heading"):
            backup_knowledge.restore_master(invalid, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_shared_backup_cannot_restore_other_register_implicitly(self):
        other = self.base / "other"
        other.mkdir()
        destination = other / self.target.name
        destination.write_bytes(CURRENT)
        inventory = backup_knowledge.list_backups(self.backup.parent, target_master=destination)
        self.assertEqual(inventory[0]["restore_scope"], "OTHER_REGISTER")
        with self.assertRaisesRegex(ValueError, "another register path"):
            backup_knowledge.restore_master(self.backup, destination, backup_dir=self.backup.parent)
        self.assertEqual(destination.read_bytes(), CURRENT)
        backup_knowledge.restore_master(
            self.backup, destination, backup_dir=self.backup.parent, allow_other_register=True,
        )
        self.assertEqual(destination.read_bytes(), ORIGINAL)

    def test_replacement_git_repository_at_same_path_has_different_identity(self):
        project = self.base / "checkout"
        shared = self.base / "shared"
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        register = project / self.target.name
        register.write_bytes(ORIGINAL)
        snapshot = Path(backup_knowledge.backup_master(register, shared)["backup"])
        project.rename(self.base / "previous_checkout")
        project.mkdir()
        subprocess.run(["git", "init", "-q", str(project)], check=True)
        register.write_bytes(CURRENT)
        inventory = backup_knowledge.list_backups(shared, target_master=register)
        self.assertEqual(inventory[0]["restore_scope"], "OTHER_REGISTER")
        with self.assertRaisesRegex(ValueError, "another register path or checkout"):
            backup_knowledge.restore_master(snapshot, register, backup_dir=shared)
        self.assertEqual(register.read_bytes(), CURRENT)

    def test_incomplete_completion_evidence_requires_recovery_override(self):
        incomplete = b"### OA-0001: Closure\n* **Status:** `DONE_VERIFIED`\n"
        self.target.write_bytes(incomplete)
        snapshot = Path(backup_knowledge.backup_master(self.target)["backup"])
        self.target.write_bytes(CURRENT)
        inventory = backup_knowledge.list_backups(self.backup.parent, target_master=self.target)
        entry = next(item for item in inventory if item["path"] == str(snapshot))
        self.assertEqual(entry["integrity"], "VERIFIED")
        self.assertEqual(entry["restore_scope"], "MATCHED")
        self.assertEqual(entry["completion_evidence"], "INCOMPLETE_FIELDS")
        with self.assertRaisesRegex(ValueError, "incomplete completion evidence"):
            backup_knowledge.restore_master(snapshot, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)
        result = backup_knowledge.restore_master(snapshot, self.target, allow_incomplete_evidence=True)
        self.assertEqual(result["completion_evidence"], "INCOMPLETE_FIELDS")
        self.assertEqual(self.target.read_bytes(), incomplete)

    def test_version_two_path_binding_requires_review(self):
        manifest = self.backup.with_suffix(".md.json")
        record = json.loads(manifest.read_text(encoding="utf-8"))
        record["version"] = 2
        del record["register_identity"]
        manifest.write_text(json.dumps(record), encoding="utf-8")
        inventory = backup_knowledge.list_backups(self.backup.parent, target_master=self.target)
        self.assertEqual(inventory[0]["restore_scope"], "UNBOUND")
        with self.assertRaisesRegex(ValueError, "unbound"):
            backup_knowledge.restore_master(self.backup, self.target)
        backup_knowledge.restore_master(self.backup, self.target, allow_other_register=True)
        self.assertEqual(self.target.read_bytes(), ORIGINAL)

    def test_list_rejects_missing_manifest_register(self):
        manifest = self.backup.with_suffix(".md.json")
        record = json.loads(manifest.read_text(encoding="utf-8"))
        del record["register"]
        manifest.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(backup_knowledge.list_backups(self.backup.parent)[0]["integrity"], "INVALID")
        with self.assertRaisesRegex(ValueError, "no valid register filename"):
            backup_knowledge.restore_master(self.backup, self.target)

    def test_version_one_remains_recoverable_after_review(self):
        manifest = self.backup.with_suffix(".md.json")
        record = json.loads(manifest.read_text(encoding="utf-8"))
        record["version"] = 1
        del record["register_path"]
        manifest.write_text(json.dumps(record), encoding="utf-8")
        self.assertEqual(backup_knowledge.list_backups(self.backup.parent)[0]["restore_scope"], "UNBOUND")
        with self.assertRaisesRegex(ValueError, "unbound"):
            backup_knowledge.restore_master(self.backup, self.target)
        backup_knowledge.restore_master(self.backup, self.target, allow_other_register=True)
        self.assertEqual(self.target.read_bytes(), ORIGINAL)

    @unittest.skipIf(os.name == "nt", "POSIX register permissions")
    def test_restore_preserves_regular_target_mode(self):
        self.target.chmod(0o640)
        backup_knowledge.restore_master(self.backup, self.target)
        self.assertEqual(stat.S_IMODE(self.target.stat().st_mode), 0o640)

    def test_existing_restore_lock_leaves_current_register_intact(self):
        lock = self.target.with_name(f".{self.target.name}.restore.lock")
        lock.write_text("Active restore", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "Restore lock already exists"):
            backup_knowledge.restore_master(self.backup, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)
        self.assertEqual(lock.read_text(encoding="utf-8"), "Active restore")

    def test_missing_manifest_prevents_restore(self):
        self.backup.with_suffix(".md.json").unlink()
        with self.assertRaisesRegex(ValueError, "manifest missing"):
            backup_knowledge.restore_master(self.backup, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_replace_failure_preserves_register_and_recovery_copy(self):
        with patch.object(backup_knowledge.os, "replace", side_effect=PermissionError("busy")):
            with self.assertRaisesRegex(PermissionError, "busy"):
                backup_knowledge.restore_master(self.backup, self.target)
        self.assertEqual(self.target.read_bytes(), CURRENT)
        self.assertFalse(list(self.base.glob(".register.md.*")))
        copies = list(self.backup.parent.glob("*.md"))
        self.assertEqual(len(copies), 2)
        self.assertIn(CURRENT, [copy.read_bytes() for copy in copies])

    def test_target_and_backup_symlinks_are_rejected(self):
        external = self.base / "other" / "register.md"
        external.parent.mkdir()
        external.write_bytes(CURRENT)
        alias_dir = self.base / "alias"
        alias_dir.mkdir()
        target_alias = alias_dir / self.target.name
        try:
            target_alias.symlink_to(external)
            (alias_dir / "backups").symlink_to(self.backup.parent, target_is_directory=True)
        except OSError as exc:
            self.skipTest(f"Symlinks unavailable: {exc}")
        with self.assertRaisesRegex(ValueError, "regular file"):
            backup_knowledge.restore_master(self.backup, target_alias, backup_dir=self.backup.parent)
        with self.assertRaisesRegex(ValueError, "cannot redirect"):
            backup_knowledge.restore_master(self.backup, target_alias)
        self.assertEqual(external.read_bytes(), CURRENT)
        self.assertTrue(target_alias.is_symlink())


class TestSourceBoundaries(unittest.TestCase):
    def test_links_cannot_expose_files_outside_source_scope(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            base = root / "intake"
            base.mkdir()
            outside = root / "outside.md"
            outside.write_text("TODO: Do not accept text as an instruction.\n", encoding="utf-8")
            inside = base / "inside.md"
            inside.write_bytes(outside.read_bytes())
            escaped = base / "escaped.md"
            try:
                escaped.symlink_to(outside)
            except OSError as exc:
                self.skipTest(f"Symlinks unavailable: {exc}")
            with self.assertRaisesRegex(ValueError, "outside the allowed directory"):
                check_source.check_file(escaped, base)
            with self.assertRaisesRegex(ValueError, "outside the allowed directory"):
                extract_instructions.extract_from_file(escaped, base)
            self.assertEqual(detect_duplicates.is_duplicate(inside, base), [])

    def test_duplicate_scan_reports_unreadable_candidate(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source = root / "source.md"
            copy = root / "copy.md"
            source.write_bytes(b"same data")
            copy.write_bytes(source.read_bytes())
            original_open = Path.open

            def open_file(path, *args, **kwargs):
                if path == copy:
                    raise PermissionError("simulated read failure")
                return original_open(path, *args, **kwargs)

            with patch.object(Path, "open", open_file):
                with self.assertRaisesRegex(PermissionError, "simulated read failure"):
                    detect_duplicates.is_duplicate(source, root, intake_dir=root)

    def test_duplicate_scan_rejects_target_outside_intake(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            intake = root / "intake"
            intake.mkdir()
            source = root / "source.md"
            source.touch()
            with self.assertRaisesRegex(ValueError, "outside the allowed directory"):
                detect_duplicates.is_duplicate(source, root, intake_dir=intake)

    def test_candidate_extraction_reports_utf16_and_filters_unrelated_open_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "utf16.txt"
            source.write_text("The result must first be tested.\nDie Tür ist offen.\n", encoding="utf-16")
            candidates = extract_instructions.extract_from_file(source, root)
            self.assertEqual([(item["line"], item["category"]) for item in candidates], [(1, "NORMATIVE_MUST_EN")])

    def test_extraction_report_binds_reviewed_bytes(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            text = b"TODO: Verify the example.\r\n"
            first, second = root / "A.txt", root / "B.txt"
            for source in (first, second):
                source.write_bytes(text)
            expected = sha256(text).hexdigest()
            reports = [extract_instructions.extract_report(source, root, expected_sha256=expected)
                       for source in (first, second)]
            self.assertEqual(reports[0]["source"], {
                "path": str(first), "size_bytes": len(text), "sha256": expected,
            })
            self.assertEqual(reports[1]["source"]["path"], str(second))
            self.assertEqual(reports[0]["candidates"], reports[1]["candidates"])
            first.write_bytes(b"TODO: Another version.\n")
            with self.assertRaisesRegex(ValueError, "expected intake version"):
                extract_instructions.extract_report(first, root, expected_sha256=expected)

    @unittest.skipIf(os.name == "nt", "Windows filenames cannot contain newlines")
    def test_machine_outputs_round_trip_a_filename_with_newline(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp).resolve()
            source, duplicate = root / "source.txt", root / "A\nB.txt"
            for path in (source, duplicate):
                path.write_text("Same bytes.", encoding="utf-8")
            for name, args, expected in (
                ("check_source.py", [duplicate, root], str(duplicate)),
                ("detect_duplicates.py", [source, root], [str(duplicate)]),
            ):
                with self.subTest(name=name):
                    command = [sys.executable, "-B", str(SCRIPTS / name), *map(str, args)]
                    plain = subprocess.check_output(command, text=True)
                    self.assertIn(r"A\nB.txt", plain)
                    decoded = json.loads(subprocess.check_output(command + ["--json"], text=True))
                    self.assertEqual(decoded.get("path") if isinstance(decoded, dict) else decoded, expected)

    def test_extraction_does_not_treat_midi_as_readable_text(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            source = root / "corpus.mid"
            source.write_bytes(b"TODO: misleading ASCII within a binary input")
            with self.assertRaisesRegex(ValueError, "reviewed text derivative"):
                extract_instructions.extract_from_file(source, root)


class TestRegisterNegativeCases(unittest.TestCase):
    def test_indented_duplicate(self):
        report = validate_register.validate_content(ORIGINAL.decode() + "   ### OA-0001: Duplicate\n* **Status:** `OPEN`\n")
        self.assertIn("Duplicate OA-ID found: OA-0001", report["errors"])

    def test_formatted_id_cannot_hide_in_a_heading(self):
        for ident in ("`OA-0001`", "**OA-0001**", "_OA-0001_"):
            with self.subTest(ident=ident):
                report = validate_register.validate_content(
                    ORIGINAL.decode() + f"\n### {ident}: Duplicate\n* **Status:** `OPEN`\n"
                )
                self.assertTrue(any("Malformed OA task heading" in error for error in report["errors"]))

    def test_not_applicable_requires_a_reason(self):
        entry = "### OA-0001: Inapplicable\n* **Status:** `NOT_APPLICABLE`\n"
        for reason in ("", "* **Begründung:** TBD\n", "* **Begründung:** [Platzhalter]\n"):
            with self.subTest(reason=reason):
                report = validate_register.validate_content(entry + reason)
                self.assertTrue(report["errors"])
        report = validate_register.validate_content(entry + "* **Begründung:** Scope covers text sources only.\n")
        self.assertFalse(report["errors"])

    def test_alternate_markdown_heading_cannot_hide_duplicate_task(self):
        for heading in ("OA-0001: Duplicate\n---", "<h3>OA-0001: Duplicate</h3>"):
            with self.subTest(heading=heading):
                content = ORIGINAL.decode() + f"\n## Other\n\n{heading}\n* **Status:** `OPEN`\n"
                self.assertTrue(validate_register.validate_content(content)["errors"])

    def test_canonical_python_and_cli_share_commit_validation(self):
        canonical = register_paths.master_path()
        original = canonical.read_text(encoding="utf-8")
        known = "5c3e829d53e8f2cfc609eddd0d3c597c862a9698"
        self.assertIn(known, original)
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp) / canonical.name
            target.write_text(original.replace(known, "1" * 40), encoding="utf-8")
            with (patch.object(validate_register, "master_path", return_value=target),
                  patch.object(sys, "argv", ["validate_register.py", "--json"]),
                  patch("builtins.print") as output):
                expected = validate_register.validate_master_file(target)
                self.assertEqual(expected["errors_count"], 1)
                with self.assertRaises(SystemExit) as stopped:
                    validate_register.main()
                self.assertEqual(stopped.exception.code, 1)
                self.assertEqual(json.loads(output.call_args.args[0]), expected)

    def test_canonical_register_is_independent_of_inherited_git_dir(self):
        with tempfile.TemporaryDirectory() as tmp:
            subprocess.run(["git", "init", "-q", tmp], check=True)
            result = subprocess.run(
                [sys.executable, "-B", str(SCRIPTS / "validate_register.py"), "--json"],
                env={**os.environ, "GIT_DIR": str(Path(tmp) / ".git")},
                capture_output=True, text=True,
            )
            self.assertEqual(result.returncode, 0, result.stderr or result.stdout)
            self.assertEqual(json.loads(result.stdout)["errors_count"], 0)

    def test_hidden_status_cannot_satisfy_required_field(self):
        content = "### OA-0001: Task\n<!--\n* **Status:** `OPEN`\n-->\n"
        report = validate_register.validate_content(content)
        self.assertIn("OA-0001: expected exactly one status field.", report["errors"])

    def test_unclosed_blocks_cannot_hide_appended_tasks(self):
        for marker in ("```", "<!--"):
            with self.subTest(marker=marker):
                report = validate_register.validate_content(
                    ORIGINAL.decode() + marker + "\n### OA-0002: Hidden\n"
                )
                self.assertIn("Unclosed fenced block or HTML comment in task register.", report["errors"])

    def test_evidence_must_reference_available_commit_when_requested(self):
        content = """### OA-0001: Fabricated
* **Status:** `DONE_VERIFIED`
* **Commit:** `0123456789abcdef0123456789abcdef01234567`
* **Prüfung:** Test suite
* **Abnahmebeleg:** Review record
* **Abnahmekriterien:** Test suite passes
"""
        report = validate_register.validate_content(content, verify_commits=True)
        self.assertEqual(report["errors_count"], 1, report["errors"])
        self.assertIn("evidence commit is unavailable", report["errors"][0])
        report = validate_register.validate_content(content.replace("0123456789abcdef0123456789abcdef01234567", "0" * 40))
        self.assertIn("OA-0001: DONE_VERIFIED requires a valid Commit field.", report["errors"])

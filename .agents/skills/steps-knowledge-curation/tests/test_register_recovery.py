"""Regression tests for register recovery using isolated fixtures."""

import json
import os
from pathlib import Path
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

    def test_no_default_restore_to_working_directory(self):
        env = os.environ.copy()
        env.pop("LOCALAPPDATA", None)
        env.pop("STEPS_KNOWLEDGE_REGISTER", None)
        before = set(self.base.iterdir())
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "backup_knowledge.py"), "restore", str(self.backup)],
            cwd=self.base, env=env, capture_output=True, text=True,
        )
        self.assertNotEqual(result.returncode, 0)
        self.assertIn("STEPS_KNOWLEDGE_REGISTER", result.stderr)
        self.assertEqual(set(self.base.iterdir()), before)
        self.assertEqual(self.target.read_bytes(), CURRENT)

    def test_cli_uses_configured_absolute_register(self):
        env = {**os.environ, "STEPS_KNOWLEDGE_REGISTER": str(self.target)}
        result = subprocess.run(
            [sys.executable, "-B", str(SCRIPTS / "backup_knowledge.py"), "restore", str(self.backup)],
            cwd=self.base, env=env, capture_output=True, check=True,
        )
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

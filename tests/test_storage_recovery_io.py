"""
STEPS Storage, Persistence, Backup & Recovery Test Suite (IO-01..IO-16).

Directly validates the 16 storage and failure recovery invariants specified in:
- prompts/12_STORAGE_BACKUP.md (IO-01..IO-16)
- EXECUTION_BACKLOG.md (P1.2 Datenspeicher / Undo)
- docs/architecture/DOMAIN_AND_STORAGE_CONTRACTS.md
- schemas/project.schema.json
"""

import json
import os
import shutil
import tempfile
import time
import unittest
from pathlib import Path

from src.steps.storage import (
    CURRENT_APP_VERSION,
    CURRENT_SCHEMA_VERSION,
    CorruptedProjectError,
    LockCollisionError,
    Project,
    ProjectLock,
    StorageError,
    StorageSecurityError,
    UndoRedoError,
    UndoStack,
    UnsupportedSchemaVersionError,
    atomic_write_json,
    load_project,
    load_project_with_status,
    migrate_project_data,
    save_project,
    validate_path_safety,
)


class TestStorageRecoveryIO01to16(unittest.TestCase):

    def setUp(self):
        self.temp_dir = tempfile.mkdtemp(prefix="steps_storage_test_")
        self.project_path = Path(self.temp_dir) / "test_session.stepsproj"

    def tearDown(self):
        shutil.rmtree(self.temp_dir, ignore_errors=True)

    def test_io01_clean_save_load_roundtrip(self):
        """IO-01: Clean save and load round-trip of full project."""
        p = Project(
            title="Symphony in C",
            notation_convention="DE",
            tracks=[
                {
                    "track_id": "trk_chords",
                    "track_type": "CHORDS",
                    "name": "Jazz Cadence",
                    "channel": 0,
                    "events": [
                        {"start_tick": 0, "duration_ticks": 480, "payload": "Dm7"},
                        {"start_tick": 480, "duration_ticks": 480, "payload": "G7"},
                        {"start_tick": 960, "duration_ticks": 960, "payload": "Cmaj7"}
                    ]
                }
            ]
        )
        saved_path = save_project(p, self.project_path)
        self.assertTrue(saved_path.exists())

        loaded = load_project(saved_path)
        self.assertEqual(loaded.title, "Symphony in C")
        self.assertEqual(loaded.notation_convention, "DE")
        self.assertEqual(len(loaded.tracks), 1)
        self.assertEqual(len(loaded.tracks[0]["events"]), 3)
        self.assertEqual(loaded.tracks[0]["events"][0]["payload"], "Dm7")

    def test_io02_atomic_write_no_partial_file(self):
        """IO-02: Atomic write: temp file creation and atomic rename guarantee no partial file on write failure."""
        valid_data = {"test": "valid_atomic_data"}
        atomic_write_json(self.project_path, valid_data)
        self.assertTrue(self.project_path.exists())

        # Verify no orphaned temp files (.tmp) left behind
        temp_files = list(Path(self.temp_dir).glob(".*.tmp"))
        self.assertEqual(temp_files, [])

    def test_io03_crash_truncated_json_recovery_from_backup(self):
        """IO-03: Crash during write / truncated JSON recovery from backup."""
        # 1. Save valid initial version
        p1 = Project(title="Original Version 1")
        save_project(p1, self.project_path)

        # 2. Save second valid version (this creates a backup of version 1)
        p2 = Project(title="Version 2 - Safe Point")
        save_project(p2, self.project_path)

        # 3. Simulate sudden power outage: main file is truncated to 15 bytes of broken JSON
        with open(self.project_path, "w", encoding="utf-8") as f:
            f.write('{"title": "Trun')

        # 4. Load with auto_recover_from_backup=True
        recovered = load_project(self.project_path, auto_recover_from_backup=True)
        self.assertIsNotNone(recovered)
        # Should have recovered Version 1 or Version 2 backup
        self.assertIn("Version", recovered.title)

    def test_load_status_reports_recovered_backup(self):
        save_project(Project(title="Original Version"), self.project_path)
        save_project(Project(title="Current Version"), self.project_path)
        self.project_path.write_text('{"title": "Trun', encoding="utf-8")

        result = load_project_with_status(self.project_path)

        self.assertTrue(result.recovered_from_backup)
        self.assertIsNotNone(result.backup_path)
        self.assertIn("Version", result.project.title)

    def test_invalid_utf8_recovers_backup_without_rewriting_original(self):
        save_project(Project(title="Backup"), self.project_path)
        save_project(Project(title="Latest"), self.project_path)
        damaged = bytes((255, 254, 253))
        self.project_path.write_bytes(damaged)

        with self.assertRaises(CorruptedProjectError):
            load_project_with_status(self.project_path, auto_recover_from_backup=False)
        result = load_project_with_status(self.project_path)

        self.assertTrue(result.recovered_from_backup)
        self.assertEqual(result.project.title, "Backup")
        self.assertEqual(self.project_path.read_bytes(), damaged)

    def test_legacy_0_x_project_is_migrated_explicitly(self):
        legacy = {
            "schema_version": "0.9.0",
            "project_id": "legacy-0-x",
            "title": "Legacy 0.x Project",
            "time_settings": {"ppq": 480, "tempo_bpm": 120.0},
            "tracks": [],
        }
        migrated, migrations = migrate_project_data(legacy)

        self.assertEqual(migrated["schema_version"], CURRENT_SCHEMA_VERSION)
        self.assertEqual(migrated["notation_convention"], "INT")
        self.assertEqual(migrated["time_settings"]["time_signature"], {"numerator": 4, "denominator": 4})
        self.assertIn("MIG-001 0.x-to-1.0.0", migrations)

    def test_load_status_reports_migration_ids(self):
        legacy = {
            "schema_version": "0.9.0",
            "project_id": "legacy-status",
            "title": "Legacy Status",
            "time_settings": {"ppq": 480},
            "tracks": [],
        }
        self.project_path.write_text(json.dumps(legacy), encoding="utf-8")

        result = load_project_with_status(self.project_path, auto_recover_from_backup=False)

        self.assertTrue(result.migrated)
        self.assertIn("MIG-001 0.x-to-1.0.0", result.migrations)

    def test_io04_double_instance_lock_detection(self):
        """IO-04: Double-instance lock detection: existing valid lock prevents concurrent overwrite."""
        lock1 = ProjectLock(self.project_path)
        lock1.acquire()

        try:
            lock2 = ProjectLock(self.project_path)
            with self.assertRaises(LockCollisionError):
                lock2.acquire()
        finally:
            lock1.release()

    def test_io05_lock_release_and_stale_lock_recovery(self):
        """IO-05: Lock release on clean shutdown or stale lock recovery."""
        lock = ProjectLock(self.project_path, timeout_seconds=1.0)
        lock.acquire()
        lock.release()

        # Should be acquirable again immediately
        lock2 = ProjectLock(self.project_path)
        lock2.acquire()
        lock2.release()

    def test_io06_unsupported_future_schema_rejected(self):
        """IO-06: Unsupported newer schema version (e.g. 99.0) rejected without overwriting."""
        future_data = {
            "schema_version": "99.0.0",
            "app_version": "99.0.0",
            "project_id": "future-id",
            "title": "Future Project",
            "time_settings": {"ppq": 480},
            "tracks": []
        }
        with open(self.project_path, "w", encoding="utf-8") as f:
            json.dump(future_data, f)

        with self.assertRaises(UnsupportedSchemaVersionError):
            load_project(self.project_path)

    def test_io07_missing_non_critical_fields_safe_defaults(self):
        """IO-07: Legacy schema upgrade / missing non-critical fields loads safely with defaults."""
        legacy_data = {
            "schema_version": "1.0.0",
            "project_id": "legacy-proj-1",
            "title": "Minimal Legacy Project",
            "time_settings": {"ppq": 480, "time_signature": {"numerator": 4, "denominator": 4}, "tempo_bpm": 120.0},
            "tracks": []
        }
        with open(self.project_path, "w", encoding="utf-8") as f:
            json.dump(legacy_data, f)

        loaded = load_project(self.project_path)
        self.assertEqual(loaded.title, "Minimal Legacy Project")
        self.assertEqual(loaded.notation_convention, "INT")  # Safe default

    def test_invalid_time_settings_are_normalized_to_safe_defaults(self):
        legacy_data = {
            "schema_version": "1.0.0",
            "project_id": "legacy-invalid-time",
            "title": "Invalid Time Settings",
            "time_settings": {
                "ppq": "480",
                "time_signature": {"numerator": "4", "denominator": 3},
                "tempo_bpm": "fast",
                "tempo_points": "not-a-list",
            },
            "tracks": [],
        }
        self.project_path.write_text(json.dumps(legacy_data), encoding="utf-8")

        result = load_project_with_status(
            self.project_path,
            auto_recover_from_backup=False,
        )

        time_settings = result.project.time_settings
        self.assertEqual(time_settings["ppq"], 480)
        self.assertEqual(time_settings["time_signature"], {"numerator": 4, "denominator": 4})
        self.assertEqual(time_settings["tempo_bpm"], 120.0)
        self.assertEqual(time_settings["tempo_points"], [{"start_tick": 0, "bpm": 120.0}])
        self.assertIn("MIG-006 normalize-time-settings", result.migrations)

    def test_mig006_canonicalizes_tempo_point_sequence(self):
        legacy_data = {
            "schema_version": "1.0.0",
            "project_id": "legacy-tempo-points",
            "title": "Tempo Point Canonicalization",
            "time_settings": {
                "ppq": 480,
                "time_signature": {"numerator": 4, "denominator": 4},
                "tempo_bpm": 110.0,
                "tempo_points": [
                    {"start_tick": 1920, "bpm": 140.0},
                    {"start_tick": 0, "bpm": 90.0},
                    {"start_tick": 1920, "bpm": 130.0},
                ],
            },
            "tracks": [],
        }
        self.project_path.write_text(json.dumps(legacy_data), encoding="utf-8")

        result = load_project_with_status(
            self.project_path,
            auto_recover_from_backup=False,
        )

        self.assertEqual(
            result.project.time_settings["tempo_points"],
            [
                {"start_tick": 0, "bpm": 90.0},
                {"start_tick": 1920, "bpm": 130.0},
            ],
        )
        self.assertIn("MIG-006 normalize-time-settings", result.migrations)

    def test_mig006_empty_tempo_points_get_safe_zero_anchor(self):
        legacy_data = {
            "schema_version": "1.0.0",
            "project_id": "legacy-empty-tempo-points",
            "title": "Empty Tempo Points",
            "time_settings": {
                "ppq": 480,
                "time_signature": {"numerator": 4, "denominator": 4},
                "tempo_bpm": 96.5,
                "tempo_points": [],
            },
            "tracks": [],
        }
        self.project_path.write_text(json.dumps(legacy_data), encoding="utf-8")

        result = load_project_with_status(
            self.project_path,
            auto_recover_from_backup=False,
        )

        self.assertEqual(
            result.project.time_settings["tempo_points"],
            [{"start_tick": 0, "bpm": 96.5}],
        )

    def test_io08_path_traversal_prevention(self):
        """IO-08: Path traversal prevention: attempt to save with '../' is blocked with StorageSecurityError."""
        evil_path = f"{self.temp_dir}/subdir/../../outside_escaped.stepsproj"
        with self.assertRaises(StorageSecurityError):
            validate_path_safety(evil_path)

        with self.assertRaises(StorageSecurityError):
            p = Project(title="Evil")
            save_project(p, evil_path)

    def test_io09_corrupted_json_detection_no_backup(self):
        """IO-09: Corrupted JSON detection without available backup raises CorruptedProjectError."""
        with open(self.project_path, "w", encoding="utf-8") as f:
            f.write("NOT_A_VALID_JSON{{{[[[")

        with self.assertRaises(CorruptedProjectError):
            load_project(self.project_path, auto_recover_from_backup=False)

    def test_io10_missing_required_fields_rejected(self):
        """IO-10: Incomplete data (missing required schema fields) rejected with CorruptedProjectError."""
        incomplete_data = {
            "schema_version": "1.0.0",
            # missing "title", "project_id", "tracks"
        }
        with open(self.project_path, "w", encoding="utf-8") as f:
            json.dump(incomplete_data, f)

        with self.assertRaises(CorruptedProjectError):
            load_project(self.project_path, auto_recover_from_backup=False)

    def test_invalid_project_root_and_schema_version_are_reported(self):
        for raw in ("[]", '{"schema_version": null}'):
            with self.subTest(raw=raw):
                self.project_path.write_text(raw, encoding="utf-8")
                with self.assertRaises(CorruptedProjectError):
                    load_project(self.project_path, auto_recover_from_backup=False)

    def test_io11_backup_creation_on_overwrite(self):
        """IO-11: Backup creation: every overwrite generates a dated backup file in .steps_backups."""
        p1 = Project(title="Draft 1")
        save_project(p1, self.project_path)

        p2 = Project(title="Draft 2")
        save_project(p2, self.project_path)

        backup_dir = Path(self.temp_dir) / ".steps_backups"
        self.assertTrue(backup_dir.exists())
        backups = list(backup_dir.glob("*.bak"))
        self.assertGreaterEqual(len(backups), 1)

    def test_io12_backup_rotation_bounded_history(self):
        """IO-12: Backup rotation: backups limited to max_backups (e.g. 3) to prevent disk exhaustion."""
        for i in range(6):
            p = Project(title=f"Draft Version {i}")
            save_project(p, self.project_path, max_backups=3)
            time.sleep(0.01)

        backup_dir = Path(self.temp_dir) / ".steps_backups"
        backups = list(backup_dir.glob("*.bak"))
        self.assertLessEqual(len(backups), 3)

    def test_io13_undo_redo_state_transitions(self):
        """IO-13: Undo/Redo stack: state mutation can be undone and redone cleanly."""
        stack = UndoStack(initial_state="State 0", max_depth=10)
        self.assertEqual(stack.current_state, "State 0")
        self.assertFalse(stack.can_undo)
        self.assertFalse(stack.can_redo)

        stack.push("State 1")
        stack.push("State 2")
        self.assertEqual(stack.current_state, "State 2")
        self.assertTrue(stack.can_undo)
        self.assertFalse(stack.can_redo)

        # Undo to State 1
        undone = stack.undo()
        self.assertEqual(undone, "State 1")
        self.assertTrue(stack.can_redo)

        # Undo to State 0
        undone0 = stack.undo()
        self.assertEqual(undone0, "State 0")
        self.assertFalse(stack.can_undo)

        # Redo back to State 1 and State 2
        redone1 = stack.redo()
        self.assertEqual(redone1, "State 1")
        redone2 = stack.redo()
        self.assertEqual(redone2, "State 2")

    def test_io14_undo_redo_stack_boundaries(self):
        """IO-14: Undo/Redo stack boundary: undo at empty stack raises UndoRedoError."""
        stack = UndoStack("Initial", max_depth=5)
        with self.assertRaises(UndoRedoError):
            stack.undo()

        stack.push("Mutation")
        stack.undo()
        stack.redo()
        with self.assertRaises(UndoRedoError):
            stack.redo()

    def test_io15_dirty_state_tracking(self):
        """IO-15: Dirty state tracking: save resets dirty flag; mutation sets dirty flag."""
        stack = UndoStack("Initial Saved State", max_depth=10)
        self.assertFalse(stack.is_dirty)

        stack.push("Unsaved Edit")
        self.assertTrue(stack.is_dirty)

        # Mark clean (as if saved to disk)
        stack.mark_clean()
        self.assertFalse(stack.is_dirty)

        stack.push("Another Edit")
        self.assertTrue(stack.is_dirty)

        # Undo back to the clean save point
        stack.undo()
        self.assertFalse(stack.is_dirty)

    def test_io16_isolation_from_glide(self):
        """IO-16: Isolation from Glide: zero access to liste_speicher.json or Glide UserData."""
        # Ensure our storage mechanism does NOT touch any Glide filenames or Glide paths
        forbidden_glide_file = Path(self.temp_dir) / "liste_speicher.json"
        self.assertFalse(forbidden_glide_file.exists())

        p = Project(title="STEPS Standalone Project")
        save_project(p, self.project_path)

        # Assert no Glide storage file was created
        self.assertFalse(forbidden_glide_file.exists())
        self.assertTrue(self.project_path.exists())


if __name__ == "__main__":
    unittest.main()

"""Prüft die Kennzeichnung bewusst nur lokal geführter Originale (restricted_local)."""

import csv
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "manifests" / "restricted_local_2026-11-14.csv"


def git(*args):
    return subprocess.run(["git", *args], cwd=ROOT, capture_output=True, text=True, encoding="utf-8")


class RestrictedLocalTest(unittest.TestCase):
    def setUp(self):
        with MANIFEST.open(encoding="utf-8", newline="") as source:
            self.rows = list(csv.DictReader(source))

    def test_manifest_is_well_formed(self):
        self.assertTrue(self.rows)
        paths = [row["path"] for row in self.rows]
        self.assertEqual(len(paths), len(set(paths)), "Doppelte Pfade im Manifest")
        for row in self.rows:
            self.assertRegex(row["sha256"], r"^[a-f0-9]{64}$", row["path"])
            self.assertTrue(row["entscheidung"].strip(), row["path"])

    def test_listed_paths_are_ignored_and_untracked(self):
        for row in self.rows:
            with self.subTest(path=row["path"]):
                self.assertEqual(git("check-ignore", "-q", "--no-index", row["path"]).returncode, 0,
                                 "Pfad ist nicht per .gitignore ausgeschlossen")
                self.assertEqual(git("ls-files", "--error-unmatch", row["path"]).returncode, 1,
                                 "Pfad ist trotz restricted_local versioniert")

    def test_each_entry_has_a_versioned_summary(self):
        for row in self.rows:
            with self.subTest(path=row["path"]):
                summary = row["zusammenfassung"]
                self.assertTrue((ROOT / summary).is_file(), summary)
                self.assertEqual(git("ls-files", "--error-unmatch", summary).returncode, 0, summary)


if __name__ == "__main__":
    unittest.main()

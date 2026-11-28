"""Negative fixtures for the Shell manifest, isolated from the checkout."""

import json
from pathlib import Path
from tempfile import TemporaryDirectory
import unittest

from glide_shell.selftest import check_manifest
from scripts.materialize_shell_check_resources import git, SHELL


class ShellCheckoutContractTests(unittest.TestCase):
    def test_manifest_detects_crlf_in_a_synthetic_copy(self):
        manifest = git("cat-file", "blob", f"HEAD:{SHELL}/SHELL_MANIFEST.json")
        entries = json.loads(manifest)["dateien"]
        with TemporaryDirectory() as temporary:
            folder = Path(temporary)
            (folder / "SHELL_MANIFEST.json").write_bytes(manifest)
            for name in entries:
                target = folder / name
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes(git("cat-file", "blob", f"HEAD:{SHELL}/{name}"))
            self.assertIn(f"{len(entries)} files match", check_manifest(folder=folder))
            changed = folder / "AI_GUIDE_NEW_PROJECTS.md"
            original = changed.read_bytes()
            self.assertIn(b"\n", original)
            changed.write_bytes(original.replace(b"\n", b"\r\n"))
            with self.assertRaisesRegex(AssertionError, "AI_GUIDE_NEW_PROJECTS.md: modified"):
                check_manifest(folder=folder)

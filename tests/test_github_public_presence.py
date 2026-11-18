"""Tests for prepared GitHub public-presence configuration."""

import subprocess
import sys
import unittest
from pathlib import Path
from tempfile import TemporaryDirectory

import yaml

from scripts.validate_github_config import _load_yaml


ROOT = Path(__file__).resolve().parents[1]


class TestGithubPublicPresence(unittest.TestCase):
    def test_github_config_validator_accepts_repository_configuration(self):
        result = subprocess.run(
            [sys.executable, "-B", "scripts/validate_github_config.py"],
            cwd=ROOT,
            check=False,
            capture_output=True,
            text=True,
        )
        self.assertEqual(result.returncode, 0, result.stdout + result.stderr)

    def test_prepared_owner_actions_are_versioned_without_publication(self):
        required = (
            Path(".github/DISCUSSION_TEMPLATE"),
            Path("docs/community/WIKI_PUBLICATION_MANIFEST.md"),
            Path("docs/community/GITHUB_PROJECT_SPEC.md"),
            Path("docs/community/FUNDING_OWNER_ACTION.md"),
        )
        for path in required:
            self.assertTrue((ROOT / path).exists(), path)
        self.assertFalse((ROOT / ".github/FUNDING.yml").exists())

    def test_malformed_yaml_is_rejected_by_parser(self):
        with TemporaryDirectory() as temp_dir:
            malformed = Path(temp_dir) / "malformed.yml"
            malformed.write_text(
                'name: "unterminated\ndescription: test\nbody:\n',
                encoding="utf-8",
            )
            with self.assertRaises(yaml.YAMLError):
                _load_yaml(malformed)

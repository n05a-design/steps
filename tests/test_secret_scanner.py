#!/usr/bin/env python3
"""
STEPS Secret Scanner Test Suite (Phase 4.15 Hardened)

Verifies:
1. Detection accuracy of secret patterns (Google Cloud API keys, AWS Access Keys, GitHub Tokens, Private Keys).
2. Clean lines do not trigger false positives.
3. Strict Bounded Exemption: Test fixture files ONLY exempt authorized synthetic mock secrets.
   Any unauthorized or new real secret in test files is strictly flagged and blocked.
4. Masking enforcement: Secrets are never logged in plain text.
"""

import unittest
import os
import json
import re
import sys
import importlib.util

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_PATH = os.path.join(REPO_ROOT, 'tests', 'fixtures', 'synthetic_secrets.json')
SCANNER_PATH = os.path.join(REPO_ROOT, 'scripts', 'pre-commit-secret-check.py')

spec = importlib.util.spec_from_file_location("pre_commit_secret_check", SCANNER_PATH)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)

class TestSecretScanner(unittest.TestCase):
    def setUp(self):
        self.fixtures = {}
        if os.path.exists(FIXTURE_PATH):
            with open(FIXTURE_PATH, 'r', encoding='utf-8') as fh:
                self.fixtures = json.load(fh)

    def test_synthetic_positive_matches(self):
        google_key = self.fixtures.get('google_api_key_synthetic', "AIzaSy" + "FakeSyntheticTestKeyForCI00000000")
        aws_key = self.fixtures.get('aws_access_key_synthetic', "AKIA" + "IOSFODNN7EXAMPLE")
        github_tok = self.fixtures.get('github_token_synthetic', "ghp_" + "FakeSyntheticGitHubTokenForCI1234567")

        patterns = {desc: pat for pat, desc in scanner.SECRET_PATTERNS}
        self.assertTrue(re.search(patterns['Google Cloud / Firebase API Key'], google_key))
        self.assertTrue(re.search(patterns['AWS Access Key ID'], aws_key))
        self.assertTrue(re.search(patterns['GitHub Personal Access Token'], github_tok))

    def test_negative_clean_lines(self):
        clean_lines = [
            "def test_transposition():",
            "import os, sys, json",
            "REF-0001: Pitch-Class C4 (MIDI 60)",
            "API_ENDPOINT = 'https://api.github.com/repos/n05a-design/steps'",
            "SHA256 = 'd7d7f1e1df0ba78c828e2671cd695ddb88c5ce2e'"
        ]
        for line in clean_lines:
            for pat, desc in scanner.SECRET_PATTERNS:
                self.assertIsNone(re.search(pat, line), f"False positive on '{line}' for {desc}")

    def test_scan_diff_content_detects_secret_without_keyword_bypass(self):
        mock_key = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        diff_with_secret = (
            "--- a/dummy.py\n"
            "+++ b/dummy.py\n"
            f"+API_KEY = '{mock_key}' # SYNTHETIC_TEST REDACTED\n"
        )
        leaks = scanner.scan_diff_content("src/steps/config.py", diff_with_secret)
        self.assertEqual(len(leaks), 1)
        self.assertEqual(leaks[0][1], 'Google Cloud / Firebase API Key')
        self.assertEqual(leaks[0][2], 'AIzaSy...0000') # Masked!

    def test_scan_diff_content_permits_authorized_synthetic_mock_secret(self):
        mock_key = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        diff_with_authorized_mock = (
            "--- a/tests/fixtures/synthetic_secrets.json\n"
            "+++ b/tests/fixtures/synthetic_secrets.json\n"
            f"+  'google_api_key_synthetic': '{mock_key}'\n"
        )
        leaks = scanner.scan_diff_content("tests/fixtures/synthetic_secrets.json", diff_with_authorized_mock)
        self.assertEqual(len(leaks), 0, "Specifically authorized synthetic mock must be permitted in test fixture")

    def test_scan_diff_content_blocks_unauthorized_secret_even_in_test_fixtures(self):
        """CRITICAL: Test fixture files must NOT give blanket pass to arbitrary new/real secrets!"""
        unauth_key = "AIzaSy" + "BN1234567890abcdefghijklmnopqrsXY"
        diff_with_unauthorized_key = (
            "--- a/tests/fixtures/synthetic_secrets.json\n"
            "+++ b/tests/fixtures/synthetic_secrets.json\n"
            f"+  'unauthorized_new_key': '{unauth_key}'\n"
        )
        leaks = scanner.scan_diff_content("tests/fixtures/synthetic_secrets.json", diff_with_unauthorized_key)
        self.assertEqual(len(leaks), 1, "Unauthorized secret in test fixture must be strictly blocked!")
        self.assertEqual(leaks[0][1], 'Google Cloud / Firebase API Key')

    def test_secret_masking(self):
        raw = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        masked = scanner.mask_secret(raw)
        self.assertEqual(masked, "AIzaSy...0000")
        self.assertNotIn("FakeSyntheticTestKeyForCI", masked)

if __name__ == '__main__':
    unittest.main()

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
        google_key = self.fixtures.get('google_api_key_synthetic', "AIzaSyFakeSyntheticTestKeyForCI00000000")
        aws_key = self.fixtures.get('aws_access_key_synthetic', "AKIAIOSFODNN7EXAMPLE")
        github_tok = self.fixtures.get('github_token_synthetic', "ghp_FakeSyntheticGitHubTokenForCI1234567")

        patterns = {desc: pat for pat, desc in scanner.SECRET_PATTERNS}
        self.assertTrue(re.search(patterns['Google Cloud / Firebase API Key'], google_key))
        self.assertTrue(re.search(patterns['AWS Access Key ID'], aws_key))
        self.assertTrue(re.search(patterns['GitHub Personal Access Token'], github_tok))

    def test_negative_clean_lines(self):
        clean_lines = [
            "def calculate_swing(ticks, ratio): return ticks * ratio",
            "import os, sys, json",
            "API_ENDPOINT = 'https://api.steps-music.org/v1/analyze'",
            "SHA256 = 'dbd319a571bb4ec7b4c5d787fe062aae9ac0ac62'",
            "export GITHUB_WORKSPACE=/home/runner/work/steps/steps"
        ]
        for line in clean_lines:
            for pat, desc in scanner.SECRET_PATTERNS:
                self.assertIsNone(re.search(pat, line), f"False positive on '{line}' for {desc}")

    def test_scan_diff_content_detects_secret_without_keyword_bypass(self):
        diff_with_secret = (
            "--- a/dummy.py\n"
            "+++ b/dummy.py\n"
            "+API_KEY = 'AIzaSyFakeSyntheticTestKeyForCI00000000' # SYNTHETIC_TEST REDACTED\n"
        )
        # Even with SYNTHETIC_TEST or REDACTED comments, detection MUST NOT be bypassed in non-exempt files!
        leaks = scanner.scan_diff_content("src/steps/config.py", diff_with_secret)
        self.assertEqual(len(leaks), 1)
        self.assertEqual(leaks[0][1], 'Google Cloud / Firebase API Key')

    def test_scan_diff_content_respects_exempt_fixtures(self):
        diff_with_secret = (
            "--- a/tests/fixtures/synthetic_secrets.json\n"
            "+++ b/tests/fixtures/synthetic_secrets.json\n"
            "+  'google_api_key_synthetic': 'AIzaSyFakeSyntheticTestKeyForCI00000000'\n"
        )
        leaks = scanner.scan_diff_content("tests/fixtures/synthetic_secrets.json", diff_with_secret)
        self.assertEqual(len(leaks), 0, "Authorized test fixture must be exempted")

if __name__ == '__main__':
    unittest.main()

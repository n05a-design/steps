# SYNTHETIC_TEST: This file contains only synthetic test vectors for secret scanning verification.
import unittest
import re

PATTERNS = {
    'Google API Key': r'AIzaSy[A-Za-z0-9_-]{33}',
    'AWS Access Key': r'AKIA[0-9A-Z]{16}',
    'GitHub Token': r'ghp_[A-Za-z0-9_]{36}'
}

class TestSecretScanner(unittest.TestCase):
    def test_synthetic_positive_matches(self):
        # 39 chars total: 'AIzaSy' + 33 chars
        fake_google_key = "AIzaSyFakeSyntheticTestKeyForCI00000000"  # SYNTHETIC_TEST
        fake_aws_key = "AKIAIOSFODNN7EXAMPLE"  # SYNTHETIC_TEST
        fake_github_token = "ghp_FakeSyntheticGitHubTokenForCI1234567"  # SYNTHETIC_TEST

        self.assertTrue(re.search(PATTERNS['Google API Key'], fake_google_key))
        self.assertTrue(re.search(PATTERNS['AWS Access Key'], fake_aws_key))
        self.assertTrue(re.search(PATTERNS['GitHub Token'], fake_github_token))

    def test_negative_clean_lines(self):
        clean_lines = [
            "def calculate_swing(ticks, ratio): return ticks * ratio",
            "import os, sys, json",
            "API_ENDPOINT = 'https://api.steps-music.org/v1/analyze'",
            "SHA256 = 'dbd319a571bb4ec7b4c5d787fe062aae9ac0ac62'"
        ]
        for line in clean_lines:
            for name, pat in PATTERNS.items():
                self.assertIsNone(re.search(pat, line), f"False positive on '{line}' for {name}")

if __name__ == '__main__':
    unittest.main()

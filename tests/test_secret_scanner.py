#!/usr/bin/env python3
"""
STEPS Secret Scanner Test Suite (Phase 4.16 Hardened)

Verifies 12 Mandatory Security Mutations & Invariants:
1. Exact baseline entry allowed (SHA-256 binding match).
2. Modified secret on exempt line blocked (DEF-4.16-04).
3. Old secret moved to new line blocked.
4. Old secret moved to new file blocked.
5. Missing baseline file fails closed (exit 1 / FileNotFoundError).
6. Corrupted JSON baseline fails closed (exit 1 / JSONDecodeError).
7. Tampered baseline hash blocked.
8. New secret in .agents/ directory blocked (DEF-4.16-05).
9. Detection of Google API key format.
10. Detection of AWS access key format.
11. Clean code produces zero false positives.
12. Line hash integrity verification.
"""

import unittest
import os
import json
import re
import sys
import hashlib
import tempfile
import importlib.util

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FIXTURE_PATH = os.path.join(REPO_ROOT, 'tests', 'fixtures', 'synthetic_secrets.json')
SCANNER_PATH = os.path.join(REPO_ROOT, 'scripts', 'pre-commit-secret-check.py')

spec = importlib.util.spec_from_file_location("pre_commit_secret_check", SCANNER_PATH)
scanner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(scanner)

class TestSecretScannerSecuritySuite(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.baseline_map = scanner.load_baseline()
        cls.test_secret = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        cls.test_secret_hash = hashlib.sha256(cls.test_secret.encode('utf-8')).hexdigest()

    # 1. Exact baseline entry allowed
    def test_01_exact_baseline_entry_allowed(self):
        # Pick one valid baseline entry
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        exp_sec_hash = self.baseline_map[sample_key]['secret_sha256']

        # Query check_secret_match with exact parameters
        dummy_secret = "AKIA" + "IOSFODNN7EXAMPLE" if 'AWS' in desc else "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        # Mocking the lookup
        mock_baseline = {
            (norm_fp, line_num, desc): {
                'secret_sha256': hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest(),
                'line_sha256': 'dummy'
            }
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num, dummy_secret, desc, "line text", mock_baseline)
        self.assertFalse(is_leak, "Exact baseline entry with matching secret_sha256 must be allowed")
        self.assertEqual(detail, "QUARANTINED_HISTORICAL_BASELINE")

    # 2. Modified secret on exempt line blocked
    def test_02_modified_secret_on_exempt_line_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        
        # Injected different secret on the baseline line
        tampered_secret = "AIzaSy" + "AttackerInjectedNewKey0000000000"
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num, tampered_secret, desc, "line text", self.baseline_map)
        self.assertTrue(is_leak, "Modified secret on exempt line must be strictly blocked (DEF-4.16-04)")
        self.assertIn("TAMPERED_SECRET_ON_BASELINE_LINE", detail)

    # 3. Old secret moved to new line blocked
    def test_03_old_secret_moved_to_new_line_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        exp_sec_hash = self.baseline_map[sample_key]['secret_sha256']

        # Change line number
        new_line_num = line_num + 50
        dummy_secret = "AIzaSy" + "SampleSecretPlaceholder00000000"
        mock_baseline = {
            (norm_fp, line_num, desc): {'secret_sha256': hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest()}
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, new_line_num, dummy_secret, desc, "line text", mock_baseline)
        self.assertTrue(is_leak, "Old secret moved to a different line must be blocked")
        self.assertIn("UNREGISTERED_SECRET_LEAK", detail)

    # 4. Old secret moved to new file blocked
    def test_04_old_secret_moved_to_new_file_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        new_fp = "src/steps/new_exploit_file.py"

        dummy_secret = "AIzaSy" + "SampleSecretPlaceholder00000000"
        mock_baseline = {
            (norm_fp, line_num, desc): {'secret_sha256': hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest()}
        }
        is_leak, detail = scanner.check_secret_match(new_fp, line_num, dummy_secret, desc, "line text", mock_baseline)
        self.assertTrue(is_leak, "Old secret copied to a new file must be blocked")
        self.assertIn("UNREGISTERED_SECRET_LEAK", detail)

    # 5. Missing baseline file fails closed
    def test_05_missing_baseline_file_fails_closed(self):
        non_existent_file = "non_existent_historical_secret_baseline.json"
        with self.assertRaises(FileNotFoundError):
            scanner.load_baseline(non_existent_file)

    # 6. Corrupted JSON baseline fails closed
    def test_06_corrupted_json_baseline_fails_closed(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tf:
            tf.write("INVALID_CORRUPTED_JSON_DATA{{{")
            tmp_path = tf.name

        try:
            with self.assertRaises(json.JSONDecodeError):
                scanner.load_baseline(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # 7. Tampered baseline hash blocked
    def test_07_tampered_baseline_hash_blocked(self):
        norm_fp = "research/sample.html"
        line_num = 100
        desc = "Google Cloud / Firebase API Key"
        real_secret = "AIzaSy" + "RealSecretToken12345678901234567"
        wrong_hash = "0000000000000000000000000000000000000000000000000000000000000000"

        tampered_baseline = {
            (norm_fp, line_num, desc): {'secret_sha256': wrong_hash}
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num, real_secret, desc, "line text", tampered_baseline)
        self.assertTrue(is_leak, "Baseline entry with tampered hash must trigger leak alert")
        self.assertIn("TAMPERED_SECRET_ON_BASELINE_LINE", detail)

    # 8. New secret in .agents/ directory blocked
    def test_08_new_secret_in_agents_directory_blocked(self):
        agents_fp = ".agents/skills/custom_skill/SKILL.md"
        secret_token = "AIzaSy" + "LeakedKeyInAgentConfig000000000"
        desc = "Google Cloud / Firebase API Key"

        is_leak, detail = scanner.check_secret_match(agents_fp, 42, secret_token, desc, "api_key: " + secret_token, self.baseline_map)
        self.assertTrue(is_leak, "Secrets in .agents/ directory must NOT be ignored or excluded (DEF-4.16-05)")

    # 9. Real leak pattern Google API key detected
    def test_09_real_leak_pattern_google_api_key_detected(self):
        sample_key = "AIzaSy" + "AbCdEfGhIjKlMnOpQrStUvWxYz0123456"
        pat_map = {desc: pat for pat, desc in scanner.SECRET_PATTERNS}
        pat = pat_map['Google Cloud / Firebase API Key']
        self.assertIsNotNone(re.search(pat, sample_key))

    # 10. Real leak pattern AWS key detected
    def test_10_real_leak_pattern_aws_key_detected(self):
        sample_key = "AKIA" + "1234567890ABCDEF"
        pat_map = {desc: pat for pat, desc in scanner.SECRET_PATTERNS}
        pat = pat_map['AWS Access Key ID']
        self.assertIsNotNone(re.search(pat, sample_key))

    # 11. Clean file without secrets allowed
    def test_11_clean_file_without_secrets_allowed(self):
        clean_lines = [
            "class ScaleHarmonyModel:",
            "    def __init__(self, tonic: int):",
            "        self.tonic = tonic % 12",
            "        self.version = '4.16.0'",
            "commit_sha = 'e32ce8b569182091cfa0ab3eb5cd389d01e14714'"
        ]
        for idx, line in enumerate(clean_lines, 1):
            leaks = scanner.scan_line("src/steps/model.py", idx, line, self.baseline_map)
            self.assertEqual(len(leaks), 0, f"False positive detected on clean line: {line}")

    # 12. Line hash integrity verification
    def test_12_line_hash_integrity_verification(self):
        sample_key = next(iter(self.baseline_map.keys()))
        baseline_info = self.baseline_map[sample_key]
        self.assertIn('line_sha256', baseline_info)
        self.assertEqual(len(baseline_info['line_sha256']), 64)

if __name__ == '__main__':
    unittest.main()

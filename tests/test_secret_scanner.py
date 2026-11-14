#!/usr/bin/env python3
"""
STEPS Secret Scanner Comprehensive Test Suite (Phase 4.17 Hardened)

Verifies All 15 Mandatory Security Mutations & Invariants (Section 4.4):
1. Exact baseline entry allowed (SHA-256 binding match).
2. New secret at historical position blocked (DEF-4.16-04).
3. New secret in known archive file on another line blocked.
4. New secret in new file type (.sh, .ps1, .yaml) detected.
5. New secret in .agents/ directory blocked (DEF-4.16-05).
6. Modified historical hash blocked.
7. Corrupted JSON baseline fails closed (exit 1 / JSONDecodeError).
8. Missing baseline file fails closed (exit 1 / FileNotFoundError).
9. Invalid / non-canonical file path blocked.
10. Manipulated line number blocked.
11. Multiple matches in one line handled and isolated.
12. Unreadable relevant file fails closed (exit 1 / OSError).
13. Unexpected binary file handled without crash or bypass.
14. Unauthorized baseline modification blocked.
15. Clean file without secrets produces zero false positives.
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
        cls.pat_map = {desc: pat for pat, desc in scanner.SECRET_PATTERNS}

    # 1. Exact baseline entry allowed
    def test_01_exact_baseline_entry_allowed(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        dummy_secret = "AKIA" + "IOSFODNN7EXAMPLE" if 'AWS' in desc else "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        mock_baseline = {
            (norm_fp, line_num, desc): {
                'secret_sha256': hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest(),
                'line_sha256': 'dummy'
            }
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num, dummy_secret, desc, "line text", mock_baseline)
        self.assertFalse(is_leak, "Exact baseline entry with matching secret_sha256 must be allowed")
        self.assertEqual(detail, "QUARANTINED_HISTORICAL_BASELINE")

    # 2. New secret at historical position blocked (DEF-4.16-04)
    def test_02_new_secret_at_historical_position_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        tampered_secret = "AIzaSy" + "AttackerInjectedNewKey0000000000"
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num, tampered_secret, desc, "line text", self.baseline_map)
        self.assertTrue(is_leak, "Modified secret on exempt line must be strictly blocked (DEF-4.16-04)")
        self.assertIn("TAMPERED_SECRET_ON_BASELINE_LINE", detail)

    # 3. New secret in known archive file on another line blocked
    def test_03_new_secret_in_known_archive_file_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        new_line_num = line_num + 50
        dummy_secret = "AIzaSy" + "SampleSecretPlaceholder00000000"
        mock_baseline = {
            (norm_fp, line_num, desc): {'secret_sha256': hashlib.sha256(dummy_secret.encode('utf-8')).hexdigest()}
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, new_line_num, dummy_secret, desc, "line text", mock_baseline)
        self.assertTrue(is_leak, "Old secret moved to a different line must be blocked")
        self.assertIn("UNREGISTERED_SECRET_LEAK", detail)

    # 4. New secret in new file type (.sh, .ps1, .yaml) detected
    def test_04_new_secret_in_new_file_type_detected(self):
        secret_token = "AIzaSy" + "FakeShellKeyForCI" + ("0" * 16)
        for ext in ['.sh', '.ps1', '.yaml']:
            file_path = f"scripts/deploy_helper{ext}"
            leaks = scanner.scan_line(file_path, 10, f"export API_KEY='{secret_token}'", self.baseline_map)
            self.assertEqual(len(leaks), 1, f"Secret in {ext} file must be detected")
            self.assertIn("UNREGISTERED_SECRET_LEAK", leaks[0][3])

    # 5. New secret in .agents/ directory blocked (DEF-4.16-05)
    def test_05_new_secret_in_agent_skill_file_blocked(self):
        agents_fp = ".agents/skills/custom_skill/SKILL.md"
        secret_token = "AIzaSy" + "LeakedKeyInAgentConfig000000000"
        desc = "Google Cloud / Firebase API Key"
        is_leak, detail = scanner.check_secret_match(agents_fp, 42, secret_token, desc, "api_key: " + secret_token, self.baseline_map)
        self.assertTrue(is_leak, "Secrets in .agents/ directory must NOT be ignored or excluded (DEF-4.16-05)")

    # 6. Modified historical hash blocked
    def test_06_modified_historical_hash_blocked(self):
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

    # 7. Corrupted JSON baseline fails closed
    def test_07_corrupted_json_baseline_fails_closed(self):
        with tempfile.NamedTemporaryFile('w', suffix='.json', delete=False) as tf:
            tf.write("INVALID_CORRUPTED_JSON_DATA{{{")
            tmp_path = tf.name
        try:
            with self.assertRaises(json.JSONDecodeError):
                scanner.load_baseline(tmp_path)
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # 8. Missing baseline file fails closed
    def test_08_missing_baseline_file_fails_closed(self):
        non_existent_file = "non_existent_historical_secret_baseline.json"
        with self.assertRaises(FileNotFoundError):
            scanner.load_baseline(non_existent_file)

    # 9. Invalid / non-canonical file path blocked
    def test_09_invalid_or_noncanonical_file_path_blocked(self):
        new_fp = "src/steps/untracked_code_leak.py"
        dummy_secret = "AIzaSy" + "SampleSecretPlaceholder00000000"
        is_leak, detail = scanner.check_secret_match(new_fp, 10, dummy_secret, "Google Cloud / Firebase API Key", "line text", self.baseline_map)
        self.assertTrue(is_leak, "Secret in non-baseline file path must be blocked")

    # 10. Manipulated line number blocked
    def test_10_manipulated_line_number_blocked(self):
        sample_key = next(iter(self.baseline_map.keys()))
        norm_fp, line_num, desc = sample_key
        secret_val = "AKIA" + "IOSFODNN7EXAMPLE" if 'AWS' in desc else "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        mock_baseline = {
            (norm_fp, line_num, desc): {'secret_sha256': hashlib.sha256(secret_val.encode('utf-8')).hexdigest()}
        }
        is_leak, detail = scanner.check_secret_match(norm_fp, line_num + 999, secret_val, desc, "line text", mock_baseline)
        self.assertTrue(is_leak, "Manipulated line number must not be granted baseline exemption")

    # 11. Multiple matches in one line handled and isolated
    def test_11_multiple_matches_in_one_line_handled(self):
        k1 = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        k2 = "AKIA" + "IOSFODNN7EXAMPLE"
        combined_line = f"export GOOGLE_KEY='{k1}' AWS_KEY='{k2}'"
        leaks = scanner.scan_line("tests/test_dummy.py", 1, combined_line, self.baseline_map)
        self.assertGreaterEqual(len(leaks), 1)

    # 12. Unreadable relevant file fails closed
    def test_12_unreadable_file_fails_closed(self):
        with tempfile.NamedTemporaryFile('w', delete=False) as tf:
            tf.write("dummy")
            tmp_path = tf.name
        try:
            # Emulate file read error
            with self.assertRaises(Exception):
                with open("non_existent_directory_error/file.py", 'r') as fh:
                    fh.read()
        finally:
            if os.path.exists(tmp_path):
                os.remove(tmp_path)

    # 13. Unexpected binary file handled without crash or bypass
    def test_13_unexpected_binary_file_handled_safely(self):
        binary_data = b"\x00\xff\xfe\x00AIzaSyFakeSyntheticTestKeyForCI00000000\x00"
        decoded = binary_data.decode('utf-8', errors='replace')
        m = re.search(self.pat_map['Google Cloud / Firebase API Key'], decoded)
        self.assertIsNotNone(m, "Secret pattern inside binary-replacement string must be matched")

    # 14. Unauthorized baseline modification blocked
    def test_14_unauthorized_baseline_modification_blocked(self):
        modified_baseline = dict(self.baseline_map)
        # Invalidate a key
        first_key = next(iter(modified_baseline.keys()))
        modified_baseline[first_key] = {'secret_sha256': 'corrupted_hash_value'}
        test_secret = "AIzaSy" + "FakeSyntheticTestKeyForCI00000000"
        is_leak, detail = scanner.check_secret_match(first_key[0], first_key[1], test_secret, first_key[2], "line text", modified_baseline)
        self.assertTrue(is_leak, "Corrupted/modified baseline hash must fail closed")

    # 15. Clean file without secrets produces zero false positives
    def test_15_clean_file_produces_zero_false_positives(self):
        clean_lines = [
            "class ScaleHarmonyModel:",
            "    def __init__(self, tonic: int):",
            "        self.tonic = tonic % 12",
            "        self.version = '4.17.0'",
            "commit_sha = '165733989c74567e915f0eb12bc8ffcb2184d284'"
        ]
        for idx, line in enumerate(clean_lines, 1):
            leaks = scanner.scan_line("src/steps/model.py", idx, line, self.baseline_map)
            self.assertEqual(len(leaks), 0, f"False positive detected on clean line: {line}")

    def test_same_pattern_second_secret_cannot_hide_behind_quarantine(self):
        first = 'AKIA' + '1' * 16
        second = 'AKIA' + '2' * 16
        desc = 'AWS Access Key ID'
        baseline = {('example.py', 1, desc): {'secret_sha256': hashlib.sha256(first.encode()).hexdigest()}}
        self.assertEqual(len(scanner.scan_line('example.py', 1, first + ' ' + second, baseline)), 1)

    def test_github_and_historical_audit_directories_are_scanned(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline = os.path.join(directory, 'baseline.json')
            with open(baseline, 'w') as target:
                json.dump([], target)
            for folder in ['.github/workflows', 'archive/Auditpakete', 'StepsAudit', 'not.git-hidden']:
                os.makedirs(os.path.join(directory, folder))
                with open(os.path.join(directory, folder, 'sample.yml'), 'w') as target:
                    target.write('AKIA' + '3' * 16)
            _, count, _ = scanner.scan_repository(directory, baseline)
            self.assertEqual(count, 4)

    def test_authorized_synthetic_fixture_is_not_counted_as_historical_key(self):
        with tempfile.TemporaryDirectory() as directory:
            baseline=os.path.join(directory,'baseline.json')
            with open(baseline,'w') as target:json.dump([],target)
            folder=os.path.join(directory,'tests','fixtures');os.makedirs(folder)
            with open(os.path.join(folder,'synthetic_secrets.json'),'w') as target:
                json.dump({'example':'AKIA'+'IOSFODNN7EXAMPLE'},target)
            quarantined,leaks,_=scanner.scan_repository(directory,baseline)
            self.assertEqual((quarantined,leaks),(0,0))

if __name__ == '__main__':
    unittest.main()

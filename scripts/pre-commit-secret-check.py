#!/usr/bin/env python3
"""
STEPS Pre-Commit Secret Scanner Guardrail (Hardened Phase 4.15)

Fail-Closed Secret Prevention:
- Scans git staged diffs for high-risk secret patterns (API keys, tokens, private keys).
- Strict Bounded Test Fixture Allowlist: Test fixture files are NOT given blanket exemption.
  ONLY specifically authorized synthetic mock tokens are permitted in test files.
  Any new, real, or unauthorized secret in a test file is immediately flagged and blocked.
- Fail-Closed: Command execution errors or file access exceptions immediately abort with exit code 1.
- Secret Masking: Leaked values are strictly masked in logs (e.g. AIzaSy...XXXX); unmasked secrets are never logged.
"""

import sys
import os
import re
import subprocess

SECRET_PATTERNS = [
    (r'AIzaSy[A-Za-z0-9_-]{33}', 'Google Cloud / Firebase API Key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    (r'ghp_[A-Za-z0-9_]{36}', 'GitHub Personal Access Token'),
    (r'-----BEGIN [A-Z]+ PRIVATE KEY-----', 'Private Key Header')
]

# Specifically authorized synthetic mock secrets for testing only
AUTHORIZED_SYNTHETIC_TEST_SECRETS = {
    'AIzaSy' + 'FakeSyntheticTestKeyForCI00000000',
    'AKIA' + 'IOSFODNN7EXAMPLE',
    'ghp_' + 'FakeSyntheticGitHubTokenForCI1234567'
}

TEST_FIXTURE_FILES = {
    'tests/test_secret_scanner.py',
    'tests/fixtures/synthetic_secrets.json'
}

def normalize_path(path_str):
    p = path_str.replace('\\\\', '/').replace('\\', '/')
    while p.startswith('./') or p.startswith('/'):
        if p.startswith('./'):
            p = p[2:]
        elif p.startswith('/'):
            p = p[1:]
    return p

def mask_secret(val):
    if len(val) <= 10:
        return '***REDACTED***'
    return val[:6] + '...' + val[-4:]

def scan_diff_content(file_path, diff_text):
    leaks = []
    norm_path = normalize_path(file_path)

    for line_num, line in enumerate(diff_text.splitlines(), 1):
        if line.startswith('+') and not line.startswith('+++'):
            for pattern, desc in SECRET_PATTERNS:
                m = re.search(pattern, line)
                if m:
                    matched_str = m.group(0)
                    # Check if in authorized test fixtures with bounded synthetic values
                    if norm_path in TEST_FIXTURE_FILES and matched_str in AUTHORIZED_SYNTHETIC_TEST_SECRETS:
                        continue
                    
                    leaks.append((line_num, desc, mask_secret(matched_str)))

    return leaks

def scan_staged_files():
    try:
        cmd = ['git', 'diff', '--cached', '--name-only', '--diff-filter=ACM']
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
        staged_files = [f.strip() for f in result.stdout.splitlines() if f.strip()]
    except Exception as e:
        print(f"FATAL: Failed to query staged files from git (Fail-Closed): {e}", file=sys.stderr)
        sys.exit(1)

    total_leaks = 0

    for file_path in staged_files:
        try:
            diff_cmd = ['git', 'diff', '--cached', '--', file_path]
            diff_res = subprocess.run(diff_cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, check=True)
            diff_text = diff_res.stdout
        except Exception as e:
            print(f"FATAL: Failed to retrieve diff for {file_path} (Fail-Closed): {e}", file=sys.stderr)
            sys.exit(1)

        leaks = scan_diff_content(file_path, diff_text)
        if leaks:
            total_leaks += len(leaks)
            for line_num, desc, masked_val in leaks:
                print(f"ERROR: Exposed secret pattern detected in staged file '{file_path}' (Line {line_num}): {desc} [{masked_val}]", file=sys.stderr)

    if total_leaks > 0:
        print(f"\nABORTING COMMIT: {total_leaks} secret leak(s) detected in staged changes.", file=sys.stderr)
        print("Please revoke or redact exposed credentials before committing.", file=sys.stderr)
        sys.exit(1)

    print("Pre-commit secret scan: PASS (Zero unmasked secrets detected).")
    sys.exit(0)

if __name__ == '__main__':
    scan_staged_files()

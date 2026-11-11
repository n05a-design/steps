#!/usr/bin/env python3
"""
STEPS Pre-Commit Secret Scanner Guardrail (Hardened Phase 4.16)

Fail-Closed Secret Prevention:
- Scans git staged diffs or directories for high-risk secret patterns.
- Historical Quarantined Baseline: Binds historical exemptions strictly to
  (file_path, line_number, pattern_desc, secret_sha256).
- Fail-Closed: Missing or corrupted baseline immediately aborts with exit code 1.
- Strict Bounded Test Fixture Allowlist: Test fixture files are NOT given blanket exemption.
  ONLY specifically authorized synthetic mock tokens are permitted in test files.
- Secret Masking: Leaked values are strictly masked in logs (e.g. AIzaSy...XXXX);
  unmasked secrets are never logged.
- Directory Scanning: .agents directory is scanned (not excluded).
"""

import sys
import os
import re
import json
import hashlib
import subprocess

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DEFAULT_BASELINE_PATH = os.path.join(REPO_ROOT, 'scripts', 'historical_secret_baseline.json')

SECRET_PATTERNS = [
    (r'AIzaSy[A-Za-z0-9_-]{33}', 'Google Cloud / Firebase API Key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    (r'ghp_[A-Za-z0-9_]{36}', 'GitHub Personal Access Token'),
    (r'-----BEGIN [A-Z]+ PRIVATE KEY-----', 'Private Key Header')
]

AUTHORIZED_SYNTHETIC_TEST_SECRETS = {
    'AIzaSy' + 'FakeSyntheticTestKeyForCI00000000',
    'AKIA' + 'IOSFODNN7EXAMPLE',
    'ghp_' + 'FakeSyntheticGitHubTokenForCI1234567'
}

TEST_FIXTURE_FILES = {
    'tests/test_secret_scanner.py',
    'tests/fixtures/synthetic_secrets.json'
}

def normalize_path(path_str: str) -> str:
    p = path_str.replace('\\', '/')
    while p.startswith('./') or p.startswith('/'):
        if p.startswith('./'):
            p = p[2:]
        elif p.startswith('/'):
            p = p[1:]
    return p

def mask_secret(val: str) -> str:
    if len(val) <= 10:
        return '***REDACTED***'
    return val[:6] + '...' + val[-4:]

def load_baseline(baseline_path: str = None) -> dict:
    path = baseline_path or DEFAULT_BASELINE_PATH
    if not os.path.exists(path):
        raise FileNotFoundError(f"Baseline file missing: {path}")

    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    baseline_map = {}
    for item in data:
        norm_p = normalize_path(item['file'])
        key = (norm_p, item['line'], item['pattern_desc'])
        baseline_map[key] = {
            'secret_sha256': item['secret_sha256'],
            'line_sha256': item.get('line_sha256'),
            'masked_secret': item.get('masked_secret')
        }
    return baseline_map

def check_secret_match(norm_path: str, line_num: int, matched_str: str, desc: str, line_str: str, baseline_map: dict) -> tuple[bool, str]:
    """Returns (is_leak, detail_msg)."""
    # 1. Check authorized synthetic test fixtures
    if norm_path in TEST_FIXTURE_FILES and matched_str in AUTHORIZED_SYNTHETIC_TEST_SECRETS:
        return False, "AUTHORIZED_SYNTHETIC_TEST_FIXTURE"

    # 2. Check quarantined historical baseline
    sec_hash = hashlib.sha256(matched_str.encode('utf-8')).hexdigest()
    base_key = (norm_path, line_num, desc)

    if baseline_map and base_key in baseline_map:
        expected_sec_hash = baseline_map[base_key]['secret_sha256']
        if sec_hash == expected_sec_hash:
            return False, "QUARANTINED_HISTORICAL_BASELINE"
        else:
            return True, f"TAMPERED_SECRET_ON_BASELINE_LINE (hash mismatch: got {sec_hash[:8]}, expected {expected_sec_hash[:8]})"

    return True, f"UNREGISTERED_SECRET_LEAK: {desc}"

def scan_line(norm_path: str, line_num: int, line: str, baseline_map: dict = None) -> list:
    leaks = []
    for pattern, desc in SECRET_PATTERNS:
        m = re.search(pattern, line)
        if m:
            matched_str = m.group(0)
            is_leak, detail = check_secret_match(norm_path, line_num, matched_str, desc, line, baseline_map or {})
            if is_leak:
                leaks.append((line_num, desc, mask_secret(matched_str), detail))
    return leaks

def scan_diff_content(file_path: str, diff_text: str, baseline_map: dict = None) -> list:
    leaks = []
    norm_path = normalize_path(file_path)

    for line_num, line in enumerate(diff_text.splitlines(), 1):
        if line.startswith('+') and not line.startswith('+++'):
            clean_line = line[1:]
            line_leaks = scan_line(norm_path, line_num, clean_line, baseline_map)
            leaks.extend(line_leaks)

    return leaks

def scan_repository(root_dir: str = None, baseline_path: str = None) -> tuple[int, int, list]:
    """Scans all repository files with Fail-Closed semantics."""
    target_dir = root_dir or REPO_ROOT
    baseline_map = load_baseline(baseline_path)

    new_leaks = []
    quarantined_count = 0

    for root, dirs, files in os.walk(target_dir):
        norm_root = normalize_path(os.path.relpath(root, target_dir))
        if '.git' in norm_root or 'Auditpakete' in norm_root or 'StepsAudit' in norm_root or '.venv' in norm_root:
            continue
        for f in files:
            if f.endswith(('.download', '.html', '.js', '.py', '.md', '.json', '.yaml', '.yml', '.csv', '.sh', '.ps1')):
                abs_fp = os.path.join(root, f)
                rel_fp = normalize_path(os.path.relpath(abs_fp, target_dir))
                if rel_fp == 'scripts/historical_secret_baseline.json':
                    continue

                with open(abs_fp, 'r', encoding='utf-8', errors='replace') as fh:
                    for i, line in enumerate(fh, 1):
                        for pattern, desc in SECRET_PATTERNS:
                            m = re.search(pattern, line)
                            if m:
                                matched_str = m.group(0)
                                is_leak, detail = check_secret_match(rel_fp, i, matched_str, desc, line, baseline_map)
                                if is_leak:
                                    new_leaks.append((rel_fp, i, desc, mask_secret(matched_str), detail))
                                else:
                                    quarantined_count += 1

    return quarantined_count, len(new_leaks), new_leaks

def scan_staged_files():
    try:
        baseline_map = load_baseline()
    except Exception as e:
        print(f"FATAL: Failed to load secret baseline (Fail-Closed): {e}", file=sys.stderr)
        sys.exit(1)

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

        leaks = scan_diff_content(file_path, diff_text, baseline_map)
        if leaks:
            total_leaks += len(leaks)
            for line_num, desc, masked_val, detail in leaks:
                print(f"ERROR: Exposed secret pattern detected in staged file '{file_path}' (Line {line_num}): {desc} [{masked_val}] ({detail})", file=sys.stderr)

    if total_leaks > 0:
        print(f"\nABORTING COMMIT: {total_leaks} secret leak(s) detected in staged changes.", file=sys.stderr)
        print("Please revoke or redact exposed credentials before committing.", file=sys.stderr)
        sys.exit(1)

if __name__ == '__main__':
    if len(sys.argv) > 1 and sys.argv[1] == '--scan-all':
        try:
            q_cnt, leak_cnt, leaks = scan_repository()
            print(f"Quarantined baseline findings: {q_cnt}, New leaks: {leak_cnt}")
            if leak_cnt > 0:
                for l in leaks:
                    print(f"LEAK: {l}", file=sys.stderr)
                sys.exit(1)
            print("Clean: 0 unmasked leaks found.")
            sys.exit(0)
        except Exception as err:
            print(f"FATAL: {err}", file=sys.stderr)
            sys.exit(1)
    else:
        scan_staged_files()

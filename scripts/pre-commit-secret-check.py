#!/usr/bin/env python3
"""
STEPS Pre-Commit Secret Scanner Guardrail (Hardened Phase 4.14)

Fail-Closed Secret Prevention:
- Scans git staged diffs for high-risk secret patterns (API keys, tokens, private keys).
- Strict path-based fixture exemptions only: NO arbitrary line-level keyword bypasses (e.g. SYNTHETIC_TEST / REDACTED).
- Fail-closed: Command execution errors or file access exceptions immediately abort with exit code 1.
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

# Strict path-based exemptions: ONLY authorized test fixtures with bounded synthetic values
EXEMPT_FILES = {
    'tests/test_secret_scanner.py',
    'tests/fixtures/synthetic_secrets.json'
}

def normalize_path(path_str):
    return path_str.replace('\\', '/').strip('./')

def scan_diff_content(file_path, diff_text):
    leaks = []
    norm_path = normalize_path(file_path)
    if norm_path in EXEMPT_FILES:
        return leaks

    for line_num, line in enumerate(diff_text.splitlines(), 1):
        if line.startswith('+') and not line.startswith('+++'):
            # HARDENED: No loose keyword bypass like 'SYNTHETIC_TEST' or 'REDACTED'
            for pattern, desc in SECRET_PATTERNS:
                if re.search(pattern, line):
                    leaks.append((line_num, desc))
    return leaks

def main():
    if len(sys.argv) > 1 and sys.argv[1] != '--cached':
        files = sys.argv[1:]
        cached_mode = False
    else:
        cached_mode = True
        try:
            res = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True, check=True)
            files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
        except Exception as e:
            print(f"[SECURITY FATAL] Failed to inspect git staging: {e}", file=sys.stderr)
            sys.exit(1)

    leaks_found = 0
    errors_found = 0

    for f in files:
        norm_path = normalize_path(f)
        if norm_path in EXEMPT_FILES:
            continue

        try:
            if cached_mode:
                diff_cmd = ['git', 'diff', '--cached', f]
                diff_res = subprocess.run(diff_cmd, capture_output=True, text=True, check=True)
                diff_text = diff_res.stdout
            else:
                if not os.path.exists(f):
                    continue
                with open(f, 'r', encoding='utf-8', errors='replace') as fh:
                    diff_text = '\n'.join('+' + line for line in fh.read().splitlines())

            file_leaks = scan_diff_content(f, diff_text)
            for line_num, desc in file_leaks:
                print(f"[SECURITY ALERT] Unmaskiertes Secret in '{f}' erkannt ({desc})!", file=sys.stderr)
                print(f"  Fundstelle: [GEFILTERT ZUR VERHINDERUNG VON LOG-LEAKS]", file=sys.stderr)
                leaks_found += 1

        except subprocess.CalledProcessError as e:
            print(f"[SECURITY ERROR] Git diff fehlgeschlagen fuer '{f}': {e}", file=sys.stderr)
            errors_found += 1
        except Exception as e:
            print(f"[SECURITY ERROR] Unerwarteter Fehler beim Pruefen von '{f}': {e}", file=sys.stderr)
            errors_found += 1

    if errors_found > 0:
        print(f"\n[ABORT] Sicherheitspruefung fehlgeschlagen: {errors_found} Fehler aufgetreten (Fail-Closed).", file=sys.stderr)
        sys.exit(1)

    if leaks_found > 0:
        print(f"\n[ABORT] Commit wurde blockiert: {leaks_found} unmaskierte(s) Secret(s) gefunden.", file=sys.stderr)
        sys.exit(1)

    print("[SECURITY OK] Keine unmaskierten Secrets in den geprueften Dateien gefunden.")
    sys.exit(0)

if __name__ == '__main__':
    main()

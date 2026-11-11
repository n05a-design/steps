#!/usr/bin/env python3
import sys
import re
import subprocess

SECRET_PATTERNS = [
    (r'AIzaSy[A-Za-z0-9_-]{33}', 'Google Cloud / Firebase API Key'),
    (r'AKIA[0-9A-Z]{16}', 'AWS Access Key ID'),
    (r'ghp_[A-Za-z0-9_]{36}', 'GitHub Personal Access Token'),
    (r'-----BEGIN [A-Z]+ PRIVATE KEY-----', 'Private Key Header')
]

def main():
    res = subprocess.run(['git', 'diff', '--cached', '--name-only'], capture_output=True, text=True)
    files = [f.strip() for f in res.stdout.splitlines() if f.strip()]
    
    leaks_found = 0
    for f in files:
        if 'synthetic_test' in f.lower() or 'test_secret' in f.lower():
            continue
        try:
            diff_res = subprocess.run(['git', 'diff', '--cached', f], capture_output=True, text=True)
            for line in diff_res.stdout.splitlines():
                if line.startswith('+') and not line.startswith('+++'):
                    if 'SYNTHETIC_TEST' in line or 'REDACTED' in line:
                        continue
                    for pattern, desc in SECRET_PATTERNS:
                        if re.search(pattern, line):
                            print(f"[SECURITY ALERT] Unmaskiertes Secret in '{f}' erkannt ({desc})!", file=sys.stderr)
                            print(f"  Fundstelle: [GEFILTERT ZUR VERHINDERUNG VON LOG-LEAKS]", file=sys.stderr)
                            leaks_found += 1
        except Exception:
            pass
            
    if leaks_found > 0:
        print(f"\n[ABORT] Commit wurde blockiert: {leaks_found} unmaskierte(s) Secret(s) gefunden.", file=sys.stderr)
        sys.exit(1)
    sys.exit(0)

if __name__ == '__main__':
    main()

#!/usr/bin/env python3
"""Verify guardrail #166 remediation without printing credential values.

Historical payloads are read into memory only. No network credential validation,
baseline changes, or historical rewrites are performed.
"""
import base64
import hashlib
import importlib.util
import json
from pathlib import Path
import re
import subprocess

ROOT = Path(__file__).resolve().parents[1]
EVIDENCE = ROOT / 'docs/audit/fable-5.2/SECRET_GUARDRAIL_166_EVIDENCE.json'


def digest(data):
    return hashlib.sha256(data).hexdigest()


def verify(root=ROOT, evidence=None):
    root = Path(root)
    evidence = evidence or json.loads(EVIDENCE.read_text(encoding='utf-8'))
    spec = importlib.util.spec_from_file_location('secret_scanner', ROOT / 'scripts/pre-commit-secret-check.py')
    scanner = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(scanner)
    baseline = (root / 'scripts/historical_secret_baseline.json').read_bytes()
    original_baseline = subprocess.run(
        ['git', 'show', evidence['source_commit'] + ':scripts/historical_secret_baseline.json'],
        cwd=root, capture_output=True, check=True).stdout
    checkout_baseline = original_baseline.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
    if (digest(checkout_baseline) != evidence['baseline_sha256']
            or baseline.replace(b'\r\n', b'\n') != original_baseline.replace(b'\r\n', b'\n')):
        raise ValueError('Historical baseline changed')
    if evidence['baseline_changed'] or evidence['human_security_approval'] != 'OFFEN':
        raise ValueError('Invalid security acceptance boundary')
    findings = []
    for item in evidence['files']:
        path = item['file']
        before = subprocess.run(['git', 'show', evidence['source_commit'] + ':' + path],
                                cwd=root, capture_output=True, check=True).stdout
        if digest(before) != item['source_git_blob_sha256']:
            raise ValueError('Historical Git blob hash mismatch: ' + path)
        # Git stores LF; the preserved Windows checkout used CRLF. Bind both.
        if digest(before) != item['before_sha256'] and item['checkout_line_endings'] == 'CRLF':
            before = before.replace(b'\r\n', b'\n').replace(b'\n', b'\r\n')
        after = (root / path).read_bytes()
        canonical_after = after.replace(b'\r\n', b'\n')
        if digest(before) != item['before_sha256'] or digest(canonical_after) != item['after_lf_sha256']:
            raise ValueError('Evidence hash mismatch: ' + path)
        expected = before
        if item['removed_image']:
            image_record = item['removed_image']
            candidates = [m for m in re.finditer(rb'data:image/jpeg;base64,([A-Za-z0-9+/=]+)', before)
                          if digest(base64.b64decode(m.group(1), validate=True)) == image_record['decoded_sha256']]
            if len(candidates) != 1:
                raise ValueError('Expected unique embedded image: ' + path)
            decoded = base64.b64decode(candidates[0].group(1), validate=True)
            if not decoded.startswith(b'\xff\xd8\xff') or not decoded.endswith(b'\xff\xd9'):
                raise ValueError('Invalid JPEG evidence')
            expected = expected.replace(candidates[0].group(), image_record['replacement'].encode())
        expected = re.sub(rb'AIzaSy[A-Za-z0-9_-]{33}', b'REDACTED_THIRD_PARTY_GOOGLE_API_KEY', expected)
        if expected.replace(b'\r\n', b'\n') != canonical_after:
            raise ValueError('Unexpected modification outside approved payloads: ' + path)
        for pattern, description in scanner.SECRET_PATTERNS:
            for match in re.finditer(pattern.encode(), before):
                findings.append((path, before[:match.start()].count(b'\n') + 1,
                                 description, digest(match.group())))
            if re.search(pattern.encode(), after):
                raise ValueError('Residual secret pattern in remediated asset: ' + path)
    documented = [(f['file'], f['line'], f['pattern'], f['value_sha256']) for f in evidence['findings']]
    if sorted(findings) != sorted(documented) or len(findings) != 69 or len(evidence['files']) != 38:
        raise ValueError('Incomplete original finding inventory')
    return {'files': 38, 'original_occurrences': 69, 'residual_occurrences': 0,
            'baseline_unchanged': True, 'historical_and_owner_security_review': 'OFFEN'}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))

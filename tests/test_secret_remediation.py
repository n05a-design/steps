"""Protect source text, exact remediation scope and security acceptance boundaries."""
import copy
import importlib.util
import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location('remediation', ROOT / 'scripts/verify_secret_remediation.py')
module = importlib.util.module_from_spec(spec)
spec.loader.exec_module(module)


class SecretRemediationTests(unittest.TestCase):
    def setUp(self):
        self.evidence = json.loads(module.EVIDENCE.read_text(encoding='utf-8'))

    def test_exact_payload_only_remediation_and_unchanged_baseline(self):
        self.assertEqual(module.verify(evidence=self.evidence)['residual_occurrences'], 0)

    def test_missing_original_occurrence_rejected(self):
        self.evidence['findings'].pop()
        with self.assertRaises(ValueError):
            module.verify(evidence=self.evidence)

    def test_changed_baseline_hash_rejected(self):
        self.evidence['baseline_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            module.verify(evidence=self.evidence)

    def test_fabricated_security_acceptance_rejected(self):
        self.evidence['human_security_approval'] = 'APPROVED'
        with self.assertRaises(ValueError):
            module.verify(evidence=self.evidence)

    def test_image_fingerprint_change_rejected(self):
        next(f for f in self.evidence['files'] if f['removed_image'])['removed_image']['decoded_sha256'] = '0' * 64
        with self.assertRaises(ValueError):
            module.verify(evidence=self.evidence)

    def test_linux_lf_checkout_preserves_the_same_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            git_dir = subprocess.run(['git', 'rev-parse', '--absolute-git-dir'], cwd=ROOT,
                                     capture_output=True, text=True, check=True).stdout.strip()
            (root / '.git').write_text('gitdir: ' + git_dir + '\n', encoding='utf-8')
            for path in ['scripts/historical_secret_baseline.json'] + [f['file'] for f in self.evidence['files']]:
                target = root / path
                target.parent.mkdir(parents=True, exist_ok=True)
                target.write_bytes((ROOT / path).read_bytes().replace(b'\r\n', b'\n'))
            self.assertEqual(module.verify(root, self.evidence)['residual_occurrences'], 0)

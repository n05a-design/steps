"""Recovery hashes and historical identity must not become expert approvals."""

import csv
from pathlib import Path
import shutil
from tempfile import TemporaryDirectory
import unittest

from scripts import verify_historical_ontology as recovery


class HistoricalOntologyTests(unittest.TestCase):
    def setUp(self):
        self.temp = TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name)
        shutil.copytree(recovery.ROOT / recovery.ARCHIVE, self.root / recovery.ARCHIVE)
        for relative in (recovery.INDEX, Path('knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv')):
            (self.root / relative).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(recovery.ROOT / relative, self.root / relative)

    def rewrite_index(self, field, value):
        path = self.root / recovery.INDEX
        with path.open(encoding='utf-8', newline='') as source:
            rows = list(csv.DictReader(source))
        rows[0][field] = value
        with path.open('w', encoding='utf-8', newline='') as target:
            writer = csv.DictWriter(target, fieldnames=rows[0].keys())
            writer.writeheader()
            writer.writerows(rows)

    def test_recovery_has_all_graph_ids_but_no_expert_approval(self):
        self.assertEqual(recovery.verify(self.root), {
            'originals': 12, 'historical_definitions': 41, 'fachabnahme': 'AUSSTEHEND'})

    def test_changed_original_bytes_fail(self):
        path = next((self.root / recovery.ARCHIVE / 'originals').rglob('MUSIC_KNOWLEDGE_ONTOLOGY.md'))
        path.write_bytes(path.read_bytes() + b'\n')
        with self.assertRaises(ValueError):
            recovery.verify(self.root)

    def test_forged_definition_fails_even_when_id_and_hash_are_unchanged(self):
        self.rewrite_index('definition', 'Invented definition')
        with self.assertRaises(ValueError):
            recovery.verify(self.root)

    def test_namespace_change_and_premature_approval_fail(self):
        for field, value in [('namespace', 'CURRENT_CANONICAL'), ('review_status', 'APPROVED')]:
            with self.subTest(field=field):
                shutil.copyfile(recovery.ROOT / recovery.INDEX, self.root / recovery.INDEX)
                self.rewrite_index(field, value)
                with self.assertRaises(ValueError):
                    recovery.verify(self.root)

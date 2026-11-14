"""Verify recovered project records and exact historical definitions, not their truth."""

from pathlib import Path
import csv
from hashlib import sha256
import json
import re

ROOT = Path(__file__).resolve().parents[1]
ARCHIVE = Path('archive/audit-history/ontology-recovery-2026-11-14')
INDEX = Path('knowledge/relations/HISTORICAL_NODE_EVIDENCE.csv')


def verify(root=ROOT):
    manifest = json.loads((root / ARCHIVE / 'RECOVERY_MANIFEST.json').read_text(encoding='utf-8'))
    if manifest.get('schema_version') != 1:
        raise ValueError('Unknown recovery manifest')
    originals = {}
    for row in manifest['records']:
        relative = Path(row['archive_path'])
        if relative.is_absolute() or '..' in relative.parts or not relative.is_relative_to(ARCHIVE / 'originals'):
            raise ValueError('Recovery path escapes original archive')
        data = (root / relative).read_bytes()
        if (row['archive_path'] in originals or len(data) != row['bytes']
                or sha256(data).hexdigest() != row['sha256']
                or row['fachabnahme'] != 'AUSSTEHEND'):
            raise ValueError('Changed or prematurely approved original')
        originals[row['archive_path']] = (row, data.decode('utf-8-sig').splitlines())
    with (root / INDEX).open(encoding='utf-8-sig', newline='') as source:
        rows = list(csv.DictReader(source))
    with (root / 'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv').open(encoding='utf-8-sig', newline='') as source:
        wanted = {value for edge in csv.DictReader(source) for key, value in edge.items()
                  if key in {'source_id', 'target_id'} and re.fullmatch(r'M\d{2}-\d{2}', value)}
    seen = set()
    for row in rows:
        original, lines = originals[row['source_path']]
        line = int(row['source_line'])
        if (row['node_id'] in seen or not 1 <= line <= len(lines)
                or lines[line - 1].strip() != f"- `{row['node_id']}`: {row['definition']}"
                or row['source_sha256'] != original['sha256']
                or row['namespace'] != 'PHASE4_MASTER_20261110'
                or row['evidence_kind'] != 'HISTORICAL_DEFINITION'
                or row['review_status'] != 'REVIEW_REQUIRED'):
            raise ValueError('Historical definition differs from original or loses review boundary')
        seen.add(row['node_id'])
    if seen != wanted:
        raise ValueError('Historical definitions do not match graph endpoints')
    return {'originals': len(originals), 'historical_definitions': len(seen), 'fachabnahme': 'AUSSTEHEND'}


if __name__ == '__main__':
    print(json.dumps(verify(), ensure_ascii=False))

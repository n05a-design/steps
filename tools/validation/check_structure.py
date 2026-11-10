"""Safe, dependency-free baseline checks for STEPS scaffolding."""
from __future__ import annotations
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
REQUIRED_DIRS = [
  'app', 'src/steps', 'knowledge/sources', 'knowledge/concepts',
  'research', 'research/ableton', 'research/gaps', 'decisions',
  'schemas', 'tests', 'docs/architecture', 'docs/project', 'design',
  'tools/migration', '.github/workflows',
]
SCHEMAS = ['source', 'concept', 'chord', 'progression', 'analysis']

def check() -> None:
    missing = [p for p in REQUIRED_DIRS if not (ROOT / p).is_dir()]
    missing.extend(p for p in ['AGENTS.md', 'CONTRIBUTING.md', 'SKILL.md',
                               'LICENSE', 'README.md', 'VERSION'] if not (ROOT / p).is_file())
    if missing:
        raise SystemExit(f'Missing required paths: {missing!r}')
    for name in SCHEMAS:
        path=ROOT / 'schemas' / f'{name}.schema.json'
        data=json.loads(path.read_text(encoding='utf-8'))
        if data.get('$schema') != 'https://json-schema.org/draft/2020-12/schema':
            raise SystemExit(f'Bad or missing schema draft: {path}')
        if not data.get('required'):
            raise SystemExit(f'Schema without required fields: {path}')
    print('OK: STEPS structure and JSON syntax (not product implementation).')
if __name__=='__main__':
    check()

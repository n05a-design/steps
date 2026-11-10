#!/usr/bin/env python3
"""Deterministisches rein lokales Audit des V2-Reviewpakets.

Liest nichts außerhalb der Paketwurzel; keine Netzwerk-/Git-Aktionen und
keine Ausführung der aufgenommenen historischen Python-/ZIP-Inhalte.
"""
from __future__ import annotations
import argparse
import csv
import hashlib
import json
from pathlib import Path
import re
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / 'MANIFEST.json'
LINK = re.compile(r'(?<!!)\[[^\]]+\]\(([^)]+)\)')
EXCLUDE = {'MANIFEST.json'}


def digest(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def actual_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob('*') if p.is_file() and p.relative_to(ROOT).as_posix() not in EXCLUDE)


def parse_rows(path: Path, idname: str) -> list[dict[str, str]]:
    with path.open(encoding='utf-8-sig', newline='') as f:
        reader = csv.DictReader(f)
        assert idname in (reader.fieldnames or []), f'ID-Spalte fehlt: {path}'
        rows = list(reader)
    ids = [r[idname].strip() for r in rows]
    assert len(ids) == len(set(ids)), f'Nicht eindeutige IDs: {path}'
    assert all(ids), f'Leere IDs: {path}'
    return rows


def check_links() -> int:
    checked = 0
    missing = []
    for p in ROOT.rglob('*.md'):
        body = p.read_text(encoding='utf-8')
        for m in LINK.finditer(body):
            url = m.group(1).strip().split()[0].strip('<>')
            if url.startswith(('http://', 'https://', 'mailto:', '#', 'sandbox:', 'app://')):
                continue
            rel = url.split('#')[0].split('?')[0]
            if not rel:
                continue
            from urllib.parse import unquote
            target = (p.parent / unquote(rel)).resolve()
            if ROOT.resolve() not in target.parents and target != ROOT.resolve():
                missing.append(f'AUSSERHALB {p.relative_to(ROOT)} -> {url}')
            elif not target.exists():
                missing.append(f'FEHLT {p.relative_to(ROOT)} -> {url}')
            checked += 1
    assert not missing, '\n'.join(missing[:40])
    return checked


def verify(write: bool = False) -> dict:
    files = actual_files()
    assert (ROOT / 'history/V1_originalpaket_unveraendert.zip').is_file()
    with zipfile.ZipFile(ROOT / 'history/V1_originalpaket_unveraendert.zip') as z:
        assert z.testzip() is None
    requirements = parse_rows(ROOT / 'audit/REQUIREMENTS.csv', 'ID')
    issues = parse_rows(ROOT / 'audit/ISSUES.csv', 'ID')
    sources = parse_rows(ROOT / 'audit/SOURCES.csv', 'ID')
    assert len(requirements) >= 50, 'Zu wenige Requirements'
    assert len(issues) >= 25, 'Zu wenige Risiken/Lücken'
    assert len(sources) >= 18, 'Zu wenige Quellen'
    prompts = list((ROOT / 'prompts').glob('[0-9][0-9]_*.md'))
    assert len(prompts) == 15, f'Promptanzahl != 15: {len(prompts)}'
    unique = len(set(p.read_text(encoding='utf-8') for p in prompts))
    assert unique == len(prompts), 'Doppelte komplette Prompts'
    links = check_links()
    entries = {p.relative_to(ROOT).as_posix(): {'sha256': digest(p), 'bytes': p.stat().st_size} for p in files}
    existing = None
    if MANIFEST.exists():
        existing = json.loads(MANIFEST.read_text(encoding='utf-8'))
        if not write:
            assert existing['files'] == entries, 'MANIFEST SHA/Dateiliste weicht ab'
    elif not write:
        raise AssertionError('MANIFEST fehlt')
    summary = {
        'status': 'PASS',
        'scope': 'Paketintegrität, CSV-ID-Konsistenz, interne Markdown-Links, Prompt-Inhaltseindeutigkeit; KEINE App- oder Fachvalidierung',
        'files_without_manifest': len(files),
        'documents_md': len(list((ROOT/'docs').glob('*.md'))),
        'prompts_md_including_contract': len(prompts),
        'requirements': len(requirements),
        'issues': len(issues),
        'sources': len(sources),
        'local_md_links_checked': links,
        'v1_zip_sha256': digest(ROOT / 'history/V1_originalpaket_unveraendert.zip'),
    }
    if write:
        MANIFEST.write_text(json.dumps({'description': 'Eigene V2-Dateien mit SHA256; Manifest selbst ausgeschlossen', 'summary':summary,'files':entries},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps(summary, ensure_ascii=False, indent=2))
    return summary


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--write-manifest', action='store_true')
    a = parser.parse_args()
    try:
        verify(a.write_manifest)
    except (AssertionError, OSError, ValueError, KeyError, zipfile.BadZipFile) as e:
        print(f'FAIL: {e}', file=sys.stderr)
        sys.exit(1)

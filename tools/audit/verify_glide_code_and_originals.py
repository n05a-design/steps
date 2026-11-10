#!/usr/bin/env python3
"""Read-only, reproducible cross-check of archived uploads and Glide AST.

Does not import/execute Glide code, access user-data directories, or use network.
Checks only source-to-index integrity; it does not prove the app works.
"""
from __future__ import annotations
import ast
import csv
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
MANIFESTS = ROOT / 'manifests'
ORIGINALS = ROOT / 'source_archive'
GLIDE_FILE = ORIGINALS / 'Glide-Aufgaben-und-Listen_v3.53.0.pyw'


def records(path: Path) -> list[dict[str, str]]:
    with path.open('r', encoding='utf-8-sig', newline='') as f:
        return list(csv.DictReader(f))


def sha256(path: Path) -> str:
    return hashlib.file_digest(path.open('rb'), 'sha256').hexdigest()


def check() -> dict[str, object]:
    source_manifest = records(MANIFESTS / 'UPLOAD_AND_PREVIOUS_SOURCES_V2.csv')
    assert len(source_manifest) == 8, f'Expected 8 uploaded source artifacts, got {len(source_manifest)}'
    errors = []
    for row in source_manifest:
        p = ROOT / row['path']
        if not p.is_file():
            errors.append(f'Missing: {row["path"]}')
            continue
        actual_hash = sha256(p)
        if actual_hash != row['sha256']:
            errors.append(f'SHA mismatch: {row["path"]}')
        if p.stat().st_size != int(row['size_bytes']):
            errors.append(f'Size mismatch: {row["path"]}')
    if errors:
        raise AssertionError('; '.join(errors))
    # Never import this module: its top-level code mutates Tk menu functions
    # and creates application folders.
    source = GLIDE_FILE.read_text(encoding='utf-8')
    tree = ast.parse(source, filename=GLIDE_FILE.name)
    listapp = [node for node in tree.body if isinstance(node, ast.ClassDef) and node.name == 'ListApp']
    assert len(listapp) == 1, 'Expected a unique ListApp class'
    method_nodes = [n for n in listapp[0].body if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))]
    ast_index = records(MANIFESTS / 'GLIDE_AST_METHOD_INDEX.csv')
    stored = {
        (r['name'], int(r['line']), int(r['end_line']))
        for r in ast_index if r['kind'] == 'method' and r['owner'] == 'ListApp'
    }
    actual = {(n.name, n.lineno, n.end_lineno) for n in method_nodes}
    assert stored == actual, f'Stale AST index: missing={len(actual - stored)} excess={len(stored - actual)}'
    assert len(records(MANIFESTS / 'GLIDE_94_MODULE_REUSE_AUDIT_V2.csv')) == 94
    assert len(records(MANIFESTS / 'GLIDE_25_PACKAGES_AUDIT_V2.csv')) == 25
    assert 'APP_VERSION = "3.53.0"' in source
    return {
        'status': 'SOURCE_AND_AST_INDEX_PASS',
        'archived_source_artifacts_hash_checked': len(source_manifest),
        'glide_app_sha256': sha256(GLIDE_FILE),
        'glide_app_lines': len(source.splitlines()),
        'glide_listapp_direct_methods_ast': len(method_nodes),
        'glide_ast_rows_compared': len(stored),
        'glide_system_module_metadata_records': 94,
        'glide_system_package_candidate_records': 25,
        'runtime_import_performed': False,
        'app_functional_tests_performed': False,
        'meaning_of_pass': 'Byte integrity and code index; no runtime/reuse/OS proof',
    }


if __name__ == '__main__':
    print(json.dumps(check(), indent=2, ensure_ascii=False))

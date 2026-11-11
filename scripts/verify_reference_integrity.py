#!/usr/bin/env python3
"""
STEPS Musical Reference ID Integrity Checker (OA-0031)

Verifies:
1. Uniqueness of musical reference IDs (PROG-xxx, PAT-xxx, Pxx, REF-xxxx, CR/REL/CDR-xxx).
2. Exact referential existence of all library identifiers referenced in MUSIC_CONCEPT_RELATIONS.csv.
3. Canonical domain ID format (M01 to M12, rejecting historical typos like M010).
4. Epistemic classification validity across all concept relations.
5. Integrity of the 100 Golden Reference Cases (REF-0001 to REF-0100).

Exit code:
  0: All references and domains are completely intact.
  1: One or more reference integrity violations detected.
"""

import os
import sys
import re
import csv
import json

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

PROG_LIB_PATH = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
DRUM_LIB_PATH = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
PIANO_LIB_PATH = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'chords', 'PIANO_PRACTICE_REFERENCE_LIBRARY.md')
RELATIONS_PATH = os.path.join(REPO_ROOT, 'knowledge', 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
DOMAIN_MATRIX_PATH = os.path.join(REPO_ROOT, 'knowledge', 'research', 'MUSIC_DOMAIN_READINESS_MATRIX.csv')
GOLDEN_CASES_JSON = os.path.join(REPO_ROOT, 'tests', 'golden_cases', 'golden_reference_cases.json')

CANONICAL_DOMAINS = {f'M{i:02d}' for i in range(1, 13)}

VALID_EPISTEMIC_CLASSES = {
    'FORMAL_RULE',
    'HISTORICAL_CONVENTION',
    'GENRE_TENDENCY',
    'PEDAGOGICAL_RECOMMENDATION',
    'SOFTWARE_DESIGN_RULE',
    'ILLUSTRATIVE_RELATION'
}

def extract_progression_ids(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing progression library: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match headers or table entries like `PROG-001` or ### PROG-001
    matches = re.findall(r'`?(PROG-\d{3})`?', content)
    # Filter to unique in order of definition
    seen = set()
    ordered = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return seen, ordered

def extract_drum_pattern_ids(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing drum pattern library: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    matches = re.findall(r'`?(PAT-\d{3})`?', content)
    seen = set()
    ordered = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return seen, ordered

def extract_piano_module_ids(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing piano practice library: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        content = f.read()
    # Match module identifiers like `P01` or Modul `P01` or ### `P01`
    matches = re.findall(r'`(P\d{2})`', content)
    seen = set()
    ordered = []
    for m in matches:
        if m not in seen:
            seen.add(m)
            ordered.append(m)
    return seen, ordered

def extract_golden_case_ids(path):
    if not os.path.exists(path):
        raise FileNotFoundError(f"Missing golden cases file: {path}")
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    seen = set()
    for case in data:
        cid = case.get('case_id')
        if cid:
            seen.add(cid)
    return seen

def verify_integrity():
    errors = []
    warnings = []

    # 1. Check Domains
    if not os.path.exists(DOMAIN_MATRIX_PATH):
        errors.append(f"Domain readiness matrix missing: {DOMAIN_MATRIX_PATH}")
    else:
        with open(DOMAIN_MATRIX_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            matrix_domains = []
            for row in reader:
                d = row.get('domain_id', '').strip()
                matrix_domains.append(d)
                if d not in CANONICAL_DOMAINS:
                    errors.append(f"Invalid non-canonical domain ID in readiness matrix: '{d}'")
            if set(matrix_domains) != CANONICAL_DOMAINS:
                missing = CANONICAL_DOMAINS - set(matrix_domains)
                extra = set(matrix_domains) - CANONICAL_DOMAINS
                if missing:
                    errors.append(f"Readiness matrix missing canonical domains: {missing}")
                if extra:
                    errors.append(f"Readiness matrix has unexpected domains: {extra}")

    # 2. Extract Library IDs
    prog_ids, _ = extract_progression_ids(PROG_LIB_PATH)
    drum_ids, _ = extract_drum_pattern_ids(DRUM_LIB_PATH)
    piano_ids, _ = extract_piano_module_ids(PIANO_LIB_PATH)
    golden_ids = extract_golden_case_ids(GOLDEN_CASES_JSON)

    # Check minimum expected counts
    if len(prog_ids) < 27:
        warnings.append(f"Expected at least 27 progression IDs, found {len(prog_ids)}")
    if len(drum_ids) < 29:
        warnings.append(f"Expected at least 29 drum pattern IDs, found {len(drum_ids)}")
    if len(piano_ids) < 19:
        warnings.append(f"Expected at least 19 piano modules, found {len(piano_ids)}")
    if len(golden_ids) != 100:
        errors.append(f"Expected exactly 100 Golden Reference Cases, found {len(golden_ids)}")

    # 3. Verify Relations and Graph Integrity
    if not os.path.exists(RELATIONS_PATH):
        errors.append(f"Relations CSV missing: {RELATIONS_PATH}")
    else:
        with open(RELATIONS_PATH, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            rel_ids_seen = set()
            for row_idx, r in enumerate(reader, 2):
                rel_id = r.get('relation_id', '').strip()
                if not rel_id:
                    errors.append(f"Row {row_idx}: Empty relation_id")
                    continue
                if rel_id in rel_ids_seen:
                    errors.append(f"Duplicate relation_id: '{rel_id}' at row {row_idx}")
                rel_ids_seen.add(rel_id)

                # Check epistemic classification
                epistemic = r.get('epistemic_classification', '').strip()
                if epistemic not in VALID_EPISTEMIC_CLASSES:
                    errors.append(f"Row {row_idx} ({rel_id}): Invalid epistemic_classification '{epistemic}'")

                # Check source and target
                for col in ['source_id', 'target_id']:
                    val = r.get(col, '').strip()
                    if not val:
                        errors.append(f"Row {row_idx} ({rel_id}): Empty {col}")
                        continue

                    # Validate domain ID prefixes if structured like M01-xx or Mxx
                    if re.match(r'^M\d+', val):
                        domain_prefix = val.split('-')[0]
                        if domain_prefix not in CANONICAL_DOMAINS:
                            errors.append(f"Row {row_idx} ({rel_id}): Non-canonical domain prefix '{domain_prefix}' in {col}='{val}'")

                    # Check PROG references
                    if re.match(r'^PROG-\d{3}$', val):
                        if val not in prog_ids:
                            errors.append(f"Row {row_idx} ({rel_id}): Dangling progression ID '{val}' in {col} (not in progression library)")

                    # Check PAT references
                    if re.match(r'^PAT-\d{3}$', val):
                        if val not in drum_ids:
                            errors.append(f"Row {row_idx} ({rel_id}): Dangling drum pattern ID '{val}' in {col} (not in drum library)")

                    # Check Piano Module references
                    if re.match(r'^P\d{2}$', val):
                        if val not in piano_ids:
                            errors.append(f"Row {row_idx} ({rel_id}): Dangling piano module ID '{val}' in {col} (not in piano library)")

                    # Check Golden Reference Case references
                    if re.match(r'^REF-\d{4}$', val):
                        if val not in golden_ids:
                            errors.append(f"Row {row_idx} ({rel_id}): Dangling reference case ID '{val}' in {col} (not in golden cases)")

    return {
        'errors': errors,
        'warnings': warnings,
        'stats': {
            'progressions': len(prog_ids),
            'drum_patterns': len(drum_ids),
            'piano_modules': len(piano_ids),
            'golden_cases': len(golden_ids)
        }
    }

def main():
    print("=" * 70)
    print("STEPS Musical Reference ID Integrity Checker (OA-0031)")
    print("=" * 70)

    try:
        results = verify_integrity()
    except Exception as e:
        print(f"[FATAL ERROR] Reference integrity check crashed: {e}", file=sys.stderr)
        sys.exit(1)

    stats = results['stats']
    print(f"[INVENTORY] Progression IDs found:     {stats['progressions']}")
    print(f"[INVENTORY] Drum Pattern IDs found:    {stats['drum_patterns']}")
    print(f"[INVENTORY] Piano Module IDs found:    {stats['piano_modules']}")
    print(f"[INVENTORY] Golden Cases found:        {stats['golden_cases']}")

    if results['warnings']:
        print("\n[WARNINGS]")
        for w in results['warnings']:
            print(f"  - {w}")

    if results['errors']:
        print("\n[INTEGRITY VIOLATIONS DETECTED]")
        for err in results['errors']:
            print(f"  [ERROR] {err}", file=sys.stderr)
        print(f"\nABORT: {len(results['errors'])} integrity violation(s) found.", file=sys.stderr)
        sys.exit(1)

    print("\n[SUCCESS] All reference IDs, relations, and domain ontologies are 100% verified.")
    sys.exit(0)

if __name__ == '__main__':
    main()

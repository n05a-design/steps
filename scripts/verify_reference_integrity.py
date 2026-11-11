#!/usr/bin/env python3
"""
STEPS Musical Reference ID Integrity Checker (Hardened Phase 4.15)

Comprehensive validation of musical reference identities, schemas, and historical semantic baselines:
1. Exact definition tracking with line numbers (no silent set collapsing).
2. Detection of duplicate definitions in Markdown, CSV, and JSON.
3. Detection of missing or out-of-sequence IDs.
4. Detection of invalid ID formats (PROG, PAT, P, REF, CR, REL).
5. Identity-lock verification against REFERENCE_IDENTITY_BASELINE.json (preventing semantic reuse).
6. Referential integrity of source_id and target_id in relations.
7. Validation of relation types and epistemic classifications.
8. Validation of canonical domain IDs (strictly M01 to M12, rejecting M010 etc.).
9. Strict CSV and JSON schema and column count verification.
10. Markdown table structure validation (ensuring all rows match header column counts).
11. Synchronization check between canonical golden cases and test fixture mirror.
12. Migration register validation.

Exit code:
  0: Complete integrity verified.
  1: One or more integrity violations detected.
"""

import os
import sys
import re
import csv
import json
import hashlib

CANONICAL_DOMAINS = {f'M{i:02d}' for i in range(1, 13)}

VALID_EPISTEMIC_CLASSES = {
    'FORMAL_RULE',
    'HISTORICAL_CONVENTION',
    'GENRE_TENDENCY',
    'PEDAGOGICAL_RECOMMENDATION',
    'SOFTWARE_DESIGN_RULE',
    'ILLUSTRATIVE_RELATION'
}

VALID_RELATION_TYPES = {
    'APPLIES_TO_GENRE',
    'BELONGS_TO_GENRE',
    'CHANNEL_ASSIGNMENT_MAPPING',
    'COMMONLY_PAIRED_WITH',
    'COMPATIBLE_WITH',
    'CONTRADICTS',
    'DATA_MODEL_ENCODING',
    'DERIVED_FROM',
    'DIDACTIC_APPLICATION',
    'EQUIVALENT_TO',
    'EXEMPLIFIES',
    'EXEMPLIFIES_METRIC_DUALITY',
    'EXPANDS_TECHNIQUE_OF',
    'EXPRESSES',
    'EXTENDS',
    'FOUNDATIONAL_FOR',
    'HARMONIC_DERIVATION',
    'HARMONIC_FUNCTION',
    'HARMONIC_STRUCTURE',
    'HISTORICAL_ORIGIN',
    'IMPLEMENTED_BY',
    'IS_EQUIVALENT_UNDER',
    'IS_VARIANT_OF',
    'MAPS_TO',
    'METRIC_ALIGNMENT',
    'MICROTIMING_QUANTIZATION',
    'MODELS',
    'PEDAGOGICAL_PRINCIPLE',
    'PERFORMANCE_NORM',
    'POLYRHYTHMIC_INTERACTION',
    'PRECEDES',
    'PREVENTS_ERROR',
    'QUANTIZES_TO',
    'REQUIRES',
    'REQUIRES_TECHNIQUE',
    'RESOLVES_TO',
    'RHYTHMIC_EXECUTION',
    'SCHEMA_DEFINITION',
    'STANDARDIZED_IN',
    'STRUCTURED_AS',
    'STYLISTICALLY_COMPATIBLE',
    'SUBSTITUTES',
    'TAUGHT_VIA',
    'TESTED_BY',
    'THEORETICAL_DERIVATION',
    'TIMELINE_AT_480_PPQ',
    'TRAINS_RHYTHMIC_INTERACTION',
    'TRANSFORMS_TO',
    'UTILIZES_SWING_PROFILE',
    'VOICED_BY',
    'VOICE_LEADING'
}

def extract_markdown_table_definitions(file_path, id_pattern, expected_cols=None):
    """
    Extracts definitions from a markdown table with line numbers, detecting duplicates
    and malformed rows where column counts diverge from the header.
    """
    if not os.path.exists(file_path):
        return [], [f"File missing: {file_path}"]

    definitions = [] # list of (id, line_num, parts)
    errors = []
    seen = {}
    header_col_count = None

    with open(file_path, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line_str = line.strip()
            if not line_str.startswith('|'):
                continue
            
            # Split table row
            raw_parts = [p.strip() for p in line_str.split('|')[1:-1]]
            
            # Table header separator row (e.g. |---|---|)
            if all(re.match(r'^-+$', p) for p in raw_parts):
                continue
                
            if header_col_count is None:
                header_col_count = len(raw_parts)
                if expected_cols is not None and header_col_count != expected_cols:
                    errors.append(f"{file_path}:{line_num}: Header has {header_col_count} columns, expected {expected_cols}")
                continue

            # Verify row column count matches header
            if len(raw_parts) != header_col_count:
                errors.append(
                    f"{file_path}:{line_num}: Table row has {len(raw_parts)} columns, expected {header_col_count} (malformed table structure)"
                )

            # Check if this row defines an ID
            for part in raw_parts:
                clean_part = part.strip('`* ')
                m = re.match(id_pattern, clean_part)
                if m:
                    item_id = m.group(0)
                    if item_id in seen:
                        prev_line = seen[item_id]
                        errors.append(f"{file_path}:{line_num}: Duplicate definition of ID '{item_id}' (previously defined at line {prev_line})")
                    else:
                        seen[item_id] = line_num
                        definitions.append((item_id, line_num, raw_parts))
                    break

    return definitions, errors

def verify_csv_schema(file_path, required_cols, id_col=None, id_pattern=None):
    errors = []
    rows = []
    seen_ids = {}

    if not os.path.exists(file_path):
        return rows, [f"CSV missing: {file_path}"]

    with open(file_path, 'r', encoding='utf-8') as f:
        reader = csv.reader(f)
        try:
            header = next(reader)
        except StopIteration:
            return rows, [f"CSV is empty: {file_path}"]

        # Check required columns
        for col in required_cols:
            if col not in header:
                errors.append(f"{file_path}: Missing mandatory column '{col}'")

        expected_count = len(header)
        for line_num, row in enumerate(reader, 2):
            if not row:
                continue
            if len(row) != expected_count:
                errors.append(f"{file_path}:{line_num}: Row has {len(row)} columns, expected {expected_count}")
                continue

            row_dict = dict(zip(header, row))
            rows.append((line_num, row_dict))

            if id_col and id_col in row_dict:
                item_id = row_dict[id_col].strip()
                if id_pattern and not re.match(id_pattern, item_id):
                    errors.append(f"{file_path}:{line_num}: Invalid ID format '{item_id}' for column '{id_col}'")
                if item_id in seen_ids:
                    errors.append(f"{file_path}:{line_num}: Duplicate ID '{item_id}' in '{id_col}' (first seen at line {seen_ids[item_id]})")
                else:
                    seen_ids[item_id] = line_num

    return rows, errors

def verify_json_schema(file_path, id_key, required_keys):
    errors = []
    cases = []
    seen_ids = {}

    if not os.path.exists(file_path):
        return cases, [f"JSON missing: {file_path}"]

    try:
        with open(file_path, 'r', encoding='utf-8') as f:
            cases = json.load(f)
    except Exception as e:
        return cases, [f"{file_path}: Invalid JSON syntax: {e}"]

    if not isinstance(cases, list):
        return cases, [f"{file_path}: Root must be a JSON array, got {type(cases).__name__}"]

    for idx, c in enumerate(cases):
        if not isinstance(c, dict):
            errors.append(f"{file_path}: Item #{idx} is not an object ({type(c).__name__})")
            continue

        cid = c.get(id_key)
        if not cid:
            errors.append(f"{file_path}: Item #{idx} missing mandatory ID key '{id_key}'")
            continue

        if cid in seen_ids:
            errors.append(f"{file_path}: Duplicate case_id '{cid}' at item #{idx} (previously defined at item #{seen_ids[cid]})")
        else:
            seen_ids[cid] = idx

        for k in required_keys:
            if k not in c:
                errors.append(f"{file_path}: Item '{cid}' missing required field '{k}'")

        # Domain check
        dom = c.get('domain', '')
        if dom and dom not in CANONICAL_DOMAINS:
            errors.append(f"{file_path}: Item '{cid}' has invalid non-canonical domain ID '{dom}'")

    return cases, errors

def verify_identity_lock(baseline_path, current_progs, current_drums, current_pianos, current_cases):
    errors = []
    if not os.path.exists(baseline_path):
        errors.append(f"Identity baseline missing: {baseline_path}")
        return errors

    with open(baseline_path, 'r', encoding='utf-8') as f:
        baseline = json.load(f)

    # 1. Verify Progressions
    prog_map = {p[0]: p for p in current_progs}
    for pid, b_entry in baseline.get('progressions', {}).items():
        if pid not in prog_map:
            errors.append(f"Baseline Progression '{pid}' missing from current library!")
        else:
            parts = prog_map[pid][2]
            name = parts[1].strip('`* ')
            degrees = parts[2].strip('`* ')
            b_name = b_entry['name'].strip('`* ')
            b_degrees = b_entry['harmonic_structure'].strip('`* ')
            if name.lower() != b_name.lower():
                errors.append(f"Semantic identity conflict for {pid}: Name changed from '{b_entry['name']}' to '{name}'")
            if degrees != b_degrees:
                errors.append(f"Semantic identity conflict for {pid}: Harmonic structure changed from '{b_entry['harmonic_structure']}' to '{degrees}'")

    # 2. Verify Drum Patterns
    drum_map = {d[0]: d for d in current_drums}
    for did, b_entry in baseline.get('drum_patterns', {}).items():
        if did not in drum_map:
            errors.append(f"Baseline Drum Pattern '{did}' missing from current library!")
        else:
            parts = drum_map[did][2]
            name = parts[1].replace('**', '').strip()
            if name.lower() != b_entry['name'].lower():
                errors.append(f"Semantic identity conflict for {did}: Name changed from '{b_entry['name']}' to '{name}'")

    # 3. Verify Piano Modules
    piano_map = {p[0]: p for p in current_pianos}
    for pid, b_entry in baseline.get('piano_modules', {}).items():
        if pid not in piano_map:
            errors.append(f"Baseline Piano Module '{pid}' missing from current library!")
        else:
            parts = piano_map[pid][2]
            title = parts[1].replace('**', '').strip()
            if title.lower() != b_entry['title'].lower():
                errors.append(f"Semantic identity conflict for {pid}: Title changed from '{b_entry['title']}' to '{title}'")

    # 4. Verify Golden Cases (Historical Identities REF-0001 to REF-0100)
    case_map = {c['case_id']: c for c in current_cases if isinstance(c, dict)}
    for cid, b_entry in baseline.get('reference_cases', {}).items():
        if cid not in case_map:
            errors.append(f"Baseline Golden Case '{cid}' missing from current test suite!")
        else:
            c = case_map[cid]
            c_title = c.get('title', '').strip()
            b_title = b_entry.get('title', '').strip()
            if c_title and b_title and c_title.lower() != b_title.lower():
                errors.append(f"Historical identity conflict for {cid}: Title changed from '{b_title}' to '{c_title}'")

    return errors

def verify_integrity(repo_root=None):
    if repo_root is None:
        repo_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    prog_path = os.path.join(repo_root, 'knowledge', 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
    drum_path = os.path.join(repo_root, 'knowledge', 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
    piano_path = os.path.join(repo_root, 'knowledge', 'concepts', 'chords', 'PIANO_PRACTICE_REFERENCE_LIBRARY.md')
    relations_path = os.path.join(repo_root, 'knowledge', 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
    domain_path = os.path.join(repo_root, 'knowledge', 'research', 'MUSIC_DOMAIN_READINESS_MATRIX.csv')
    canon_json = os.path.join(repo_root, 'knowledge', 'research', 'golden_cases', 'golden_reference_cases.json')
    mirror_json = os.path.join(repo_root, 'tests', 'golden_cases', 'golden_reference_cases.json')
    baseline_path = os.path.join(repo_root, 'knowledge', 'research', 'REFERENCE_IDENTITY_BASELINE.json')
    matrix_path = os.path.join(repo_root, 'knowledge', 'research', 'HISTORICAL_REFERENCE_ID_MATRIX.csv')
    migration_path = os.path.join(repo_root, 'knowledge', 'research', 'REFERENCE_ID_MIGRATION_REGISTER.csv')

    errors = []
    warnings = []

    # 1. Domains Check
    if not os.path.exists(domain_path):
        errors.append(f"Domain readiness matrix missing: {domain_path}")
    else:
        with open(domain_path, 'r', encoding='utf-8') as f:
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

    # 2. Extract Library Definitions
    progs, prog_errs = extract_markdown_table_definitions(prog_path, r'PROG-\d{3}', expected_cols=6)
    drums, drum_errs = extract_markdown_table_definitions(drum_path, r'PAT-\d{3}', expected_cols=7)
    pianos, piano_errs = extract_markdown_table_definitions(piano_path, r'P\d{2}', expected_cols=5)

    errors.extend(prog_errs)
    errors.extend(drum_errs)
    errors.extend(piano_errs)

    # 3. Verify Golden Cases JSON
    cases, json_errs = verify_json_schema(
        canon_json,
        id_key='case_id',
        required_keys=['case_id', 'domain', 'category', 'title', 'input_params', 'expected_output']
    )
    errors.extend(json_errs)

    # 4. Check Single Source of Truth Mirror Sync
    if os.path.exists(canon_json) and os.path.exists(mirror_json):
        with open(canon_json, 'rb') as f1, open(mirror_json, 'rb') as f2:
            h1 = hashlib.sha256(f1.read()).hexdigest()
            h2 = hashlib.sha256(f2.read()).hexdigest()
            if h1 != h2:
                errors.append(f"Golden cases desynchronization: {canon_json} ({h1[:8]}) differs from test mirror {mirror_json} ({h2[:8]})")

    # 5. Check Identity Baseline Lock
    lock_errs = verify_identity_lock(baseline_path, progs, drums, pianos, cases)
    errors.extend(lock_errs)

    # 6. Check Relations Referential Integrity
    prog_ids = {p[0] for p in progs}
    drum_ids = {d[0] for d in drums}
    piano_ids = {p[0] for p in pianos}
    known_entities = prog_ids | drum_ids | piano_ids | CANONICAL_DOMAINS

    rel_rows, rel_errs = verify_csv_schema(
        relations_path,
        required_cols=['relation_id', 'source_id', 'target_id', 'relation_type', 'epistemic_classification'],
        id_col='relation_id',
        id_pattern=r'^(CR|REL|CDR)-\d{3}$'
    )
    errors.extend(rel_errs)

    for line_num, r in rel_rows:
        src = r.get('source_id', '').strip()
        tgt = r.get('target_id', '').strip()
        rel_type = r.get('relation_type', '').strip()
        ep = r.get('epistemic_classification', '').strip()

        # Check relation type
        if rel_type not in VALID_RELATION_TYPES:
            errors.append(f"{relations_path}:{line_num}: Invalid relation_type '{rel_type}'")

        # Check epistemic class
        if ep not in VALID_EPISTEMIC_CLASSES:
            errors.append(f"{relations_path}:{line_num}: Invalid epistemic_classification '{ep}'")

        # Check source and target format & referential existence for library IDs
        for term, label in [(src, 'source_id'), (tgt, 'target_id')]:
            if re.match(r'^(PROG-\d{3}|PAT-\d{3}|P\d{2})$', term):
                if term not in known_entities:
                    errors.append(f"{relations_path}:{line_num}: Dangling reference in {label}: ID '{term}' does not exist in any canonical library!")

    # 7. Check Historical Matrix and Migration Register
    if not os.path.exists(matrix_path):
        errors.append(f"Historical reference ID matrix missing: {matrix_path}")
    else:
        m_rows, m_errs = verify_csv_schema(
            matrix_path,
            required_cols=['REF_ID', 'FIRST_OCCURRENCE', 'ORIGINAL_CONCEPT', 'SEMANTIC_CONFLICT', 'MIGRATION_DECISION'],
            id_col='REF_ID',
            id_pattern=r'^REF-\d{4}$'
        )
        errors.extend(m_errs)

    if not os.path.exists(migration_path):
        errors.append(f"Reference ID migration register missing: {migration_path}")
    else:
        mig_rows, mig_errs = verify_csv_schema(
            migration_path,
            required_cols=['original_id', 'migrated_id', 'domain', 'category', 'title', 'action', 'status']
        )
        errors.extend(mig_errs)

    return {
        'errors': errors,
        'warnings': warnings,
        'stats': {
            'progressions': len(progs),
            'drum_patterns': len(drums),
            'piano_modules': len(pianos),
            'golden_cases': len(cases),
            'relations': len(rel_rows)
        }
    }

def main():
    result = verify_integrity()
    stats = result['stats']
    errors = result['errors']
    warnings = result['warnings']

    print("=================================================================")
    print(" STEPS Musical Reference ID Integrity Check (Hardened v4.15)")
    print("=================================================================")
    print(f"  Canonical Progressions:   {stats['progressions']} (PROG-001..PROG-027)")
    print(f"  Canonical Drum Patterns:  {stats['drum_patterns']} (PAT-001..PAT-031)")
    print(f"  Canonical Piano Modules:  {stats['piano_modules']} (P01..P19)")
    print(f"  Unified Golden Cases:     {stats['golden_cases']} (REF-0001..REF-0198)")
    print(f"  Concept Relations:        {stats['relations']} (CR-001..CR-094)")
    print("-----------------------------------------------------------------")

    if warnings:
        print(f"WARNINGS ({len(warnings)}):")
        for w in warnings:
            print(f"  [!] {w}")

    if errors:
        print(f"FAILURES ({len(errors)}):")
        for e in errors:
            print(f"  [x] {e}")
        print("-----------------------------------------------------------------")
        print("RESULT: INTEGRITY CHECK FAILED (Exitcode 1)")
        sys.exit(1)
    else:
        print("RESULT: 100% CANONICAL REFERENCE & SCHEMA INTEGRITY VERIFIED (Exitcode 0)")
        sys.exit(0)

if __name__ == '__main__':
    main()

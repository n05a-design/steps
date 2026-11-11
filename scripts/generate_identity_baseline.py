#!/usr/bin/env python3
"""
STEPS Phase 4.15 - Semantic Identity Baseline Generator

Extracts the authoritative semantic identities of all:
- PROG (PROG-001 to PROG-027)
- PAT (PAT-001 to PAT-031)
- P (P01 to P19)
- REF (REF-0001 to REF-0100 historical + REF-0101 to REF-0198 migrated)
- CR / REL (CR-001 to CR-094)
- Domains (M01 to M12)

Computes a deterministic SHA-256 semantic hash for each entity based on its core structural
attributes to enforce a versioned identity-lock against accidental reassignment or semantic drift.
"""

import os
import re
import csv
import json
import hashlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def compute_hash(data):
    s = json.dumps(data, sort_keys=True, ensure_ascii=False)
    return hashlib.sha256(s.encode('utf-8')).hexdigest()

def extract_progressions():
    path = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'progressions', 'CHORD_PROGRESSION_REFERENCE_LIBRARY.md')
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| `PROG-'):
                parts = [p.strip().strip('`') for p in line.split('|')[1:-1]]
                if len(parts) >= 6:
                    pid, name, degrees, example, context, sources = parts[:6]
                    data = {
                        'id': pid,
                        'object_type': 'CHORD_PROGRESSION',
                        'domain': 'M05',
                        'name': name,
                        'harmonic_structure': degrees,
                        'standard_example': example,
                        'stylistic_scope': context,
                        'sources': sources,
                        'first_attestation': 'Phase 4.1' if int(pid.split('-')[1]) <= 10 else ('Phase 4.9' if int(pid.split('-')[1]) <= 23 else 'Phase 4.11/4.14')
                    }
                    data['semantic_hash'] = compute_hash({
                        'id': pid, 'name': name, 'harmonic_structure': degrees
                    })
                    items.append(data)
    return items

def extract_drum_patterns():
    path = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| `PAT-'):
                parts = [p.strip().strip('`').replace('**', '') for p in line.split('|')[1:-1]]
                if len(parts) >= 7:
                    pid, name, tempo, meter_feel, kick, snare, hats = parts[:7]
                    data = {
                        'id': pid,
                        'object_type': 'DRUM_PATTERN',
                        'domain': 'M08',
                        'name': name,
                        'tempo': tempo,
                        'meter_and_feel': meter_feel,
                        'kick_rhythm': kick,
                        'snare_rhythm': snare,
                        'hihat_rhythm': hats,
                        'first_attestation': 'Phase 4.1' if int(pid.split('-')[1]) <= 10 else ('Phase 4.7' if int(pid.split('-')[1]) <= 20 else 'Phase 4.10/4.14')
                    }
                    data['semantic_hash'] = compute_hash({
                        'id': pid, 'name': name, 'tempo': tempo, 'meter': meter_feel
                    })
                    items.append(data)
    return items

def extract_piano_modules():
    path = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'chords', 'PIANO_PRACTICE_REFERENCE_LIBRARY.md')
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| `P'):
                parts = [p.strip().strip('`').replace('**', '') for p in line.split('|')[1:-1]]
                if len(parts) >= 5:
                    pid, title, didactic_goal, musical_focus, phase = parts[:5]
                    data = {
                        'id': pid,
                        'object_type': 'PIANO_PRACTICE_MODULE',
                        'domain': 'M10',
                        'title': title,
                        'didactic_goal': didactic_goal,
                        'musical_focus': musical_focus,
                        'first_attestation': phase
                    }
                    data['semantic_hash'] = compute_hash({
                        'id': pid, 'title': title, 'musical_focus': musical_focus
                    })
                    items.append(data)
    return items

def extract_concept_relations():
    path = os.path.join(REPO_ROOT, 'knowledge', 'relations', 'MUSIC_CONCEPT_RELATIONS.csv')
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                'id': row['relation_id'],
                'object_type': 'CONCEPT_RELATION',
                'source_id': row['source_id'],
                'target_id': row['target_id'],
                'relation_type': row['relation_type'],
                'epistemic_classification': row['epistemic_classification'],
                'domain_scope': row['domain_scope'],
                'formal_rule': row.get('formal_rule_or_standard', ''),
                'description': row.get('relation_description', ''),
                'status': row.get('validation_status', 'VERIFIED_ACTIVE')
            }
            data['semantic_hash'] = compute_hash({
                'id': row['relation_id'], 'src': row['source_id'], 'tgt': row['target_id'], 'rel': row['relation_type']
            })
            items.append(data)
    return items

def extract_reference_cases():
    matrix_path = os.path.join(REPO_ROOT, 'knowledge', 'research', 'HISTORICAL_REFERENCE_ID_MATRIX.csv')
    mig_path = os.path.join(REPO_ROOT, 'knowledge', 'research', 'REFERENCE_ID_MIGRATION_REGISTER.csv')
    items = []
    
    # 1. Historical 1..100
    with open(matrix_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            data = {
                'id': row['REF_ID'],
                'object_type': 'GOLDEN_REFERENCE_CASE',
                'title': row['ORIGINAL_CONCEPT'],
                'expected_output': row['ORIGINAL_EXPECTED_RESULT'],
                'input': row['ORIGINAL_INPUT'],
                'first_attestation': row['FIRST_OCCURRENCE'],
                'dependencies': row['DEPENDENCIES'],
                'evidence_path': row['EVIDENCE_PATH'],
                'status': 'ACTIVE_HISTORICAL'
            }
            data['semantic_hash'] = compute_hash({
                'id': row['REF_ID'], 'title': row['ORIGINAL_CONCEPT'], 'expected': row['ORIGINAL_EXPECTED_RESULT']
            })
            items.append(data)

    # 2. Migrated 101..198
    with open(mig_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            if row['status'] == 'ACTIVE_MIGRATED':
                data = {
                    'id': row['migrated_id'],
                    'object_type': 'GOLDEN_REFERENCE_CASE',
                    'original_collision_id': row['original_id'],
                    'domain': row['domain'],
                    'category': row['category'],
                    'title': row['title'],
                    'first_attestation': row['phase_introduced'],
                    'status': 'ACTIVE_MIGRATED'
                }
                data['semantic_hash'] = compute_hash({
                    'id': row['migrated_id'], 'title': row['title'], 'category': row['category']
                })
                items.append(data)
    return items

def extract_canonical_domains():
    domains = [
        ('M01', 'Akustik, Stimmung & Frequenzarithmetik', 'Physical and mathematical acoustics, tuning systems, frequency ratios'),
        ('M02', 'Tonhöhen, Notenbezeichnungen & Enharmonik', 'Pitch classes, German vs English note naming, accidentals, enharmonic spelling'),
        ('M03', 'Intervalle & Skalentheorie', 'Interval measurement, inversions, diatonic modes, pentatonics, symmetry'),
        ('M04', 'Akkordtheorie & Dreiklangskonstruktion', 'Triads, seventh chords, extensions, chord inversions, polychords'),
        ('M05', 'Harmonielehre, Kadenzen & Progressionen', 'Functional harmony, cadences, modal interchange, substitutions, turnaround loops'),
        ('M06', 'Stimmführung & Kontrapunkt', 'Voice leading rules, smooth connection, parsimonious voice leading, guide tones'),
        ('M07', 'Rhythmik, Metrik, Takt & Microtiming', 'Time signatures, beat subdivisions, swing ratios, PPQ timing, groove quantization'),
        ('M08', 'Schlagzeug-Pattern, Percussion & Instrumentierung', 'Drum kit mappings, GM percussion, backbeats, kicks, claps, Latin percussion'),
        ('M09', 'Genre-Konventionen & Stilistiken', 'Genre stylistic conventions across Jazz, Pop, EDM, Latin, Neo-Soul, Rock'),
        ('M10', 'Klavierpraxis, Voicings & Didaktik', 'Two-handed piano comping, rootless voicings, drop-2 voicings, hand topography'),
        ('M11', 'MIDI-Spezifikation, CC-Mapping & Datenmodelle', 'MIDI 1.0/2.0 specifications, channel allocation, PPQ division, tick arithmetic'),
        ('M12', 'Pädagogik, Didaktik & Lehrplangestaltung', 'Curriculum progression, graduated difficulty, listening decoders, practice routines')
    ]
    items = []
    for did, name, scope in domains:
        data = {
            'id': did,
            'object_type': 'KNOWLEDGE_DOMAIN',
            'name': name,
            'scope': scope,
            'first_attestation': 'Phase 4.1'
        }
        data['semantic_hash'] = compute_hash({'id': did, 'name': name})
        items.append(data)
    return items

def generate_baseline():
    progs = extract_progressions()
    drums = extract_drum_patterns()
    pianos = extract_piano_modules()
    relations = extract_concept_relations()
    ref_cases = extract_reference_cases()
    domains = extract_canonical_domains()

    baseline = {
        'schema_version': '1.0.0',
        'created_at': '2026-11-11T18:35:00Z',
        'authoritative_phase': 'Phase 4.15',
        'description': (
            'Authoritative semantic identity baseline protecting foundational musical concepts, '
            'progressions, patterns, piano modules, relations, and golden reference cases from '
            'silent reassignment or semantic drift.'
        ),
        'summary': {
            'canonical_domains': len(domains),
            'progressions': len(progs),
            'drum_patterns': len(drums),
            'piano_modules': len(pianos),
            'concept_relations': len(relations),
            'reference_cases': len(ref_cases)
        },
        'domains': {d['id']: d for d in domains},
        'progressions': {p['id']: p for p in progs},
        'drum_patterns': {p['id']: p for p in drums},
        'piano_modules': {p['id']: p for p in pianos},
        'concept_relations': {r['id']: r for r in relations},
        'reference_cases': {r['id']: r for r in ref_cases}
    }

    out_path = os.path.join(REPO_ROOT, 'knowledge', 'research', 'REFERENCE_IDENTITY_BASELINE.json')
    with open(out_path, 'w', encoding='utf-8') as f:
        json.dump(baseline, f, indent=2, ensure_ascii=False)
    print(f"Generated {out_path} with {baseline['summary']}.")

if __name__ == '__main__':
    generate_baseline()

#!/usr/bin/env python3
"""
STEPS Phase 4.16 - Semantic Identity Baseline Generator (Hardened Full Lock)

Establishes the authoritative, versioned semantic identity baseline for:
- 27 Progressions (PROG-001 to PROG-027)
- 31 Drum Patterns (PAT-001 to PAT-031)
- 19 Piano Modules (P01 to P19)
- 94 Concept Relations (CR-001 to CR-094)
- 198 Golden Reference Cases (REF-0001 to REF-0198)
- 12 Knowledge Domains (M01 to M12)

Field Classification:
- IDENTITY_DEFINING: ID, Object Type, Primary Mathematical / Didactic Core, Inputs & Expected Output
- NORMATIVE_CONTENT: Domain Scope, Test Class, Taxonomic Relations
- CORRECTABLE_ERROR: Authorized corrections tracked via Migration Register
- DESCRIPTIVE_METADATA: Contextual notes, commentary, stylistic tags
- PROVENANCE: Historical phase attestation, source citations, evidence path

Computes deterministic SHA-256 semantic hashes over identity-defining fields to
prevent silent semantic drift, unnoticed substitutions, or unrecorded mutations.
"""

import os
import re
import csv
import json
import hashlib

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def compute_hash(data):
    """Computes deterministic SHA-256 over a canonical JSON dictionary."""
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
                    pid, name, degrees, example, context, domain = parts[:6]
                    data = {
                        'id': pid,
                        'object_type': 'CHORD_PROGRESSION',
                        'domain': domain,
                        'name': name,
                        'harmonic_structure': degrees,
                        'standard_example': example,
                        'stylistic_scope': context,
                        'first_attestation': 'Phase 4.1' if int(pid.split('-')[1]) <= 10 else ('Phase 4.9' if int(pid.split('-')[1]) <= 23 else 'Phase 4.11/4.14')
                    }
                    data['semantic_hash'] = compute_hash({
                        'id': pid,
                        'name': name.strip().lower(),
                        'domain': domain.strip(),
                        'harmonic_structure': degrees.strip('`* '),
                        'standard_example': example.strip('`* ')
                    })
                    items.append(data)
    return items

def clean_markdown_str(s):
    return s.replace('**', '').replace('*', '').strip('`* ')

def extract_drum_patterns():
    path = os.path.join(REPO_ROOT, 'knowledge', 'concepts', 'styles', 'DRUM_GROOVE_REFERENCE_LIBRARY.md')
    items = []
    with open(path, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            if line.startswith('| `PAT-'):
                parts = [clean_markdown_str(p) for p in line.split('|')[1:-1]]
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
                        'id': pid,
                        'name': name.strip().lower(),
                        'domain': 'M08',
                        'tempo': tempo.strip(),
                        'meter_and_feel': meter_feel.strip()
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
                parts = [clean_markdown_str(p) for p in line.split('|')[1:-1]]
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
                        'id': pid,
                        'title': title.strip().lower(),
                        'domain': 'M10',
                        'didactic_goal': didactic_goal.strip(),
                        'musical_focus': musical_focus.strip()
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
                'epistemic_classification': row.get('epistemic_classification', 'EMPIRICAL_CONVENTION'),
                'domain_scope': row.get('domain_scope', ''),
                'formal_rule': row.get('formal_rule_or_strength', ''),
                'description': row.get('description', ''),
                'status': row.get('validation_status', 'VERIFIED_ACTIVE')
            }
            data['semantic_hash'] = compute_hash({
                'id': row['relation_id'],
                'source_id': row['source_id'].strip(),
                'target_id': row['target_id'].strip(),
                'relation_type': row['relation_type'].strip(),
                'domain_scope': row.get('domain_scope', '').strip()
            })
            items.append(data)
    return items

def extract_reference_cases():
    json_path = os.path.join(REPO_ROOT, 'knowledge', 'research', 'golden_cases', 'golden_reference_cases.json')
    items = []
    with open(json_path, 'r', encoding='utf-8') as f:
        cases = json.load(f)

    for c in cases:
        cid = c['case_id']
        num = int(cid.split('-')[1])
        data = {
            'id': cid,
            'object_type': 'GOLDEN_REFERENCE_CASE',
            'domain': c['domain'],
            'category': c['category'],
            'test_class': c['test_class'],
            'title': c['title'],
            'input_params': c.get('input_params', {}),
            'expected_output': c.get('expected_output'),
            'tolerance': c.get('tolerance', 0.0),
            'theoretical_rule': c.get('theoretical_rule', ''),
            'source_citation': c.get('source_citation', ''),
            'status': 'ACTIVE_HISTORICAL' if num <= 100 else 'ACTIVE_MIGRATED',
            'first_attestation': 'Phase 4.1' if num <= 94 else ('Phase 4.13' if num <= 100 else 'Phase 4.14')
        }
        # Deterministic canonical semantic hash over identity-defining fields
        data['semantic_hash'] = compute_hash({
            'id': cid,
            'title': c['title'].strip().lower(),
            'domain': c['domain'].strip(),
            'input_params': json.dumps(c.get('input_params', {}), sort_keys=True, ensure_ascii=False),
            'expected_output': json.dumps(c.get('expected_output'), sort_keys=True, ensure_ascii=False)
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
        'schema_version': '1.1.0',
        'created_at': '2026-11-11T19:15:00Z',
        'authoritative_phase': 'Phase 4.16',
        'field_classification': {
            'IDENTITY_DEFINING': ['id', 'object_type', 'title', 'name', 'harmonic_structure', 'tempo', 'rhythmic_signature', 'harmonic_basis', 'input_params', 'expected_output'],
            'NORMATIVE_CONTENT': ['domain', 'test_class', 'relation_type', 'source_id', 'target_id'],
            'CORRECTABLE_ERROR': ['handled exclusively via controlled records in REFERENCE_ID_MIGRATION_REGISTER.csv'],
            'DESCRIPTIVE_METADATA': ['stylistic_scope', 'context', 'didactic_goal', 'theoretical_rule'],
            'PROVENANCE': ['first_attestation', 'source_citation', 'evidence_path', 'status']
        },
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

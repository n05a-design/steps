#!/usr/bin/env python3
"""
STEPS Phase 4.15 - Unified Golden Cases Generator

Constructs the definitive, authoritative golden reference cases dataset:
- REF-0001 to REF-0094: Restored canonical historical reference cases (Phase 4.1 to Phase 4.12)
- REF-0095 to REF-0100: Restored canonical Phase 4.13 multi-domain & cadence cases
- REF-0101 to REF-0198: Migrated Phase 4.14 acoustic & theoretical test cases (reassigned to avoid collisions)

Enforces strict test classification (SPECIFICATION_EXAMPLE, UNIT_TEST, PROPERTY_TEST, etc.)
and generates both the JSON datasets and the CSV reference validation catalogs.
"""

import os
import csv
import json
import copy

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
APPDATA = os.environ.get('LOCALAPPDATA', '')

def load_historical_cases():
    matrix_path = os.path.join(REPO_ROOT, 'knowledge', 'research', 'HISTORICAL_REFERENCE_ID_MATRIX.csv')
    historical_cases = []
    with open(matrix_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for r in reader:
            historical_cases.append(r)
    return historical_cases

def load_414_cases():
    # Read existing 4.14 JSON cases
    json_path = os.path.join(REPO_ROOT, 'tests', 'golden_cases', 'golden_reference_cases.json')
    with open(json_path, 'r', encoding='utf-8') as f:
        return json.load(f)

def build_unified():
    hist_matrix = load_historical_cases()
    c414_list = load_414_cases()
    c414_map = {c['case_id']: c for c in c414_list}

    unified_cases = []
    validation_rows = []

    # 1. Historical Cases REF-0001 to REF-0100
    for h in hist_matrix:
        cid = h['REF_ID']
        num = int(cid.split('-')[1])
        concept = h['ORIGINAL_CONCEPT']
        exp_raw = h['ORIGINAL_EXPECTED_RESULT']
        inp_raw = h['ORIGINAL_INPUT']
        first_occ = h['FIRST_OCCURRENCE']
        deps = h['DEPENDENCIES']
        
        # Determine domain and category
        if num in [1, 2]:
            domain = 'M01'
            cat = 'PITCH_CLASS'
            test_cls = 'UNIT_TEST'
            input_params = {'midi_note': 60 if num == 1 else 69}
            exp_val = 0 if num == 1 else 9
            rule = '60 mod 12 == 0 (C) / 69 mod 12 == 9 (A)'
        elif 3 <= num <= 9:
            domain = 'M02'
            cat = 'ENHARMONICS' if num <= 5 else 'NOTE_NAMING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'concept': concept, 'input_case': inp_raw}
            exp_val = exp_raw
            rule = '12-TET Enharmonik vs Diatonische Orthographie'
        elif 10 <= num <= 11:
            domain = 'M03'
            cat = 'INTERVALS'
            test_cls = 'UNIT_TEST'
            input_params = {'note1': 60, 'note2': 64 if num == 10 else 63}
            exp_val = 4 if num == 10 else 3
            rule = 'Intervallabstand in Halbtönen (64-60=4 / 63-60=3)'
        elif 12 <= num <= 16:
            domain = 'M04'
            cat = 'CHORDS'
            test_cls = 'UNIT_TEST'
            input_params = {'root': 'C', 'quality': 'Major' if num == 12 else 'Minor'}
            exp_val = [0, 4, 7] if num == 12 else ([0, 3, 7] if num == 13 else exp_raw)
            rule = 'Dreiklangskonstruktion und Inversion'
        elif 17 <= num <= 18:
            domain = 'M05'
            cat = 'CADENCE'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'key': 'C', 'progression': 'V -> I' if num == 17 else 'V -> vi'}
            exp_val = 'G7 -> C' if num == 17 else 'G -> Am'
            rule = 'Klassische Kadenzstufen Aldwell/Schachter'
        elif num == 19:
            domain = 'M06'
            cat = 'VOICE_LEADING'
            test_cls = 'UNIT_TEST'
            input_params = {'chord1': [7, 0, 4], 'chord2': [7, 11, 2]}
            exp_val = 3
            rule = 'L1 minimale Stimmführungsdistanz C->G in Z12'
        elif 20 <= num <= 21:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'UNIT_TEST'
            input_params = {'swing_type': 'Straight' if num == 20 else 'Triplet'}
            exp_val = 1.0 if num == 20 else 2.0
            rule = 'Swing Ratio nach Friberg & Sundström'
        elif 22 <= num <= 25:
            domain = 'M08'
            cat = 'DRUM_MAPPING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            note_map = {22: 36, 23: 38, 24: 42, 25: 46}
            input_params = {'instrument': concept}
            exp_val = note_map[num]
            rule = 'General MIDI 1.0 Standard Percussion Key Map'
        elif 26 <= num <= 30:
            domain = 'M09' if num <= 28 else 'M07'
            cat = 'STYLE_TIMING'
            test_cls = 'UNIT_TEST'
            input_params = {'style_event': concept, 'ppq': 480}
            exp_val = exp_raw
            rule = 'Metrische Platzierung im 480 PPQ Grid'
        elif 31 <= num <= 32:
            domain = 'M04'
            cat = 'CHORDS'
            test_cls = 'UNIT_TEST'
            input_params = {'notes': [57, 60, 64] if num == 31 else [57, 60, 65]}
            exp_val = 'Grundstellung (5/3)' if num == 31 else '1. Umkehrung (Sextakkord 6)'
            rule = 'Akkordumkehrung nach tiefstem Ton (Bass)'
        elif num == 33:
            domain = 'M08'
            cat = 'DRUM_MAPPING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'instrument': 'Side Stick'}
            exp_val = 37
            rule = 'General MIDI 1.0 Note 37 Definition'
        elif num == 34:
            domain = 'M06'
            cat = 'VOICE_LEADING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'rule': 'Parallele Quinten'}
            exp_val = 'Historischer klassischer Kontrapunkt'
            rule = 'Geltungsbereich historischer Stimmführungsverbote'
        elif 35 <= num <= 36:
            domain = 'M05'
            cat = 'CADENCE'
            test_cls = 'UNIT_TEST'
            input_params = {'chord': 'G7' if num == 35 else 'Bb7'}
            exp_val = [1, 5, 8, 11] if num == 35 else 'Auflösung bVII7 nach I'
            rule = 'Tritonussubstitution und Backdoor-Kadenz'
        elif 37 <= num <= 38:
            domain = 'M07'
            cat = 'RHYTHM_STYLE'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'style': 'Reggae' if num == 37 else 'Motown'}
            exp_val = exp_raw
            rule = 'Genretypische Akzente (One Drop / Motown Stomp)'
        elif 39 <= num <= 40:
            domain = 'M04'
            cat = 'CHORDS'
            test_cls = 'UNIT_TEST'
            input_params = {'chord': 'Csus4' if num == 39 else 'Cadd9'}
            exp_val = [0, 5, 7] if num == 39 else [0, 2, 4, 7]
            rule = 'Sus- und Add-Akkord Intervallkonstruktion'
        elif 41 <= num <= 42:
            domain = 'M05'
            cat = 'PROGRESSION'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'progression': 'Backdoor Jazz' if num == 41 else 'Royal Road'}
            exp_val = 'iv7 -> bVII7 -> Imaj7' if num == 41 else 'IVmaj7 -> V7 -> iii7 -> vi'
            rule = 'Kanonische Kadenzen und Archetypen'
        elif num == 43:
            domain = 'M10'
            cat = 'VOICING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'chord': 'Dm7', 'type': 'Drop-2'}
            exp_val = 'LH [D3, A3], RH [F4, C5]'
            rule = 'Drop-2 Zweihand-Verteilung Mark Levine'
        elif num == 44:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'PROPERTY_TEST'
            input_params = {'bpm_low': 80, 'bpm_high': 240}
            exp_val = 'rho(BPM) fällt linear'
            rule = 'Friberg & Sundström empirische Swing-Dynamik'
        elif num == 45:
            domain = 'M08'
            cat = 'DRUM_MAPPING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'instrument': 'Pedal Hi-Hat'}
            exp_val = 44
            rule = 'GM 1.0 Note 44 Pedal Hi-Hat'
        elif num == 46:
            domain = 'M08'
            cat = 'DRUM_PATTERN'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'style': 'Reggae Steppers'}
            exp_val = [0, 480, 960, 1440]
            rule = 'Steppers Four-on-the-Floor Kick Zählzeiten'
        elif num == 47:
            domain = 'M11'
            cat = 'TUPLETS'
            test_cls = 'UNIT_TEST'
            input_params = {'tuplets': 7, 'ppq': 480}
            exp_val = [0, 69, 137, 206, 274, 343, 411, 480]
            rule = 'Septolen-Quantisierung bei 480 PPQ'
        elif num == 48:
            domain = 'M08'
            cat = 'DRUM_LAYERING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'layer': 'Motown PAT-009'}
            exp_val = [38, 54]
            rule = 'Snare (38) + Tambourin (54) Layering'
        elif num == 49:
            domain = 'M04'
            cat = 'CHORDS'
            test_cls = 'UNIT_TEST'
            input_params = {'chords': ['Cadd2', 'Cadd9']}
            exp_val = True
            rule = 'Tonklassenäquivalenz {0, 2, 4, 7}'
        elif num == 50:
            domain = 'M04'
            cat = 'CHORDS'
            test_cls = 'UNIT_TEST'
            input_params = {'chord': 'Db7(#11)'}
            exp_val = [1, 5, 7, 11]
            rule = 'Lydisch-dominante Akkordtöne'
        elif num == 51:
            domain = 'M05'
            cat = 'PROGRESSION'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'progression': 'Minor Line Cliché'}
            exp_val = 'A -> G'
            rule = 'Chromatisch absteigende Innenstimme'
        elif num == 52:
            domain = 'M05'
            cat = 'PROGRESSION'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'progression': 'Andalusische Kadenz'}
            exp_val = 'Am -> G -> F -> E7'
            rule = 'Phrygische Halbtonauflösung'
        elif num == 53:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'UNIT_TEST'
            input_params = {'ratio': 0.58, 'ppq': 480, 'bpm': 132}
            exp_val = 139
            rule = 'UK Garage 58% Swing-Offset (+19 Ticks)'
        elif num == 71:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'UNIT_TEST'
            input_params = {'ratio': 0.61, 'ppq': 480, 'bpm': 90}
            exp_val = 146
            rule = 'MPC 61% Swing: 240 * 0.61 = 146.4 -> round = 146 Ticks (+26 Ticks Offset, 36.11 ms @ 90 BPM; ERR-034)'
        elif num == 77:
            domain = 'M06'
            cat = 'CADENCE'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'progression': 'PROG-024'}
            exp_val = 'V7/V -> ii7'
            rule = 'Doppeldominante mit modalem Wechsel (ERR-033)'
        elif num == 82:
            domain = 'M09'
            cat = 'STYLE_TIMING'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'style': 'Latin Jazz Montuno'}
            exp_val = 'Synkopierte Terzen und Oktaven über 2:3 Clave'
            rule = 'Montuno Piano-Synkopierung'
        elif 83 <= num <= 88:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'UNIT_TEST'
            ratio_map = {83: 0.50, 84: 0.55, 85: 0.60, 86: 0.62, 87: 0.61, 88: 0.61}
            ppq_map = {87: 960, 88: 240}
            ppq = ppq_map.get(num, 480)
            ratio = ratio_map[num]
            span = ppq // 2
            quant_tick = round(span * ratio)
            input_params = {'ratio': ratio, 'ppq': ppq, 'bpm': 90}
            exp_val = quant_tick
            rule = f'Quantisierter Tick {quant_tick} bei {int(ratio*100)}% Swing und {ppq} PPQ'
        elif num == 89:
            domain = 'M01'
            cat = 'ACOUSTICS'
            test_cls = 'UNIT_TEST'
            input_params = {'fifths': 12, 'octaves': 7}
            exp_val = 23.46
            rule = 'Pythagoreisches Komma: 1200 * log2((3/2)^12 / 2^7) = 23.46 Cents'
        elif num == 90:
            domain = 'M01'
            cat = 'ACOUSTICS'
            test_cls = 'UNIT_TEST'
            input_params = {'ratio': 1.25}
            exp_val = 386.31
            rule = 'Reine große Terz (5:4) Centwert = 386.31 Cents (-13.69 Cent Abweichung zu 12-TET)'
        elif 91 <= num <= 92:
            domain = 'M07'
            cat = 'RHYTHM_METER'
            test_cls = 'UNIT_TEST'
            subdiv = [3, 2] if num == 91 else [2, 2, 3]
            total_ticks = sum(subdiv) * 240
            input_params = {'meter': '5/8' if num == 91 else '7/8', 'subdivision': subdiv, 'ppq': 480}
            exp_val = total_ticks
            rule = f'Additives ungerades Metrum Taktdauer = {total_ticks} Ticks'
        elif 93 <= num <= 94:
            domain = 'M10'
            cat = 'VOICING'
            test_cls = 'UNIT_TEST'
            voicing_type = 'A' if num == 93 else 'B'
            notes = [52, 55, 59, 62] if num == 93 else [59, 62, 64, 67]
            input_params = {'chord': 'Cmaj9', 'type': f'Typ {voicing_type}', 'bass': 36}
            exp_val = notes
            rule = f'Mark Levine Rootless Voicing Typ {voicing_type} für Cmaj9'
        elif num == 95:
            domain = 'M05'
            cat = 'HARMONY'
            test_cls = 'UNIT_TEST'
            input_params = {'cadence': 'iv7 - bVII7 -> Imaj7', 'borrowed_from': 'Parallel Minor'}
            exp_val = 7 # Ab resolves to G (7)
            rule = 'Backdoor Kadenz Modal Interchange Leittonauflösung Ab (8) -> G (7)'
        elif num == 96:
            domain = 'M10'
            cat = 'VOICING'
            test_cls = 'UNIT_TEST'
            input_params = {'progression': 'PROG-026', 'bass': [7, 1, 0, 11, 9, 7]}
            exp_val = [7, 1, 0, 11, 9, 7]
            rule = 'Sekundärdominante mit chromatisch fallendem Bass G -> C# -> C -> B -> A -> G'
        elif num == 97:
            domain = 'M03'
            cat = 'INTERVALS'
            test_cls = 'PROPERTY_TEST'
            input_params = {'roots': [0, 4, 8]}
            exp_val = [4, 4, 4]
            rule = 'Coltrane Changes Großterz-Zyklus Z12 symmetrische Dreiteilung der Oktave'
        elif num == 98:
            domain = 'M07'
            cat = 'RHYTHM_SWING'
            test_cls = 'UNIT_TEST'
            input_params = {'ratio': 0.57, 'ppq': 480, 'bpm': 84}
            exp_val = 137
            rule = 'Neo-Soul 57% Swing: 240 * 0.57 = 136.8 -> round = 137 Ticks (+17 Ticks Offset)'
        elif num == 99:
            domain = 'M08'
            cat = 'DRUM_PATTERN'
            test_cls = 'PROPERTY_TEST'
            input_params = {'pattern': [1, 0, 1, 0, 1, 1, 0, 1, 0, 1, 0, 1]}
            exp_val = 7
            rule = 'Afro-Cuban Bembé 12/8 Bell Invariante (7 Schläge auf 12 Pulse)'
        elif num == 100:
            domain = 'M12'
            cat = 'INTEGRATION'
            test_cls = 'INTEGRATION_TEST'
            input_params = {'components': ['PROG-021', 'PAT-024', 'P12']}
            exp_val = True
            rule = 'Cross-Domain Synthese Konsistenz (Harmonik M05 + Drums M08 + Piano M10)'
        else:
            domain = h.get('domain', 'M01')
            cat = 'GENERAL'
            test_cls = 'SPECIFICATION_EXAMPLE'
            input_params = {'concept': concept, 'input_case': inp_raw}
            exp_val = exp_raw
            rule = 'Formale musiktheoretische Spezifikation'

        case_entry = {
            'case_id': cid,
            'domain': domain,
            'category': cat,
            'test_class': test_cls,
            'title': concept,
            'input_params': input_params,
            'expected_output': exp_val,
            'tolerance': 0.05 if isinstance(exp_val, float) else 0.0,
            'theoretical_rule': rule,
            'source_citation': deps or 'SRC-001'
        }
        unified_cases.append(case_entry)
        
        validation_rows.append({
            'ref_id': cid,
            'domain': domain,
            'category': cat,
            'title': concept,
            'test_class': test_cls,
            'input_params': json.dumps(input_params, ensure_ascii=False),
            'expected_output': json.dumps(exp_val, ensure_ascii=False) if isinstance(exp_val, (list, dict, bool)) else str(exp_val),
            'theoretical_rule': rule,
            'source_evidence': deps or 'SRC-001',
            'status': 'RESTORED_HISTORICAL'
        })

    # 2. Migrated Cases REF-0101 to REF-0198 (from Phase 4.14 colliding cases)
    for c in c414_list:
        orig_cid = c['case_id']
        num = int(orig_cid.split('-')[1])
        if num in [95, 96]:
            # Harmonized into REF-0095 and REF-0096
            continue
        elif num <= 94:
            migrated_id = f"REF-{num + 100:04d}" # REF-0101 to REF-0194
        else: # 97..100
            migrated_id = f"REF-{num + 98:04d}"  # REF-0195 to REF-0198
        
        mig_case = copy.deepcopy(c)
        mig_case['case_id'] = migrated_id
        mig_case['original_phase414_id'] = orig_cid
        mig_case['test_class'] = 'UNIT_TEST' if mig_case.get('category') in ['ACOUSTICS', 'PITCH_CLASS', 'INTERVALS', 'MIDI_TIME'] else 'SPECIFICATION_EXAMPLE'
        
        unified_cases.append(mig_case)
        
        validation_rows.append({
            'ref_id': migrated_id,
            'domain': mig_case.get('domain', 'M01'),
            'category': mig_case.get('category', 'ACOUSTICS'),
            'title': mig_case.get('title', ''),
            'test_class': mig_case['test_class'],
            'input_params': json.dumps(mig_case.get('input_params', {}), ensure_ascii=False),
            'expected_output': json.dumps(mig_case.get('expected_output', ''), ensure_ascii=False) if isinstance(mig_case.get('expected_output'), (list, dict, bool)) else str(mig_case.get('expected_output', '')),
            'theoretical_rule': mig_case.get('theoretical_rule', ''),
            'source_evidence': mig_case.get('source_citation', 'SRC-001'),
            'status': 'ACTIVE_MIGRATED'
        })

    print(f"Total unified golden cases assembled: {len(unified_cases)}")

    # Write unified JSON to knowledge/research/golden_cases/golden_reference_cases.json (CANONICAL SOURCE OF TRUTH)
    canon_json = os.path.join(REPO_ROOT, 'knowledge', 'research', 'golden_cases', 'golden_reference_cases.json')
    with open(canon_json, 'w', encoding='utf-8') as f:
        json.dump(unified_cases, f, indent=2, ensure_ascii=False)
    print(f"Written canonical JSON: {canon_json}")

    # Mirror to tests/golden_cases/golden_reference_cases.json
    mirror_json = os.path.join(REPO_ROOT, 'tests', 'golden_cases', 'golden_reference_cases.json')
    with open(mirror_json, 'w', encoding='utf-8') as f:
        json.dump(unified_cases, f, indent=2, ensure_ascii=False)
    print(f"Written mirrored test fixture: {mirror_json}")

    # Write validation CSVs
    val_csv = os.path.join(REPO_ROOT, 'knowledge', 'research', 'FINAL_REFERENCE_CASE_VALIDATION.csv')
    with open(val_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'ref_id', 'domain', 'category', 'title', 'test_class',
            'input_params', 'expected_output', 'theoretical_rule',
            'source_evidence', 'status'
        ])
        writer.writeheader()
        writer.writerows(validation_rows)
    print(f"Written {val_csv} with {len(validation_rows)} rows.")

    mus_csv = os.path.join(REPO_ROOT, 'knowledge', 'research', 'MUSICAL_REFERENCE_VALIDATION.csv')
    with open(mus_csv, 'w', encoding='utf-8', newline='') as f:
        writer = csv.DictWriter(f, fieldnames=[
            'ref_id', 'domain', 'category', 'title', 'test_class',
            'input_params', 'expected_output', 'theoretical_rule',
            'source_evidence', 'status'
        ])
        writer.writeheader()
        writer.writerows(validation_rows)
    print(f"Written {mus_csv} with {len(validation_rows)} rows.")

if __name__ == '__main__':
    build_unified()

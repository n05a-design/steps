"""Inventory remaining cases and original Fable findings without granting approvals."""

import argparse
from collections import Counter
import csv
import io
import json
from pathlib import Path
import re

ROOT=Path(__file__).resolve().parents[1]


def write_csv(path,rows):
    with path.open('w',encoding='utf-8',newline='') as target:
        writer=csv.DictWriter(target,fieldnames=rows[0].keys());writer.writeheader();writer.writerows(rows)


def pending_cases(benchmark):
    cases=json.loads((ROOT/'knowledge/benchmark/cases.json').read_text(encoding='utf-8'))['cases']
    by_id={c['id']:c for c in cases};rows=[]
    for result in benchmark['results']:
        if result['status']!='PENDING':continue
        case=by_id[result['id']];ident=case['id']
        if case['method']=='coach':group='EXTERNAL_COACH_REVIEW';need='Reale Antwort samt Modell-/Skill-Version, Quellen und unabhängiger menschlicher Bewertung.'
        elif ident.startswith('KB-HISTORY-F'):group='CSS_RIGHTS_AND_ARCHIVE_AUTHORITY';need='Bundle-Rechte und dauerhafte Archivzuordnung; vorhandene Byte-/Herkunftskette ersetzt diese nicht.'
        elif 'PPR-MIDI' in ident:group='ORIGINAL_DELIVERY_AND_RIGHTS';need='Vollständige Originallieferung, README-Zuordnung und Rechtebeleg. 112 technisch lesbare SMFs beweisen keine Paketprovenienz.'
        elif ident=='KB-GRAPH-NODES':group='GRAPH_EXPERT_REVIEW';need='Sechs historische Bedeutungen und Vorschläge sowie alle Kanten fachlich abnehmen; keine Vollabnahme aus Modelltests.'
        elif ident=='KB-SRC-033-PROVENANCE':group='BIBLIOGRAPHIC_IDENTITY';need='Historische Robert-Prehn-Publikation belegen oder autorisierte Ablösung; Oliver-Prehn-Chart ist ein anderes Werk.'
        else:group='HUMAN_LISTEN_PLAY';need='Benannte Person führt die notierte Hör-/Spielprobe durch; Kriterien und Gegenurteile erhalten.'
        rows.append({'case_id':ident,'content':case['content'],'status':'PENDING','blocker_class':group,
                     'required_evidence':need,'criteria':json.dumps(case['expected'],ensure_ascii=False),
                     'next_step':case['next_step'],'automatic_approval':False})
    return rows


def fable_findings():
    document=ROOT/'docs/audit/fable-5.2/STEPS_FABLE_5_2_MASSNAHMENPLAN.md'
    rows=[]
    tests={'M1':'tests/test_pilot_review_evidence.py','M2':'.agents/skills/steps-knowledge-curation/tests',
           'M3':'tests/test_notation_contract.py','M4':'tests/test_progression_engine.py',
           'M5':'tests/test_golden_reference_cases.py','M6':'tests/test_pilot_publication.py',
           'M7':'tests/test_voicing_contract.py','M8':'tests/test_voicing_contract.py','M9':'scripts/audit_graph.py'}
    for number,line in enumerate(document.read_text(encoding='utf-8').splitlines(),1):
        if not re.match(r'\| F-[A-Z0-9-]+ \|',line):continue
        ident,priority,packages,note=[s.strip() for s in line.strip('|').split('|')]
        references=[tests[k] for k in tests if k in packages]
        status='TECHNICAL_COUNTERCHECK_WITH_ACCEPTANCE_BOUNDARY'
        if ident in {'F-W02-01','F-W07-01','F-W04-01'}:status='PARTIAL_SOURCE_AND_EXPERT_REVIEW_OPEN'
        if ident=='F-A04-01':status='ARCHITECTURE_DISTRIBUTION_SCOPE_OPEN'
        rows.append({'finding_id':ident,'original_priority':priority,'packages':packages,
                     'original_locator':document.relative_to(ROOT).as_posix()+':'+str(number),
                     'original_finding':note,'current_status':status,'validation_references':';'.join(references),
                     'boundary':'Testreferenzen sind technische Gegenprüfungen, keine pauschale Fachabnahme oder erneute Einzelreproduktion jeder historischen Probe.'})
    if len(rows)!=33 or len({r['finding_id'] for r in rows})!=33:raise ValueError('Fable scope differs from 33 findings')
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--benchmark',type=Path,required=True)
    args=parser.parse_args();document=json.loads(args.benchmark.read_text(encoding='utf-8'))
    pending=pending_cases(document);findings=fable_findings()
    write_csv(ROOT/'docs/audit/fable-5.2/NACHT_PENDING_2026-11-14.csv',pending)
    write_csv(ROOT/'docs/audit/fable-5.2/NACHT_FABLE_ABGLEICH_2026-11-14.csv',findings)
    print(json.dumps({'pending_cases':len(pending),'groups':dict(Counter(r['blocker_class'] for r in pending)),'fable_findings':len(findings)}))


if __name__=='__main__':main()

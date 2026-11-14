"""Track all 58 originally open edges and reject ambiguous historical aliases."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts import audit_graph
from scripts.audit_conflict_revisions import source_bytes

SCOPE=Path('knowledge/relations/GRAPH_FOLLOWUP_PROBES.json')
IDENTITIES=Path('knowledge/relations/VERSIONED_ERROR_IDENTITIES.json')
MATRIX=Path('docs/audit/fable-5.2/GRAPH_FORTSETZUNG_58_2026-11-14.csv')
REPLACEMENTS={
    'CR-001':'USES_REFERENCE_FOR_DECLARED_FREQUENCY_CONVERSION',
    'CR-008':'HAS_INTEGER_SEMITONE_REPRESENTATION_WHEN_12TET',
    'CR-015':'HAS_BASS_NOTE_WITH_INVERSION_IF_CHORD_TONE',
    'CR-024':'HAS_SEPARATE_PULSE_AND_PITCH_PARAMETERS',
    'CR-026':'HAS_ALTERNATIVE_SUBDIVISION_GRID',
    'REL-003':'HAS_EXPLICIT_SHELL_EXERCISE',
    'REL-004':'HAS_MINIMUM_WITHIN_DECLARED_VOICING_SPACE',
    'REL-008':'HAS_NEW_DROP2_EXERCISE',
    'REL-022':'HAS_RH_ROOTLESS_EXERCISE_WITH_LH_ROOT',
    'CR-038':'HAS_EXPLICIT_TRANSPOSED_EXERCISE',
    'REL-002':'HAS_NEW_ARPEGGIO_EXERCISE',
    'REL-012':'HAS_EXPLICIT_GRID_OVERLAY',
    'REL-018':'HAS_EXPLICIT_GRID_OVERLAY',
    'CDR-017':'HAS_SCOPED_2023_REGRESSION_MODEL',
    'REL-020':'REQUIRES_VERSIONED_ERROR_TARGET_DECISION',
    'CDR-012':'CHANGES_CHORD_QUALITY_WITH_SAME_ROOT',
}


def identities(document=None):
    document=document if document is not None else json.loads((ROOT/IDENTITIES).read_text(encoding='utf-8'))
    if (document.get('schema_version')!=1 or document.get('automatic_bare_id_alias_allowed') is not False
            or len(document['records'])!=2
            or {r['namespace'] for r in document['records']}!={'PHASE4_8_ARCHIVE','REGISTER_9AFAF33'}):
        raise ValueError('Ambiguous aliases must stay disabled')
    result={}
    for record in document['records']:
        if (record['versioned_id'] in result or record['bare_id']!='ERR-026'
                or record['versioned_id']!=record['bare_id']+'@'+record['namespace']
                or record['status']!='SOURCE_IDENTITY_ONLY' or record['human_review']!='AUSSTEHEND'
                or record['production_use_allowed'] is not False):raise ValueError('Invalid versioned error identity')
        expected_path=('archive/audit-history/ontology-recovery-2026-11-14/originals/20261111T0040_Phase4_8/MUSIC_KNOWLEDGE_CORRECTIONS.md'
                       if record['namespace']=='PHASE4_8_ARCHIVE' else 'knowledge/research/MUSICAL_ERROR_REGISTER.csv')
        if record['source']['path']!=expected_path:raise ValueError('Source namespace swapped')
        source_bytes(record['source']);result[record['versioned_id']]=record
    return result


def resolve_error(identifier,document=None):
    records=identities(document)
    if identifier in records:return records[identifier]
    if identifier=='ERR-026':raise ValueError('Ambiguous ERR-026: explicit source namespace required')
    raise ValueError('Unknown versioned error identity')


def audit():
    scope=json.loads((ROOT/SCOPE).read_text(encoding='utf-8'))
    ids=scope['original_open_edges']
    if (scope.get('schema_version')!=1 or len(ids)!=58 or len(set(ids))!=58
            or sha256(json.dumps(sorted(ids)).encode()).hexdigest()!='6079ccf1d03c0314491b9c41289049126e08e6f74d6462e338348e099e9efb8a'
            or scope['human_review']!='AUSSTEHEND' or scope['production_use_allowed'] is not False):
        raise ValueError('Invalid original open-edge scope')
    identities()
    plan=json.loads((ROOT/audit_graph.PLAN).read_text(encoding='utf-8'))
    probes={p['id']:p for p in plan['probes']}
    if (len(scope['probe_ids'])!=16 or len(set(scope['probe_ids']))!=16
            or any(p not in probes or probes[p]['kind']!='followup' for p in scope['probe_ids'])):
        raise ValueError('Incomplete follow-up probe inventory')
    if scope.get('reused_probe_ids')!=['SAME_ROOT_SHIFT'] or 'SAME_ROOT_SHIFT' not in probes:
        raise ValueError('Missing explicitly reused quality-shift probe')
    selected=scope['probe_ids']+scope['reused_probe_ids']
    graph,outcomes=audit_graph.audit();reviews={r['relation_id']:r for r in graph};rows=[]
    for ident in ids:
        row=reviews[ident];bound=[p for p in selected if ident in probes[p]['relations']]
        category=row['review_category']
        kind=('EXECUTABLE_PROPOSAL_REVIEW_REQUIRED' if bound else
              'EXTERNAL_CORPUS_REQUIRED' if category=='CORPUS_REQUIRED' else
              'EXTERNAL_HUMAN_REVIEW_REQUIRED' if category in {'PLAY_REVIEW','DIDACTIC_REVIEW'} else
              'EXACT_SOURCE_OR_SEMANTIC_DECISION_REQUIRED')
        rows.append({'relation_id':ident,'original_row_sha256':row['original_row_sha256'],
                     'source_id':row['source_id'],'target_id':row['target_id'],'historical_relation_type':row['relation_type'],
                     'historical_relation_status':row['relation_status'],'followup_status':kind,
                     'proposal_relation_type':REPLACEMENTS.get(ident,''),'validation_probe_ids':';'.join(bound),
                     'validation_status':'PASS' if bound and all(outcomes[p]['status']=='PASS' for p in bound) else 'NOT_EXECUTED' if not bound else 'FAIL',
                     'evidence_and_limit':row['review_note'],'required_next_action':row['blocker_and_action'],
                     'human_approval':'AUSSTEHEND','production_use_allowed':False})
    return rows


def render(rows):
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows);return out.getvalue()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    rows=audit();text=render(rows)
    if args.write:(ROOT/MATRIX).write_text(text,encoding='utf-8')
    if args.check and (ROOT/MATRIX).read_text(encoding='utf-8')!=text:raise SystemExit('Follow-up matrix stale')
    print(json.dumps({'original_open_scope':len(rows),'followup':dict(Counter(r['followup_status'] for r in rows)),
                      'human_approvals':0}))
    if any(r['validation_status']=='FAIL' for r in rows):raise SystemExit(1)


if __name__=='__main__':main()

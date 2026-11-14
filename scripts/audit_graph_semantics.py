"""Check 18 scoped relation proposals without approving historical assertions."""
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

PLAN=Path('knowledge/relations/GRAPH_SEMANTIC_PROPOSALS.json')
MATRIX=Path('docs/audit/fable-5.2/GRAPH_SEMANTIK_18_2026-11-14.csv')
SCOPE_HASH='322c44d295e1559db246ce3b0cb50bd9f1ae1a9cf165194328ddf2a1510562ba'
TYPES={'IS_REFERENCE_INTERVAL_FOR','INTERPRETED_IN_DECLARED_NOTATION','USES_KEY_DEPENDENT_SPELLING',
       'MAPS_PRIMARY_FUNCTION_SUBSET','REPRESENTABLE_BY_PPQ_AUDIT_CONTROL','HAS_EXPLICIT_PAIR_TIMING',
       'HAS_PROFILE_DEPENDENT_DRUM_MAPPING','CAN_BE_ACCOMPANIED_BY','HAS_EXPLICIT_SWING_EXERCISE',
       'DERIVES_SELECTED_TRIAD_INSTANCES','HAS_PROFILE_DEPENDENT_CHANNEL_MAP','HAS_SOURCE_BOUND_CROSS_STICK_TIMELINE',
       'REQUIRES_MODE_FOR_LEADING_TONE_ANALYSIS','HAS_EXPLICIT_METRIC_OVERLAY_DRAFT',
       'HAS_NEW_PIANO_DRAFT_NOT_TRANSCRIPTION','HAS_ATTRIBUTED_ANALOGY_NOT_VERIFIED_ORIGIN',
       'USES_SCOPED_GM1_BASE_MAP','HAS_SOURCE_DEPENDENT_ROLE_ACCENT'}
GUARDED_CONTEXT={'midi_profile':'GM1','mapping_scope':'PERCUSSION','historical_transcription':False,
                 'historical_origin_verified':False,'namespace':'PHASE4_MASTER_20261110',
                 'index_base':0,'exporter_scope':'AUDIT_CONTROL','time_format':'PPQ'}


def eligible_for_review(proposal,context):
    """Eligibility for a scoped proposal, never acceptance of a musical claim."""
    return all(k in context and type(context[k])is type(v) and context[k]==v
               for k,v in proposal['required_context'].items())


def validate(document,relations,probes):
    rows=document['proposals'];by={r['relation_id']:r for r in relations}
    ids=[r['historical_relation_id'] for r in rows]
    if (document.get('schema_version')!=1 or len(ids)!=18 or len(set(ids))!=18
            or sha256(json.dumps(sorted(ids)).encode()).hexdigest()!=SCOPE_HASH):
        raise ValueError('The original 18-case semantic scope must be preserved')
    for row in rows:
        ident=row['historical_relation_id'];original=by[ident]
        if (row['original_row_sha256']!=sha256(json.dumps(original,ensure_ascii=False,sort_keys=True).encode()).hexdigest()
                or row['original_edge']!={k:original[k] for k in ['source_id','target_id','relation_type']}
                or row['proposed_relation_type'] not in TYPES or not row['required_context']
                or not all(isinstance(k,str) and k and type(v)in (str,int,bool) for k,v in row['required_context'].items())
                or not row['excluded_claims'] or not all(isinstance(x,str) and x.strip() for x in row['excluded_claims'])
                or not row['remaining_requirement'].strip() or not row['source_note'].strip()
                or row['human_approval']!='AUSSTEHEND' or row['review_status']!='REVIEW_REQUIRED'
                or row['production_use_allowed'] is not False or row['historical_assertion_closed'] is not False
                or any(p not in probes or ident not in probes[p]['relations'] for p in row['probe_ids'])):
            raise ValueError('Invalid scoped proposal or premature approval: '+ident)
        for key,value in GUARDED_CONTEXT.items():
            if key in row['required_context'] and (type(row['required_context'][key])is not type(value)
                                                   or row['required_context'][key]!=value):
                raise ValueError('Protected scope or evidence boundary changed: '+ident)
        if not eligible_for_review(row,row['required_context']) or eligible_for_review(row,{}):
            raise ValueError('Unconditional interpretation is forbidden')


def audit(document=None):
    document=document if document is not None else json.loads((ROOT/PLAN).read_text(encoding='utf-8'))
    relations=audit_graph.read_csv(ROOT/'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv')
    plan=json.loads((ROOT/audit_graph.PLAN).read_text(encoding='utf-8'));probes={p['id']:p for p in plan['probes']}
    validate(document,relations,probes);graph,outcomes=audit_graph.audit();current={r['relation_id']:r for r in graph};rows=[]
    for p in document['proposals']:
        ident=p['historical_relation_id'];bound=p['probe_ids']
        states=[outcomes[x]['status'] for x in bound]
        rows.append({'relation_id':ident,'original_row_sha256':p['original_row_sha256'],
                     'historical_relation_type':p['original_edge']['relation_type'],
                     'proposal_relation_type':p['proposed_relation_type'],
                     'required_context':json.dumps(p['required_context'],ensure_ascii=False,sort_keys=True),
                     'contract_validation':'PASS','model_status':'FAIL' if 'FAIL' in states else 'PASS' if states else 'NOT_EXECUTED',
                     'probe_ids':';'.join(bound),'historical_relation_status':current[ident]['relation_status'],
                     'remaining_requirement':p['remaining_requirement'],
                     'human_approval':'AUSSTEHEND','production_use_allowed':False,'historical_assertion_closed':False})
    return rows


def render(rows):
    out=io.StringIO(newline='');w=csv.DictWriter(out,fieldnames=rows[0],lineterminator='\n');w.writeheader();w.writerows(rows);return out.getvalue()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    rows=audit();text=render(rows)
    if args.write:(ROOT/MATRIX).write_text(text,encoding='utf-8')
    if args.check and (ROOT/MATRIX).read_text(encoding='utf-8')!=text:raise SystemExit('Semantic matrix stale')
    print(json.dumps({'proposals':len(rows),'contract_checks':dict(Counter(r['contract_validation'] for r in rows)),
                      'model_checks':dict(Counter(r['model_status'] for r in rows)),
                      'historical_assertions_closed':0,'human_approvals':0}))
    if any(r['model_status']=='FAIL' for r in rows):raise SystemExit(1)


if __name__=='__main__':main()

"""Build an evidence-separated audit matrix for every immutable historical edge."""

import argparse
from collections import Counter
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import sys

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts import graph_probes

PLAN = Path('knowledge/relations/GRAPH_AUDIT_PLAN.json')
MATRIX = Path('knowledge/relations/GRAPH_AUDIT_MATRIX.csv')


def validate_proposals(document, relations, probes, expected_nodes):
    rows=document['proposals']
    if (document.get('schema_version')!=1 or document.get('status')!='REVIEW_REQUIRED'
            or document.get('production_use_allowed') is not False
            or document.get('historical_definitions_resolved') is not False
            or len(rows)!=len(expected_nodes) or {r['historical_node_id'] for r in rows}!=set(expected_nodes)):
        raise ValueError('Invalid or prematurely approved node proposals')
    by_id={r['relation_id']:r for r in relations}
    for row in rows:
        if (not row['relation_ids'] or any(i not in by_id or row['historical_node_id'] not in
                (by_id[i]['source_id'],by_id[i]['target_id']) for i in row['relation_ids'])
                or row['proposed_id']==row['historical_node_id']
                or (row['probe_id'] is not None and row['probe_id'] not in probes)
                or not all(isinstance(row[k],str) and row[k].strip() for k in
                           ('definition','original_locator','source_url','source_scope','blocker'))):
            raise ValueError('Unbound node proposal')


def read_csv(path):
    with path.open(encoding='utf-8-sig', newline='') as source:
        return list(csv.DictReader(source))


def validate(plan, relations, root=ROOT):
    if plan.get('schema_version') != 1 or len(relations) != 97:
        raise ValueError('Unknown graph scope')
    originals = {r['relation_id']: r for r in relations}
    reviews = plan['reviews']
    if len(reviews) != 97 or {r['relation_id'] for r in reviews} != originals.keys():
        raise ValueError('Missing, duplicate or unexpected edge review')
    probes = plan['probes']
    if len(probes) != len({p['id'] for p in probes}):
        raise ValueError('Duplicate graph probe')
    by_probe = {p['id']: p for p in probes}
    claim_ids={r['claim_id'] for r in read_csv(root/'knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv')}
    for probe in probes:
        if not probe['relations'] or not set(probe['relations']) <= originals.keys():
            raise ValueError('Probe references unknown edge')
    for row in reviews:
        original = originals[row['relation_id']]
        digest = sha256(json.dumps(original, ensure_ascii=False, sort_keys=True).encode()).hexdigest()
        if (row['original_row_sha256'] != digest or row['edge'] != {k: original[k] for k in ('source_id','target_id','relation_type')}
                or row['human_review'] != 'AUSSTEHEND' or row['production_use_allowed'] is not False
                or row['source_assertion_verified'] is not False
                or not set(row.get('candidate_claim_ids', [])) <= claim_ids
                or not row['review_note'].strip() or not row['action'].strip()
                or not row['references'] or any(not (root / p).is_file() or Path(p).is_absolute() or '..' in Path(p).parts for p in row['references'])
                or any(p not in by_probe or row['relation_id'] not in by_probe[p]['relations'] for p in row['probe_ids'])):
            raise ValueError('Changed original, invalid evidence or premature approval: '+row['relation_id'])
        if 'scoped_source_evidence' in row:
            evidence=row['scoped_source_evidence']
            if (evidence.get('status')!='PRIMARY_NOTATION_SCOPED_CHECK'
                    or not evidence.get('url','').startswith('https://www.shermusic.com/')
                    or not evidence.get('locator') or not re.fullmatch(r'[0-9a-f]{64}',evidence.get('pdf_sha256',''))):
                raise ValueError('Invalid scoped source evidence')
    if next(r for r in reviews if r['relation_id']=='CDR-010')['category'] != 'COUNTEREXAMPLE':
        raise ValueError('Historical CDR-010 failure must remain visible')
    return by_probe


def audit(root=ROOT, plan=None):
    plan = plan or json.loads((root / PLAN).read_text(encoding='utf-8'))
    relations = read_csv(root / 'knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv')
    probes = validate(plan, relations, root)
    expected_nodes={r['node_id'] for r in read_csv(root/'docs/audit/fable-5.2/GRAPH_RESTKNOTEN_NACH_ORIGINALFUND_2026-11-14.csv')}
    validate_proposals(json.loads((root/'knowledge/relations/NODE_DEFINITION_PROPOSALS.json').read_text(encoding='utf-8')),
                       relations,probes,expected_nodes)
    outcomes = {}
    for ident, spec in probes.items():
        try:
            outcomes[ident] = {'status':'PASS', 'observed': graph_probes.evaluate(spec)}
        except (ValueError, AssertionError, TypeError, KeyError) as error:
            outcomes[ident] = {'status':'FAIL', 'observed': str(error)}
    nodes = {}
    for name in ('HISTORICAL_NODE_EVIDENCE.csv','MUSIC_NODE_EVIDENCE.csv','FORMAT_NODE_EVIDENCE.csv'):
        for node in read_csv(root/'knowledge/relations'/name):
            nodes[node['node_id']] = f"{node.get('namespace','EXPLICIT_SCOPED_NODE')} | {node['source_url']} | {node['locator']}"
    prior_sources={r['relation_id']:r for r in read_csv(root/'knowledge/relations/RELATION_EVIDENCE.csv')}
    versioned_errors=json.loads((root/'knowledge/relations/VERSIONED_ERROR_IDENTITIES.json').read_text(encoding='utf-8'))['records']
    from scripts import run_knowledge_benchmark as benchmark
    from src.steps.progression import reviewed
    examples, claims = reviewed._candidates()
    old_checks = benchmark.run([c for c in benchmark.load_cases() if c['method']=='graph_sample'],examples,claims,{})
    by_old = {}
    for check in old_checks:
        by_old.setdefault(check['content'],[]).append(check)
    rows=[]
    for review in plan['reviews']:
        ident=review['relation_id']; checks=[outcomes[p] for p in review['probe_ids']]
        old=by_old.get(ident,[])
        states=[c['status'] for c in checks+old]
        technical='FAIL' if 'FAIL' in states else 'PASS' if states else 'NOT_EXECUTED'
        sample_supported=(review['category'] in {'MODEL_SAMPLE','EXISTING_SAMPLE'} and technical=='PASS')
        relation_status='FAIL' if ident=='CDR-010' else 'SAMPLE_SUPPORTED' if sample_supported else 'OPEN'
        endpoints=[]
        for term in review['edge'].values():
            if term in nodes: endpoints.append(term+': '+nodes[term])
            elif re.fullmatch(r'(?:PROG[-_]\d{3}|PAT-\d{3}|P\d{2})',term):endpoints.append(term+': project catalog definition; no automatic musical approval')
            elif re.fullmatch(r'M\d{2}',term):endpoints.append(term+': DOMAIN CONTEXT REQUIRED; historical and later domains differ')
        if ident=='REL-020':
            endpoints += [r['versioned_id']+' | '+r['source']['path']+' | '+r['source']['sha256']
                          for r in versioned_errors]
        source=prior_sources.get(ident)
        source_status='PRIOR_SOURCE_SAMPLE_DOCUMENTED' if source and source['assessment']=='SOURCE_SUPPORTED_SAMPLE' else 'PROJECT_RECORD_ONLY'
        source_locator=f"{source['source_url']} | {source['locator']}" if source else ';'.join(review['references'])
        if 'scoped_source_evidence' in review:
            evidence=review['scoped_source_evidence']
            source_status='CURRENT_PRIMARY_NOTATION_SCOPED_CHECK'
            source_locator=evidence['url']+' | '+evidence['locator']+' | PDF SHA-256 '+evidence['pdf_sha256']
        if ident in {'REL-033','CDR-022'}:
            source_status='CURRENT_SOURCE_PAGE_PARTIAL_CHECK'
            source_locator='https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/ | Content: step, alter optional, octave; semitones decimal type. No full converter proof.'
        definition_status=lambda term: ('HISTORICAL_DEFINITION' if term in nodes and re.fullmatch(r'M\d{2}-\d{2}',term) else
                                      'SCOPED_NODE_DEFINITION' if term in nodes else 'PROJECT_CATALOG' if re.fullmatch(r'(?:PROG[-_]\d{3}|PAT-\d{3}|P\d{2})',term) else
                                      'DOMAIN_CONTEXT_REQUIRED' if re.fullmatch(r'M\d{2}',term) else 'UNRESOLVED')
        rows.append({'relation_id':ident,**review['edge'],'original_row_sha256':review['original_row_sha256'],
                     'source_definition_status':definition_status(review['edge']['source_id']),
                     'target_definition_status':('AMBIGUOUS_VERSIONED_IDENTITY' if ident=='REL-020'
                                                 else definition_status(review['edge']['target_id'])),
                     'definition_evidence':' || '.join(endpoints) or 'UNRESOLVED',
                     'source_assertion_status':source_status,'source_locator':source_locator,
                     'candidate_claim_ids':';'.join(review.get('candidate_claim_ids',[])),
                     'technical_status':technical,'probe_ids':';'.join(review['probe_ids']),
                     'existing_benchmark_ids':';'.join(c['id'] for c in old),'relation_status':relation_status,
                     'review_category':review['category'],'review_note':review['review_note'],
                     'human_review':'AUSSTEHEND','production_use_allowed':False,
                     'references':';'.join(review['references']),'blocker_and_action':review['action']})
    return rows,outcomes


def render(rows):
    target=io.StringIO(newline='')
    writer=csv.DictWriter(target,fieldnames=rows[0].keys(),lineterminator='\n')
    writer.writeheader();writer.writerows(rows)
    return target.getvalue()


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--write',action='store_true')
    parser.add_argument('--check',action='store_true')
    parser.add_argument('--json-out',type=Path)
    args=parser.parse_args();rows,probes=audit();content=render(rows)
    if args.write:(ROOT/MATRIX).write_text(content,encoding='utf-8')
    if args.check and (ROOT/MATRIX).read_text(encoding='utf-8')!=content:raise SystemExit('Graph matrix is stale')
    if args.json_out:args.json_out.write_text(json.dumps({'edges':rows,'probes':probes},ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({'edges':len(rows),'relation_status':dict(Counter(r['relation_status'] for r in rows)),
                      'technical_status':dict(Counter(r['technical_status'] for r in rows)),
                      'probe_status':dict(Counter(p['status'] for p in probes.values())), 'human_approvals':0}))
    if any(p['status']=='FAIL' for p in probes.values()):raise SystemExit(1)


if __name__=='__main__':main()

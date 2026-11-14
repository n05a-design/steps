"""Executable, source-bound proposals for seven Golden conflicts; originals stay frozen."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import re
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_golden_remaining import calculate as bounded, fingerprint
from src.steps.theory import parse_chord

PLAN=Path('knowledge/research/golden_cases/CONFLICT_REVISION_PROPOSALS.json')
MATRIX=Path('docs/audit/fable-5.2/GOLDEN_KONFLIKTREVISIONEN_2026-11-14.csv')
CONFLICT_IDS={'REF-0016','REF-0017','REF-0051','REF-0052','REF-0062','REF-0063','REF-0073'}


def source_bytes(source,root=ROOT):
    path=(root/source['path']).resolve()
    if not path.is_relative_to(root.resolve()):raise ValueError('Source escapes repository')
    data=path.read_bytes()
    if source.get('hash_mode')=='git_text_lf':data=data.replace(b'\r\n',b'\n')
    elif source.get('hash_mode')!='bytes':raise ValueError('Unknown source hash convention')
    if sha256(data).hexdigest()!=source['sha256']:raise ValueError('Source version changed: '+source['path'])
    return data


def calculate(model,root=ROOT):
    kind,data=model['kind'],model['input']
    if kind=='chord_identity':
        chord=parse_chord(data['symbol'],'INT')
        return {'chord_pcs':sorted(map(int,chord.pitch_class_set)),
                'bass_pc':int((chord.bass or chord.root).pitch_class)}
    if kind=='chord_sequence':
        return [sorted(map(int,parse_chord(c,'INT').pitch_class_set)) for c in data['symbols']]
    if kind=='historical_dnb':
        text=source_bytes(data['source'],root).decode('utf-8')
        section=re.search(r'### '+re.escape(data['pattern'])+r':[^\n]+(?P<body>.*?)(?=\n### |\Z)',text,re.S)
        if not section:raise ValueError('Missing original pattern section')
        bpm=int(re.search(r'(\d+) BPM',section[0])[1])
        if data['pattern']=='PAT-021':
            hits=[(int(m[1]),m[2]) for m in re.finditer(r'^- \*\*Tick (\d+)[^\n]*?:\*\*(.*)$',section['body'],re.M)]
            return {'bpm':bpm,'kicks':[t for t,s in hits if 'Kick' in s],
                    'ghosts':[t for t,s in hits if 'Snare Ghost' in s],'documented_bars':1}
        if data['pattern']=='PAT-022':
            m=re.search(r'Kick[^\n]*?Tick (\d+) und Tick (\d+)',section['body'])
            if not m:raise ValueError('Missing explicit historical kick positions')
            return {'bpm':bpm,'kicks':[int(m[1]),int(m[2])],'documented_bars':2}
        raise ValueError('Unsupported historical pattern')
    if kind=='current_dnb':
        text=source_bytes(data['source'],root).decode('utf-8')
        lines=[line for line in text.splitlines() if line.startswith('| `'+data['pattern']+'` |')]
        if len(lines)!=1:raise ValueError('Ambiguous current catalog row')
        cells=[s.strip() for s in lines[0].strip('|').split('|')]
        bpm=int(re.search(r'(\d+) BPM',cells[2])[1])
        if data['pattern']=='PAT-021':
            return {'bpm':bpm,'kicks':[int(n) for n in re.search(r'\(([^)]+)\)',cells[4])[1].split(',')],
                    'ghosts':[int(n) for n in re.search(r'Ticks ([^)]+)',cells[5])[1].split(',')]}
        if data['pattern']=='PAT-022':
            # Parse the explicitly written beats, do not copy the expected ticks.
            m=re.search(r'auf (\d+) und (\d+)\+',cells[4])
            return {'bpm':bpm,'kicks':[480*(int(m[1])-1),480*(int(m[2])-1)+240],
                    'snare_gm':int(re.search(r'\((\d+)\)',cells[5])[1])}
        raise ValueError('Unsupported current pattern')
    return bounded(kind,data)


def audit(document=None,root=ROOT):
    document=document if document is not None else json.loads((root/PLAN).read_text(encoding='utf-8'))
    originals={c['case_id']:c for c in json.loads((root/'knowledge/research/golden_cases/golden_reference_cases.json').read_text(encoding='utf-8'))}
    revisions=document['revisions']
    if (document.get('schema_version')!=1 or len(revisions)!=7
            or {r['historical_case_id'] for r in revisions}!=CONFLICT_IDS):raise ValueError('Seven original identities required')
    rows=[];ids=set()
    for revision in revisions:
        ident=revision['historical_case_id']
        if (revision['original_sha256']!=fingerprint(originals[ident]) or revision['historical_status']!='CONFLICT_RETAINED'
                or revision['review_status']!='REVIEW_REQUIRED' or revision['production_use_allowed'] is not False
                or revision['human_approval']!='AUSSTEHEND' or not revision['decision_required'].strip()
                or len(revision['variants'])<2):raise ValueError('Changed original or premature acceptance')
        for source in revision['sources']:source_bytes(source,root)
        for variant in revision['variants']:
            if variant['id'] in ids or not variant['id'].startswith(ident+'/PROPOSAL-'):
                raise ValueError('Revision identity collision')
            ids.add(variant['id']);model=variant['model']
            if not variant['scope'].strip() or not variant['title'].strip():raise ValueError('Missing scope')
            observed=calculate(model,root)
            rows.append({'historical_case_id':ident,'original_sha256':revision['original_sha256'],
                         'proposal_id':variant['id'],'proposal_title':variant['title'],
                         'model_status':'PASS' if observed==model['expected'] else 'FAIL',
                         'observed':json.dumps(observed,ensure_ascii=False),
                         'historical_status':'CONFLICT_RETAINED','scope':variant['scope'],
                         'decision_required':revision['decision_required'],'human_approval':'AUSSTEHEND',
                         'production_use_allowed':False})
    return rows


def render(rows):
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=rows[0],lineterminator='\n')
    writer.writeheader();writer.writerows(rows);return out.getvalue()


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--write',action='store_true');parser.add_argument('--check',action='store_true')
    args=parser.parse_args();rows=audit();text=render(rows)
    if args.write:(ROOT/MATRIX).write_text(text,encoding='utf-8')
    if args.check and (ROOT/MATRIX).read_text(encoding='utf-8')!=text:raise SystemExit('Revision matrix stale')
    print(json.dumps({'conflicts':7,'proposals':len(rows),'models':dict(Counter(r['model_status'] for r in rows)),
                      'original_conflicts_closed':0,'human_approvals':0}))
    if any(r['model_status']=='FAIL' for r in rows):raise SystemExit(1)


if __name__=='__main__':main()

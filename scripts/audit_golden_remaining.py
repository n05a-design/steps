"""Version-bound examination of the 64 remaining historical Golden examples.

Typed audit interpretations are separate from original inputs and outcomes.
They never turn contextual claims or human acceptance into software passes.
"""

import argparse
from collections import Counter
import csv
from hashlib import sha256
import json
from pathlib import Path
import re
import sys
from xml.etree import ElementTree

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_golden_supplements import SUPPORTED
from src.steps.theory import parse_chord,parse_spelling,Voicing
from src.steps.progression import get_progression,resolve_roman_degree,absolute_semitone_distance

PLAN=Path('knowledge/research/golden_cases/REMAINING_64_AUDIT.json')
MATRIX=Path('docs/audit/fable-5.2/GOLDEN_64_PRUEFMATRIX_2026-11-14.csv')
ARCHIVE=Path('archive/audit-history/golden-source-recovery-2026-11-14/RECOVERY_MANIFEST.json')
CONFLICTS={'REF-0016':'CONFLICTING_INPUTS','REF-0017':'EXPECTATION_CONFLICT',
           'REF-0051':'EXPECTATION_INCOMPLETE','REF-0052':'CONFLICTING_INPUTS',
           'REF-0062':'VERSION_CONFLICT','REF-0063':'VERSION_CONFLICT',
           'REF-0073':'EXPECTATION_SCOPE_CONFLICT','REF-0176':'STYLE_POLICY_OPEN'}


def fingerprint(case):
    return sha256(json.dumps(case,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def verify_archives(root=ROOT):
    records=json.loads((root/ARCHIVE).read_text(encoding='utf-8'))['records']
    if len(records)!=12 or len({r['archive_path'] for r in records})!=12:
        raise ValueError('Historical recovery scope changed')
    for record in records:
        path=(root/record['archive_path']).resolve()
        if not path.is_relative_to((root/ARCHIVE.parent/'originals').resolve()):
            raise ValueError('Archive path outside preserved originals')
        data=path.read_bytes()
        if len(data)!=record['bytes'] or sha256(data).hexdigest()!=record['sha256']:
            raise ValueError('Historical source bytes changed')
    return len(records)


def calculate(kind,data):
    if kind=='note':
        n=parse_spelling(data['note'],data['convention'])
        return {'pitch_class':int(n.pitch_class),'midi':n.midi_number}
    if kind=='enharmonic':
        a,b=[parse_spelling(s,'INT') for s in data['notes']]
        return {'same_pc':a.pitch_class==b.pitch_class,'same_spelling':a==b,'pc':int(a.pitch_class)}
    if kind=='diatonic':
        n=parse_spelling(data['note'],'INT');scale=[parse_spelling(s,'INT') for s in data['scale']]
        exact=[i+1 for i,s in enumerate(scale) if (s.step,s.alteration)==(n.step,n.alteration)]
        return {'written_degree':exact[0] if exact else None,'pc_present':n.pitch_class in {s.pitch_class for s in scale}}
    if kind=='roman':return [resolve_roman_degree(s,data['key'],convention='INT').symbol for s in data['degrees']]
    if kind=='catalog':
        p=get_progression(data['id'])
        return {'chords':[c.symbol for c in p.chord_definitions],
                'bass':[int((c.bass or c.root).pitch_class) for c in p.chord_definitions]}
    if kind=='union':return sorted(set().union(*(parse_chord(c,'INT').pitch_class_set for c in data['chords'])))
    if kind=='membership':
        pcs=set().union(*(parse_chord(c,'INT').pitch_class_set for c in data['chords']))
        return {'collection':sorted(pcs),'matches_named_collection':pcs==set(data['collection'])}
    if kind=='voice_path':
        notes=[parse_spelling(s,'INT') for s in data['notes']]
        chords=[parse_chord(s,'INT') for s in data['chords']]
        if len(notes)!=len(chords) or any(n.pitch_class not in c.pitch_class_set for n,c in zip(notes,chords)):
            raise ValueError('Voice path is not in the stated chords')
        return {'pcs':[int(n.pitch_class) for n in notes],
                'motions':[b.midi_number-a.midi_number for a,b in zip(notes,notes[1:])]}
    if kind=='l1':return absolute_semitone_distance(data['from'],data['to'])
    if kind=='ticks':
        if data['ppq']<=0:raise ValueError('Nonpositive PPQ')
        return [round((beat-1)*data['ppq']) for beat in data['beats']]
    if kind=='clave':
        return [(bar*4+beat-1)*data['ppq'] for bar,beats in enumerate(data['bars']) for beat in beats]
    if kind=='swing':
        return [{'percent':p,'tick':round(data['ppq']/2*p/100),'offset':round(data['ppq']/2*p/100)-data['ppq']//4}
                for p in data['percent']]
    if kind=='swing_regression':
        if data['slope']>=0 or any(bpm<=0 for bpm in data['bpm']):
            raise ValueError('Invalid bounded regression parameters')
        return [round(max(1,data['slope']*bpm+data['intercept']),4) for bpm in data['bpm']]
    if kind=='duality':return {'fast_bar_seconds':round(240/data['fast'],6),'slow_halfbar_seconds':round(120/data['slow'],6)}
    if kind=='families':
        rotations={tuple(s[i:]+s[:i]) for s in data['families'] for i in range(len(s))}
        if any(len(s)!=7 or sum(s)!=12 for s in data['families']):raise ValueError('Invalid family')
        return len(rotations)
    if kind=='inversion':
        c=parse_chord(data['chord'],'INT');v=c.to_voicing(3,'CLOSE').invert(data['inversion'])
        diff=(v.bass_note-int(c.root.pitch_class))%12
        return 'Root' if diff==0 else 'Third' if diff in (3,4) else 'Fifth' if diff in (6,7,8) else 'Other'
    if kind=='upper_structure':
        lower=sorted(parse_chord(data['lower_chord'],'INT').pitch_class_set-set(data['omit']))
        upper=sorted(parse_chord(data['upper_chord'],'INT').pitch_class_set)
        if data['declared_lower']!=lower or data['declared_upper']!=upper:raise ValueError('Declared pitches conflict with named chords')
        return lower+upper
    if kind=='white_keys':
        pcs=parse_chord(data['chord'],'INT').pitch_class_set
        return pcs <= {0,2,4,5,7,9,11}
    if kind=='xml':
        notes=[ElementTree.fromstring(x) for x in data['pitches']]
        spellings=[parse_spelling(data['names'][i],'INT') for i in range(len(notes))]
        if any((n.findtext('step'),int(n.findtext('alter','0')),int(n.findtext('octave'))) !=
               (s.step,s.alteration,s.octave) for n,s in zip(notes,spellings)):raise ValueError('XML differs from spelling')
        return {'same_midi':spellings[0].midi_number==spellings[1].midi_number,
                'different_step':notes[0].findtext('step')!=notes[1].findtext('step'),'midi':spellings[0].midi_number}
    if kind=='direct_fifth':
        a,b=[parse_spelling(x,'INT').midi_number for x in data['bass']]
        c,d=[parse_spelling(x,'INT').midi_number for x in data['soprano']]
        return {'vertical_intervals':[(c-a)%12,(d-b)%12], 'motions':[b-a,d-c],
                'direct_fifth':(d-b)%12==7 and (b-a)*(d-c)>0,'style_prohibition_determined':False}
    if kind=='signature_order':
        sharps=[re.sub(r'-?\d+$','',parse_spelling(data['sharp_start'],'INT').transpose_diatonic(4*i,7*i).render('INT')) for i in range(7)]
        flats=[re.sub(r'-?\d+$','',parse_spelling(data['flat_start'],'INT').transpose_diatonic(-4*i,-7*i).render('INT')) for i in range(7)]
        return {'sharps':sharps,'flats':flats}
    if kind=='root_presence':
        c=parse_chord(data['chord'],'INT');notes=[parse_spelling(n,'INT') for n in data['notes']]
        return {'contains_root':int(c.root.pitch_class) in {int(n.pitch_class) for n in notes},
                'all_chord_tones':all(n.pitch_class in c.pitch_class_set for n in notes)}
    raise ValueError('Unknown bounded Golden adapter '+kind)


def validate(plan,cases):
    remaining={c['case_id']:c for c in cases if c['test_class']=='SPECIFICATION_EXAMPLE' and c['case_id'] not in SUPPORTED}
    rows=plan['reviews']
    if plan.get('schema_version')!=1 or len(rows)!=64 or {r['case_id'] for r in rows}!=remaining.keys():
        raise ValueError('The complete original 64-case scope must be retained')
    for row in rows:
        if (row['original_sha256']!=fingerprint(remaining[row['case_id']]) or row['human_review']!='AUSSTEHEND'
                or row['production_use_allowed'] is not False or not row['finding'].strip() or not row['next_step'].strip()
                or not row['source_locator'].strip()):raise ValueError('Changed original or premature acceptance')
        if row['case_id'] in CONFLICTS and row['original_assessment']!=CONFLICTS[row['case_id']]:
            raise ValueError('An original conflict or open style policy was hidden')
    return remaining


def audit(plan=None,cases=None):
    verify_archives()
    plan=plan or json.loads((ROOT/PLAN).read_text(encoding='utf-8'))
    cases=cases or json.loads((ROOT/'knowledge/research/golden_cases/golden_reference_cases.json').read_text(encoding='utf-8'))
    original=validate(plan,cases);rows=[]
    for r in plan['reviews']:
        model=r.get('model');observed=None;model_status='NOT_EXECUTED'
        if model:
            try:
                observed=calculate(model['kind'],model['input'])
                model_status='PASS' if observed==model['expected'] else 'FAIL'
            except (ValueError,KeyError,TypeError) as error:observed=str(error);model_status='FAIL'
        rows.append({'case_id':r['case_id'],'original_sha256':r['original_sha256'],
                     'original_assessment':r['original_assessment'],'model_status':model_status,
                     'observed':json.dumps(observed,ensure_ascii=False),'finding':r['finding'],
                     'source_locator':r['source_locator'],'next_step':r['next_step'],
                     'human_review':'AUSSTEHEND','production_use_allowed':False})
    return rows


def render(rows):
    import io
    target=io.StringIO(newline='');writer=csv.DictWriter(target,fieldnames=rows[0],lineterminator='\n');writer.writeheader();writer.writerows(rows)
    return target.getvalue()


def main():
    p=argparse.ArgumentParser(description=__doc__);p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');args=p.parse_args()
    rows=audit();text=render(rows)
    if args.write:(ROOT/MATRIX).write_text(text,encoding='utf-8')
    if args.check and (ROOT/MATRIX).read_text(encoding='utf-8')!=text:raise SystemExit('64-case matrix is stale')
    print(json.dumps({'cases':len(rows),'models':dict(Counter(r['model_status'] for r in rows)),
                      'original_assessments':dict(Counter(r['original_assessment'] for r in rows)),'human_approvals':0}))
    if any(r['model_status']=='FAIL' for r in rows):raise SystemExit(1)


if __name__=='__main__':main()

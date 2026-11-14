"""Additional calculations for sufficiently specified historical examples.

Original classes and source claims remain unchanged. These are bounded
arithmetic/product examples, not expert approval of their musical labels.
"""

import argparse
import csv
import json
from pathlib import Path
import sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))

from src.steps.theory import parse_chord
from src.steps.progression import circular_pc_distance

PAIR_FIELDS={
    'REF-0158':('ab','g'),'REF-0159':('d','e'),'REF-0161':('f_sharp','f_nat'),
    'REF-0163':('minor_3rd','major_3rd'),'REF-0165':('iv_minor_3rd','tonic_5th'),
    'REF-0167':('v_root','vi_root'),
}
SUPPORTED=set(PAIR_FIELDS)|{'REF-0093','REF-0094','REF-0150','REF-0151','REF-0164','REF-0193','REF-0195','REF-0196'}


def calculate(case):
    ident=case['case_id'];data=case['input_params']
    if ident in PAIR_FIELDS:
        first,second=(data[k] for k in PAIR_FIELDS[ident])
        return circular_pc_distance([first],[second])
    if ident in {'REF-0093','REF-0094','REF-0150','REF-0151'}:
        chord=parse_chord(data['chord'],'INT')
        # These historical A/B examples retain the theoretical fifth.
        # The runtime ROOTLESS layout may intentionally omit it, so its
        # reduction policy must not be mistaken for this separate example.
        a=[48+int(chord.root.pitch_class)+interval for interval in chord.theoretical_intervals if interval%12]
        if len(a)!=4:raise ValueError('Specified example needs four rootless tones')
        layout=data['type'].removeprefix('Typ ')
        if layout=='B':a=a[2:]+[x+12 for x in a[:2]]
        elif layout!='A':raise ValueError('Unknown historical layout')
        return a if ident in {'REF-0093','REF-0094'} else [x%12 for x in a]
    if ident=='REF-0164':
        roots=data['roots']
        return [(b-a)%12 for a,b in zip(roots,roots[1:]+roots[:1])]
    if ident=='REF-0193':return circular_pc_distance(data['dm7_guide'],data['g7_guide'])
    low,high=(data[k] for k in (('min_note','max_note') if ident=='REF-0195' else ('min_vel','max_vel')))
    if type(low) is not int or type(high) is not int or not 0<=low<=high<=127:raise ValueError('Invalid 7-bit range')
    return high-low+1


def audit(cases):
    rows=[]
    for case in cases:
        ident=case['case_id'];status='EXISTING_EXECUTABLE_CLASS' if case['test_class']!='SPECIFICATION_EXAMPLE' else 'STRUCTURE_ONLY_CONTEXT_OR_IMPLEMENTATION_REQUIRED'
        observed=None
        if ident in SUPPORTED:
            observed=calculate(case);status='BOUNDED_CALCULATION_PASS' if observed==case['expected_output'] else 'BOUNDED_CALCULATION_FAIL'
        rows.append({'case_id':ident,'original_class':case['test_class'],'supplement_status':status,
                     'observed':json.dumps(observed,ensure_ascii=False),'source_locator':case['source_citation'],
                     'human_review':'AUSSTEHEND','limitation':'Arithmetic/register model only; source, musical context, hand assignment and pedagogical effectiveness are not thereby approved.'})
    return rows


def main():
    parser=argparse.ArgumentParser(description=__doc__);parser.add_argument('--csv-out',type=Path,required=True)
    args=parser.parse_args();cases=json.loads((ROOT/'knowledge/research/golden_cases/golden_reference_cases.json').read_text(encoding='utf-8'))
    rows=audit(cases)
    # Keep the original 14-case calculator distinct, but publish an up-to-date
    # inventory instead of continuing to call the remaining 64 unexamined.
    from scripts.audit_golden_remaining import audit as audit_remaining
    remaining={r['case_id']:r for r in audit_remaining(cases=cases)}
    for row in rows:
        if row['case_id'] in remaining:
            review=remaining[row['case_id']]
            row['supplement_status']='REVIEWED_64_'+review['model_status']
            row['observed']=review['observed']
            row['source_locator']=review['source_locator']
            row['limitation']=review['original_assessment']+': '+review['finding']+' Next: '+review['next_step']
    with args.csv_out.open('w',encoding='utf-8',newline='') as target:
        writer=csv.DictWriter(target,fieldnames=rows[0]);writer.writeheader();writer.writerows(rows)
    print('198 cases inventoried;',sum(r['supplement_status']=='BOUNDED_CALCULATION_PASS' for r in rows),
          'original supplements;',len(remaining),'individual reviews;',
          sum(r['model_status']=='PASS' for r in remaining.values()),'separate typed model passes; zero new expert approvals.')
    if (any(r['supplement_status']=='BOUNDED_CALCULATION_FAIL' for r in rows)
            or any(r['model_status']=='FAIL' for r in remaining.values())):raise SystemExit(1)


if __name__=='__main__':main()

"""REF-0030-bound PAT-001 onset extension; historical measurements stay unchanged."""
import argparse
import csv
from fractions import Fraction
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT))
from scripts.audit_relation_patterns import events, grid_match
from scripts.audit_rwc_joint import ARCHIVE_SHA, COMMIT, four_four_bars

OUTPUT = ROOT/'docs/audit/fable-5.2/PAT001_SYNKOPE_2026-11-15.json'
GOLDEN = ROOT/'knowledge/research/golden_cases/golden_reference_cases.json'


def anchor():
    records = json.loads(GOLDEN.read_text(encoding='utf8'))
    case = next(r for r in records if r['case_id']=='REF-0030')
    if (case['title']!='16tel-Synkope vor Schlag 4 (3e+)' or case['input_params']['ppq']!=480
            or case['expected_output']!='Tick 1320 bei 480 PPQ'):
        raise ValueError('Historical timing anchor changed; review before measuring')
    return {'path':GOLDEN.relative_to(ROOT).as_posix(),'case_id':'REF-0030',
            'case_sha256':sha256(json.dumps(case,ensure_ascii=False,sort_keys=True).encode()).hexdigest(),
            'ppq':480,'tick':1320,'zero_based_quarter_phase':str(Fraction(1320,480)),
            'scope':'Project timing definition only; linking it to PAT001 is a disclosed cross-reference, not human style acceptance.'}


def observe(bar, note_times, tolerance):
    kick = sorted(t for n in (35,36) for t in note_times.get(n, []))
    sync = grid_match(bar,kick,[2.75],tolerance)
    kick_grid = grid_match(bar,kick,[0,2,2.75],tolerance)
    snare = grid_match(bar,note_times.get(38,[]),[1,3],tolerance)
    hats = grid_match(bar,note_times.get(42,[]),[i/2 for i in range(8)],tolerance)
    return {'syncopation_subset':sync['subset'],'kick_grid_subset':kick_grid['subset'],
            'kick_same_note_grid':kick_grid['same_note_grid'],
            'joint_core_and_syncopation_subset':all(v['subset'] for v in (kick_grid,snare,hats))}


def measure(archive):
    raw=Path(archive).read_bytes()
    if sha256(raw).hexdigest()!=ARCHIVE_SHA: raise ValueError('Unexpected RWC source')
    z=zipfile.ZipFile(io.BytesIO(raw));prefix='rwc-annotations-'+COMMIT+'/01_annotations_preprocessed/'
    old=json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json').read_text(encoding='utf8'))
    rows=[]
    for row in old['records']:
        windows=row['patterns']['PROG-001']['exact']
        if not windows:continue
        ident=row['recording_id'];midi=z.read(prefix+'MIDI_aligned/RWC-P/'+ident+'.mid');beat_raw=z.read(prefix+'beats/RWC-P/'+ident+'.csv')
        if sha256(midi).hexdigest()!=row['member_sha256']['midi'] or sha256(beat_raw).hexdigest()!=row['member_sha256']['beats']:
            raise ValueError('Source member mismatch')
        bars=four_four_bars(list(csv.DictReader(io.StringIO(beat_raw.decode()),delimiter=';')))
        selected=[b for b in bars if any(w['start_seconds']<=b[0] and b[-1]<=w['end_seconds'] for w in windows)]
        notes=events(midi);counts={}
        for tolerance in (.04,.1):
            measurements=[observe(b,notes,tolerance) for b in selected]
            counts[str(tolerance)]={k:sum(v[k] for v in measurements) for k in measurements[0]} if measurements else {}
        rows.append({'recording_id':ident,'midi_sha256':sha256(midi).hexdigest(),'beat_sha256':sha256(beat_raw).hexdigest(),
                     'unique_complete_bars':len(selected),'tolerances_in_local_quarters':counts})
    return {'schema_version':1,'source_archive_sha256':ARCHIVE_SHA,'anchor':anchor(),
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'instrument_mapping_verified':False,
            'exact_pattern_verified':False,'method':'Half-open complete bars in union of strict PROG001 windows; channel9 positive note-ons; kick35/36, snare38, hat42; existing one-to-one matcher. Compare0.04 and0.1 local-quarter tolerances.',
            'limits':'0.04 separates ideal2.75 from ideal2+2/3;0.1 does not. This is sensitivity analysis, no measured error distribution or human approval. Timing anchor is project evidence, not authentic instrumentation,115BPM identity, style prevalence or independent performance acceptance.',
            'rows':rows}


def validate(d):
    if d['schema_version']!=1 or d['source_archive_sha256']!=ARCHIVE_SHA or d['anchor']!=anchor():raise ValueError('Timing provenance changed')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('historical_assertion_closed','instrument_mapping_verified','exact_pattern_verified')):
        raise ValueError('Premature musical acceptance')
    old=json.loads((ROOT/'docs/audit/fable-5.2/REL_PATTERN_KOMPONENTEN_2026-11-14.json').read_text(encoding='utf8'))
    joint=json.loads((ROOT/'docs/audit/fable-5.2/KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json').read_text(encoding='utf8'))
    beats={r['recording_id']:r['member_sha256']['beats'] for r in joint['records']}
    expected={r['record_id']:r for r in old['rows'] if r['relation_id']=='REL-001'}
    if len(d['rows'])!=len(expected) or {r['recording_id'] for r in d['rows']}!=set(expected):raise ValueError('Selection mismatch')
    for row in d['rows']:
        ref=expected[row['recording_id']];n=row['unique_complete_bars']
        if row['midi_sha256']!=ref['source_sha256'] or row['beat_sha256']!=beats[row['recording_id']] or type(n) is not int or n!=ref['observation']['unique_complete_bars_in_harmony_windows']:
            raise ValueError('Source or denominator mismatch')
        if set(row['tolerances_in_local_quarters'])!={'0.04','0.1'}:raise ValueError('Sensitivity scope changed')
        for counts in row['tolerances_in_local_quarters'].values():
            if set(counts)!={'syncopation_subset','kick_grid_subset','kick_same_note_grid','joint_core_and_syncopation_subset'} or any(type(v) is not int or not 0<=v<=n for v in counts.values()):
                raise ValueError('Invalid sensitivity counts')
            if counts['kick_same_note_grid']>counts['kick_grid_subset'] or counts['joint_core_and_syncopation_subset']>counts['kick_grid_subset'] or counts['kick_grid_subset']>counts['syncopation_subset']:
                raise ValueError('Invalid subset hierarchy')
        for key in ('syncopation_subset','kick_grid_subset','joint_core_and_syncopation_subset'):
            if row['tolerances_in_local_quarters']['0.04'][key]>row['tolerances_in_local_quarters']['0.1'][key]:raise ValueError('Nonmonotonic tolerance')


def main():
    p=argparse.ArgumentParser();p.add_argument('--rwc-archive');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.rwc_archive:p.error('Source archive required for writing')
    d=measure(a.rwc_archive) if a.rwc_archive else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Syncopation observation stale')
    print(json.dumps({'recordings':len(d['rows']),'bars':sum(r['unique_complete_bars'] for r in d['rows']),'historical_assertion_closed':False}))


if __name__=='__main__':main()

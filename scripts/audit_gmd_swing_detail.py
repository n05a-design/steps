"""Source-bound timing/velocity diagnostics; no acoustic dynamics or style approval."""
import argparse
from fractions import Fraction
from hashlib import sha256
import io
import json
import math
from pathlib import Path
from statistics import median
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_gmd_swing import OUTPUT as SOURCE,GMD_SHA,validate as validate_source

OUTPUT=ROOT/'docs/audit/fable-5.2/GMD_SWING_DETAIL_2026-11-15.json'


def interval(events,start,ppq,quarter,tolerance=.04):
    """Use unique actual quarter endpoints; next-bar endpoint is timing only."""
    if type(ppq) is not int or ppq<=0 or quarter not in (1,3) or not 0<=tolerance<.25:
        raise ValueError('Explicit beat2/4 context required')
    events=[(t,v) for t,v in events if v>0]
    a=start+quarter*ppq;b=a+ppq
    left=[t for t,_ in events if abs(t-a)<=tolerance*ppq]
    right=[t for t,_ in events if abs(t-b)<=tolerance*ppq]
    if not left or not right:return {'status':'MISSING_ENDPOINT'}
    if len(left)!=1 or len(right)!=1:return {'status':'AMBIGUOUS_ENDPOINT'}
    inside=[t for t,_ in events if left[0]<t<right[0]]
    if not inside:return {'status':'NO_INTERIOR'}
    if len(inside)!=1:return {'status':'AMBIGUOUS_INTERIOR'}
    long=inside[0]-left[0];short=right[0]-inside[0]
    return {'status':'MEASURED','first_interval_ticks':long,'second_interval_ticks':short,
            'ratio_fraction':str(Fraction(long,short)),'ratio':long/short}


def velocities(events,start,end):
    values=[v for t,v in events if start<=t<end and v>0]
    return {'positive_onsets':len(values),'min':min(values) if values else None,
            'max':max(values) if values else None,'median':median(values) if values else None}


def quarter_hits(events,start,ppq):
    bounded=[t for t,v in events if start<=t<start+4*ppq and v>0]
    return sum(any(abs(t-(start+q*ppq))<=.04*ppq for t in bounded) for q in range(4))


def measure(archive):
    import mido
    raw=Path(archive).read_bytes()
    if sha256(raw).hexdigest()!=GMD_SHA:raise ValueError('Unexpected source archive')
    z=zipfile.ZipFile(io.BytesIO(raw));source=json.loads(SOURCE.read_text(encoding='utf8'));validate_source(source)
    records=[]
    for r in source['records']:
        bar=r['first_joint_bow_pedal_bar_zero_based']['0.04']
        if bar is None:continue
        blob=z.read(r['member'])
        if sha256(blob).hexdigest()!=r['midi_sha256']:raise ValueError('MIDI source mismatch')
        m=mido.MidiFile(file=io.BytesIO(blob));tick=0;notes={}
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='note_on' and msg.velocity>0 and msg.channel==9:notes.setdefault(msg.note,[]).append((tick,msg.velocity))
        ppq=m.ticks_per_beat
        if ppq!=r['ppq']:raise ValueError('PPQ mismatch')
        start=bar*4*ppq;end=start+4*ppq
        records.append({'recording_id':r['recording_id'],'midi_sha256':r['midi_sha256'],'bar_zero_based':bar,'ppq':ppq,
                        'bpm_metadata':r['bpm_metadata'],'ride_bow_intervals':{str(q+1):interval(notes.get(51,[]),start,ppq,q) for q in (1,3)},
                        'literal35_quarter_hits':quarter_hits(notes.get(35,[]),start,ppq),'source36_quarter_hits':quarter_hits(notes.get(36,[]),start,ppq),
                        'velocity_diagnostics':{str(n):velocities(notes.get(n,[]),start,end) for n in (35,36,51,44)}})
    return {'schema_version':1,'archive_sha256':GMD_SHA,'candidate_scope':'First narrow literal51/44 candidate per selected Swing performance from prior source-bound receipt',
            'method':'Unique actual51 quarter endpoints within0.04 metronome quarters; one strictly intermediate51 onset. Beat4-to-next-downbeat endpoint may belong to next bar and is used only as interval endpoint. Velocity summaries use half-open current bar.',
            'publisher_mapping_url':'https://magenta.tensorflow.org/datasets/groove#drum-mapping',
            'mapping_scope':'Source36 Kick and51 Ride Bow per GMD publisher; source36 is not silently renamed to historical PAT012 literal35.',
            'limits':'Descriptive MIDI inter-onset ratios, no fixed Swing norm. MIDI velocity is not acoustic loudness or cross-instrument loudness calibration. Quiet feathering, complete PAT012,130BPM identity and harmony pairing unapproved.',
            'human_approval':'AUSSTEHEND','acoustic_loudness_verified':False,'pat012_feathering_verified':False,
            'harmonic_pairing_verified':False,'historical_assertion_closed':False,'records':records}


def validate(d):
    source=json.loads(SOURCE.read_text(encoding='utf8'));validate_source(source)
    expected={r['recording_id']:r for r in source['records'] if r['first_joint_bow_pedal_bar_zero_based']['0.04'] is not None}
    if d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or len(d['records'])!=len(expected) or {r['recording_id'] for r in d['records']}!=set(expected):raise ValueError('Candidate scope changed')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('acoustic_loudness_verified','pat012_feathering_verified','harmonic_pairing_verified','historical_assertion_closed')):raise ValueError('Premature approval')
    for r in d['records']:
        ref=expected[r['recording_id']]
        if any(type(r[k]) is not int for k in ('bar_zero_based','ppq','bpm_metadata')) or r['midi_sha256']!=ref['midi_sha256'] or r['bar_zero_based']!=ref['first_joint_bow_pedal_bar_zero_based']['0.04'] or r['ppq']!=ref['ppq'] or r['bpm_metadata']!=ref['bpm_metadata']:raise ValueError('Review-source identity mismatch')
        if set(r['ride_bow_intervals'])!={'2','4'} or set(r['velocity_diagnostics'])!={'35','36','51','44'}:raise ValueError('Incomplete diagnostic scope')
        for v in r['ride_bow_intervals'].values():
            if v['status'] not in {'MEASURED','NO_INTERIOR','MISSING_ENDPOINT','AMBIGUOUS_ENDPOINT','AMBIGUOUS_INTERIOR'}:raise ValueError('Unknown interval state')
            if v['status']=='MEASURED':
                a,b=v['first_interval_ticks'],v['second_interval_ticks']
                if type(a) is not int or type(b) is not int or min(a,b)<=0 or type(v['ratio']) not in (int,float) or not math.isfinite(v['ratio']) or v['ratio_fraction']!=str(Fraction(a,b)) or abs(v['ratio']-a/b)>1e-12:raise ValueError('Invalid measured ratio')
        for key in ('literal35_quarter_hits','source36_quarter_hits'):
            if type(r[key]) is not int or not 0<=r[key]<=4:raise ValueError('Invalid quarter count')
        for v in r['velocity_diagnostics'].values():
            if type(v['positive_onsets']) is not int or v['positive_onsets']<0:raise ValueError('Invalid onset count')
            if v['positive_onsets']==0:
                if any(v[k] is not None for k in ('min','max','median')):raise ValueError('Empty instrument has velocity')
            elif type(v['min']) is not int or type(v['max']) is not int or type(v['median']) not in (int,float) or not 1<=v['min']<=v['median']<=v['max']<=127:raise ValueError('Invalid MIDI velocity')


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmd-zip');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.gmd_zip:p.error('Source required for writing')
    d=measure(a.gmd_zip) if a.gmd_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Swing detail observation stale')
    print(json.dumps({'candidates':len(d['records']),'measured_intervals':sum(v['status']=='MEASURED' for r in d['records'] for v in r['ride_bow_intervals'].values()),'acoustic_loudness_verified':False}))


if __name__=='__main__':main()

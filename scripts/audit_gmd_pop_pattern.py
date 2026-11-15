"""PAT001 component/interpretation probes; no implicit historical pattern revision."""
import argparse
from collections import Counter
import csv
from hashlib import sha256
import io
import json
from pathlib import Path
import sys
import zipfile

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT))
from scripts.audit_graph_corpus import GMD_SHA,OBS,validate_observation
from scripts.audit_pattern_syncopation import anchor
from scripts.audit_relation_patterns import grid_match

OUTPUT=ROOT/'docs/audit/fable-5.2/GMD_POP_PATTERN_2026-11-15.json'


def components(bar,notes,tolerance):
    kick=notes.get(36,[])
    match=lambda ns,phases:grid_match(bar,ns,phases,tolerance)['subset']
    add=match(kick,[0,2,2.75])
    shift=match(kick,[0,2.75]) and not match(kick,[2])
    snare=match(notes.get(38,[]),[1,3])
    hat=match(notes.get(42,[]),[i/2 for i in range(8)])
    family=match(sorted(notes.get(42,[])+notes.get(22,[])),[i/2 for i in range(8)])
    return {'base_kick_1_3':match(kick,[0,2]),'additional_kick_grid':add,'shifted_kick_without_beat3':shift,
            'literal_snare38':snare,'literal_hat42':hat,'hat_family42_22':family,
            'additional_joint_literal':add and snare and hat,'additional_joint_hatfamily':add and snare and family,
            'shifted_joint_literal':shift and snare and hat,'shifted_joint_hatfamily':shift and snare and family}


def measure(archive):
    import mido
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=GMD_SHA:raise ValueError('GMD delivery mismatch')
    z=zipfile.ZipFile(io.BytesIO(payload));metadata_path=next(n for n in z.namelist() if n.endswith('/info.csv'));prefix=metadata_path[:-len('info.csv')]
    rows=list(csv.DictReader(io.StringIO(z.read(metadata_path).decode('utf8'))))
    selected=[r for r in rows if r['style'].split('/')[0]=='pop' and r['beat_type']=='beat' and r['time_signature']=='4-4'];records=[]
    for row in selected:
        raw=z.read(prefix+row['midi_filename']);m=mido.MidiFile(file=io.BytesIO(raw));tick=0;notes={};meters=[]
        if m.type not in (0,1) or m.ticks_per_beat<=0:raise ValueError('Metrical MIDI required')
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='time_signature':meters.append((msg.numerator,msg.denominator))
            if msg.type=='note_on' and msg.velocity>0:
                if msg.channel!=9:raise ValueError('Unexpected source channel')
                notes.setdefault(msg.note,[]).append(tick)
        if not meters or set(meters)!={(4,4)}:raise ValueError('Metadata/meter mismatch')
        bars=tick//(4*m.ticks_per_beat);counts={}
        for t in (.04,.1):
            c=Counter()
            for b in range(bars):c.update({k:int(v) for k,v in components([(b*4+q)*m.ticks_per_beat for q in range(5)],notes,t).items()})
            counts[str(t)]=dict(c)
        records.append({'recording_id':row['id'],'member':prefix+row['midi_filename'],'midi_sha256':sha256(raw).hexdigest(),
                        'drummer':row['drummer'],'style':row['style'],'bpm_metadata':int(row['bpm']),
                        'ppq':m.ticks_per_beat,'complete_bars':bars,'counts':counts})
    return {'schema_version':1,'archive_sha256':GMD_SHA,'anchor':anchor(),
            'source_mapping_url':'https://magenta.tensorflow.org/datasets/groove#drum-mapping',
            'mapping_scope':'GMD publisher36 Kick,38 Snare Head,42 Closed Hat Bow,22 Closed Hat Edge; no transfer to RWC/JazzSAMBA.',
            'interpretations':'Proposals only: additional requires0,2,2.75; shifted requires0,2.75 and absence of2. Hat42 literal versus source22/42 family remain separate. Neither interpretation approved as historical PAT001 identity.',
            'method':'All primary-style pop, beat,4-4 source records, tick-zero metronome bars; positive channel9 onsets, half-open complete bars, one-to-one0.04/0.1-quarter tolerance; extra events allowed unless explicitly forbidden.',
            'rights':'Google LLC, GMDv1.0.0, CC BY4.0; Gillick et al.2019. Original MIDI/audio stay local.',
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'exact_pat001_verified':False,'harmonic_pairing_verified':False,'population_generalization':False,
            'summary':{t:{k:sum(r['counts'][t][k] for r in records) for k in records[0]['counts'][t]} for t in ('0.04','0.1')},'records':records}


def validate(d):
    old=json.loads(OBS.read_text(encoding='utf8'));validate_observation(old);expected={r['recording_id']:r for r in old['recordings']}
    if d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or d['anchor']!=anchor() or len(d['records'])!=len(expected) or {r['recording_id'] for r in d['records']}!=set(expected):raise ValueError('Source selection/anchor mismatch')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('historical_assertion_closed','exact_pat001_verified','harmonic_pairing_verified','population_generalization')):raise ValueError('Premature approval')
    keys=set(components([0,1,2,3,4],{},.04))
    for r in d['records']:
        ref=expected[r['recording_id']]
        if r['midi_sha256']!=ref['sha256'] or r['member']!=ref['member'] or r['style']!=ref['style'] or r['drummer']!=ref['drummer'] or r['bpm_metadata']!=ref['bpm'] or r['ppq']!=ref['ppq'] or type(r['complete_bars']) is not int or r['complete_bars']!=ref['complete_bars']:raise ValueError('Changed source identity or denominator')
        for t in ('0.04','0.1'):
            c=r['counts'][t]
            if set(c)!=keys or any(type(v) is not int or not 0<=v<=r['complete_bars'] for v in c.values()):raise ValueError('Invalid component counts')
            if c['literal_hat42']>c['hat_family42_22'] or c['additional_kick_grid']>c['base_kick_1_3']:raise ValueError('Invalid subset hierarchy')
            for mode,kick in [('additional','additional_kick_grid'),('shifted','shifted_kick_without_beat3')]:
                if c[mode+'_joint_literal']>min(c[kick],c['literal_snare38'],c['literal_hat42'],c[mode+'_joint_hatfamily']) or c[mode+'_joint_hatfamily']>min(c[kick],c['literal_snare38'],c['hat_family42_22']):raise ValueError('Invalid joint hierarchy')
        # Shift includes a forbidden event; it is deliberately NOT monotonic in tolerance.
        for key in ('base_kick_1_3','additional_kick_grid','literal_snare38','literal_hat42','hat_family42_22','additional_joint_literal','additional_joint_hatfamily'):
            if r['counts']['0.04'][key]>r['counts']['0.1'][key]:raise ValueError('Nonmonotonic positive-only pattern')
    for t in ('0.04','0.1'):
        if d['summary'][t]!={k:sum(r['counts'][t][k] for r in d['records']) for k in keys}:raise ValueError('Aggregate mismatch')


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmd-zip');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.gmd_zip:p.error('Original source required for writing')
    d=measure(a.gmd_zip) if a.gmd_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Pop pattern observation stale')
    print(json.dumps({'recordings':len(d['records']),'bars':sum(r['complete_bars'] for r in d['records']),'summary':d['summary'],'historical_assertion_closed':False}))


if __name__=='__main__':main()

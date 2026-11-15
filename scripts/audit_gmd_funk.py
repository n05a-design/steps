"""Source-bound Funk component probes; velocities and timing are not musical approval."""
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
from scripts.audit_graph_corpus import GMD_SHA
from scripts.audit_relation_patterns import grid_match

OUTPUT=ROOT/'docs/audit/fable-5.2/GMD_FUNK_PATTERN_2026-11-15.json'
SELECTION_SHA='2d2f860de8fb4d5e240a9751100a9131ff8873b6d185b746d281d92a494be418'


def selection_digest(records):
    fields=('recording_id','member','midi_sha256','drummer','style','bpm_metadata','ppq','complete_bars')
    return sha256(json.dumps(sorted([{k:r[k] for k in fields} for r in records],key=lambda r:r['recording_id']),sort_keys=True).encode()).hexdigest()


def components(bar,events,tolerance):
    """Events are positive (tick,note,velocity); extra hits allowed in subset grids."""
    notes={}
    for tick,note,velocity in events:
        if velocity>0:notes.setdefault(note,[]).append(tick)
    notes={n:sorted(ts) for n,ts in notes.items()}
    match=lambda pitches,phases:grid_match(bar,sorted(t for n in pitches for t in notes.get(n,[])),phases,tolerance)['subset']
    width=bar[1]-bar[0]
    inside=[(t,n,v) for t,n,v in events if v>0 and bar[0]<=t<bar[-1]]
    kicks=[(t,v) for t,n,v in inside if n==36]
    downbeat=[v for t,v in kicks if abs(t-bar[0])<=tolerance*width+1e-9]
    ghost=any(n==38 and 25<=v<=45 and all(abs(t-bar[q])>tolerance*width+1e-9 for q in (1,3)) for t,n,v in inside)
    c={'kick36_downbeat':match([36],[0]),'snare38_backbeat':match([38],[1,3]),
       'hat42_sixteenths':match([42],[i/4 for i in range(16)]),
       'hat42_22_sixteenths':match([42,22],[i/4 for i in range(16)]),
       'pat013_kick_grid':match([36],[0,.75,2.5,3.25]),
       'snare38_velocity25_45_off_backbeat':ghost,
       'downbeat_kick_at_bar_max_velocity':bool(downbeat) and max(downbeat)==max(v for _,v in kicks),
       'exact_tick_multi_pitch_collision':any(len({n for t,n,v in inside if t==tick})>1 for tick,_,_ in inside)}
    c['pat007_component_joint']=c['kick36_downbeat'] and c['snare38_backbeat'] and c['hat42_22_sixteenths'] and ghost
    c['pat013_component_joint']=c['pat013_kick_grid'] and c['snare38_backbeat'] and c['hat42_22_sixteenths']
    return c


def measure(archive):
    import mido
    payload=Path(archive).read_bytes()
    if sha256(payload).hexdigest()!=GMD_SHA:raise ValueError('Source delivery mismatch')
    z=zipfile.ZipFile(io.BytesIO(payload));info=next(n for n in z.namelist() if n.endswith('/info.csv'));prefix=info[:-len('info.csv')]
    selected=[r for r in csv.DictReader(io.StringIO(z.read(info).decode())) if r['style'].split('/')[0]=='funk' and r['beat_type']=='beat' and r['time_signature']=='4-4']
    records=[]
    for r in selected:
        raw=z.read(prefix+r['midi_filename']);m=mido.MidiFile(file=io.BytesIO(raw));tick=0;events=[];meters=[]
        if m.type not in (0,1) or m.ticks_per_beat<=0:raise ValueError('Metrical MIDI required')
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='time_signature':meters.append((msg.numerator,msg.denominator))
            if msg.type=='note_on' and msg.velocity>0:
                if msg.channel!=9:raise ValueError('Unexpected channel')
                events.append((tick,msg.note,msg.velocity))
        if not meters or set(meters)!={(4,4)}:raise ValueError('Source meter mismatch')
        bars=tick//(4*m.ticks_per_beat);counts={}
        for tolerance in (.04,.1):
            c=Counter()
            for b in range(bars):
                bar=[(b*4+q)*m.ticks_per_beat for q in range(5)]
                c.update({k:int(v) for k,v in components(bar,events,tolerance).items()})
            counts[str(tolerance)]=dict(c)
        records.append({'recording_id':r['id'],'member':prefix+r['midi_filename'],'midi_sha256':sha256(raw).hexdigest(),
                        'drummer':r['drummer'],'style':r['style'],'bpm_metadata':int(r['bpm']),
                        'ppq':m.ticks_per_beat,'complete_bars':bars,'counts':counts})
    return {'schema_version':1,'archive_sha256':GMD_SHA,'metadata_sha256':sha256(z.read(info)).hexdigest(),
            'selection':'primary style funk; beat;4-4; all substyles retained including shuffle; no straight subdivision inferred from genre',
            'method':'tick-zero complete half-open bars; positive channel9 events; one-to-one subset grids at0.04/0.1 quarter tolerance',
            'mapping_url':'https://magenta.tensorflow.org/datasets/groove#drum-mapping',
            'mapping_scope':'GMD publisher only:36 Kick,38 Snare Head,42 Closed Hat Bow,22 Closed Hat Edge',
            'limits':'25-45 is project MIDI velocity, not acoustic ghost-note approval. At least one off-backbeat hit is not density. Within-kick maximum may tie and is not The One accent. Exact tick collision can refute strict simultaneity-free MIDI at that tick; absence cannot prove musical linearity. Open-hat release undefined, untested. No harmonic annotations or representative song sample.',
            'rights':'Google LLC GMDv1.0.0 CC BY4.0; Gillick et al.2019; raw MIDI stays local',
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'harmonic_pairing_verified':False,
            'exact_pattern_verified':False,'population_generalization':False,
            'summary':{t:{k:sum(r['counts'][t][k] for r in records) for k in records[0]['counts'][t]} for t in ('0.04','0.1')},'records':records}


def validate(d):
    if d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or d['metadata_sha256']!='3e17eef2f18012c0160c183ad5b106964eb429876cceb1eee1b746def4e6b11b' or len(d['records'])!=53 or selection_digest(d['records'])!=SELECTION_SHA:raise ValueError('Changed source selection/identity/denominators')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('historical_assertion_closed','harmonic_pairing_verified','exact_pattern_verified','population_generalization')):raise ValueError('Premature approval')
    keys=set(components([0,1,2,3,4],[],.04))
    if len({r['recording_id'] for r in d['records']})!=53:raise ValueError('Duplicate source identity')
    for r in d['records']:
        if type(r['complete_bars']) is not int or r['complete_bars']<=0:raise ValueError('Invalid denominator')
        for t in ('0.04','0.1'):
            c=r['counts'][t]
            if set(c)!=keys or any(type(v)is not int or not 0<=v<=r['complete_bars'] for v in c.values()):raise ValueError('Invalid count')
            if c['hat42_sixteenths']>c['hat42_22_sixteenths'] or c['downbeat_kick_at_bar_max_velocity']>c['kick36_downbeat']:raise ValueError('Invalid subset')
            for joint,required in [('pat007_component_joint',['kick36_downbeat','snare38_backbeat','hat42_22_sixteenths','snare38_velocity25_45_off_backbeat']),('pat013_component_joint',['pat013_kick_grid','snare38_backbeat','hat42_22_sixteenths'])]:
                if c[joint]>min(c[k] for k in required):raise ValueError('Invalid joint')
        # Off-backbeat excludes events: increasing tolerance need not preserve ghost/joint counts.
        for key in ('kick36_downbeat','snare38_backbeat','hat42_sixteenths','hat42_22_sixteenths','pat013_kick_grid','pat013_component_joint','downbeat_kick_at_bar_max_velocity'):
            if r['counts']['0.04'][key]>r['counts']['0.1'][key]:raise ValueError('Nonmonotonic positive grid')
    for t in ('0.04','0.1'):
        if d['summary'][t]!={k:sum(r['counts'][t][k] for r in d['records']) for k in keys}:raise ValueError('Aggregate mismatch')


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmd-zip');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.gmd_zip:p.error('Original source required')
    d=measure(a.gmd_zip) if a.gmd_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Stale Funk observation')
    print(json.dumps({'recordings':len(d['records']),'bars':sum(r['complete_bars'] for r in d['records']),'summary':d['summary']}))


if __name__=='__main__':main()

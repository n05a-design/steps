"""Explicit label coverage for all14 corpus cases and bounded Soul proxy probes."""
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
from scripts.audit_graph_corpus import GMD_SHA,PLAN
from scripts.audit_relation_patterns import grid_match

OUTPUT=ROOT/'docs/audit/fable-5.2/GMD_KORPUS_ABDECKUNG_2026-11-15.json'
MATRIX=ROOT/'docs/audit/fable-5.2/GMD_KORPUS_ABDECKUNG_2026-11-15.csv'
METADATA_SHA='3e17eef2f18012c0160c183ad5b106964eb429876cceb1eee1b746def4e6b11b'
INVENTORY_SHA='ff0f4c8d6d44bd17bc4dc6ea02444857cc312d7959eb204d7870043dc870d438'
SOUL_SHA='49c7f7f006776ae0e470e94cc85838a6df2b75f4713b7ad7c9fa257b304d2ebd'
SELECTORS={
    'CR-029':('primary','pop'),'CR-030':('primary','house'),
    'CR-031':('primary','pop'),'CR-032':('primary','house'),
    'REL-001':('primary','pop'),'REL-005':('exact','jazz/swing'),
    'REL-006':('primary','funk'),'REL-007':('primary','funk'),
    'REL-014':('primary','dnb'),'REL-015':('primary','ukg'),
    'REL-017':('exact','dnb/jumpup'),'REL-026':('primary','dnb'),
    'REL-032':('exact','afrocuban/chacha'),'REL-035':('exact','soul/neosoul')}


def select(rows,mode,value):
    if mode not in ('primary','exact'):raise ValueError('Explicit selector required')
    return [r for r in rows if r['beat_type']=='beat' and r['time_signature']=='4-4'
            and (r['style'].split('/')[0] if mode=='primary' else r['style'])==value]


def digest(value):return sha256(json.dumps(value,sort_keys=True).encode()).hexdigest()


def source_digest(records):
    keys=('recording_id','member','midi_sha256','drummer','style','bpm_metadata','ppq','complete_bars')
    return digest(sorted([{k:r[k] for k in keys} for r in records],key=lambda r:r['recording_id']))


def components(bar,notes,tolerance):
    match=lambda ns,phases:grid_match(bar,sorted(t for n in ns for t in notes.get(n,[])),phases,tolerance)['subset']
    kick=match([36],[0,2.5]);snare=match([38],[2])
    c={'kick36_1_and_3plus':kick,'snare38_beat3':snare,
       'snare38_proposed_drag_anchor_2plus':match([38],[1.5]),
       'kick_snare_literal_joint':kick and snare,
       'closed_hat_and_pedal_copresent':any(bar[0]<=t<bar[-1] for n in (42,22) for t in notes.get(n,[])) and any(bar[0]<=t<bar[-1] for t in notes.get(44,[]))}
    c['joint_with_proposed_drag_anchor']=c['kick_snare_literal_joint'] and c['snare38_proposed_drag_anchor_2plus']
    return c


def measure(archive):
    import mido
    raw=Path(archive).read_bytes()
    if sha256(raw).hexdigest()!=GMD_SHA:raise ValueError('Unexpected GMD delivery')
    z=zipfile.ZipFile(io.BytesIO(raw));info=next(n for n in z.namelist() if n.endswith('/info.csv'));prefix=info[:-8]
    metadata=z.read(info)
    if sha256(metadata).hexdigest()!=METADATA_SHA:raise ValueError('Changed metadata')
    rows=list(csv.DictReader(io.StringIO(metadata.decode('utf8'))));plan=json.loads(PLAN.read_text(encoding='utf8'));by={r['relation_id']:r for r in plan['cases']}
    frames=[]
    for ident,(mode,value) in SELECTORS.items():
        selected=select(rows,mode,value)
        frames.append({'relation_id':ident,'original_row_sha256':by[ident]['original_row_sha256'],
                       'selector_mode':mode,'selector_value':value,'source_ids':sorted(r['id'] for r in selected),
                       'label_scope':'EXPLICIT_LABEL_COMPONENT_ONLY' if selected else 'NO_MATCHING_EXPLICIT_LABEL_IN_THIS_DELIVERY',
                       'relation_status':'OPEN','human_approval':'AUSSTEHEND'})
    records=[]
    for row in select(rows,'primary','soul'):
        payload=z.read(prefix+row['midi_filename']);m=mido.MidiFile(file=io.BytesIO(payload));tick=0;notes={};meters=[]
        if m.type not in (0,1) or m.ticks_per_beat<=0:raise ValueError('Metrical MIDI required')
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='time_signature':meters.append((msg.numerator,msg.denominator))
            if msg.type=='note_on' and msg.velocity>0:
                if msg.channel!=9:raise ValueError('Unexpected channel')
                notes.setdefault(msg.note,[]).append(tick)
        if not meters or set(meters)!={(4,4)}:raise ValueError('Meter mismatch')
        bars=tick//(4*m.ticks_per_beat);counts={}
        for tolerance in (.04,.1):
            c=Counter()
            for b in range(bars):c.update({k:int(v) for k,v in components([(b*4+q)*m.ticks_per_beat for q in range(5)],notes,tolerance).items()})
            counts[str(tolerance)]=dict(c)
        records.append({'recording_id':row['id'],'member':prefix+row['midi_filename'],'midi_sha256':sha256(payload).hexdigest(),
                        'drummer':row['drummer'],'style':row['style'],'bpm_metadata':int(row['bpm']),'ppq':m.ticks_per_beat,'complete_bars':bars,'counts':counts})
    return {'schema_version':1,'archive_sha256':GMD_SHA,'metadata_sha256':METADATA_SHA,
            'metadata_rows':len(rows),'style_counts':dict(sorted(Counter(r['style'] for r in rows).items())),
            'frames':frames,'proxy_selection':'primary soul; beat;4-4, all substyles including motown retained; NOT verified Neo-Soul',
            'proxy_for_relation':'REL-035','records':records,
            'summary':{t:{k:sum(r['counts'][t][k] for r in records) for k in records[0]['counts'][t]} for t in ('0.04','0.1')},
            'mapping_url':'https://magenta.tensorflow.org/datasets/groove#drum-mapping',
            'method':'Positive channel9 hits, tick-zero half-open complete bars, one-to-one0.04/0.1-quarter subset grids. Drag anchor is a proposal for an onset, not a measured drag. Closed/pedal co-presence is not ordered alternation.',
            'limits':'Label absence is not absence of musical practice. Neworleans/chacha is not automatically Afro-Cuban chacha; dance/breakbeat not DnB, soul not Neo-Soul. GMD has no aligned performed chords/bass/cadence labels/representative song sampling. Native source map has no clap/conga/guiro classes; no GM substitution.57percent/Tick137 interpretation, Phrygian harmony, acoustic depth and exactPAT030 not verified.',
            'rights':'Google LLC GMDv1.0.0 CC BY4.0; Gillick et al.2019; raw MIDI remains local',
            'human_approval':'AUSSTEHEND','historical_assertion_closed':False,'exact_pattern_verified':False,'harmonic_pairing_verified':False,'population_generalization':False}


def validate(d):
    if d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or d['metadata_sha256']!=METADATA_SHA or d['metadata_rows']!=1150:raise ValueError('Changed delivery')
    if digest({'style_counts':d['style_counts'],'frames':d['frames']})!=INVENTORY_SHA:raise ValueError('Changed metadata selection or original identity')
    if len(d['records'])!=28 or source_digest(d['records'])!=SOUL_SHA:raise ValueError('Changed proxy identity or denominators')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('historical_assertion_closed','exact_pattern_verified','harmonic_pairing_verified','population_generalization')):raise ValueError('Premature approval')
    keys=set(components([0,1,2,3,4],{},.04));cases={r['relation_id']:r for r in json.loads(PLAN.read_text(encoding='utf8'))['cases']}
    for f in d['frames']:
        if f['original_row_sha256']!=cases[f['relation_id']]['original_row_sha256'] or f['relation_status']!='OPEN' or f['human_approval']!='AUSSTEHEND':raise ValueError('Changed historical frame')
    for r in d['records']:
        if type(r['complete_bars'])is not int or r['complete_bars']<=0:raise ValueError('Invalid denominator')
        for t in ('0.04','0.1'):
            c=r['counts'][t]
            if set(c)!=keys or any(type(v)is not int or not 0<=v<=r['complete_bars'] for v in c.values()):raise ValueError('Invalid component count')
            if c['kick_snare_literal_joint']>min(c['kick36_1_and_3plus'],c['snare38_beat3']) or c['joint_with_proposed_drag_anchor']>min(c['kick_snare_literal_joint'],c['snare38_proposed_drag_anchor_2plus']):raise ValueError('Invalid subset')
        if any(r['counts']['0.04'][k]>r['counts']['0.1'][k] for k in keys):raise ValueError('Nonmonotonic subset')
    for t in ('0.04','0.1'):
        if d['summary'][t]!={k:sum(r['counts'][t][k] for r in d['records']) for k in keys}:raise ValueError('Aggregate mismatch')


def render(d):
    out=io.StringIO(newline='');w=csv.writer(out,lineterminator='\n');w.writerow(['relation_id','selector_mode','selector_value','beat_4_4_recordings','label_scope','relation_status','human_approval'])
    for f in d['frames']:w.writerow([f['relation_id'],f['selector_mode'],f['selector_value'],len(f['source_ids']),f['label_scope'],f['relation_status'],f['human_approval']])
    return out.getvalue()


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmd-zip');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.gmd_zip:p.error('Original delivery required')
    d=measure(a.gmd_zip) if a.gmd_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8');MATRIX.write_text(render(d),encoding='utf8')
    if a.check and (d!=json.loads(OUTPUT.read_text(encoding='utf8')) or render(d)!=MATRIX.read_text(encoding='utf8')):raise SystemExit('Stale coverage observation/matrix')
    print(json.dumps({'frames':len(d['frames']),'proxy_recordings':len(d['records']),'bars':sum(r['complete_bars'] for r in d['records']),'summary':d['summary']}))


if __name__=='__main__':main()

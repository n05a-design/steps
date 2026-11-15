"""Publisher-mapped Swing drum components; never infer harmonic pairing or approval."""
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

OUTPUT=ROOT/'docs/audit/fable-5.2/GMD_SWING_PATTERN_2026-11-15.json'
REVIEW=ROOT/'docs/audit/fable-5.2/GMD_SWING_PRUEFSTELLEN_2026-11-15.csv'
METADATA_SHA='3e17eef2f18012c0160c183ad5b106964eb429876cceb1eee1b746def4e6b11b'
SELECTION_SHA='d4d1fd45a2c04cc192e3d032b25d66638ac9e0101226a9eb37358189e32dbc81'


def selection_digest(records):
    keys=('recording_id','member','midi_sha256','drummer','session','split','style','bpm_metadata','ppq','complete_bars')
    selected=[{k:r[k] for k in keys} for r in sorted(records,key=lambda r:r['recording_id'])]
    return sha256(json.dumps(selected,ensure_ascii=False,sort_keys=True).encode()).hexdigest()


def components(bar,notes,tolerance):
    literal=grid_match(bar,notes.get(51,[]),[0,1,2,3],tolerance)['subset']
    family=grid_match(bar,sorted(t for n in (51,53,59) for t in notes.get(n,[])),[0,1,2,3],tolerance)['subset']
    pedal=grid_match(bar,notes.get(44,[]),[1,3],tolerance)['subset']
    return {'ride_bow_quarters':literal,'ride_family_quarters':family,'pedal_2_4':pedal,
            'joint_bow_pedal':literal and pedal,'joint_family_pedal':family and pedal}


def measure(archive):
    import mido
    raw=Path(archive).read_bytes()
    if sha256(raw).hexdigest()!=GMD_SHA:raise ValueError('Unexpected GMD archive')
    z=zipfile.ZipFile(io.BytesIO(raw));metadata_path=next(n for n in z.namelist() if n.endswith('/info.csv'));prefix=metadata_path[:-len('info.csv')]
    metadata_raw=z.read(metadata_path);metadata=list(csv.DictReader(io.StringIO(metadata_raw.decode('utf8'))))
    selected=[r for r in metadata if r['style']=='jazz/swing' and r['beat_type']=='beat' and r['time_signature']=='4-4']
    records=[]
    for row in selected:
        blob=z.read(prefix+row['midi_filename']);m=mido.MidiFile(file=io.BytesIO(blob))
        if m.type not in (0,1) or m.ticks_per_beat<=0:raise ValueError('Metrical MIDI required')
        tick=0;notes={};meters=[];tempos=[]
        for msg in mido.merge_tracks(m.tracks):
            tick+=msg.time
            if msg.type=='time_signature':meters.append((msg.numerator,msg.denominator))
            if msg.type=='set_tempo':tempos.append(msg.tempo)
            if msg.type=='note_on' and msg.velocity>0:
                if msg.channel!=9:raise ValueError('Unexpected note channel')
                notes.setdefault(msg.note,[]).append(tick)
        if not meters or set(meters)!={(4,4)}:raise ValueError('Metadata/meter mismatch')
        bars=tick//(4*m.ticks_per_beat);counts={};candidates={}
        for tolerance in (.04,.1):
            count=Counter();first=None
            for index in range(bars):
                bar=[(index*4+q)*m.ticks_per_beat for q in range(5)];result=components(bar,notes,tolerance)
                count.update({k:int(v) for k,v in result.items()})
                if first is None and result['joint_bow_pedal']:first=index
            counts[str(tolerance)]=dict(count);candidates[str(tolerance)]=first
        records.append({'recording_id':row['id'],'member':prefix+row['midi_filename'],'midi_sha256':sha256(blob).hexdigest(),
                        'drummer':row['drummer'],'session':row['session'],'split':row['split'],'style':row['style'],
                        'bpm_metadata':int(row['bpm']),'ppq':m.ticks_per_beat,'midi_tempos_microseconds':sorted(set(tempos)),
                        'complete_bars':bars,'positive_note_histogram':{str(k):len(v) for k,v in sorted(notes.items())},
                        'counts':counts,'first_joint_bow_pedal_bar_zero_based':candidates})
    summary={t:{k:sum(r['counts'][t][k] for r in records) for k in records[0]['counts'][t]} for t in ('0.04','0.1')}
    return {'schema_version':1,'archive_sha256':GMD_SHA,'metadata_sha256':sha256(metadata_raw).hexdigest(),
            'selection':'style exactly jazz/swing; beat_type beat; time_signature4-4',
            'source_mapping_scope':'PUBLISHER_DECLARED_GMD_TD11_TABLE_ONLY',
            'source_mapping_url':'https://magenta.tensorflow.org/datasets/groove#drum-mapping',
            'source_mapping':{'51':'Ride Bow','53':'Ride Bell','59':'Ride Edge','44':'HH Pedal'},
            'source_mapping_limits':'Publisher declaration verified against its table; not independent listening or a mapping for RWC/JazzSAMBA. Family51/53/59 remains separate from literal PAT012 note51.',
            'source_mapping_documented':True,'exact_pat012_verified':False,'harmonic_pairing_verified':False,
            'population_generalization':False,'historical_assertion_closed':False,'human_approval':'AUSSTEHEND',
            'rights':'Google LLC, GMDv1.0.0, CC BY4.0; Gillick et al.2019. Raw MIDI/audio remain local; no CSS or security approval.',
            'method':'Tick-zero metronome4/4 grid; positive channel9 note-ons; half-open complete bars before SMF end; one-to-one ±0.04/0.1 quarter. Ride quarter/pedal subsets permit extras; not complete swung/feathering130BPM pattern.',
            'denominator':'Commissioned drum performances, not independent songs; no chord annotations; all splits inspected for audit, not evaluation claims.',
            'selected_recordings':len(records),'selected_drummers':len({r['drummer'] for r in records}),
            'complete_bars':sum(r['complete_bars'] for r in records),'summary':summary,'records':records}


def validate(d):
    if d['schema_version']!=1 or d['archive_sha256']!=GMD_SHA or d['metadata_sha256']!=METADATA_SHA or d['selected_recordings']!=11 or len(d['records'])!=11 or selection_digest(d['records'])!=SELECTION_SHA:
        raise ValueError('Source or selection scope changed')
    if d['human_approval']!='AUSSTEHEND' or any(d[k] is not False for k in ('exact_pat012_verified','harmonic_pairing_verified','population_generalization','historical_assertion_closed')):
        raise ValueError('Premature acceptance')
    if d['source_mapping_scope']!='PUBLISHER_DECLARED_GMD_TD11_TABLE_ONLY' or d['source_mapping_documented'] is not True or d['source_mapping']!={'51':'Ride Bow','53':'Ride Bell','59':'Ride Edge','44':'HH Pedal'}:raise ValueError('Mapping scope changed')
    if len({r['recording_id'] for r in d['records']})!=11 or d['selected_drummers']!=len({r['drummer'] for r in d['records']}) or d['complete_bars']!=sum(r['complete_bars'] for r in d['records']):raise ValueError('Denominator mismatch')
    keys={'ride_bow_quarters','ride_family_quarters','pedal_2_4','joint_bow_pedal','joint_family_pedal'}
    for r in d['records']:
        if r['style']!='jazz/swing' or type(r['complete_bars']) is not int or r['complete_bars']<=0:raise ValueError('Invalid selected performance')
        for t in ('0.04','0.1'):
            c=r['counts'][t]
            if set(c)!=keys or any(type(v) is not int or not 0<=v<=r['complete_bars'] for v in c.values()):raise ValueError('Invalid component counts')
            if c['ride_bow_quarters']>c['ride_family_quarters'] or c['joint_bow_pedal']>min(c['ride_bow_quarters'],c['pedal_2_4'],c['joint_family_pedal']) or c['joint_family_pedal']>min(c['ride_family_quarters'],c['pedal_2_4']):raise ValueError('Invalid literal/family hierarchy')
            candidate=r['first_joint_bow_pedal_bar_zero_based'][t]
            if (c['joint_bow_pedal']==0)!=(candidate is None) or (candidate is not None and (type(candidate) is not int or not 0<=candidate<r['complete_bars'])):raise ValueError('Invalid review candidate')
        if any(r['counts']['0.04'][k]>r['counts']['0.1'][k] for k in keys):raise ValueError('Nonmonotonic tolerance')
    for t in ('0.04','0.1'):
        if d['summary'][t]!={k:sum(r['counts'][t][k] for r in d['records']) for k in keys}:raise ValueError('Aggregate mismatch')


def review_candidates(d):
    fields=['recording_id','member','midi_sha256','bar_zero_based','start_tick','end_tick','ppq','bpm_metadata','scope','human_approval']
    out=io.StringIO(newline='');writer=csv.DictWriter(out,fieldnames=fields,lineterminator='\n');writer.writeheader()
    for r in d['records']:
        bar=r['first_joint_bow_pedal_bar_zero_based']['0.04']
        if bar is not None:
            writer.writerow({'recording_id':r['recording_id'],'member':r['member'],'midi_sha256':r['midi_sha256'],
                             'bar_zero_based':bar,'start_tick':bar*4*r['ppq'],'end_tick':(bar+1)*4*r['ppq'],
                             'ppq':r['ppq'],'bpm_metadata':r['bpm_metadata'],
                             'scope':'First narrow literal51/44 component candidate per performance; no harmony or fullPAT012 approval',
                             'human_approval':'AUSSTEHEND'})
    return out.getvalue()


def main():
    p=argparse.ArgumentParser();p.add_argument('--gmd-zip');p.add_argument('--write',action='store_true');p.add_argument('--check',action='store_true');a=p.parse_args()
    if a.write and not a.gmd_zip:p.error('Source required for writing')
    d=measure(a.gmd_zip) if a.gmd_zip else json.loads(OUTPUT.read_text(encoding='utf8'));validate(d)
    if a.write:
        OUTPUT.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf8')
        REVIEW.write_text(review_candidates(d),encoding='utf8')
    if a.check and d!=json.loads(OUTPUT.read_text(encoding='utf8')):raise SystemExit('Swing observation stale')
    if a.check and review_candidates(d)!=REVIEW.read_text(encoding='utf8'):raise SystemExit('Review candidate locations stale')
    print(json.dumps({'recordings':d['selected_recordings'],'drummers':d['selected_drummers'],'bars':d['complete_bars'],'summary':d['summary'],'harmonic_pairing_verified':False}))


if __name__=='__main__':main()

#!/usr/bin/env python3
"""Technical validation of original V5.3 drum studies; no audio/music review."""
import json, math, hashlib, csv
from pathlib import Path
from collections import Counter, defaultdict
import mido, jsonschema
ROOT=Path(__file__).resolve().parent.parent
STUDIES=ROOT/'05_DRUMS_RHYTHM_GROOVE'/'Eigene_MIDI_Studien'
SCHEMA=ROOT/'14_DATENMODELLE'/'STEPS_SCHEMA__DrumPattern-Metadaten-Vertrag__SCHEMA__V5_3.json'

def check_all():
    schema=json.loads(SCHEMA.read_text());checks=0;errors=[];ids=set()
    for p in sorted(STUDIES.glob('*__NOTEN_DATEN__V5_3.json')):
        d=json.loads(p.read_text());jsonschema.validate(d,schema);checks+=1
        if d['id'] in ids: errors.append('duplicate id '+d['id'])
        ids.add(d['id']);checks+=1
        nn,dd=d['meter'];expected=d['ppq']*4*nn//dd
        if expected!=d['ticks_per_bar']:errors.append('bar_ticks '+d['id'])
        checks+=1
        if d['steps_per_bar'] <=0 or expected%d['steps_per_bar']!=0:errors.append('step_grid '+d['id'])
        checks+=1
        step_ticks=expected//d['steps_per_bar']
        for e in d['events']:
            if not (1<=e['bar']<=d['bars'] and 0<=e['step0']<d['steps_per_bar']): errors.append('out_of_bars '+d['id'])
            checks+=1
            if not 0<=e['tick']<expected*d['bars'] or e['tick']+e['duration_ticks']>expected*d['bars']:errors.append('out_of_ticks '+d['id'])
            checks+=1
            if e['tick']!=(e['bar']-1)*expected+e['step0']*step_ticks+e['offset_ticks']:errors.append('onset_mismatch '+d['id'])
            checks+=1
        mp=STUDIES/('STEPS_DRUMS__'+d['id']+'__ORIGINAL_MIDI__V5_3.mid')
        mid=mido.MidiFile(mp)
        if mid.ticks_per_beat!=d['ppq']:errors.append('ppq '+d['id'])
        checks+=1
        note_events=[];starts=defaultdict(list);sig=[];tempos=[]
        for track in mid.tracks:
            tick=0
            for msg in track:
                tick+=msg.time
                if msg.type=='time_signature':sig.append((msg.numerator,msg.denominator));checks+=1
                if msg.type=='set_tempo':tempos.append(msg.tempo);checks+=1
                if msg.type=='note_on' and msg.velocity>0:
                    starts[(msg.channel,msg.note)].append((tick,msg.velocity))
                elif msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
                    k=(msg.channel,msg.note)
                    if not starts[k]:errors.append('unmatched_off '+d['id']);continue
                    t,v=starts[k].pop(0);note_events.append((t,tick-t,msg.note,v,msg.channel));checks+=1
        if any(starts.values()):errors.append('unclosed '+d['id'])
        checks+=1
        exp=sorted((e['tick'],e['duration_ticks'],e['note'],e['velocity'],9) for e in d['events'])
        if sorted(note_events)!=exp:errors.append('JSON_MIDI_event_disagreement '+d['id'])
        checks+=1
        if (nn,dd) not in sig:errors.append('time_sig '+d['id'])
        checks+=1
        if not tempos or abs(mido.tempo2bpm(tempos[0])-d['bpm'])>0.01:errors.append('tempo '+d['id'])
        checks+=1
    if len(ids)!=12:errors.append('not_12_studies')
    checks+=1
    f=lambda n:440*2**((n-69)/12)
    for expr,exp in [(f(69),440),(f(81),880),(f(27),38.89087296),(15000/132,113.6363636),(240000/174,1379.3103448),((15000/132)*.292,33.1818182),(480*4*7/8,1680)]:
        checks+=1
        if not math.isclose(expr,exp,rel_tol=0,abs_tol=.02):errors.append('numeric_reference_failed')
    idx=ROOT/'00_NAVIGATION'/'STEPS_DATEIENINDEX_V5_3.csv'
    if not idx.exists():errors.append('new_file_index_missing')
    else:
        with idx.open(encoding='utf-8-sig',newline='') as f:rows=list(csv.DictReader(f,delimiter=';'))
        for rec in rows:
            path=ROOT/rec['path']
            checks+=1
            if not path.exists() or hashlib.sha256(path.read_bytes()).hexdigest()!=rec['sha256']:errors.append('file_index_hash_'+rec['path'])
    return {'library_version':'5.3.0','technical_checks':checks,'technical_errors':errors,'own_midi_studies':len(ids),'claim':'technical_only_no_musicological_or_listening_review'}

if __name__=='__main__':
    r=check_all();print(json.dumps(r,indent=2,ensure_ascii=False));raise SystemExit(1 if r['technical_errors'] else 0)

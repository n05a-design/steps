#!/usr/bin/env python3
"""Run from anywhere; validates STEPS V5.4 local data and preserved V5.3 integrity."""
import hashlib,json,re,sys
from pathlib import Path
import mido
try:
 import jsonschema
except ImportError:
 jsonschema=None
root=Path(__file__).resolve().parents[1];errors=[];checks=0

def verify(ok,what):
 global checks
 checks+=1
 if not ok:errors.append(what)

old=json.loads((root/'00_NAVIGATION/STEPS_BASE_HASHES_V5_3__V5_4.json').read_text())
for path,sha in old.items():
 p=root/path
 verify(p.is_file(),'base file absent: '+path)
 if p.is_file():verify(hashlib.sha256(p.read_bytes()).hexdigest()==sha,'base file differs: '+path)
reg=json.loads((root/'10_QUELLEN_LIZENZEN/STEPS_QUELLEN__V5_4-Oeffentliche-Referenzen-Claim-Status__REGISTER__V5_4.json').read_text())
source_ids={r['id'] for r in reg}
verify(len(source_ids)==len(reg),'source ids duplicate')
for r in reg:
 verify(r['url'].startswith('https://'),'source HTTPS '+r['id'])
 verify(r['reading_status']=='public_page_or_abstract_only','unsupported full read '+r['id'])
chap=json.loads((root/'14_DATENMODELLE/STEPS_KNOWLEDGE__V5_4-Fachstudien-Quellen-Linkmatrix__DATEN__V5_4.json').read_text())
for c in chap:
 verify((root/c['file']).is_file(),'chapter not found '+c['id'])
 for sid in c['source_ids']:verify(sid in source_ids,'unresolved source '+sid)
prog=json.loads((root/'03_CHORD_PROGRESSIONS/STEPS_PROGRESSIONS__V5_4-Originale-Progressionsfaelle__DATEN__V5_4.json').read_text())
schema=json.loads((root/'14_DATENMODELLE/STEPS_SCHEMA__V5_4-Progression-Cases__SCHEMA__V5_4.json').read_text())
pcs={'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
regex=re.compile(r'^([A-G](?:#|b)?)(maj7|m7b5|m7|7sus4|7|dim|sus4|add9|m)?(?:/([A-G](?:#|b)?))?$')
for c in prog:
 if jsonschema: 
  try:jsonschema.validate(c,schema);checks+=1
  except Exception as e:errors.append('schema '+c['id']+str(e))
 verify(len(c['chord_events'])==c['bars'],'chord length '+c['id'])
 for ix,chord in enumerate(c['chord_events']):
  m=regex.fullmatch(chord['symbol']);verify(bool(m),'chord syntax '+str(chord))
  if m:
   verify(chord['root_pc']==pcs[m.group(1)],'chord root pc '+c['id'])
   verify(chord['bass_pc']==pcs[m.group(3) or m.group(1)],'chord bass pc '+c['id'])
  verify(chord['start_beats']==ix*4,'chord onsets '+c['id'])
  verify(chord['duration_beats']==4,'chord durations '+c['id'])
  verify(len(set(chord['pcs']))==len(chord['pcs']),'pc duplicates '+c['id'])

for n in range(1,17):
 id=f'CS54-{n:02d}'
 stem=f'04_COMPOSING/V5_4_Eigene_MIDI_Studien/STEPS_COMPOSING__{id}'
 notes=json.loads((root/(stem+'__NOTEN_JSON__V5_4.json')).read_text())
 p=root/(stem+'__ORIGINAL_16BAR__V5_4.mid');mid=mido.MidiFile(str(p))
 verify(mid.type==1,'midi format '+id)
 verify(mid.ticks_per_beat==480,'tpq '+id)
 verify(len(mid.tracks)==5,'track count '+id)
 verify(notes['bars']==16,'bar count '+id)
 expected={}
 for e in notes['notes']:
  verify(0<=e['midi']<=127,'note pitch '+id)
  verify(1<=e['velocity']<=127,'velocity '+id)
  verify(e['duration_ticks']>0,'note length '+id)
  verify(e['onset_ticks']>=0,'onset '+id)
  verify(e['onset_ticks']+e['duration_ticks']<=16*4*480,'overbar '+id)
  expected[(e['track'],e['midi'],e['onset_ticks'],e['duration_ticks'],e['velocity'])]=expected.get((e['track'],e['midi'],e['onset_ticks'],e['duration_ticks'],e['velocity']),0)+1
 actual={}
 for i,tr in enumerate(mid.tracks[1:]):
  abspos=0;on={}
  for msg in tr:
   abspos+=msg.time
   if msg.type=='note_on' and msg.velocity>0: on.setdefault(msg.note,[]).append((abspos,msg.velocity))
   elif msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
    starts=on.get(msg.note,[])
    verify(bool(starts),'unpaired off '+id)
    if starts:
     st,v=starts.pop(0);key=(['Chords','Bass','Melody','Drums'][i],msg.note,st,abspos-st,v)
     actual[key]=actual.get(key,0)+1
  verify(not any(on.values()),'unfinished note_on '+id)
 verify(expected==actual,'JSON/MIDI mismatch '+id)

r={'version':'5.4.0','checks':checks,'errors':errors,'old_v53_files_checked':len(old),
 'new_chapters_checked':len(chap),'new_progressions_checked':len(prog),
 'new_midi_checked':16,'status':'passed' if not errors else 'failed',
 'warnings':['Does not validate aesthetics, exact notation, copyright permissions or audio rendering.']}
print(json.dumps(r,indent=2,ensure_ascii=False))
sys.exit(1 if errors else 0)

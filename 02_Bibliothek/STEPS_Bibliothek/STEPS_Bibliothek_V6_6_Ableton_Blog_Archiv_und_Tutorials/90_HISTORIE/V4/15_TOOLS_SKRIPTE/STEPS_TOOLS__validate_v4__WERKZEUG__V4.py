#!/usr/bin/env python3
"""STEPS V4 mechanical QA. Does not validate music aesthetics or all theory claims."""
from pathlib import Path
import json, sys, re, hashlib, collections, datetime
try:
 import jsonschema
except ImportError:
 jsonschema=None
try:
 import mido
except ImportError:
 mido=None
ROOT=Path(__file__).resolve().parents[1]
issues=[]
passed=0

def check(ok,why):
 global passed
 if ok:passed+=1
 else:issues.append(why)

def load(rel):return json.loads((ROOT/rel).read_text(encoding='utf8'))

sources=load('05_Quellen/QUELLENREGISTER_V4.json')
new_sources=[s for s in sources if s.get('id','').startswith('EXT-V4-')]
ids=[s['id'] for s in sources]
check(len(ids)==len(set(ids)),'Quellen-IDs nicht eindeutig')
check(len(new_sources)==30,'30 neue Quellen-/Editionseinträge nicht gefunden')
check(all(s.get('url','').startswith('https://') for s in new_sources),'Neue Quellen ohne dauerhafte https URL')
modules=load('01_Studienbaende/RESEARCH_MODULES_V4.json')
check(len(modules)==49,'49 Module fehlen')
for m in modules:
 check(bool(m['explanation'] and m['original_worked_example'] and m['limits'] and m['codex_implementation']),f"Leeres Modul {m['id']}")
 for id in m['source_family_ids']:
  check(id in ids,f"Quellenkandidat {id} fehlt ({m['id']})")

tax=load('02_Fachlexikon/TAXONOMIE_V4.json')
check(sum(map(len,tax['pillars'].values()))==tax['total_subtopics'],'Taxonomie-Zählung falsch')
prog=load('03_Progressionsatlas/NEUE_PROGRESSIONSFAMILIEN_V4.json')
allprog=load('03_Progressionsatlas/GESAMTREGISTER_V3_UND_V4.json')
check(len(prog)==131 and len(allprog)==226,'Progressionszählung falsch')
check(len({p['id'] for p in allprog})==len(allprog),'Progression IDs doppelt')
for p in prog:
 check(len(p['chord_symbols'])>=2,f"Nur ein Chord: {p['id']}")
 check(p['status']=='editorial_example_pending_musical_review',f"Unzulässiger Reviewstatus: {p['id']}")
 check(bool(p['roman_label_candidates'] and p['composition_intent']),f"Unvollständige Progressionsanalyse: {p['id']}")

rules=load('02_Fachlexikon/NEUE_REGELENTWUERFE_V4.json')
allrules=load('02_Fachlexikon/GESAMTREGELREGISTER_V3_UND_V4.json')
tech=load('04_Kompositionslabor/TECHNIKREGISTER_V4.json')
check(len(rules)==59 and len(allrules)==136,'Regelzählung falsch')
check(len(tech)==134,'Technikzählung falsch')
check(len({r['id'] for r in allrules})==len(allrules),'Regel-IDs doppelt')
for item in rules:
 check(bool(item.get('non_applicability_or_counterexample')),f"Regel ohne Geltungsgrenze: {item['id']}")

# 12-TET only, chord quality grammar for newly composed studies.
PITCH={'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'Bb':10,'B':11}
QUALITY={'':(0,4,7),'m':(0,3,7),'7':(0,4,7,10),'maj7':(0,4,7,11),'m7':(0,3,7,10),'dim':(0,3,6)}
def chord(sym):
 match=re.fullmatch(r'([A-G](?:#|b)?)(maj7|m7|dim|m|7)?',sym)
 if not match:raise ValueError(sym)
 name,quality=match.groups()
 root=PITCH[name]
 return root,{(root+i)%12 for i in QUALITY[quality or '']}

studies=sorted((ROOT/'04_Kompositionslabor/Partituren').glob('ETUDE-V4-*.json'))
check(len(studies)==30,'30 vollständige Etüden-JSONs fehlen')
if jsonschema:
 sch=load('06_Datenmodelle/study.v4.schema.json')
else:
 issues.append('jsonschema nicht verfügbar – Schemaprüfung nicht ausgeführt')
for path in studies:
 e=json.loads(path.read_text(encoding='utf8'))
 if jsonschema:
  try:jsonschema.validate(e,sch);passed+=1
  except Exception as exc:issues.append(f'Schema {e["id"]}: {exc}')
 check(e['bars_count']==len(e['bars'])==16,f'16 Takte fehlen: {e["id"]}')
 check(e['duration_beats']==64,f'Dauer fehlt {e["id"]}')
 check(len(e['harmonic_plan'])==8,f'Harmonieplan nicht 8 Segmente: {e["id"]}')
 for j,b in enumerate(e['bars']):
  check(b['bar']==j+1,f'Taktzähler falsch {e["id"]}:{j+1}')
  check(b['chord']==e['harmonic_plan'][j//2],f'Akkordsymbol passt nicht zu 2-Bar Segment: {e["id"]}:{j+1}')
  try:root,pcs=chord(b['chord'])
  except Exception as exc:issues.append(f'Unbekannter Akkord {e["id"]} Takt {j+1}: {exc}');continue
  check(abs(sum(n['duration_beats'] for n in b['melody'])-4)<1e-8,f'Melodie-Takt zu kurz/lang: {e["id"]}:{j+1}')
  check(abs(sum(n['duration_beats'] for n in b['bass'])-4)<1e-8,f'Bass-Takt zu kurz/lang: {e["id"]}:{j+1}')
  check(b['bass'][0]['midi']%12==root,f'Bass ist nicht Akkordgrundton: {e["id"]}:{j+1}')
  check(all(n['midi']%12 in pcs for n in b['melody']),f'Melodie enthält unerwartete Chord-Note: {e["id"]}:{j+1}')
  check(all(n%12 in pcs for n in b['accompaniment_midi']),f'Pad enthält fremde Töne: {e["id"]}:{j+1}')
  check(all(n['start_beat']>=0 and n['duration_beats']>0 and n['start_beat']+n['duration_beats']<=4.0000001 for n in b['melody']),'Melodie-Event außer Takt')
  check(all(0<=n['midi']<=127 for n in b['melody']+b['bass']),f'MIDI pitch außerhalb 0..127: {e["id"]}:{j+1}')
 mp=ROOT/'04_Kompositionslabor/MIDI'/f'{e["id"]}.mid'
 check(mp.exists(),f'MIDI-Datei fehlt {e["id"]}')
 if mp.exists() and mido:
  try:
   midi=mido.MidiFile(mp)
   check(len(midi.tracks)==4,f'Spurenanzahl fehlt {e["id"]}')
   check(midi.ticks_per_beat==480,f'PPQ falsch {e["id"]}')
   for ti,track in enumerate(midi.tracks[1:],1):
    active=collections.Counter();cnt=collections.Counter();last=0
    for msg in track:
     check(msg.time>=0,f'Negative delta ticks: {e["id"]}')
     last+=msg.time
     if msg.type=='note_on' and msg.velocity>0:active[msg.note]+=1;cnt['on']+=1
     if msg.type=='note_off' or (msg.type=='note_on' and msg.velocity==0):
      active[msg.note]-=1;cnt['off']+=1
      check(active[msg.note]>=0,f'Orphan note off {e["id"]} track {ti}')
    check(not any(active.values()),f'Hängende MIDI-Noten {e["id"]} track {ti}')
    check(cnt['on']==cnt['off'],f'Unbalancierte MIDI-Events {e["id"]}')
    check(last<=64*480,f'MIDI-Material nach 16 Takten {e["id"]}')
  except Exception as exc:issues.append(f'MIDI parse {e["id"]}: {exc}')
 elif mp.exists() and not mido: issues.append('mido fehlt – MIDI Parse Tests nicht ausführbar')

# Source and schema validation, no claim source-level review.
if jsonschema:
 for s in new_sources:
  try:jsonschema.validate(s,load('06_Datenmodelle/source.v4.schema.json'));passed+=1
  except Exception as exc:issues.append(f'Source schema {s["id"]}: {exc}')
 for r in rules:
  try:jsonschema.validate(r,load('06_Datenmodelle/rule.v4.schema.json'));passed+=1
  except Exception as exc:issues.append(f'Rule schema {r["id"]}: {exc}')

# Historischer Bestand muss unverändert erhalten sein.
old=ROOT/'00_HISTORISCH_V3'/'00_Archiv_V1'
check(len([p for p in old.glob('*.md')])==7,'Die sieben ursprünglichen Markdown-Dateien fehlen im V3-Archiv')
check((old/'Master-Research-Prompt.md').exists(),'Master Research Prompt fehlt – alte Handover-Warnung nicht mehr aktuell')

report={
 'tool':'STEPS_V4_MECHANICAL_VALIDATOR',
 'date':'2026-11-08',
 'status':'pass' if not issues else 'fail',
 'passed_individual_assertions':passed,
 'issues':issues,
 'subjects':{'source_records_total':len(sources),'new_web_records':len(new_sources),'topics':tax['total_subtopics'],'new_research_modules':len(modules),'progressions_total':len(allprog),'new_progressions':len(prog),'rules_total':len(allrules),'composing_methods_total':len(tech),'playable_16_bar_studies':len(studies)},
 'limitations':['No expert musicological review','No absolute originality audit','No license clearance for underlying source works','No actual STEPS Git repository audit','Historical V3 tests not rerun here','Roman-numeral interpretation and stylistic fit not automatically tested','MIDI note spellings are neutral 12-TET display names, not harmonically verified enharmonic spellings']
}
(ROOT/'08_Validierung/MECHANISCHER_PRUEFBERICHT_V4.json').write_text(json.dumps(report,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
print(json.dumps({'status':report['status'],'assertions':passed,'issues':len(issues),'studies':len(studies)},ensure_ascii=False))
if issues:
 print('\n'.join(issues[:50]))
 sys.exit(1)

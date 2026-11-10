#!/usr/bin/env python3
"""Structural quality check for STEPS V3 seed knowledge. Not a music theory peer review."""
from pathlib import Path
import sys,json,re,collections
root=Path(__file__).resolve().parent.parent
locations={
 'sources':'05_Quellen/SOURCE_REGISTRY_VERIFIED_METADATA.json',
 'candidates':'05_Quellen/BIBLIOGRAPHY_ACQUISITION_QUEUE.json',
 'concepts':'02_Wissensdaten/THEORY_CONCEPTS_V3.json',
 'progressions':'02_Wissensdaten/PROGRESSION_ATLAS_V3.json',
 'techniques':'02_Wissensdaten/COMPOSITION_TECHNIQUES_V3.json',
 'studies':'02_Wissensdaten/ORIGINAL_COMPOSITION_STUDIES_V3.json',
 'rules':'02_Wissensdaten/TYPED_RULES_V3.json',
 'qa':'04_Qualitaet/VALIDATION_CASES_V3.json',
}
all_data={};errors=[];notes=[]
for name,p in locations.items():
 try:
  data=json.loads((root/p).read_text(encoding='utf-8'));assert isinstance(data,list)
  all_data[name]=data
 except Exception as exc:errors.append(f'{name}: {exc}')
ids=[]
for name,rows in all_data.items():
 for r in rows:
  if not isinstance(r,dict):errors.append(f'{name}: not object');continue
  if not r.get('id'):errors.append(f'{name}: missing ID')
  ids.append(r.get('id'))
  if name=='sources':
   for f in ('canonical_url','metadata_status','reading_status','license_note','title'):
    if not r.get(f): errors.append(f"{r.get('id')}: missing {f}")
  if name=='concepts':
   for f in ('definition','original_illustration','limits_and_misconceptions','review_status'):
    if not r.get(f):errors.append(f"{r.get('id')}: missing {f}")
  if name=='progressions':
   if len(r.get('chord_sequence',[]))<2:errors.append(f"{r.get('id')}: no progression")
   if not r.get('key_or_center') or not r.get('roman_analysis'):errors.append(f"{r.get('id')}: missing harmonic context")
  if name=='studies':
   for f in ('seed_motif','chord_plan','form_plan','development_steps','bass_and_voice_leading_plan'):
    if not r.get(f):errors.append(f"{r.get('id')}: missing {f}")
  if name=='rules':
   if r.get('type') not in ('constraint','tendency','convention','transformation','interpretation','heuristic','empirical_observation'):
    errors.append(f"{r.get('id')}: unknown type")
   if not r.get('scope_limit'):errors.append(f"{r.get('id')}: missing limit")
if len(ids)!=len(set(ids)):errors.append('IDs not unique')
source_ids={r['id'] for r in all_data.get('sources',[])}
for r in all_data.get('concepts',[]):
 for sid in r.get('source_candidates',[]):
  if sid not in source_ids:errors.append(f"{r['id']} unknown source candidate {sid}")
for r in all_data.get('progressions',[]):
 for sid in r.get('source_candidate_ids',[]):
  if sid not in source_ids:errors.append(f"{r['id']} unknown source candidate {sid}")
for r in all_data.get('sources',[]):
 if r.get('full_text_verified') is True and r.get('reading_status')=='landing_page_or_excerpt_only':errors.append(f"{r['id']}: impossible access status")
# Independent, implemented small 12-TET pitch model as a real smoke check. Does not parse every chord!
pc={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def note_to_midi(note):
 m=re.fullmatch(r'([A-G])([#b]?)(-?\d+)',note)
 if not m:raise ValueError(note)
 k,acc,octv=m.groups();return (int(octv)+1)*12+pc[k]+({'#':1,'b':-1,'':0}[acc])
for a,b,n in [('C4','E4',4),('C4','Eb4',3),('B3','C4',1),('G3','D4',7),('C4','F#4',6)]:
 try:
  if note_to_midi(b)-note_to_midi(a)!=n:errors.append(f'pitch smoke {a} {b} mismatch')
 except Exception as ex:errors.append(f'pitch smoke parse {ex}')
# Execute actual 12-TET chord quality and mode-interval checks from specified QA cases.
def pc_of(s):
 m=re.fullmatch(r'([A-G])([#b]?)',s)
 if not m:raise ValueError('Invalid pitch '+s)
 n,acc=m.groups();return (pc[n]+({'#':1,'b':-1,'':0}[acc]))%12
qualities={'major':[0,4,7],'minor':[0,3,7],'diminished':[0,3,6],
 'augmented':[0,4,8],'major_seventh':[0,4,7,11],
 'dominant_seventh':[0,4,7,10],'minor_seventh':[0,3,7,10],
 'half_diminished':[0,3,6,10],'fully_diminished':[0,3,6,9]}
scales={'major':[0,2,4,5,7,9,11],'natural_minor':[0,2,3,5,7,8,10],
 'harmonic_minor':[0,2,3,5,7,8,11],'dorian':[0,2,3,5,7,9,10],
 'lydian':[0,2,4,6,7,9,11],'mixolydian':[0,2,4,5,7,9,10],
 'phrygian':[0,1,3,5,7,8,10],'locrian':[0,1,3,5,6,8,10],
 'whole_tone':[0,2,4,6,8,10],'major_pentatonic':[0,2,4,7,9]}
checked_chords=checked_scales=0
for case in all_data.get('qa',[]):
 inp=case.get('input',{});expected=case.get('expected',{})
 if 'quality' in inp and 'notes_spelled' in expected:
  try:
   root_pc=pc_of(inp['root'])
   actual=[(pc_of(n)-root_pc)%12 for n in expected['notes_spelled']]
   if actual!=qualities[inp['quality']]:errors.append(f"{case['id']}: chord tones disagree with quality")
   checked_chords+=1
  except Exception as ex:errors.append(f"{case['id']}: {ex}")
 if 'mode' in inp and 'notes' in expected:
  try:
   root_pc=pc_of(inp['tonic'])
   actual=[(pc_of(n)-root_pc)%12 for n in expected['notes']]
   if actual!=scales[inp['mode']]:errors.append(f"{case['id']}: scale spelling interval pattern mismatch")
   checked_scales+=1
  except Exception as ex:errors.append(f"{case['id']}: {ex}")
notes.append(f'Executed {checked_chords} chord-quality and {checked_scales} scale-interval 12-TET cases.')
notes.append('Executed five interval smoke checks, JSON parsing, unique/referential IDs, field completeness and typed-rule validation.')
notes.append('NOT EXECUTED: remainder of 110 full QA specifications, formal roman analysis, MusicXML/MIDI roundtrips, human musical review, licensing.')
report='\n'.join([
 '# STEPS V3 – Executed Structural Audit',
 '',f"**Result:** {'PASS' if not errors else 'FAIL'} (structural only)",
 f"**Error count:** {len(errors)}",'',
 '## Object counts',
 *[f'- {k}: {len(v)}' for k,v in all_data.items()],
 '', '## What was actually checked',
 *[f'- {s}' for s in notes],
 '', '## Errors',
 *([f'- {e}' for e in errors] if errors else ['- No structural errors detected.']),
 '', '## Limitations',
 '- This audit is NOT proof of scientific correctness, book full-text access, rights clearance or finished code integration.',
 '- All draft theory/pattern/composition records require explicit specialist review before canonical release.',
 ])+'\n'
(root/'04_Qualitaet/STRUCTURAL_AUDIT_EXECUTED_V3.md').write_text(report,encoding='utf-8')
print(report)
sys.exit(1 if errors else 0)

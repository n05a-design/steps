#!/usr/bin/env python3
"""Independent mechanical audit of V5 examples, not a peer-reviewed music-theory audit."""
import json, pathlib, collections, xml.etree.ElementTree as ET, re, sys
import mido
BASE=pathlib.Path(__file__).resolve().parents[1]
N=0;failures=[]
def check(cond,msg):
 global N
 N+=1
 if not cond:failures.append(msg)

src=json.loads((BASE/'06_Quellen_und_Rechte/V5_EXTERN_RECHERCHIERTE_QUELLEN.json').read_text())
check(len(src)==27,'source register count')
check(len({x['source_id'] for x in src})==len(src),'source unique IDs')
for x in src:
 check(x['canonical_url'].startswith('https://'),'source https '+x['source_id'])
 check(x['verification_status'] in ('landing_page_checked','content_section_checked'),'source status '+x['source_id'])
 check(x['full_work_read'] is False,'never claim full source was read '+x['source_id'])

families=json.loads((BASE/'05_Wissensobjekte/KURATIERTE_PROGRESSIONSFAMILIEN_V5.json').read_text())
progressions=json.loads((BASE/'05_Wissensobjekte/TRANSPONIERTE_PROGRESSIONSVARIANTEN_V5.json').read_text())
check(len(families)==53,'progression family count')
check(len(progressions)==len(families)*13*2,'progression 13 key x 2 variants')
check(len({x['id'] for x in progressions})==len(progressions),'unique progression IDs')
NOTES='C D E F G A B'.split();pcbase={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
def pc(s):
 if not re.fullmatch(r'[A-G][#b]{0,2}',s):raise ValueError(s)
 return (pcbase[s[0]]+s.count('#')-s.count('b'))%12
for x in progressions:
 check(len(x['events'])==len(next(f['degree_tokens'] for f in families if f['id']==x['family_id'])),'degree/event count '+x['id'])
 check(len({n[0] for n in x['major_scale_spelling']})==7,'7 diatonic note letters '+x['id'])
 p=0
 for e in x['events']:
  check(e['onset_beat']==p,'onset '+x['id']); p+=e['duration_beats']
  check(e['duration_beats']>0,'duration '+x['id'])
  check(all(pc(n)==v for n,v in zip(e['chord_tones_spelled'],e['pitch_classes'])),'spelling/PC '+x['id'])
  check(len(e['chord_tones_spelled'])==len(e['pitch_classes']),'chord tones length '+x['id'])
 check(x['total_beats']==p,'sum durations '+x['id'])
 check(x['genre_frequency_claim'] is None,'no false empirical claim '+x['id'])

studies=json.loads((BASE/'04_Kompositionslabor/STUDIENREGISTER_V5.json').read_text())
check(len(studies)==16,'score count')
for item in studies:
 wid=item['id'];work=json.loads((BASE/f'04_Kompositionslabor/Partituren/{wid}.json').read_text())
 meter=int(work['meter'].split('/')[0])
 check(work['total_bars']==32,'bars '+wid)
 check([s['first_bar'] for s in work['sections']]==[1,9,17,25],'section boundaries '+wid)
 check([s['last_bar'] for s in work['sections']]==[8,16,24,32],'section boundaries + lengths '+wid)
 check(len(work['chords'])==32,'chord bars '+wid)
 check(set(work['voices'])=={'melody','bass','harmony','countermelody'},'4 parts '+wid)
 for part,events in work['voices'].items():
  for e in events:
   check(0<=e['pitch']<=127,'MIDI range '+wid)
   check(e['duration_beats']>0,'event duration '+wid)
   check(0<=e['onset_beats'] and e['onset_beats']+e['duration_beats']<=32*meter,'event bounds '+wid)
  for bar in range(1,33):
   es=[e for e in events if e['bar']==bar]
   if part=='harmony':
    check(all(e['duration_beats']==meter for e in es),'harmonic simultaneity '+wid)
   else:
    check(sum(e['duration_beats'] for e in es)==meter,'non-chord voice bar duration '+wid)
    check([e['onset_beats'] for e in es]==sorted(e['onset_beats'] for e in es),'voice onset order '+wid)
 f=BASE/f'04_Kompositionslabor/MIDI/{wid}.mid'
 mid=mido.MidiFile(f)
 check(mid.type==1,'MIDI type 1 '+wid);check(len(mid.tracks)==4,'4 MIDI tracks '+wid)
 for i,track in enumerate(mid.tracks):
  active=collections.Counter();absolute=0;end=0
  for msg in track:
   absolute+=msg.time
   if msg.type=='note_on' and msg.velocity>0:active[msg.note]+=1
   if msg.type=='note_off' or msg.type=='note_on' and msg.velocity==0:
    active[msg.note]-=1;check(active[msg.note]>=0,'note off without on '+wid)
  check(not any(active.values()),'unbalanced MIDI notes '+wid)
  check(absolute==32*meter*480,'track length '+wid)
 xml=ET.parse(BASE/f'04_Kompositionslabor/Partituren/{wid}.musicxml').getroot()
 check(xml.tag=='score-partwise','xml root '+wid)
 parts=xml.findall('part');check(len(parts)==4,'xml parts '+wid)
 for part in parts:
  measures=part.findall('measure');check(len(measures)==32,'xml 32 measures '+wid)
  for measure in measures:
   count=sum(int(no.findtext('duration')) for no in measure.findall('note') if no.find('chord') is None)
   check(count==meter*480,'musicxml measure durations '+wid)

summary={'format':'STEPS-mechanical-validation-v5','generated':'2026-11-08','checks_executed':N,'failures':failures[:50], 'failures_count':len(failures), 'source_records':len(src),'curated_progression_families':len(families),'algorithmic_progression_variants':len(progressions),'original_study_scores':len(studies),'score_bars_generated':sum(32 for _ in studies),'scientific_peer_review':'NOT_PERFORMED','musical_quality_review':'NOT_PERFORMED','external_source_full_text_audit':'NOT_PERFORMED','result':'PASSED' if not failures else 'FAILED'}
(BASE/'08_Validierung/PRUEFBERICHT_V5.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(summary,indent=2))
sys.exit(0 if not failures else 1)

#!/usr/bin/env python3
"""Generate original pedagogical composition sketches (not peer-reviewed finished works)."""
from __future__ import annotations
import json, re, pathlib, copy, xml.etree.ElementTree as ET
import mido
ROOT=pathlib.Path(__file__).resolve().parent
(ROOT/'MIDI').mkdir(exist_ok=True);(ROOT/'Partituren').mkdir(exist_ok=True)
NOTE_PC={'C':0,'C#':1,'Db':1,'D':2,'D#':3,'Eb':3,'E':4,'F':5,'F#':6,'Gb':6,'G':7,'G#':8,'Ab':8,'A':9,'A#':10,'Bb':10,'B':11}
SCALES={'major':[0,2,4,5,7,9,11],'minor':[0,2,3,5,7,8,10],'dorian':[0,2,3,5,7,9,10],'mixolydian':[0,2,4,5,7,9,10],'phrygian':[0,1,3,5,7,8,10],'blues':[0,3,5,6,7,10]}
STUDIES=[
('Satz und Fortsetzung','C','major',4,94,'C F G C','C Am Dm G7','F Dm G7 C','C Fm G7 C','Motivwiederholung → Fragmentierung → Dominantziel', 'common_practice'),
('Periodenmodell und Halbschluss','F','major',4,86,'F Bb C7 C7','F Dm Gm C7','Dm Bb C7 F','Bb Bbm F/C F','Vordersatz offen, Nachsatz mit stärkerer Rückkehr','classical_period'),
('Emergente Songtonika','C','major',4,112,'Am F G Em','Am F G G','Dm F G G','C G Am F','Vorbereiteter C-Einsatz erst im letzten Formteil','pop_form'),
('Dorischer Zentralton','D','dorian',4,102,'Dm7 G7 Dm7 G7','Dm7 Em7 Dm7 G7','C Dm7 G7 Dm7','Dm7 G7 Dm7 Dm7','D-Pedal und charakteristische große Sexte','modal_dorian'),
('Mixolydische Rockschleife','G','mixolydian',4,118,'G F C G','G C F G','Am C F G','G F C G','bVII statt ausschließlich klassischer Dominantik','pop_rock'),
('Aeolische Ballade','A','minor',4,76,'Am G F Em','Am Dm E7 Am','F G Am F','Dm E7 Am Am','Wechsel aeolisch/nachdrücklich leittönig','minor_harmony'),
('Jazz Turnaround und Guide Tones','C','major',4,124,'Cmaj7 A7 Dm7 G7','Em7 A7 Dm7 G7','Dm7 Db7 Cmaj7 Am7','Dm7 G7 Cmaj7 Cmaj7','lokale Ziele und Vergleich der Substitution','jazz'),
('Blues mit Dominant-Tonika','C','blues',4,100,'C7 F7 C7 C7','F7 F7 C7 C7','G7 F7 C7 G7','C7 F7 G7 C7','I7 als tonikaler Bluesklang, nicht V/IV als Default','blues'),
('Soul mit chromatischen Innentönen','C','major',4,92,'Cmaj9 E7 Am9 Dm9','Cmaj9 Fmaj7 Fm6 G7','Am9 Dm9 G13 Cmaj9','Fmaj7 Fm6 Cmaj9 Cmaj9','Septime/None und gleitende Innenstimme','neo_soul'),
('Cinematic color fields','C','minor',4,70,'Cm Ab Eb Bb','Cm Ab Fm G7','Cm Eb Db Ab','Fm G7 Cm Cm','Lange Klangflächen, Abschnitts-Kontrast, spätere Konvergenz','cinematic'),
('Walzer mit Phrasenrückkehr','G','major',3,146,'G C D7 G','G Em Am D7','C G Am D7','C Cm G G','3/4-Metrum, drei Viertel je Takt','waltz'),
('Minimalistischer Pedalprozess','D','dorian',4,108,'Dm7 Dm7 G7 Dm7','Dm7 Em7 Dm7 G7','Dm7 G7 Dm7 Dm7','Dm7 Dm7 G7 Dm7','Wiederholung, registrale/rythmische Änderung vor Harmonievielfalt','minimalism'),
('Chromatic mediants','C','major',4,80,'C E Ab C','C Ab Eb Bb','C E Am Fm','C Fm G7 C','Terzbeziehung und Stimmführung statt globaler Funktionspflicht','chromatic'),
('Gospel harmonic arrival','Bb','major',4,98,'Bb Eb F7 Bb','Gm7 Cm7 F7 Bb','Eb Ab Bb F7','Eb Ebm Bb Bb','Rückkehr über IV/iv und echte Formankunft','gospel'),
('Triadische Transformationen','C','major',4,89,'C Cm Ab C','Em G C Am','C E Am Ab','C Fm G7 C','P/L/R-nahe Schritte als farbige Klangmotive','neo_riemannian'),
('Phrygische Grenzfälle','E','phrygian',4,96,'Em F Em F','Em Am F Em','Dm Em F Em','Em F Em Em','bII als charakteristische Stufe, Kontextzentrum E','modal_phrygian')
]
assert len(STUDIES)==16
CHORD_PAT=re.compile(r'^([A-G](?:#|b)?)(maj9|maj7|m9|m7|m6|m|13|9|7|dim7|sus4|add9)?(?:/([A-G](?:#|b)?))?$')
def chord_info(symbol):
 m=CHORD_PAT.fullmatch(symbol)
 if not m: raise ValueError(f'Unsupported chord symbol {symbol}')
 root,q,bass=m.group(1),m.group(2) or '',m.group(3)
 intervals={'':[0,4,7],'maj7':[0,4,7,11],'maj9':[0,4,7,11,2],'m':[0,3,7],'m7':[0,3,7,10],'m9':[0,3,7,10,2],'m6':[0,3,7,9],'7':[0,4,7,10],'9':[0,4,7,10,2],'13':[0,4,7,10,2,9],'dim7':[0,3,6,9],'sus4':[0,5,7],'add9':[0,4,7,2]}[q]
 pc=NOTE_PC[root]
 return {'root':root,'bass':bass or root,'quality':q or 'major','pitch_classes':sorted({(pc+i)%12 for i in intervals})}

def pitch_from_pc(pc,base):
 # return nearest pitch at or above base with the given pitch class
 return base+(pc-base)%12

def melody_pattern(tonic_pc,scale,bar,phrase,section):
 # authored contour families; adapt to modes and return stable, repeatable motivic variations
 cells=((0,1,2,1),(2,3,4,2),(4,5,4,2),(1,2,1,0),(0,2,4,3),(4,3,2,1),(1,3,4,5),(3,2,1,0))
 cell=cells[bar%8]
 if section==1: cell=tuple((i+1)%7 for i in cell)
 if section==2: cell=tuple(reversed(cell))
 if section==3: cell=tuple((i+(1 if bar%2 else 0))%7 for i in cell)
 if scale=='blues': cell=tuple(i%6 for i in cell)
 return [(tonic_pc+SCALES[scale][i])%12 for i in cell]

def midinote_name(n):
 pc=n%12;step,alt={0:('C',0),1:('C',1),2:('D',0),3:('E',-1),4:('E',0),5:('F',0),6:('F',1),7:('G',0),8:('A',-1),9:('A',0),10:('B',-1),11:('B',0)}[pc]
 return step,alt,n//12-1

works=[]
for n,(title,key,mode,meter,bpm,seg1,seg2,seg3,seg4,intent,lens) in enumerate(STUDIES,1):
 wid=f'STEPS-V5-STUDY-{n:03d}'
 sequences=[a.split() for a in [seg1,seg2,seg3,seg4]]
 assert all(len(a)==4 for a in sequences)
 # Each part repeats its four-chord sentence with 2 variations, giving 8 measures.
 bars=[c for seq in sequences for c in seq+seq]
 assert len(bars)==32
 tonic_pc=NOTE_PC[key]
 pieces={'melody':[],'bass':[],'harmony':[],'countermelody':[]}
 harmonic=[];review=[]
 for bar,symbol in enumerate(bars):
  info=chord_info(symbol);harmonic.append({'bar':bar+1,'symbol':symbol,'pc':info['pitch_classes'],'analysis_status':'not_expert_reviewed'})
  sec=bar//8
  pcs=melody_pattern(tonic_pc,mode,bar,bar//4,sec)
  durations=[1]*meter
  if meter==3: pcs=pcs[:3]
  for j,(pc,dur) in enumerate(zip(pcs,durations)):
   pitch=pitch_from_pc(pc,72 if mode!='minor' else 69)
   if sec==2: pitch+=0 if pitch<=81 else -12
   pieces['melody'].append({'onset_beats':bar*meter+j,'duration_beats':dur,'pitch':pitch,'bar':bar+1,'role':'melody'})
  strong=pcs[0]
  if strong not in info['pitch_classes']:
   review.append({'bar':bar+1,'issue':'strong_beat_melody_not_chord_tone','pitch_class':strong,'note':'May be intentional tension; review resolution'})
  bp=NOTE_PC[info['bass']]
  bassnote=pitch_from_pc(bp,36 if bp in [0,1,2,3] else 35)
  # A bass note sustained through the bar
  pieces['bass'].append({'onset_beats':bar*meter,'duration_beats':meter,'pitch':bassnote,'bar':bar+1,'role':'bass'})
  chordpcs=info['pitch_classes']
  mid=[pitch_from_pc(pc,55) for pc in chordpcs[:3]]
  for pitch in mid:
   pieces['harmony'].append({'onset_beats':bar*meter,'duration_beats':meter,'pitch':pitch,'bar':bar+1,'role':'harmony'})
  counterpc=chordpcs[-1]
  cp=pitch_from_pc(counterpc,64)
  if meter==4:
   pieces['countermelody'] += [
     {'onset_beats':bar*meter,'duration_beats':2,'pitch':cp,'bar':bar+1,'role':'countermelody'},
     {'onset_beats':bar*meter+2,'duration_beats':2,'pitch':pitch_from_pc(chordpcs[0],64),'bar':bar+1,'role':'countermelody'}]
  else:
   pieces['countermelody'] += [
     {'onset_beats':bar*meter,'duration_beats':1,'pitch':cp,'bar':bar+1,'role':'countermelody'},
     {'onset_beats':bar*meter+1,'duration_beats':2,'pitch':pitch_from_pc(chordpcs[0],64),'bar':bar+1,'role':'countermelody'}]
 data={'id':wid,'title':title,'composed_as':'original_algorithmically_elaborated_pedagogical_study','status':'technical_validation_only','human_musical_review':'not_performed','musical_intent':intent,'analysis_lens':lens,'key':key,'mode':mode,'tempo_bpm':bpm,'meter':f'{meter}/4','total_bars':32,'sections':[{'id':i,'label':['A','A_prime','B','Coda'][i],'first_bar':i*8+1,'last_bar':(i+1)*8,'compositional_role':['establish material','variation and continuation','contrast/expansion','return or departure'][i]} for i in range(4)],'chords':harmonic,'voices':pieces,'review_findings':review,'rights':'original_generated_in_this_project_no_third_party_composition','source_evidence':[]}
 (ROOT/'Partituren'/f'{wid}.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf8')
 # Generate SMF MIDI with precise ticks and 4 separate tracks
 midifile=mido.MidiFile(ticks_per_beat=480)
 for track_index,(part,events) in enumerate(pieces.items()):
  track=mido.MidiTrack();midifile.tracks.append(track)
  track.append(mido.MetaMessage('track_name',name=part,time=0))
  if track_index==0: track.append(mido.MetaMessage('set_tempo',tempo=mido.bpm2tempo(bpm),time=0))
  messages=[]
  for e in events:
   on=int(e['onset_beats']*480);off=int((e['onset_beats']+e['duration_beats'])*480)
   messages += [(on,1,e['pitch']),(off,0,e['pitch'])]
  last=0
  for tick,on,pitch in sorted(messages,key=lambda x:(x[0],x[1],x[2])):
   track.append(mido.Message('note_on' if on else 'note_off',channel=track_index,note=pitch,velocity=75 if on else 0,time=tick-last));last=tick
  track.append(mido.MetaMessage('end_of_track',time=0))
 midifile.save(ROOT/'MIDI'/f'{wid}.mid')
 # MusicXML score-partwise: each part has one measure for each bar, with rudimentary notation; preserves notes, not analytical enharmonic spelling.
 score=ET.Element('score-partwise',{'version':'4.0'});wl=ET.SubElement(score,'work');ET.SubElement(wl,'work-title').text=title
 partlist=ET.SubElement(score,'part-list')
 for i,part in enumerate(pieces,1):
  p=ET.SubElement(partlist,'score-part',{'id':f'P{i}'});ET.SubElement(p,'part-name').text=part
 for i,(part,events) in enumerate(pieces.items(),1):
  p=ET.SubElement(score,'part',{'id':f'P{i}'})
  for bar in range(1,33):
   mes=ET.SubElement(p,'measure',{'number':str(bar)})
   if bar==1:
    attrs=ET.SubElement(mes,'attributes');ET.SubElement(attrs,'divisions').text='480'
    tm=ET.SubElement(attrs,'time');ET.SubElement(tm,'beats').text=str(meter);ET.SubElement(tm,'beat-type').text='4'
    cl=ET.SubElement(attrs,'clef');ET.SubElement(cl,'sign').text='F' if part=='bass' else 'G';ET.SubElement(cl,'line').text='4' if part=='bass' else '2'
   if i==1:
    direction=ET.SubElement(mes,'direction');dt=ET.SubElement(direction,'direction-type');ET.SubElement(dt,'words').text=bars[bar-1]
   es=[e for e in events if e['bar']==bar]
   if part=='harmony':
    # chord notes are simultaneous, not sequenced
    for idx,e in enumerate(es):
     note=ET.SubElement(mes,'note')
     if idx>0:ET.SubElement(note,'chord')
     pi=ET.SubElement(note,'pitch');st,alt,octv=midinote_name(e['pitch']);ET.SubElement(pi,'step').text=st
     if alt: ET.SubElement(pi,'alter').text=str(alt)
     ET.SubElement(pi,'octave').text=str(octv);ET.SubElement(note,'duration').text=str(meter*480)
     ET.SubElement(note,'type').text='whole' if meter==4 else 'half'
     if meter==3:ET.SubElement(note,'dot')
   else:
    for e in es:
     note=ET.SubElement(mes,'note');pi=ET.SubElement(note,'pitch');st,alt,octv=midinote_name(e['pitch']);ET.SubElement(pi,'step').text=st
     if alt: ET.SubElement(pi,'alter').text=str(alt)
     ET.SubElement(pi,'octave').text=str(octv);ET.SubElement(note,'duration').text=str(e['duration_beats']*480)
     ET.SubElement(note,'type').text={1:'quarter',2:'half',3:'half',4:'whole'}[e['duration_beats']]
     if e['duration_beats']==3: ET.SubElement(note,'dot')
 ET.ElementTree(score).write(ROOT/'Partituren'/f'{wid}.musicxml',encoding='utf-8',xml_declaration=True)
 # Individual study note with facts/limitations
 lines=[f'# {wid} – {title}', '',f'**Originale, generativ ausgearbeitete Lehrstudie; kein extern begutachtetes Kompositionswerk.**', '',f'- Tonales/Modales Zentrum: {key} {mode}; analytische Perspektive: {lens}.',f'- Takt/Metrum: {meter}/4, BPM: {bpm}, 32 Takte, vier Stimmen.',f'- Kompositorisches Ziel: {intent}.',f'- Material A (T1–8): {seg1}, wiederholt mit motivisch alternierendem Verlauf.',f'- A’ (T9–16): {seg2}, transformierte Melodie.',f'- B (T17–24): {seg3}, Kontrast, rückläufige Motivfolge.',f'- Coda (T25–32): {seg4}, Rückkehr/Abschluss.','', '## Was sich im MIDI überprüfen lässt','', 'Alle Note-Events, Zeitkoordinaten, Stimmen und Akkordsymbole sind in JSON hinterlegt; die vierstimmige MIDI-Datei ist spielbar. Das MusicXML ist ein einfaches maschinenlesbares Notationsderivat, ohne ausgearbeitete Dynamik/Artikulation und ohne Anspruch auf fehlerfreie instrumentengerechte enharmonische Darstellung.','', '## Offene musikalische Fragen','',f'- {len(review)} starker Melodieeinsatz/Chord-Tone-Fälle benötigen potenziell bewusste Non-Chord-Tone-Klärung; die entsprechenden Takte sind im JSON markiert.', '- Auflösung, Motivkohärenz, harmonisches Stilurteil und Spielbarkeit wurden nicht durch unabhängige Musiker geprüft.', '- Die Notenschreibung muss bei repräsentativer Partiturlektüre und ggf. Spelling-Refinement geprüft werden.', '- Der Algorithmus generiert variable Konturen und Formabschnitte, ersetzt jedoch kein manuelles kompositorisches Finetuning.','', '## Dateien', '',f'- `{wid}.json` (vollständige Noten und Quellenstatus)',f'- `{wid}.musicxml` (einfache Partitur)',f'- `{wid}.mid` (MIDI Type 1, 4 Tracks)']
 (ROOT/'Partituren'/f'{wid}.md').write_text('\n'.join(lines)+'\n',encoding='utf8')
 works.append({'id':wid,'title':title,'meter':f'{meter}/4','bars':32,'mode':mode,'lens':lens,'melody_not_chord_tone_count':len(review),'status':'mechanical_review_pending'})
(ROOT/'STUDIENREGISTER_V5.json').write_text(json.dumps(works,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'README.md').write_text('# Originales STEPS-Kompositionslabor V5\n\n16 neue generativ ausgearbeitete Lehrstudien zu je 32 Takten, mit vier getrennten Stimmen und MIDI/MusicXML/JSON. Das sind keine 16 professionell komponierten, unabhängig fachgeprüften Stücke; Anzahl und Track-Parsebarkeit sind keine ästhetische Qualitätsprüfung.\n\nJeder JSON-Datensatz dokumentiert die bewusst offen gelassenen melodischen Non-Chord-Tone-Fälle. V4 mit 30 separaten 16-Takt-MIDI-Studien ist im Archiv erhalten.\n',encoding='utf8')
print(f'Created {len(works)} original 32-bar 4-part study scores')

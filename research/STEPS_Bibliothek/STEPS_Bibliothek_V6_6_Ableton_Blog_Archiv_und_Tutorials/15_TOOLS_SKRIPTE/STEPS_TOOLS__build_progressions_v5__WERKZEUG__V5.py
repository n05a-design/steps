"""Original pedagogical progression families, with transposition generated deterministically.
Not corpus observations, not genre frequency claims, and not expert-approved analyses.
"""
import json,pathlib,re
ROOT=pathlib.Path(__file__).resolve().parent
NOTES='C D E F G A B'.split();PC={'C':0,'D':2,'E':4,'F':5,'G':7,'A':9,'B':11}
KEYS=['C','G','D','A','E','B','F#','Gb','Db','Ab','Eb','Bb','F']
T=(
'functional|I ii V7 I|preparatory and dominant return|common_practice|Cadence requires phrase boundary',
'functional|I vi ii V7|tonic prolongation and pre-dominant preparation|common_practice|No formal cadence until return',
'functional|I IV V7 I|two dominant-region preparations|common_practice|Not all IV-V-I turns are phrase closure',
'functional|I IV I V7|open ending on dominant|common_practice|Cadential context uncertain',
'functional|I iii vi V7|mediant and relative-minor motion|common_practice|iii may be linear prolongation',
'functional|IV I V7 I|plagal-colored preface to authentic goal|common_practice|Not a universal cadence schema',
'functional|I V7 vi IV|deceptive target followed by IV|common_practice|vi is not always deceptive in a loop',
'functional|I ii V7 vi|deceptive cadence attempt|common_practice|Requires phrase context',
'functional|vi ii V7 I|departure from relative minor toward tonic|common_practice|vi opening may imply another center',
'functional|I V7/V V7 I|applied dominant chain|common_practice|Tonicization is not sustained modulation',
'functional|I V7/ii ii V7|dominant to pre-dominant preparation|common_practice|Next I not guaranteed',
'functional|I V7/vi vi IV|temporary tonicization of relative minor|common_practice|May be genre loop',
'functional|I IV V7/vi vi|applied dominant to submediant|common_practice|One applied chord is not modulation',
'functional|I I7 IV iv|pivot to IV then borrowed minor IV|common_practice|I7 can be V/IV, but may also be blues',
'functional|I IV iv I|minor subdominant and return|common_practice|Mood not determined',
'functional|I IVmaj7 iv6 I|chromatic voice-leading on parallel subdominant|common_practice|Voicing and tone spelling matter',
'pop_rock|I V vi IV|four-chord loop axis family|pop_rock|Rotation changes formal salience',
'pop_rock|vi IV I V|rotation with vi first|pop_rock|Tonal center ambiguous',
'pop_rock|IV I V vi|rotation with IV first|pop_rock|I not necessarily strongest chord',
'pop_rock|I bVII IV I|mixolydian-adjacent loop|pop_rock|Modal center requires more than chord roots',
'pop_rock|I bVI bVII I|chromatic pop turnaround|pop_rock|bVI and bVII not universal functions',
'pop_rock|vi bVII I IV|stepwise/root-chain color|pop_rock|Root naming relative to major key',
'pop_rock|vi IV V V|tonic may be emergent rather than present|pop_rock|Do not invent I',
'pop_rock|ii IV V V|prechorus rising function|pop_rock|Only form context supports prechorus claim',
'pop_rock|I bIII IV I|rock major-third mixture|pop_rock|Melody may imply another tonic',
'pop_rock|I iv bVII IV|mixed major-minor modal palette|pop_rock|No fixed classical functional path',
'blues|I7 IV7 I7 V7|blues-root chord family|blues|One-takt compression of blues color, not full 12-bar form',
'blues|I7 I7 IV7 I7|blues tonic and IV color|blues|I7 is not automatically secondary dominant',
'blues|IV7 I7 V7 IV7|blues approach to turnaround|blues|Needs actual 12-bar context to label form',
'jazz|ii7 V7 Imaj7 Imaj7|jazz ii-V-I tonic extension|jazz|Voicing not specified',
'jazz|Imaj7 VI7 ii7 V7|extended jazz turnaround|jazz|VI7 functions applied to ii under conditions',
'jazz|iii7 VI7 ii7 V7|cycle of applied dominants|jazz|iii may have modal reinterpretation',
'jazz|ii7 bII7 Imaj7 Imaj7|tritone substitution into I|jazz|Guide tones not identical in spelling',
'jazz|iv7 bVII7 Imaj7 Imaj7|backdoor approach to I|jazz|Borrowed iv and bVII7 are style-lensed',
'jazz|Imaj7 V7/vi vi7 V7/V|chain of local goals|jazz|Local tonicization does not equal modulation',
'jazz|Imaj9 VI7 ii9 V13|extended ninth/thirteenth cycle|jazz|Voicings and omission semantics essential',
'jazz|IVmaj7 bVII7 Imaj7 V7|modal/jazz coloration|jazz|bVII7 can be backdoor; context needed',
'jazz|vi7 V7/ii ii7 V7|minor-start turnaround|jazz|Functional claim is style-dependent',
'jazz|ii7 V7/vi vi7 V7|off-tonic arrival|jazz|Additional form needed to establish vi',
'chromatic|I bVI bIII bVII|chromatic roots and modal mixture|transformational|Avoid forcing tonic-dominant hierarchy',
'chromatic|I bIII bVI I|chromatic mediant sequence|transformational|Common tone motion needs voicing',
'chromatic|I bVI IV iv|two-color contrasting mixture|transformational|May be interpreted multiple ways',
'chromatic|I III7 vi iv|applied triadic color and borrowed iv|transformational|III7 may act V7/vi',
'chromatic|I bII7 Imaj7 I|bII dominant color resolves to tonic|transformational|bII7 not universally tritone sub',
'chromatic|I iv bVI V7|chromatic predominant coloration|transformational|Voicing crucial for functional reading',
'chromatic|I bIII bVII IV|chromatic-mediant and modal descent|transformational|No universal genre/quality claim',
'chromatic|I bVI I bVII|back-and-forth remote color|transformational|Tempo and context can dominate perception',
'composing|I Imaj7 IVmaj7 iv|textural color before cadence|composition|Need phrase finish to call closure',
'composing|I vi ii V7|presentation with consequent option|composition|Takt count alone not sentence',
'composing|I V7/vi vi IV|foreground relative minor contrast|composition|Part writing must be evaluated',
'composing|I bVII IV I|ostinato with held melody tonic|composition|Mode claims require bass/melody',
'composing|Imaj7 IVmaj7 ii7 V7|lyrical four-bar melodic setting|composition|Strong melody notes may be tensions',
'composing|vi7 ii7 V7 Imaj7|melody goal delayed to fourth harmony|composition|Goal must be heard, not assumed',
)
FAMILIES=[]
for i,line in enumerate(T,1):
 category,seq,mechanism,lens,caveat=line.split('|'); tokens=seq.split()
 FAMILIES.append({'id':f'V5-FAM-{i:03d}','category':category,'degree_tokens':tokens,'design_mechanism':mechanism,'primary_lens':lens,'uncertainty_or_counterexample':caveat,'provenance':'original_pedagogical_design','expert_review_status':'pending'})
assert len(FAMILIES)>=50

def parse_note(s):
 m=re.fullmatch(r'([A-G])([#b]{0,2})',s);assert m,s
 return (PC[m.group(1)]+m.group(2).count('#')-m.group(2).count('b'))%12

def spell(letter,pc):
 diff=(pc-PC[letter])%12
 if diff>6:diff-=12
 assert -2<=diff<=2,(letter,pc,diff)
 return letter + ('#'*diff if diff>0 else 'b'*(-diff))

def maj_scale(key):
 rt,acc=key[0],key[1:];start=NOTES.index(rt);tonic=parse_note(key)
 ints=[0,2,4,5,7,9,11]
 return [spell(NOTES[(start+i)%7],(tonic+ints[i])%12) for i in range(7)]

# token -> root degree index, semitone change to scale degree, chord suffix and normalized analysis label
DEFS={'I':(1,0,''),'ii':(2,0,'m'),'iii':(3,0,'m'),'IV':(4,0,''),'V':(5,0,''),'vi':(6,0,'m'),'vii°':(7,0,'dim'),
 'bVII':(7,-1,''),'bVI':(6,-1,''),'bIII':(3,-1,''),'iv':(4,0,'m'), 'I7':(1,0,'7'),'IV7':(4,0,'7'),'V7':(5,0,'7'),
 'bVII7':(7,-1,'7'),'bII7':(2,-1,'7'),'V7/ii':(6,0,'7'),'V7/vi':(3,0,'7'),'V7/V':(2,0,'7'),
 'V7/IV':(1,0,'7'),'III7':(3,0,'7'),'VI7':(6,0,'7'),'Imaj7':(1,0,'maj7'),'IVmaj7':(4,0,'maj7'),
 'Imaj9':(1,0,'maj9'),'ii7':(2,0,'m7'),'iii7':(3,0,'m7'),'vi7':(6,0,'m7'),'iv7':(4,0,'m7'),
 'ii9':(2,0,'m9'),'V13':(5,0,'13'),'iv6':(4,0,'m6')}
assert all(t in DEFS for f in FAMILIES for t in f['degree_tokens']),sorted({t for f in FAMILIES for t in f['degree_tokens'] if t not in DEFS})

def chord_notes(root,qual):
  intervals,steps={'':([0,4,7],[0,2,4]),'m':([0,3,7],[0,2,4]),'dim':([0,3,6],[0,2,4]),'7':([0,4,7,10],[0,2,4,6]),'maj7':([0,4,7,11],[0,2,4,6]),'m7':([0,3,7,10],[0,2,4,6]),'m6':([0,3,7,9],[0,2,4,5]),'m9':([0,3,7,10,2],[0,2,4,6,1]),'maj9':([0,4,7,11,2],[0,2,4,6,1]),'13':([0,4,7,10,2,9],[0,2,4,6,1,5])}[qual]
  r_pc=parse_note(root);j=NOTES.index(root[0]);return [spell(NOTES[(j+letterstep)%7],(r_pc+offset)%12) for offset,letterstep in zip(intervals,steps)]

records=[]
for key in KEYS:
  scale=maj_scale(key)
  for f in FAMILIES:
    chords=[]
    for tok in f['degree_tokens']:
      degree,shift,qual=DEFS[tok];orig=scale[degree-1]
      root=spell(orig[0],(parse_note(orig)+shift)%12)
      symbol=root+qual;notes=chord_notes(root,qual)
      chords.append({'degree_token':tok,'symbol':symbol,'root_spelling':root,'chord_tones_spelled':notes,'pitch_classes':[parse_note(x) for x in notes]})
    for variant,durations in [('steady',[4]*len(chords)),('syncopated',[6,2,4,4] if len(chords)==4 else [4]*len(chords))]:
      pos=0;events=[]
      for ch,dur in zip(chords,durations):
        events.append({**ch,'onset_beat':pos,'duration_beats':dur});pos+=dur
      rec={'id':f"{f['id']}-{key.replace('#','s').replace('b','f')}-{variant}", 'family_id':f['id'],'type':'algorithmic_transposition_and_duration_variant','key':key,'major_scale_spelling':scale,'style_lens':f['primary_lens'],'category':f['category'],'mechanism':f['design_mechanism'],'caveat':f['uncertainty_or_counterexample'],'events':events,'total_beats':pos,'origin':'generated_from_original_v5_family','review_status':'technical_only','genre_frequency_claim':None}
      records.append(rec)
(ROOT/'KURATIERTE_PROGRESSIONSFAMILIEN_V5.json').write_text(json.dumps(FAMILIES,ensure_ascii=False,indent=2),encoding='utf8')
(ROOT/'TRANSPONIERTE_PROGRESSIONSVARIANTEN_V5.json').write_text(json.dumps(records,ensure_ascii=False,indent=2),encoding='utf8')
# An accessible readable reference with one exemplar per family
s=['# V5 Progressionsatlas – kuratierte Familien und algorithmische Varianten','',f'**{len(FAMILIES)} eigenständig definierte didaktische Progressionsfamilien; {len(records)} algorithmische Key-/Timingvarianten in 13 verschiedenen geschriebenen Durtonarten (einschließlich enharmonischem F# vs. Gb).**','', 'Die Varianten sind **keine** jeweils eigenständig empirisch erforschten oder gehörgeprüften Songs. Source-Claims in fremden Werken werden hier nicht vorgetäuscht. Alle Ton-/Akkordbuchstabierungen werden durch den lokalen Generator und eine eigene strukturelle Test-Suite geprüft.','']
for f in FAMILIES:
 example=next(r for r in records if r['family_id']==f['id'] and r['key']=='C' and r['id'].endswith('-steady'))
 s.extend([f"## {f['id']} – {f['category']} · {f['primary_lens']}", '', f"**Stufen:** {' – '.join(f['degree_tokens'])}",f"**Konkretes Beispiel in C:** {' – '.join(x['symbol'] for x in example['events'])}", f"**Erklärung / kompositorische Absicht:** {f['design_mechanism']}",f"**Grenzfall:** {f['uncertainty_or_counterexample']}", '**Konkreter Nutzungsschritt:** Tonart/Style-Lens auswählen, Stimmführung und Melodie ergänzen, Harmonic-Rhythm-Varianten vergleichen; musikalischen Geltungsbereich vor Freigabe prüfen.',''])
(ROOT/'ATLAS_V5.md').write_text('\n'.join(s),encoding='utf8')
print('Progression families',len(FAMILIES),'mechanically generated written variants',len(records))

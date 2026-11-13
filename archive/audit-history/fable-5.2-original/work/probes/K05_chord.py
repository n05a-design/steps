# K05/K06: Sollwerte aus Lead-Sheet-Konvention (Terzschichtung, Halbtöne ab Grundton), unabhängig vom STEPS-Code notiert
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from src.steps.theory.chord import CHORD_TEMPLATES, parse_chord as PC
REF = {'':(0,4,7),'m':(0,3,7),'dim':(0,3,6),'aug':(0,4,8),'sus4':(0,5,7),'sus2':(0,2,7),'add9':(0,4,7,14),
 '6':(0,4,7,9),'m6':(0,3,7,9),'7':(0,4,7,10),'maj7':(0,4,7,11),'m7':(0,3,7,10),'m7b5':(0,3,6,10),'dim7':(0,3,6,9),
 'm(maj7)':(0,3,7,11),'7#5':(0,4,8,10),'maj7#5':(0,4,8,11),'7sus4':(0,5,7,10),'9':(0,4,7,10,14),'maj9':(0,4,7,11,14),
 'm9':(0,3,7,10,14),'7b9':(0,4,7,10,13),'7#9':(0,4,7,10,15),'7#11':(0,4,7,10,18),'7b5':(0,4,6,10),'7b13':(0,4,7,10,20),
 '13':(0,4,7,10,14,21),'maj13':(0,4,7,11,14,21),'m11':(0,3,7,10,14,17)}
chk("K05","Templatemenge = 29 unabhängige Rezepte",sorted(REF),lambda: sorted(CHORD_TEMPLATES))
chk("K05","Tonklassenmengen aller Templates",[],lambda: [k for k in REF if {x%12 for x in REF[k]}!={x%12 for x in CHORD_TEMPLATES[k]['theoretical']}])
chk("K05","Exakte Intervalltupel (Erweiterungen >12)",[],lambda: [(k,CHORD_TEMPLATES[k]['theoretical']) for k in REF if tuple(sorted(REF[k]))!=tuple(sorted(CHORD_TEMPLATES[k]['theoretical']))],"Darstellung der 9/#11 als 2/6 statt 14/18")
chk("K05","voiced ist Teilmenge von theoretical",[],lambda: [k for k,t in CHORD_TEMPLATES.items() if not set(t['voiced'])<=set(t['theoretical'])])
def q(sym,conv='AUTO'):
    c=PC(sym,conv); return (int(c.root.pitch_class), c.quality, None if c.bass is None else int(c.bass.pitch_class))
cases = [
 ("INT","CM7",(0,'maj7',None)),("INT","Cm7",(0,'m7',None)),("INT","CMaj7",(0,'maj7',None)),("INT","CMAJ7",(0,'maj7',None)),
 ("INT","CMIN7",(0,'m7',None)),("INT","C-7",(0,'m7',None)),("INT","CΔ7",(0,'maj7',None)),("INT","C°7",(0,'dim7',None)),
 ("INT","Cø7",(0,'m7b5',None)),("INT","C+",(0,'aug',None)),("INT","Csus",(0,'sus4',None)),("INT","CM",(0,'',None)),("INT","Cm",(0,'m',None)),
 ("INT","C7(b9)",(0,'7b9',None)),("INT","C7(#11)",(0,'7#11',None)),("INT","Cm(maj7)",(0,'m(maj7)',None)),("INT","C7+",(0,'7#5',None)),
 ("INT","C11","ERR"),("INT","C5","ERR"),("INT","C7alt","ERR"),("INT","Cmaj7#11","ERR"),("INT","Cmi7","ERR"),("INT","CM7b5","ERR"),
 ("INT","C69","ERR"),("INT","C2","ERR"),("INT","C7b9#11","ERR"),("INT","C7(b9","ERR"),("INT","C()","ERR"),("INT","X7","ERR"),("INT","","ERR"),
 ("INT","CMmaj7","ERR"),("INT","CMMAJ7","ERR"),
 ("INT","Bm7",(11,'m7',None)),("DE","Bm7",(10,'m7',None)),("INT","Bb",(10,'',None)),("DE","Bb","ERR"),("DE","Hm7",(11,'m7',None)),
 ("INT","Hm7","ERR"),("AUTO","Hm7",(11,'m7',None)),("AUTO","Bm7","ERR"),
 ("AUTO","Esus4",(4,'sus4',None)),("DE","Esus4",(4,'sus4',None)),("AUTO","Asus2",(9,'sus2',None)),("DE","Asus2",(9,'sus2',None)),
 ("DE","As7",(8,'7',None)),("INT","As7","ERR"),("AUTO","As7",(8,'7',None)),("DE","Assus4",(8,'sus4',None)),
 ("DE","Es",(3,'',None)),("AUTO","Es",(3,'',None)),("AUTO","Fis",(6,'',None)),("AUTO","Des",(1,'',None)),("AUTO","Fism",(6,'m',None)),
 ("AUTO","Es7",(3,'7',None)),("DE","Esmaj7/B",(3,'maj7',10)),("AUTO","Esmaj7/B",(3,'maj7',10)),("AUTO","Hm7/B","ERR"),
 ("DE","Bis7","ERR"),("DE","Bes7","ERR"),("DE","Eb7","ERR"),("DE","F#m","ERR"),
 ("INT","C/B",(0,'',11)),("INT","C/E",(0,'',4)),("INT","C/Bb",(0,'',10)),("INT","C/D",(0,'',2)),("INT","Dm7/G",(2,'m7',7)),
 ("INT","C/","ERR"),("INT","/E","ERR"),("INT","C/E/G","ERR"),("INT","C/E5","ERR"),("INT","C/X","ERR"),
 ("INT","Dbmaj7",(1,'maj7',None)),("INT","F#m7b5",(6,'m7b5',None)),("INT","Bbb7",(9,'7',None)),("INT","Cbmaj7",(11,'maj7',None)),
 ("INT","B♭maj7",(10,'maj7',None)),("INT","c","ERR"),("INT","bb","ERR"),("INT","C maj7","ERR"),
]
for conv,sym,exp in cases:
    note = {"Bm7":"AUTO mehrdeutig: INT B-Moll7 oder DE B(=Bb)-Moll7","c":"Kleinbuchstabe als Grundton unüblich","bb":"Kleinbuchstaben","C maj7":"Leerzeichen im Symbol","Hm7/B":"H und B im selben Symbol: Bass INT-B oder DE-B?"}.get(sym,"") if conv in("AUTO","INT") else ""
    chk("K05",f"{conv} {sym!r}",exp,lambda s=sym,c=conv: q(s,c),note)
def rt():
    bad=[]
    for r in ("C","F#","Bb","Cb"):
        for k in CHORD_TEMPLATES:
            s=PC(r+k,'INT').symbol
            try:
                if PC(s,'INT')!=PC(r+k,'INT'): bad.append(s)
            except Exception: bad.append(s)
    return bad
chk("K05","symbol-Round-Trip 4 Grundtöne x 29 Qualitäten",[],rt)
chk("K05","parse_chord(None) Domänenfehler","ERR:ChordConstructionError",lambda: PC(None))
chk("K05","Root-Schreibweise Cb bleibt C mit b",('C',-1),lambda: (PC('Cbmaj7','INT').root.step,PC('Cbmaj7','INT').root.alteration))
# K06 Voicings
v = lambda s,t='CLOSE',o=3: PC(s,'INT').to_voicing(o,t).notes
chk("K06","C CLOSE",(48,52,55),lambda: v('C'))
chk("K06","Cmaj7 CLOSE",(48,52,55,59),lambda: v('Cmaj7'))
chk("K06","C/E CLOSE",(52,55,60),lambda: v('C/E'))
chk("K06","C/G CLOSE",(55,60,64),lambda: v('C/G'))
chk("K06","Cmaj7/B CLOSE",(59,60,64,67),lambda: v('Cmaj7/B'))
chk("K06","C/D CLOSE Bass D + alle Akkordtöne",(50,[0,4,7]),lambda: (min(v('C/D')),sorted({n%12 for n in v('C/D')}-{2})))
chk("K06","C9 CLOSE (ohne Quinte)",(48,52,58,62),lambda: v('C9'))
chk("K06","Cmaj7 DROP2 = Close mit 2. Stimme von oben -12",(43,48,52,59),lambda: v('Cmaj7','DROP2'))
chk("K06","Dm7 DROP2",(45,50,53,60),lambda: v('Dm7','DROP2'))
chk("K06","C DROP2 (Dreiklang) abweisen oder kennzeichnen","ERR",lambda: PC('C','INT').to_voicing(3,'DROP2').voicing_type,"Drop-2 braucht 4 Stimmen")
chk("K06","C13 DROP2 enthält die 13",True,lambda: 9 in {n%12 for n in v('C13','DROP2')})
chk("K06","Cmaj7/E DROP2: Bass E, 4 verschiedene Tonklassen",(4,4),lambda: (min(v('Cmaj7/E','DROP2'))%12,len({n%12 for n in v('Cmaj7/E','DROP2')})))
chk("K06","C7 SHELL = Grundton, Terz, Septime",[0,4,10],lambda: sorted({n%12 for n in v('C7','SHELL')}))
chk("K06","Dm7 SHELL",[0,2,5],lambda: sorted({n%12 for n in v('Dm7','SHELL')}))
chk("K06","C6 SHELL = Grundton, Terz, Sexte",[0,4,9],lambda: sorted({n%12 for n in v('C6','SHELL')}),"Sexte ersetzt die Septime")
chk("K06","Cadd9 SHELL enthält Terz, nicht nur None",True,lambda: 4 in {n%12 for n in v('Cadd9','SHELL')})
chk("K06","C9 ROOTLESS ohne Grundton",[2,4,10],lambda: sorted({n%12 for n in v('C9','ROOTLESS')}))
chk("K06","ROOTLESS beachtet bass_octave",True,lambda: v('C9','ROOTLESS',2)!=v('C9','ROOTLESS',5),"Parameter wird laut Signatur angenommen")
chk("K06","C7/C ROOTLESS enthält keinen Grundton",False,lambda: 0 in {n%12 for n in v('C7/C','ROOTLESS')})
chk("K06","keine Duplikate in allen CLOSE-Voicings",[],lambda: [k for k in CHORD_TEMPLATES if len(set(v('C'+k)))!=len(v('C'+k))])
chk("K06","Oktave 9 für G ausserhalb MIDI","ERR",lambda: v('G','CLOSE',9))
chk("K06","bass_octave True","ERR",lambda: v('C','CLOSE',True))
chk("K06","Voicing-Typ 'OPEN' unbekannt","ERR",lambda: v('C','OPEN'))
chk("K06","Cmaj7 DROP2 Oktave -1","ERR",lambda: v('Cmaj7','DROP2',-1),"Drop unter MIDI 0")
summary()

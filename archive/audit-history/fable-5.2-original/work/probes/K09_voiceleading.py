# K04/K09/K10: Brute-Force-Gegenrechnung des Solvers; Definitionen Terzschichtung, Drop-2, Parallelen
import sys, itertools, random; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from src.steps.progression import *
from src.steps.progression.voice_leading import *
from src.steps.theory.triad import *
from src.steps.theory.seventh import *
from src.steps.theory import parse_chord
from src.steps.theory.chord import Voicing
def brute(src, target, bass=None):
    cands=[[n for n in range(max(0,c-12),min(127,c+12)+1) if n%12 in target and (i or bass is None or n%12==bass)] for i,c in enumerate(src)]
    best=None
    for combo in itertools.product(*cands):
        if any(b<=a for a,b in zip(combo,combo[1:])): continue
        if {n%12 for n in combo}!=set(target): continue
        d=sum(abs(a-b) for a,b in zip(src,combo))
        if best is None or d<best: best=d
    return best
def compare(n=250, seed=7):
    rnd=random.Random(seed); bad=[]
    for _ in range(n):
        k=rnd.choice((3,4)); src=sorted(rnd.sample(range(36,84),k)); tgt=set(rnd.sample(range(12),rnd.choice((2,3,min(k,4))))); bass=rnd.choice((None,rnd.choice(sorted(tgt))))
        exp=brute(src,tgt,bass)
        try: got=optimize_smooth_voice_leading(src,tgt,bass); gd=sum(abs(a-b) for a,b in zip(src,got))
        except VoiceLeadingError: gd=None
        if gd!=exp: bad.append((src,tgt,bass,exp,gd))
    return bad
chk("K09","Solver-Optimum == Brute-Force (250 Zufallsfälle, 3-4 Stimmen)",[],compare)
chk("K09","Determinismus: 2 Läufe gleich",True,lambda: optimize_smooth_voice_leading([48,55,60,64],{2,5,9,0})==optimize_smooth_voice_leading([48,55,60,64],{2,5,9,0}))
chk("K09","C->G mit Bass G: [43,55,59,62] oder gleich teuer (L1=15?) Brute-Force",brute([48,55,60,64],{7,11,2},7),lambda: sum(abs(a-b) for a,b in zip([48,55,60,64],optimize_smooth_voice_leading([48,55,60,64],{7,11,2},7))))
chk("K09","Ziel mit mehr Tonklassen als Stimmen","ERR",lambda: optimize_smooth_voice_leading([60,64],{0,4,7}))
chk("K09","Quelle nicht aufsteigend","ERR",lambda: optimize_smooth_voice_leading([64,60],{0,4}))
chk("K09","Quelle mit Einklang","ERR",lambda: optimize_smooth_voice_leading([60,60],{0,4}))
chk("K09","Tonklasse 12 (ausserhalb 0..11) abweisen","ERR",lambda: optimize_smooth_voice_leading([60],{12}),"Code reduziert mod 12")
chk("K09","leeres Ziel","ERR",lambda: optimize_smooth_voice_leading([60],set()))
chk("K09","STRICT: Quintparallele wird vermieden",[],lambda: detect_parallel_fifths_octaves([48,55],optimize_smooth_voice_leading([48,55],{2,9},style=VoiceLeadingStyle.STRICT_COUNTERPOINT)))
P=lambda a,b,s=VoiceLeadingStyle.STRICT_COUNTERPOINT: len(detect_parallel_fifths_octaves(a,b,s))
chk("K09","Quintparallele 60/67->62/69",1,lambda: P([60,67],[62,69]))
chk("K09","Oktavparallele 48/60->50/62",1,lambda: P([48,60],[50,62]))
chk("K09","Einklangsparallele 60/60->62/62",1,lambda: P([60,60],[62,62]))
chk("K09","Quartparallele nicht gemeldet",0,lambda: P([60,65],[62,67]))
chk("K09","liegende Quinte (keine Bewegung) nicht gemeldet",0,lambda: P([60,67],[60,67]))
chk("K09","Seitenbewegung nicht gemeldet",0,lambda: P([60,67],[60,69]))
chk("K09","Antiparallele Quinte->Duodezime in Gegenbewegung (48/67 -> 55/62) im strengen Satz gemeldet",1,lambda: P([48,67],[55,62]),"Gegenbewegung von Quinte zu Quinte gilt im strengen Satz ebenfalls als fehlerhaft")
chk("K09","Antiparallele Oktave->Einklang (48/60 -> 55/55)",1,lambda: P([48,60],[55,55]))
chk("K09","v5->r5 (ungleiche Quinten 59/65->60/67) nicht gemeldet",0,lambda: P([59,65],[60,67]))
chk("K09","JAZZ_POP meldet laut Docstring 'acknowledged' -> mindestens Kennzeichnung",1,lambda: P([60,67],[62,69],VoiceLeadingStyle.JAZZ_POP),"Docstring: acknowledged but marked as non-violating")
chk("K09","detect_voice_overlap 60/64 -> 65/67 (Unterstimme über alte Oberstimme)",True,lambda: detect_voice_overlap([60,64],[65,67]))
chk("K09","detect_voice_crossing [60,60] (Einklang ist keine Kreuzung)",False,lambda: detect_voice_crossing([60,60]),"Docstring definiert >= als Kreuzung")
# K04
chk("K04","Dreiklänge Dur/Moll/vermindert/übermäßig",[[0,4,7],[0,3,7],[0,3,6],[0,4,8]],lambda: [[int(x) for x in construct_triad(0,q)] for q in (TriadQuality.MAJOR,TriadQuality.MINOR,TriadQuality.DIMINISHED,TriadQuality.AUGMENTED)])
chk("K04","ADD9 als 'Dreiklang' hat 3 Töne",3,lambda: len(construct_triad(0,TriadQuality.ADD9)),"add9 ist ein Vierklang")
chk("K04","G-Dur ab Grundton 7",[7,11,2],lambda: [int(x) for x in construct_triad(7,TriadQuality.MAJOR)])
chk("K04","1. Umkehrung C",[64,67,72],lambda: invert_triad_voicing([60,64,67],1))
chk("K04","2. Umkehrung C",[67,72,76],lambda: invert_triad_voicing([60,64,67],2))
chk("K04","Umkehrung 3 eines Dreiklangs abweisen","ERR",lambda: invert_triad_voicing([60,64,67],3),"Code: modulo -> Grundstellung")
chk("K04","Umkehrung -1 abweisen","ERR",lambda: invert_triad_voicing([60,64,67],-1))
chk("K04","Septakkorde 7/maj7/m7/ø/o7/mM7",[[0,4,7,10],[0,4,7,11],[0,3,7,10],[0,3,6,10],[0,3,6,9],[0,3,7,11]],lambda: [[int(x) for x in construct_seventh(0,q)] for q in list(SeventhQuality)[:6]])
chk("K04","3. Umkehrung G7 (F im Bass)",[65,67,71,74],lambda: invert_seventh_voicing([55,59,62,65],3))
chk("K04","Drop-2 Dm7 [65,69,72,74] -> [60,65,69,74]",[60,65,69,74],lambda: make_drop2_voicing([65,69,72,74]))
chk("K04","Drop-2 mit 3 Stimmen","ERR",lambda: make_drop2_voicing([60,64,67]))
chk("K04","Drop-2 nicht-enge Lage (Spanne > Oktave) abweisen","ERR",lambda: make_drop2_voicing([48,60,72,84]),"Vorbedingung 'close position' wird nicht geprüft")
chk("K04","Shell C7 ab C3: (48,(64,70))",(48,(64,70)),lambda: make_shell_voicing(48,SeventhQuality.DOMINANT_SEVENTH))
chk("K04","Shell root_midi 200 abweisen","ERR",lambda: make_shell_voicing(200,SeventhQuality.DOMINANT_SEVENTH))
chk("K04","Lydisch-dominant theoretisch enthält #11 als 18",True,lambda: 18 in THEORETICAL_INTERVALS[SeventhQuality.LYDIAN_DOMINANT],"Darstellung als 6")
# K10
keys = lambda n: sorted(analyze_progression_voice_leading(generate_progression_voicings(get_progression('PROG-003'))[:n]).keys())
chk("K10","Rückgabeschlüssel für 0, 1, 2 Voicings identisch",True,lambda: keys(0)==keys(1)==keys(3))
print("   Schlüssel n=1:",keys(1)); print("   Schlüssel n=3:",keys(3))
chk("K10","leere Akkordliste -> []",[],lambda: generate_progression_voicings([]))
chk("K10","PROG-003 CLOSE Bässe 2,7,0",[2,7,0],lambda: [v.bass_note%12 for v in generate_progression_voicings(get_progression('PROG-003'))])
chk("K10","PROG-003 DROP2: Folgeakkorde behalten Typ DROP2 oder sind als CUSTOM gekennzeichnet",True,lambda: all(v.voicing_type in('DROP2','CUSTOM') for v in generate_progression_voicings(get_progression('PROG-003'),initial_voicing_type='DROP2')))
chk("K10","PROG-003 SHELL: Bässe = Grundtöne",[2,7,0],lambda: [v.bass_note%12 for v in generate_progression_voicings(get_progression('PROG-003'),initial_voicing_type='SHELL')])
chk("K10","PROG-003 ROOTLESS: kein Grundton in den Folgeakkorden",[False,False,False],lambda: [r in {n%12 for n in v.notes} for r,v in zip((2,7,0),generate_progression_voicings(get_progression('PROG-003'),initial_voicing_type='ROOTLESS'))])
chk("K10","Analyse erkennt Stimmkreuzung in unsortiertem Voicing",1,lambda: analyze_progression_voice_leading([Voicing((64,60,67)),Voicing((60,64,67))])['voice_crossings_count'],"midi_notes sortiert vor der Prüfung")
chk("K10","Analyse: Parallelen STRICT in C-Dm Parallelverschiebung",True,lambda: len(analyze_progression_voice_leading([Voicing((48,55,60,64)),Voicing((50,57,62,65))],VoiceLeadingStyle.STRICT_COUNTERPOINT)['parallel_violations'])>=2)
chk("K10","Analyse mit ungleicher Stimmenzahl","ERR",lambda: analyze_progression_voice_leading([Voicing((48,55,60)),Voicing((50,57,62,65))]))
for t in ('CLOSE','DROP2','SHELL','ROOTLESS'):
    try: print("   PROG-003",t,[ (v.notes,v.voicing_type) for v in generate_progression_voicings(get_progression('PROG-003'),initial_voicing_type=t)])
    except Exception as e: print("   PROG-003",t,"ERR",type(e).__name__,e)
summary()

# W08/D5 + K08 + K12: Sollwerte aus C-Dur-Skala und Akkorddefinitionen, nicht aus STEPS
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from app.knowledge import get_reviewed_progression as G, list_reviewed_progressions as L
import app.knowledge as AK
from src.steps.progression import get_progression, list_progressions, resolve_roman_degree as R
from src.steps.theory import parse_chord, parse_spelling
pcs = lambda ex: [sorted(c.pitch_class_set) for c in ex.progression.chord_definitions]
p3, p9 = G('PROG-003'), G('PROG-009')
chk("W08","PROG-003 Tonklassen Dm7 G7 Cmaj7",[[0,2,5,9],[2,5,7,11],[0,4,7,11]],lambda: pcs(p3))
chk("W08","PROG-003 Stufen->Akkorde (ii7 V7 Imaj7 in C)",["Dm7","G7","Cmaj7"],lambda: [R(d,'C',convention='INT').symbol for d in p3.progression.roman_numerals.split(' - ')])
chk("W08","PROG-003 Akkordspalte",["Dm7","G7","Cmaj7"],lambda: [c.symbol for c in p3.progression.chord_definitions])
chk("W08","PROG-003 Stimme C4->H3 (DE) = 60->59",[60,59],lambda: [parse_spelling(n,'DE').midi_number for _,n in p3.claims[2].claim.voice_path])
chk("W08","PROG-003 Stimme F4->E4 = 65->64",[65,64],lambda: [parse_spelling(n,'DE').midi_number for _,n in p3.claims[3].claim.voice_path])
chk("W08","PROG-003 Claims: Notation + 3",["PILOT-NOTATION-001","PROG-003-HARMONY","PROG-003-VOICE-II-V","PROG-003-VOICE-V-I"],lambda: [c.claim.claim_id for c in p3.claims])
chk("W08","PROG-003 Quellen der Ausgabe",("yale-key-names","omt-ii-v-i"),lambda: p3.source_ids)
chk("W08","PROG-003 Bestandskatalog nennt dieselbe Quelle wie Freigabe",True,lambda: set(get_progression('PROG-003').sources.split(', '))<=set(p3.source_ids))
chk("W08","PROG-003 Bestandskatalog == freigegebene Progression (ohne Quellenfeld)",True,lambda: (lambda a,b:(a.name,a.roman_numerals,a.default_key,a.chords_str,a.context)==(b.name,b.roman_numerals,b.default_key,b.chords_str,b.context))(get_progression('PROG-003'),p3.progression))
chk("W08","PROG-003 Lesson enthält alle 3 Claimtexte",True,lambda: all(c.claim.text in p3.lesson for c in p3.claims[1:]))
chk("W08","PROG-003 Transposition +1 behält Quintfall-Schreibweise (Ebm7 Ab7 Dbmaj7)",["Ebm7","Ab7","Dbmaj7"],lambda: [c.symbol for c in p3.progression.transpose(1)],"enharmonisch vertretbar: D#m7 G#7 C#maj7, aber nicht gemischt")
chk("W08","PROG-009 Tonklassen C F Fm C",[[0,4,7],[0,5,9],[0,5,8],[0,4,7]],lambda: pcs(p9))
chk("W08","PROG-009 Stufen->Akkorde",["C","F","Fm","C"],lambda: [R(d,'C',convention='INT').symbol for d in p9.progression.roman_numerals.split(' - ')])
chk("W08","PROG-009 Stimme A4->As4->G4 = 69,68,67",[69,68,67],lambda: [parse_spelling(n,'DE').midi_number for _,n in p9.claims[2].claim.voice_path])
chk("W08","PROG-009 Stimmtöne sind Akkordtöne (Terz F, Terz Fm, Quinte C)",[True,True,True],lambda: [parse_spelling(n,'DE').midi_number%12 in p9.progression.chord_definitions[i].pitch_class_set for i,n in p9.claims[2].claim.voice_path])
chk("W08","PROG-009 Quellen der Ausgabe",("yale-key-names","omt-blues-based-schemas"),lambda: p9.source_ids)
chk("W08","PROG-009 Bestandskatalog nennt dieselbe Quelle wie Freigabe",True,lambda: set(get_progression('PROG-009').sources.split(', '))<=set(p9.source_ids),"Bestand: "+get_progression('PROG-009').sources)
chk("W08","PROG-009 Transposition +8 (As-Dur): Ab Db Dbm Ab",["Ab","Db","Dbm","Ab"],lambda: [c.symbol for c in p9.progression.transpose(8)])
chk("W08","Fassungsbindung: catalog_version 64 hex, für alle gleich",True,lambda: len(p3.catalog_version)==64 and len({e.catalog_version for e in L()})==1)
chk("W08","reviewed_on",'2026-11-12',lambda: p9.reviewed_on)
chk("K12","Adapter exportiert genau 2 Namen",["get_reviewed_progression","list_reviewed_progressions"],lambda: sorted(AK.__all__))
chk("K12","Adapter liefert genau 3 Pilot-IDs",["PROG-001","PROG-003","PROG-009"],lambda: [e.progression.prog_id for e in L()])
chk("K12","nicht freigegebene ID PROG-002 -> Fehler","ERR",lambda: G('PROG-002'))
chk("K12","Kleinschreibung 'prog-003' wird aufgelöst","PROG-003",lambda: G('prog-003').progression.prog_id)
chk("K12","G(None) Domänenfehler","ERR:ProgressionParsingError",lambda: G(None))
# K08: alle 28 Bestandsprogressionen: Stufen gegen Akkordspalte
def k08():
    bad=[]
    for p in list_progressions():
        key=p.default_key; minor=key.endswith('m'); key=key[:-1] if minor else key
        for d,ch in zip(p.roman_numerals.split(' - '),p.chords_str.split(' - '),strict=True):
            try: got=R(d,key,minor,convention='INT').symbol
            except Exception as e: got='ERR:'+type(e).__name__
            if got!=parse_chord(ch,'INT').symbol: bad.append((p.prog_id,d,ch,got))
    return bad
chk("K08","28 PROG: resolve(roman) == Akkordspalte",[],k08)
STEPS='CDEFGAB'
def k08t():
    bad=[]
    for p in list_progressions():
        o=p.chord_definitions
        for s in range(12):
            t=p.transpose(s)
            for a,b,c,d in zip(o,o[1:],t,t[1:]):
                if (STEPS.index(b.root.step)-STEPS.index(a.root.step))%7 != (STEPS.index(d.root.step)-STEPS.index(c.root.step))%7:
                    bad.append((p.prog_id,s)); break
    return len(bad), bad[:6]
chk("K08","336 Transpositionen: Stufenabstand benachbarter Grundtöne bleibt erhalten",(0,[]),k08t,"Schreibweisen-Invarianz")
chk("K08","PROG-001 +8: Ab Eb Fm Db",["Ab","Eb","Fm","Db"],lambda: [c.symbol for c in get_progression('PROG-001').transpose(8)])
chk("K08","Transposition 0 ist Identität für alle 28",[],lambda: [p.prog_id for p in list_progressions() if p.transpose(0)!=p.chord_definitions])
chk("K08","Transposition +12 erhält Symbole",[],lambda: [p.prog_id for p in list_progressions() if [c.symbol for c in p.transpose(12)]!=[c.symbol for c in p.chord_definitions]])
summary()

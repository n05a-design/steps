# K07: Sollwerte aus Stufentabelle Dur (0,2,4,5,7,9,11) und natürlich Moll (0,2,3,5,7,8,10); Leitton bei vii°; V/x = Quinte über x
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from src.steps.progression import resolve_roman_degree as R
s = lambda d,k='C',m=False,c='AUTO': R(d,k,m,convention=c).symbol
MAJ = {"I":"C","ii":"Dm","iii":"Em","IV":"F","V":"G","vi":"Am","vii°":"Bdim","I7":"Cmaj7","ii7":"Dm7","iii7":"Em7","IV7":"Fmaj7",
 "V7":"G7","vi7":"Am7","viiø7":"Bm7b5","vii°7":"Bdim7","bVII":"Bb","bVII7":"Bb7","bIII":"Eb","bVI":"Ab","bII":"Db","#IV":"F#",
 "#iv°":"F#dim","iv":"Fm","iv7":"Fm7","v":"Gm","V/V":"D","V7/V":"D7","V7/ii":"A7","V7/vi":"E7","V7/IV":"C7","vii°/V":"F#dim",
 "vii°7/ii":"C#dim7","V7/bVI":"Eb7","V/V/V":"A","I6":"C/E","I64":"C/G","V65":"G7/B","V43":"G7/D","V42":"G7/F","V2":"G7/F",
 "ii65":"Dm7/F","vii°6":"Bdim/D","viiø65":"Bm7b5/D","V7(6/5)/V":"D7/F#","V6/5/V":"D7/F#","V6/V":"D/F#","V6/4":"G/D","♭VII":"Bb",
 "V^7(b9)":"G7(b9)","bII^7(#11)":"Db7(#11)","i^(maj7)":"Cm(maj7)","Idom7":"C7","im6":"Cm6","V7(alt)":"ERR","VIII":"ERR","iV":"ERR",
 "":"ERR","I/":"ERR","IV/IV":"ERR","ii/V":"ERR","V7 / V":"ERR","iadd9":"ERR","ii13":"ERR","IVm":"ERR","Vb5":"ERR","vii":"ERR","vii7":"ERR",
 "V7#11(42)":"G7(#11)/F","Iadd9(6)":"Cadd9/E","V7sus4(65)":"ERR","I+":"Caug"}
NOTE = {"iadd9":"Moll-Numeral + add9: Cm(add9) oder Fehler, nicht Dur","ii13":"m13 nicht registriert","IVm":"Widerspruch Groß/Qualität","Vb5":"Dur-b5 ist nicht vermindert",
 "vii":"vii ohne ° ergäbe leiterfremdes Bm; vertretbar: Bm zurückgeben","vii7":"dito Bm7","I7":"diatonische Lesart; Pop-Lesart C7 vertretbar","IV7":"diatonisch Fmaj7; Blues-Lesart F7 vertretbar",
 "V7sus4(65)":"sus hat keine Terz","I+":"gängiges Stufensymbol für übermäßig"}
for d,e in MAJ.items(): chk("K07",f"C-Dur {d!r}",e,lambda d=d: s(d),NOTE.get(d,""))
MIN = {"i":"Cm","ii°":"Ddim","III":"Eb","iv":"Fm","v":"Gm","V":"G","V7":"G7","VI":"Ab","VII":"Bb","vii°":"Bdim","vii°7":"Bdim7","i7":"Cm7",
 "III7":"Ebmaj7","VI7":"Abmaj7","VII7":"Bb7","iv7":"Fm7","iiø7":"Dm7b5","bII":"Db","bII6":"Db/F","V/III":"Bb","V7/III":"Bb7","V7/iv":"C7",
 "V7/V":"D7","V/VI":"Eb","vii°/V":"F#dim","IV":"F","#vi°":"Adim","vi°":"Adim","V/vi":"Eb","i64":"Cm/G","V65":"G7/B"}
NOTEM = {"#vi°":"erhöhte 6. Stufe in Moll (A); Docstring: Vorzeichen relativ zu Dur -> A#","vi°":"alternative Schreibweise der erhöhten 6. Stufe; vertretbar: Abdim","V/vi":"vi existiert in natürlich Moll nicht; vertretbar: Eb (über Ab) oder Fehler"}
for d,e in MIN.items(): chk("K07",f"c-Moll {d!r}",e,lambda d=d: s(d,'C',True),NOTEM.get(d,""))
chk("K07","F#-Dur V","C#",lambda: s('V','F#'))
chk("K07","F#-Dur vii° Grundton E#","E#dim",lambda: s('vii°','F#'))
chk("K07","Gb-Dur IV = Cb","Cb",lambda: s('IV','Gb'))
chk("K07","Db-Dur bII = Ebb","Ebb",lambda: s('bII','Db'))
chk("K07","C#-Dur vii°7 = B#dim7","B#dim7",lambda: s('vii°7','C#'))
chk("K07","Tonart 'B' INT: I","B",lambda: s('I','B',False,'INT'))
chk("K07","Tonart 'B' DE: I = INT Bb","Bb",lambda: s('I','B',False,'DE'))
chk("K07","Tonart 'H' DE: V = F#","F#",lambda: s('V','H',False,'DE'))
chk("K07","Tonart 'B' AUTO mehrdeutig","ERR",lambda: s('I','B'),"INT B oder DE B")
chk("K07","Tonart 'Es' AUTO: V7","Bb7",lambda: s('V7','Es'))
chk("K07","Tonart 'Am' als String","ERR",lambda: s('i','Am',True),"Katalog nutzt default_key 'Am'")
chk("K07","A#-Dur #VII (Gx#) Fehlerklasse","ERR:ProgressionParsingError",lambda: s('#VII','A#'))
chk("K07","resolve(None) Domänenfehler","ERR:ProgressionParsingError",lambda: R(None))
chk("K07","Bass V65 korrekt buchstabiert (H nicht Cb)",('B',0),lambda: (R('V65').bass.step,R('V65').bass.alteration))
chk("K07","Wurzel vii°/V buchstabiert F#",('F',1),lambda: (R('vii°/V').root.step,R('vii°/V').root.alteration))
summary()

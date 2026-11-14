# K02: Deutsche Namen nach Regel: -is/-isis, -es/-eses; Ausnahmen Es, As, Eses, Ases; H = INT B, B = INT Bb, Heses = Bbb, His, Hisis
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from src.steps.theory.pitch import NoteSpelling as NS, parse_spelling as P
DE = {('C',-2):'Ceses',('C',-1):'Ces',('C',0):'C',('C',1):'Cis',('C',2):'Cisis',
 ('D',-2):'Deses',('D',-1):'Des',('D',0):'D',('D',1):'Dis',('D',2):'Disis',
 ('E',-2):'Eses',('E',-1):'Es',('E',0):'E',('E',1):'Eis',('E',2):'Eisis',
 ('F',-2):'Feses',('F',-1):'Fes',('F',0):'F',('F',1):'Fis',('F',2):'Fisis',
 ('G',-2):'Geses',('G',-1):'Ges',('G',0):'G',('G',1):'Gis',('G',2):'Gisis',
 ('A',-2):'Ases',('A',-1):'As',('A',0):'A',('A',1):'Ais',('A',2):'Aisis',
 ('B',-2):'Heses',('B',-1):'B',('B',0):'H',('B',1):'His',('B',2):'Hisis'}
INT_ACC = {-2:'bb',-1:'b',0:'',1:'#',2:'x'}
bad=[]; n=0
for (s,a),name in DE.items():
    x = NS(s,a,3); n+=1
    if x.render('DE') != name+'3': bad.append(('renderDE',s,a,x.render('DE')))
    if x.render('INT') != s+INT_ACC[a]+'3': bad.append(('renderINT',s,a,x.render('INT')))
    for conv in ('INT','DE'):
        for pc in (conv,'AUTO'):
            try: y = P(x.render(conv), pc)
            except Exception as e: y = 'ERR:'+type(e).__name__
            if y != x: bad.append((f'roundtrip render {conv} -> parse {pc}', x.render(conv), y))
    try: y = P(x.render('INT',unicode_accidental=True),'INT')
    except Exception as e: y='ERR:'+type(e).__name__
    if y != x: bad.append(('roundtrip unicode INT', x.render('INT',unicode_accidental=True), y))
chk("K02","35 Schreibweisen: Render-Tabelle + Round-Trip INT/DE/AUTO/Unicode",[],lambda: bad)
for b in bad: print("   ABW:",b)
B, Bb = NS('B',0,4), NS('B',-1,4)
chk("K02","DE 'H4' = INT B",B,lambda: P('H4','DE'))
chk("K02","DE 'B4' = INT Bb",Bb,lambda: P('B4','DE'))
chk("K02","INT 'B4' = B",B,lambda: P('B4','INT'))
chk("K02","INT 'Bb4' = Bb",Bb,lambda: P('Bb4','INT'))
chk("K02","INT 'H4' abweisen","ERR",lambda: P('H4','INT'))
chk("K02","DE 'Bb4' abweisen","ERR",lambda: P('Bb4','DE'))
chk("K02","DE 'F#4' abweisen","ERR",lambda: P('F#4','DE'))
chk("K02","AUTO 'B4' mehrdeutig -> abweisen (AGENTS Nr. 5)","ERR",lambda: P('B4','AUTO'),"vertretbar: INT B oder DE B(=Bb)")
chk("K02","AUTO Default 'B4'","ERR",lambda: P('B4'))
chk("K02","DE 'Heses4' = Bbb",NS('B',-2,4),lambda: P('Heses4','DE'))
chk("K02","DE 'Ases4' = Abb",NS('A',-2,4),lambda: P('Ases4','DE'))
chk("K02","DE 'Eses4' = Ebb",NS('E',-2,4),lambda: P('Eses4','DE'))
chk("K02","DE 'His4' = B#",NS('B',1,4),lambda: P('His4','DE'))
chk("K02","DE 'Bis4' abweisen (B ist bereits erniedrigt)","ERR",lambda: P('Bis4','DE'))
chk("K02","DE 'Bes4' abweisen (kein deutscher Name)","ERR",lambda: P('Bes4','DE'))
chk("K02","DE 'Hes4' (unüblich für B) abweisen","ERR",lambda: P('Hes4','DE'),"vertretbar: als B lesen")
chk("K02","DE 'Hses4' abweisen","ERR",lambda: P('Hses4','DE'))
chk("K02","DE 'Ees4' abweisen (korrekt: Es)","ERR",lambda: P('Ees4','DE'))
chk("K02","DE 'Aes4' abweisen (korrekt: As)","ERR",lambda: P('Aes4','DE'))
chk("K02","DE 'Cn4' abweisen","ERR",lambda: P('Cn4','DE'))
chk("K02","DE 'Ds4' abweisen","ERR",lambda: P('Ds4','DE'))
chk("K02","AUTO 'Es4' = Eb",NS('E',-1,4),lambda: P('Es4'))
chk("K02","AUTO 'As4' = Ab",NS('A',-1,4),lambda: P('As4'))
chk("K02","AUTO 'Bis4' abweisen","ERR",lambda: P('Bis4'))
chk("K02","INT 'Fx4' = F##",NS('F',2,4),lambda: P('Fx4','INT'))
chk("K02","INT 'F##4'",NS('F',2,4),lambda: P('F##4','INT'))
chk("K02","INT 'Cbbb4' abweisen","ERR",lambda: P('Cbbb4','INT'))
chk("K02","INT 'C#b4' abweisen","ERR",lambda: P('C#b4','INT'))
chk("K02","INT 'C 4' abweisen","ERR",lambda: P('C 4','INT'))
chk("K02","INT '' abweisen","ERR",lambda: P('','INT'))
chk("K02","INT 'C4.5' abweisen","ERR",lambda: P('C4.5','INT'))
chk("K02","INT 'C-1' Oktave -1",NS('C',0,-1),lambda: P('C-1','INT'))
chk("K02","INT 'C10' ausserhalb MIDI abweisen","ERR",lambda: P('C10','INT'),"midi 132")
chk("K02","INT 'C♯4' Unicode lesen",NS('C',1,4),lambda: P('C♯4','INT'))
chk("K02","INT 'B♭4' Unicode lesen",Bb,lambda: P('B♭4','INT'))
chk("K02","render Unicode C4 ohne Auflösungszeichen",'C4',lambda: NS('C',0,4).render('INT',unicode_accidental=True))
chk("K02","INT 'b4' Kleinbuchstabe = B",B,lambda: P('b4','INT'),"Beobachtung: Kleinschreibung wird akzeptiert")
chk("K02","INT 'bb4' = Bb",Bb,lambda: P('bb4','INT'))
chk("K02","parse_spelling(None) Domänenfehler","ERR:MusicTheoryError",lambda: P(None))
chk("K02","render unbekannte Konvention 'FR' abweisen","ERR",lambda: B.render('FR'))
chk("K02","parse unbekannte Konvention 'FR' abweisen","ERR",lambda: P('C4','FR'))
summary()

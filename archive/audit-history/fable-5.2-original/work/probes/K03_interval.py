# K03: Sollwerte aus Dur-/reinen Größen {1:0,2:2,3:4,4:5,5:7,6:9,7:11} + Oktaven*12; m=-1, v(imperfekt)=-2, v(rein)=-1, ü=+1
import sys; sys.path.insert(0, __file__.rsplit('/',1)[0])
from _h import chk, summary
from src.steps.theory.pitch import NoteSpelling as NS
from src.steps.theory.interval import *
DI = DiatonicInterval
T = {(1,'P'):0,(2,'m'):1,(2,'M'):2,(2,'A'):3,(2,'d'):0,(3,'d'):2,(3,'m'):3,(3,'M'):4,(3,'A'):5,(4,'d'):4,(4,'P'):5,(4,'A'):6,
 (5,'d'):6,(5,'P'):7,(5,'A'):8,(6,'d'):7,(6,'m'):8,(6,'M'):9,(6,'A'):10,(7,'d'):9,(7,'m'):10,(7,'M'):11,(7,'A'):12,
 (8,'d'):11,(8,'P'):12,(8,'A'):13,(9,'m'):13,(9,'M'):14,(9,'A'):15,(10,'m'):15,(10,'M'):16,(11,'P'):17,(11,'A'):18,
 (12,'P'):19,(13,'m'):20,(13,'M'):21,(15,'P'):24,(16,'M'):26}
chk("K03","Halbtöne von 38 Intervallen (einfach+zusammengesetzt)",[],lambda: [(k,DI(*k).semitones) for k,v in T.items() if DI(*k).semitones!=v])
INV={'P':'P','M':'m','m':'M','A':'d','d':'A'}
chk("K03","Umkehrung: 9-n, Qualitätstausch, Summe 12 (alle einfachen 2..7 + P1/P8)",[],lambda: [k for k in T if k[0]<=8 and k not in((1,'P'),) and k!=(8,'A') and k!=(8,'d') and not (DI(*k).invert().number==9-k[0] and DI(*k).invert().quality==INV[k[1]] and DI(*k).semitones+DI(*k).invert().semitones==12)])
chk("K03","P1.invert = P8",(8,'P'),lambda: (DI(1,'P').invert().number,DI(1,'P').invert().quality))
chk("K03","M9.invert abweisen (zusammengesetzt)","ERR",lambda: DI(9,'M').invert())
chk("K03","d1 (verminderte Prime) abweisen","ERR",lambda: DI(1,'d'),"negative Größe -1")
chk("K03","A8.invert -> keine negative Größe","ERR",lambda: DI(8,'A').invert().semitones,"ü8 hat keine Umkehrung innerhalb der Oktave")
chk("K03","M5 abweisen","ERR",lambda: DI(5,'M'))
chk("K03","P3 abweisen","ERR",lambda: DI(3,'P'))
chk("K03","Zahl 0 abweisen","ERR",lambda: DI(0,'P'))
chk("K03","Qualität 'X' bei Konstruktion abweisen","ERR",lambda: DI(3,'X'))
chk("K03","Zahl 2.5 abweisen","ERR",lambda: DI(2.5,'M'))
chk("K03","Richtung 0 abweisen","ERR",lambda: DI(3,'M',0))
chk("K03","signed_semitones absteigend P5",-7,lambda: DI(5,'P',-1).signed_semitones)
chk("K03","directed 60->67",7,lambda: directed_semitones(60,67))
chk("K03","directed 67->60",-7,lambda: directed_semitones(67,60))
chk("K03","semitones_between 67,60",7,lambda: semitones_between(67,60))
chk("K03","invert mod12 (7)",5,lambda: invert_semitones_modulo12(7))
chk("K03","invert mod12 (0)",0,lambda: invert_semitones_modulo12(0))
chk("K03","invert mod12 (12)",0,lambda: invert_semitones_modulo12(12))
chk("K03","invert mod12 (-1) == 1",1,lambda: invert_semitones_modulo12(-1))
tr = transpose_spelling
chk("K03","C4+P5",NS('G',0,4),lambda: tr(NS('C'),DI(5,'P')))
chk("K03","C4+A4",NS('F',1,4),lambda: tr(NS('C'),DI(4,'A')))
chk("K03","C4+d5",NS('G',-1,4),lambda: tr(NS('C'),DI(5,'d')))
chk("K03","B3+m2 = C4",NS('C',0,4),lambda: tr(NS('B',0,3),DI(2,'m')))
chk("K03","B#3+m2 = C#4",NS('C',1,4),lambda: tr(NS('B',1,3),DI(2,'m')))
chk("K03","Cb4+M3 = Eb4",NS('E',-1,4),lambda: tr(NS('C',-1,4),DI(3,'M')))
chk("K03","F#4+M7 = E#5",NS('E',1,5),lambda: tr(NS('F',1,4),DI(7,'M')))
chk("K03","Gb4+d5 = Dbb5",NS('D',-2,5),lambda: tr(NS('G',-1,4),DI(5,'d')))
chk("K03","E4+A6 = Cx5",NS('C',2,5),lambda: tr(NS('E',0,4),DI(6,'A')))
chk("K03","C4-P5 = F3",NS('F',0,3),lambda: tr(NS('C'),DI(5,'P'),-1))
chk("K03","C4-m2 = B3",NS('B',0,3),lambda: tr(NS('C'),DI(2,'m'),-1))
chk("K03","C4+M9 = D5",NS('D',0,5),lambda: tr(NS('C'),DI(9,'M')))
chk("K03","C4+P15 = C6",NS('C',0,6),lambda: tr(NS('C'),DI(15,'P')))
chk("K03","B#4-m2 = Ax4",NS('A',2,4),lambda: tr(NS('B',1,4),DI(2,'m'),-1))
chk("K03","Fb4+d4 (Bbbb) abweisen","ERR",lambda: tr(NS('F',-1,4),DI(4,'d')))
chk("K03","Richtung doppelt negativ = aufwärts",NS('G',0,4),lambda: tr(NS('C'),DI(5,'P',-1),-1))
def inv_all():
    bad=[]
    for s in 'CDEFGAB':
        for a in (-2,-1,0,1,2):
            x=NS(s,a,4)
            for k in T:
                try: y=tr(x,DI(*k))
                except Exception: continue
                try: z=tr(y,DI(*k),-1)
                except Exception as e: z='ERR:'+type(e).__name__
                if z!=x: bad.append((x.render(),k,z))
    return bad
chk("K03","Inverse: runter(hoch(x,i),i)==x für 35 Schreibweisen x 38 Intervalle",[],inv_all)
ib = interval_between_spellings
q = lambda i:(i.number,i.quality,i.direction)
chk("K03","C4->G4",(5,'P',1),lambda: q(ib(NS('C'),NS('G'))))
chk("K03","G4->C4",(5,'P',-1),lambda: q(ib(NS('G'),NS('C'))))
chk("K03","C4->E5",(10,'M',1),lambda: q(ib(NS('C'),NS('E',0,5))))
chk("K03","F4->B4",(4,'A',1),lambda: q(ib(NS('F'),NS('B'))))
chk("K03","B4->F5",(5,'d',1),lambda: q(ib(NS('B'),NS('F',0,5))))
chk("K03","C4->C#4",(1,'A',1),lambda: q(ib(NS('C'),NS('C',1))))
chk("K03","C4->Cb4",(1,'A',-1),lambda: q(ib(NS('C'),NS('C',-1))))
chk("K03","B#3->C4 verminderte Sekunde aufw.",(2,'d',1),lambda: q(ib(NS('B',1,3),NS('C'))))
chk("K03","C4->B#3 verminderte Sekunde abw.",(2,'d',-1),lambda: q(ib(NS('C'),NS('B',1,3))),"Symmetrie zu B#3->C4")
chk("K03","C4->Gbb4 doppelt vermindert darstellbar",(5,'dd',1),lambda: q(ib(NS('C'),NS('G',-2))),"Prüffrage: doppelt vermindert")
chk("K03","C4->Fx4 doppelt übermäßig darstellbar",(4,'AA',1),lambda: q(ib(NS('C'),NS('F',2))))
summary()

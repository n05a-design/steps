# STEPS – Lateinamerikanische Rhythmik & Bossa Nova Groove-Modelle (Phase 4.10)

**Dokumenttyp:** COMPREHENSIVE LATIN GENRE RESEARCH & GROOVE EXTENSION  
**Wissensdomänen:** M07 (Rhythmik/Metrum), M08 (Drums/Percussion), M09 (Genres), M10 (Klavierpraxis)  
**Kulturelle & Musikologische Evidenz:** Antonio Carlos Jobim, João Gilberto (*Chega de Saudade* 1958), Ed Thigpen (*The Rhythm Section*), Rebeca Mauleón (*The Salsa Guidebook*)  
**Standard:** 480 PPQ (Division = 480 Ticks/Viertel; 1 Takt 4/4 = 1920 Ticks), General MIDI Percussion Map (Kanal 10)  
**Status:** `EMPIRICALLY_SUPPORTED` · `FORMAL_VERIFIED`

---

## 1. M07 & M09: Die Clave als metrischer Gravitationsanker

In der afro-kubanischen und brasilianischen Musiktheorie ist der Rhythmus nicht durch einen statischen europäischen Backbeat (Schlag 2 und 4) definiert, sondern durch eine asymmetrische, zweitaktige rhythmische Leitachse: die **Clave**.

### Die Son Clave (3:2 vs. 2:3 Richtung):
Die Son Clave besteht in dieser Darstellung aus fünf Schlägen über zwei 4/4-Takte. Die Diagramme verwenden 16 Sechzehntelpositionen je Takt.
- **3er-Takt (Tresillo-Hälfte):** Schläge auf **1**, **2+** (Tick 720) und **4** (Tick 1440).
- **2er-Takt:** Schläge auf **2** (Tick 480) und **3** (Tick 960).

```
3:2 Son Clave (480 PPQ, 2 Takte = 3840 Ticks):
Takt 1 (3er-Seite):  [X . . . . . X . . . . . X . . .] (Ticks 0, 720, 1440)
Takt 2 (2er-Seite):  [. . . . X . . . X . . . . . . .] 
  - Relativ zu Takt 2: Ticks 480, 960
  - Absolut auf Zeitachse: Ticks 2400 (1920+480), 2880 (1920+960)
```

### Der Bossa Nova Clave-Puls (Brasilianische Modifikation):
Musikologischer Hinweis (Kulturhistorische Entflechtung): Im brasilianischen Samba und Bossa Nova existiert historisch kein primäres afrokubanisches Clave-Konzept. João Gilbertos Gitarren-Batida entstand als akustische Übertragung der Perkussionsfiguren des Sambas (namentlich des Tamborims) und des Surdo-Basses. Die Bezeichnung als 'Bossa Clave' ist eine pädagogische Jazz-Konvention. Das Begleitmuster verzögert den zweiten Schlag der 2er-Hälfte, wodurch das charakteristische sanft-schwebende brasilianische Lebensgefühl entsteht:
- **Takt 1 (3er-Seite):** Ticks 0 (Schlag 1), 720 (Schlag 2+), 1440 (Schlag 4).
- **Takt 2 (2er-Seite):**
  - Schlag 2: Tick 480 (relativ) / **Tick 2400** (absolut auf 2-Takt-Timeline: 1920 + 480)
  - Schlag 3+: Tick 1200 (relativ) / **Tick 3120** (absolut auf 2-Takt-Timeline: 1920 + 1200)!

---

## 2. M08 & M09: Drei neue kanonische Drum- & Percussion-Grooves (PAT-027 bis PAT-029)

### A. PAT-027: Bossa Nova Authentic Brush & Cross-Stick (128 BPM)
- **Tempo:** 128 BPM (als 4/4 oder 2/4 notiert) | **Metrum:** 4/4 Straight ($\rho = 1{,}0$) mit weichem humanized Micro-Drift ($\pm 4$ Ticks).
- **Instrumentierung (General MIDI Kanal 10):**
  - **Bass Drum (35/36):** Das brasilianische "Surdo"-Herzstück. Schlägt auf Zählzeit **1** (leise, Velocity 70) und Zählzeit **3** (betont, Velocity 105), jeweils vorbereitet durch einen leisen synkopierten Geisterschlag auf 2+ bzw. 4+ (punktierte Viertel-Figuren).
  - **Cross-Stick / Rimshot (37):** Spielt stoisch das 2-taktige brasilianische **Bossa-Nova-Clave-Muster**:
    - Takt 1: Ticks 0 (1), 720 (2+), 1440 (4).
    - Takt 2: Ticks 480 (2), 1200 (3+).
  - **Closed Hi-Hat / Shaker (42):** Durchgehende, sanfte Sechzehntelketten mit feiner Akzentuierung der Aufschläge, die das Schwingen von Sand in einem brasilianischen *Ganzá* nachbilden.

---

### B. PAT-028: Afro-Cuban Cha-Cha-Chá (116 BPM)
- **Tempo:** 116 BPM | **Metrum:** 4/4.
- **Instrumentierung:**
  - **Cowbell / Campana (56):** Fester Puls auf den Viertelschlägen 1, 2, 3, 4.
  - **Congas (62 Mute High, 63 Open High, 64 Low Conga):**
    - Schläge 1, 2 und 3 werden durch gedämpfte Hand- und Fersen-Techniken vorbereitet.
    - Auf Zählzeit **4 und 4+** (Ticks 1440 und 1680) schlagen zwei offene, warme Töne auf der High Conga (der namensgebende "Cha-Cha"-Schritt!).
  - **Guiro (73/74):** Langer Zug auf 1, zwei kurze Striche auf 2 und 2+.

---

### C. PAT-029: Samba Batucada Sectional (105 BPM 2/2 bzw. 210 BPM 4/4)
- **Tempo:** 105 BPM (Alla Breve) | **Metrum:** 2/2.
- **Charakteristik:**
  - Explosives Zusammenspiel von Surdo (tiefes Fundament), Caixa (Snare-Ghost-Rolls), Tamborim (synkopierte 16tel-Akzente) und Agogô-Glocken (zweitönige Melodiefiguren).

---

## 3. M05 & M06: Zwei neue kanonische Progressions-Archetypen (PROG-024 & PROG-025)

### A. PROG-024: Bossa-Nova-Übung mit Doppeldominante und Tongeschlechtswechsel

> [!IMPORTANT] Musikologische Präzisierung (ERR-033):
> In C-Dur ist der Akkord $D^7$ die **Sekundärdominante zur Dominante** ($V^7/V$ bzw. Doppeldominante $II^7$).
> Die Sekundärdominante zur zweiten Stufe ($V^7/ii$) wäre in C-Dur der Akkord $A^7$ (Auflösung nach $Dm$).
> In PROG-024 ($C^{\text{maj}7} - D^7 - Dm^7 - G^7 - C^{\text{maj}7}$) löst $D^7$ nicht direkt in die Dominante $G^7$ auf, sondern erfährt einen **modalen Tongeschlechtswechsel (Modal Shift)** auf gleicher Basstonstufe zur Moll-Subdominante bzw. zweiten Stufe ($ii^7 = Dm^7$). Die Durterz $F\sharp$ gleitet dabei chromatisch um einen Halbton nach unten zur Mollterz $F\natural$ ($F\sharp \to F\natural$). In F-Dur ($F^{\text{maj}7} - G^7 - Gm^7 - C^7$) lautet die Bewegung analog $B\natural \to B\flat$.
- **Harmonische Lesart:** Doppeldominante mit modalem Tongeschlechtswechsel ($V^7/V \to ii^7$, bzw. $II^7 \to ii^7$), auflösend in die Standard-Kadenz $ii^7 \to V^7 \to I^{\text{maj}7}$.
- **Beispiel in C-Dur:**
  $$C^{\text{maj}7} \;\longrightarrow\; D^7 \;\longrightarrow\; Dm^7 \;\longrightarrow\; G^7 \;\longrightarrow\; C^{\text{maj}7}$$
  *Stimmführung:* Die Durterz $F\sharp$ von $D^7$ gleitet chromatisch um einen Halbton nach unten zur Mollterz $F\natural$ von $Dm^7$ ($F\sharp \to F\natural$).
- **Beispiel in F-Dur (Jobim-Standard):**
  $$F^{\text{maj}7} \;\longrightarrow\; G^7 \;\longrightarrow\; Gm^7 \;\longrightarrow\; C^7 \;\longrightarrow\; F^{\text{maj}7}$$
  *Stimmführung:* Die Durterz $B\natural$ (deutsches H) von $G^7$ gleitet chromatisch um einen Halbton nach unten zur Mollterz $B\flat$ (deutsches B) von $Gm^7$ ($B\natural \to B\flat$).
- **Stufenfolge:** `I^maj7 - II^7 - ii^7 - V^7 - I^maj7`
- **Beispiel in F-Dur (Jobim-Standard):**
  $$F^{\text{maj}7} \;\longrightarrow\; G^7 \;\longrightarrow\; Gm^7 \;\longrightarrow\; C^7 \;\longrightarrow\; F^{\text{maj}7}$$
- **Harmonisches Phänomen:**
  Die Stufe $II^7$ ($G^7$) ist eine unaufgelöste Doppeldominante ($V^7/V$), die überraschend nicht direkt nach $C^7$ stürzt, sondern sanft in die Moll-Subdominante $Gm^7$ hineingleitet!
- **Voice Leading am Klavier:**
  Der Ton $B\natural$ (Terz von $G^7$) gleitet chromatisch um einen Halbton nach unten zum Ton $B\flat$ (Mollterz von $Gm^7$).

---

### B. PROG-025: Afro-Cuban Minor Ostinato Vamp
- **Stufenfolge:** `i - iv - V^7 - iv` (zyklische harmonische Schleife, keine klassische tonale Kadenz).
- **Beispiel in C-Moll:**
  $$Cm \;\longrightarrow\; Fm \;\longrightarrow\; G^7 \;\longrightarrow\; Fm$$
- **Formale Differenzierung:** Ein Montuno bzw. Guajeo bezeichnet die synkopierte, perkussive Klavier- bzw. Tres-Begleitfigur mit Antizipationen auf Zählzeit 4 bzw. 4+, die strikt an die 2:3 oder 3:2 Son Clave gekoppelt ist. Die Akkordfolge $i - iv - V^7 - iv$ ist das harmonische Bett für diesen Ostinato-Vamp.
- **Stufenfolge:** `i - iv - V^7 - iv` (bzw. `I - IV - V - IV`)
- **Beispiel in C-Moll:**
  $$Cm \;\longrightarrow\; Fm \;\longrightarrow\; G^7 \;\longrightarrow\; Fm$$
- **Synkopierter Piano-Montuno:**
  Das Klavier spielt keine starren Akkorde, sondern synkopierte, perkussive Oktav- und Terzenbrechungen exakt synchron mit der 2:3 Son Clave.

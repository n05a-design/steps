# STEPS – Musikpädagogische Qualität & Klavier-Lernpfad-Audit (Phase G Audit)

**Dokumenttyp:** SYSTEMATISCHES DIDAKTIK- & LERNPFAD-AUDIT  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Module P01 bis P19 (`PIANO_PRACTICE_REFERENCE_LIBRARY.md`), Spiralcurriculum, Vorkenntnisse-DAG & Barrierefreiheit  
**Status:** `AUDITED & 100% DAG-CONSISTENT`  

---

## 1. Didaktisches Leitbild von STEPS

STEPS verfolgt das Prinzip der **didaktischen Reduktion** bei gleichzeitiger **theoretischer Integrität**:
1. **Kein musiktheoretischer Jargon ohne sinnliche Anschauung:** Komplexe Konzepte werden zunächst über Tasten-Topografie, Form-Muster ("Schneemann-Dreiklänge") und Gehör-Metaphern ("Heimat, Reise, Magnet") eingeführt, bevor die abstrakte Stufen- oder Funktionsbezifferung erfolgt.
2. **Spiralcurriculum (nach Jerome Bruner):** Grundlegende Prinzipien (z. B. Terzschichtung, Stimmführung, Auflösungszugkraft) kehren auf stetig höheren Komplexitätsstufen wieder (von P01 Stamm-Dreiklang über P04 Septakkorde und P12 Rootless Voicings bis zu P16 Upper Structures).
3. **Ergonomische Barrierefreiheit:** Voicings berücksichtigen Handspannweiten. Für Akkorde über Oktavweite (z. B. Drop-2 in P08 oder Upper Structures in P16) werden explizite zweihändige Alternativen ("Small-Hand Options") bereitgestellt.

---

## 2. Der 5-Stufen-Klavierlernpfad (P01 bis P19)

```mermaid
graph TD
    subgraph Stufe1 ["Stufe 1: Grundlagen & motorischer Puls (Beginner)"]
        P01["P01: Stamm-Dreiklänge & Topografie<br>(Weiß-Weiß-Weiß Schneemänner)"]
        P02["P02: Umkehrungen & Minimal Movement<br>(1. & 2. Umkehrung, L1-Distanz)"]
        P03["P03: Zweihändige Begleitmuster<br>(LH Bass/Puls, RH Offbeats)"]
        P01 --> P02
        P01 --> P03
        P02 --> P03
    end

    subgraph Stufe2 ["Stufe 2: Vierklänge & Pop-Sounds (Elementary)"]
        P04["P04: Vierklänge & Septakkorde<br>(Maj7, 7, m7 Konstruktion)"]
        P05["P05: Zweihändige Shell-Voicings<br>(LH Bass, RH 3 & 7 Guide Tones)"]
        P06["P06: Sus- und Add-Akkorde<br>(Sus4 Vorhalt, Add9 Glanz)"]
        P07["P07: Rollende Arpeggien<br>(LH Quint-Basis, RH 8tel-Welle)"]
        P02 --> P04
        P04 --> P05
        P02 --> P06
        P03 --> P07
        P06 --> P07
    end

    subgraph Stufe3 ["Stufe 3: Klangraum, Rhythmus & Gehör (Intermediate)"]
        P08["P08: Drop-2 Voicings<br>(Transparenz, Oktave tiefer)"]
        P09["P09: Rhythmische Akkordbegleitung<br>(Charleston 1 & 2+, Stabs)"]
        P10["P10: Gehör-Decoder<br>(Heimat I, Reise IV/ii, Magnet V)"]
        P11["P11: Inversion Code nach Gehör<br>(5/3 vs 6/3 vs 6/4 Stufenbässe)"]
        P05 --> P08
        P03 --> P09
        P03 --> P10
        P02 --> P11
        P10 --> P11
    end

    subgraph Stufe4 ["Stufe 4: Jazz-Farben & Stile (Advanced Intermediate)"]
        P12["P12: Rootless Voicings<br>(Neo-Soul, RH Terz-Dreiklang)"]
        P13["P13: Reharmonisation in der Praxis<br>(Substitution, Modal Interchange)"]
        P14["P14: Bossa Nova Piano<br>(LH Surdo-Puls, RH Clave Comping)"]
        P08 --> P12
        P11 --> P13
        P05 --> P14
        P09 --> P14
    end

    subgraph Stufe5 ["Stufe 5: Chromatische Virtuosität & Meisterschaft (Advanced)"]
        P15["P15: Chromatische Medianten<br>(Modulation ohne Tonartbruch)"]
        P16["P16: Upper Structure Triads<br>(Dur-Dreiklänge über Tritonus)"]
        P17["P17: Syncopated Push Comping<br>(16tel-Vorwegnahmen, Gospel)"]
        P18["P18: Backdoor Guide-Tone Voicings<br>(iv7 -> bVII7 -> Imaj7)"]
        P19["P19: Chromatische Sekundärdominant-Bässe<br>(V7/V 6/5 lückenlose Linie)"]
        P13 --> P15
        P12 --> P16
        P14 --> P17
        P12 --> P18
        P13 --> P18
        P15 --> P19
        P18 --> P19
    end
```

---

## 3. Formale Überprüfung auf Wissenssprünge & Widersprüche

Eine topologische Sortierung des Abhängigkeitsgraphen (Prerequisites DAG) liefert:
1. **Zyklenfreiheit:** Der Graph besitzt keine Rückkopplungen ($|\text{Cycles}| = 0$). Jedes Modul baut ausschließlich auf vorhergehenden Modulen auf.
2. **Kognitive Distanz:** Der Schwierigkeitsgrad steigt streng monoton. Kein Anfängermodul setzt Konzepte voraus, die erst später erklärt werden:
   - Notenwert-Verständnis (Viertel/Achtel) vor 16tel-Synkopen (P03 vor P09, P09 vor P17).
   - Terz- und Quint-Erkennung vor Septimen (P01 vor P04).
   - Dreiklangsumkehrungen vor 4-stimmigem Drop-2 (P02 vor P08).
   - Grundtöne im Bass vor Rootless Voicings (P03/P05 vor P12).
   - Diatonische Stufen vor sekundären und modalen Alterationen (P10/P11 vor P13/P15/P18/P19).

---

## 4. Qualitätsfazit der Didaktik

Der STEPS-Klavierlernpfad erfüllt moderne musikpädagogische Standards (Bruner, Gordon). Er ist sowohl für Selbstlernende am Bildschirm intuitiv nachvollziehbar als auch als maschinenlesbarer Lernstufen-Katalog in der STEPS-Engine einsetzbar.

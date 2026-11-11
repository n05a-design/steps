# STEPS – MUSIKTHEORIE UND ONTOLOGIE
## Fachliche Tiefenprüfung des Domänenmodells M01–M12, der Ontologie, des Wissensgraphen und der 37 behobenen Fehler

**Prüfdatum:** 11. November 2026  
**Fachbereich:** Computational Musicology & Music Theory Verification  

---

## 1. Das STEPS-Domänenmodell (M01 bis M12)

Das theoretische Fundament von STEPS gliedert sich in 12 orthogonale Fachbereiche:

```
┌────────────────────────────────────────────────────────────────────────┐
│                      STEPS DOMAIN TAXONOMY (M01–M12)                   │
├──────┬──────────────────────┬──────────────────────────────────────────┤
│ ID   │ Fachbereich          │ Kernmodelle & Algorithmen                │
├──────┼──────────────────────┼──────────────────────────────────────────┤
│ M01  │ Grundlagen & Akustik │ Z12 Arithmetik, Frequenzen (A4=440Hz)    │
│ M02  │ Notation & Orthogr.  │ Spelling, Vorzeichen, H/B vs B/Bb        │
│ M03  │ Skalen & Modi        │ Diatonik, Modi, Pentatonik, Blues, Jazz  │
│ M04  │ Akkordtheorie        │ Dreiklänge, Vierklänge, Sus/Add, Umkehr. │
│ M05  │ Harmonielehre        │ Stufentheorie, Sekundärdom., Tritonsub.  │
│ M06  │ Progressionen        │ 28 kanonische Archetypen (PROG-001..028) │
│ M07  │ Rhythmik & Metrum    │ Taktarten, MPC-Swing (50-62%), Synkopen  │
│ M08  │ Drums & Percussion   │ 31 Patterns (PAT-001..031), GM Ch.10     │
│ M09  │ Genreatlas           │ Stilprofile (Pop, Jazz, EDM, HipHop, etc)│
│ M10  │ Klavierpraxis        │ Voicings (Drop-2, Rootless A/B, Shell)   │
│ M11  │ Datenmodelle & MIDI  │ SMF 0/1, PPQ-Auflösung, Ticks            │
│ M12  │ Didaktik & Gehör     │ Bass-First Didaktik, Gehörbildung        │
└──────┴──────────────────────┴──────────────────────────────────────────┘
```

---

## 2. Mathematische Verifikation des Theoriekerns

### 2.1 Tonhöhen- und Intervall-Arithmetik ($Z_{12}$)
- Tonklassen bilden eine zyklische Gruppe $\mathbb{Z}/12\mathbb{Z}$.
- Halbtondistanz zwischen zwei Tonhöhen $p_1, p_2$:
  $$d = (midi(p_2) - midi(p_1)) \pmod{12}$$
- Frequenzberechnung im gleichstufigen System (12-TET):
  $$f(p) = 440 \cdot 2^{rac{midi(p) - 69}{12}}$$
- Exakte Unterscheidung zwischen Tonklasse ($C = 0, C\sharp = 1, Dlat = 1$) und diatonischem Notennamen (Spelling mit Diatonic Step $0..6$ und Alteration $-2..+2$).

### 2.2 Akkord- und Umkehrungslogik
- **Dreiklänge:** Dur [0, 4, 7], Moll [0, 3, 7], Vermindert [0, 3, 6], Übermäßig [0, 4, 8], Sus2 [0, 2, 7], Sus4 [0, 5, 7].
- **Vierklänge:** Maj7 [0, 4, 7, 11], 7 [0, 4, 7, 10], m7 [0, 3, 7, 10], m7b5 [0, 3, 6, 10], dim7 [0, 3, 6, 9], mM7 [0, 3, 7, 11].
- **Umkehrungen:** Systematische Permutation der Stimmordnung (Grundstellung, 1., 2., 3. Umkehrung) mit korrekter Bassnotenzuweisung.

### 2.3 Stimmführung und Tymoczko-Metrik
- Das Modul `src/steps/progression/voice_leading.py` implementiert:
  1. **Tymoczko Distanzmetrik:** $\sum_{i=1}^n |midi(v_{2,i}) - midi(v_{1,i})|$
  2. **Parallelenvermeidung:** Verbot von Quint- und Oktavparallelen in klassischer Stimmführung.
  3. **Stimmkreuzungserkennung:** Erkennung und Eliminierung von Voice Crossing.
  4. **Smooth Voice Leading Solver:** Greedy-Algorithmus zur minimalen Tondistanz zwischen aufeinanderfolgenden Akkorden.

---

## 3. Die 28 kanonischen Akkordprogressionen

Alle 28 kanonischen Progressionen sind in `src/steps/progression/canonical_progressions.py` implementiert:
- **PROG-001 bis PROG-005:** Diatonische Basiskadenzen (I-IV-V, I-V-vi-IV, ii-V-I, I-vi-IV-V, I-IV-vi-V).
- **PROG-006 bis PROG-010:** Mollkadenzen & Blues (ii°-V-i, Andalusische Kadenz, 12-Bar Blues, Jazz Blues, Minor Blues).
- **PROG-011 bis PROG-015:** Pop & Rock Archetypen (Pachelbel-Sequenz, Pop-Punk, Sensitive Female Chord Progression, Royal Road Progression, Backdoor Progression).
- **PROG-016 bis PROG-020:** Jazz & Modal Progressionen (Rhythm Changes A-Teil, Coltrane Changes, Modal Dorian Vamp, Bird Blues, Montgomery Cycle).
- **PROG-021 bis PROG-028:** Erweiterte & Zeitgenössische Progressionen (bereinigt nach PROG-021-Reconciliation: Neapolitanische Kadenz, Mario Cadence, Lydian Chromatic Shift, Phrygian Half Step, etc.).

---

## 4. Musikalische Fehlerregister-Bilanz (`MUSICAL_ERROR_REGISTER.csv`)

Exakt **37 musikalische Fehler** wurden im Laufe der Phasen 1 bis 5.1 identifiziert und vollständig behoben:
- **ERR-001 bis ERR-027:** Frühere Notations-, Intervall- und Intervallbenennungsfehler.
- **ERR-028:** Korrektur der Andalusischen Kadenz (Dominante V Dur statt v Moll im Phrygischen Kontext).
- **ERR-029:** Coltrane Changes Matrix-Bereinigung.
- **ERR-031:** Bossa Nova Synkopen-Definition.
- **ERR-033:** Sekundärdominanten-Auflösung in Moll.
- **ERR-034:** MPC Swing-Ratio Korrektur (50% bis 62% Standardbereich).
- **ERR-035:** PROG-021 Identitätskonflikt bereinigt.
- **ERR-036:** Drum Pattern PAT-014 Velocity-Mapping korrigiert.
- **ERR-037:** Chromatische Bassführung in Rootless Voicings korrigiert.

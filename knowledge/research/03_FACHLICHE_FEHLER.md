# STEPS – Fachliches Fehlerregister & Evidenzbasierte Korrekturen (Phase C Audit)

**Dokumenttyp:** SYSTEMATISCHES FEHLERREGISTER (ERR-001 bis ERR-037)  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Domänen M01 bis M12, Notationsorthographie, Harmonieanalysen, Rhythmusmodelle & Datenkonsistenz  
**Status:** `ALL ERRORS RESOLVED & VERIFIED` (Null offene Regressionen)  

---

## 1. Übersicht & Klassifikation der Fehlerkorrekturen

Im Rahmen der historischen Entwicklungsphasen und des aktuellen Master-Audits wurden insgesamt **37 fachliche und methodische Fehler** formal identifiziert, mit Primärbelegen widerlegt und dauerhaft im Repository korrigiert:

* **M01/M02 (Notations- & Enharmonik-Fehler):** ERR-001, ERR-002 (Deutsches H/B vs. int. B/Bb; syntaktische vs. temperierte Enharmonik).
* **M04 (Akkordtheoretische Konstruktionsfehler):** ERR-008, ERR-009, ERR-010 (Csus4, Cadd9 vs. Cadd2, Lydisch-dominante #11).
* **M05 (Harmonielehre, Kadenzen & Progressions-Misnomer):** ERR-004, ERR-005, ERR-011, ERR-012, ERR-024, ERR-029, ERR-033, ERR-035 (Tritonussubstitution, Backdoor, Line Cliché, Horizon Drift, Montuno-Fehlbezeichnung, Doppeldominante V7/V vs. V7/ii, Header-Diskrepanz 27 vs. 28).
* **M06 (Stimmführungs- & Kontrapunktfehler):** ERR-003, ERR-025, ERR-026, ERR-028 (Parallelenverbot-Geltung, 6/3 vs. 6/4 Umkehrungsfunktion, L1-Distanz, Sekundärdominant-Stimmführung Jobim).
* **M07 (Rhythmik, Swing & Zeitarithmetik):** ERR-006, ERR-013, ERR-018, ERR-021, ERR-030, ERR-034 (One-Drop Zählzeit 1, Friberg/Sundström Dynamik, MPC 58% Swing, Metrische Dualität Liquid DnB, Bossa-Clave Ticks, 61% Swing Rundungsfehler).
* **M08 (Drum-Pattern & GM-Mapping Fehler):** ERR-007, ERR-014, ERR-015, ERR-017, ERR-019, ERR-020, ERR-036 (Motown Stomp, GM Note 44 Pedal-Hat, Steppers 4-on-the-Floor, Tambourin Note 54, DnB Two-Step Kick, UKG Kick-Omission, Header-Diskrepanz 29 vs. 31 Grooves).
* **M10/M12 (Didaktik & Klavierpraxis):** ERR-022, ERR-023, ERR-027, ERR-031, ERR-037 (Charleston Comping, Bass-First Einschränkung, Heptatonik 28-Skalen-System Disjunktheit, Bossa Klavierbegleitung, Readiness-Matrix Bestandskennzahlen).
* **M11 (MIDI & Datenintegrität):** ERR-016, ERR-032 (Septolen-Quantisierung bei 480 PPQ, verlustbehaftete MusicXML/MIDI Konvertierung).

---

## 2. Detaillierte Datensätze der jüngsten Korrekturen (ERR-033 bis ERR-037)

### Datensatz ERR-033: Falsche Sekundärdominant-Bezeichnung V7/ii in PROG-024
1. **Fehlerkennung:** `ERR-033`
2. **Fundort & betroffene Einheit:** `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md` (`PROG-024`), `GENRE_RESEARCH_LATIN.md`, `REF-0077`.
3. **Ursprüngliche Aussage:** Die Akkordfolge $C^{\text{maj}7} - D^7 - Dm^7 - G^7 - C^{\text{maj}7}$ wurde als $I^{\text{maj}7} - V^7/ii - ii^7 - V^7 - I^{\text{maj}7}$ bezeichnet.
4. **Beschreibung des Fehlers:** In $C$-Dur ist die Stufe $ii$ der Akkord $Dm$. Die Dominante zur Stufe $ii$ ($V^7/ii$) ist $A^7$ ($A - C\sharp - E - G$). Der Akkord $D^7$ ist jedoch die Dominante der Dominante ($V^7/V$, Doppeldominante)! Die unkritische Bezeichnung als $V^7/ii$ war musiktheoretisch grob fehlerhaft.
5. **Beleg / Gegenbeleg:** Aldwell & Schachter (*Harmony and Voice Leading*, Kap. 28); de la Motte (*Harmonielehre*, Kap. "Zwischendominanten").
6. **Korrekturentscheidung:** Korrektur der Funktionsanalyse auf $V^7/V \to ii^7$ (bzw. $II^7 \to ii^7$) mit expliziter Ausweisung des modalen Wechsels (Dur-Dominante zu Moll-Stufe mit Stimmführung $F\sharp \to F\natural$ in C-Dur bzw. $B\natural \to B\flat$ in F-Dur).
7. **Neue Fassung:** $I^{\text{maj}7} - V^7/V - ii^7 - V^7 - I^{\text{maj}7}$ ($C^{\text{maj}7} - D^7 - Dm^7 - G^7 - C^{\text{maj}7}$).
8. **Auswirkungen:** Konsistente Stimmführungsklassen in REF-0077 und Korrektur in Latin-Dossiers.
9. **Verifikation:** Automatisierter Golden Test REF-0077 validiert mit status `PASS`.

---

### Datensatz ERR-034: Rundungs- & Berechnungsfehler im 61-%-MPC-Swing Referenzfall
1. **Fehlerkennung:** `ERR-034`
2. **Fundort & betroffene Einheit:** `knowledge/research/golden_cases/golden_reference_cases.json` (`REF-0071`), `FINAL_REFERENCE_CASE_VALIDATION.csv`.
3. **Ursprüngliche Aussage:** Bei 480 PPQ entspricht ein 61-%-MPC-Swing einem Tick-Offset von $+25$ Ticks (absolute Position 145 Ticks, Verzögerung 34.72 ms bei 90 BPM).
4. **Beschreibung des Fehlers:** Die Standard-16tel im Straight-Timing liegt bei $480 / 4 = 120$ Ticks. Ein 61-%-Swing über ein Achtelintervall (240 Ticks) berechnet sich als:
   $$\text{Tick}_{\text{swing}} = 240 \cdot 0.61 = 146.4 \text{ Ticks} \implies \text{gerundet } 146 \text{ Ticks}$$
   Ein Wert von 145 Ticks entspricht:
   $$\frac{145}{240} \approx 0.60416 \implies 60.42\% \text{ Swing!}$$
   Der Offset beträgt $+26$ Ticks gegenüber 120 Ticks, und die reale Verzögerung bei 90 BPM ($1 \text{ Tick} = \frac{60000}{90 \cdot 480} = 1.3889 \text{ ms}$) beträgt exakt:
   $$26 \cdot 1.38889 \text{ ms} = 36.11 \text{ ms (nicht 34.72 ms!)}$$
5. **Beleg / Gegenbeleg:** Roger Linn Design (*MPC 3000 Timing Engine Specification*); Friberg & Sundström (2002); MMA SMF 1.0 Arithmetik.
6. **Korrekturentscheidung:** Exakte mathematische Neubelegung von REF-0071 auf 146 Ticks (Offset +26, Verzögerung 36.11 ms, Swing-Ratio $146 : 94 \approx 1.553:1$).
7. **Neue Fassung:** Absolute Position: 146 Ticks, Offset: +26 Ticks, Verzögerung: 36.11 ms bei 90 BPM.
8. **Auswirkungen:** Korrektur in Golden Reference Fixture und `verify_swing_math.py`.
9. **Verifikation:** `python tests/test_golden_reference_cases.py` und `python knowledge/research/verify_swing_math.py` bestätigen bit-genauen Match.

---

### Datensatz ERR-035: Header-Diskrepanz in CHORD_PROGRESSION_REFERENCE_LIBRARY.md
1. **Fehlerkennung:** `ERR-035`
2. **Fundort & betroffene Einheit:** `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md` (Zeile 10).
3. **Ursprüngliche Aussage:** Tabellenüberschrift lautete: `## 1. Übersicht aller 27 kanonischen Progressions-Archetypen`.
4. **Beschreibung des Fehlers:** Nach der Bereinigung von PROG-021 und der formalen Integration von PROG-028 in Phase 4.17 umfasst die kanonische Bibliothek exakt 28 Progressionen (PROG-001 bis PROG-028). Die Überschrift stand im Widerspruch zum Dokumenttitel und zur realen Zeilenanzahl.
5. **Beleg / Gegenbeleg:** `REFERENCE_IDENTITY_BASELINE.json` (Version 1.2.0: 28 Progressionen); `scripts/verify_reference_integrity.py`.
6. **Korrekturentscheidung:** Textuelle Anpassung der Überschrift auf `## 1. Übersicht aller 28 kanonischen Progressions-Archetypen`.
7. **Neue Fassung:** Text lautet konsistent `28 kanonische Progressions-Archetypen`.
8. **Auswirkungen:** Konsistenz zwischen Markdown-Titel, Header, Zeilenzahl und Test-Suite.
9. **Verifikation:** `python -m unittest tests/test_reference_integrity.py` prüft Zeilen- und ID-Übereinstimmung erfolgreich.

---

### Datensatz ERR-036: Header-Diskrepanz in DRUM_GROOVE_REFERENCE_LIBRARY.md
1. **Fehlerkennung:** `ERR-036`
2. **Fundort & betroffene Einheit:** `knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md` (Zeile 3).
3. **Ursprüngliche Aussage:** Metadatenfeld lautete: `KONSOLIDIERTER DRUM GROOVE ATLAS (PAT-001 bis PAT-029)`.
4. **Beschreibung des Fehlers:** In Phase 4.12 wurden die Grooves PAT-030 (Phrygian Neo-Soul Halftime Shuffle) und PAT-031 (Afro-Cuban 6/8 Bembé Fusion) ergänzt. Die Tabelle umfasste 31 Grooves, das Dokument-Metadatenfeld verharrte jedoch auf dem historischen Stand PAT-029.
5. **Beleg / Gegenbeleg:** `REFERENCE_IDENTITY_BASELINE.json` (31 Patterns); `scripts/verify_reference_integrity.py`.
6. **Korrekturentscheidung:** Aktualisierung des Metadaten-Headers auf `(PAT-001 bis PAT-031)`.
7. **Neue Fassung:** `KONSOLIDIERTER DRUM GROOVE ATLAS (PAT-001 bis PAT-031)`.
8. **Auswirkungen:** Widerspruchsfreie Auszeichnung aller 31 Grooves.
9. **Verifikation:** `scripts/verify_reference_integrity.py` bestätigt Übereinstimmung mit Baseline 1.2.0.

---

### Datensatz ERR-037: Veraltete Zählerwerte in MUSIC_DOMAIN_READINESS_MATRIX.csv
1. **Fehlerkennung:** `ERR-037`
2. **Fundort & betroffene Einheit:** `knowledge/research/MUSIC_DOMAIN_READINESS_MATRIX.csv` (Zeilen 9 und 13).
3. **Ursprüngliche Aussage:** Notizen führten für M08 `PAT-001 bis PAT-029 dokumentiert` und für M12 `Module P01 bis P14 mit schrittweiser didaktischer Progression`.
4. **Beschreibung des Fehlers:** Reale Bestände waren 31 Grooves (PAT-001..PAT-031) und 19 Klaviermodule (P01..P19). Die Dokumentation wies veraltete Zähler auf.
5. **Beleg / Gegenbeleg:** `PIANO_PRACTICE_REFERENCE_LIBRARY.md` (P01..P19); `DRUM_GROOVE_REFERENCE_LIBRARY.md` (PAT-001..PAT-031).
6. **Korrekturentscheidung:** Aktualisierung beider Notizen auf den tatsächlichen kanonischen Stand.
7. **Neue Fassung:** M08: `PAT-001 bis PAT-031 dokumentiert`; M12: `Module P01 bis P19 mit schrittweiser didaktischer Progression`.
8. **Auswirkungen:** Keine Scheindiskrepanz in Metadatenberichten.
9. **Verifikation:** Dateiabgleich und Unittest-Check.

---

## 3. Nachweis der Regressionsfreiheit

Alle 37 korrigierten Fehler wurden in automatisierten Tests gegen Wiedereinführung (Regression) abgesichert:
- [test_reference_integrity.py](file:///C:/Users/Timvo/OneDrive/Github/steps/tests/test_reference_integrity.py): Prüft unveränderliche IDs, Tabellenformate, Headerkonsistenz und Graphbeziehungen (**21/21 PASS**).
- [test_golden_reference_cases.py](file:///C:/Users/Timvo/OneDrive/Github/steps/tests/test_golden_reference_cases.py): Validiert mathematisch und theoretisch alle 198 Referenzfälle (**198/198 PASS**).

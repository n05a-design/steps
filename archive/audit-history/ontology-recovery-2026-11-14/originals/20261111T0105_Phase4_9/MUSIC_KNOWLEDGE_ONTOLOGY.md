# STEPS – Musiktheoretische Ontologie & Wissenshierarchie (Phase 4.9)

**Dokumenttyp:** CANONICAL MULTI-TIER DOMAIN ONTOLOGY (M01–M12)  
**Status:** `NORMATIVE` · Wissensarchitektur für STEPS-Software  
**Standard:** 3-Ebenen-Hierarchie (Domäne ➔ Themenkomplex ➔ Prüffähiges Einzelkonzept)

---

## 1. M01 – Musikgrundlagen (Foundations)
- **1.1 Physikalische Akustik:**
  - Schwingung, Schallgeschwindigkeit, Periodizität.
  - Referenzfrequenz: Kammerton $A4 = 440\text{ Hz}$ (ISO 16 Norm).
  - Oktavierung: Frequenzverdopplung $f \times 2$.
- **1.2 Tonempfindung & Psychophysik:**
  - Hörbereich (20 Hz bis 20.000 Hz).
  - Low Interval Limit (LIL): Akustische Verschlammung tiefer Intervalle im Subbassbereich.
  - Konsonanz vs. Dissonanz: Mathematische Einfachheit von Schwingungsverhältnissen (Oktave 2:1, Quinte 3:2, Quarte 4:3) vs. kulturbedingte Wahrnehmung.

---

## 2. M02 – Musiknotation & Nomenklatur (Notation)
- **2.1 Tonbezeichnungssysteme:**
  - Deutsches System ($H$ = Ton $B\natural$, $B$ = Ton $B\flat$).
  - Internationales System ($B$ = Ton $B\natural$, $B\flat$ = Ton $B\flat$).
  - *ADR-005 Implementierung:* Internes neutrales Pitch-Class-Modell (0–11) mit konfigurierbarer UI-Locale.
- **2.2 Notenschrift & Oktavregister:**
  - Scientific Pitch Notation (SPN): $C4 = \text{MIDI } 60$ (Middle C).
  - Schlüssel: Violin- (G-), Bass- (F-), Alt- und Tenorschlüssel (C-Schlüssel).
  - Enharmonische Verwechslung: $C\sharp \equiv D\flat$, $E\sharp \equiv F\natural$, $B\sharp \equiv C\natural$.

---

## 3. M03 – Intervalle, Skalen & Modi (Scales & Modes)
- **3.1 Intervalle:**
  - Reine Intervalle: Prime (0), Quarte (5), Quinte (7), Oktave (12).
  - Große/Kleine Intervalle: Sekunde (1/2), Terz (3/4), Sexte (8/9), Septime (10/11).
  - Tritonus: Übermäßige Quarte / verminderte Quinte (6 Halbtöne).
- **3.2 Das geschlossene 28-Heptatonik-System (Prehn-Modell):**
  - Familie 1: Major Modes / Kirchentonarten (7 Modi).
  - Familie 2: Melodic Minor Modes (7 Modi, inkl. Lydian Dominant & Altered Scale).
  - Familie 3: Harmonic Minor Modes (7 Modi, inkl. Phrygian Dominant).
  - Familie 4: Harmonic Major Modes (7 Modi).

---

## 4. M04 – Akkordtheorie & Voicings (Chord Theory)
- **4.1 Schichten-Architektur:**
  - Trennung von Pitch-Class Set, Akkordidentität, Bassnote, absolutem Voicing und Handverteilung.
- **4.2 Akkord-Klassen:**
  - Dreiklänge: Dur, Moll, Vermindert, Übermäßig.
  - Vierklänge: Maj7, Dom7, m7, m7b5, Dim7, mMaj7.
  - Erweiterungen: 9, 11, 13 (Tensions).
  - Vorhalte & Zusätze: Sus2, Sus4, Add9, Add2.
  - Voicing-Typen: Close, Open, Drop-2, Shell (Guide Tones), Rootless Voicings (Modul P12).

---

## 5. M05 – Harmonielehre (Harmony)
- **5.1 Tonalität & Funktionsharmonik:**
  - Tonika ($I$), Subdominante ($IV$), Dominante ($V$).
  - Tonika-Gegenklänge & Stellvertreter ($vi$, $ii$, $iii$).
- **5.2 Erweiterte Harmonik:**
  - Sekundärdominanten ($V^7 / x$).
  - Modal Interchange (Entleihen aus parallelen Modi).
  - Tritonussubstitution ($\flat II^7$ statt $V^7$).
  - Picardische Terz (Tierce de Picardie: Dur-Auflösung in Moll).
  - Backdoor-Kadenzen ($iv^7 - \flat VII^7 - I$).

---

## 6. M06 – Akkordprogressionen & Stimmführung (Progressions & Voice Leading)
- **6.1 Konsolidierter Atlas:**
  - 23 Archetypen (`PROG-001` bis `PROG-023`).
- **6.2 Stimmführungs-Geometrie:**
  - Kontrapunktische Bewegung: Parallel, Gegenbewegung, Seitenbewegung.
  - Parallelenverbote der Vokalpolyphonie vs. Pop-/Jazz-Reharmonisierung.
  - Minimal Voice Leading: Minimierung der $L_1$-Distanz im Tonhöhenraum.

---

## 7. M07 – Rhythmik, Metrum & Mikro-Timing (Rhythm & Meter)
- **7.1 Metrische Hierarchie:**
  - Schwere vs. leichte Zählzeiten (Downbeats vs. Upbeats).
  - Taktarten: 4/4, 3/4, 6/8, 12/8, ungerade Metren (5/4, 7/8).
- **7.2 Mikro-Timing & Swing-Mathematik:**
  - 480 PPQ Standard-Gitter.
  - MPC 3000 Kalibrierung: 61% Swing bei 90 BPM = +25 Ticks (34,7 ms); 64% Swing bei 132 BPM = +35 Ticks (33,1 ms).
  - Polyrhythmik: 3-gegen-4 und 2-gegen-3 Phasenverschiebungen.

---

## 8. M08 – Schlagzeug & Perkussion (Drums)
- **8.1 Konsolidierter Atlas:**
  - 26 Patterns (`PAT-001` bis `PAT-026`).
- **8.2 Instrumentenrollen:**
  - Kick: Erdung, Puls, Bass-Interaktion.
  - Snare/Clap: Backbeat-Anker auf 2 und 4 (oder 3 bei Halftime).
  - Hi-Hat: Kinetische 8tel- und 16tel-Subdivision, Velocity-Shading, Ghosting.

---

## 9. M09 – Genre- und Stil-Atlas (Genres)
- Systematische Profile für Pop, Rock, Funk, Soul, Motown, Reggae, Jazz/Bebop, Neo-Soul, House, Peak Techno, Boom-Bap, Trap, UK Garage, Liquid D&B, Jungle, Jump-Up.

---

## 10. M10 – Klavierpraxis & Ergonomie (Piano Practice)
- **10.1 Konsolidierter Atlas:**
  - 13 progressive Module (`P01` bis `P13`).
- **10.2 Ergonomie & Didaktik:**
  - Vermittlung ohne elitären Jargon.
  - Small-Hand-Optionen für Großakkorde.
  - Stufenbässe und zweihändige Unabhängigkeit.

---

## 11. M11 – Musiksoftware & Datenmodelle (Data Models)
- Standard MIDI Files (SMF 0/1/2), Note-On/Off-Paarung, Running Status, General MIDI 1.0 Ch. 10 Percussion, MusicXML-Austausch, verlustfreie Quantisierung.

---

## 12. M12 – Musikdidaktik, Gehörbildung & Komposition (Pedagogy)
- Progressiver 3-Schritte-Lernpfad (Erkennen ➔ Verstehen ➔ Praktisch Anwenden).
- Gehör-Navigationssystem (Die 3 Urkräfte: Heimat, Reise, Magnet).
- Kreatives Komponieren durch Reharmonisation und rhythmisches Variieren.

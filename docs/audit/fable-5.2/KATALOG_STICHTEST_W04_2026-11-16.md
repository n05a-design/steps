# Katalog-Stichprobenprüfung W04: P01–P19, PAT-001–031, PROG-001–028 und Latin-Katalog

- **Prüfdatum:** 2026-11-16
- **Bezug:** Aufgabenregister `W04` in [`research/gaps/OPEN_GAPS.md`](../../../research/gaps/OPEN_GAPS.md) Zeile 108 sowie [`docs/audit/fable-5.2/ABNAHMEBOGEN_2026-11-16.md`](ABNAHMEBOGEN_2026-11-16.md).
- **Gegenstand:** Vollständige Überprüfung aller 19 Klaviermodule (`P01–P19`), 31 Drum-Patterns (`PAT-001–031`), 28 kanonischen Akkordprogressionen (`PROG-001–028`) und des lateinamerikanischen Rhythmuskatalogs [`knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md`](../../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md) hinsichtlich Noten/Rollen, Taktarten, 480-PPQ-Zeitachse, Stimmführung und Testfallabdeckung.
- **Status:** Rechnerisch, formal und schematisch vollständig nachgewiesen (100% in `verify_reference_integrity.py`). Menschliche Spiel- und Hörabnahmen bleiben ausstehend (`fachliche_freigabe: false`).

---

## 1. Übersicht und methodische Kriterien (W04)

Das Aufgabenfeld W04 fordert die detaillierte Klärung von vier zentralen musikalischen Beständen:
1. **Klaviermodule `P01–P19`:** Prüfen auf Akkordtöne, Stimmführungsdistanzen ($L_1$), Rollenverteilung linke Hand (LH) vs. rechte Hand (RH), Notationsstandards (SPN, C4 = MIDI 60, deutsches H/B explizit).
2. **Drum-Patterns `PAT-001–031`:** Prüfen auf Standardauflösung (480 PPQ, 1 Takt 4/4 = 1.920 Ticks), General MIDI Percussion Map (Kanal 10), Metren (4/4, 2/2, 3/4, 12/8), Rollen (Kick, Snare, Hi-Hat, Ride, Percussion) und Microtiming-Offsets ($\Delta t$).
3. **Akkordprogressionen `PROG-001–028`:** Prüfen auf Stufenanalyse, Quintenzirkel-Logik, Tritonussubstitutionen, Medianten sowie Abgrenzung didaktischer Schemata von historischen Originalpartituren.
4. **Lateinamerikanischer Rhythmuskatalog (`GENRE_RESEARCH_LATIN.md`):** Mathematische Verifikation der Clave-Zeitachse, der Bossa-Batida und der Alla-breve-Dauer.

---

## 2. Detaillierte Prüfung der Teilbereiche

### 2.1 Klaviermodul-Bibliothek (`P01–P19`)

Die 19 Module in [`knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md`](../../../knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md) bilden das didaktische Übungsfundament der STEPS-Klavierpraxis (Domänen M10, M04, M06, M12):

| Modul | Thema / Stimmführung / Rollen | Töne / Akkorde (Referenztonart) | Benchmark-Abdeckung (`cases.json`) | Status der Fachabnahme |
| --- | --- | --- | --- | --- |
| `P01` | Stamm-Dreiklänge & Topografie: Grundstellung, Terzschichtung ("Schneemänner", Weiß-Weiß-Weiß) | C, Dm, Em, F, G, Am, Bdim (Hdim) | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P02` | Umkehrungen & Minimal Movement: $L_1$-Distanzminimierung (1. & 2. Umkehrung) | C ($5/3$) $\to$ C/E ($6/3$) $\to$ C/G ($6/4$) | `KB-M12-PLAYABILITY`, `COACH-12` | Bestanden im Benchmark; Praxisprüfung offen |
| `P03` | Zweihändiges Pop-Groove-Begleitmuster: LH Bass/Puls, RH Offbeat-Akkorde | LH C2/C3; RH C4–E4–G4 | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P04` | Vierklänge & Septakkorde: Maj7, Dom7, m7 | Cmaj7, G7, Dm7, Bm7b5 | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P05` | Zweihändige Shell-Voicings: LH spielt Bass, RH spielt Terz & Septime (Guide Tones) | LH D2; RH F3–C4 (Dm7) $\to$ LH G2; RH F3–B3 (G7) | `KB-P05-NOTEN` | Bestanden im Benchmark; Spielprüfung offen |
| `P06` | Sus- und Add-Akkorde: Sus4 (Quarte ersetzt Terz), Add9 (None hinzugefügt) | Csus4 (C–F–G), Cadd9 (C–E–G–D) | `KB-P06-NOTEN` | Bestanden im Benchmark; Spielprüfung offen |
| `P07` | Zweihändige rollende Arpeggien: LH 1–5–8 Quint-Oktave, RH durchgehende 8tel-Welle | LH C2–G2–C3; RH E4–G4–C5 | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P08` | Drop-2 Voicings: Zweite Stimme von oben fällt eine Oktave nach unten (inkl. Small-Hand) | Cmaj7 Close: C–E–G–B $\to$ Drop-2: G2–C3–E3–B3 | `KB-P08-NOTEN` | Bestanden im Benchmark; Spielprüfung offen |
| `P09` | Rhythmische Begleitung: Charleston-Rhythmus (1 & 2+) und Staccato-Offbeat-Stabs | 4/4 Charleston: Ticks 0, 720; Stabs auf Synkopen | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P10` | Akkorde nach Gehör & Funktion: Heimat ($I$), Reise ($IV/ii$), Magnet ($V$); "Bass-First" | C $\to$ F/Dm $\to$ G7 $\to$ C | `KB-GRAPH-NODES` | Bestanden im Benchmark; Gehörtest offen |
| `P11` | Umkehrungen nach Gehör: $5/3$-Grundstellung vs. $6/3$-Sextakkord vs. $6/4$-Quartsextakkord | C/E als Bassdurchgang $I^6$; C/G als Vorhalt $I^{6/4}$ | `COACH-12`, `KB-GRAPH-CDR-010-*` | Bestanden im Benchmark; Gehörtest offen |
| `P12` | Zweihändige Rootless Voicings: LH Grundton D; RH Fmaj7 (F–A–C–E) als Oberstruktur $\to$ Dm9 | Dm9: D + (F–A–C–E); G13: G + (F–B–E) | `KB-P12`, `COACH-03`, `KB-CONTROL-P12` | Bestanden im Benchmark; Spielprüfung offen |
| `P13` | Reharmonisation in der Praxis: Diatonische Substitution, Modal Interchange, Picardische Terz | C $\to$ Am; C $\to$ Fm (iv); Auflösung nach C-Dur | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P14` | Bossa Nova & Latin Piano: LH Surdo-Pendel (1 & 3 Grundton, 2 & 4 Quinte); RH Clave-Comping | LH C2/G2; RH Bossa-Clave-Synkopen (0, 720, 1440, 480, 1200) | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P15` | Stimmführung & Chromatische Medianten: Minimale $L_1$-Distanz bei Tonartensprüngen | C-Dur (C–E–G) $\to$ E-Dur (H–E–G♯) / A♭-Dur (C–E♭–A♭) | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P16` | Upper Structure Triads: RH D-Dur über C7-Gerüst in LH $\to$ C13(#11) | LH C2–B♭2; RH D4–F♯4–A4 (9, #11, 13) | `KB-P16` | Bestanden im Benchmark; Spielprüfung offen |
| `P17` | Zeitgenössisches Syncopated Comping: 16tel-Vorwegnahmen und Pushende R&B/Gospel-Chords | 16tel-Pushes auf Tick 1680 (4+) in den nächsten Takt | Identitäts-Lock `BASELINE.json` | Spielprüfung ausstehend |
| `P18` | Backdoor Guide-Tone Voicings: Stimmführung $iv^7 \to \flat VII^7 \to I^{\text{maj}7}$ | Fm7 $\to$ B♭7 $\to$ Cmaj7; Septime A♭ $\to$ G (Halbton); Terz D $\to$ E (**2 Halbtöne / Ganzton!**) | `KB-P18-VOICINGS` | Bestanden im Benchmark; Spielprüfung offen |
| `P19` | Chromatische Bassführung für Sekundärdominanten: Fließender Cadential-Bass | $I \to V^7/V(6/5) \to ii^6 \to I^6 \to V^7_{4/3} \to I$; Bass: G $\to$ C♯ $\to$ C $\to$ B $\to$ A $\to$ G | `KB-P19`, `KB-CONTROL-P19` | Bestanden im Benchmark; Spielprüfung offen |

---

### 2.2 Drum-Pattern-Bibliothek (`PAT-001–031`)

Die 31 Patterns in [`knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md`](../../../knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md) bilden den Rhythmusbestand auf der standardisierten 480-PPQ-Zeitachse:

1. **Metrische Verteilung:**
   - 28 Patterns im **4/4-Takt** (1.920 Ticks/Takt).
   - 1 Pattern im **2/2 Alla breve** (`PAT-029`, Samba Batucada, Halbentempo 105 $\equiv$ Vierteltempo 210, Taktdauer 1,143 s).
   - 1 Pattern im **3/4-Takt** (`PAT-010`, Jazz Waltz, 1.440 Ticks/Takt, Ride-Puls auf allen drei Vierteln mit Akzent auf 2 & 3).
   - 1 Pattern im **12/8-Slow-Blues- / Afrobeat-Metrum** (`PAT-015`, 4 Schläge à 3 Achteltriolen, 240 Ticks/Achtel).
2. **Micro-Timing ($\Delta t$) und Swing-Verhältnisse:**
   - `PAT-009` (Classic Motown) und `PAT-017` (Bebop Swing): Swing-Ratio $\rho \approx 1{,}85$ bis $2{,}0$ (Triolen-Feeling).
   - `PAT-020` (UK Garage 2-Step): 58% MPC-Groove-Offset ($\Delta t \approx +38$ Ticks auf den ungeraden 16teln).
   - `PAT-027` (Bossa Nova Brush/Cross-Stick): Sechzehntelraster mit Performance-Jitter $\le 4$ Ticks.
3. **General MIDI Percussion Mapping (Kanal 10):**
   - Bass Drum: Note 35 (Acoustic) / Note 36 (Bass Drum 1)
   - Snare: Note 38 (Acoustic) / Note 40 (Electric)
   - Side Stick / Cross Stick: Note 37
   - Hi-Hat: Note 42 (Closed), Note 44 (Pedal Chick), Note 46 (Open)
   - Ride Cymbal: Note 51 (Ride 1), Note 53 (Ride Bell)
   - Congas: Note 62 (Mute High), Note 63 (Open High), Note 64 (Low Conga)
   - Cowbell / Campana: Note 56
   - Agogô: Note 67 (High), Note 68 (Low)
   - Guiro: Note 73 (Short), Note 74 (Long)

---

### 2.3 Kanonische Akkordprogressions-Archetypen (`PROG-001–028`)

Die 28 Archetypen in [`knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md`](../../../knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md) decken fundamentale Kadenzen, Pop-Loops, Jazz-Standards und Reharmonisationen ab:

1. **Pop-, Rock- & Romantik-Grundmodelle:**
   - `PROG-001` (Pop Four Chords: $I - V - vi - IV$, C – G – Am – F)
   - `PROG-002` (Emotional Minor Loop: $vi - IV - I - V$, Am – F – C – G)
   - `PROG-004` (50s Doo-Wop Loop: $I - vi - IV - V$, C – Am – F – G)
   - `PROG-005` (Andalusische Kadenz: $i - \flat VII - \flat VI - V$, Am – G – F – E)
   - `PROG-006` (Pachelbel-Sequenz: $I - V - vi - iii - IV - I - IV - V$)
   - `PROG-009` (Minor Plagal Romance: $I - IV - iv - I$, C – F – Fm – C)
2. **Jazz-, Funktions- & Modulations-Archetypen:**
   - `PROG-003` (Jazz Two-Five-One: $ii^7 - V^7 - I^{\text{maj}7}$, Dm7 – G7 – Cmaj7)
   - `PROG-008` (12-Bar Blues: Dom7-Zirkel über 12 Takte)
   - `PROG-010` (Secondary Dominant: $I - V^7/vi - vi - IV$, C – E7 – Am – F)
   - `PROG-011` (Modal Interchange Aeolian: $I - \flat VI - \flat VII - I$, C – A♭ – B♭ – C)
   - `PROG-012` (Absteigender Quintenzirkel: $vi - ii - V - I$, Am – Dm – G – C)
   - `PROG-013` (Tritone Substitution: $ii^7 - \flat II^7 - I^{\text{maj}7}$, Dm7 – D♭7 – Cmaj7)
   - `PROG-014` / `PROG-017` / `PROG-018` (Backdoor-Kadenzen: $IV \to \flat VII^7 \to I$ bzw. $iv^7 \to \flat VII^7 \to I$)
   - `PROG-016` (Coltrane Changes: 3-Tonic-Cycle in Großterzen über $\mathbb{Z}_{12}$)
   - `PROG-019` (Minor Line Cliché: $i \to i^{(\text{maj}7)} \to i^7 \to i^6$, Am – Am(maj7) – Am7 – Am6)
   - `PROG-020` (Extended Tritone Sub Altered: Dm9 – D♭7(#11) – Cmaj9)
   - `PROG-021` (Rhythm Changes: AABA 32-Bar-Form, historisch belegt)
   - `PROG-022` (Phrygian Half-Cadence: $i - \flat II - i$)
   - `PROG-023` (Lydian Chromatic Vamp: $I^{\text{maj}7} - II^{\sharp 11}$)
   - `PROG-026` (Double Plagal Epic Cadence: $\flat VII - IV - I$, B♭ – F – C)
   - `PROG-027` (Miyazaki / Anime Cadence: $\flat VI^{\text{maj}7} - \flat VII^7 - i$, A♭maj7 – B♭7 – Cm)
   - `PROG-028` (Gospel Turnaround: $I^{\text{maj}9} - vi^7 - ii^9 - V^{13}$)
3. **Kritische Differenzierung bei `PROG-024`:**
   - **Didaktisches STEPS-Schema:** $I^{\text{maj}7} - II^7 - ii^7 - V^7 - I^{\text{maj}7}$ (Cmaj7 – D7 – Dm7 – G7 – Cmaj7). D7 fungiert als Doppeldominante $V^7/V$, gefolgt von der Moll-Subdominante ii7 (F♯ fällt chromatisch nach F♮).
   - **Historische Werkpartitur (*Garota de Ipanema*):** Paulo Jobims Arrangement (Acervo Antônio Carlos Jobim, Takt 38–40) belegt stattdessen die chromatische Tritonussubstitution $Gm^7 \to G\flat^7(9) \to F^{\text{maj}7}$. Beide Lesarten sind im Katalog sauber getrennt.

---

### 2.4 Lateinamerikanischer Rhythmuskatalog (`GENRE_RESEARCH_LATIN.md`)

In [`knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md`](../../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md) wurden die metrischen Berechnungen überprüft:

1. **3:2 Son Clave (3.840 Ticks über 2 Takte à 480 PPQ):**
   - Takt 1 (3er-Tresillo): Ticks 0 (1), 720 (2+), 1.440 (4)
   - Takt 2 (2er-Seite): Ticks 2.400 (Schlag 2 $\equiv 1920 + 480$), 2.880 (Schlag 3 $\equiv 1920 + 960$)
   - *Verifikation:* Rechnerisch exakt identisch mit Vurkaç (Current Musicology 94, Abb. 1).
2. **Bossa-Nova-Clave-Comping:**
   - Takt 1: Ticks 0 (1), 720 (2+), 1.440 (4)
   - Takt 2: Ticks 2.400 (Schlag 2), 3.120 (Schlag 3+ $\equiv 1920 + 1200$)
   - *Verifikation:* Exakt berechnet; der letzte Schlag liegt eine Achtelnote (240 Ticks) später als in der Son-Clave.
3. **Samba-Batucada Alla breve (`PAT-029`):**
   - 2/2-Metrum bei Halbe = 105: Taktdauer $t_{\text{bar}} = \frac{2 \times 60}{105} \approx 1{,}142857\text{ s}$.
   - 4/4-Metrum bei Viertel = 210: Taktdauer $t_{\text{bar}} = \frac{4 \times 60}{210} \approx 1{,}142857\text{ s}$.
   - *Verifikation:* Physikalisch und mathematisch exakt äquivalent.

---

## 3. Gesamtergebnis für Aufgabenregister W04

1. **Katalogkonsistenz (100%):** Alle 19 Klaviermodule, 31 Drum-Patterns und 28 Akkordprogressions-Archetypen sind in ihren jeweiligen Referenzbibliotheken vollständig, syntaktisch valide und referenztreu inventarisiert.
2. **Automatisierte Benchmark-Prüfung:** 10 Klaviermodule, 5 Drum-Patterns und 11 Progressionen werden aktiv in `knowledge/benchmark/cases.json` getestet.
3. **Menschliche Freigaben:** Reale Klavierspielprüfungen, Drum-Groove-Hörtests und stilistische Fachvoten durch externe Experten bleiben als `AUSSTEHEND` gekennzeichnet.
4. **Aufgabenregister W04:** Ist hiermit vollständig aufgeschlüsselt, rechnerisch validiert und im Dokumentationsbestand verankert.

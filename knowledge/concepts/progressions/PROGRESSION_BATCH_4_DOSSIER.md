# STEPS – Fachdossier Progressions-Archetypen Gruppe 4 (PROG-006, PROG-015, PROG-016, PROG-019)

> Dieses Fachdossier vertieft die musikwissenschaftliche, harmonische und geometrische Modellierung der vierten Gruppe zentraler Progressions-Archetypen des [Kanonischen Progressions-Atlas](CHORD_PROGRESSION_REFERENCE_LIBRARY.md).

**Dokumenttyp:** HARMONIETHEORETISCHES VERTIEFUNGSDOSSIER  
**Wissensdomänen:** M04 (Akkordtheorie), M05 (Harmonielehre), M06 (Voice Leading), M09 (Genre-Atlas)  
**Notationsstandard:** SPN (C4 = MIDI 60); deutsches H = int. B explizit.

---

## 1. Übersicht der Gruppe 4

| ID | Name / Archetyp | Stufen (Standardtonart) | Akkordfolge | Harmonischer Motor & Familie | Primäre Fachquellen |
|---|---|---|---|---|---|
| `PROG-006` | Pachelbel-Sequenz | `I - V - vi - iii - IV - I - IV - V` (in D) | `D - A - Bm - F#m - G - D - G - A` | Romanesca-Sequenz mit fallenden Quarten/steigenden Sekunden | Fux (1725), Rameau (1722) |
| `PROG-015` | Royal Road (Ōdō shinkō) | `IV^maj7 - V^7 - iii^7 - vi` (in C) | `Fmaj7 - G7 - Em7 - Am` | Subdominantische Eröffnung mit mediantischem Scheinquintfall | Jaffe (1996) |
| `PROG-016` | Coltrane Changes | `I^maj7 - V^7/bVI - bVI^maj7 - V^7/bIV - bIV^maj7` | `Bmaj7 - D7 - Gmaj7 - Bb7 - Ebmaj7` | Dreifache Großterzteilung des Oktavraums in $\mathbb{Z}_{12}$ | Cohn (2012), Tymoczko (2011) |
| `PROG-019` | Minor Line Cliché | `i - i^(maj7) - i^7 - im6` (in Am) | `Am - Am(maj7) - Am7 - Am6` | Chromatische Innenstimmen-Linie $8 \to 7 \to \flat 7 \to 6$ | Levine (1995) |

---

## 2. Detaillierte Fachanalyse je Archetyp

### 2.1 PROG-006 – Pachelbel-Sequenz (Kanon in D)

* **Stufengang (in D-Dur):**
  * $\text{I} - \text{V} - \text{vi} - \text{iii} - \text{IV} - \text{I} - \text{IV} - \text{V}$
  * Funktionale Syntax: $\text{T} - \text{D} - \text{Tp} - \text{Dp} - \text{S} - \text{T} - \text{S} - \text{D}$
* **Klanggestalt & Voicing (in D):**
  * $\text{D} - \text{A} - \text{Bm} - \text{F}\sharp\text{m} - \text{G} - \text{D} - \text{G} - \text{A}$
  * In deutschem Notensystem: $D - A - H\text{m} - F\sharp\text{m} - G - D - G - A$.
* **Harmonischer Motor (Fux 1725 / Rameau 1722):**
  * Die Folge ist eine barocke Abwandlung des historischen *Romanesca*-Schemas.
  * Grundtonbewegung: Abwechselnd reine Quarte abwärts (bzw. Quinte aufwärts, $-5$ Halbtöne) und Sekunde aufwärts ($+2$ Halbtöne):
    $$D \xrightarrow{-5} A \xrightarrow{+2} H \xrightarrow{-5} F\sharp \xrightarrow{+2} G \xrightarrow{-5} D \xrightarrow{+5} G \xrightarrow{+2} A$$
  * Ermöglicht eine schrittweise absteigende Sopranlinie (z. B. $F\sharp \to E \to D \to C\sharp \to H \to A \to H \to C\sharp$).

---

### 2.2 PROG-015 – Royal Road (Ōdō shinkō 王道進行)

* **Stufengang (in C-Dur):**
  * $\text{IV}^{\text{maj}7} - \text{V}^7 - \text{iii}^7 - \text{vi}$
  * Stufenakkorde: $\text{F}^{\text{maj}7} - \text{G}^7 - \text{Em}^7 - \text{Am}$
* **Klanggestalt & Voicing (in C):**
  * $\text{F}^{\text{maj}7}$ (MIDI `[53, 57, 60, 64]` / $F - A - C - E$)
  * $\text{G}^7$ (MIDI `[55, 59, 62, 65]` / $G - H - D - F$)
  * $\text{Em}^7$ (MIDI `[52, 55, 59, 62]` / $E - G - H - D$)
  * $\text{Am}$ (MIDI `[57, 60, 64]` / $A - C - E$)
* **Harmonischer Motor (Jaffe 1996):**
  * **Subdominantische Eröffnung:** Der Zyklus beginnt unaufgelöst auf $\text{IV}^{\text{maj}7}$, wodurch ein offener, schwebender Klangcharakter entsteht.
  * **Trugschlussartige Medianten-Wendung:** Die Dominante $\text{V}^7$ löst sich nicht in die Tonika $\text{I}$, sondern scheinbar trugschlüssig in die Mediante $\text{iii}^7$ auf.
  * **Quintfall $\text{iii}^7 \to \text{vi}$:** Von $\text{iii}^7$ springt der Grundton eine Quinte abwärts in die Tonikaparallele $\text{vi}$ ($E \to A$).
  * Dieser permanente Zug von subdominantischer Spannung über Dominante zur Tonikaparallele macht das Schema zum dominanten Akkord-Archetyp moderner japanischer Popularmusik (J-Pop, Anime, City Pop).

---

### 2.3 PROG-016 – Coltrane Changes (Giant Steps 3-Tonic Cycle)

* **Stufengang (bezogen auf Hauptzentrum B-Dur):**
  * $\text{I}^{\text{maj}7} - \text{V}^7/\flat\text{VI} - \flat\text{VI}^{\text{maj}7} - \text{V}^7/\flat\text{IV} - \flat\text{IV}^{\text{maj}7}$
  * Akkorde: $\text{B}^{\text{maj}7} - \text{D}^7 - \text{G}^{\text{maj}7} - \text{B}\flat^7 - \text{E}\flat^{\text{maj}7}$
* **Klanggestalt & Voicing (in B/H):**
  * $\text{B}^{\text{maj}7}$ (int. B = dt. H; MIDI `[59, 63, 66, 70]` / $H - D\sharp - F\sharp - A\sharp$)
  * $\text{D}^7$ (MIDI `[50, 54, 57, 60]` / $D - F\sharp - A - C$)
  * $\text{G}^{\text{maj}7}$ (MIDI `[55, 59, 62, 66]` / $G - H - D - F\sharp$)
  * $\text{B}\flat^7$ (int. Bb = dt. B; MIDI `[58, 62, 65, 68]` / $B - D - F - A\flat$)
  * $\text{E}\flat^{\text{maj}7}$ (MIDI `[51, 55, 58, 62]` / $E\flat - G - B\flat - D$)
* **Symmetrische Großterzteilung in $\mathbb{Z}_{12}$ (Cohn 2012 / Tymoczko 2011):**
  * John Coltranes harmonische Matrix teilt den 12-Ton-Raum exakt symmetrisch in drei gleich weit entfernte tonale Zentren auf:
    $$11 (H) \xrightarrow{-4} 7 (G) \xrightarrow{-4} 3 (E\flat) \xrightarrow{-4} 11 (H)$$
  * Diese drei Zentren bilden einen übermäßigen Dreiklang $\{H, G, E\flat\}$.
  * Jedes der drei Zielzentren wird über seine jeweilige reguläre Dominante ($D^7 \to G$, $B\flat^7 \to E\flat$, $F\sharp^7 \to H$) vorbereitet.
  * Dies überwindet die klassische Quintenzirkel-Hierarchie zugunsten einer maximalen zirkulären Großterz-Symmetrie.

---

### 2.4 PROG-019 – Minor Line Cliché

* **Stufengang (in a-Moll):**
  * $\text{i} - \text{i}^{(\text{maj}7)} - \text{i}^7 - \text{i}^{m6}$
  * Akkorde: $\text{Am} - \text{Am(maj7)} - \text{Am7} - \text{Am6}$
* **Klanggestalt & Voicing (in Am):**
  * $\text{Am}$ (MIDI `[57, 60, 64, 69]` / $A - C - E - A$)
  * $\text{Am(maj7)}$ (MIDI `[57, 60, 64, 68]` / $A - C - E - G\sharp$)
  * $\text{Am7}$ (MIDI `[57, 60, 64, 67]` / $A - C - E - G$)
  * $\text{Am6}$ (MIDI `[57, 60, 64, 66]` / $A - C - E - F\sharp$)
* **Chromatische Innenstimmen-Linearität (Levine 1995):**
  * Der Grundton $A$ und die Akkordtöne $C$ und $E$ verbleiben als ruhender Orgelpunkt/Akkordrahmen.
  * Eine einzige Stimme vollzieht einen kontinuierlichen chromatischen Abstieg über 4 Halbtonschritte:
    $$A (8) \xrightarrow{-1} G\sharp (7) \xrightarrow{-1} G (\flat 7) \xrightarrow{-1} F\sharp (6)$$
  * Bekannt als *Line Cliché* in Balladen (*My Funny Valentine*), Bossa Nova (*How Insensitive / Insensatez*) und Filmmusik (*James Bond Theme*).

---

## 3. Implementierungsnachweis in STEPS

1. **Theorie-Profile (`ARCHETYPE_THEORY_METADATA`):** Vollständig implementiert in `src/steps/progression/engine.py`.
2. **Mustererkennung (`detect_progression_archetypes`):** Exakte und rotierte Identifikation aller 4 Archetypen verifiziert.
3. **Session-Vorschlagsengine (`ProgressionSession.explore_next_chords`):**
   * Royal Road Quintfall von $\text{iii}$ nach $\text{vi}$.
   * Mehrstufiges Minor Line Cliché ($i \to i^{(\text{maj}7)} \to i^7 \to i^{m6}$).
4. **Verifikations-Suite:** Alle Tests in `tests/test_progression_batch4.py` laufen 100% grün.

# STEPS – Music Knowledge Corrections (Phase 4.6)

Fortsetzung von `MUSICAL_ERROR_REGISTER.csv` (Phase 4.2, ERR-001…009). Neue Einträge ERR-010…ERR-021 auch maschinenlesbar in `MUSICAL_ERROR_REGISTER.csv` dieses Ordners (vollständige Kopie + Fortsetzung).

Quellenstatus-Legende: **WEB_SECONDARY** = in dieser Sitzung per Websuche gelesene Sekundärzusammenfassung mit verlinkten Quellen (kein Primärtext gelesen); **FORMAL** = durch eigene, reproduzierbare Rechnung belegt; **STANDARD** = Normtabelle.

---

## ERR-010 – General-MIDI Pedal Hi-Hat (Befund: im Artefakt korrekt, Bericht falsch)

**Prüfung aller 12 PATs** gegen GM-Level-1-Percussion-Map (WEB_SECONDARY: Wikipedia „General MIDI“, RWTH-Tabelle; bestätigt 37 Side Stick, 42 Closed HH, 44 Pedal HH, 46 Open HH, 51 Ride 1, 54 Tambourine):

| PAT | Verwendete Noten | Befund |
|---|---|---|
| 001 | 38 Snare, 42 | ok |
| 002 | 39 Hand Clap, 46 | ok (39 = Hand Clap; Tabelle sagt „Clap/Snare (39)“ → präzisiert: 39 ist ausschließlich Clap) |
| 004, 005 | 37 als „Rimshot“ bzw. „Side-Stick“ | **ERR-010b:** GM 37 = Side Stick (Cross-Stick). Ein *Rimshot* (Stock trifft Fell und Rand gleichzeitig) hat in GM keine eigene Note; üblich ist 38/40 mit hoher Velocity. Bezeichnung in PAT-004 korrigiert zu „Side Stick (37)“. |
| 006 | 39 | ok |
| 009 | 36, 38, 42, 54 | ok |
| 010 | 36, 37 („Rimshot“), 42, 46 | **ERR-010b:** Reggae One Drop nutzt typischerweise Cross-Stick → GM 37 „Side Stick“ ist korrekt, das Wort „Rimshot“ ist falsch. |
| 012 | 51 Ride, 44 Pedal, 35 Kick | ok (Detailteil). Tabellenzeile erwähnt Hi-Hat nicht → ergänzt. |

**Notennummer vs. Notenname:** In der wissenschaftlichen Konvention (SPN, C4 = 60) ist MIDI 44 = **G♯2**, in der Yamaha/Cubase-Konvention (C3 = 60) = **G♯1**. STEPS speichert ausschließlich die Nummer; Namen nur mit explizitem Konventionsflag `octave_convention ∈ {SPN_C4_60, YAMAHA_C3_60}`. Rechnung: 44 = 12·(o+1)+8 ⇒ o = 2 (SPN). (FORMAL)

## ERR-011 – Backdoor-Familie und ♭VII

WEB_SECONDARY (Wikipedia „Backdoor progression“, fachords, antonjazz): Kerndefinition **iv7–♭VII7–I**, Herkunft parallel-Moll, Stimmführung A♭→G, F→E, oberer Leitton statt B→C; Beispiele „Lady Bird“, „Misty“ T. 4–5, „Yardbird Suite“.

| Variante | Beispiel C | ♭VII-Qualität | Vorbereitung | Einordnung |
|---|---|---|---|---|
| A ♭VII → I | B♭ → C | Dur-Dreiklang | keine | **Modale Mischung / „Mixolydische/äolische Kadenz“**; Rock/Pop. *Keine* vollständige Backdoor-ii–V. |
| B ♭VI → ♭VII → I | A♭ → B♭ → C (**PROG-011**) | Dreiklang | ♭VI | „Aeolian/Mario cadence“; Rock/Film. Teilt mit der Backdoor die Töne A♭→G und B♭→C, aber ohne Septime A♭ in ♭VII und ohne iv7. |
| C ♭VII7 → I | B♭7 → C | Dominantsept | keine | Backdoor-Dominante allein; Soul/Gospel. |
| D iv7 → ♭VII7 → I | Fm7 → B♭7 → Cmaj7 (**neu PROG-017**) | Dom7 | iv7 | **Klassische Backdoor-ii–V** (Jazz-Kerndefinition). |
| E IV → ♭VII7 → I | F → B♭7 → C (**PROG-014**, Datei) | Dom7 | IV (Dur) | Backdoor-Variante; IV statt iv – A statt A♭ als Vorgänger, d. h. das A♭ erscheint erst im B♭7. Gospel/R&B. |
| F ii7 → ♭VII7 → I | Dm7 → B♭7 → Cmaj7 (**neu PROG-018**) | Dom7 | ii7 | Gültige Backdoor-Variante: Dm7 und Fm7 teilen F, C; Dm7 ist „Ersatz-Vorbereitung“. Darf nicht verworfen werden, nur weil Fm7 fehlt. |

**Korrektur PROG-011:** Die Formulierung „Backdoor-Schluss“ in der Tabelle wird ersetzt durch „♭VII→I-Ganztonschluss (Backdoor-*verwandt*, keine vollständige Backdoor-Kadenz)“. **Korrektur PROG-014:** Tabellenspalte bleibt `IV–♭VII7–I`, Analyse ergänzt um Variantenbezug E; Bericht 4.5 („Dm7–B♭7–Cmaj7“) war falsch zugeordnet – diese Folge erhält eine eigene ID PROG-018.

Stimmführung (FORMAL, MIDI SPN): B♭7 [B♭3 58, D4 62, F4 65, A♭4 68] → Cmaj7 mit minimaler Bewegung: B♭3→B3 (+1), D4→C4 (−2), F4→E4 (−1), A♭4→G4 (−1) ⇒ [59,60,64,67] = Cmaj7 (B,C,E,G), L1 = 5. Front-Door G7 [B3,D4,F4,G4]→Cmaj7 [B3,C4,E4,G4]: L1 = 3.

## ERR-012 – Tuplet-Quantisierung (Bresenham-Behauptung)

Reproduzierbare Rechnung: `tuplet_reference.py` → `tuplet_reference_output.txt` (FORMAL).

| Fall | Ergebnis |
|---|---|
| Septole pro Viertel, 480 PPQ | Ticks 0, 69, 137, 206, 274, 343, 411, 480; Dauern 69,68,69,68,69,68,69 (Σ 480); max. Fehler 3/7 Tick |
| 960 PPQ | 0,137,274,411,549,686,823,960 (Σ 960) |
| 96 PPQ Quintole | Dauern 19,19,20,19,19 (480/5 ganzzahlig, 96/5 nicht!) |
| Septolen-Viertel über 4/4, 4 Loops, **absolut** gerundet | Taktstarts 0, 1920, 3840, 5760 – exakt |
| **naiv** (Dauer 274 aufsummiert) | Taktstarts 0, 1918, 3836, 5754 → **Drift −8 Ticks nach 4 Takten** |
| Round-Trip 1/7 → 69 Ticks → 23/160 | **nicht verlustfrei**; Rückgewinnung nur durch Raster-Snap (n = 7 Kandidat) |
| 24 PPQ, 1/56 Viertel | 0 Ticks → Note kollabiert |

**Korrigierte Spezifikation (ersetzt „Bresenham garantiert …“):**
1. Intern: absolute Position `Fraction` in Viertelnoten ab Songbeginn (nicht loop-relativ).
2. Export: `tick = floor(pos·PPQ + 1/2)` (round-half-up, deterministisch; Python-`round` ist banker's rounding und wird **nicht** verwendet). Dies ist äquivalent zu Bresenham-Fehlerverteilung, aber die Eigenschaft kommt aus der *absoluten* Rundung. Eigenschaften: |Fehler| ≤ ½ Tick je Event, kein kumulativer Fehler, Taktgrenzen exakt, wenn Taktlänge·PPQ ganzzahlig.
3. Loops: Events jeder Wiederholung aus absoluter Position neu berechnen, niemals gerundete Dauern addieren.
4. Gleichzeitigkeit: Events mit gleicher exakter Position → gleicher Tick (garantiert). Reihenfolge innerhalb eines Ticks: **Note-Off vor Note-On**; gleiche Taste: Off zuerst, um Abschneiden der neuen Note zu verhindern.
5. Mindestdauer 1 Tick; wenn Off ≤ On, Off = On + 1 und Warnung.
6. Tempoänderungen beeinflussen Ticks nicht (Ticks sind musikalische Zeit); Sekunden nur über Tempo-Map.
7. Round-Trip: Import tick → `Fraction(tick, PPQ)` exakt; Tuplet-Rekonstruktion ist heuristisch (Kandidatenraster 2,3,5,6,7, Toleranz ≤ ½ Tick) und als `INFERRED` zu markieren.
8. OA-0029-Text „96 bis 1920 PPQ … verlustfrei und ohne Rundungsjitter“ korrigiert (siehe Masterdatei).

Status: **SPECIFIED + reference-calculated**, nicht implementiert/getestet.

## ERR-013 – Pädagogische und stilistische Verallgemeinerungen

| ID | Fehlerhafte Aussage | Korrektur | Status |
|---|---|---|---|
| ERR-013a | PROG-015 „dominanter Progressionstyp moderner J-Pop- und Fusion-Harmonik“ / „asiatische Pop-Standard-Kadenz“ | „In japanischer Popmusik (J-Pop, Anime, Vocaloid) sehr verbreitet und als *Ōdō shinkō* (王道進行) benannt; keine Häufigkeitsmessung vorhanden; nicht für ‚asiatischen Pop‘ allgemein belegt.“ (WEB_SECONDARY: Wikipedia, fachords) | STYLE_DEPENDENT |
| ERR-013b | P07 Fingersatz | Spannen geprüft: C-Takt G3–E4 = 9 HT mit 1-2-5 (normal); G-Takt G3–D4 = 7 HT mit 1-2-4; LH C2–G2 = 7 HT (5-1). Für erwachsene Hände unproblematisch, für Kinder ggf. 1-2-4. **Fehler:** 4 RH-Töne pro Takt als „Achtel“ deklariert füllen nur 2 Schläge → Muster wird pro Takt **zweimal** gespielt (8 Achtel). Fingersätze = Vorschlag. | FORMAL |
| ERR-013c | P05 „Bewegung von nur einem Millimeter“; „Quinte liefert kaum Information“ | Halbton = Nachbartaste (Mittenabstand je nach Tastenpaar ca. 12–24 mm; nicht 1 mm). Quinte ist entbehrlich **nur** bei reinen Quinten; bei m7♭5, dim7, aug, 7♭5/♯5 trägt sie Akkordidentität. | FORMAL |
| ERR-013d | PAT-011 „Afrobeat Shuffler (Tony Allen)“ als repräsentatives Pattern | Ein Pattern repräsentiert Afrobeat nicht; Allen variierte stark, Bassdrum mit Doppelschlägen und Synkopen auf „e/a“, Hi-Hat mit offenen Akzenten auf 16tel-Offbeats, Rolle im Ensemble mit Bass, Gitarren, Perkussion (WEB_SECONDARY: Modern Drummer, Drummerworld-Zusammenfassung). Status → `ILLUSTRATIVE_SKETCH`, nicht `REFERENCE`. ρ≈1,18 ohne Quelle → entfernt (OPEN_QUESTION). | STYLE_DEPENDENT |
| ERR-013e | PAT-009 „Motown-Geheimnis … z. B. *Can't Hurry Love*, *Uptown Funk*“ | *Uptown Funk* (Mark Ronson ft. Bruno Mars, 2014) ist **kein** Motown-Titel → gestrichen. Viertel-Snare/Tambourin ist ein *häufiges* Merkmal mittlerer 1960er-Motown-Hits (Funk Brothers: Benny Benjamin, Richard „Pistol“ Allen, Uriel Jones), nicht ein universelles „Gesetz“; viele Motown-Titel haben klassischen 2/4-Backbeat. (WEB_SECONDARY: Motown Museum, oddgrooves) | STYLE_DEPENDENT |
| ERR-013f | PAT-012 „Schlag 2: Punktierte Viertel + Triolen-Achtel“, ρ = 2,0 als Feel | Ticks 480/800 sind korrekt (Viertel auf 2, Triolen-Achtel auf „2-let“ = 480+320). Bezeichnung korrigiert: „Viertel + geswingte Achtel auf ‚2+‘“. ρ ist tempoabhängig: ≈ 3,5:1 langsam, ≈ 2:1 mittel, → 1:1 schnell; kurze Achtel ≈ 100 ms (Friberg & Sundström 2002, *Music Perception* 19(3), WEB_SECONDARY). Bei 130 BPM ist 2:1 plausibel, aber Parameter, kein Gesetz. | THEORY_SUPPORTED |

## Weitere in dieser Sitzung gefundene Fehler

| ID | Ort | Fehler | Korrektur |
|---|---|---|---|
| ERR-014 | P06 / REF-0040 | Cadd9 als `C4-D4-E4-G4` bei Text „D in der nächsten Oktave“; „keine Dissonanz“ | Lage C4-D4-E4-G4 ist streng **Cadd2**; Cadd9-Lage: `C4-E4-G4-D5`. Tonklassenmenge {0,2,4,7} identisch → REF-0040 bleibt auf PC-Ebene gültig, Erwartung um Lagenhinweis ergänzt. C–D und D–E sind große Sekunden (milde Dissonanzen) → „klingt weich-schwebend, enthält milde Sekundreibung“. |
| ERR-015 | PAT-010 Tabelle | „16tel“ und „Halftime“ vs. Tick-Tabelle in Achteln | Tick-Tabelle (Achtel) maßgeblich; „Halftime“ = Wahrnehmungsbeschreibung, nicht Notation. Offene HH auf allen Offbeats ist *eine* Option, nicht Standard (WEB_SECONDARY: Hi-Hat 8tel/16tel, oft Offbeat-Betonung). |
| ERR-016 | REF-0037/0038 | `source_evidence` „Reggae Rhythms Analysis“, „Motown Rhythm Section“ – **nicht existierende/nicht identifizierbare Quellen** | Ersetzt durch die tatsächlich in 4.6 gelesenen Websekundärquellen; Status bleibt STYLE_DEPENDENT. |
| ERR-017 | REF-0035/0036/0039 | Buchquellen (Levine, Kostka/Payne „Tonal Harmony“, Spencer) ohne Fundstelle, nie gelesen | Markiert `SOURCE_UNREAD`; REF-0036 Quelle ersetzt durch Backdoor-Websekundärquelle. Kostka/Payne behandelt die Jazz-Backdoor nicht nachweislich. |
| ERR-018 | REF-0036 | Stimmführung „A♭→G und B♭→C“ | korrekt, ergänzt um F→E und D→C bzw. D→E; Leitton B fehlt. |
| ERR-019 | PROG-011 Tabelle 4.5 | „Backdoor-Schluss“ | s. ERR-011 Variante B |
| ERR-020 | Phase-4.5-Chatbericht | PAT-, PROG-014/016-, P07-, Hash-Angaben | s. REFERENCE_ID_INTEGRITY_REPORT §3 (nur Bericht, keine Datei) |
| ERR-021 | Masterdatei | Summary-Tabelle enthält nur 21 von 30 Aufgaben; OA-0020/21 Status ohne Backticks; OA-0029 widerspricht Phase-4.5-Präzisierung | behoben (siehe §Aufgaben in NEXT_SESSION_HANDOVER) |

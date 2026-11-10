# Band III — CHORD PROGRESSIONS: Harmonie in Zeit, Form, Stil und kompositorischer Absicht

## 1. Eine Akkordfolge ist ein musikalischer Vorgang, kein String-Array

`C | Am | F | G` beschreibt zwar vier Symbole, lässt aber Grundfragen offen: Wann beginnt der Akkord? Wie lange dauert er? Welche Melodie klingt darüber? Gibt es eine Kadenz, einen durchlaufenden Bass, eine Phrase oder ein Loop? Ist C Tonika oder nur scheinbares Zentrum? Wie sind Akkorde gesetzt? Ein strukturiertes Steps-Progression-Objekt benötigt `chord_event` mit onset, duration, root spelling, inversion, voicing, texture, local/global key und `analysis[]`.

Ein abstraktes Progressionsmuster kann unter Transposition erhalten bleiben. Eine konkrete Notenschreibung kann sich jedoch verändern: Beim Transponieren von `C–G7–C` nach F# sollten die passenden Akkorde `F#–C#7–F#` korrekt als E# in der C#-Dominante buchstabiert werden, nicht als F naturals bloßer Pitch-Class-Umrechnung. Eine Roman-Analyse kann nicht einfach die Songtonart ersetzen, wenn eine klare Modulation vorliegt.

## 2. Sechs unterschiedliche Arten von Progressionsidentität

1. **Chord sequence identity:** exakt dieselben Symbole, z.B. `C–G–Am–F`.
2. **Roman/functional identity:** `I–V–vi–IV` in mehreren Durtonarten; Transposition erhält Stufenstruktur.
3. **Rotation-equivalent loop:** `I–V–vi–IV` und `vi–IV–I–V` gehören zu einer zyklischen Familie, können aber andere Ankunfts-/Downbeat-Effekte haben.
4. **Voice-leading neighborhood:** zwei Folgen können ähnlich in ihren Stimmen, aber völlig verschieden in der Tonartrelation sein.
5. **Harmonic-rhythm identity:** gleicher Akkordplan mit gleichbleibenden Einsätzen/Dauern – oder bewusst veränderter rhythmischer Akzentuierung.
6. **Formal-process identity:** Verse/Prechorus/Chorus kann eine längere harmonische Ankunft modellieren, obwohl einzelne Akkorde einer Loopform entsprechen.

Der Progressionsatlas darf diese sechs Relationen nicht durch einen einzigen `same_pattern`-Boolean nivellieren.

## 3. Urtypen der Funktionsharmonik

| Typ | Beispiel C-Dur | Funktionale Lesart | Nicht zulässige Verallgemeinerung |
|---|---|---|---|
| Authentische Schlussbewegung | Dm7–G7–C | ii–V7–I, PD–D–T | Nicht jeder G7–C ist formale Kadenz |
| Plagale Färbung | C–F–C | I–IV–I | Der Begriff „Plagal“ ist nicht für jeden IV–I-Loop zwingend |
| Circle movement | Em7–Am7–Dm7–G7–Cmaj7 | iii–vi–ii–V–I | funktionales Gewicht je Phrase variabel |
| Deceptive cadence | C–G7–Am | I–V7–vi | täuschende Wirkung braucht Kadenzkontext |
| Applied dominant | C–A7–Dm–G7–C | I–V7/ii–ii–V7–I | A7 beweist keine Modulation |
| Borrowed iv | C–F–Fm–C | I–IV–iv–I | iv muss nicht zwingend „traurig“ heißen |

## 4. Moll als Verlauf und nicht als starre Skala

`Am–Dm–E7–Am` ist ein kompaktes i–iv–V7–i-Modell. Bei `Am–F–G–Em` fehlt die leittönige Dominante; dennoch kann die Folge in Aeolisch/Moll-Songwriting völlig plausibel sein. Für ein 16-Takt-Beispiel lässt sich ein kompositorischer Bogen bilden: A: `Am–G–F–E7` (Abstieg und Dominantziel), A': `Am–Dm–E7–Am` (Antwort und Tonikaziel), B: `C–G–Dm–E7` (Relative-Dur-Farbe mit Rückzug), A'': `Am–F–E7–Am` (Verdichtung). **Jede Vierergruppe** bekommt Taktzeiten, Melodie und Bass, bevor sie als formale Erklärung freigegeben wird.

## 5. Rock, Pop und Loops

`C–G–Am–F` lässt sich als I–V–vi–IV in C beschreiben, aber die simple Roman-Folge ersetzt nicht Produktionsrhythmus, Hook-Position und Melodiebetonung. Eine Rotation `Am–F–C–G` kann einen a-Moll-orientierten ersten Eindruck erzeugen. Wiederholtes C–Bb–F–C kann Mixolydisch/rocktypisch klingen, muss jedoch nicht als *klassische* Subdominantdominantharmonik etikettiert werden. Spicers `fragile/emergent/absent tonic` [V5-005] fordert sogar Analysen ohne erklingenden I-Akkord. Nobile [V5-003] zeigt, warum Verse-/Chorus-Struktur als harmonischer Prozess, nicht nur als Aneinanderreihung, zu verstehen ist.

**Arbeitsfall:** Verse `Am–F–G–G` im viermaligen Loop, Prechorus `Dm–F–G–G` mit steigendem Register, Chorus `C–G–Am–F`. Das Werk kann den Chorus-Anfang als erstes deutliches C-Zentrum inszenieren. Der Algorithmus soll dort ein `emergent_tonic`-Hypothese anbieten, nicht sie automatisch als bewiesene Analyse festschreiben.

## 6. Jazz: lineare und lokale Ziele

- ii–V–I: `Dm7 | G7 | Cmaj7`. Je nach Metadaten kann dieselbe Kadenz ein kurzes Fragment oder eine mehrtaktige Phrase sein.
- Extended turnaround: `Cmaj7–A7–Dm7–G7` (I–V/ii–ii–V), im Loop mit nachfolgender Tonika.
- Tritone substitution: `Dm7–Db7–Cmaj7`. Die Oberstimmen B/F und Cb/F können Leittonbezüge erhalten, aber Bassbewegung ändert sich.
- Backdoor: `Fm7–Bb7–Cmaj7`, eine andere Klang- und Satzbeziehung als `G7–Cmaj7`.
- Side-slip: `Dm7–Ebm7–Dm7–G7` als chromatische Verzierung. Die Zwischenharmonie ist nicht zwangsläufig ein modulierender Funktionsakkord.
- Modal jazz: `Dm9–Em9` über D-Pedal kann als modal-/planend gemeint sein; die kategorische Kennzeichnung „ii–iii“ wäre im D-Zentrum methodisch fraglich.

## 7. Blues: 12 Takte als Formgerüst

Das traditionelle 12-Takt-Schema in C ist `C7 | C7 | C7 | C7 | F7 | F7 | C7 | C7 | G7 | F7 | C7 | G7`. Dass C7 als I7 tonikal und F7 als IV7 auftreten, erklärt eine gesonderte Blues-Analyse besser als ein klassisches Durdiatonik-Fehlermodell. In Blues kann ein Turnaround die letzten zwei Takte mit melodischer Chromatik oder Dominantvarianten ausfüllen. Ein guter Steps-Generator fragt nach Formvariante, Bassbewegung und Interaktion mit Blues-Melodik, statt alle Blues mit einem identischen Zwölftaktschema gleichzusetzen.

## 8. Chromatische Farbprogressionen

`C–E–Am–Ab–G7–C` kann E als `V/vi` in C mit nachfolgendem Am erklären; Ab ist eine chromatische bVI-Farbe und kann durch Stimmenbewegung Richtung G7 führen. Eine alternative Lesart wäre passagenweise tonikalisierende Harmonisierung der chromatischen Basslinie. Beides setzt voraus, dass `E` tatsächlich Durqualität inklusive G# hat. `C–Em–Am–Ab` ist ein anderer Verlauf.

`Cmaj7–Ebmaj7–Abmaj7–Dbmaj7` erzeugt eine Folge stark chromatischer farbiger Klangfelder. Ohne Tonzentrum/Kadenz sollte sie nicht künstlich als Kette von Tonika, Subdominante, Dominante deklariert werden. Stimme, Farbe, Register und Compound-Timbre können hier wichtiger sein.

## 9. Reharmonisierung einer gegebenen Melodie

Annahme: Originalmelodie in C, vier Takte mit starken Tönen `[E4, D4, C4, B3]` jeweils auf Beat 1. Eine erste Harmonisierung `[Cmaj7, G7, Am7, G7]` enthält E als Terz von Cmaj7, D als Quinte von G7, C als Terz von Am7, B als Terz von G7. Eine Alternative `[Am7, Dm7, Fmaj7, G7]` enthält E als Quinte von Am7, D als Grundton von Dm7, C als Quinte von Fmaj7, B als Terz von G7. Zwei legitime Sets können dieselbe Topline harmonisieren, ohne dass eines „die“ Lösung ist.

Eine bewusst dissonantere Alternative mit `Db7` unter D4 erzeugt b9 gegen Db – mit geeigneter Lage/Auflösung eine Spannung, **nicht automatisch einen Fehler**. Ein Melody-Fit-Score muss `strong_beat`, `note_role`, `resolves_to`, `style_scope` und reale Tonhöhen berücksichtigen.

## 10. Bass- und Inversionsplanung

Vergleiche in C die Oberflächen `[C, G, Am, F]` gegen `[C/E, G/D, Am/C, F/A]`. Beide teilen dieselben abstrakten Akkordwurzeln, aber der Bass bewegt sich E–D–C–A statt C–G–A–F. Die lineare Bassrichtung und die Bassauflösung sind deutlich verschieden. Ein kompositorischer Schritt ist daher oft: zuerst Harmonie grob planen → Bassbewegung entwerfen → Inversionen prüfen → Voicings ableiten → Melodie adaptieren. Ein reiner Akkordvorschlagsautomat überspringt diese Ebene.

## 11. Harmonic Rhythm: derselbe Satz anders empfunden

Vier Akkorde `Cmaj7–Am7–Dm7–G7` können vier Takte lang jeweils einen Takt halten oder als rhythmische Folge `[6,2,4,4]` Beats über vier 4/4-Takte laufen. Die Grundakkordreihenfolge bleibt gleich, aber die tonikale Prolongation und der Dominanteinsatz ändern sich. Für eine Kadenz darf nicht nur die letzte Akkordposition, sondern die metrische und formale Stärke bewertet werden.

## 12. Vorschlag: mindestens fünf verschiedene Rankings nebeneinander

Ein Kandidat `F minor` nach C major kann je nach Einstellung verschiedene Begründungen besitzen: „Mischung aus Parallelmoll“, „kleine Bewegung zweier Stimmen“, „chromatische Farbe“, „möglicher Weg zu E oder G“, „passend zur vorliegenden Melodie“ – dies sind nicht dieselbe Evidenzart. Die UI soll sie getrennt und ohne fiktive Konsens-Wahrscheinlichkeiten anzeigen.

**Ein Ranking braucht:** (1) klar definierte Features, (2) Gültigkeitsbereich, (3) Datengrundlage, (4) Gewichtung/Methode, (5) Referenzgegenbeispiele, (6) Nutzerkontrolle. Ohne Benchmark sollte ein „Best Score 0.93“ nicht angezeigt werden.

## 13. Progression Data Contract – technisch ausführbarer Entwurf

```json
{
  "id": "V5-PROG-DEMO-001",
  "status": "pedagogical_draft",
  "key": {"tonic": "C", "mode": "major"},
  "meter": {"numerator": 4, "denominator": 4},
  "tempo_bpm": 100,
  "sections": [{"id": "A", "start_bar": 1, "end_bar": 4}],
  "chord_events": [
    {"onset_beats": 0, "duration_beats": 6, "symbol": "Cmaj7", "root": "C", "bass": "C"},
    {"onset_beats": 6, "duration_beats": 2, "symbol": "Fmaj7", "root": "F", "bass": "F"},
    {"onset_beats": 8, "duration_beats": 4, "symbol": "Dm7", "root": "D", "bass": "D"},
    {"onset_beats": 12, "duration_beats": 4, "symbol": "G7", "root": "G", "bass": "G"}
  ],
  "analyses": [{"lens": "functional", "roman": ["Imaj7", "IVmaj7", "ii7", "V7"], "status": "interpretation"}],
  "provenance": {"type": "original_pedagogical_example"}
}
```

**Invarianten:** Ereignisse in einem Layer überlappen nicht, onsets sind zeitlich sortiert, die Summe der endlichen Ereignisse ist vom Section-Length abhängig, jede notierte Tondauer ist positiv, jeder gespielte Ton besitzt eine Stimme/Instrument oder explizit instrument-unabhängige Voice-ID. Eine Funktionsdeutung bleibt ein separates Interpretationsobjekt.

## 14. Vergleich: Was Korpusstatistik leisten kann

Temperley berichtet für ein konkretes historisch selektiertes Pop/Rock-Material Ergebnisse zu cadential IV und V [V5-007]. Aus einem solchen Korpus lassen sich bedingte Häufigkeiten berechnen, wenn zuvor Segmentierungs- und Analysekriterien festliegen. Sie dürfen weder als „alle Rockmusik“ noch als „universell guter Akkord“ bezeichnet werden. Die Codex-Pipeline sollte Stichprobenverteilung, Genre, Epoche, Zeitdauer, Lizenz und Annotation Consensus stets mit ausgeben.

## 15. Abnahmeprotokoll je Progressionsfamilie

- **Notation:** Alle Akkordtöne und Funktionssymbole überprüft?
- **Key-Analyse:** Gibt es mindestens einen belegten Grund für das angenommene tonale Zentrum?
- **Form:** Sind Start-/Endpositionen, Phrasen und Kadenzen bezeichnet?
- **Alternativen:** Ist eine zweite plausible Lesart dokumentiert, falls vorhanden?
- **Komposition:** Ist eine eigenständige Variation durch Reharmonization, Inversion, Rhythmus oder Voice Leading ausgearbeitet?
- **Korpus:** Werden Frequency-Claims nur bei realen Daten und klarer Stichprobe gemacht?
- **Rechte:** Originalbeispiel vs. fremdes Werk ausdrücklich getrennt?

**Forschungsanker:** [V5-005] Spicer, [V5-007] Temperley, [V5-008] Biamonte, [V5-010] DCML, [V5-011] ChoCo, [V5-012] When in Rome, [V5-026] music21. Diese Quellen belegen nicht automatisch jedes von uns frei entworfene Lehrbeispiel.

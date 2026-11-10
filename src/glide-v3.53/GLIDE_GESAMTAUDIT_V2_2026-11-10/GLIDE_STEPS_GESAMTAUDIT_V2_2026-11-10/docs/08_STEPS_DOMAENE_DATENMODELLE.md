# 08 — Steps-Domänenarchitektur, Rhythmus, MIDI und Schema-Review

## Was im Repository nachgewiesen ist

`src/steps/` ist ein Verzeichnis mit README-Platzhaltern; `app/` ebenso. Das Root-`VERSION` meldet `0.0.0-dev`; die fünf JSON-Schemata sind Draft 2020-12 Startformen. Der vorhandene Strukturtest (`tools/validation/check_structure.py`) prüft Pfadexistenz, parsebares JSON, `$schema`-Kennung und nichtleere `required`-Liste; er führt **keine** semantische Schemaprüfung, Music-Theory-Unit-Suite, MIDI-Export oder GUI-Annahme aus. `knowledge/sources/registry.yaml` enthält `sources: []`. Ein erfolgreiches CI-Ergebnis dieses Tests ist für diese beschränkte Aussage korrekt, aber für eine musikalisch funktionierende App nicht aussagekräftig.

## Befund am Schema, direkte Dateiinspektion

| Objekt | Nachgewiesene Eigenschaften | Fehlender oder ungeklärter Vertrag (Vorschlag) |
|---|---|---|
| `chord.schema.json` | required `root`, `quality`; freie Strings; optionale Intervalle 0–23, `spelling_system`, `bass`, `inversion` | normalisierte PitchClass+Schreibweise+Oktave, chord quality ontology, Akkordtöne / Doubling / slash notation, enharmonischer Kontext, Validierungsregeln |
| `progression.schema.json` | required `notation`, `bars`; `bars[].chords` nichtleere Stringliste; optional `key`, `time_signature`, `tempo_bpm`, `style` | **keine** Akkorddauern, Taktpositionen, ungleich lange Sections, Pausen, Transposition aus Objekt, Tempo-Map, Repeat/Loop IDs, Drums/velocity/humanization |
| `analysis.schema.json` | interpretations[] mit framework/explanation, optional confidence und Quelle | Aussage zu Gültigkeitsbedingungen/Stil/Schlüssel, alternative Evidenz, Provenienz pro Relation, algorithm vs pedagogy |
| `concept.schema.json` | id, term, definition, source_ids, status, alternatives | Sprachversion, fachliche Schule/Gültigkeit, Definition vs Interpretation, Referenzanker/Revision und Prüfer |
| `source.schema.json` | id/title/rights_status/kind required, License optional | Rechteentscheidung ohne bloßes Label, Fundstelle/Seite, Umverteilungs-/Zitierrecht, Lizenznachweis, Publizierungszweck, Dritt-/Originalmaterial, verifizierter Hash |

**Korrektur:** Schema-Dateien sind zunächst *Prototypen*. Ein neuer Domänenvertrag braucht Versionierung und Migration; er darf nicht einfach die vorhandenen Schemas still überschreiben. Source-Schema und `registry.yaml` als getrennte Verantwortlichkeiten interpretieren, nicht automatisch mit Runtime-Projektdateien mischen.

## Empfohlene fachliche Kernmodelle (PROPOSED)

- `PitchClass` und `SpelledPitch` getrennt: chromatische Klasse 0–11 **plus** Buchstabennamen, Vorzeichen, Tonhöhen/Oktave; DE `H/B` gegen international `B/Bb` explizit im Parser, internal representation unabhängig von UI-Sprache; keine Annahme, enharmonische Gleichheit sei Funktionsgleichheit.
- `Interval` mit diatonischer Stufe, chromatischen Halbtönen und Qualitätsbezeichnung; rein semitonisches Intervall verliert z. B. übermäßige vs. kleine Bezeichnung.
- `Scale`/`Mode` als Notenfolge, Grundton, Familie, Spelling-Kontext und Tonmaterial; Styles wie Jazz/Pop/klassische Funktionslehre nur explizit als Regeln/Interpretationsrahmen.
- `ChordSymbol` und `Voicing` getrennt: Symbol benennt Harmonie/Extensions/Alterations, Voicing einzelne MIDI-Pitches/Spielbarkeit/Register, Bassnote getrennt. Nicht jeder Akkord hat eindeutige funktionale Deutung.
- `HarmonicEvent`: stabile ID, `chord_ref`, `start` und `duration` als rationale musikalische Position, ggf. articulation/velocity/muted/rest, Section. Takte allein sind keine präzisen Eventpositionen.
- `Progression`: geordnete HarmonicEvents, Taktart, Tempokontext, Wiederholungs-/Section-Semantik, Notation preference, technische Schema-Version; musikalische Analyse als **separates** Objekt, nicht in harmonierelevante Werte fest eingebacken.
- `DrumPattern`: Step-Grid mit `pattern_length`, `steps_per_beat`/rationalen Offsets, kit mapping (Pitch/Instrument), velocities, swing/offset/probability (erst nach explizitem Scope), Tuplet/Swing-Repräsentation; pattern event IDs erhalten.
- `Arrangement`/`Timeline`: Chord/Drum-Spuren in gemeinsamer Zeitbasis als nichtdestruktive Referenzen auf Events/Patterns; klare Loop-/Taktgrenzen und Stop/Start-Semantik.
- `AnalysisCandidate`: Rahmen (`functional`, `modal`, `jazz`, `popular`, etc.), Schlüssel/Modus/Stil, Evidence IDs, Voraussetzungen/Limitierungen, Konfidenz *nur bei kalibrierter Methode*, Alternativen ohne vorgetäuschte Sicherheit.
- `ProjectDocument`: Produkt-/Schema-Version, ID und Provenienz, Bearbeitungs- und Austauschmetadaten, content-IDs und optional referenzierte Medien; keine Glide-Aufgabenstruktur.

## Rhythmus- und MIDI-Referenzrahmen

**Positionsarithmetik:** Für reine Musiklogik rationale Beatpositionen (`Fraction`) oder klare Tickauflösung; bei Konversion in SMF-PPQ müssen alle Eventpositionen durch konsistente Rundung/Quantisierung abbildbar sein. Ein Export kann nicht beliebige nichtquantisierte mathematische Positionen exakt darstellen; Ein-/Ausgabe darf das offen protokollieren.

**MIDI-1-Standarddatei:** Bevor Export funktioniert, SMF-Type (0/1), Trackstruktur, Ticks-per-beat, Tempo-Metaevent (Mikrosekunden pro Viertelnote), Taktart-Metaevent, Note-On/Note-Off, Kanal, Drum-Channel-Konvention, Delta-Zeit, Reihenfolge bei identischem Tick, End-of-Track, Velocity, Pitchrange und Note-Off/Zero-Velocity prüfen. `mido` ist ein möglicher Adapter, kein zwingend bereits beschlossenes Runtime-Dependency. **MIDI ist kein Audio**: Export ist ohne eingebauten Synthesizer möglich; hörbare Wiedergabe braucht eine gesonderte, betriebssystem-/soundfontabhängige Lösung und eventuelle Latenz-/Lizenztests.

**Sonderfälle:** Auftakt, Tempoänderung, MIDI-Clock vs. Datei, beliebige Taktarten, Drums und Akkorde auf gemeinsamen Beats, verkürzte letzte Takte, Repeats/alternierende Enden, Triolen, Swing, Short Notes, Panic/Note-Off bei Stop. Groove-Qualität kann nicht allein an Ticks/Metronom gemessen werden; für Abnahme sind Hör-/UX-Gegenproben sinnvoll.

## Pflicht-Golden- und negative Tests

1. International `B` = deutsches `H`; deutsches `B` = international `Bb` und beide als verschiedenen Namen derselben Tonklasse nur wenn korrekt spezifiziert. Test mit enharmonischen Tonarten (F# / Gb) statt bloß C-Dur.
2. `Cmaj7` ≠ `C7` ≠ `Cm7`; Qualität und spezifische Töne prüfen. `E7→Am` in a-Moll typischerweise V7–i und in C-Dur sekundäre Dominante V7/vi; ohne Kontext keine absolute Rollenbehauptung.
3. Voicing-Optimierung darf Symbol/ChordQuality nicht umdefinieren und darf absichtlich hohe/ tiefe Basstöne erhalten, wenn fixiert.
4. Notation/Serializer Roundtrip: Alle geprüften musikalischen Eigenschaften erhalten oder klar als verlustbehaftet ausgeben; nicht nur `json.loads` erfolgreich.
5. Progression-Länge mit 3/4 und 5/8; position/duration konsistent, keine End-Überläufe; negative Start-/Dauerwerte werden zurückgewiesen.
6. DrumPattern 16 Steps: Trigger/Velocity/Kanal, 32 Steps und fehlende Hits; Swing/Offset darf NoteOrder nicht umkehren; ein gesetzter Step landet an der erwarteten Tickposition.
7. MIDI-Export gegen unabhängigen Parser re-importieren, Eventzeiten, Tonhöhen, Kanäle und Metaevents vergleichen; leere Folge/ungültiges Tempo/korruptes Eingangs-MIDI kontrolliert ablehnen.
8. Undo/Redo: Event löschen, neue Note erzeugen, Undo, neu laden, Redo, Cache/View erneut berechnen; keine stale IDs nach Wiederherstellung.
9. Unbekannte Lizenz/Quelle: Skill gibt keine konkrete fremde Textstelle erfunden aus und erfindet keine Buchseiten.
10. Musik-Domain-Import bei deaktiviertem DISPLAY/ohne Tk muss funktionieren; UI-Import darf keine produktiven Dateien berühren.

## Research/Produkt-Abgrenzung

Die beiden Research-Dokumente empfehlen einen deterministischen, provienzbewussten Theory Engine-Ansatz und eine getrennte Skill-Schicht. Das ist eine plausible Architekturidee, keine ausgewertete Genauigkeitsmessung. Externe Korpora wie ChoCo/When in Rome sowie Standards müssen vor Ingestion auf Lizenz, Format, Annotationstiefe, Musikstil-Bias und Kosten geprüft werden. Klassische Funktionstheorie, modale, Jazz- und Pop-Perspektiven liefern unterschiedliche Deutungen; ein 'einfacher chord-to-next-chord Algorithmus' wäre didaktisch unzureichend. **Weitere DAW-/Mixing-/Masteringforschung bleibt ein eigenes Zukunfts- oder Archivprogramm**, sofern kein separater Produktbeschluss.

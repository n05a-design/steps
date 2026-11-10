# STEPS Codex Masterauftrag V6.0 — moderne Musikproduktion als überprüfbare Wissensbasis

## Auftrag und Grenzen
Integriere die neue V6.0-Informationsarchitektur nach Repository-Audit **ohne** frühere Dateien ungesteuert zu verschieben. Ziel ist ein pflegbares, source-aware Knowledge-System, kein stiller Umbau von STEPS zur vollwertigen DAW. Die vier Ursprungsdomänen plus Drums plus Producer Tools bleiben als Kern. Neue Kategorien 16–44 sind recherchierte Felder; Umsetzung nur mit expliziter Priorisierung.

### Sicherheitsregeln
- Keine automatisch veranlasste Merge-Aktion; Änderungen in separater Branch/PR.
- Nie Nutzerdateien oder Kursmaterial mit ungeklärter Lizenz veröffentlichen, keine Fan-Remake-MIDI als frei verfügbare Originals deklarieren.
- V5.4-Basis-Hashes bewahren und vor Integration vergleichen; V5.4-ZIP = Source of Truth. Entpackter Arbeitsstand besitzt 126 zusätzliche nicht kanonisch eingestufte Dateien.
- Dateinamen, Category IDs, Typen und Versionsangaben stabil halten; Migrationen reversibel und mit Test.
- Automatisierte Parser- und Schematests ersetzen keine musikalischen Reviews, und keine Stilregel ist eine universelle Naturkonstante.

## Phasen und Arbeitspakete
### AP-00 — Repository-Audit
**Aufgabe:** Branch, Softwarearchitektur, vorhandene Datenmodelle, Python-Versionen und CI auf macOS/Windows/Linux auslesen; kein impliziter Zugriff.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-01 — Bibliothek konsolidieren
**Aufgabe:** V5.4-Hashliste verifizieren, V6.0-Importer bauen, frühere neue/alte Kopien sichtbar erhalten.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-02 — Taxonomie vereinheitlichen
**Aufgabe:** 01–15 + 16–44 als stabile Domain-IDs mit eindeutiger Suche und Crosslinks verwenden.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-03 — Quellen- und Lizenzmodell
**Aufgabe:** Claim-Level-Evidence, Rechte, Zugriffsstatus, Versionsstand, Widersprüche und Haftungshinweise.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-04 — MIDI-Quelle lokal prüfen
**Aufgabe:** Original-MIDI & ZIP/Readmes in tatsächlichem Steps-Ordner suchen, Dateihashes, NoteOff, CC, Tempo, Time Signature auslesen.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-05 — Pitch-/Zeitachsenmodell
**Aufgabe:** MIDI-Nummer vs DAW-Oktave, Tick-Quarters-Units, Swing und Microtiming korrekt trennen.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-06 — Stilkontexte
**Aufgabe:** Genregrammatik als weiche Tendenz, kulturelle Quellenkritik und mehrere plausible Analyse-Lenses.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-07 — Chord Progressions
**Aufgabe:** bestehende Akkord-/Analyse-Logik fachlich und schema-technisch erhalten, echte Primärtests.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-08 — Composing
**Aufgabe:** Melodie-/Motiv-/Form-Workflows mit originalen Beispielen, Instrumentationsreviews.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-09 — Groove-Modell
**Aufgabe:** Kick, Snare, Hats, Sub, Velocity, Events, Swing, humanization mit editierbarer Zeitreferenz.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-10 — Producer-Tools-Knowledge
**Aufgabe:** Synthesis, Sampling, Vocal, Mix, Master als Knowledge Cards mit Eingriffsfolgen und Checklisten.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-11 — Session-Objekte
**Aufgabe:** DAW-neutraler Projekt-/Clip-/Automation-/Routing-Entwurf, keine Plugins als Voraussetzung.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-12 — Recording & Mic
**Aufgabe:** Nur erklärbare Knowledge-/Checklistenobjekte; keine versprochene Audioeingabe vor Hardware-/OS-Test.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-13 — Vocal-Production
**Aufgabe:** Consent, Formant/Pitch-Korrektur, Comping/Layering Datenmodell, keine Voice-Cloning-Default.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-14 — Sound-Design
**Aufgabe:** Envelope/Filter/Modulation/Tuning als theoretische Parameterdaten, Pluginnamen optional.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-15 — Mix-Entscheidungslab
**Aufgabe:** Level-Match A/B, Mono-Test, Masking-Hypothesen, mehrere Lösungen ohne pauschale Gewinner.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-16 — Mastering/QC
**Aufgabe:** EBU/ITU/Spotify als kontextspezifische Standards, nie -14/-23 LUFS als universelles Masteringgesetz.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-17 — Immersive
**Aufgabe:** Bed/Object/Renderer-Kontext, Ausgabe-/Hör-QC als Recherche zuerst, nicht volle Atmos-Engine bauen.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-18 — Interoperabilität
**Aufgabe:** MIDI1/2, MusicXML, WAV/FLAC/ADM, DAW-Stereo-Stems: Import/Export-Verlustmodelle.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-19 — Spiel- und Filmmusik
**Aufgabe:** State-Graphen, Transition-Check und Cue Sheets; Middleware später.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-20 — Live/DJ
**Aufgabe:** Performance-Metadata, Cue-Szenen, MIDI-Mapping als Wissensebene; echtes Hosting nicht implizit.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-21 — Collaboration
**Aufgabe:** Asset-Metadaten, Versionen, Stems, Projektabgabe, Zugriff und Freigabe.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-22 — Rights/Release
**Aufgabe:** ISRC≠ISWC, Splits, GEMA/GVL, DDEX-Metadaten, Release-Blocker bei ungeklärter Lizenz.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-23 — Responsible AI
**Aufgabe:** Provenienz, Privacy, Consent, Evaluation, Opt-in, kein ungenehmigtes Fremd-Stimmtraining.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-24 — Accessibility
**Aufgabe:** Screenreader, Keyboard-only, Farbunabhängigkeit, alternative rhythmische Textrepräsentationen.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-25 — Bibliothek-UI
**Aufgabe:** Suche, Filter, Domain, Status, Text/MIDI-Verknüpfung und Herkunft pro Wissenskarte.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-26 — Testing
**Aufgabe:** Schemavalidation, Pitch/Time-Goldens, Source-License-Tests, nicht ausgeführte Audio-Tests als pending.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

### AP-27 — Review & Handover
**Aufgabe:** CI-Bericht, offener Lückenstand, Prüfsummen, Freigaben, PR Beschreibung, kein Merge ohne Benutzerentscheidung.
**Abnahme:** dokumentierte konkrete Pfade/Datenobjekte, ausgeführte Prüfungen mit reproduzierbarem Ergebnis und offengelegte Restunsicherheit. Bei Blocker nicht stumm überspringen.

## Akzeptanzmatrix
- **Data correctness:** Klassifizierte Felder und stabile IDs; Fehlermeldungen für ungültige Dateinamen, Duplikate, Zeit-/Notennummern.
- **Source correctness:** Einzel-Claims besitzen Fundstelle und Prüfstatus; fremde Quelltexte werden nicht mitkopiert.
- **Creative quality:** Fachliche Hörbewertungen werden von echten Fachmenschen bzw. Nutzern getrennt dokumentiert; kein numerischer Scheinbeweis.
- **Repo impact:** Keine Spekulation über bestehenden Code; Integration nach Testinventar.
- **Product scope:** Knowledge first, anschließend im PR eine begründete Vorschlagsliste für technisch machbare Features.

## Startreihenfolge
`00_NAVIGATION/STEPS_V6_0__START_HIER-Gesamte-Produktionskette__WEGWEISER__V6_0.md` → `...PRODUKTIONSLANDKARTE...` → `...THEMENREGISTER...json` → `...GAPREGISTER...` → `10_QUELLEN_LIZENZEN/...REGISTER...json` → `11_VALIDIERUNG_QUALITAET/...TESTPLAN...json` → dieser Auftrag.

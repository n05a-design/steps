# STEPS – vorgeschlagene fachliche und technische Verträge


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Layer-Zuordnung

`src/steps/models`: PitchClass, SpelledPitch, Interval, Scale, ChordIdentity, ChordVoicing, ChordSymbol, HarmonicContext, AnalysisCandidate, ChordEvent, Progression, DrumEvent, GroovePattern (letzte zwei erst nach Scope-ADR). `src/steps/theory`: transponieren, analysieren, Relation-Rechner; ohne GUI/IO. `app/ui`: Tk Shell und Views. `app/adapters`: Storage/Audio/Knowledge/Plugin Ports. `knowledge`: überprüfte Konzeptrecords und Registry. `research`: Rohquellen/Claim Intake, nicht Runtime.

## Minimale Datensemantik

| Objekt | Muss unterscheiden | Testfälle |
|---|---|---|
| Pitch / SpelledPitch | 12-TET PitchClass vs. konkreter Notenname/Oktave/Alteration, optional Temperierung später | F#≠Gb als Schreibweise, pc gleich; deutsches H/B |
| Chord | Identität, Name, Voicing, Bass/Umkehrung, konkrete Töne, Harmonic Interpretation | `C7` ≠ `Cmaj7`; `C/E` Bass E; rootless |
| Context | Tonika, Modus, Analysis Framework, Stil, vorheriger/nächster Akkord | `E7` in a-Moll V7, in C-Dur V7/vi |
| Progression | Akkordereignisse mit Start/Dauer/Takt; relative/absolute Darstellung, Revision | `C-G-Am-F` +2 = `D-A-Bm-G`, ein Save/Load-Roundtrip |
| Analysis | `framework`, Kandidat, Erklärung, Source-ID(s), Konfidenzart, Alternativen, Validator | kreative Suggestion nicht als belegtes Theoriegesetz |
| Knowledge Claim | `source_id`, Edition/URL, Fundstelle, exaktes Claim-Summary, Kontext/Stil, Status, Gegenaussagen | ohne Quelle nicht approved |
| Drum Events (später) | Instrument, Step/Tick, Velocity, Swing, Pattern Version, MIDI Map | Roundtrip und Tempo/PPQ erst nach MIDI-ADR |

## Speichern und Migration

Eigene Steps-Formatversion, explizite schema_version, UUIDs ohne Glide-Task-ID-Vererbung, gesichertes atomisches Schreiben, fsync/rename nach Systemprüfung, Backup nur nach validem Hauptwrite, Load von neueren Dateien schreibgeschützt oder mit eindeutigem Fehler; nicht als leeres Dokument starten. Settings und Arbeitsdaten außerhalb des Installationsverzeichnisses unter projekt-/OS-eigenen Pfaden. Unbekannte optionale Felder nicht still löschen; Kompatibilitätsvertrag ist gesondert zu testen. Import von Glide-Todo-Daten **nicht** Teil des ersten Steps-Speicherwegs.

## Schnittstellen (Entwurf, keine bereits implementierten APIs)

- `NavigationRegistry.list_items() -> readonly UI view model`
- `WorkspaceHost.activate(view_id)`, `PlaceholderView` falls nicht freigegeben
- `PreferencesStore.load/save` mit getrennter Steps-Identity
- `KnowledgeRepository.lookup(concept_id, locale, framework)` mit Quellenstatus
- `ProgressionRepository.read/write(document)` in eigener Version
- `PlaybackPort.schedule(events, tempo, soundbank)` – zunächst deaktiviert
- `MidiExportPort.render(progression, ppq, tempo_map)` – nach technischen Tests

Jede Schemaänderung erzeugt `decisions/ADR-...`, Version/Fixture/Negativtest und Migrationsstrategie. Die bereits vorhandenen JSON-Schemas gelten als **provisorische Drafts**, nicht als validierte Musikformate.

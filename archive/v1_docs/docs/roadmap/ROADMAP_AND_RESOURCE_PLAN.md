# STEPS – stufenweise Roadmap, Ressourcen und Freigabepunkte

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Planungslogik

Kein kalendarischer Liefertermin ist verbindlich. Abfolge nach gesicherten Abhängigkeiten, nicht nach verfügbaren Modell-Tokens. Glide-Entwicklung am lokalen 3.53.0-Stand läuft bereits in Copilot; kein konkurrierender großer Rewrite parallel. Der Nutzer hat berichtet, dass ChatGPT-Token voraussichtlich Mittwoch, Claude-Token Donnerstag zurückkehren und ein gesonderter Modellzugang („Fable 5.2“, Bezeichnung/Verfügbarkeit hier nicht extern bestätigt) zur Verfügung steht. Ressourcenannahmen sind **keine Produktbelege** und kein Grund, Sicherheits-Gates zu umgehen.

| Phase | Arbeitsziel und konkreter Output | Muss vorher stimmen | Abnahme (Definition of Done) | Risiko |
|---|---|---|---|---|
| S0-A / sofort | Vollständiges Standmanifest Glide lokal + Github, saubere SHA/Status-Änderungsübersicht | Copilot-Fortsetzung beenden; alle 94 Module/Assets/QA-Berichte verfügbar machen | reproduzierbarer Commit, isolierte Prüfung, offene Abnahmen markiert | P0 |
| S0-B / parallel | Steps-/Glide-Dokumentation, Lizenz- und Rechteaudit, Scope/2-Pane-ADR, quellbasierter Skill-Plan | keine Manipulation am produktiven Glide | im PR dokumentiert, Owner entscheidet offene Alternativen | P0 |
| S1 | neutrale Steps-Shell (Sidebar und Workspace), eigenes Branding und Appdaten-Root, erhaltene Settings/Theme/Icon/Menu/Navigation-Chrome | S0-A + Architektur/Änderungstestliste | Desktop startet und schließt; Layout und sämtliche geerbten Shell-Funktionen demonstriert; Todo-Services bleiben aus | P0 |
| S2 | Datenverträge & 1. Harmonie-Engine (Pitch, Spelling, Chord, Mode, Progression, Transposition) | getrennte Domain-/Storage-Port-Spezifikation | Golden Cases und Negativfälle grün, kein Tk in `src/steps` | P0 |
| S3 | Chord Progression Workspace und persistente eigene Projekte | S1+S2, SaveResult-Adapter | Create/Edit/Undo/Save/Load/Restore mit Testdaten, Smoke auf OS | P1 |
| S4 | Quellenregister, originale Concept-/Claim-Karten, Validierungs-Skill und Literatur-Intake | Rechteprüfung + Source-Schema | Quellenbelege/IDs/Hashes/Status; Skill zitiert nicht erfundene Quellen | P1 |
| S5 | Harmoniegraph und erklärende UI (Diatonik, Dominanten, Borrowing, Voice Leading, Alternativanalyse) | S2+S4 | explizite Regel/Interpretation, Stil/Confidence, Beispiel/Counterexample | P1 |
| S6 | MIDI/Playback/Loop und Chord-/Takt-Editor | Domain stabil, MIDI-Adapter gewählt, OS-Backends geprüft | SMF-Roundtrip, Timing/Tempo, No-Device-Fallback, Audio-Test | P1 |
| S7 | Drum-Progressions-/Groove-Modul und Verbindung Harmony ↔ Rhythm | Scope-Entscheidung, S3+S6 oder paralleler Minimalpfad | Step Grid, Swing/Velocity/Patterns, deterministische Exporttests | P2 (Vision behalten) |
| S8 | Knowledge-Search, MIDI/MusicXML/JAMS, fortgeschrittene Reharmonisierung und Stilkontexte | Quelle-/Produktionsreife | getestete Importgrenzen, Provenienz und Lernqualität | P2 |
| S9 | Public Beta/Release mit Plattformpaketen | QA, Rechte, Supply Chain, Feedback | Signierung/Release-BOM, Barrierefreiheit, manuelle Abnahme, Dokumentation | P2 |

## Freigaben als Entscheidungs- oder Arbeitspakete

**ADR-001**: Was bedeutet „2 Fenster“: ein Tk-Root mit zwei Panels (Vorschlag) oder zwei getrennte OS-Fenster? Bildschirmfoto zeigt eine Ansicht mit linker Seitenliste und zentraler Arbeitsfläche. Wird aus diesem Dokument ausdrücklich keine endgültige Entscheidung gemacht.

**ADR-002**: MVP: Chord-only oder Chord+Drum, Reihenfolge Audio und MIDI, Objekttypen. Der Nutzer nennt explizit Drum-/Akkordfolgen, während ältere Forschung Drums zurückstellt. Product Vision und MVP dürfen sich unterscheiden.

**ADR-003**: Steps-eigenes Branding: Name/Logo/Symbol, Farb- und Font-Ableitungen, GPL/MPL/Fremdasset-Lizenzen; Glide-Bundle-ID darf keinesfalls gleich bleiben.

**ADR-004**: Datenschema + lokaler Speicher, Undo, Crash Recovery, Migration. Keine Glide-Aufgabendatei als Steps-Projektdokument verkaufen.

**ADR-005**: Musiknotation `H/B`, Chromatik, alternative Interpretationen und Tonartenmodell.

**ADR-006**: Audioengine/MIDI-Bibliothek (nicht ohne technisches Benchmark und Lizenzreview festlegen).

**ADR-007**: Bibliothekszukunft – 49 Verzeichnisse als unveränderter Legacy-Snapshot und separate kanonische `knowledge/`-Registry; Aufnahme neuer Verzeichnisse über Taxonomieänderungs-ADR.

## Sichere parallele Arbeit mit KI-Konten

| Arbeit | Beste Ressourcennutzung | Nicht parallel bearbeiten | Kontrolldokument |
|---|---|---|---|
| Copilot in VS Code | lokalen Glide-3.53-Abschluss, gezielter CI-/UI-Fix, Stand einfrieren | gleichzeitige Glide-Quellreparatur in anderen Agenten | `prompts/02_GLIDE_FINISH_FREEZE.md` |
| ChatGPT/weiterer Account | Quellenregister, Roadmap, Konfliktabgleich, fachliche Daten- und Testfixtures | bereits von Copilot geänderte UI-Dateien | `prompts/14_SOURCE_INGESTION.md`, `prompts/01_ORCHESTRATOR.md` |
| Claude/Fable-Zugang | nach Token-Freigabe zunächst Architekturreview und isolierte Shell-Diff-Vorschläge | große direkt gemergte Migration ohne Baseline | `prompts/04_GLIDE_TO_STEPS_SHELL.md` |
| Gemini/Antigravity | unabhängiger Konkurrenz-/Wissensabdeckungs- und Designreview | als einziges Prüf-Orakel seiner eigenen Implementierung | `prompts/18_COMPETITOR_RESEARCH.md` |

**Wichtige Ressourcengrenze:** Kein Tool-/AI-Konto garantiert aktuelle Modellnamen oder Guthaben. Für Portabilität Prompts als Dateien und Fortschritt als commits/ADRs/Source-IDs speichern, niemals nur im Chatkontext. Ein Agent = ein klar abgegrenzter Änderungsbereich + ein Branch + ein Evidence Report. Dieselbe Datei nicht gleichzeitig in zwei Agentensitzungen ändern.

## Rückfall und Scope-Schutz

Bei einem fehlgeschlagenen Gate wird keine nächste Phase aktiviert: Fehler dokumentieren, vorherigen Commit unverändert nutzbar halten, minimalen Revert ermöglichen, Details der Abweichung an einer Stelle führen. Die Roadmap bleibt lebend: neue Crawls/Ordner ändern zuerst Source-Index/Taxonomie, nicht unmittelbar den Runtime-Code. Keine Dauer/Abschlussquote erfinden.

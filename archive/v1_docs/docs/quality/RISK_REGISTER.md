# Risiken, Chancen, offene Entscheidungen und Gegenmaßnahmen

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

| Kennung | Art / Gewicht | Gefahr/Chance | Frühwarnzeichen | Gegenmaßnahme / Verantwortlichkeit |
|---|---|---|---|---|
| R-01 | Recht/P0 | öffentlich gepushte fremde Bücher/HTML/MIDI/Schriftassets ohne belegte Freigabe | Lizenz leer oder nur Filename | originäre Rechteprüfung je Blob, Git-History-Beratung, **keine neue Redistribution**; Owner+Legal |
| R-02 | Architektur/P0 | `ListApp`-Monolith übernimmt Task-Domain und Nutzerdatenpfade in Steps | neue App importiert Glide-Speicher-Globals | Ports, separate Bundle-/UserData-IDs, isolated app root; Engineering |
| R-03 | Abnahme/P0 | Glide lokal 3.53.0, Github 3.50.7 – falscher portierter Stand | untracked lokale Dateien, Hash mismatch | source of truth und vollständiges Referenzmanifest; Copilot/Inhaber |
| R-04 | Daten/P0 | Datei-/Importverlust beim Entfernen alter Todos | Backup-/Undo-/Restore-Fall rot | zweistufige Migration, Dry-Run, atomare Speicherung, Restore-Test; Engineering |
| R-05 | Qualität/P0 | vorhandener QA-Status von Glide wird für Steps behauptet | Tests verweisen nur auf Glide SHAs | eigene Steps-Regression auf aktuellem Commit und nativer Plattform |
| R-06 | UX/P0 | 2-pane/2-OS-window-Interpretation missverstanden | divergierende Wireframes | ADR und UI-Layout-Prototyp mit Rückweg; Owner |
| R-07 | Forschung/P1 | falsche Eindeutigkeit von Harmonie-Claims | `E7 → Am` ohne Tonart klassifiziert | Framework, Alternate Analysis, Beispiele/Counterexamples |
| R-08 | Bibliothek/P1 | dedup zerstört historische Referenzen und Sprach-/Versionsvarianten | `rm` nur nach hash | duplicate classes, reverse link graph, Preservation-first |
| R-09 | Skill/P1 | Halluzinierte Literatur- und Seitenzitate | keine `locator` in Registry | Zitat- und Retrievaltests, `unverified` Status |
| R-10 | UX/P1 | Mac/Tk-Menüs, Symbolfallback, Fontgrößen/Clip fehlen | Fokus-/UI-Regressionsfälle rot | Glide-erprobte after_idle/semantic widget tests, native UI |
| R-11 | Ressourcen/P1 | Token-Abläufe unterbrechen Kontext, mehrere Agenten kollidieren | zwei Agenten gleiche Datei/Branch | kleine Reposchnitte, Handovers, Owner-Freigabe, klare Zuständigkeit |
| R-12 | Performance/P1 | Tk-UI blockiert durch 1000+ Researchtexte/Audio | Startup/Render > Budget | vorberechnete kompakte Indizes, background IO, unprofiliertes Vorher/Nachher |
| R-13 | Product/P1 | Drums verschwinden aus Vision, weil Harmony-MVP dominiert | keine ADR/Backlog-ID für Drums | eigenständige verschobene S7-Planung |
| R-14 | Veröffentlichung/P1 | schlechte Build-/Lizenz-/SBOM-Abdeckung | packaging nur auf einer Plattform | Buildmatrix, Dateihashes, BOM und Signierung prüfen |
| O-01 | Chance | bewährtes UI-Design statt vollständigem Neubau | Widgets lassen sich per Adapter isolieren | kleine vertikale Portierung, wiederverwendbares UI-Pack |
| O-02 | Chance | eigener Quellenkorpus mit nachvollziehbarer Didaktik | Claim-/Source-IDs etabliert | explainable harmony statt Black-Box-Generator |
| O-03 | Chance | KI-unabhängige Fach-Skills und kleine Prompts | Providerwechsel ohne Formatbruch | portable Markdown/YAML/JSON/Fixture-Retrieval |
| O-04 | Chance | Polyfunktion von Chord-/Drum-Progressions | Harmonie- und Beat-Editor teilen Takt/Timing-Verträge | getrennte Module auf gemeinsamer Transport-/Grid-Abstraktion |

**Status:** Risikoanalyse, nicht verifizierte Ereignisprognose. Für jede priorisierte Gefahr Owner, Datum, Gegenmaßnahme, tatsächliche Test-Evidence und Restwahrscheinlichkeit im Issue erfassen.

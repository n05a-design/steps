# QA, Roadmap und Workpackages – Steps nach Glide 3.53

## Gate 0 – Dokumentation und Kontinuität

`AGENTS.md`/Quelle/History/Glide-Bestandsaufnahme/V1–V5-Pakete/aktuelle 29 Fachprompts indexiert; `STATE.json`, `OUTPUT_REGISTER.csv`, `SOURCE_COVERAGE.csv`, `NEXT_SESSION_HANDOVER.md` existieren und sind in sich konsistent. Fehlendes wird mit Status benannt. Ownerentscheidung „Steps auf Glide-3.53-Grundgerüst“ nachvollziehbar.

## Gate 1 – eingefrorene Glide-Basis

Upstream-SHA `9e767bea5e21063466a28ac3a679406484ad5d5f` bestätigt, eingebettete 1.580 Dateien mit Source-/Asset-/Test-/Runtime-Vergleich erfasst, Abweichungen dokumentiert; Hauptworkflow `42822511966` erfolgreich und macOS-arm64-Paketjob `42822511486` erfolgreich. Separate Liste optionaler Skips. Keine Kopier-/Umbaumaßnahmen nötig, um Glide 3.53 nochmals „grün zu machen“.

## Gate 2 – STEPS-Paket und CI

`src/steps-0.00` vs `src/steps` via Python-Package-ADR klären; Ziel und Tests aktualisieren. Letzte historisch rote Steps-Struktur-CI `42842449461` ist **nicht** Glide-Problem. Neue CI-Läufe mit korrektem Steps-SHA, Pflichtcheck auch bei `app/`-/`src/`-Änderungen, konkrete Testreport-Pfade.

## Gate 3 – Shell-Architektur/Freigabe

30 dokumentierte UI-Szenarien mappen, volle Erhaltungs- und No-op-Aktionsmatrix, Design-Parität, DataRoot-Isolation, alle `ListApp`-Side Effects/Callbacks, Modullizenzen und Rollback. Eingriffsvariante (inkrementeller Rückbau / selektive Shell / Hybrid / kleine paritätsgetreue Neukomponente) als ADR mit Gegenproben; **erst dann** Codearbeit auf STEPS-Branch.

## Gate 4 – Steps-Musik-Vertikalschnitt

UI-freier Pitch/Chord/Progression/Time-Kern; DE H/B, enharmonische Schreibweise, Voicing/Transposition; eigene Project/Track/Event-Datenmodelle und atomarer Save-/Load-Roundtrip, MIDI-Export mit externem Parser. Drums/Audio/Timeline nach Owner-MVP-Scope, nicht als fiktiv integriert ausgeben.

## Gate 5 – Wissen/Skill und Distribution

Rechtefilter für Quellen/Fremdassets, geprüfte claim/Concept/Rule/Test-Pipeline mit kleinem Pilot, music-harmony-coach Skill mit Evaluation und zitierfähiger Provenienz; Windows/Linux/macOS/A11y/nativer Start/Packaging/Source-SBOM/Owner-Release-Freigaben getrennt.

## Je Task auszugebender Dokumentensatz

`scope`, `owner_decision`, `source_sha`, `input_hashes`, `affected_paths`, `features_and_modules`, `architecture_decision`, `changes`, `tests_run_with_results`, `tests_not_run`, `generated_analyses_and_general_outputs`, `risks`, `next_action`, `rollback`, `output_registry_update`, `handover`. **Auch bei keinem Code-Diff** ist die Ergebnisdokumentation Pflicht.

## Priorisierte, sichere nächste Aufgaben

1. Audit-Gate A und Quell-/Historienregister mit V5 + Glide-Antigravity-Bestandsaufnahme erstellen – Produktcode read-only.
2. Upstream/integrierte Glide-3.53-Kopie auf Module, Assets und Hashes vergleichen; Abweichungen und Risiken.
3. Steps-Struktur-/CI-Defekt `src/steps-0.00` als separaten kleinen PR-Plan samt Regressionen.
4. Shell-/Sidebar-Action-Matrix und Component-Reuse-Versionierung definieren; Design-/No-Glide-Touch-Tests spezifizieren.
5. Nach unabhängiger Owner-Freigabe ersten sicheren STEPS-Shell-Mikroschnitt ausführen; parallel Rechte-/Knowledge-Pilot in separatem Workstream.

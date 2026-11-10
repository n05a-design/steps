# Tatsächlicher Glide-Import-, Runtime-, Side-Effect- und Mutationsgraph

**Prompt-ID:** `02_GLIDE_MONOLITH_DEPENDENCY_AUDIT` · **Arbeitsart:** ANALYSE (Code nur lesen, keine Refactoringänderungen) · **Roadmap:** P0/P4

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

`src/glide/app.pyw` (vollständig in isolierter lokaler Kopie), 93 weitere Laufzeitmodule, `src/glide/README.md` V1.15, `docs/02_ARCHITECTURE.md`, `AGENTS.md`, `tests/`, `GLIDE_SYSTEM_VERSION`.

## Fachlich konkreter Arbeitsauftrag

Erzeuge zuerst ein statisches AST-Inventar ohne Modulimporte und ohne echten App-Start: Modul, Top-Level-Statements und Seiteneffekte, direkte/relative/dynamische Imports, Callgraph approximiert, Class `ListApp`-Methoden/Funktionen und Zustandsowner. Sammle Calls, die Dateipfade konfigurieren, `Tk()` anlegen, globale Menükonfiguration patchen, Umgebungsvariablen auslesen, Lock/Backup/Save/Undo anstoßen, `after` oder Worker verwenden. Exakt für B01–B25 alle **transitiven** Modulabhängigkeiten ausweisen: `core pure`, `Tk adapter`, `Glide domain`, `resource/native`, `test only`, `unknown`. Verfolge die Seitennavigation, Kopf, Suche, Settings und Nebenansicht nicht nur bis zum Widget, sondern bis zu ihrer Command-/State-/Datei-Mutation. Vergleiche für relevante Funktionen alle Aufrufer, Counterfactual ohne Glide-Tasks und Auswirkungen auf Datenformat/Undo/Restore. Definiere eine Core-Extraktionsreihenfolge mit kleinen PRs und Rückfallmechanismus.

## Reproduzierbare Abnahmen und Gegenproben

Keine unkontrollierten `import app.pyw`: Side-Effect-Suche zunächst rein statisch, dann **nur** mit synthetischer isolierter DataDir und Path-Spies. Red Case: Dummy-Core-Import, der unerwartet `glide`-Taskmodell oder produktives Datenverzeichnis öffnet, muss scheitern. Test: Widget nach `dispose` darf keine `after`-Callback aufrufen. Alle Tests mit Vorher-/Nachher-Baseline und `NOT_RUN` für nicht verfügbare Plattformen.

## Ergebnis und Übergabeformat

`module_graph.json/csv`, `runtime_dependency_graph.md`, `state_owner_matrix.csv`, `mutation_paths.md`, `package_readiness_B01_B25.csv`, `minimal_extraction_sequence.md`; pro Befund Datei/Zeile, nicht nur Katalogquote.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Vermischen von Shell und Task-Domain, impliziter Datei-I/O beim Import und doppelte Mutationswege gelten als Blocker für Freigabe eines Core-Pakets. `app.pyw` nicht durch globale Suchen/Ersetzen automatisch zerlegen.

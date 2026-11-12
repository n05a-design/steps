# STEPS · Anleitung für den Fable-5.2-Lauf

## Reihenfolge der Übergabe

| Nr. | Datei | Pflicht | Zweck |
|---|---|---|---|
| 1 | `docs/audit/fable-5.2/STEPS_FABLE_5_2_MASTERPROMPT.md` | ja | Auftrag. Als erste Nachricht vollständig einfügen |
| 2 | `docs/audit/fable-5.2/STEPS_FABLE_5_2_CONTEXT_PACK.md` | ja | Baseline und Landkarte |
| 3 | `docs/audit/fable-5.2/STEPS_FABLE_5_2_AUDIT_SCOPE.md` | ja | Prüfmatrix mit IDs |
| 4 | Repository-Zugriff oder Kontextbündel (siehe unten) | ja | Ohne Code, Tests und Daten ist kein Audit möglich |

Diese Anleitung und der Vorbereitungsbericht werden nicht an Fable übergeben.

## Fall A: Fable arbeitet direkt im Repository (z. B. Claude Code)

```bash
git fetch origin
```

```bash
git switch --detach 22f3f5f348d060abfd4e2ffc917d0c95a639441e
```

Das Paket selbst liegt nicht auf `22f3f5f`. Deshalb Datei 1 als Auftrag einfügen und die Dateien 2 und 3 als Anhang mitgeben oder außerhalb des Checkouts bereitstellen. Gelesen wird das Paket als Auftrag, geprüft wird der Code auf `22f3f5f`. Für `scripts/audit_knowledge_coverage.py` wird `PyYAML==6.0.3` benötigt (`knowledge/benchmark/requirements.txt`), am besten in einer eigenen venv.

## Fall B: Fable hat keinen Repository-Zugriff

Ein GitHub-Link genügt nicht. Fable braucht die Dateien selbst. Erzeuge im Repository-Root ein Bündel ohne Fremdmaterial und ohne Secret-Daten:

```bash
git archive --format=zip -o steps_fable_22f3f5f.zip 22f3f5f -- . research/gaps ':(exclude)research/[!g]*' ':(exclude)archive' ':(exclude)source_archive' ':(exclude)src/glide-v3.53' ':(exclude)src/steps-0.00' ':(exclude)scripts/historical_secret_baseline.json' ':(exclude)scripts/pre-commit-secret-check.py' ':(exclude)tests/fixtures' ':(exclude)tests/test_secret_scanner.py' ':(exclude)knowledge/research/*SECRET*'
```

Das Bündel ist etwa 1,7 MB groß und enthält rund 440 Dateien. Die ZIP-Datei nicht ins Repository committen. Verhalten nach dem Entpacken, so in der Vorbereitung getestet:

- Kernsuite: 105 Tests (ohne die 15 Secret-Scanner-Tests). `test_structure` schlägt erwartungsgemäß fehl, weil `research/ableton` fehlt. Werte das nicht als Befund.
- `scripts/run_knowledge_benchmark.py` und `tests/test_knowledge_benchmark.py` rufen `git rev-parse HEAD` auf. Ohne Git-Repository brechen sie ab. Abhilfe im entpackten Ordner: `git init`, `git add -A`, `git commit -m "STEPS 22f3f5f"`. Der Bericht zeigt dann die lokale Commit-ID. Fable vermerkt dazu `Bündel von 22f3f5f`.

Hat Fable keine Codeausführung, kann es Tests nur lesen. Jede Ausführung ist dann `NOT_RUN`. P0-Gegenproben müssen als hergeleitete Soll-Ist-Tabellen mit ausdrücklich unbeobachtetem Ist-Wert geführt werden, oder Codex führt sie nachträglich aus (siehe Rückgabe).

Muss der Kontext noch kleiner sein, gilt diese Mindestauswahl für P0: `src/steps/`, `app/knowledge.py`, `tests/test_theory_core.py`, `tests/test_progression_engine.py`, `tests/test_reviewed_progressions.py`, `tests/test_pilot_publication.py`, `tests/test_golden_reference_cases.py`, `knowledge/sources/registry.yaml`, `knowledge/benchmark/PILOT_ABNAHME.md`, `docs/IMPLEMENTATION.md`, `docs/theory/API.md`, `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`. Geschätzt rund 56.000 Tokens. Skills (`.agents/skills/steps-knowledge-curation/`, `SKILL.md`, `skills/`) kommen mit etwa 13.000 Tokens hinzu.

## Budget (Planungsannahme)

Ein konkretes Fable-Kontingent ist hier nicht bekannt. Die Werte sind Schätzungen (Zeichen geteilt durch 4) und keine Plattformangaben.

| Block | Umfang ca. |
|---|---|
| Prompt, Kontextpaket, Prüfmatrix | 10.000 Tokens |
| Kern-Code und Pilotdaten | 27.000 |
| Kern-Tests inkl. Golden-Test | 18.000 |
| Skills inkl. Tests | 13.000 |
| Wissensregister, Kataloge, Benchmark (gezielt lesen) | bis 31.000 |
| Golden-Case-Daten (gezielt lesen) | bis 25.000 |
| Abschlussbericht | 8.000–15.000 |

## Fortsetzungsauftrag

Nur sinnvoll, wenn die Abdeckungsmatrix des Berichts offene P0- oder P1-IDs zeigt oder ein Befund `HYPOTHESIS` eine Reproduktion braucht. Vorlage:

> Setze das STEPS-Audit auf `22f3f5f` fort. Bereits geprüft: <IDs>. Offen: <IDs mit Grund aus Abschnitt 8>. Bisherige Befunde: <F-IDs, nur Kurzzeile>. Prüfe nur die offenen IDs nach denselben Regeln und demselben Befundstandard. Liefere nur neue oder geänderte Befunde und die aktualisierte Abdeckungsmatrix.

Den vollständigen Erstbericht nicht erneut übergeben.

## Rückgabe an Codex

1. Den Bericht als `docs/audit/fable-5.2/results/FABLE_AUDIT_REPORT_<JJJJ-MM-TT>.md` auf einem eigenen Branch ablegen. Die YAML-Befundblöcke bleiben unverändert.
2. Codex reproduziert jeden `CONFIRMED`- und `STRONGLY_INDICATED`-Befund auf `22f3f5f` oder einem späteren Stand und vermerkt die Abweichung. Befunde mit `NOT_RUN` führt Codex zuerst aus.
3. Je Befund: Regressionstest zuerst, dann Korrektur, jeweils in einem eigenen PR nach `AGENTS.md` Nr. 7. Offene Fachfragen kommen nach `research/gaps/`.

# STEPS-Wissensbenchmark

Der Benchmark verbindet die [Abnahmeliste der acht Pilotaussagen](PILOT_ABNAHME.md),
die [Abdeckungsmatrix](COVERAGE.csv), [Prüffälle und Sollwerte](cases.json) und
[Stichproben der zwölf Domänen](THEMENSTICHPROBEN.md).

## Ausführen

Aus dem Repository-Root mit Python 3.11 oder 3.12.

```sh
python -B -m src.steps.progression.reviewed --review-manifest
python -B scripts/run_knowledge_benchmark.py --review-sheet knowledge/benchmark/PILOT_ABNAHME.md
python -B scripts/audit_knowledge_coverage.py --check --details /tmp/steps-coverage-details.csv
python -B scripts/run_knowledge_benchmark.py --scope pilot
python -B scripts/run_knowledge_benchmark.py --scope all --json-out /tmp/steps-benchmark.json --markdown-out /tmp/steps-benchmark.md
python -B scripts/run_knowledge_benchmark.py --content PROG-008
python -B scripts/render_reviewed_progressions.py --check
```

`--scope all` und `--content` geben Exit 1 zurück, wenn die jeweilige
Auswahl fehlgeschlagene oder ausstehende Pflichtfälle enthält. Die
Ausgabe nennt betroffene Inhalte und Fall-IDs. Der Pilot-CI-Job prüft
nur die acht Pilotpflichtfälle und anschließend die menschlichen Freigaben
die Abnahmeliste und das generierte Lernmaterial. Abnahmeliste und Matrix
nach belegten Statusänderungen erneut erzeugen. Andere Inhaltsbereiche bleiben gemäß
ihren eigenen Ergebnissen gesperrt.

`PASS` bescheinigt das im Fall definierte Soll, beispielsweise Tonklassen
oder Ticks. Das Freigaberegister erfasst die menschliche Abnahme separat.
Menschliche Beschlüsse mit Claim-ID und vollständigem Fingerabdruck gehören
in den Draft-PR. [Freigabeablauf](../concepts/progressions/README.md)

## Abdeckungsmatrix lesen

Formale Prüfung umfasst je nach Sammlung IDs, Pflichtfelder, Referenzziele,
Tabellenstruktur, Parserkonsistenz oder vorhandene Git-Pfade. Historische
YAML-Quellen sind auf Eintrags-ID und Titelfeld geprüft. Bei Graphrelationen
fehlt ein direkter Quellen- oder Claim-Bezug. Die in der Detaildatei genannten
Endpunkte ohne kanonische Definition bleiben offen.

Die Spalten zur Fachprüfung zählen explizit ausgeführte, gegen Sollwerte
oder konkrete Quellen begrenzte Fälle. Ein bestandener Teilaspekt ist keine
Freigabe des ganzen Eintrags. Ein älteres Label wie `VERIFIED_TRUE`
zählt nicht als erneute Prüfung. Die Zeilen überlappen, etwa App-Beispiele,
Lernaussagen und Progressionspositionen. Historische Dateien und
Dateiregister sind getrennte Zählungen. Inventarisierung belegt Pfadbestand,
keinen Inhalt und keine Nutzungsrechte. `--write` aktualisiert die Matrix.

## Harmony Coach separat prüfen

Mit `--scope coach` die fünf Aufgaben und Sollbestandteile erfassen.
Jede Antwort muss aus einem tatsächlich mit dem historischen Skill
ausgeführten Lauf stammen. Modell, Skill-Version, Eingaben und erlaubte
Hilfsmittel dokumentieren. Eine fachkundige Person prüft jede Pflichtaussage,
die zulässigen Varianten und die konkret genannte Quellenfundstelle.

Die JSON-Eingabe zu `--coach-assessment` ist nach Fall-ID indiziert.
Jeder Eintrag enthält `reviewer`, `response`, `source_evidence`,
`sources_verified` und `criteria`. Das letzte Feld ordnet jedem
Pflichtbestandteil aus `expected` einen booleschen Befund zu. Der Runner
wertet diese dokumentierte Bewertung aus. Der Freitext selbst bleibt
Gegenstand der Fachprüfung. Ohne bewertete Antwort bleibt der Fall offen.

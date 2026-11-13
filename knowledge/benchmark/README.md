# STEPS-Wissensbenchmark

[Versionierte Abdeckung](COVERAGE.csv) · [Fallregister mit Sollantworten](cases.json)
· [Pilot-Abnahmeliste](PILOT_ABNAHME.md) · [Domänenstichproben](THEMENSTICHPROBEN.md)

## Lauf und Freigabe

Aus dem Repository-Root mit Python 3.11 oder 3.12. Die Inventur historischer
YAML-Register verwendet eine getrennte Audit-Abhängigkeit. Laufzeit und
Benchmark-Prüffälle benötigen sie nicht.

```sh
python -B scripts/run_knowledge_benchmark.py --scope all --json-out /tmp/steps-benchmark.json --markdown-out /tmp/steps-benchmark.md
python -B scripts/run_knowledge_benchmark.py --scope pilot
python -B scripts/run_knowledge_benchmark.py --scope publication
python -B scripts/run_knowledge_benchmark.py --scope api
python -B scripts/run_knowledge_benchmark.py --scope backlog
python -B scripts/run_knowledge_benchmark.py --content PROG-008
python -B scripts/run_knowledge_benchmark.py --scope coach --markdown-out /tmp/steps-coach.md

python -m venv /tmp/steps-knowledge-audit
/tmp/steps-knowledge-audit/bin/python -m pip install -r knowledge/benchmark/requirements.txt
/tmp/steps-knowledge-audit/bin/python -B scripts/audit_knowledge_coverage.py --check --details /tmp/steps-coverage-details.csv --report /tmp/steps-coverage.md
/tmp/steps-knowledge-audit/bin/python -B scripts/audit_knowledge_coverage.py --check --gate-content PROG-008

python -B -m src.steps.progression.reviewed --review-manifest
python -B scripts/run_knowledge_benchmark.py --check-review-sheet knowledge/benchmark/PILOT_ABNAHME.md
python -B scripts/render_reviewed_progressions.py --check
```

Die Berichte nennen Git-SHA, Bereich, Einzelfall und den nächsten konkreten
Schritt für beanstandete und ungeprüfte Fälle. Fehlgeschlagene oder offene
Pflichtfälle führen im jeweiligen Lauf zu Exit 1. Für einen einzelnen Inhalt
bei Übernahme beide Prüfungen ausführen, den Benchmark mit `--content` und
die Inventur mit `--gate-content`. Die Inventur sperrt formale Befunde.
Der Benchmark sperrt fehlgeschlagene und offene Pflichtfälle. Die fachliche
Einzelabnahme wird mit den jeweiligen Belegen dokumentiert. Die Pilot-CI führt die
Pilot-Sollwerte, die Veröffentlichungstests mit synthetischen Freigaben,
den Abgleich der Abnahmeliste und den echten Publikationscheck aus.
Die allgemeine Progressions-API bleibt als historischer Bestandskatalog
verfügbar. Ihre Einträge erhalten durch Abruf keine Freigabe.

Abnahmeliste und Matrix nach belegten Statusänderungen mit `--review-sheet`
bzw. `--write` neu erzeugen. Menschliche Pilotentscheidungen gehören mit
Claim-ID und Fingerabdruck in den Draft-PR. [Freigabeablauf](../concepts/progressions/README.md)

## Abdeckungsmatrix lesen

- **Vollständig fachlich geprüft** gilt bei einer belegten, zum aktuellen
  Inhalt passenden Fachabnahme. **Stichprobe** nennt einen gegen unabhängiges
  Soll oder eine konkrete Quelle geprüften Teilaspekt. **Nicht geprüft**
  umfasst formale Prüfungen, reine Inventarisierung und ausstehende Abnahmen.
- Die Detaildatei erfasst alle Einträge der aktiven Register und Kataloge.
  Die automatisierte Prüfung umfasst Eindeutigkeit, Pflichtfelder,
  bibliografische Verweise bzw. lokale Pfade, referenzierte IDs, Graph-Endpunkte,
  Akkordaliase und die Konsistenz jeder Progressionsposition. Nicht auflösbare
  Quellen oder Endpunkte bleiben als Befunde sichtbar. Das Freigaberegister
  bleibt maßgeblich für die Pilottexte.
- Historische JSON-, CSV- und YAML-Dateien in den inventarisierten Beständen
  erhalten eine zusätzliche Syntax- bzw. Spaltenprüfung. Semantische
  Querverweise und Originalfundstellen dieser Dateien bleiben zur Prüfung
  offen. Archive, Rohmedien und historische Dokumente werden als Git-Pfade
  inventarisiert. Das belegt weder Inhalt noch Nutzungsrechte.
- Zählungen überlappen, etwa Pilot-Lernaussagen, App-Beispiele, Golden Cases
  und Progressionspositionen. Alte Statuswerte wie `VERIFIED_TRUE` zählen
  nicht als neue Fachprüfung. Der Graph hat keinen direkten Claim- oder
  Quellenbezug pro Kante. Die Detailtabelle nennt fehlende Endpunktdefinitionen.

## Hör-, Spiel- und Didaktikabnahme

Aus dem sauberen Checkout lassen sich leere Formulare für den gewählten
Git-Stand und die aktuellen Fallfingerabdrücke erzeugen. Ein
unbewertetes Kriterium ist `null`. Nach der Prüfung je Kriterium
`true` oder `false` eintragen.

```sh
python -B scripts/run_knowledge_benchmark.py --scope sample --manual-template /tmp/steps-hoer-spiel.json
python -B scripts/run_knowledge_benchmark.py --scope coach --coach-template /tmp/steps-coach.json
```

Der Bericht nennt pro offener manueller Aufgabe die konkrete nächste Probe
und die Pflichtkriterien. Für `--manual-assessment` eine JSON-Datei nach
Fall-ID indizieren. Jeder Eintrag enthält `fingerprint` aus dem Ergebnis,
`git_sha`, `reviewer`, `evidence` (Aufnahme, Notenblatt oder Protokoll),
`observations` und `criteria`. `criteria` bildet jeden erwarteten
Pflichtbestandteil auf einen booleschen Befund ab. Stale Versionen bleiben
offen. Fehlende oder beanstandete Pflichtbestandteile blockieren den Fall.

[Hörmaterial und Spielaufgabe für PAT-031, PROG-001 und P02](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_ABNAHMEPROBEN.md)

## Harmony Coach

`--scope coach` protokolliert Aufgaben und tatsächlich bewertete Antworten
für jede der zwölf Domänen separat. Für `--coach-assessment` eine JSON-Datei
nach Fall-ID indizieren. Jeder Eintrag enthält `fingerprint`, `reviewer`,
`response`, `source_evidence`, `sources_verified`, `criteria`,
`model`, `skill_revision` und `run_evidence`. `criteria` bildet die
Pflichtbestandteile auf boolesche Befunde ab. Eine fachkundige Person
bewertet Antwort, zulässige Varianten und Fundstellen anhand der Rubrik.
Der Runner wertet die dokumentierte Bewertung aus. Ohne reale bewertete
Antwort bleibt die betreffende Domäne offen.

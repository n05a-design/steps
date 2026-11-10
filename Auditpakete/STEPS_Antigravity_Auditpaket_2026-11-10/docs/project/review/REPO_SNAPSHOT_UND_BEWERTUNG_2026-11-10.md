# STEPS – aktueller GitHub-Snapshot, Befunde und Grenzen der Prüfung

**Datum:** 10.11.2026 (Europe/Berlin)
**Untersuchter Remote-Snapshot:** `n05a-design/steps@1fc07e230dc6a2fe92fd6662da43e332d596b376`
**Glide-Referenz:** `n05a-design/glide-to-do@9e767bea5e21063466a28ac3a679406484ad5d5f`
**Methodischer Status:** Git-Tree-/Blob-/CI-Metadaten und **gezielt gelesene** Projekt-, Architektur-, Audit-, Prompt- und README-Dateien geprüft. **Keine vollständige Inhaltsprüfung aller 3.768 Dateien oder aller Binär-/Forschungsdokumente** durch diesen Bericht. Der beiliegende Master-Prompt beauftragt erst die vollständige lokale Abdeckungsprüfung.

## 1. Quantitativer Ist-Snapshot

| Sachverhalt | Feststellung | Evidenzgrenze |
|---|---:|---|
| Git-Baum | 4.293 Einträge | 3.768 Dateien, 525 Verzeichnisse; API-Baum `truncated=false` |
| `research/` | 1.811 Dateien | Verzeichnispfade, kein Volltextreview |
| `src/glide-v3.53/` | 1.580 Dateien | Importierter Glide-Quell-/Dokumentationsbaum im STEPS-Repository |
| `prompts/` | 30 Dateien | README + Aufträge 01–29 |
| Gleiche Git-Blob-ID in mehreren Pfaden | 463 Gruppen, 942 zusätzliche Pfadvorkommen | Kein Beweis semantisch verzichtbarer Duplikate; Git dedupliziert Objekte bereits |
| STEPS-Appversion | `0.0.0-dev` | Kein produktives Release |
| Glide-Version | `3.53.0` | `src/glide-v3.53/01_Repository/Glide/VERSION` |

Die drei Pfade `source_archive/Glide-Aufgaben-und-Listen_v3.53.0.pyw`, `src/glide-v3.53/07_Python-Versionen/Glide-Aufgaben-und-Listen_v3.53.0.pyw` und `src/glide-v3.53/01_Repository/Glide/src/glide/app.pyw` tragen denselben Git-Blob `0fc522fb5faf9694dbd28d2ca43b1f415a010139`. Dieser Befund sagt **nichts** über die vollständige Bytegleichheit aller anderen Glide-Module mit Upstream aus; dafür ist ein kompletter Baumvergleich erforderlich.

## 2. Sicherheitsrelevante Befunde P0

### P0-01 – Glide 3.53.0 ist technisch geeigneter Referenzstand, aber nicht freigegebene STEPS-App

Der Glide-`main`-Commit `9e767bea...` enthält in GitHub erfolgreich abgeschlossene Windows-/Linux-/macOS-Prüfungen und Paketierungsarbeiten. Einzelne optionale UI-/Accessibility-Schritte wurden übersprungen. Diese Resultate gelten **nur** für Glide. Für STEPS ist bisher kein entsprechender funktionsfähiger Musik-/Shell-End-to-End-Stand nachgewiesen. Die Owner-Zielrichtung ist nun ausdrücklich: Glide 3.53.0 kontrolliert auf eine neutrale Shell zurückbauen und STEPS darauf aufbauen.

**Maßnahme:** unveränderliches Baseline-Manifest für `src/glide-v3.53/`, isolierte STEPS-Identität, Reuse-/Abhängigkeitsschicht, zwei-Pane-Shell als reversibler Prototyp; negative Tests gegen alte Glide-Daten-/Taskzugriffe.

### P0-02 – Versionsordner und importierbarer Python-Pfad widersprechen sich

`src/steps-0.00/README.md` lautet aktuell noch `# src/steps` und nennt ein späteres importierbares Paket. Gleichzeitig erwartet `tools/validation/check_structure.py` den Pfad `src/steps`, der im geprüften Baum nicht vorhanden war. Der Struktur-CI-Workflow [42842449461](https://github.com/n05a-design/steps/actions/runs/42842449461) scheiterte konkret mit `Missing required paths: ['src/steps']`.

**Maßnahme:** ADR über validen `src/steps/`-Python-Paketpfad versus historischen Entwicklungsordner `src/steps-0.00/`; anschließend synchronisierter Code-/Test-/CI-/Doku-Wechsel. Nicht bloß Testerwartung absenken. Dieses Paket enthält eine überarbeitete `src/steps-0.00/README.md`, und den neuen Importpfad als **optionalen** Vorschlag.

### P0-03 – mehrere kanonisch wirkende, aber unterschiedlich datierte Projektübersichten

Root-`README.md`, `docs/project/PROJECT_OVERVIEW.md`, `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, V4-Reviewpakete, `source_archive/` und `publish_overlay/` behandeln teils denselben Bestand mit unterschiedlichen Versions- und Repo-Referenzen. Mehrere Kerntexte enthalten `Steps 75329fef`, obwohl das aktuelle `main` `1fc07e23` ist. Historische Aussagen sollen **nicht** rückwirkend überschrieben werden, aber aktuelle Referenzdokumente benötigen klar datierte Nachträge.

**Maßnahme:** Single-Source-of-Truth-Konzept mit kanonischer Gegenwartsdarstellung, historischen Originalen, `supersedes`-/Linkbeziehungen und maschinenlesbarem Coverage-/Claim-Register.

### P0-04 – öffentliches Forschungs-/Drittmaterial und Provenienz

Das Repository enthält große Mengen von externen Fach-PDFs, heruntergeladenen Webseiten und Design-/Musikmaterialien. Es ist aus dem Git-Tree allein **nicht** belegt, dass Veröffentlichung und Einbettung in eine MPL-2.0-App pro Material erlaubt sind. Bereits veröffentlichte Objekte können in älteren Git-Commits weiter verfügbar bleiben.

**Maßnahme:** separates nicht destruktives Asset-, Rechte- und Git-History-Audit; vor rechtlicher Prüfung keine neuen massenhaften Fremdtexte in öffentliche Artefakte überführen. Kein automatischer Force-Push oder History-Rewrite.

## 3. Weitere wesentliche Prüflücken

| ID | Priorität | Befund | Prüfauftrag |
|---|---|---|---|
| R-05 | P1 | 29 aktive Aufgaben-Prompts plus historische Kopien/Overlays | Doppelungen, Versionierung und Verweisgültigkeit prüfen; kein Blind-Merge |
| R-06 | P1 | 28 Requirements, 33 Auditdimensionen, 40 historische Konflikte und 34 Lücken | Vollständige Traceability am aktuellen Snapshot gegen Originalquellen nachweisen |
| R-07 | P1 | `knowledge/sources/registry.yaml` hatte im verifizierten Projektkontext leeres `sources: []` | Aktuelle Datei/KB-Ingestion nachprüfen, Source/Claim/Rule/Test-Pipeline real verifizieren |
| R-08 | P1 | Sechs referenzierte Originaldokumente, aber nur fünf unter `docs/project/Archiv/` | Weitere Originalkopien in V4-`private_sources/` und `source_archive/` vergleichen; keine vorschnelle „fehlt“-Behauptung |
| R-09 | P1 | `src/glide-v3.53/` jetzt vollständig aufgenommen, ältere Doku berichtet nur Einzelskript | Komplettes Upstream-/importiertes Quell-/Resource-/Lizenz-Mapping erstellen |
| R-10 | P1 | Historischer Scope Chords vs Drums/MIDI | Nutzerproduktentscheidung, MVP/Timeline und Domainmodelle entflechten |
| R-11 | P2 | Identische Git-Blob-Gruppen und mehrere ZIP-/Overlay-/V4-Kopien | Semantische Identität, Referenzen, Provenienz und Versionierungsnutzen klassifizieren |
| R-12 | P2 | Uneinheitliche Dokumentationsautorität und alte relative Pfade | Link-/Hash-/Markdown-/Manifest-Review gegen aktuelle Struktur |
| R-13 | P2 | Unterschiedliche V6.6/V6.7-Zahlen und frühere Bibliothekskategorien | Nenner, Scope, Quelle und Datum jeder Behauptung zuordnen |
| R-14 | P2 | Einträge mit ungewöhnlichen Namen, Nullbytes bzw. nicht druckbaren Zeichen im Baum | UTF-8-/Pfad-Inventar, Explorer-/Windows-Pfad-Kompatibilität und Reproduzierbarkeit prüfen |

## 4. Bereits vorhandene Stärken

- Dokumentierte Schutzprinzipien in `AGENTS.md`: Preservation-first, keine destruktiven Git-Operationen, Trennung von App/Domain/Knowledge.
- Umfangreiche Product-/Engineering-/Research-/QA-Dokumente mit fachlichen Negativtests und klarer Abgrenzung von Planung versus Implementierung.
- Quellen- und Requirements-Register (`manifests/`), historische Originale und Vergleichspakete erhalten grundsätzlich die Nachvollziehbarkeit.
- Konkreter Glide-3.53.0-Quellbestand und grün geprüfter Glide-Upstream als reproduzierbare technische Referenz.
- Ausgearbeitete Shell-Extraction-Spec, 29 aufgeteilte Arbeitsaufträge und getrennte Product-/Research-/Engineering-Workstreams.

## 5. Prüfungsschranken dieses Berichts

**Tatsächlich geprüft:** aktueller GitHub-Baum, relevante Pfad-/Blob-IDs, Repository-Berechtigung (`pull:true`, `push:false`), Glide-/STEPS-Aktionsstatus und wesentliche zentrale Textdateien aus Projekt, Architektur, Audits, Prompts, Source-README und Validator.

**Nicht tatsächlich geprüft:** jeder der 3.768 Inhalte zeilenweise; alle PDF-/Bild-/Audio-/MIDI-Inhalte; lokale nicht veröffentlichte Dateien; sämtliche historischen Git-Objekte; OS-native STEPS-Starts; vollständiger aktueller `pytest`-/CI-Testlauf. Für diese Bereiche darf aus diesem Bericht keine Projekt-Gesamtfreigabe abgeleitet werden.

**GitHub-Schreibgrenze:** Die verbundene Integration hat für `n05a-design/steps` nur `pull:true`, `push:false`. Daher wurden keine Branches, Dateien, PRs oder Commits im Remote erstellt. Das mitgelieferte Overlay ist **ein lokaler Änderungsvorschlag**, kein GitHub-Erfolgsnachweis.

## 6. Quellen-Links

- [STEPS HEAD](https://github.com/n05a-design/steps/commit/1fc07e230dc6a2fe92fd6662da43e332d596b376)
- [Glide 3.53 HEAD](https://github.com/n05a-design/glide-to-do/commit/9e767bea5e21063466a28ac3a679406484ad5d5f)
- [Glide-Prüfung erfolgreich](https://github.com/n05a-design/glide-to-do/actions/runs/42822511966)
- [STEPS-Strukturcheck fehlgeschlagen](https://github.com/n05a-design/steps/actions/runs/42842449461)
- [STEPS Dependabot-/pip-Graph erfolgreich](https://github.com/n05a-design/steps/actions/runs/42849387382) – **nicht** mit Strukturprüfung verwechseln

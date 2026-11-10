# 02 — Revisionsmethodik, Quellen und Grenzen

## Untersuchungsdesign

**Fragestellung:** Ist die bisherige Dokumentationsarbeit hinreichend, damit Glide langfristig als wartbares Desktop-Fundament für Steps und weitere Projekte fungieren kann, ohne Glides Produktverhalten, Nutzerdaten, Design- und QA-Verträge zu beschädigen, und ohne die eigenständige Steps-Domäne und ihre Forschungs-/Rechtebasis zu verwischen?

**Gegenbeweismethode** statt Bestätigung: Für jede große These wurde geprüft, ob ein einzelner negativer Fund sie widerlegen würde. Beispiel: '88/94 ohne Tk' widerlegt sich als Übertragbarkeitsbeweis bereits durch Imports auf Glide-spezifische Fachmodelle, implizite Zustandsbesitzer, Settings oder globale Pfade. 'Steps CI grün' widerlegt sich als Musiktest-Beweis durch den Source-Review des `check_structure.py`.

**Dimensionen (Bewertungsrahmen):** Produktidentität/Zielgruppen; Funktionsscope/Vertical Slice; UI-Shell; Navigation/Interaktion/Accessibility; Layout/Fonts/Theme/Branding; Python-Import/Runtime; Tk-/OS-Lebenszyklus; Core API/Adapter; Paket-/Versionierungsstrategie; State Ownership/Undo; Datenformat/Migration/Isolation; Security/Threat-Model/Privacy; Repository-Hygiene; Bibliotheks- und Lizenzrechte; Ingestion/Quellenstatus; Musiktheorie/Erklärung; Rhythmus/MIDI/Tempo; Knowledge/Schemas/Skill; QA/CI/Regression; Performance/Profiling; Plattform-/Packaging; Prozesse/Agenten/Branches; Wartungskosten/Governance; Projektfinanzierung und Token-/Zeitbudget; Dokumente/Beweiskette; Community/Open-Source-Lizenz.

## Ausgewertete Original-Snapshots

**GitHub Live-Tree** am 10.11.2026:

- G1: `n05a-design/glide-to-do`, [`main@9e767bea`](https://github.com/n05a-design/glide-to-do/tree/9e767bea5e21063466a28ac3a679406484ad5d5f), 1.714 Einträge, 1.542 Dateien, 172 Verzeichnisse, ~315,12 MB logische Dateigrößen. `01_Repository/Glide/src/glide`: 94 direkte Python-Dateien (93 Laufzeit + 1 separater Prototyp laut Katalog). `GLIDE_SYSTEM_VERSION=1.15`, `VERSION=3.53.0`. Glides Hauptdatei `app.pyw` mit ~3,59 MB war über die verfügbare Quelltext-Schnittstelle **nicht** in voller Länge auslesbar; seine Innereien sind aus projektverbindlichen Dokumenten belegt, nicht unabhängig AST-geprüft.
- S1: `n05a-design/steps`, [`main@75329fef`](https://github.com/n05a-design/steps/tree/75329fef46878a5ac816cef3690e612a9e8fe52c), 2.219 Einträge, 1.931 Dateien, 288 Verzeichnisse, ~668,68 MB logische Dateigrößen. 60 PDF-Dateien mit zusammen 451.999.999 Bytes; 160 Gruppen sha-identischer Blobs/426 überzählige Pfade, logisch ~115,69 MB Dateigröße. Diese Größen sagen **nichts** über tatsächliche Bandbreite des Git-Packs oder über Urheberrechte. Im Pfad `src/steps/` / `app/` wurden nur README-Platzhalter, kein ausführbarer Musikcode gefunden.

**Glide-Primärdokumente:** [`src/glide/README.md`](https://github.com/n05a-design/glide-to-do/blob/9e767bea5e21063466a28ac3a679406484ad5d5f/01_Repository/Glide/src/glide/README.md) (System V1.15, Module, Pakete B01-B25, QA/Grenzen); `docs/02_ARCHITECTURE.md`; `docs/DESIGN_RICHTLINIEN.md`; `docs/05_QA_TESTPLAN.md`; `docs/07_QA_BERICHT.md`; `docs/ARBEITSRICHTUNG.md`; `docs/01_PRODUCT_CONSTRAINTS.md`; `docs/06_DATA_BACKUP_MIGRATION.md`; `00_Arbeitsvorbereitung/Glide_Uebergabe.md`, `Glide_Entwicklungsplan.md`; `01_Repository/Glide/AGENTS.md`, Root `CLAUDE.md`; Versionen, ausgewählte Core-Quelldateien und `sidebar_policy.py`, `appearance.py`, `compact_mode.py`.

**Steps-Primärdokumente:** `AGENTS.md`; `ANALYSE_REPOSITORY.md`; `STEPS_Zielstruktur.md`; `README_SETUP.md`; `docs/architecture/{architecture,legacy-mapping,migration}.md`; `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`; historische fünf Original-Reviews in `docs/project/Archiv/`; technischer Anhang und Quellenabdeckungs-CSV; `research/notes/deep-research/legacy/{Master-Research-Prompt,PROJECT_CONTEXT_HANDOVER}.md`; `research/gaps/OPEN_GAPS.md`; alle fünf `schemas/*.schema.json`; `knowledge/sources/registry.yaml`; Root- und Harmony-Skill; `pyproject.toml`, `tools/validation/check_structure.py`, `tests/test_structure.py`.

**Lokale Dokumente**: Byteverifizierter 48-Dateien-V1-Export; historische `Glide_Steps_Modulbibliothek_2026-11-07.xlsx` mit 10 Blättern (über artifact_tool inspiziert), CSVs, die zwei voll lesbaren Research-Grundlagen (~51/27 KB). Beide waren auch im V1-ZIP enthalten.

**Externe Primärreferenzen**: Mozilla MPL 2.0 FAQ und Volltext; Python 3.14 `tkinter` Threading Model und Tcl-Ereignisloop; PyPA Packaging-Guide für pyproject; GitHub Dokumentation zur Git-Historienentfernung; Anthropic Fable-5.2-Ankündigung vom 09.11.2026. Ein externer Produkt-/Benchmarktvergleich von Musiksoftware wurde **nicht** neu im vollen Marktumfang durchgeführt; Preis-/Featuresnapshots der alten Research-Berichte bleiben veraltet möglich.

Referenzen: https://www.mozilla.org/en-US/MPL/2.0/FAQ/ · https://www.mozilla.org/en-US/MPL/2.0/ · https://docs.python.org/3.14/library/tkinter.html#threading-model · https://packaging.python.org/en/latest/guides/writing-pyproject-toml/ · https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository · https://www.anthropic.com/claude-fable-and-mythos-5-2 .

## Tiefe und Grenzen des Quellchecks

| Ebene | Durchgeführt | Was nicht durchgeführt wurde |
|---|---|---|
| Git-Dateibestand | Gesamter Tree und Dateigrößen/SHA-Metadaten auf bezeichneten HEADs | History sämtlicher Branches, Clone mit LFS, Dateibytes aller Binärartefakte |
| Python-Modulstruktur | Import-Ausschnitt aus praktisch allen **separaten** Glide-Modulen via Source-Fetch; konkrete Modulgruppen analysiert | Vollständiger AST-/Call-/Mutationsgraph der 3,59-MB-`app.pyw`; dynamische Imports/Callables und Runtime-Graph |
| UI | Design-/QA-Verträge, Modul- und Zustandspläne | Realer Tk-Start, Screenshots und visuelle Pixel-/DPI-Abnahme auf allen OS |
| Steps-Domain | Schemas, leere Registry, Platzhalter, Starttest gelesen | Keine Musik-Engine getestet; keine MIDI-Datei erzeugt oder gelesen |
| Dokumente | Große kanonische Projekt-, Forschungs- und Architekturtexte nach Struktur/zentralen Aussagen gegengeprüft | Nicht jede historische Unterdatei der ~1.800 Forschungsdateien voll gelesen |
| Recht | Dateiarten/-größen, erkennbare Lizenzrisiken, MPL-Primärquelle | Keine individuelle juristische Rechtebewertung oder Autorenschaft jedes PDFs |
| Paket | V1-HASH-Manifest, Links, ZIP-Test, Promptduplikate, Textumfang | Kein Publikums- oder Langzeitnutzungstest, kein GitHub-Push |
| Actions | Die zum Zeitpunkt der Abfrage über GitHub sichtbaren Workflow-Zustände | Kein neuer eigener CI- oder macOS-Hardwarelauf |

## Evidenz- und Zeitlogik

Quell-Claims werden durch volle `repo + path + SHA + ggf. Abschnitt` identifiziert. Git-Blob-SHAs sind **Inhaltsadressen**, keine Aussagen über Tests. Historische Reports behalten ihren ursprünglichen Quellstand. Zentrale Auswertungsvokabeln:

- `VERIFIED_REPO`: Quelle direkt an festem Git-Commit gesehen; genau dieser Inhalt, nicht aktueller Dateipfad später.
- `VERIFIED_ARTIFACT`: Byte-/Strukturcheck eines lokalen Artefakts.
- `DOCUMENTED_QA`: früherer Testbericht sagt etwas, aber keine Reproduktion in diesem Audit.
- `PROPOSED`: neue Handlung; nicht freigegeben.
- `OPEN`: nicht belegt, nachzureichen; `CONFLICT`: mindestens zwei nicht ohne weiteres vereinbare Versionen oder Definitionsräume.
- `REQUIRES_OWNER_DECISION`: kein Agent darf die Wahl still treffen.

**Regel bei unvollständiger Datenlage:** Einstufung herabsetzen, Risiko und kleinste Prüfhandlung nennen, statt Behauptungen zu ergänzen. Null gefunden ist kein Beweis, dass eine Datei in der lokalen Arbeitskopie oder alten History nie vorhanden war.

## Reproduzierbarkeit

Der lokale V1-Audit wurde durch einen Python-Standardbibliotheksskriptlauf ausgeführt: Anzahl MD/CSV/ZIP, SHA256 des 47-Einträge-Manifests, relative Markdown-Links, identische Prompt-Absätze. Ergebnisse in `03_V1_QUALITAETSAUDIT.md`. Der externe Modulcheck nutzte GitHub-Quelldateien und einfachen Import-Ausdruck, **keinen** syntaktisch vollständigen AST: importierte Namen und Tk-Importfreiheit gelten als *direkter Importausschnitt*, nicht als transitive Entkopplungszertifizierung. Der Projekt-Branch wurde nicht geschrieben. Beim geplanten Code-Audit sollen syntaktischer AST-/Importgraph, dynamische Imports, Side-Effects und Runtime-Port-Verträge lokal in isolierter Kopie ausgewertet werden.

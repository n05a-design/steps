# STEPS – konsolidierte Projekt-Overview nach kritischer Zweitprüfung

**Stand:** 10. November 2026, Europe/Berlin. **Status:** *Prüf- und Arbeitsgrundlage, keine Release- oder Owner-Freigabe*. **GitHub-Referenz:** Steps `main` [`75329fef`](https://github.com/n05a-design/steps/commit/75329fef46878a5ac816cef3690e612a9e8fe52c), Glide `main` [`9e767bea`](https://github.com/n05a-design/glide-to-do/commit/9e767bea5e21063466a28ac3a679406484ad5d5f). **Lokaler Code-Upload:** `Glide-Aufgaben-und-Listen_v3.53.0.pyw`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`, Git-Blob `0fc522fb5faf9694dbd28d2ca43b1f415a010139`, **identisch** mit Glide-HEAD-`app.pyw`; **nicht** alle weiteren Glide-Modul-/Assetdateien lokal geliefert. Die ältere 66-Dateien-Fassung und ihre damaligen Snapshots werden in `archive/v1_docs` bewahrt.

## 1. Präzises Projektbild

STEPS ist ein eigenständiges, offenes Musikprojekt, dessen gegenwärtig am besten belegtes Produktbild eine **lokale, unabhängige Desktop-Anwendung zum Erstellen, Erkunden, Analysieren und Verstehen von Akkordfolgen** ist. Die aktuelle Projektbeschreibung nennt zusätzlich *drum progressions*, MIDI-Export und das Lernen von Musiktheorie. Beide Perspektiven sind berechtigt: **Harmonik und Akkordbeziehungen** bilden einen sehr gut vorbereiteten Forschungs- und didaktischen Kern, **Drums/MIDI und musikalische Bedienbarkeit** einen ausdrücklich beabsichtigten Nutzungsbereich. Der Zeitpunkt, zu dem Drums in der App funktional werden, ist jedoch noch nicht entschieden: historisches Handover `REQ-024` setzt Drums vorläufig `DEFERRED`; die spätere Beschreibung macht sie zur Produktvision. Dies ist eine offene Priorisierungsfrage, kein Grund, Drum-Forschung oder Archive zu löschen.

Die STEPS-Produktforschung nennt als Leitidee **Exploration → Explanation → Education**. Im sinnvollen Kernfall legt ein Mensch Akkorde an, sieht mögliche Beziehungen, kann Transpositionen überprüfen und erhält eine verständliche kontextgebundene Erklärung – nicht bloß eine Liste von Generatorvorschlägen. Die Differenzierung muss in echten Nutzeraufgaben nachgewiesen werden: Hookpad bietet bereits Chord-Vorschläge, tonartbewusste Oberfläche, Musiktheoriebezug, Wiedergabe inkl. Drumspur und MIDI-Export (https://www.hooktheory.com/support/hookpad). Ein Alleinstellungsmerkmal ist deshalb **Hypothese**, nicht Marktbeleg.

## 2. Die fünf Projektbestände – bewusst getrennt

| Ebene | Aufgabe | Nachgewiesener Bestand | Fehlende Leistung |
|---|---|---|---|
| **P1 App/Produkt** | Musikprojekte bearbeiten, Transposition/Erklärung/MIDI | Steps-Git-Scaffold in `app/`, `src/steps/`, fünf Schema-Entwürfe, Strukturcheck | keine nachgewiesene lauffähige Musik-App oder End-to-End-Proben |
| **P2 Fachwissen/Knowledge** | überprüfbare Konzepte, Regeln, Ausnahmen, Claims, Beispiele, Referenzen | historische 20 Initialquellen, Bibliothek V6.6, Knowledge-Struktur, Skill-Vorarbeiten | aktuelle `knowledge/sources/registry.yaml` ist `sources: []`, keine nachgewiesenen modernen Review-Batches |
| **P3 Glide-Transfer** | Desktop-Shell, Navigation, Design, Persistenz-/QA-Muster | `glide-to-do` mit dokumentiert 94 Modulen, 147 Fähigkeiten inkl. Technikfeatures, 25 **Kandidaten**paketen; aktueller Glide-Hauptcode 3.53.0 | keine unabhängige Steps-Shell; Modul-/Ressourcen- und OS-Tests nicht für Steps erbracht |
| **P4 Forschungsdokumente** | Theorie, Product Blueprint, Übergabe, Codex-Auftrag | sieben Dateien unter `research/notes/deep-research/legacy/`, **einschließlich** `PROJECT_CONTEXT_HANDOVER.md` | Research-/Owner-Freigabe und überprüfbare Claim-Ingestion |
| **P5 Produktions-/Ableton-Archiv** | Drums, DAW, Recording, Sounddesign, Mixing, weitere Studien | 1.000 Dateien in V6.6-Legacy-Baum, V6.7-Skripte, registrierte Ableton-/MIDI-/Wettbewerbsunterlagen | Rechte-/Duplikat-/Quellenreview und fachliche Zielzuordnung |

Die historische Großübersicht behandelt viele Themen ausführlicher und bleibt bytegenau in [`source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`](../../source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md). Sie bewahrt **40 historische Widerspruchs- und 34 Lücken-IDs**, 20 Quellen, 37 Archivkategorien, Glide-Entwicklungsgeschichte und 39 Codevorlagen aus dem technischen Anhang. Diese Daten nicht erneut in einer „neuen Wahrheit“ verkürzen: Der vorliegende Text gibt den **heutigen Status und die Beziehungen** an; die fachlichen Details stehen in den verlinkten Originalen und Fachmodulen.

## 3. Evidenzstatus und harte Zahlen – genau abgegrenzt

| Aussage | Evidenzart | Tatsächliche Grenze |
|---|---|---|
| Steps `main` 2.219 Tree-Einträge, 1.931 Dateien, ca. 668,68 MB unkomprimierte Blob-Summen | `GITHUB`, Commit `75329fef` | keine Inhaltsprüfung aller Dateien oder historischer Objekte |
| Steps hat 160 SHA-identische Blob-Gruppen/426 zusätzliche Pfade | `GITHUB`, Baum-/Blob-Abgleich | kein automatischer Beweis *inhaltlich unnötiger* Duplikate; keine Löschfreigabe |
| 60 PDFs im aktuellen Steps-Git-Tree | `GITHUB`, Dateibaum | keine vollständige Seiten-/Rechte-/Editionenprüfung; öffentliches Risiko separat auditieren |
| V6.6 Legacy enthält 1.000 Dateien im thematischen Teilbaum | `GITHUB`, Baum-Snapshot | nicht identisch mit historisch behaupteten 1.146/≈1.166/1.306 Gesamtdateien |
| Glide `main` 1.714 Tree-Einträge, 1.542 Dateiblobs, ca. 315,12 MB | `GITHUB`, Commit `9e767bea` | Paket-/QA-/Testausführung nicht unabhängig wiederholt |
| Glide lokaler `app.pyw` ist identisch mit GitHub `main` | `UPLOAD` + Git-Blob-SHA-Vergleich | **nur** diese einzelne 69k-Zeilen-Datei; nicht 93 weitere Module, Assets, Tests |
| Glide-Systemkatalog 94 Module / 147 Features / 25 Bausteinpakete | Quellen `README-Glide-System.md`, Glide-Repo | Modulregister ist keine Liste sofort entkoppelter Libraries |
| Sieben Deep-Research-Dateien inkl. 797-Zeilen-Handover | GitHub-Pfade/Blob-SHAs erfasst | ein Draft ist kein Owner-approved Abschluss |
| Aktuelles `knowledge/sources/registry.yaml` hat `sources: []` | `GITHUB`, Textinhalt | echtes registriertes und reviewtes KB-Quelleninventar steht aus |

**Statusformen:** `verifiziert bei Snapshot`, `aus Original berichtet`, `fachlich abgeleitet`, `vorgeschlagen`, `in Ausführung gemeldet`, `ausgeführt und getestet`, `extern rechtlich freigegeben`, `nicht bekannt`. Sätze wie „fertig“ oder „100% abgedeckt“ sind ohne diese Qualifikation zu vermeiden. Bei alten Quellen und echten Repositories hängt jede Behauptung am Datum und am Quell-SHA.

## 4. Wissenschaftlicher Kern – Warum das Datenmodell vor der GUI kommt

Die Forschungsgrundlage warnt vor vorschneller Gleichsetzung von Akkordsymbol, Tonhöhenklasse, Schreibweise, Voicing und Funktion. `F#` und `Gb` sind unter 12-TET enharmonisch gleichklingend, aber in ihrer diatonischen Rolle unterschiedlich; deutsches `H`/`B` ist nicht dasselbe wie internationales `B`/`Bb`. `C7` und `Cmaj7` sind andere Akkorde; `C/E` hat einen separaten Bass-/Inversionsvertrag. `E7 → Am` kann in a-Moll als V7→i, in C-Dur als V7/vi→vi erläutert werden. Harmonische Relationen sind `theoretical framework`- und `style context`-abhängig; eine Klavier-Versetzung (Voice Leading) hängt außerdem vom konkreten Register und Voicing ab.

Das System braucht getypte Konzepte, kontextgebundene Relationen und **alternative Interpretationen**, nicht eine globale „richtige“ nächste Akkordliste. Deterministische Regeln, empirische Korpusstichproben und kreative Heuristiken erhalten je eigene Evidenzklassen. Bei Drums und Akkorden kann ein gemeinsames **MusicTime**-/Takt-/Tick-/Tempo-/Timeline-Modell spätere teure Formatmigration vermeiden. Die detaillierten Invarianten stehen in [`docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`](../engineering/MUSIC_DOMAIN_AND_MIDI.md). Fachwissen und menschliche Erklärung stehen in [`docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`](../research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md), mit konkretem Pilot-Intake statt bloßer Struktur.

## 5. Glide-Shell – Erhalten, aber nicht blind kopieren

Die aktuelle Glide-App verwendet Python/Tkinter, eine zentrale `ListApp` mit ca. 1.866 direkten Methoden und Importzeit-Nebenwirkungen (Pfade/Cache, Tk-Menü-Patches, Dateiverzeichnisse, Runtime). Anders als eine kleine Widget-Library besteht die Shell nicht aus neutralen Bausteinen. Die 94 katalogisierten Module enthalten viele hohe Reuse-Kandidaten, aber auch stark an Glide-Modelle gekoppelte Teile. Eine vollständige Appkopie mit anschließender Löschung von Todo-Funktionen birgt Risiken für unerreichbare Commands, Actions, Daten, Undo, Crash-Recovery und UI-Fokus.

**Vier reale Strategien:** kompletter Fork/Rückbau, komponentenweise Extraktion, begrenzte Hybrid-Shell, kleine neu entwickelte Steps-Tk-Shell mit übernommenen Design-/QA-Verträgen. **Vorschlag:** zwei kleine Vergleichsspikes unter denselben 30 Shell-Abnahmeszenarien, statt „Fork und löschen“ vorab zu beschließen. Die zwei gewünschten Fenster werden aus dem Screenshot als `Sidebar + Workspace` in einer Tk-Root interpretiert, bleiben aber hinsichtlich unabhängiger OS-`Toplevel`-Fenster **offen**. Eingaben, Einstellungen, Theme, Hover, Fokus, Sidebars, globale Suche und Design bleiben als *Technik* erhalten; ihre alten Aufgabenaktionen nicht. Details und negative Tests: [`docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`](../engineering/SHELL_EXTRACTION_DEEP_SPEC.md).

## 6. Wissensbasis – Erweiterung ohne Verlust der Originale

Die 20 namentlichen Initialquellen, V6.6/V6.7-Wissensbände, Ableton-Interview-/Assetkataloge, Bücher, Crawls und zukünftige neue Ordner müssen über **Provenienz- und Ingestion-IDs**, nicht über einen starren Dateibaum als alleinige Wahrheit verbunden werden. Die P2-Schicht enthält `Source`, `Extract`, `Claim`, `Concept`, `Relation`, `Rule`, `Example`, `Revision`. Jede Relation besitzt Quelle, Definition, Gegenbeispiel, Theorie-Rahmen, Stilgeltung, Reviewstatus und verwertbare Testfälle. Ein Skill ist die Zugriffsmethode, **nicht** der vollständige Fachspeicher.

Bücher und Website-Caches können rechtlich oder technisch unverwendbar sein; Rechte müssen je Werk/Edition/Asset geprüft werden. Der nächste realistische Erfüllungsnachweis ist **ein kleiner legaler Batch**, der vollständig bis zu einem geprüften, korrekt zitierenden Query-/Unit-Test durchläuft. Strukturdateien, leere `README`s oder importierte Dateinamen allein genügen nicht. Ingestion und Security werden in [`docs/research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md`](../research/KNOWLEDGE_AND_RESEARCH_SYSTEM.md) behandelt.

## 7. Roadmap und Qualität – keine Scheingenauigkeit

P0: öffentlicher Drittmaterial-/Rechteaudit, Glide 3.53.0 vollständig einfrieren, Produkt-/Zwei-Fenster-ADRs, MusicTime/Chord/Notation-Invarianten, erstes vollständiges Knowledge-Pilotpaket. P1: B/D-Shell-Spikes, eigene Steps-Datenroots, korrektes Save/Load, Transposition/SMF, Datenmigrationsregeln. P2: Explorer + Erklärung + ausgewählte Drums/Groove-Interaktion abhängig von Scope, Audio/Playback-Freigabe, Usability und Native-A11y. P3: produktionsweite Korpora, Mixing/DAW-Breitenausbau, KI-/RAG-Modellierungsvarianten nach belegtem Mehrwert.

**Prüfgates:** Q0–Q7 und 30 Shell-Szenarien, 16 Theory/MIDI-Invarianten, 16 geplante IO-Failure-Checks sowie eigenes Source-/Citation-Review; sämtliche Zahlen sind derzeit **Pläne**, nicht `PASS`. Veröffentlichung und menschliche Native-Freigabe sind eigene Tore. Referenz: [`docs/quality/VERIFICATION_PLAN_V2.md`](../quality/VERIFICATION_PLAN_V2.md). Das gesamte aktuelle `33-Dimensionen`-Raster: [`docs/audit/01_UNTERSUCHUNGSDIMENSIONEN.md`](../audit/01_UNTERSUCHUNGSDIMENSIONEN.md).

## 8. Entscheidungsregister – Was ausdrücklich offen bleibt

- **Produkt:** Chord-only/Chord+MIDI/Chord+Drums in v0.1, Spielbarkeit vs. Lehrfokus; primäre Personas.
- **Fenster:** eine Tk-Root mit zwei Bereichen vs. `Toplevel`-Fenster; Ergonomie und Tastaturbedienung.
- **Glide-Reuse:** B vs. D Spike, Code-/Font-/Asset- und Lizenzübernahme; Module nicht blind portieren.
- **Datenschema:** Chord-Spelling/Voicing/Timing/Drum-Track, Undo- und Save/Load-Kontrakt, Versionierung.
- **Wissensbasis:** Fachtheorien/Quellenpriorität, Review-Owner, Pilotquellen, private versus öffentliche Inhalte.
- **Audio:** Datei-MIDI vs. Live-Playback, Ausgabebackend und Rechte an Soundfonts.
- **Governance:** wer trifft Scope-/License-/Release-/Brand-Entscheidungen, wer führt native QA durch, welche Agents besitzen welche Pfade.

Als **sofortige Arbeit** (nicht offene Nutzerfragen im Chat): Deliverables A0–A5 und `REQ-001–REQ-028` in [`manifests/REQUIREMENTS_TRACE_28.csv`](../../manifests/REQUIREMENTS_TRACE_28.csv) als Issues/ADRs mit Owner und Akzeptanztest bereitstellen.

## 9. Rechtliche und praktische Grenzen dieser Prüfung

In den öffentlichen Repositories wurden die Git-Bäume, zentrale Dokumente, Quellmetadata und der große lokale Glide-Einstiegscode geprüft. **Nicht** alle 3.473 Dateien beider aktuellen Repositories und nicht alle verfügbaren PDF-Bücher Seite für Seite verarbeitet. Historische Projekttexte behaupten Prüfungen/Quellenstatus teils ohne unabhängig prüfbaren Byte-/Runbeleg. Vollständige Revalidierung aller Lizenztexte, CI- und Plattformläufe, aller Ableton-URLs und aller musikalischen Aussagen ist offen. Diese Fassung führt daher ausdrücklich *kein* „alles fertig“ oder „vollständig verifiziert“.

## 10. Navigationsindex

- [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md): verlangte strukturierte Gegenüberstellung.
- [`docs/product/PRODUCT_STRATEGY_AND_MVP.md`](../product/PRODUCT_STRATEGY_AND_MVP.md), [`LEARNING_AND_EXPERIENCE.md`](../product/LEARNING_AND_EXPERIENCE.md), [`MARKET_AND_VALIDATION.md`](../product/MARKET_AND_VALIDATION.md): Produkt-/Didaktik-/Marktentscheidungen.
- [`docs/engineering/DATA_STORAGE_AND_PORTABILITY.md`](../engineering/DATA_STORAGE_AND_PORTABILITY.md), [`MUSIC_DOMAIN_AND_MIDI.md`](../engineering/MUSIC_DOMAIN_AND_MIDI.md), [`SHELL_EXTRACTION_DEEP_SPEC.md`](../engineering/SHELL_EXTRACTION_DEEP_SPEC.md): technische Verträge.
- [`docs/governance/RIGHTS_SECURITY_AND_RELEASE.md`](../governance/RIGHTS_SECURITY_AND_RELEASE.md), [`docs/operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md`](../operations/MULTI_AGENT_EXECUTION_AND_HANDOVER.md): Rechte und Agentenbetrieb.
- [`docs/quality/VERIFICATION_PLAN_V2.md`](../quality/VERIFICATION_PLAN_V2.md): Tests, PASS-/NOT_RUN-Abgrenzung.
- [`manifests/DEEP_RESEARCH_REFS.csv`](../../manifests/DEEP_RESEARCH_REFS.csv), [`manifests/REQUIREMENTS_TRACE_28.csv`](../../manifests/REQUIREMENTS_TRACE_28.csv): Primärquellen-/Anforderungsindex.
- [`archive/v1_docs`](../../archive/v1_docs/) und [`source_archive`](../../source_archive/): unveränderte Historie und sämtliche Originaluploads.

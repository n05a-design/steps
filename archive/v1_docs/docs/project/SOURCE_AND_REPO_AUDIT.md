# Audit – Quellen, vollständiger Upload-Index und Live-GitHub-Snapshots

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## 1. Nachweisgrenzen

**Vollständig verfügbar in diesem ZIP:** die sieben vom Nutzer hochgeladenen Text-/Code-/CSV-Dateien (als Bytes unverändert), der Screenshot und ein reproduzierbares strukturelles AST-Modul-Index-CSV. Die 89 Zeilen der historischen Quellabdeckung referenzieren sechs ursprüngliche, in einem älteren Research verwendete Dokumente; fünf sind im aktuellen Steps-GitHub-Verzeichnis `docs/project/Archiv/` sichtbar, `Glide Kontext für Fable(2).md` fehlt dort (die konsolidierte Overview behält seine historischen Zitate). Aktuelle externe Webseiten und 60 PDF-Inhalte wurden **nicht** kapitelweise gelesen oder wissenschaftlich validiert; nur Pfade/Git-Tree-Bytes sowie ausgewählte Repo-Dokumentationen wurden geprüft.

## 2. Tatsächliche Git-Repositories (GITHUB, 10.11.2026)

| Fakt | Steps | Glide |
|---|---:|---:|
| Branch | `main` | `main` |
| Head-SHA | `75329fef46878a5ac816cef3690e612a9e8fe52c` | `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d` |
| Git-Tree Einträge | 2.219 | 1.759 |
| Dateien (blobs) / Ordner (trees) | 1.931 / 288 | 1.575 / 184 |
| logische Dateigröße | ~668,68 MB | ~309,32 MB |
| Git-Blob-identische Mehrfachgruppen | 160 | 210 |
| zusätzliche Pfade in diesen Gruppen | 426 | 420 |
| primäre Zielbereiche | `research` 1.810 Dateien; `docs` 27; `knowledge` 20; `app` 5; `src` 5 | `01_Repository` 1.106; `07_Python-Versionen` 274; `20_Grafik_Master` 159 |
| Produktionsstand | `VERSION=0.0.0-dev`; keine nachgewiesene Musik-Runtime | `main` 3.50.7; #71 **merged** |
| Schreibrecht der aktuellen Verbindung | `push:true` (abgefragt), nur eigener PR-Branch empfohlen | `push:true`, keine Änderung beauftragt |

Die sechs ursprünglichen Schritte-Dokumente prüften das Git-Repo explizit **nicht**. Ein früheres `ANALYSE_REPOSITORY.md` prüfte `b42a990...` mit 1.827 Dateien/2.043 Einträgen; der aktuelle Head hat **104 zusätzliche Dateien und 176 zusätzliche Tree-Einträge**. Das ist **kein Widerspruch** ohne Vergleichsdatum, sondern zwei Snapshots. Beide zählten zufällig dieselben 426 SHA-identischen Zusatzpfade; die Byteidentität rechtfertigt noch keine Löschung oder Lizenzfreigabe.

## 3. V6.6-Fachbibliothek tatsächlich unter GitHub

Pfad `research/STEPS_Bibliothek/STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials/`: **1.000 Dateien** unter der Archivwurzel. Darunter sind exakt **49 sichtbare nummerierte Hauptverzeichnisse** (die README benennt 49), sowie zusätzliche Rootdateien. Fachverzeichnisse enthalten beispielsweise `00_NAVIGATION=62`, `03_CHORD_PROGRESSIONS=45`, `04_COMPOSING=154`, `06_PRODUCER_TOOLS=101`, `90_HISTORIE=163` Dateien. Die **doppelt nummerierten 21 und 39 bestehen tatsächlich**, aber Inhalte wurden nicht semantisch als gleich nachgewiesen; erst SHA/Metadaten/Inhaltsanalyse dann Entscheidung. Die in Screenshots gekürzten vollständigen Namen sind `16_CREATIVE_DIRECTION_PREPRODUCTION`, `22_SYNTHESIS_SAMPLING_SOUND_DESIGN`, `43_PRESERVATION_BACKUP_PROVENANCE`.

Im Repo gibt es V6.7-Generatoren (`tools/legacy/generators/create_steps_v6_7_*.py`); das berichtete Delta 7 Karten/7 Labore/12 Module ist damit nicht unabhängig als integrierter, geprüfter Stand bewiesen. Die frühere Overview behauptete 1.146 bzw. 1.166 und aus Summierung 1.306 Dateien; diese Zahlen gehören **anderen Inventarumfängen** und dürfen nicht durch die jetzt gemessenen 1.000 Archivdateien heimlich überschrieben werden.

## 4. Source-Rechte, Risiko

Im öffentlichen Steps-Repo sind 60 PDFs mit teils großen urheberrechtlich potentiell geschützten Büchern vorhanden; reine Repo-Anwesenheit ist keine Veröffentlichungsberechtigung. Größte Dateien: `Fundamentals of Music Proce_ (Z-Library).pdf` ~52,93 MB, `Schachter_Aldwell-Harmony_Voice_Leading.pdf` ~51,58 MB, `MusicTheory.pdf` ~47,49 MB, `The Piano Chord Collection HI RES.pdf` ~37,90 MB. Kein Export fremder Volltexte in diese neue ZIP-Datei; separates Rechte-/History-Audit priorisieren. Auch nach `git rm` bleiben frühere Git-Commits eine mögliche Expositionsquelle.

## 5. Glide-Verifikation und Abweichung

`glide-to-do` GitHub main ist 3.50.7 (Merge PR #71). Der hochgeladene **lokale** Quellstand `Glide-Aufgaben-und-Listen_v3.53.0.pyw` meldet 3.53.0, 69.015 Zeilen. Statische Python-AST-Analyse (nur dieses Einzelmodul, **keine Laufzeitprüfung**): **39 Top-Level-Klassen, 35 Top-Level-Funktionen, 2.648 direkte Klassenmethoden, 1.866 direkte `ListApp`-Methoden**. Die alte Overview berichtet 1.863 Methoden aus einem früheren Commit; das ist eine plausible Versionsdifferenz, keine unmögliche Strukturabweichung. Das 3.53-Skript referenziert zahlreiche weitere Glide-Module; **der Upload allein ist nicht lauffähig ohne Restrepo/Assets**. Unterschiede der Repo-Version 3.50.7 zur lokalen 3.53.0 wurden **nicht** als vollständiger Git-Diff verifiziert.

Die Glide-System-Doku meldet V1.15, 94 Quelldateien, 147 Features inklusive 20 systemtechnischer, 25 Bausteinpakete, 25 QA-Risiken und 311 Test-/Tooldateien (Zählung = Inventar, nicht bestandene Tests). Das sind **berichtete Katalogzahlen**, kein aktueller Runner-Proof. Die GitHub-DESIGN_RICHTLINIEN, ARBEITSRICHTUNG, Produktgrenzen, QA-Bericht, AGENTS.md und der Skill `design-richtlinien` wurden zum Architekturplan herangezogen.

## 6. Live-Stand des Steps-Scaffolds

`README.md` ist nur 117 Zeichen. `knowledge/sources/registry.yaml` enthält `sources: []`. Der Root-`SKILL.md` ist ein Routenplan und kein KB-Store. Harmony-Coach befindet sich verschachtelt unter `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md`, nicht direkt unter `skills/music-harmony-coach/SKILL.md` – keine Links raten. Die fünf JSON-Schemata und `tools/validation/check_structure.py` existieren; der Strukturtest behauptet selbst **keine Produktimplementierung**. `README_SETUP.md` nennt einen älteren Git-Stand und `push:false`, während die aktuelle GitHub-Verbindung `push:true` hat. `knowledge/legacy/MAPPING.md` benutzt noch den **historischen** Pfad `02_Bibliothek/STEPS_Bibliothek/`, die Live-Daten liegen unter `research/STEPS_Bibliothek/`; Verweisreparatur getrennt planen.

## 7. Quelle-zu-Befund-Verlinkung

- Nutzer-Upload: `source_archive/README_STEPS_BIBLIOTHEK.md`, `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, `source_archive/README-Glide-System.md`, `source_archive/Glide_Entwicklungsplan.md`, `source_archive/Glide-Aufgaben-und-Listen_v3.53.0.pyw`, `source_archive/Steps_Quellenabdeckung_2026-11-09.csv`, `source_archive/Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md`, Screenshot.
- Repo-Referenzen: https://github.com/n05a-design/steps/tree/75329fef46878a5ac816cef3690e612a9e8fe52c ; https://github.com/n05a-design/glide-to-do/tree/61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d
- Ältere Vollregister behalten: Overview §14 W-01–W-40, §15 G-01–G-34, V6.6-Sektion §5, 89-Zeilen-CSV `source_archive/Steps_Quellenabdeckung...`, technischer Anhang mit 39 einzigartigen Rohblöcken.

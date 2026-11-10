# STEPS – Unabhängige Zweitprüfung: Gesamtbewertung und Untersuchungsmethode

**Prüfdatum:** 2026-11-10 · **Bericht V2:** kritisch überarbeitete Arbeitsgrundlage, **keine Releasefreigabe**.  
**Repository-Snapshots:** Steps `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `9e767bea5e21063466a28ac3a679406484ad5d5f`.  
**Lokaler Glide-Upload:** `Glide-Aufgaben-und-Listen_v3.53.0.pyw`, Git-Blob `0fc522fb5faf9694dbd28d2ca43b1f415a010139`, **identisch** zur aktuellen Glide-`app.pyw` aus GitHub. Quelle für die Prüfung: hochgeladene Datei, GitHub API und `git hash-object`. Keine Programmausführung.

## Executive Summary – was sich gegenüber V1 wirklich ändert

**Gesamturteil:** V1 ist ein strukturiertes Starterpaket, keine voll belastbare Gesamtanalyse. Es bewahrt die hochgeladenen Originale und gibt 24 brauchbare Aufgabenrouten an, aber integriert den eigentlichen Inhalt unzureichend: 14.257 Wörter der vorherigen konsolidierten Overview wurden auf 789 Wörter in einer neuen Kurz-Overview reduziert; die ursprünglichen W-01–W-40 und G-01–G-34 werden nicht als maschinell bearbeitbares, aktuelles Entscheidungssystem geführt. Die 24 Prompts haben jeweils nur etwa 360–390 Wörter, sodass mehrere Kontrollfragen noch gar nicht operationalisiert wurden. V1 behauptet keine vollendete Software, enthält aber einige Aussagen über `main`, die seit einem GitHub-Merge am 10.11. historisch sind.

Die neue Prüfung zeigt vier bislang besonders folgenreiche Schwachstellen:

1. **Aktualitätsbruch:** Glide `main` ist jetzt 3.53.0/Glide-System 1.15, nicht mehr 3.50.7. Der einzelne lokale App-Hauptcode stimmt byteweise mit dem öffentlichen `app.pyw` überein. Das ist mehr als eine Übereinstimmung von Versionsstrings; die Übereinstimmung der separaten 93 Module, Ressourcen, Plattformpakete und Testbelege ist damit jedoch noch nicht bewiesen. Der aktuelle `07_QA_BERICHT.md` ist in Teilen als Bericht über einen *damals lokalen* Releasekandidaten formuliert und nennt `main` 3.50.7; diese Zeitform ist nach Merge #74/#75 veraltet. Der Bericht sagt außerdem explizit, dass Linux-/macOS-Vollprüfungen und native/menschliche Freigabe separat ausstehen. 
2. **Übersehener Projektbestand:** Unter `research/notes/deep-research/legacy/` existieren *sieben* konzeptionell wichtige Dateien, darunter zwei lange Research Papers (ca. 50 k bzw. 26 k Zeichen), der Master-Research-Prompt, der Handover-Prompt, der ausführliche Codex-KB-Auftrag sowie ein bereits geschriebenes `PROJECT_CONTEXT_HANDOVER.md` (ca. 83 k Zeichen). V1 hat diese vorhandenen Dokumente nicht einzeln gegen die 24 neu erstellten Prompts oder die Architektur geprüft. Eine behauptete „fehlende Übergabe“ ist daher neu zu differenzieren: **Ein Handover existiert, seine Freigabe/Aktualität bleibt offen.**
3. **Migration und Testtiefe:** `app.pyw` ist ein großer Tk-zentrierter Orchestrator (39 top-level Klassen, 1.866 direkte `ListApp`-Methoden, rund 69.015 Zeilen) mit Importzeit-Nebenwirkungen. Eine „Seitenliste ohne Funktionen“ ist kein rein visueller Eingriff: sie berührt Tastenkürzel, Kontextmenüs, Drag-and-drop, Auswahl/Focus, Schließen/Speichern, Home-Kacheln, Such- und Datengenerierung sowie globale Callback-Registrierungen. Das Übernehmen einer Python-Datei allein bildet die Glide-Systemgrundlage nicht ab.
4. **Produkt-/Wissensumfang:** Der Ausgangsbericht und die zwei Deep-Research-Arbeiten fordern ausdrücklich eine Wissensbasis vor dem Skill – fachliche Evidenz, Claims, Beispiele, Gegenbeispiele, unterschiedliche Harmonietheorien und Testorakel. Die V1-Roadmap macht aus diesem Forschungsprogramm überwiegend eine Reihe technischer Phasen. Die bisher wenig ausgearbeitete didaktische Lernerfahrung, Rhythmus-/Drum-Integration, Barrierefreiheit, internationale Musiknotation und Ressourcenverwaltung müssen als zusammenhängende Produktachsen behandelt werden.

**Sicheres Ergebnis des Audits:** Die Investition in Glide ist weiterhin wertvoll, die reine „Glide abspecken und neue Seitennamen einsetzen“-Strategie ist jedoch *nicht* als beste technische Lösung bewiesen. Bevor man sie akzeptiert, muss eine **reversible Shell-Extraktion gegen einen kleinen neu aufgebauten UI-Prototyp** mit identischen Prüfkriterien verglichen werden. Priorität erhalten das nutzbare musikalische Datenmodell, die abgesicherte Rechtefrage im öffentlichen Archiv und die reale Abnahme statt bloßer README-Vollständigkeit.

## 1. Gegenstand und Evidenzumfang

**Vollständig lokal lesbar und statisch verarbeitet:** sieben hochgeladene Text-/Quell-/CSV-Dateien, ein Screenshot; darin vor allem 14.257-Wörter-Overview, 65k-Wörter-Glide-Entwicklungsplan, 23k-Wörter-Glide-Systemkatalog und 69k-Zeilen-`app.pyw`. Der letzte V1-Paketstand wurde einschließlich aller 24 Prompts, README, Roadmap, Qualitäts- und Migrationsdokumente gelesen und quantifiziert. Das Originalmaterial bleibt im `source_archive/` byteidentisch. Das V1-Projektpaket bleibt unter `archive/v1_docs/` in seinen durch V2 ersetzten Teilen erhalten; nicht ersetzte V1-Dokumente bleiben an ihrem Ort.

**Live verifizierte GitHub-Metadaten:** Steps `main` 1.931 Dateiblobs/2.219 Tree-Einträge/ca. 668,68 MB logische Byte-Summe; Glide `main` nach PR #75 1.542 Blobs/1.714 Tree-Einträge/ca. 315,12 MB. Die Inventare beziehen sich auf *Git-Bäume*, nicht vollständige Repo-Historie oder lokale ungetrackte Dateien. Die Git-Blob-Gleichheit beweist nur die `app.pyw`, nicht eine komplette Runtime oder funktionierende Kompilierung.

**Zusätzlich gelesene Repo-Inhalte:** Steps `AGENTS.md`, `SKILL.md`, README, VERSION, fünf Schema-Dateien stichprobenweise, Struktur-/Migrationstests, bestehende Architektur-/Lizenzdokumente, `ANALYSE_REPOSITORY.md`, Harmony-Coach-Skill und seine Ingestion-Anleitung; sieben Deep-Research-Dateien mit vollständigem Textzugriff und Abschnittsindex; Glide `AGENTS.md`, `CLAUDE.md`, Designrichtlinien, Arbeitsrichtung, Produktgrenzen, Architektur und QA inkl. neuer 3.53.0-Einleitung; beide Git-Repositories als Verzeichnisbaum. Weitere rund 1.000 Archiv-PDFs, MIDI-/HTML-/Medien-Dateien wurden *nicht einzeln fachlich gelesen*. **Ein Dateipfad ist kein Inhalts- oder Lizenzbeleg.**

**Externe Primärquellen selektiv überprüft:** Mozilla MPL-2.0/FAQ; GitHub Größen-, LFS- und History-Leitlinien; Python/Tk-Threading-Modell; MIDI Association SMF, Mido-Zeitvertrag, music21-Notation; W3C WCAG; Herstellerdokumente Hooktheory, Scaler, Chordbot, MuseScore. Die Aussagen daraus sind von internen Dokumentbehauptungen getrennt. Keine unabhängige Vollbibliografie aller Fachquellen.

## 2. Maßstab: sechs Nachweiskategorien statt ein „fertig“

| Code | Kategorie | Einordnung | Was diese Kategorie **nicht** beweist |
|---|---|---|---|
| `V` | Direkt überprüft | Git-Blob/Tree, existierender Inhalt, lokale AST- oder Hash-Prüfung | dass Code läuft, dass Fachinhalt richtig ist oder lizenziert werden darf |
| `D` | Dokumentiert | Behauptung/Entscheidung in einer benannten historischen Datei | aktuelle Wahrheit über HEAD, CI, Originaldaten oder Produktrelease |
| `E` | Extern belegt | konkrete Hersteller-/Norm-/Rechtsquelle, URL und Prüfungstag | Übertragung auf Steps ohne Integrationstest |
| `A` | Abgeleitet | Schlussfolgerung aus dokumentierten Voraussetzungen | empirischen Messwert/Owner-Entscheidung |
| `P` | Vorgeschlagen | technischer oder fachlicher Weg mit Trade-offs | genehmigte Umsetzung oder bestehende App-Funktion |
| `O` | Offen | Material fehlt oder Alternativen nicht entschieden | dass keine Lösung existiert |

Die Stufen sind **nicht ordinal**: Ein extern belegter Standard kann korrekt sein, aber für eine bestimmte Implementierungsentscheidung irrelevant. Ein negativer Test und eine fehlende Messung werden niemals als dasselbe behandelt. Jede neue Annahme muss einen **Falsifikator** erhalten: welche Datei, Codeprobe, Messung oder Nutzerentscheidung könnte sie widerlegen?

## 3. Wie V1 gegen die tatsächlichen Anforderungen geprüft wurde

1. **Bestand:** Dateien, Wortzahlen, ursprüngliche Aufträge, 24 Prompts, 89 historische Traceability-Einträge, acht lokale Upload-Artefakte sowie die zwei Git-Bäume erfasst. Statistische Inventare stufenweise geprüft; keine gefälschte Abdeckung durch Verzeichniszählung.
2. **Informationskette:** Anforderungen aus der aktuellen Nutzeranweisung und beiden Research-Strängen gegen V1 README, Projekt-Overview, Roadmap, Modul-/Reuse- und Prompt-Verträge gestellt. Eine bloße Ablage des Originals zählt nur als `preserved`, nicht als `actionable` oder `validated`.
3. **Quellenglaubwürdigkeit:** Repo-Dokument, HEAD, lokaler Upload, Forschungsreferenz und externe Primärquelle getrennt. Weitergeltende historische Details nicht gelöscht, aber als solche datiert.
4. **Widerspruch:** Was ist ein realer logischer Widerspruch (gleicher Gegenstand/gleicher Snapshot) und was ist nur unterschiedlicher Umfang, Zeitpunkt, Maßstab oder Modell? Beispiele: 1.146/1.306 Dateiangaben (Berichtssumme) gegen 1.000 tatsächlich gemessene Archivdateien (andere Bezugsgröße); 3.50.7 `main` gegen 3.53.0 *neuen* `main` (Zeitpunkt, kein gleichzeitiger Konflikt).
5. **Alternativen:** mindestens drei technische Übernahmewege, mehrere MVP-Scopes, Wissensrecherche/-Speicheroptionen, UI-/Audio-Auswahl und Organisation der KI-Arbeit bewertet. Empfehlungen nur vorläufig; sichtbarer Nutzen muss testbar sein.
6. **Reproduzierbarkeit:** referenzierte Commit-SHAs, Dateihashes, selbst erzeugte AST- und Modulregister und lokale read-only Auditwerkzeuge in `tools/audit/` bereitgestellt. Automatische Tests laufen nur auf dem Paket und künstlichen lokalen Fixtures, nicht auf fremden Nutzerdaten.

## 4. Umfang der Neubewertung

Die Abdeckungsmatrix `01_UNTERSUCHUNGSDIMENSIONEN.md` umfasst **33 voneinander abgegrenzte Dimensionen**, gruppiert nach Produkt, Fachwissen, Technik, Daten, Design, Rechte, Betrieb und Governance. Für jede Dimension ist der V1-Zustand, ein konkreter Defekt, der V2-Nachtrag und eine verbleibende Nachweisgrenze dokumentiert. Das `02_KORREKTUREN_UND_WIDERSPRUECHE.md` enthält fallbezogene Korrekturen mit Eingangs-/Ausgangsstatus. `03_ALTERNATIVEN_UND_ENTSCHEIDUNGEN.md` prüft Alternativen explizit. `docs/quality/VERIFICATION_PLAN_V2.md` und `docs/audit/05_VALIDIERUNGSBERICHT.md` sind die Prüf- und Beweislastdokumente; sie unterscheiden ausdrücklich durchgeführte Integritätschecks von nur geplanten Fach-/OS-Tests.

## 5. Kritische Schlussfolgerungen

- **Nicht über die Runtime entscheiden, bevor das Zielverhalten definiert ist.** Die vollständige Bewahrung *jeder* Glide-Funktion wäre mit dem Neuzuschnitt unvereinbar. Erhalten werden nach überprüfter Entscheidung *generische Fähigkeiten* – nicht unbemerkt Todo-Daten- oder Importverhalten. Für jedes Modul gilt eine eigenständige Übernahmeentscheidung.
- **Nicht aus einer Vorlagendatei auf eine funktionale Knowledge Base schließen.** `knowledge/sources/registry.yaml` ist laut Repo noch `sources: []`; die vorhandenen Forschungsberichte und 1.000 Archivdateien ersetzen keine normalisierten, reviewten Konzepte oder Retrieval-Tests.
- **Nicht ein einziges unprüfbares Produktversprechen verkaufen.** Chord Explorer + Harmony Theory + Drums + Groove + MIDI + Skill + Lernplattform + vollständige Musikproduktion + alle Glide-Funktionen sind in einem ersten Release voraussichtlich nicht belastbar abnehmbar. Vision und erster *nutzbarer vertikaler Slice* müssen unterschieden werden.
- **Nicht Forschungs- oder Fremdmaterial automatisch veröffentlichen.** Die MPL-Lizenz des Repositories gibt keine Rechte an beigefügten PDFs, Screenshots oder MIDI-Samples. Das öffentliche Repo wurde nicht allein durch `git rm` bereinigt, solange historische Commits weiter existieren.
- **Nicht Übernahme-„Werte“ ohne Kostenmodell behaupten.** Ein Modul, dessen Entkopplung plus Tests mehr kostet als eine kleine eigenständige Neufassung, ist keine echte Ersparnis. Abnahmedaten sollen die Wahl steuern.

## 6. Abgrenzung und wissenschaftliche Ehrlichkeit

Diese zweite Prüfung **ist keine erschöpfende Inhaltsanalyse sämtlicher GitHub-Artefakte und aller Musikbücher**. Ebenso ist ohne den abgeschlossenen Research-Chat-Export, Original-DOIs/Publikationsdateien, volle Git-Historie und native Rechnerläufe keine Bestätigung jeder Behauptung möglich. Sie macht aber die Lücken präziser sichtbar, prüft wesentlich mehr unabhängige Projektbelege, korrigiert relevante Statusfehler und übersetzt Erwartungen in testbare Vertragsobjekte. `100 % Dokumente im ZIP` ≠ `100 % Aussagen belegt` ≠ `100 % Funktionen implementiert` ≠ `100 % Release geprüft`.

**Startpunkt für das Projekt:** `docs/operations/EXECUTION_BACKLOG.md` – dort sind der nächste einzelne Schritt, benötigte Eingaben, Prüfgates und zulässige Parallelität notiert. Erst wenn ein Gate bestanden ist, als nächstes die darauf angewiesene Implementierung beginnen.

## Quellenanker

- Intern lokal: `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, §§1–18; `source_archive/Glide_Entwicklungsplan.md`, besonders §§18–21; `source_archive/README-Glide-System.md`, §§1–9; `source_archive/Glide-Aufgaben-und-Listen_v3.53.0.pyw`.
- Steps GitHub: https://github.com/n05a-design/steps/tree/75329fef46878a5ac816cef3690e612a9e8fe52c
- Glide GitHub: https://github.com/n05a-design/glide-to-do/tree/9e767bea5e21063466a28ac3a679406484ad5d5f
- Forschung: `research/notes/deep-research/legacy/` im Steps-Repo (sieben Einzeldateien, gesondertes Audit).
- Offizielle Standards/Dokumentation: https://www.mozilla.org/en-US/MPL/2.0/FAQ/ · https://www.mozilla.org/en-US/MPL/2.0/ · https://docs.github.com/en/repositories/working-with-files/managing-large-files/about-large-files-on-github · https://docs.python.org/3/library/tkinter.html · https://midi.org/standard-midi-files · https://www.w3.org/WAI/standards-guidelines/wcag/new-in-22/ .

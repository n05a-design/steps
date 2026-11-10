---
document_id: STEPS-PROJECT-CONTEXT-HANDOVER
version: 3.0.0
project: Steps
status: draft_pending_project_approval
created_at: 2026-11-08
language: de
---
# STEPS – Projektübergabe V3 (Forschungs- und Wissensaufbau)

## 1. Verbindliche Richtung

STEPS wird als unabhängige Open-Source-Anwendung zur musikalischen Erforschung, Erklärung und praktischen Komposition entwickelt. Die vier **gleichberechtigten** Forschungssäulen sind `Music Theory`, `Harmony`, `Chord Progressions`, `Composing`. Die explizite Erweiterung **Composing** hat gegenüber den älteren zwei Forschungsberichten Vorrang, ohne deren Inhalte zu verwerfen. Ein 'weiteres Konzept' genügt nicht: Codex soll schrittweise eine wirklich befüllte, fachlich überprüfbare Knowledge Base aufbauen. Der eigentliche Produktionscode, die Python-/Tkinter-GUI, die Branches, CI und Releases wurden **nicht** anhand eines STEPS-Repositories geprüft. Sie bleiben unbekannt, bis Codex vor Ort read-only auditiert.

## 2. Dokumentenlage

In `00_Archiv_V1/` befinden sich die **sieben** jetzt tatsächlich zugänglichen ursprünglichen Dateien: ursprüngliches README, der Master-Research-Prompt, zwei ältere Research-Berichte, Handover-Erstellungs-Prompt, Codex V1 Auftrag und die **fertig erzeugte** `PROJECT_CONTEXT_HANDOVER_V1.md`. Im alten ZIP waren nur sechs Dokumente, weil das Handover-Ergebnis damals noch nicht beigelegt war. Die veraltete Aussage im alten Handover, `Master-Research-Prompt.md` sei nicht vorhanden, ist **für dieses Paket widerlegt**: Die Datei existiert hier und wurde archiviert. Der alte Handover bleibt als historischer Kontext unverändert; V3 aktualisiert die nachweisbare Dokumentenlage. Das zuvor vom separaten Deep-Research-Lauf gemeldete V2-Erweiterungs-ZIP mit 18 Dateien war in der aktuellen Containerumgebung nicht als physisches Archiv verfügbar. Dessen in der Gesprächssitzung bekannte Konzepte sind berücksichtigt; die exakten V2-Bytes werden **nicht** als vorhanden ausgegeben. Eine umfassende Finalversion des ursprünglichen Research Papers ist von den zwei älteren Markdown-Reports zu unterscheiden; deren Existenz wird nicht fingiert.

## 3. Neu in V3

- 47 Web-/Edition-/Standard-/Datensatz-Registereinträge mit nachvollziehbaren Original-URLs, darunter Editions- und Metadatenalias-Einträge, keine 47 vollständig gelesenen Bücher.
- 50 explizit **nicht verifizierte** bibliografische Acquisition Candidates.
- 142 `THEORY-V3-*`-Konzeptkarten mit Definition, Beispiel, Scope-Grenzen und Quellenkandidaten.
- 77 typisierte `RULE-V3-*`-Objekte.
- 95 originale `PROG-V3-*`-Beispiele über verschiedene Stile mit Einschränkungen; teilweise Varianten und Transpositionen.
- 69 operative Kompositionstechniken.
- 19 originäre Kompositions**skizzen** mit Motiv, Harmonie, Form, Besetzung und Entwicklung.
- 110 spezifizierte Validation Cases, Mischung aus technisch und menschlich zu überprüfenden Fällen.
- Verknüpfte ausführliche Monografie, Concepts-/Progression-/Composition-Kataloge und V3 Codex Master Execution Prompt.

## 4. Historische Entscheidungen und Neuerungen

| Entscheidung | Status | Einordnung |
|---|---|---|
| Project name Steps und open-source Unabhängigkeit | CONFIRMED | Historische Anforderung erhalten |
| Theory/Harmony/Chord Progressions breit erforschen | CONFIRMED | Historischer Schwerpunkt erhalten |
| **Composing als gleichberechtigter eigener Forschungspfeiler** | CONFIRMED | Neu nach ausdrücklicher Nutzeranweisung |
| Research Library, Knowledge Base und Skill trennen | CONFIRMED als Zweck, konkrete Architektur PROPOSED | Bestehender Plan präzisiert |
| Mehrere Analyseschulen und mögliche Deutungen erhalten | CONFIRMED als wissenschaftliches Ziel | Kein einziges Universalmodell |
| Drum-/Groove-Engine und eigenständige Drum-Corpora zurückstellen | CONFIRMED/DEFERRED | Rhythmus/Metrum für Composing dennoch einbeziehen |
| Produktive KI und ML später, erklärbare Modelle zuerst | PROPOSED | Noch keine freigegebene Systemarchitektur |
| Vorhandene App wirklich umbauen | NOT AUTHORIZED IN THIS RESEARCH PACKAGE | Kein Repo-Audit erfolgte |

## 5. Forschungsabdeckung

Die V3 Monografie und Datenbibliotheken decken Notation, Intonation/Tuning, Intervalle/Enharmonik, Skalen/Modi, Akkorde, Funktionstheorie, modale/chromatische/Jazz-/Blues-/Pop-/R&B-/Gospel-/elektronische Harmonie, Stufen-/Multi-Lens-Analyse, Chord Progressions, Reharmonisierung, Voice Leading, formale Theorien, motivische Komposition, musikalische Form, Arrangement/Instrumentierung, Kognition/Erwartung, Transformation/Set Theory und computational data representation ab. Jede Kategorie ist mehr oder minder tief erschlossen; **nicht** alle sind aus Primärquellen atomar belegt und fachlich freigegeben. Traditionen wie Maqam/Raga/Gamelan erfordern spezialisierte zukünftige Arbeit.

## 6. P0-Blocker

- Echte STEPS-Repo-Realität nicht verifiziert.
- 20 ursprüngliche Roh-PDF-/TXT-Dateien nicht in diesem ZIP; nur ihre Beschreibung/Metadaten in historischen Reports.
- Original-Full-Text-Zugriff auf viele priorisierte Monografien fehlt.
- Urheberrechtliche Veröffentlichung der Original-PDFs nicht freigegeben.
- Exakte Claim-Seiten-/Abschnitts-Locators in V3-Seed-Objekten noch zu überprüfen; Quellkandidaten sind keine echten Claim-Evidenzen.
- Fachdurchsicht aller Chord-, Noten-, Harmoniefunktions- und Kompositionsstudien ausstehend.
- Alter Handover enthält zeitgebundene und jetzt veraltete Dokumentenlage; aktuell ist V3 maßgeblich.
- V2-Archiv nicht physisch beigelegt; bei Verfügbarkeit später gegen V3 reconciliieren.

## 7. Codex-Start

Beginne mit einer **read-only Bestandsprüfung**. Wende anschließend `CODEX_MASTER_EXECUTION_PROMPT_V3.md` an. Übernimm zunächst die V3-Daten als `draft`-Wissensobjekte und prüfe sie schrittweise, anstatt ihre bloße Existenz als fachliche Bestätigung zu behandeln. Bewahre alle alten Dokumente und Entscheidungen nachvollziehbar. Keine automatische Änderung am produktiven GUI-/Engine-Code und kein ungefragter Merge. Am Ende vollständige Zahl- und Qualitätsbilanz statt der Behauptung 'alles fertig'.

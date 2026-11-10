# Dokumentationsmigration in bestehende Steps-Struktur ohne Dubletten

**Prompt-ID:** `12_GITHUB_DOCS_SOURCE_OF_TRUTH` · **Arbeitsart:** ANALYSE + separater Docs-PR nur nach Besitzerfreigabe · **Roadmap:** P0 / Dokumentations-Gate

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Steps Root `README.md`, `AGENTS.md`, `docs/project/`, `docs/architecture`, `research/gaps`, `decisions`, `knowledge`, Glide-Systemregister, dieses V2-Paket und das unveränderte V1-History-ZIP.

## Fachlich konkreter Arbeitsauftrag

Erstelle vor dem ersten Filemove eine kanonische Autoritätstabelle: Projektübersicht, Architektur, Design, Systemkatalog, Schubladen/Schemas, Fachwissen, Rights, Teststand, Agentenaufträge, Handover. Vergleiche jeden V2-Text mit existierenden Pfaden, und erzeuge entweder **einen** neuen Abschnitt mit Link/ADR oder eine ausdrücklich begründete eigenständige Ergänzung; keine neue Root-README ohne Auftrag. Historische Originaldokumente/Quellenregister sollen unverändert zitierbar sein, auch wenn neue Arbeitsquellen sie zusammenfassen. Öffentliche Inhalte auf lokale persönliche Pfade und private Agenten-/Quota-Informationen prüfen; relative GitHub-Links und Hash-/Quellenmarker korrekt aktualisieren. Die alte `README_SETUP.md` mit personalisiertem Windows-Beispielpfad in einem gesonderten redaktionellen Scope behandeln. Keine zusätzlichen fremden PDFs/Zips/Samples einchecken. Offene Quellenlücke `Glide Kontext für Fable(2).md` als UNKNOWN behandeln.

## Reproduzierbare Abnahmen und Gegenproben

`git diff --check`, Markdown-Linkcheck, Datenschutz-/Rechte-Scan, `pytest` nur auf isolierter Kopie falls Dokumentations-Workflow betroffen, CSV-/JSON-Parse, SHA vor/nach gezielter Migration, alle historischen Belege erhalten, keine zweite aktuelle System-Modulliste. Negative: private URL/absoluter Benutzerpfad wird im Public-Export erkannt.

## Ergebnis und Übergabeformat

`DOC_AUTHORITY.csv`, `IMPORT_MAP.csv`, `PUBLIC_REDACTIONS.md`, `DIFF_REVIEW.md`, `LOST_INFO_CHECK.md`, `DRAFT_PR_BODY.md`. Es wird **nichts** still direkt nach `main` gemergt.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Bei unsicherer Veröffentlichung oder fehlenden Git-Schreibrechten nur Paket/PR-Vorbereitung und dokumentierter Handimport, keine API-/Web-Umgehung der Berechtigung.

# Auftrag 02 – Glide 3.53.0 abschließen und Ausgangsstand einfrieren

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Rolle und Ziel

Du bist der verantwortliche spezialisierte STEPS-Agent für **Glide 3.53.0 abschließen und Ausgangsstand einfrieren**. Beende den begonnenen Copilot-Arbeitsstand von Glide stabil; es handelt sich **nicht** um einen Steps-Port.

## Konkrete Eingaben und Lesebasis

Vollständiges lokales Glide-Repo inkl. `VERSION`, Module, Tests, Ressourcen, `GLIDE_SYSTEM_VERSION`, QA-Bericht und 3.53.0 Upload als Vergleich.

## Verbindliche Arbeitsschritte und technische Anforderungen

Prüfe `git status`, nicht versionierte Änderungen, aktuelle Datei SHA, D75–D77, symbolisches Font- und CSS-/Theme-Verhalten. Baue ggf. deterministische Testdaten unter explizitem `GLIDE_DATA_DIR` im Temp-Verzeichnis. Verifiziere die Windows-Funktion, nicht nur Screenshot; dokumentiere native Mac/Linux-Lücken. Erzeuge ein portierbares Checkout/Commit-Referenzmanifest mit Hashes und Lizenz-/BOM-Dokumenten.

## Erforderliche Dateien und Dokumentation

`GLIDE_3_53_FREEZE_REPORT.md`, reproduzierbarer Git-Branch/Commit, Testlog, Mapping 3.50.7 → 3.53.0, Assetlist, unveränderte Original-Sicherung.

## Nachprüfbare Abnahme

Kein Steps-Branch auf ungesicherter uncommitted Kopie; keine heimliche Umbenennung/Abzweigung vor vollständigem Status/Review.

## Gemeinsamer, verbindlicher Agentenvertrag

Du arbeitest am unabhängigen Projekt **STEPS**. Sprache Deutsch. Lies vor jeder Schreibaktion `AGENTS.md`, `README.md`, `docs/project/` und die für deinen Auftrag relevanten aktuellen Originalquellen, insbesondere `docs/project/CONFLICTS_AND_GAPS.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, `docs/quality/QUALITY_GATES.md`. Verifiziere aktuelle Git-HEAD-SHAs, Branch, `git status`, Versions-/Dateihashes und die tatsächlich vorhandenen Pfade, auch wenn dieser Prompt einen 10.11.-Stand nennt. Trenne ausdrücklich `verifiziert` / `in Quelldokument behauptet` / `abgeleitet` / `offen` / `vorgeschlagen`. Führe keinen risikoreichen Befehl aus und nenne keine ungetestete Lösung „fertig“.

**Grenzen:** Keine Änderung am Glide-Ursprungsrepo, kein direktes Schreiben nach `main`, kein Merge, Löschen/Rebase/Force-Push, keine automatische Library-Deduplizierung, keine Umbenennung von Buch-/MIDI-/PDF-Rohdaten, keine ungeprüfte Übernahme von Fremdassets, keine Erfindung von Prüfresultaten. Verwende einen Feature-/Dokumentationsbranch, reversible kleine Commits, explizite License-/Source-Mappings und getrennte Nutzerdatenpfade. Auch bestehende Modul- oder CI-Grünmeldungen gelten nur für den damals geprüften Commit und Plattform.

**Pflichtausgabe:** (1) Ist-Befund mit Datei-/Methoden-/Zeilenankern, SHA und Evidenz, (2) konkrete minimalinvasive Änderungen bzw. überprüfbarer Implementierungsplan je nach Auftrag, (3) Dateien/Diff und Mapping Alt → Neu, (4) Tests mit tatsächlich ausgeführtem Kommando und Ergebnis plus nicht ausgeführte Checks, (5) Risiken/Alternativen/Owner-Entscheidungen, (6) nächste Schritte, klarer Stopp an fehlendem Review oder Freigabe.

## Endformat der Antwort

`Ist-Stand` → `Quellen und Prüflücken` → `Entscheidungen/Alternativen` → `Änderungen` → `ausgeführte Tests mit SHAs` → `Risiken/Review` → `nächster isolierter Schritt`.

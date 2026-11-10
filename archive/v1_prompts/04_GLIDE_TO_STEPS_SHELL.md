# Auftrag 04 – Glide auf STEPS-Zweibereichs-Shell rückbauen

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Rolle und Ziel

Du bist der verantwortliche spezialisierte STEPS-Agent für **Glide auf STEPS-Zweibereichs-Shell rückbauen**. Erzeuge ein eigenes Steps-Desktopfundament mit **Sidebar + Workspace**, ohne Glide-Tasks zu aktivieren, aber mit sämtlichen UX-Infrastrukturfähigkeiten.

## Konkrete Eingaben und Lesebasis

Gepinnter Glide-3.53-Commit (nach Freeze), `GLIDE_TO_STEPS_2_AREA_SHELL.md`, `DESIGN_RICHTLINIEN`, Screenshot, `SIDEBAR_ACTION_AUDIT`, Steps app scaffold.

## Verbindliche Arbeitsschritte und technische Anforderungen

Extrahiere neutrales Tk-root, separat benannte App-/Cache-/Config-/Lock-Identität, Theme/Fonts/Logo-Mechanik, Menübar, Header mit Unterzeile, Icon-Toolbar, Tastatur/Focus/Scroll, Kompaktmodus, Sidebarein-/ausklappen, Section-Toggles, Settings, Such-Widget und statusfähige Arbeitsfläche. Keine Todo-Services. Deaktiviere nur Fachaktionen, **nicht** Shell-Bedienbarkeit. Falls 2 tatsächliche OS-Fenster gewünscht, zunächst ADR statt Architekturwechsel.

## Erforderliche Dateien und Dokumentation

`app/ui/shell`, `app/adapters`, Demo/Smoke, Vorher-Nachher-Fotos, Quell- und Lizenzmapping, Rollback-Commit.

## Nachprüfbare Abnahme

Tests: alle Seitenpunkte no-op, Menüs/Dialoge/Settings funktionieren, Fokus/Theme/Shutdown stabil, kein Glide-Datenzugriff/Glide-Branding; native Windows/Linux/Mac getrennt berichtet.

## Gemeinsamer, verbindlicher Agentenvertrag

Du arbeitest am unabhängigen Projekt **STEPS**. Sprache Deutsch. Lies vor jeder Schreibaktion `AGENTS.md`, `README.md`, `docs/project/` und die für deinen Auftrag relevanten aktuellen Originalquellen, insbesondere `docs/project/CONFLICTS_AND_GAPS.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, `docs/quality/QUALITY_GATES.md`. Verifiziere aktuelle Git-HEAD-SHAs, Branch, `git status`, Versions-/Dateihashes und die tatsächlich vorhandenen Pfade, auch wenn dieser Prompt einen 10.11.-Stand nennt. Trenne ausdrücklich `verifiziert` / `in Quelldokument behauptet` / `abgeleitet` / `offen` / `vorgeschlagen`. Führe keinen risikoreichen Befehl aus und nenne keine ungetestete Lösung „fertig“.

**Grenzen:** Keine Änderung am Glide-Ursprungsrepo, kein direktes Schreiben nach `main`, kein Merge, Löschen/Rebase/Force-Push, keine automatische Library-Deduplizierung, keine Umbenennung von Buch-/MIDI-/PDF-Rohdaten, keine ungeprüfte Übernahme von Fremdassets, keine Erfindung von Prüfresultaten. Verwende einen Feature-/Dokumentationsbranch, reversible kleine Commits, explizite License-/Source-Mappings und getrennte Nutzerdatenpfade. Auch bestehende Modul- oder CI-Grünmeldungen gelten nur für den damals geprüften Commit und Plattform.

**Pflichtausgabe:** (1) Ist-Befund mit Datei-/Methoden-/Zeilenankern, SHA und Evidenz, (2) konkrete minimalinvasive Änderungen bzw. überprüfbarer Implementierungsplan je nach Auftrag, (3) Dateien/Diff und Mapping Alt → Neu, (4) Tests mit tatsächlich ausgeführtem Kommando und Ergebnis plus nicht ausgeführte Checks, (5) Risiken/Alternativen/Owner-Entscheidungen, (6) nächste Schritte, klarer Stopp an fehlendem Review oder Freigabe.

## Endformat der Antwort

`Ist-Stand` → `Quellen und Prüflücken` → `Entscheidungen/Alternativen` → `Änderungen` → `ausgeführte Tests mit SHAs` → `Risiken/Review` → `nächster isolierter Schritt`.

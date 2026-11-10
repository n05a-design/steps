# Auftrag 09 – Chord Progression Editor, Harmony Explorer und Erklärung

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `9e767bea5e21063466a28ac3a679406484ad5d5f`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Rolle und Ziel

Du bist der verantwortliche spezialisierte STEPS-Agent für **Chord Progression Editor, Harmony Explorer und Erklärung**. Mach aus getesteten Musikmodellen eine nutzbare und erklärbare Arbeitsfläche.

## Konkrete Eingaben und Lesebasis

Chordmodelle, Progression Schema, Produkt-Overview U-01–U-11, gültiger neuer Steps Workspace, Quellen/Claims.

## Verbindliche Arbeitsschritte und technische Anforderungen

Ermögliche editierbare Akkordfolgen mit stabilem Step/Measure/Beat, Transposition, Tonartwechsel, Undo/Redo, History. Explorationsrelationen diatonisch/dominant/borrowed/voice-leading/transformational als getrennte typisierte, kontextualisierte Layers. UI zeigt Begründung, Stil/Framework, alternative Analysen, Evidenz und sichere Unknown-Hinweise; keine als universal etikettierte Popularität.

## Erforderliche Dateien und Dokumentation

`src/steps/progression/`, `app/ui/progression/`, Relations-Tests, 5 End-to-End-Szenarien und eigene Example-Daten.

## Nachprüfbare Abnahme

E7 → Am korrekt in a-Moll vs C-Dur, Fm als iv in C, transponierte I-V-vi-IV, mehrere Interpretationen und Back/Redo ohne Datenverlust.

## Gemeinsamer, verbindlicher Agentenvertrag

Du arbeitest am unabhängigen Projekt **STEPS**. Sprache Deutsch. Lies vor jeder Schreibaktion `AGENTS.md`, `README.md`, `docs/project/` und die für deinen Auftrag relevanten aktuellen Originalquellen, insbesondere `docs/project/CONFLICTS_AND_GAPS.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, `docs/quality/QUALITY_GATES.md`. Verifiziere aktuelle Git-HEAD-SHAs, Branch, `git status`, Versions-/Dateihashes und die tatsächlich vorhandenen Pfade, auch wenn dieser Prompt einen 10.11.-Stand nennt. Trenne ausdrücklich `verifiziert` / `in Quelldokument behauptet` / `abgeleitet` / `offen` / `vorgeschlagen`. Führe keinen risikoreichen Befehl aus und nenne keine ungetestete Lösung „fertig“.

**Grenzen:** Keine Änderung am Glide-Ursprungsrepo, kein direktes Schreiben nach `main`, kein Merge, Löschen/Rebase/Force-Push, keine automatische Library-Deduplizierung, keine Umbenennung von Buch-/MIDI-/PDF-Rohdaten, keine ungeprüfte Übernahme von Fremdassets, keine Erfindung von Prüfresultaten. Verwende einen Feature-/Dokumentationsbranch, reversible kleine Commits, explizite License-/Source-Mappings und getrennte Nutzerdatenpfade. Auch bestehende Modul- oder CI-Grünmeldungen gelten nur für den damals geprüften Commit und Plattform.

**Pflichtausgabe:** (1) Ist-Befund mit Datei-/Methoden-/Zeilenankern, SHA und Evidenz, (2) konkrete minimalinvasive Änderungen bzw. überprüfbarer Implementierungsplan je nach Auftrag, (3) Dateien/Diff und Mapping Alt → Neu, (4) Tests mit tatsächlich ausgeführtem Kommando und Ergebnis plus nicht ausgeführte Checks, (5) Risiken/Alternativen/Owner-Entscheidungen, (6) nächste Schritte, klarer Stopp an fehlendem Review oder Freigabe.

## Endformat der Antwort

`Ist-Stand` → `Quellen und Prüflücken` → `Entscheidungen/Alternativen` → `Änderungen` → `ausgeführte Tests mit SHAs` → `Risiken/Review` → `nächster isolierter Schritt`.


## Ergänzender Auditauftrag – explizite, bisher fehlende Prüftiefe

**Aktueller Quellenbezug:** Steps `75329fe`, Glide `9e767bea` (3.53.0); der lokale Glide-Upload ist *nur bei der Hauptdatei* blobgleich mit diesem Glide-HEAD. Siehe `docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`, `docs/quality/VERIFICATION_PLAN_V2.md` und `manifests/REQUIREMENTS_TRACE_28.csv`. Der ursprüngliche Prompttext ist in `archive/v1_prompts/` erhalten. 

1. Unterscheide Relationstypen `DOMINANT_OF`, `RESOLVES_TO`, `BORROWED_FROM`, `VOICE_LEADING_NEAR`, `TRANSFORMATION_OF`; gerichtete/symmetrische Regeln nicht vermischen.
2. Rankings nach expliziten Regeln, empirischen Häufigkeiten und kreativen Zielen trennen; jede Erklärung referenziert Claim-/Concept-ID, Kontext, Stil, Gegenbeispiel.
3. E7→Am als V7 in a-Moll und V7/vi in C-Dur, sowie bVII→I als stilabhängiger Fall testen; Unwissen sichtbar markieren.

**Zusätzliche Abnahme:** Liefere für jeden der genannten Punkte Quellenpfad und SHA, eindeutige Ergebnisartefakte, positive und negative Tests, einen getrennten `NOT_RUN`-Block sowie gegebenenfalls Owner-/Rechtsfreigabe. Dokumentiere den Unterschied zwischen *Entwurf* und *ausgeführter Arbeit* explizit.

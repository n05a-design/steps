# Index-Abdeckung und Prüfumfang


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

- `source_archive/`: **7 Text-/Code-/CSV-Originaldateien + 1 Screenshot** bytegleich kopiert.
- `source_archive/Steps_Quellenabdeckung_2026-11-09.csv`: **90 CSV-Zeilen einschließlich Header**, sechs historische Originalquellen als Teilkatalog; kein Index aller 1.931 aktuellen Repo-Dateien.
- `manifests/GLIDE_AST_METHOD_INDEX.csv`: **2722 Einträge** (einschließlich Klassen, Funktionen und Methoden), parse-only. Kein Runner/keine Isolation sämtlicher Methoden.
- `source_archive/Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md`: 39 ursprüngliche eigenständige Codeblöcke gemäß Vorbericht; Versionsvarianten stehen trotz Überschneidungen weiterhin darin.
- `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`: W01–W40/G01–G34 vollständig und unverändert; neue N01–N15 separat.
- Remote Trees strukturell abgefragt; alle PDFs und 1.000 Legacy-Dateien **nicht** vollständig inhaltlich extrahiert. Kein wissenschaftlicher Re-Review aller Quellen. Fehlender Originalbeleg C: `Glide Kontext für Fable(2).md`.

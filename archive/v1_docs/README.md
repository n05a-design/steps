# STEPS – konsolidiertes Projekt-, Übergabe- und Prompt-Paket

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Einstiegsreihenfolge

1. `docs/project/PROJECT_OVERVIEW.md` – Ziel, Ressourcen, aktuelle Tatsachen, Abgrenzung.
2. `docs/project/CHAT_HANDOVER.md` – präziser Kontext der heutigen Anfrage.
3. `docs/project/SOURCE_AND_REPO_AUDIT.md` – Quellen-, Code- und GitHub-Inventur.
4. `docs/project/CONFLICTS_AND_GAPS.md` – Konflikte, Inkonsistenzen und offene Gates.
5. `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md` – schonender Rückbauplan.
6. `docs/architecture/REUSE_AND_MIGRATION_MATRIX.md` – Teile, Entscheidungen, Migrationswellen.
7. `docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md` – Sequenz, Prioritäten, KI-Guthaben, DoD.
8. `knowledge/README.md` und `knowledge/INGESTION_PIPELINE.md` – evolvierende Bibliothek und Skill.
9. `prompts/README.md` – sofort verwendbare, getrennte Agent-Aufträge; Prompts erst **nach** dem Vorab-Audit freigeben.
10. `source_archive/` – vollständige unveränderte Kopien aller sieben Upload-Dateien und des Screenshots als Auditgrundlage. Bewusst **keine** externen Bücher oder Live-Website-Caches in diesem Paket.

## Dokumentationspolitik

- Ein Thema = eine kanonische Fachdatei; README verweist statt Fremdtexte zu duplizieren. Alle Upload-Originale und die bisherige 992-zeilige konsolidierte Overview bleiben unverändert im Archiv. `docs/project/CONFLICTS_AND_GAPS.md` ergänzt sie statt sie heimlich zu überschreiben.
- Erledigter Stand, technischer Versuch, vorgeschlagene Architektur und Produktentscheidung bleiben getrennt. Keine implizite Auswahl von Lizenz, Audioengine, Zwei-Fenster-Semantik, Markenidentität, Freigabe, Veröffentlichung oder Drum-MVP.
- Kein Programmcode von Glide in Steps kopiert, keine Quelle gelöscht, kein History-Rewrite, kein automatisch als frei lizenzierter Drittinhalt behandeltes Material.
- Repository-Dateien wurden remote strukturell inventarisiert, nicht alle 1.931 + 1.575 Dateien vollständig inhaltlich gelesen. Bücher und private/ungelieferte Originale benötigen separate Prüfung.

## Vor Arbeit auf GitHub

`git fetch` → `git status` → SHA der Quellen notieren → kurzer Feature-Branch → Diff/Tests → Review/Draft-PR. **Kein Merge ohne menschliche Abnahme**. Für echte Code-Arbeit den Glide-Lokalstand 3.53.0 zunächst commit-/dateigenau gegen Glide `main` 3.50.7 vergleichen. `docs/project/` des bestehenden Steps-Repositorys ist bereits befüllt und muss erhalten bleiben.

## GitHub-Übernahme ohne Datenverlust

Die aktuelle GitHub-Integration ließ am 10.11.2026 das Erstellen eines eigenen Dokumentationsbranches trotz angezeigter Repo-Schreibberechtigung **nicht** zu (HTTP 403). Daher kein Commit/PR und **keine Änderung an `main`**. Siehe [`HOW_TO_IMPORT_IN_GITHUB.md`](HOW_TO_IMPORT_IN_GITHUB.md) und das geprüfte Dry-Run-Skript [`tools/safe_stage_steps_docs.py`](tools/safe_stage_steps_docs.py): Es übernimmt auf einem lokalen **eigenen sauberen Branch** nur bislang fehlende Textdokumentation, überschreibt keine vorhandenen Files, ändert keine Git-Historie und publiziert die Original-Uploads nicht automatisch. In einem simulierten Git-Checkout bestanden Dry Run, Apply und Wiederholung mit 51 erzeugten Dokumenten und null Schreibkollisionen.

# STEPS – Skill-System für KI-gestützte Entwicklung und Fachfragen


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Zielarchitektur

`SKILL.md` an der Projektwurzel nur als orchestrierender Einstieg; Domain-Skills unter `skills/` nach klaren `name`-Kennungen. Ein Skill enthält Arbeitsanweisungen, Quellenwege, Rollen und Quality Gates, **nicht** alle 1.000+ Rohdateien als Kontext. Kompetenzen teilen: `music-harmony-coach` (vorhandene Vorlage), `steps-source-ingestion`, `steps-glide-migration`, `steps-domain-tests`, `steps-documentation-governance`, `steps-security-licensing` (neue Vorschläge, erst implementieren/registrieren nach Review).

## Vorhandener realer Stand

- `steps/SKILL.md`: existiert und verweist auf Projektkontext/Wissen/Migration.
- `steps/skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md`: existiert, zusammen mit `references/music-theory.md`, `harmonic-analysis.md`, `chord-progressions.md`, `voice-leading.md`, `sources.md`, `ingestion-guide.md` sowie einem Progression-Schema. Datumspfad kann nicht als automatisch entdeckter Skill angenommen werden; separaten normierten Symlink/Kopiervertrag für Toolprovider planen.
- `knowledge/sources/registry.yaml`: **leer**, eine Quelle aus fachlichen Texten allein macht den Skill nicht verifiziert.

## Regeln der AI-Abfragen

1. Nutzerfrage → Intent (`analysis`, `composition`, `explanation`, `source_ingest`, `migration`) → Fachgebiet/Framework (klassisch, Jazz, Pop usw.) → betroffene `concept_id`/Claims → überprüfter Retrieval-Index → Antwort mit Source-ID/Seitenlocator.
2. Falls nur unreviewed / restricted Daten vorhanden: nicht als gesichert ausgeben. Lizenzgrenzen bleiben auch für Chattexte und Repo-Publikationen bestehen.
3. Skill darf Interpretationen und kreative Vorschläge bieten, muss sie gegenüber überprüften Regeln und empirischen Tendenzen abgrenzen.
4. Für Codex/App-Implementierung liefert Skill Testfixtures, Datenmodelle und akzeptierte Quellen-IDs, nicht untestbare Produktentscheidungen.
5. Portable Ausgabe auch ohne ein bestimmtes Modell: pure Markdown-/YAML-/JSON-Schemas und CLI-Testreport. Claude-, ChatGPT-, Gemini- und Copilot-Adapter sind nur dünne provider-spezifische Einstiegspunkte.
6. Tokenbudget: nur relevante Dokumentabschnitte und die aktuell benötigten Source-Claims referenzieren; langes Research nicht bei jedem kleinen UI-Fix neu einlesen.

## Abnahme des ersten Skills

20 golden prompts (verschiedene Genres, enharmonisches Spelling, H/B, Transposition, sekundäre Dominante, Borrowing, bass/inversions, unklarer Stil, erfundene Quellen, geschützte Langauszüge) testen. Jedes Ergebnis: `pass`, `fail`, `review_required` plus überprüfte IDs, tatsächliche gelesene Quellen, Modell-/Skill-/Index-Version, Fehlerklasse. Bei Konflikten **kein** stilles Auswählen einer Theorie. Erst nach wissenschaftlichem Review `reviewed`.

# Kanonisches Knowledge-Register und fachlich geprüfter Harmony-Skill

**Prompt-ID:** `07_KNOWLEDGE_INGEST_SKILL_EVAL` · **Arbeitsart:** ANALYSE und begrenzter ingest-SPIKE nur nach Rights-Freigabe · **Roadmap:** P8

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Steps `knowledge/sources/registry.yaml`, `schemas/source,concept,analysis`, `skills/music-harmony-coach/.../SKILL.md`, Root `SKILL.md`, wissenschaftliche Research-Grundlagen, Rights-Triage Prompt 06.

## Fachlich konkreter Arbeitsauftrag

Baue zuerst keine riesige Skill-Datei. Entwerfe SourceRecord, Claim, Concept, Rule, Relation, Example, Evidence und Lizenzstatus als **getrennte Datenobjekte**. Eine Quelle mit `rights_status=unknown` wird nur als Metadateneintrag behandelt, nicht automatisch als öffentlich zitierfähiger Volltext. Prüfe 10–20 repräsentative kleine und erwiesenermaßen erlaubte Quellen/Notizen, dokumentiere Autor, Edition, URL, Abschnitt, Hash und alternative Forschungstraditionen. Füge nur *eigene, überprüfte* Begriffsdefinitionen mit SourceIDs in `knowledge/` hinzu; Root-Skill bleibt Router und Harmony-Skill Referenzindex. Entwirf Retrieval, das nicht einfach semantische Ähnlichkeit als Fachgültigkeit benutzt: begrenzte StyleLenses, Kritikerfälle und Rangierung nach Quellenqualität. Konkrete Erklärungen müssen `E7→Am` im Kontext und Pitchspelling unterschiedlich behandeln. Bei fehlender Fundstelle ausdrücklich verweigern, eine Buchseite zu erfinden. Neue Musiktheorie-Behauptungen vor App-Lerntext an einen Fachreview-Gate binden.

## Reproduzierbare Abnahmen und Gegenproben

Negative Eval-Sets: erfundene Seite, falsches H/B, Cmaj7→C7 Gleichsetzung, E7→Am ohne Schlüssel, widersprüchliche Schulen, unrechtmäßige Langzitate, `missing source`, Schema-/Linkfehler. Positive Evals: korrekt belegte Definition, alternative Analyse, deterministische Regel vs. probabilistische Stilstatistik getrennt. Eval muss bei absichtlich entferntem SourceRecord scheitern.

## Ergebnis und Übergabeformat

`KNOWLEDGE_SCHEMA_RFC.md`, `SOURCE_CARDS_10-20.csv`, `CLAIMS.csv`, `SKILL_EVALS.jsonl`, `EVAL_RESULTS.md` (nur tatsächlich ausgeführte Tests als PASS), Verweismatrix Ingest→Concept→Rule→UI/Skill.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Kein Freigabelabel für ungesehene Bücher/Datasets. Kein Direktimport der `research/`-Volltexte als Runtime-Abhängigkeit, kein zweites unabhängiges Faktenregister im Skill.

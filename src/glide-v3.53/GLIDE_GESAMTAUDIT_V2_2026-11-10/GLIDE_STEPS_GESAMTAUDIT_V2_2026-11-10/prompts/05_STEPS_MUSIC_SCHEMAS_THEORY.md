# Musiktheorie-Engine, Notation, Datenmodelle und Schema-Revision

**Prompt-ID:** `05_STEPS_MUSIC_SCHEMAS_THEORY` · **Arbeitsart:** ANALYSE, RFC und Testspezifikation; Code erst nach Domain-ADR · **Roadmap:** P5

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Steps `schemas/*.schema.json`, `src/steps/README.md`, `research/notes/deep-research/legacy/01_STEPS_Research_Foundation.md`, `02_...Blueprint.md`, `docs/project/overview`, `knowledge/sources/registry.yaml`.

## Fachlich konkreter Arbeitsauftrag

Erfasse die tatsächlichen Schemafelder per Git-Commit und liste jede unentscheidbare musikalische Semantik. Definiere eine kanonische Notations-/Pitch-/Interval-/Chord-/Voicing-/Key-/Analysis-Struktur mit expliziter deutscher H/B und internationaler B/Bb Darstellung, enharmonischem Spelling, Oktave und Intervallkategorien. Modell für HarmonicEvents inklusive rationaler Beatposition und Duration, rests, Sections, repeat, TempoMap und Status/ID; Progression als Eventliste statt nur chord Strings pro Takt. Analysen müssen alternative Stilrahmen und Evidenz zulassen, nicht eine algorithmische Wahrscheinlichkeitszahl als absolute Wahrheit behandeln. Schlage eine versionierte v2-Schema-Migration mit Fixtures und Unknown-Field-Verhalten vor, die bestehende v1-Quellnachweise erhält. Bestimme klare Boundary `src/steps` ohne Tk/Filesystem und Ports für Save/MIDI/UI. Arbeitsschritt MusicXML/Ableton-Import nur als spätere Option, sofern nicht im Produktauftrag als verbindliches Feature gewählt.

## Reproduzierbare Abnahmen und Gegenproben

Cmaj7/C7/Cm7, `E7→Am` in zwei Tonarten, F# vs Gb, enharmonic roundtrip, verschiedene Taktarten, Auftakt/Tempoänderung, Undo eines Spelling-Change und negative Werte. Für jedes Schema JSON-Syntax, Validation bei `additionalProperties`, deterministische Roundtrips, negative Inputsets; Golden Cases unabhängig manuell fachlich reviewen.

## Ergebnis und Übergabeformat

`DOMAIN_MODEL_RFC.md`, `schema_v2_proposals/` (nicht bestehende Schemas überschreiben), `GOLDEN_TEST_MATRIX.csv`, `SOURCE_CLAIM_TRACE.csv`, `MIGRATION_CONTRACT.md`, explizite offene Musiktheorieentscheidungen für Inhaber/Fachexperten.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Kein Chord-/Drum-Produktcode in `app/ui`, keine MIDI-Magie ohne Zeitmodell, keine erfundenen Buchquellen/Seiten und keine stillen Schemabrüche.

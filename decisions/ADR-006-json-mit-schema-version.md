# ADR-006: Datenhaltung – JSON mit ganzzahliger Schemaversion

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Gesamtspezifikation vom 17.11.2026 mit Angleichung an den Bestand

## Kontext
Der Vorschlag lautete JSON + Schema + atomarer Writer für den MVP, eine Datenbank erst nach gemessenem Bedarf. Bestehende JSON-Dateien führen `schema_version` als ganze Zahl (z. B. `GRAPH_AUDIT_PLAN.json`: `1`); die Schemas in `schemas/` heißen „v1“. Laut [`MUSIC_DOMAIN_AND_MIDI.md`](../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md) §6 sind `chord.schema.json` und `progression.schema.json` noch Stubs.

## Entscheidung
- Primäres Speicherformat ist **JSON mit versioniertem Schema**: menschenlesbar, in Git vergleichbar, ohne Zusatzbibliothek lesbar.
- **`schema_version` ist eine ganze Zahl**, beginnend bei `1`, konsistent zum Bestand. Kein zweites Format wie `"0.1.0"`.
- Schreiben atomar (temporäre Datei, dann Umbenennen).

## Auswirkungen
- Jede inkompatible Änderung erhöht `schema_version` und braucht Migrationspfad und Rückwärtslesbarkeit (§6).
- Vor dem Schema werden Testfixtures festgelegt.
- Rückfall: Eine Datenbank kann später als Index neben JSON entstehen.

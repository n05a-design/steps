# P05 – Reiner Steps-Musikkern und kanonische Datenmodelle

## Direkt nutzbarer Prompt

Erstelle aus den tatsächlich beschlossenen PRD-/ADR-Grundlagen ein **UI-freies, deterministisches und testbares Musikmodell** in `src/steps`. Der gegenwärtige `src/steps`-Baum im alten Git-Snapshot enthält hauptsächlich READMEs. Alte JSON-Schemas (`schemas/chord.schema.json`, `progression.schema.json`, `source.schema.json`, `analysis.schema.json`, `concept.schema.json`) vor Änderungen vollständig lesen und Migrationen planen, nicht brechen.

Definiere Werttypen für `PitchClass`, `SpelledPitch`, `Octave`, `Interval`, `NoteEvent`, `ChordSymbol`, `Voicing`, `ChordEvent`, `Track`, `Pattern`, `Project`, `TempoMap`, `MeterMap`, `TimePosition`, `Duration`, `SourceProvenance`, `Interpretation`. Identität/Seriellisierungsformat und die Versionierungsachsen `app_version`, `project_file_schema_version`, `music_domain_schema_version`, `knowledge_release`, `skill_release`, `glide_source_sha` separat führen.

Spezifiziere 12-TET als Anfangsscope oder explizit anderen Umfang; `H/B/Bb` und Tonartkontext, enharmonisches Spelling, Umkehrung vs. Slash-Bass, Akkordfamilien (Maj7/Dom7/Moll7), Alterationen, Stimmführung, Transposition, lokale Tonarten, Stile und alternative Analysen. Keine erzwungene singuläre Funktionsdeutung. Datenvalidierung vor MIDI/UI, keine Soundfont-/GUI-Abhängigkeit in der Domain.

Testfälle: Cmaj7≠C7≠Cm7, deutsch B vs englisch Bb, EN-B vs DE-H, transponiertes C–G–Am–F um +2 Halbtonschritte, chromatische Grenzen, leere/ungültige Namen, alternative Funktionsanalysen; interne Golden-Fixtures mit exakten Tönen und Notenlängen. Negative Property-Tests und deterministische Serialisierung. Erhalte Provenienz der eigenen Beispieldaten und Copyright-Grenzen fremder Songs.

## Akzeptanz

Lauffähige pure-Python-Tests aus frischem Checkout (ohne Tk/Audio), stabile immutable IDs/Serialisierung, dokumentierte Defaults, definierte Fehlerfälle und Schema-/Migrationtests; keine angeblich volle Musiktheoriedeckung nach wenigen Fällen.

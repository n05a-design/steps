# Drumgrid und MIDI-Export als eigener vertikaler Teststrang

**Prompt-ID:** `14_DRUM_GROOVE_MIDI_VERTICAL` · **Arbeitsart:** ANALYSE/Design; Implementierung nach eigener Freigabe · **Roadmap:** P7

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Steps `schemas/progression.schema.json`, Research Drums/MIDI-Archiv nur lizenzkonform, Domain-RFC aus Prompt 05, `app/audio` und `src/steps`-Platzhalter.

## Fachlich konkreter Arbeitsauftrag

Bevor irgendetwas hörbar wird, definiere eine **reine** DrumEvent-Timingstruktur: pattern ID, step index, beat offset/length, velocity, note/pitch, kit mapping, chance/swing (nur nach Scopeentscheidung), Per-Pattern-Meter/BPM und Loopphase. Trenne Pattern, Arrangement, Wiedergabe (optional) und Standard-MIDI-File-Export. Für gemeinsamen Chord+Drum-Loop muss dieselbe rationale Beatposition/Takt-/Tempomap gelten. Plane SMF-Type 0/1, PPQ, Track/Channel, Drum-Channel, metrical rounding, Tempo/TimeSignature-Metaevents, Note-Off und End-of-Track, robust gegen Events mit gleicher Tickposition. Dokumentiere Grenzen der Konversion zurück zu Styles/VoiceLeading/Probability und einen expliziten verlustbehafteten Import. Definiere eine einfache Bedienoberfläche mit Groove-Step-Knöpfen und Tastatur, ohne die Aufgabe durch Drum-DAW/Audioeffekte zu vergrößern. Prüfe externe Groove- und Samplekorpora auf Rechte, bevor ein einzelner geschützter MIDI-Loop als Demo getrackt wird.

## Reproduzierbare Abnahmen und Gegenproben

16/32 Steps, 3/4, 5/8, negative tempo/offset/velocity, simultane Hits, Chord+Drum bei unterschiedlicher Rasterunterteilung, Loop unter Tempoänderung, MIDI-Track parse in unabhängiger Library, Note-On/Off-Grenzen, keine negativen Delta-Ticks; exportierten Datei-Hash und musikalische Invariante getrennt. UI Keyboard + Stop-/Cleanup-/Restart-Tests, DataDir isoliert.

## Ergebnis und Übergabeformat

`DRUM_DOMAIN_RFC.md`, `MIDI_SMF_CONTRACT.md`, `MIDI_ROUNDTRIP_GOLDEN.csv`, `GROOVE_SCOPE.md`, `UI_KEYBOARD_MATRIX.md`, mögliche Bibliotheken mit Lizenz-/Dependency-Protokoll und Teststrategie.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Keine Echtzeit-/Audio-Latenzgarantien versprechen; MIDI-Export ≠ eingebauter Synth; keine kommerziellen Samples in öffentliche Testfixtures übernehmen.

# P02 – Produktdefinition, MVP und Entscheidungen

## Direkt nutzbarer Prompt

Du entwickelst das PRD für **Steps**, eine unabhängige Open-Source-Musikanwendung für Akkord- **und** Drum-Progressions, Harmonielehre und MIDI. Vorher die vorhandene konsolidierte Overview, V3-Prüfung, alte Positionierung, `AGENTS.md` und bestehenden Skill lesen; Widersprüche nicht glätten.

Formuliere zwei getrennte Ebenen: **(A) Engineering-M1**: vier Akkordtakte (C–G–Am–F), Analyse/Transposition, Save/Load/Undo und korrektes MIDI. **(B) Produkt-M2**: mindestens eine synchronisierte Drum-Spur plus gemeinsamer Zeitraster und belastbarer End-to-End-Workflow. Ein Chord-only-Demo darf nicht als vollständiger Chord+Drum-MVP dargestellt werden.

Lege nachvollziehbar dar: Jobs-to-be-done, Kernzielgruppen Anfänger/Musiker/Lehrende, primäre Nutzerreise (Akkordmuster bearbeiten, Rhythmus hinzufügen, anhören oder bewusst nicht, exportieren, später öffnen), Fehler-/No-Data-States, nichtfunktionale Anforderungen, Offline-Standard, Accessibility, Performance, Cross-Platform-Scope, Datenschutz, Lizenzgrenzen, Nicht-Ziele. Unterscheide musikalischen Tonhöhenvertrag von Audioplayback, und `H/B/Bb` von internationaler Notation.

Erzeuge pro ungelöster Frage eine ADR-Entscheidungsvorlage mit Alternativen/Kosten/Gates: tatsächliche zwei Fenster vs. zwei Inhaltsbereiche; notwendiges Playback und Synth-Soundbank; Ziel-OS; MIDI/DAW; harmonischer Erkläranspruch; Drum-Pattern vs. Step-Sequencer; Source/Knowledge-Anbindung; eigene Branding- und Datenpfade; eigene UI-Themen vs. Übernahme Glide.

Die ursprünglichen Dokumente sind historische Eingaben, kein Freigabebeschluss. **Keine Entscheidung stillschweigend als `accepted` markieren**, keine App-Codeänderung. Zentrale Produkt-Overview fortschreiben oder verlinkte PRD erstellen, je nach bestehendem Dokumentenvertrag. Führe messbare Nutzer-DoD, Risiken, Abhängigkeiten und offene Entscheidungen auf.

## Akzeptanz

Ein konsistenter MVP-Vertrag, klare M0/M1/M2/M3-Beschreibung, mindestens zwei prüfbare Nutzerreisen, offene Entscheidungen mit owner/status und Quellbezug, keine Verschmelzung von App- und Bibliotheksversion.

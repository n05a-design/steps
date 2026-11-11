# P06 – Akkord-/Drum-Timeline, MIDI und Playback-Entscheidung

## Direkt nutzbarer Prompt

Entwickle nach P05 ein gemeinsames, reproduzierbares **Timeline-Modell**, auf dem sowohl Akkorde als auch Drums in Steps aufliegen. **MIDI-Export erzeugt noch keine interne Tonwiedergabe.** Ein Drum-MVP ist von einem bloßen Akkordexport zu unterscheiden.

Lege in einem ADR fest: Tick-/PPQ-Basis, explizite Zeitpositions- und Dauerrechnung (Brüche statt früh float-Rundungen), Tempo-Map, Time-Signature, Taktgrenzen, Verschachtelung von Patterns, Velocity, Note-Off, Gate, Overlap, Swing/Groove, Triplets/Tuplets, Quantisierung, Mute/Solo, Loopgrenzen, Spurnummern, MIDI-Kanäle, Drum-Channel, Program/CC, Metaevents, Time-Delta-Sortierung. Dokumentiere, was absichtlich **nicht** zum MVP gehört.

Implementiere M1: vier Takte C–G–Am–F bei festem Tempo/4/4 mit bekannten Note-Events, Export Type-1-MIDI und **unabhängigem zweiten Parser** als Testoracle. M2 danach: separate Drumspur mit Kick/Snare/Hi-Hat, 1–2-Takt-Pattern, Velocity, Loop und Export synchron zum Akkordlauf. Lade die MIDI-Datei in einer externen DAW und dokumentiere reproduzierbares Prüfergebnis. Interne Projektdatei muss Undo/Redo, Save/Load und definierte Datenverluste beim MIDI-Reimport unterstützen. Akkordnamen, Funktionsanalysen und Provenienz sind ohne Metadaten nicht aus MIDI rekonstruierbar.

Erzeuge eine Playback-ADR mit mindestens drei Optionen: (a) export-only Engineering-Milestone, (b) externes MIDI-Gerät/DAW, (c) interner Synth/Soundbank mit rechtlich geklärter Quelle. Bei interner Wiedergabe Scheduler/UI-Thread-Abgrenzung, Device-Verlust, Stop/Panic, Latenz und native Backendtests; kein zweifelhafter Download von Soundbanks.

## Akzeptanz

M1 Parser-Roundtrip mit expliziter Eventtreue; M2 synchrone Chord/Drum-Spuren; erzwungene Fehlerfälle (null/negative Tempo, ungültige Note, Note-Off-Order, Dateiüberlauf) kontrolliert; keine Playback-Behauptung ohne Audio-/Backendtest.

# ADR-007: Audio/MIDI: Ports zuerst, Backend nach Plattform-/Lizenzbenchmark

**Status:** accepted  
**Datum:** 2026-11-17  
**Entscheidungsträger / Beleg:** STEPS Core Architecture Team; M05/M07/M11 Spezifikation; PR #108; Arbeitsvertrag AGENTS.md

## Kontext
Für STEPS ist die akustische Wiedergabe und der Export von Akkorden, Kadenzen und Grooves eine zentrale Anforderung. Allerdings bestehen bei Desktop-Audio gravierende Risiken:
1. **Thread-Deadlocks in Tkinter:** Audio-Bibliotheken oder Scheduler, die `time.sleep()` direkt in Event-Callbacks ausführen, frieren die grafische Oberfläche ein.
2. **Plattformabhängigkeiten & Lizenzen:** Externe C-Bibliotheken (z. B. PortMidi, Fluidsynth, RtMidi) erfordern plattformspezifische Binaries, erzeugen Installationsprobleme auf Windows/macOS/Linux und werfen Lizenzfragen auf.
3. **Headless & CI-Testbarkeit:** In CI-Pipelines (z. B. GitHub Actions oder Headless-Containern) existieren oft keine Audio-Treiber oder Hardware-Soundkarten.
4. **Hängende Noten (Hung Notes):** Unvollständige oder fehlende Note-Off-Meldungen bei Abbruch, Loop oder Stop ruinieren die User Experience und verletzen Invariante T14.

## Entscheidung
Wir etablieren eine strikte **Ports & Adapters (Hexagonale) Architektur** für Audio und MIDI:
1. **Domain-Trennung:** Der Musikkern (`src/steps/theory/`, `src/steps/models/`) erzeugt reine mathematische und musikalische Strukturen (Ticks, Pitch-Klassen, Voicings) und importiert niemals Audio-Treiber oder Tkinter.
2. **AudioBackendPort & NullAudioBackend:** Definition eines abstrakten Ports `AudioBackendPort`. Das integrierte `NullAudioBackend` fungiert als speicherbasiertes, thread-sicheres Referenz-Backend für Headless-CI und Fallback ohne Audio-Geräte.
3. **MonotonicPlaybackScheduler:** Eigener Daemon-Worker-Thread, getrieben von `time.monotonic()`. Unterstützt Pause, Stop, Seek und Seamless-Looping. Sendet bei jedem Stop, Pause, Seek und Loop-Sprung zwingend `all_notes_off()` zur Garantie der T14-Invariante.
4. **UI-Thread-Isolation:** Optionaler `ui_dispatcher` (z. B. Tkinter `root.after_idle`) entkoppelt Status- und Tick-Meldungen vollständig vom Audio-Thread. Kein Audio-Sleep im Hauptthread.
5. **Reiner Python SMF-Export:** `src/steps/midi/` implementiert vollständigen Standard-MIDI-File (SMF) Format 0 und 1 Export ohne externe C-Bibliotheken.

## Auswirkungen
- **Trade-offs:** Direkte Klangsynthese (Softsynth/Soundfonts) wird im ersten MVP-Schnitt auf native MIDI-Outs oder Null-Playback beschränkt; Software-Synthesizer werden später über separate Adapter angebunden.
- **Kompatibilität:** 100% plattformunabhängig und offlinefähig auf macOS, Linux und Windows ohne zusätzliche native Shared Libraries.
- **Testbarkeit:** Alle Transport-Zustandswechsel, Loops und Note-Off-Paarungen sind in Millisekunden deterministisch testbar.

## Links
- `prompts/07_ARCHITECTURE_PORTS.md`, `prompts/11_MIDI_AUDIO.md`
- `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`
- `src/steps/ports/audio.py`, `src/steps/midi/`
- Golden Invariants T14 & T15 in `tests/test_golden_music_invariants.py`

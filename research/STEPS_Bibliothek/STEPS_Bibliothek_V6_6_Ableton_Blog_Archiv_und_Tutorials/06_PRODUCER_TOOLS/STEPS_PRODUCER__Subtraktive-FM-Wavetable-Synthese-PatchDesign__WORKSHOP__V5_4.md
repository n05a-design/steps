# STEPS V5.4 – Synthese als reproduzierbare Klangkomposition

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Warum Noten und Timbre getrennt sind
Ein 16-taktiger Akkordplan enthält noch keinen fertigen Track. **Synthesestruktur** bestimmt Spektrum und Zeitverlauf: Oszillatoren, Frequenzmodulation, Wavetable-Position, Filter, LFO, Hüllkurven, Sättigung und Stimmenzahl. Steps soll die analytische Beschreibung (welches Signal wird wie moduliert?) von konkreten Plug-in-Presets unterscheiden. Offizielle Ableton-Operator-Dokumentation (SRC54-012) belegt FM sowie subtraktive/additive Komponenten in diesem Instrument, ist aber keine allgemeingültige Klangbewertung.

## Patch A – Subbass mit Grundtonkontrolle
Oszillator: Sinus oder schwach angereicherte Welle, monophon, kein Unison; Filter optional. Amplitudenhüllkurve Attack 3 ms, Decay 130 ms, Sustain nahe 0,75, Release 80 ms, nur **Ausgangspunkt**. Achte auf hörbares Click bei sehr kurzen Zeiten und auf die Bassdauer beim Wechsel zwischen `legato` und `retrigger`. Bei 43,65 Hz (F1) beträgt eine Sinusperiode ca. 22,9 ms. Ein 1-ms-Hüllkurvenwechsel kann darum starke transiente Anteile erzeugen. Lasse eine Bassnote 0,25s und die nächste 0,5s triggern; beurteile, ob definierte Note-Offs hörbar sind.

## Patch B – Pad mit beweglicher Obertonstruktur
Zwei leicht gegeneinander verstimmte Oszillatoren (z. B. Sinus + Sägezahn), sanfter 24-dB-Tiefpass als Ausgangshypothese, langsame Attack/Release, sparsame Filtermodulation. Für dichte Akkorde Clip/Masking bei gleichen Registern prüfen. „Warmes Pad“ ist kein numerisch wissenschaftliches Label, sondern ein ästhetischer Eindruck.

## Patch C – FM-Pluck
Ein Trägeroszillator auf Grundfrequenz und Modulator mit nicht zu hohem Index; exponentiell abklingender Modulationsindex, kurze Amp-Decay. Ergebnis spektral komplexer als reiner Sinus, ohne dass ein einziges Spektrum als Genredefinition gelten darf. Prüfe Aliasing für hohe Noten; eine MIDI-Note von C7 klingt auf Instrumenten mit unterschiedlicher Oversampling-Strategie verschieden.

## Patch-Schema und Test
`algorithm`, `oscillators`, `frequency_ratio`, `filter_type/cutoff/resonance`, `envelopes`, `mod_routes`, `tuning`, `polyphony`, `preset_origin`, `plugin_version`, `audio_render_hash`. Datenprüfung verifiziert zulässige Parameterbereiche, nicht klangliche Qualität. Nur mit realem Render lassen sich Headroom, ungewollte Obertöne und Latenz prüfen.

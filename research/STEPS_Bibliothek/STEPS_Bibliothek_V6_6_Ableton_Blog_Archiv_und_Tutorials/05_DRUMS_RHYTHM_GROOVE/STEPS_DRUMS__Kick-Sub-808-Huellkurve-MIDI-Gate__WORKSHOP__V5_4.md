# STEPS V5.4 – Kick, Sub und 808: drei unabhängige Lebenszyklen

**Stand:** 2026-11-08 · **Status:** ausgearbeitete Arbeitsfassung; stilistische und akustische Fachprüfung offen · **Urheberschaft:** eigene didaktische Beispiele

## Fehlerquelle
Ein MIDI-Note-On startet ein Ereignis, Note-Off beendet **den Triggerzustand**; ob der Klang dann endet, hängt vom Sample-Modus und den Lautstärke-/Filterhüllkurven ab. Bei einer 808-One-Shot mit langem Sample kann ein Rechteck mit 0,2 s MIDI-Dauer trotzdem 2 s hörbar klingen. Umgekehrt kann ein 808-ADSR mit aktiviertem Release auf Note-Off reagieren. Das ist ein hörbarer Produktionsunterschied, der im MIDI allein nicht beweisbar ist.

## Eigene 4-Takt-Studie
Bei 154 BPM (77-BPM-Halftime-Empfindung) platziere Kick onsets auf T1 Step 1, T2 Steps 5/11, T3 Step 1, T4 Steps 5/11. Wähle im Bass Eb1, C1, Ab1, F1 als eigenständige Originalübung **ohne** Übernahme einer veröffentlichten musikalischen Aufnahme. Für die zugehörigen Basstöne lege Stopps bei `0,81s`, `0,23s`, `0,62s`, `0,23s` als konkrete **Testparameter** fest, aber interpretiere die Ergebnisse nicht als historische Produktionsdaten.

## Interlock-Analysen
- `OnsetInterlock`: Anteil von Kick-Hits, bei denen innerhalb tolerierter Zeit ein neuer Sub-Hit startet.
- `PitchInterference`: Kick-Fundamental und Sub-Grundton können überlappen; konkrete Maskierung erfordert Audio-FFT/Hörtest und ist aus Noten allein nicht ableitbar.
- `EnvelopeOverlap`: Bass-Release und nächste Note können sich überlappen; eine Probe braucht Patch/Sampleparameter.
- `SidechainDuck`: misst Pegelkurve oder bekannten Compressorzustand, ist nicht aus CC7 oder MIDI-Note-Off garantiert.

## Gute Testbedingungen
Ein Sampler mit ausdrücklichem `note_off_mode=release` und einer mit `note_off_mode=ignore` müssen bei identischem MIDI unterschiedliche Klanglängen *erlauben*. Ein sicherer Steps-Befund lautet daher `midi_gate_length=...`, `sounding_duration=unknown` solange weder Audio noch Instrumentenparameter vorliegen. Formatierung `Eb1 vs D#0 Live` ist als `octave_policy`-Thema zu behandeln (SRC54-015 dokumentiert GM-Notenbelegung, nicht Live-Oktavnamen).

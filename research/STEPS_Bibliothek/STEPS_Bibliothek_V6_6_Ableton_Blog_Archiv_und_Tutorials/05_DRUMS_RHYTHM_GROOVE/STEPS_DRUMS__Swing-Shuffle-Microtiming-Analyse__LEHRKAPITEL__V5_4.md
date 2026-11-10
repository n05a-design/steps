# STEPS V5.4 – Swing, Shuffle, Timing-Offset und messbarer Groove

**Stand:** 2026-11-08 · **Status:** ausgearbeitete Arbeitsfassung; stilistische und akustische Fachprüfung offen · **Urheberschaft:** eigene didaktische Beispiele

## Definition mit Einheiten
Im 16-Schritt-Raster bei 120 BPM beträgt ein Schritt 125 ms. Verschiebe nur die zweite Sechzehntelposition jedes Achtelpaares von 125 ms auf 165 ms, dann beträgt das Offset +40 ms relativ zum geraden Grid. Das ist eine *Timing*-Änderung. Eine „65%-Swing“-Angabe kann je nach Hersteller eine andere Bezugsdefinition haben und muss deshalb in Steps mit einer präzisen mathematischen Konvention und einer importierten DAW-Quelle abgelegt werden.

## Das Originalexperiment
Muster A: Kick [1,9], Snare [5,13], Hats [3,7,11,15] (1-basiert), alle exakt auf 16tel-Raster. Muster B: dieselben Onsets plus zusätzliche Hats auf [4,8,12,16], diese zweiten Hats mit +35 ms und niedrigeren Velocities. Muster C: Onsets wie B, ohne Zeitversatz, aber mit denselben Velocity-Werten. A→B ändert Dichte, Timing und Akzent; B→C isoliert *ausschließlich den Einfluss des Timing-Offsets*. Für eine kontrollierte A/B-Frage muss nur **eine** Variable verändert werden.

## Gemessene vs. geschätzte Parameter
Wenn der Kurs z. B. eine 33,1-ms-Verschiebung für UK Garage bei 132 BPM nennt, ist das eine konkrete Kurskonfiguration, kein Ersatz für eine professionelle Schlagzeuger-Messstudie. Songtranskriptionen aus Audio führen einen `measurement_uncertainty`-Wert und können Sample-Start-Latenz, Humanization oder Materialfehler nicht vollständig unterscheiden.

## Datenschema und Checks
Jeder Hit erhält `step_1based`, `onset_beat`, `onset_offset_ms`, `velocity`, `gate_beats`, `instrument_role`, `source_type`. `swing_policy` definiert delayed step group, offset formula and clamp behavior. Quantisierte und geswungene Varianten werden getrennt exportiert. Die Metadaten enthalten `timing_origin=authored|measured|imported`. In der Live-Groove-Pool-Dokumentation (SRC54-010) sind Timing, Random und Velocity getrennt steuerbar; konkrete Gerätewerte sind nur DAW-spezifisch übertragbar.

## Regression
An 132 BPM beträgt ein 16tel `113,636...` ms; addiere +33,1 ms nur zu definierten Steps. Unbetroffene Ereignisse bleiben tickgleich. Beim Runden auf MIDI-PPQ max. Quantisierungsabweichung als Prüfwert protokollieren.

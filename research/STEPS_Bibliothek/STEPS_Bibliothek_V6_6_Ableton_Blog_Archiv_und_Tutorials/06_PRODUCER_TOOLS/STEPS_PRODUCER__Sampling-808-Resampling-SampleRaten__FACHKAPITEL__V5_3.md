> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Sampling, Resampling und 808-Artikulation

## 1. Sampling ist nicht nur ein Waveform-File
Relevante Daten: `sample_id`, `creator`, `rights`, `recording_source`, `sample_rate`, `bit_depth`, `channels`, `root_note`, `loop_start/end`, `attack/release`, `transposition`, `warp_mode`, `playback_mode`, `velocity_mapping`, `choke_group`. Tonhöhe, zeitliche Länge und Envelope-Verhalten können unabhängig voneinander verändert werden. Sampling-Lizenzen gelten nicht automatisch als frei, nur weil ein Audiofile in einer DAW geöffnet werden kann.

## 2. Sample Rate und Aliasing
Die Nyquist-Frequenz beträgt bei Abtastrate `Fs` die Hälfte der Rate. Ein ideales Signal oberhalb von Fs/2 kann nicht ohne geeignete Vorfilterung in dieses Raster überführt werden; Aliasing und Rekonstruktionsfehler sind zwei unterschiedliche Prüfziele. Sample-Rate-Conversion braucht ein Filter- und Qualitätsmodell. **Vermeide** die Aussage, dass das Exportieren von 44,1 auf 96 kHz nachträglich fehlende hochfrequente Information wiederherstellt.

## 3. 808-Sound: vier getrennte Ereignisbegriffe
(a) MIDI-Note-On, (b) MIDI-Note-Off, (c) Sampler-Hüllkurve, (d) tatsächlich hörbarer Audioausklang. In einem One-Shot-Modus kann die Note-Off-Länge den Sound nicht beenden. **Eigener Versuch:** Zwei identische MIDI-Onsets für eine A1-Subbass-Note, aber 200 ms und 800 ms Note-Off; einmal One-Shot, einmal Gate/Envelope. Erwartung: nur im Gate-Modell folgt die Klangdauer zuverlässig der MIDI-Länge. Klangdatei und exakte ADSR-Werte müssen dokumentiert sein, sonst bleibt es Hypothese.

## 4. Kick–Bass-Beziehung
Überlappung von Kick und Sub kann musikalisch gewünscht sein oder Transienten maskieren. Es existiert keine physikalische Vorschrift „Kick und Bass dürfen nie gleichzeitig spielen“. Drei Entscheidungen getrennt: **Arrangement** (Bass attack verschieben), **Sound Design** (Envelope/Spektrum), **Mixing** (EQ/Dynamics/Sidechain). Jede erzeugt andere Klang- und Groove-Effekte. Sidechain-Pumping ist eine Option, kein universeller Reparaturmechanismus.

## 5. Transposition und Identität
MIDI 27 ergibt bei A4=440 und 12-TET ca. 38,89 Hz; die DAW-Anzeige kann dieselbe Note `D#0`, `Eb1` oder anders nennen, je nach Oktavkonvention. Die tatsächliche Samplefrequenz kann von transponiertem und detuntem Sample abhängen. Ein PPR-Fan-Remake ist deshalb nicht mit einem authentifizierten Originalstemsatz zu verwechseln.

## 6. Prüfroutine
Berechne und dokumentiere Root-Pitch, gespielte Note, Abspielrate, Envelope-/Warp-Modus, tatsächliche Ausgangsfrequenz (falls Audio verfügbar), Out-of-Tune-Status und Rechte. Überprüfe neue Samples vor öffentlicher Aufnahme durch einen Lizenzgate. Eigene generierte Sinus-/Rausch-Beispiele sind für technische Unit Tests häufig besser als kommerzielle Loop-Packs.

### Nachweise
Ableton Live 12 Simpler/Sampler/Drum Rack: https://www.ableton.com/en/manual/live-instrument-reference/ und https://www.ableton.com/en/manual/instrument-drum-and-effect-racks/ . Nutzer-Remake-Lektion als private, nicht-authentifizierte Lehrquelle, V5.1-Registry.

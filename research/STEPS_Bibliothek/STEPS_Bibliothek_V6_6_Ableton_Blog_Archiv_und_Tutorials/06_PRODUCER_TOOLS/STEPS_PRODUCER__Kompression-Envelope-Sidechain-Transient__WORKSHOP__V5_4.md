# STEPS V5.4 – Kompression, Transienten und Sidechain ohne magische Presets

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Regelkreis
Ein klassischer dynamischer Kompressor erkennt einen Pegelverlauf und setzt über Threshold, Ratio, Attack, Release, Knee und ggf. Lookahead eine zeitabhängige Verstärkungsregelung um. Attack 30 ms „lässt alle Transienten durch“ ist falsch als allgemeine Aussage: Frequenzinhalt und Detector/Feedforward-Design beeinflussen die Wirkung. Bei Kick und Snare kann derselbe Parameter auf zwei Plug-ins hörbar verschieden wirken.

## Vier experimentelle Setups
A. **Klassische Snare-Kontrolle:** Input so pegeln, dass im Backbeat kurzzeitig 2–4 dB Reduktion erscheinen; A/B bei gleichem Ausgangspegel. Release so wählen, dass Gain Reduction vor dem nächsten relevanten Hit sinnvoll zurückgeht. 2–4 dB ist ein *Arbeitswert*, kein Normziel.
B. **Kick→Bass-Sidechain:** Kick triggert Envelope auf separatem Bus, Bass bekommt max. -3 dB zum Onset und erholt sich binnen konfigurierter Zeit. Die musikbezogene Seite ist `kick_bass_interlock`; die technische ist ein Gain-Control-Signal.
C. **Parallelkompression:** Dry/Wet getrennt aufnehmen; Pegel steigen häufig allein durch Summe, daher loudness-matchen.
D. **Limiter/Clipping:** Limiter fängt Peaks unter Ceiling ab, kann aber bei zu starken Parametern Transienten und Verzerrungen ändern. Keine unüberprüfte Genre-Lautheitsregel ausgeben.

## Quantitative Cases
Ein idealisierter statischer 4:1-Kompressor über Threshold und 8 dB Eingangs-Übersteuerung würde im einfachen Modell 2 dB oberhalb Threshold ausgeben, also 6 dB statische Reduktion – **nicht** die tatsächliche Peak-Hüllkurve im komplexen Song. Gain Reduction in dB ist eine zeitabhängige Größe; langsame Attack verhindert nicht grundsätzlich Peak-Überschreitung.

## Codex-Daten
`detector_type`, `routing`, `envelope_attack_ms`, `release_ms`, `ratio`, `knee`, `threshold_db`, `gain_reduction_trace`, `sample_rate`, `plugin_model`, `experiment_provenance`. Ohne Audio kein fiktiver GR-Meter-Output. Der Drum-Buss/Glue-Workflow aus den Nutzertexten wird als gerätespezifische Fallstudie behandelt.

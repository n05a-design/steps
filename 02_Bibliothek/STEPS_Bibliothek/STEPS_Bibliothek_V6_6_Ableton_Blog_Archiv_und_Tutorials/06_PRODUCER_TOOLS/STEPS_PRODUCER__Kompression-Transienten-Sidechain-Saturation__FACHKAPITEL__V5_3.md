> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Dynamikbearbeitung: Compressor, Sidechain, Saturation und Transienten

## Grundmechanik eines Compressors
Ein Compressor modelliert einen Pegeldetektor (Peak/RMS-ähnlich oder spezialisierter), eine Steuerkennlinie (Threshold, Ratio, Knee), zeitliches Verhalten (Attack, Release) und Gain-Anpassung. Bei einer vereinfachten statischen Kennlinie oberhalb des Thresholds `T` und Ratio `R` kann die Ausgabe als `T + (input_dB - T)/R` modelliert werden; dies beschreibt **nicht** alle dynamischen Eigenschaften realer Geräte. Attack und Release bestimmen, wie schnell das System auf Änderungen reagiert; hohe Ratio und langer Release können das musikalische Pulsgefühl deutlich verändern.

## Drei unterschiedliche Ziele
**Dynamic control:** leise und laute Bestandteile ausgleichen, damit eine Spur im Arrangement stabil ist. **Envelope design:** Punch oder Sustain anders formen, z. B. per Transient Designer oder Drumbus. **Rhythmic sidechain:** ein Steuersignal (z. B. Kick) löst auf einer anderen Spur (z. B. Bass/Pad) regelbare Gain-Reduktion aus. Diese drei Ziele unterscheiden sich selbst dann, wenn dasselbe Plugin verwendet wird.

## Originalversuch auf vier Takten
Bei 120 BPM spiele eine Kick auf jeder Viertel, einen gehaltenen Subton und einen langen Padakkord. Version A: keine Sidechain. Version B: leichte Kick-getriggerte Reduktion am Pad mit kurzer Erholungszeit. Version C: stärkere Reduktion und längere Erholung. Version D: keine Sidechain, stattdessen Note-Längen/Pad-Lautstärken rhythmisch komponieren. **Vergleich:** A/B/C/D bei angeglichenem Gesamtpegel; hörbare Pumpstärke, Klarheit der Kick und melodische Kontinuität separat bewerten. Effekt-Einstellungen sind Stilentscheidungen, kein Konsens über „richtiges Mixing“.

## Saturation versus Clipping
Saturation verändert durch nichtlineare Übertragung das Obertonspektrum; Clipping begrenzt Signalwerte und kann deutliche Verzerrungen und Aliasing erzeugen. Die Art der Kennlinie, Input Gain, Oversampling, Headroom und nachgelagerter Pegel beeinflussen die Wirkung. **Tests:** identischer Sine-Pegel vor der nichtlinearen Stufe, Output-Lautheit matchen, Spektrum vor/nachher vergleichen und Alias-Spiegelungen prüfen. Nicht „Saturation macht Bass immer größer“ als Norm ablegen.

## Debugging
Muss der Snare-Transient erhalten bleiben? Attack/Threshold/Gain Reduction betrachten. Pumpt die ganze Summe unerwünscht? Routing- und Detektorsignal prüfen. Fehlt der Bass? Effekt und Arrangement gemeinsam betrachten. Equalizer-/Compressor-Reihenfolge beeinflusst Detektion und Klang; das muss dokumentiert sein. Kein unbesehenes „Threshold -4.9 dB“ aus einem bestimmten Kurs-Kit auf andere Samples übertragen.

### Nachweise
Ableton Live 12 Audio Effect Reference (Compressor, Glue, Drum Buss): https://www.ableton.com/en/manual/live-audio-effect-reference/ . Herstellerbeschreibung der Funktionen; genaue Effektkurven/Audioreview nur mit konkreter Instanz bestätigt.

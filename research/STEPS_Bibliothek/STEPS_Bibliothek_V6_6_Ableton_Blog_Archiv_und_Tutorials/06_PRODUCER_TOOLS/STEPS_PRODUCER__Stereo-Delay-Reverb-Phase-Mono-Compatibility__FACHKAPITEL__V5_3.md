> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Raum, Panorama und zeitliche Effekte – Mixing und Composing

## Stereo ist eine Relation, keine beliebige „Breite“-Skala
Die Wahrnehmung räumlicher Breite hängt von Pegel-, Laufzeit-, Phasen- und spektralen Unterschieden sowie vom Wiedergabesystem ab. Bei übermäßiger gegenphasiger Bearbeitung kann die Monosumme Inhalte stark auslöschen. Eine gute DAW-Werkstatt prüft deshalb nicht nur einen Korrelationsmeter, sondern hört die Mischung auch mono, leise und in unterschiedlichen Wiedergabekontexten.

## Delay gegen Reverb
**Delay** erzeugt erkennbare Wiederholungen, deren Timing sowohl in Millisekunden als auch in Beat-Divisionen beschrieben werden kann. Beispiel bei 120 BPM: ein Achtel entspricht 250 ms, eine punktierte Achtel 375 ms. **Reverb** simuliert diffuse Nachhall-/Raumantworten; Pre-Delay, Early Reflections, Decay, Damping und Wet/Dry-Balance sind eigenständige Stellgrößen. Ein rhythmisches Delay kann als kontrapunktische Figur wirken; ein langer Hall kann Phrasengrenzen verwischen.

## Originalübungen
**R-01:** Mono-Pluck, Delay auf 1/8 punktiert, vier Takte 120 BPM. Stummes Audiosignal nach Note-On ist nicht identisch mit ausklingenden Effekt-Wiederholungen. Noten- und Effekt-Tails separat speichern.

**R-02:** Pad in 4/4, Reverb-Decay stark verlängern und harmonic rhythm von jedem Takt auf jeden zweiten Takt verringern. Höre, wie Nachhall und Akkordwechsel sich überschneiden; musikalische Harmoniespannung ist nicht gleich technischer Phasenauslöschung.

**R-03:** Bass in mono zentrieren, zwei hohe Gegenstimmen seitlich differenzieren; dann die Stereosumme mono abhören. Das ist eine Arbeitsheuristik, keine universelle Forderung, dass jeder Bass mono sein muss.

## DAW-/Datenmodell
`bus_id`, `pan_law`, `channel_layout`, `effect_type`, `input_bus`, `wet`, `dry`, `predelay_ms`, `decay_s`, `delay_sync_fraction`, `feedback`, `automation_points`, `tail_duration_estimate`, `mono_compatibility_review`. Ein rechts/links-Label ohne Kanalkonvention ist nicht interoperabel; Surround/Atmos und binaurale Verfahren benötigen getrennte spätere Modelle.

### Nachweise
Ableton Live 12 Audio Effect Reference und Mixer/Dynamics: https://www.ableton.com/en/manual/live-audio-effect-reference/ . Eigene Übungen; keine wissenschaftlich universellen Stereo-Presets behauptet.

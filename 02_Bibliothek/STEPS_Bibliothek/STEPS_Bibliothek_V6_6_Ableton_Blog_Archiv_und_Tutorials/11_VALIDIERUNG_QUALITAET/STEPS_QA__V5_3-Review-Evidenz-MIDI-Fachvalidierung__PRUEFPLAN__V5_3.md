> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Forschungs- und Maschinenvalidierung: zwei voneinander unabhängige Gates

## Maschinen-Gate M
M1 JSON-Schemas und obligatorische Felder; M2 eindeutige IDs; M3 Dauer und Step-Grenzen; M4 MIDI-File-Parsability; M5 Note-on/off-Paarung; M6 Velocity 1–127; M7 Tempo und Time Signature; M8 MIDI-/JSON-Onsets im exakt selben PPQ; M9 Kontext-abhängige Zahlen (Tempo/Frequenz) mit Toleranzen; M10 SHA-256-Manifest; M11 Quell-ID-Auflösung. Ein grüner Durchlauf beweist technische Konsistenz, nicht Gehör-/Stilkorrektheit.

## Fach-Gate F
F1 fachlich korrekte Tonhöhen/Schreibweisen; F2 Akkordfunktion unter gewähltem Lens; F3 Melodie-Kompatibilität; F4 Bass-/Voicing-Review; F5 hörbare Drum-Groove-Qualität; F6 kultur-/genrespezifische Einordnung mit konkreter Quelle; F7 Audioqualität/Signaltechnik; F8 Rechteprüfung; F9 didaktische Erklärbarkeit; F10 Reviewer mit Version und Datum. Bis Review bleibt V5.3 `working_reference`, niemals `validated_musicology`.

## Audio-Gate A (noch nicht ausgeführt)
A1 Pegelmatched A/B; A2 geschulte und/oder relevante Hörer; A3 Reproduktions-Setup; A4 Instrumente/Plugins und Version; A5 Audio-Hash; A6 True Peak/LUFS nur mit dafür eingerichtetem validiertem Meter; A7 Artefakte; A8 Version und Abhörbedingungen. Es werden **keine** Hör- oder Spektraltests behauptet, solange nur MIDI-/Markdown-Daten vorliegen.

## Negativkatalog
`BPM=0`, `steps_per_bar<1`, Event jenseits Taktdauer, Note 128, Velocity 0 als NOTE-ON ohne dokumentierte Semantik, ein unvollständiges Note-off-Paar, „Channel 10“ als 0-index Kanal 10 interpretiert, 7/8 mit 4/4-16tel-Länge, DAW-Oktavnamen als MIDI-Frequenz, vermeintlich originaler Song-Session-Beleg aus Fan-Remake, „-23 LUFS ist für alle Master vorgeschrieben“, geschützte Samples im Public ZIP. Die ersten Fälle sind technisch testbar; die letzten erfordern Kontext- und Rechteprüfung.

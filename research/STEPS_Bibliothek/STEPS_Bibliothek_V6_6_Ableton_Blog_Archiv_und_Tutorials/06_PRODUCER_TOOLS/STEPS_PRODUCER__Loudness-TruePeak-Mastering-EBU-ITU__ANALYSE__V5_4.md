# STEPS V5.4 – Loudness und True Peak: Messung ist nicht Geschmacksurteil

**Stand:** 2026-11-08 · **Status:** neue ausführliche Arbeitsfassung; nicht vollumfänglich begutachtet · **Urheberschaft:** eigenständiges Lehrmaterial

## Zwei externe Standards und ihre Reichweite
ITU-R BS.1770-5 beschreibt Algorithmen zur Loudness- und True-Peak-Messung (SRC54-014). EBU R 128 Version 5.0 (2023) gibt eine Broadcast-Normalisierungs-Empfehlung mit -23 LUFS an (SRC54-013). Eine daraus abgeleitete Regel „Jeder EDM-Master muss -23 LUFS haben“ wäre **falsch**: Programmmaterial, Zielplattform, Normalisierung und künstlerische Absicht unterscheiden sich. Steps darf Standards nicht mit marktorientierten Plattformtargets verwechseln.

## Glossar
`Integrated LUFS` – programmbezogene Lautheit über einen definierten Zeitraum/Algorithmus. `Short-term` und `Momentary` – andere Zeitfenster; `Loudness Range` – Variation; `True Peak` – Schätzung von Zwischensample-Peaks. `Sample peak` und `true peak` sind unterschiedliche Messgrößen. Ein Clip mit -1 dBFS Sample Peak muss nicht zwingend -1 dBTP haben.

## Eigenes QA-Szenario
Teste drei Ausgangsmaster A/B/C: A dynamisch mit niedrigem Integrated LUFS, B lauter durch Limiting, C lauter durch statischen Gain ohne Limit. Beurteile bei normalisierter Abhörlautheit, wie Transienten und Verzerrungen sich ändern. Für echte Zahlen ist eine implementierte Messung an realen Audiodateien notwendig. Diese Bibliothek **erfindet keine Werte**.

## Format- und Rechtefragen
MIDI hat keinen LUFS. MusicXML auch nicht. Erst das gerenderte Audio in einem dokumentierten Kanal-/Samplerate-/Lautheitsmesskontext ist analysierbar. Copyright/Publisher-Policy kann neben Musikrecht gelten; kein Export kommerzieller Referenzmaster in die offene Library ohne Erlaubnis.

## Freigabegate
Wenn ein Tool einen `master_loudness_target` vorschlägt, müssen `target_context` (broadcast, streaming, cinema, game etc.), `reference_standard`, `measurement_implementation`, `audio_id` und `override_by_user` vorhanden sein. Eine reine Zahl ohne Kontext ist ein Designfehler.

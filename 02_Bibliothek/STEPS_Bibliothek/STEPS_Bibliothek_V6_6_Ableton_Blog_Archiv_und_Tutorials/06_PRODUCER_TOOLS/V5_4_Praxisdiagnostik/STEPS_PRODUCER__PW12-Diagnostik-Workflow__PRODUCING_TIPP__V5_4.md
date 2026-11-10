# MIDI-Import verliert Groove · Producer-Diagnostik PW12

**Kategorie:** Diagnose, kein genreübergreifendes Rezept. **Quellenanker:** R12,R13.

## Symptom und Aufteilung der Ursachen
Tempo-Map, Clipgroove vs committe Note-On-Positionen, Tick-Resolution und Plugin-Latenz aufzeichnen.

## Konkreter Reparaturpfad
Einen Straight-Export und einen committed Swing-Export mit eindeutigem Namen liefern.

## Verifikation und akustischer Gegencheck
Roundtrip Tick-Abweichung; nicht unbemerkt doppelt grooven.

## Lessons learned für Steps
- Jede Diagnose wird als **Hypothese** gespeichert, nicht als belegte Ursache, solange keine Messung vorliegt.
- `observed`, `suspected`, `tested`, `resolved` und `hearing_reviewed` bleiben eigene Statuswerte.
- Eine MIDI-Datei beweist keine Audio-Phasenlage, Kompressorkennlinie, Filterwirkung oder gehörte Emotionalität.
- Bei Samples und Kursmaterial Herkunft, Rechte, Version und eventuelle DAW-Abhängigkeit erfassen.

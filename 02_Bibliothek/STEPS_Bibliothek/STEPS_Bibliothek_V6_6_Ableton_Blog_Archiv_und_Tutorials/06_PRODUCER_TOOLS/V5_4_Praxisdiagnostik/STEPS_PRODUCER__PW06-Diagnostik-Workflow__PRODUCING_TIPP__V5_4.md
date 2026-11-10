# Sub spielt falsche Oktave · Producer-Diagnostik PW06

**Kategorie:** Diagnose, kein genreübergreifendes Rezept. **Quellenanker:** R12.

## Symptom und Aufteilung der Ursachen
DAW-Oktavnamen, Instrument-Transpose und MIDI-Pitch im Sample/Patch unterscheiden.

## Konkreter Reparaturpfad
MIDI 27 -> Eb1 bei wissenschaftlicher Notation, Frequenz 38.89 Hz 12TET A440.

## Verifikation und akustischer Gegencheck
Note On + Audiofrequenz bei deaktiver Pitch-Modulation vergleichen.

## Lessons learned für Steps
- Jede Diagnose wird als **Hypothese** gespeichert, nicht als belegte Ursache, solange keine Messung vorliegt.
- `observed`, `suspected`, `tested`, `resolved` und `hearing_reviewed` bleiben eigene Statuswerte.
- Eine MIDI-Datei beweist keine Audio-Phasenlage, Kompressorkennlinie, Filterwirkung oder gehörte Emotionalität.
- Bei Samples und Kursmaterial Herkunft, Rechte, Version und eventuelle DAW-Abhängigkeit erfassen.

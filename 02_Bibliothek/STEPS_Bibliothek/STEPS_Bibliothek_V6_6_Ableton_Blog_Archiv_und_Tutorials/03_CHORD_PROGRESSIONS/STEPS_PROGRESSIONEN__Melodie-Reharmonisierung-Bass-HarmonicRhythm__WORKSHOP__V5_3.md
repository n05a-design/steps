> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Progressionen-Werkstatt: Melodie, Bass, Harmonic Rhythm und Reharmonisierung

## Ausgangspunkt: ein Originalmotiv
Vier 4/4-Takte in C-Dur, eine einfache Melodie mit Viertelwerten (MIDI-Notation ohne Oktavierungsfrage):

| Takt | Melodie auf Beats 1–4 | Grundharmonie | Bass |
|---|---|---|---|
| 1 | E4 – G4 – A4 – G4 | Cmaj7 | C3 |
| 2 | F4 – E4 – D4 – C4 | Fmaj7 | F2 |
| 3 | D4 – F4 – G4 – B4 | G7 | G2 |
| 4 | C5 – G4 – E4 – C4 | Cmaj7 | C3 |

Die Melodietöne sind absichtlich nicht alle Akkordtöne: A4 über Cmaj7 ist eine 13-Farbe und F4 über Fmaj7 ist der Grundton; Noten außerhalb eines Dreiklangs sind nicht automatisch Fehler.

## Fünf schrittweise Reharmonisierungsebenen
| Ebene | Harmonie (je ein Akkord/Takt, soweit nicht geteilt) | Denkweg und Caveat |
|---|---|---|
| 0 | Cmaj7 / Fmaj7 / G7 / Cmaj7 | einfache funktionale Grundlage |
| 1 | Cmaj7/E / Fmaj7/A / G7/B / Cmaj7 | stufenweise Bassfarbe; Oberstimmen müssen überprüft werden |
| 2 | Cmaj9 / Fmaj9 / G13 / Cmaj9 | Erweiterungen; im dritten Takt enthalten Melodietöne D, F, G, B kompatible Akkordtöne |
| 3 | Cmaj7 / Fm6 / G7 / Cmaj7 | Borrowed `iv`-Farbe; **F4 in Takt 2 bleibt Grundton**, E4 wirkt als chromatischer Nachbar, nicht automatisch stabiler Akkordton |
| 4 | Cmaj7 / A7(b9) → Dm7 / G7(b9) / Cmaj7 | Zwischendominante plus geteiltes Taktmaß; tatsächliche Note-Fit und Einsatzzeit prüfen |

## Timing-Grenze
Eine Substitution kann durch die Melodie **zum falschen Zeitpunkt** Spannung erzeugen. Bei Takt 2 und der geteilten A7–Dm7-Variante ist der Melodieton F4 über A7 eine ♭13-Farbe; er ist nicht automatisch Akkordton. Eine regelbasierte Engine sollte `harmonic_event_start`, `duration`, `melody_event_start`, `duration` schneiden und pro Überschneidung erklären, ob Chord Tone, Extension, Suspension, Passing Tone, Appoggiatura oder unklare Dissonanz vorliegt.

## Kontextabhängige Basslinien
`C/E–F–G–C`: E–F–G erzeugt Aufwärtszug und kann eine melodische Gegenbewegung hervorheben. `C–G/B–Am–F`: Bass C–B–A–F verschiebt die Wahrnehmung stärker als bloße Roman-Funktionen. Bei inversionsbezogenen Empfehlungen darf Steps nicht einfach die Chord Root als Bass abspeichern; die Bass- und Akkordfelder müssen getrennt vorliegen.

## Praktisches Entscheidungsverfahren
1. Melodie-Ereignisse zeitlich normalisieren; 2. lokale Tonika-/Modus-Hypothesen festhalten; 3. harmonische Kandidaten aus unterschiedlichen Mechanismen erzeugen; 4. Melody-Fit analysieren; 5. Bassführung separat; 6. Voice-leading der tatsächlichen Voicings; 7. Dissonanzen und Auflösungszeit erfassen; 8. Stil-/Genre-Grenzen; 9. Alternativen begründen; 10. Hörreview. Kein numerisches „ästhetisch am besten“ ohne definierte Benutzerziele.

## Datenvertrag
`progression_id`, `events[{start_beats,duration_beats,chord_symbol,bass_note,voicing_notes}]`, `melody_events`, `key_hypotheses`, `analyses[]`, `transforms[]`, `source_evidence[]`, `copyright`, `review_status`. `duration_beats` >0; keine Überlappungen innerhalb einer monophonen Bassstimme, außer ausdrücklich geführter Sustain-/Portamento-Verlauf.

### Nachweise
Open Music Theory Grundlagen, Mehrstimmigkeit, Akkorde: https://openmusictheory.github.io/contents ; music21 Harmony/Roman: https://music21.org/music21docs/moduleReference/moduleRoman.html . Musikbeispiele ausschließlich eigene Übungsfälle; keine Audioqualität automatisch bewiesen.

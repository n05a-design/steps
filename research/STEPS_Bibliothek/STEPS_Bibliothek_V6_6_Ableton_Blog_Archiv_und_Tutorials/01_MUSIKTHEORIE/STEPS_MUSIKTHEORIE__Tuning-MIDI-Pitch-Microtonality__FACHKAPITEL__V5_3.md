> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Stimmungssysteme, Frequenzen und MIDI-Pitch

## Begriffe und Datenebenen
Notierter Tonname, MIDI-Notennummer, Klangfrequenz, Tuning-System und Pitchbend-Information sind getrennte Repräsentationen. Ein `note_number=69` bezeichnet in der üblichen 12-TET-Referenz bei A4=440 Hz den Ton 440 Hz, allerdings nur **unter diesen expliziten Voraussetzungen**. Bei einer anderen Stimmung ist diese Identifikation nicht generell gültig. DAWs benennen Oktaven unterschiedlich; MIDI-Nummer 60 bleibt als Zahl eindeutig, selbst wenn die Oberfläche C3 oder C4 anzeigt.

Die Standardformel für gleichstufige 12-Ton-Stimmung lautet
\[f(n)=440\cdot 2^{(n-69)/12}\]
mit n als MIDI-Notennummer und explizitem Kammerton 440 Hz. Sie ist **keine** universelle Beschreibung von reiner Stimmung, historischer Temperatur, MPE oder freien mikrotonalen Tonhöhen.

| Beispiel | MIDI | 12-TET-Frequenz (ca.) | Bedeutung |
|---|---:|---:|---|
| A4 | 69 | 440,00 Hz | Referenz in diesem Modell |
| C4 | 60 | 261,63 Hz | häufig als mittleres C bezeichnet |
| E♭1 | 27 | 38,89 Hz | tiefer elektronischer Subbereich |
| C2 | 36 | 65,41 Hz | kann im GM-Drummapping dennoch Kick triggern |

## Mehrdeutige Schreibweisen
`F#4` und `Gb4` teilen in 12-TET den Frequenzwert, aber nicht in jedem Notations-/Stimmkontext die funktionsharmonische Bedeutung. Für „Deutsch“ gilt `H` = internationales B natural und `B` = internationales B-flat; die Oberflächensprache muss daher mitgespeichert werden. Die Tonart `F♯-Dur` wird theoretisch mit F♯–G♯–A♯–H–C♯–D♯–E♯ geschrieben, nicht mit F♯–G♯–B♭–H–C♯–D♯–F. Ein Parser darf gleiche Pitch Classes nicht als gleiche orthografische Bedeutung behandeln.

## Microtonalität und MPE
Microtonalität erfordert feinere Modelle als `pitch_class ∈ 0…11`. Eine Spezifikation soll notierten Grad, Ratio/Cents, Tuning-Profil, Referenzton, möglicherweise sich änderndes System und die tatsächlich ausgegebene MIDI-/Audio-Tonhöhe halten. MPE kann kanalbezogene Ausdrucksdaten ermöglichen, ist aber nicht gleichbedeutend mit beliebigen **korrekt notierten** nichtwestlichen Tonleitern. Ein Raga oder Maqam kann nicht seriös allein als zwölf gleichstufige Pitch Classes mit einem `mood`-Label repräsentiert werden.

## Konkrete Tests
1. `midi_to_hz(69,440)==440` mit Toleranz; 2. `midi_to_hz(81,440)==880`; 3. MIDI 27 ≈38,89; 4. `note_display_locale` bei gleicher Zahl unterschiedlich; 5. enharmonische Rundreise darf Schreibweise nur auf ausdrückliche Anweisung normalisieren; 6. unbekannte Stimmung muss `unknown`, nicht implizit `12-TET` ergeben; 7. Frequenz plus Notenname ohne Tuning darf nicht als exakte physikalische Identität gelten.

### Nachweise
Ableton-Live-12-Referenz zum Umgang mit Tuning-Systemen und MPE (Kapitel 12 und 15): https://www.ableton.com/de/live-manual/12/ . Quelle ist ein Herstellerhandbuch, keine kulturvergleichende Musikwissenschaft. Weiterer traditionsbezogener Fachreview offen.

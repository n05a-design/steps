# Fable-Audit · Hör- und Spielproben

Die Beispiele bereiten drei offene Benchmark-Abnahmen vor. Grundlage ist
`main` bei `38a1544bb28acde9997128da5b8b89c739ea8c97`.
Die Hördateien entstehen lokal aus eigenen Tönen und Rhythmen.

```sh
python -B scripts/render_audit_listening_examples.py /tmp/steps-fable-hoerproben
```

Den Hörenden nur die jeweilige A/B-Datei geben und die Zuordnung bis zur
Auswertung zurückhalten. Reihenfolge, Wiedergabe, Antwort und gegebenenfalls
abweichende Urteile protokollieren. Die Wellenform lässt sich reproduzieren.
Die Einschätzung der gehörten Metrik bzw. Tonika erfolgt durch Hörende.

## PAT-031 · Metrum

Beide Varianten verwenden das Glockenmuster `X.X.XX.X.X.X` über zwölf
Achteln. Der Puls liegt bei 120 punktierten Vierteln pro Minute. Jeder
Clip wiederholt die Folge viermal. Bei 480 PPQ entsprechen die
Pulsabstände 240 Ticks.

- Variante A setzt Taktanfänge bei Achtelposition 0 eines 12/8-Takts.
  Der tiefere Markierungston betont diese Position.
- Variante B betont die Positionen 0 und 6 und illustriert zwei
  6/8-Takte. Das Glockenmuster bleibt gleich.
- Aufnahme je einmal frei und einmal mit Zählen hören. Die Hörenden
  notieren die wahrgenommenen Taktanfänge und sagen, ob beide Raster
  verständlich sind. Für eine bevorzugte Lesart den musikalischen
  Verwendungszweck dokumentieren. Bei Uneinigkeit beide erhalten.

[Open Music Theory · Compound Meter and Time Signatures, Example 2](https://viva.pressbooks.pub/openmusictheory/chapter/compound-meters-and-time-signatures/)

## PROG-001 · Tonales Zentrum

Zwei dreifach wiederholte Durchläufe mit C–G–Am–F, je ein Akkord
pro 4/4-Takt bei Viertel = 100 BPM. Lautstärke, Akkordlage, Timing und
Melodierhythmus sind gleich. Die Melodien beginnen und enden auf C
(Variante A) bzw. A (Variante B). Internationale Notation.

| Akkord | Melodie A | Melodie B |
| --- | --- | --- |
| C | C5 E5 G5 E5 | A4 C5 E5 C5 |
| G | D5 B4 D5 D5 | B4 D5 B4 D5 |
| Am | C5 E5 C5 A4 | A4 C5 E5 A4 |
| F | A4 F4 G4 C5 | C5 F4 G4 A4 |

Je Variante angeben, ob C, A oder ein anderes bzw. kein eindeutiges
Zentrum gehört wird. Nach der ersten Antwort benennen, welcher Moment
oder Melodieton den Eindruck stützt. Beide Urteile mit Reihenfolge
und Begründung aufnehmen.

[Mark Richards · Tonal Ambiguity in Popular Music’s Axis Progressions, Abs. 9–11 und 29–30](https://mtosmt.org/issues/mto.17.23.3/mto.17.23.3.richards.html)

## P02 · Umkehrung und Handspanne

Rechte Hand bei Viertel = 60 BPM. Jede Lage zwei Schläge halten.
Die Noten stehen tief nach hoch. Für die enge Folge ist 1–3–5 ein Ausgangspunkt.
Komfortable Handspanne vor dem Versuch erfassen. Bei Spannung die
Lage abbrechen oder die Töne auf beide Hände verteilen.

| Folge | C-Dur in 1. Umkehrung | F-Dur in Grundstellung | Bewegung je Stimme |
| --- | --- | --- | --- |
| Eng, Fingersatz je 1–3–5 | E4 G4 C5 | F4 A4 C5 | +1, +2, 0 Halbtöne |
| Weit, Anschlag nur bei bequemer Reichweite | E4 C5 G5 | F4 C5 A5 | +1, 0, +2 Halbtöne |

Beide Folgen ergeben L1 = 3. Die enge Folge spannt 8 bzw. 7 Halbtöne
auf, die weite 15 bzw. 16. Einen geeigneten Fingersatz für die enge
Folge und einen realen Versuch über drei Wiederholungen festhalten.
Für die weite Folge genügt die Feststellung, ab welcher Lage sie für
die betreffende Person eine andere Handverteilung braucht. Beobachtungen
zu Puls, sicher erreichtem Bass und Komfort einzeln festhalten.

## Beleg aufnehmen

Für jeden Versuch Datum, Git-SHA, beteiligte Person, Dateien oder
Spielprotokoll und Beobachtungen sichern. Die Kriterien stehen in
`KB-M08-METER`, `KB-M09-LOOP-HEAR` und `KB-M12-PLAYABILITY`.
Die Übernahme der fachlichen Bewertung in den Benchmark ist in der
[Benchmark-Anleitung](../../../knowledge/benchmark/README.md#hör--spiel--und-didaktikabnahme)
beschrieben.

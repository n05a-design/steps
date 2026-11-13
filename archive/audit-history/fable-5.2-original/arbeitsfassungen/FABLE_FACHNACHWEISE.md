# Fachnachweise aus dem Fable-Audit

Stand 13.11.2026. Die Antworten sind Entwürfe für die menschliche Coach-Abnahme.
Die Fälle und Kriterien stehen im [Benchmark](../../knowledge/benchmark/cases.json).

| Fall | Antwortentwurf | Prüfbasis |
| --- | --- | --- |
| COACH-01 | Dm7 ist ii⁷, G7 ist V⁷ und Cmaj7 ist Imaj7 in C-Dur. C4 ist die Septime von Dm7 und sinkt um einen Halbton zu H3, der Terz von G7. F4 als Septime von G7 sinkt zu E4, der Terz von Cmaj7. | [Open Music Theory, ii–V–I, Key Takeaways](https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/) |
| COACH-02 | C und A sind mögliche Zentren. C–G–Am–F lässt sich als I–V–vi–IV oder III–VII–i–VI lesen. Melodie, metrisches Gewicht und Form entscheiden mit. Aus der Akkordliste allein folgt keine eindeutige gehörte Tonika. | [Open Music Theory, Singer/Songwriter und Tonal ambiguity](https://viva.pressbooks.pub/openmusictheory/chapter/4-chord-schemas/) |
| COACH-03 | Fmaj7 ist der Vierklang F–A–C–E. Über D liegen diese Töne eine kleine Terz, reine Quinte, kleine Septime und große None über dem Grundton. Beide Hände zusammen ergeben Dm9 mit Grundton. Die rechte Hand ist relativ zu D grundtonlos. | Unabhängige Terzschichtung, Kontrollfall P12 |
| COACH-04 | Swing hat keine universell vorgeschriebene Onset-Ratio. Die Schlagzeugverhältnisse in der Studie ändern sich mit dem Tempo. Auch Spielweise und Timing zwischen den Ensemblemitgliedern sind für die Interpretation relevant. | [Friberg und Sundström, 2002, Abstract](https://doi.org/10.1525/mp.2002.19.3.333) |
| COACH-05 | Deutsch H entspricht international B und Tonklasse 11. Deutsch B entspricht international B♭ beziehungsweise Bb und Tonklasse 10. Ein unmarkiertes B ist ohne Schreibkonvention mehrdeutig. | [Yale University Library, Vergleichstabelle S. 1](https://web.library.yale.edu/printpdf/cataloging/music/names-keys-french-german-italian-and-spanish) |
| COACH-06 | In zwölfstufig gleichstufiger Stimmung mit A4 = 440 Hz liegen C4 bei MIDI 60 und A4 bei 69. Aus dem Oktavverhältnis 2:1 folgt 440 × 2^((60−69)/12) ≈ 261,63 Hz. | Unabhängige Rechnung |
| COACH-07 | A natürlich Moll enthält G, A harmonisch Moll Gis als erhöhten Leitton. F4→G♯4 umfasst 68−65 = 3 Halbtöne. Die Buchstaben F und G bilden eine Sekunde, hier übermäßig. | Stufenfolge und unabhängige Intervallrechnung |
| COACH-08 | A4 ist die Terz von F, As4 die Terz von Fm und G4 die Quinte von C. MIDI 69→68→67 ergibt zweimal −1 Halbton. Das ist ein lokaler Stimmweg. Die übrigen Stimmen können verschieden geführt werden. | [Open Music Theory, Blues-Based Schemas, Minor iv](https://viva.pressbooks.pub/openmusictheory/chapter/blues-based-schemas/) |
| COACH-09 | Zwölf gleichmäßige Achtelpulse allein entscheiden die Metrumfrage nicht. Ein 12/8-Takt enthält vier Dreiergruppen. Zwei 6/8-Takte enthalten je zwei Dreiergruppen mit einem Taktstrich nach Puls 6. Akzente und Phrasierung können einen erneuten Taktbeginn auf Puls 7 stützen. | PAT-031, Zählvergleich in der Drum-Bibliothek |
| COACH-10 | Erste Aufteilung links D3, rechts F4–A4–C5–E5. Zweite Aufteilung links D3–A3, rechts F4–C5–E5. Beide enthalten D–F–A–C–E. Die Handspanne kann eine andere Lage oder gebrochene Ausführung erfordern. | Unabhängige Terzschichtung |
| COACH-11 | MusicXML 4.0 akzeptiert `<alter>0.5</alter>`. Das entspricht einem halben Halbton über dem geschriebenen Stammton. Eine ganzzahlige MIDI-Notennummer trägt diese Abweichung allein nicht. | [W3C, MusicXML 4.0, semitones](https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/semitones/) |
| COACH-12 | Rechte Hand spielt E4–G4–C5, anschließend G4–C5–E5. Bei 60 BPM bekommt jede Lage zwei Schläge. Fingersatz je nach Hand anpassen. Abnahme mit drei Wiederholungen im Puls und korrekt benanntem tiefstem Ton E bzw. G. | C-Dur-Dreiklang und Umkehrung, P02/P11 |

Für eine formale Coach-Abnahme braucht es einen dokumentierten Lauf mit Modell
und Skillrevision sowie eine fachkundige Person, die Antwort und Fundstellen
gegen die Rubrik prüft. Die Entwürfe können dafür als Vergleich dienen.

## Rhythmus und Klavierkatalog

- Die Son-Clave-Ticks 0, 720, 1440 und 2400, 2880 stimmen mit einem
  Sechzehntelraster bei 480 PPQ. Das Bossa-Übungsmuster verschiebt den letzten
  Schlag auf 3120. Stilgeschichte und Terminologie brauchen eigene Belege.
- PAT-031 erlaubt zwei metrische Lesarten für dieselbe Glockenfolge. Bei 480 PPQ
  ergeben die zwölf Achtel 2880 Ticks. Ein einzelner 12/8-Takt beginnt bei 0.
  Zwei 6/8-Takte beginnen bei 0 und 1440. Die Wahl bleibt Gegenstand einer
  Hörprobe mit unterschiedlicher metrischer Betonung.
- Bei P12 ist nur die rechte Hand relativ zu D grundtonlos. Bei P19 sind
  C♯→C→H zwei Halbtonschritte und H→A→G zwei Ganztonschritte. Beide Beispiele
  sollten mit ihren konkreten Grenzen unterrichtet werden.
- PROG-024 beschreibt die Doppeldominante D7 in C-Dur, deren Terz hier
  chromatisch zu Dm7 umgedeutet wird. Die Sekundärdominante zur zweiten Stufe
  wäre A7. Die Zuordnung des Schemas zu einer bestimmten Aufnahme braucht
  eine editionsgenaue Belegstelle.

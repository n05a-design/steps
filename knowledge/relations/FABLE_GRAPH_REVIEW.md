# Wissensgraph · Gegenproben zu den Relationen

Geprüfte Basis `38a1544bb28acde9997128da5b8b89c739ea8c97`.
Die folgenden Nachweise korrigieren Beschreibungen und Zahlen im
Forschungsgraphen. Die Kanten behalten ihre IDs, Endpunkte, Typen und den
Status `REVIEW_REQUIRED`. Quellenbelege können einen Teil der Aussage
stützen, während die Kantenrichtung und Knotenbedeutung offen bleiben.

| Kante | Gegenprobe und Geltungsbereich |
| --- | --- |
| CR-001 | 440 Hz ist eine standardisierte Referenz. Dieselbe relative Oktave kann von verschiedenen Referenzfrequenzen ausgehen. [ISO 16:1975, Abstract](https://www.iso.org/standard/3601.html) |
| CR-015 | C/E ist eine Umkehrung. C/F♯ hat einen akkordfremden Bass. Eine Pedalfunktion hängt vom musikalischen Verlauf ab. [Open Music Theory, Chord Symbols, Bass notes](https://viva.pressbooks.pub/openmusictheory/chapter/chord-symbols/) |
| CR-020 | G7 und D♭7 teilen die Tonklassen F und H/C♭. Das liefert eine lokale Stimmführungsoption für den Ersatz. [Open Music Theory, Substitutions](https://viva.pressbooks.pub/openmusictheory/chapter/substitutions/) |
| REL-021 | Der Katalog weist PAT-024 als 90 BPM und 61 % Swing aus. Die Verbindung mit PROG-021 ist ein didaktisches Beispiel. Eine Aussage zur typischen Häufigkeit oder Hörwirkung benötigt weitere Evidenz. [Drum-Katalog](../concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md) |
| REL-022 | Das P12-Beispiel F–A–C–E über D ergibt Dm9. Es belegt die erste Lage, weitere Lagen der Folge brauchen eigene Griffe. [Piano-Katalog](../concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md) |
| REL-024 | 240 × 0,64 = 153,6, gerundet 154. Gerader Onset 120. 34 × 60000/(132 × 480) ≈ 32,20 ms. [Benchmark KB-PAT-026-TICKS](../benchmark/cases.json) |
| REL-027 | Vier ausgewählte Familien mit je sieben unterschiedlichen Rotationen. Der Tonvorrat bestimmt, welche Terzschichtungen auf seinen Stufen möglich sind. [Oliver Prehn, The Modes, S. 1–2](https://newjazz.dk/Compendiums/Major_Melmi_Harmmi_HarmMa_Modes.pdf) |
| REL-029 | Die Paarung von Progression und Groove ist eine STEPS-Übung. Die Werkpartitur belegt nur ihre eigene Fassung. [Latin-Katalog, PROG-024](../concepts/styles/GENRE_RESEARCH_LATIN.md) |
| REL-030 | Die Paarung von P14 und PROG-024 ist eine vorgeschlagene Übung. [Piano-Katalog, P14](../concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md) |
| REL-031 | Das beschriebene Tick-Raster gehört zum konkreten Cross-Stick-Modell. [Latin-Katalog, Bossa-Nova-Übungsmuster](../concepts/styles/GENRE_RESEARCH_LATIN.md) |

Die Kataloge und Domänen lösen beide Endpunkte von 36 der 97 Kanten auf.
61 Kanten verwenden mindestens eine der 86 noch nicht kanonisch
definierten IDs. Die Zuordnung dieser IDs braucht die ursprüngliche
Ontologie oder eine dokumentierte Migration. Die zehn Gegenproben
liefern keine Freigabe für automatische Empfehlungen.

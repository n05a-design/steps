# Stichproben in den zwölf Wissensdomänen

Die Beobachtungen betreffen die benannten Passagen. Die jeweilige
Quellenedition, der fachliche Teilbefund und die Veröffentlichungseignung
werden getrennt bewertet. Automatisierte Fälle und offene Abnahmen stehen
in [cases.json](cases.json).

| Domäne | Gelesene Passage | Fachlicher Befund und Grenze |
|---|---|---|
| M01 Grundlagen | [CLAIM-001](../sources/MUSIC_SOURCE_CLAIM_REGISTER.csv) | C4 bei 12-TET und A4=440 liegt rechnerisch bei 261,626 Hz. Die konkrete Müller-Seite bleibt offen. |
| M02 Notation | [Fachmodell, T01–T03](../../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md#minimale-fachliche-invarianten) und [Pilotkonvention](PILOT_ABNAHME.md#pilot-notation-001) | Die ausdrücklich bezeichneten Konventionen und gleichen MIDI-Werte enharmonischer Töne stimmen. Die Forderung, unmarkiertes B abzuweisen, steht im Fachmodell als Zielanforderung. [Yale University Library, S. 1](https://web.library.yale.edu/printpdf/cataloging/music/names-keys-french-german-italian-and-spanish) |
| M03 Skalen | [CLAIM-016](../sources/MUSIC_SOURCE_CLAIM_REGISTER.csv) | Vier ausgewählte Familien liefern je sieben Rotationen. Das begründet keine vollständige Taxonomie aller heptatonischen Skalen. F→G♯ in A harmonisch Moll umfasst drei Halbtöne. Die genannte Quellenseite bleibt offen. |
| M04 Akkorde | [Fachmodell, T04–T05](../../docs/engineering/MUSIC_DOMAIN_AND_MIDI.md#minimale-fachliche-invarianten) | Dursept, Dominantsept und Mollsept sind anhand der Terz und Septime unterscheidbar. Die produktive Prüfung verwendet literale Intervalle. |
| M05 Harmonik | [Pilottext PROG-003](PILOT_ABNAHME.md#prog-003-harmony) | Dm7–G7–Cmaj7 passt zum genannten Jazz-Schema in C-Dur. Diese Stufenanalyse setzt C als Tonika voraus. [Open Music Theory, ii–V–I](https://viva.pressbooks.pub/openmusictheorycopy/chapter/ii-v-i/) |
| M06 Progressionen und Stimmführung | [PROG-008 und PROG-016](../concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md) | Die falschen Septimen an fünf Blues-Positionen und die drei fehlenden Maj7-Zielakkorde bei PROG-016 wurden mit [Commit 792b2dd](https://github.com/n05a-design/steps/commit/792b2dd0ed46ab4e189e183f3134a9aeea629702) korrigiert. Am 12. November 2026 auf `b0abd41` bestätigt. Für PROG-008 bestehen fünf Positionsfälle und ein Kontrollfall. [Open Music Theory, Blues Harmony](https://viva.pressbooks.pub/openmusictheory/chapter/blues-harmony/) |
| M07 Rhythmik | [CLAIM-034 und CLAIM-036](../sources/MUSIC_SOURCE_CLAIM_REGISTER.csv) | Die Clave-Ticks stimmen im angegebenen Raster. Bei CLAIM-034 wurden die falsche JASA-Fundstelle und die pauschale Tempo-Regel beanstandet. Die korrigierte Forschungsnotiz beschreibt den beobachteten Trend aus vier Aufnahmen und verweist auf den Verlagsabstract. Feste BPM-Zuordnungen sind damit nicht belegt. [Friberg und Sundström, Music Perception 19(3), 333–349](https://doi.org/10.1525/mp.2002.19.3.333) |
| M08 Drums | [PAT-031](../concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md#pat-031--offene-taktgrenze) | Zwölf notierte Pulspositionen legen die Taktgrenze nicht fest. Der Übergang zwischen 6/8 und dem beschriebenen 12/8-Raster bleibt für eine spielbare Vorlage offen. |
| M09 Stil | [Pilottext PROG-001](PILOT_ABNAHME.md#prog-001-tonal-center) | Relative Dur- und Moll-Lesart sind musikalisch plausibel. Die tatsächliche Wahrnehmung setzt eine konkrete Darbietung voraus. [Open Music Theory, Four-Chord Schemas, Example 4](https://viva.pressbooks.pub/openmusictheorycopy/chapter/4-chord-schemas/) |
| M10 Klavier | [P12 und P19](../concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md) | Fmaj7 ist ein Vierklang. D darunter ergibt Dm9 mit Grundton. Die Bassfolge in P19 enthält auch Ganztonschritte. |
| M11 Datenmodelle | [CLAIM-011](../sources/MUSIC_SOURCE_CLAIM_REGISTER.csv) | MusicXML erlaubt Dezimalwerte wie 0,5 und kennt für den Typ keine Begrenzung auf −2 bis +2. Der behauptete Wertebereich ist falsch. [W3C, MusicXML 4.0](https://www.w3.org/2021/06/musicxml40/musicxml-reference/data-types/semitones/) |
| M12 Didaktik | [P02](../concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md) und [Didaktische Prüfung](../research/07_DIDAKTISCHE_PRUEFUNG.md) | Kleine L1-Distanz belegt weder Handspanne noch brauchbaren Fingersatz oder Lernerfolg. Für den spielpraktischen Nachweis fehlen Handposition, Tempo und Spielprobe. |

## Historischer Harmony Coach

Die hinterlegten Beispiele in `references/harmonic-analysis.md` und
`references/chord-progressions.md` enthalten plausible Jazz- und Pop-Analysen.
Das eigene `references/sources.md` führt weiterhin einen Buchplatzhalter.
Zwölf separate Fälle in [cases.json](cases.json) prüfen deshalb neben
Pflichtaussagen auch Alternativen, Kontextgrenzen und Quellen. Der Ergebnislauf
weist sie als ausstehend aus, solange keine tatsächlichen Antworten und
nachvollziehbare Bewertungen vorliegen.

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

## Abgleich historischer Endpunkt-IDs

Die Original-IDs bleiben in den Kanten und in der Baseline erhalten.
Für `PROG_024` und `PROG_025` liegen übereinstimmende
Bezeichnungen in den katalogisierten Übungen und den historischen
Kantenbeschreibungen vor. Die Abdeckungsprüfung kann diese beiden
Verweise über die dokumentierten Aliasse auflösen. 84 Endpunkt-IDs
bleiben offen, darunter die fachlich abweichende Zuordnung in REL-020.

| Historische ID | Katalog-ID | Begründung |
| --- | --- | --- |
| PROG_024 | PROG-024 | CDR-011/012 nennen die Doppeldominante und den Wechsel der Terz im Latin-Übungsschema. [Latin-Katalog](../concepts/styles/GENRE_RESEARCH_LATIN.md) |
| PROG_025 | PROG-025 | CDR-013/014 nennen den zyklischen Mollvamp und seine mögliche Montuno-Begleitung. [Latin-Katalog](../concepts/styles/GENRE_RESEARCH_LATIN.md) |

REL-020 nennt `ERR-026` als Ziel für eine Umkehrungsübung. Im
[Fehlerregister](../research/MUSICAL_ERROR_REGISTER.csv) bezeichnet
ERR-026 eine falsche L1-Distanz. P11 und der Fehlereintrag können
eingesehen werden. Die behauptete fachliche Beziehung bleibt offen.

Die zusätzlichen Gegenproben CR-002, CR-004, CR-024, CR-032 und REL-011
begrenzen historische Aussagen auf die jeweiligen Modelle und Übungen.
Für die Unterscheidung von Puls und Taktgruppierung dient
[Open Music Theory, Compound Meter and Time Signatures](https://viva.pressbooks.pub/openmusictheory/chapter/compound-meters-and-time-signatures/).
Für die Stimmungs- und Rhythmusmodelle gelten die dokumentierten
Referenzfrequenzen, Taktarten und Beispielgrenzen.

## Quellenbelegte Formatknoten

Das [Knotenregister](FORMAT_NODE_EVIDENCE.csv) definiert die vier
Endpunkte von CDR-020 und CDR-022. Bei CDR-020 stammen Kanal 10 und
die Zuordnung der 47 Klänge zur MIDI-Notennummer jeweils aus Tabelle 3,
Druckseite 6. [The MIDI Association, General MIDI System Level 1](https://drive.google.com/file/d/1TTM2HI2JAp_XiTJYEJ8gPNvuJpIjJiTP/view)

Bei CDR-022 bewahren `step`, das optionale `alter` und `octave` die
geschriebene Tonhöhe. Die Kombinationen C, +1, 4 und D, −1, 4
sind getrennt darstellbar. Im gleichstufigen Zwölftonsystem
entsprechen beide der MIDI-Notennummer 61. [W3C, MusicXML 4.0, pitch](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/)

Nach Auflösung der zwei historischen Aliasse und der vier Formatknoten
bleiben 80 eindeutige Endpunkt-IDs offen. Die Abdeckungsprüfung führt
die Quellen der aufgelösten Endpunkte auf. Die Relationseinträge
bleiben zur fachlichen Prüfung ihrer Richtung und Bedeutung offen.

## Fortsetzung vom 14.11.2026

Sechs zusätzliche Knoten zu melodischen Mollmodi und Drop-2 haben
konkrete Fundstellen. Damit bleiben 74 eindeutige Endpunkt-IDs offen.
Die vier neuen Kantenproben sind begrenzte Nachweise. CDR-010 bleibt
wegen der unbestimmten Polychord-Zuordnung beanstandet: Ein bestandener
Test der Gegenprobe zählt nicht als Bestätigung der ursprünglichen Kante.
[Einzelnachweise und offene Knoten](../../docs/audit/fable-5.2/GRAPH_NACHWEISE_2026-11-14.md).

## Weiterführung nach dem Merge von PR #52

CDR-010 ist technisch als Zweidreiklang geklärt: C-Dur plus D-Dur ergibt
die Sammlung C6 plus D und F♯, ohne H. `GRAPH_CORRECTIONS.json` hält den
konkreten Korrekturvorschlag ohne Produktionsfreigabe fest. Die alte
Graphzuordnung bleibt FAIL und unverändert dokumentiert.
25 der zuvor 74 Restknoten sind begrenzt zugeordnet; 49 Definitionen
bleiben offen. Die Graphmatrix nennt 14 bestätigte Stichproben, einen
beanstandeten und 82 fachlich offene Einträge; keine vollständige Abnahme.
[Korrektur und vollständige Bearbeitungsliste](../../docs/audit/fable-5.2/GRAPH_KLAERUNG_CDR010_2026-11-14.md).

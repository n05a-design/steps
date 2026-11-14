# Graphfortsetzung · CDR-010 und sämtliche 74 Restknoten

Geprüfte Basis: `19f3fee85a998fc5127d0f3e5dcc8e32694aa7ef`.
[PR #52](https://github.com/n05a-design/steps/pull/52) wurde von
`timvontrostorff` freigegeben und am 14.11.2026 um 00:20 Uhr
Europe/Berlin gemergt. Diese Fortsetzung setzt auf dem Merge auf.

## CDR-010: technische Korrektur eindeutig festgelegt

Der ursprüngliche Zweidreiklang ist in CLAIM-022 und im historischen
Solltext von REF-0016 als D-Dur über C-Dur beschrieben. Das ist ein
Projektbeispiel, keine neu behauptete Prüfung der Persichetti-Buchseite.
Die [Akkordsymbolreferenz](https://viva.pressbooks.pub/openmusictheory/chapter/chord-symbols/)
unterscheidet Slashbass und Akkorderweiterungen einschließlich der Septime.

| Konstruktion | Tonklassen mit C = 0 |
| --- | --- |
| C-Dur plus D-Dur | 0, 2, 4, 6, 7, 9 |
| C6 plus D und F♯ | 0, 2, 4, 6, 7, 9 |
| Vollständiges Cmaj13(#11) | 0, 2, 4, 6, 7, 9, 11 |

Die korrekte explizite Sammlung heißt im neuen Knotenregister
`C6_9_SHARP11_COLLECTION`. Der lesbare Bezeichnungsvorschlag
`C6/9(#11)` impliziert keine Septime. Der bestehende Parser unterstützt
diese Schreibweise nicht direkt; die Rechnung verwendet ausdrücklich
C6 plus die geschriebenen Töne D und F♯. Keine Parsererweiterung wurde vorgenommen.

[GRAPH_CORRECTIONS.json](../../../knowledge/relations/GRAPH_CORRECTIONS.json)
bindet den Vorschlag an die exakten historischen Endpunkte und den Typ
von CDR-010. Er schlägt die präzise Beziehung `HAS_PITCH_CLASS_COLLECTION`
zum neuen Sammlungsknoten vor. Der neue Beziehungstyp gehört zum
Korrekturvorschlag und ist keine zusätzliche aktive Kante des alten Registers.
Die ursprüngliche Kante bleibt unverändert und als FAIL sichtbar.
Damit werden Identitätssperre und historische Fehlerdokumentation erhalten.

Der Vorschlag bleibt `REVIEW_REQUIRED`, `production_use_allowed` ist
`false`. Der [Validator](../../../scripts/graph_corrections.py) lehnt
abweichende historische Endpunkte, vorweggenommene Freigaben, unbekannte
Zielknoten und ungültige Tonklassensammlungen ab. Der Benchmark prüft
zusätzlich die konkrete Ziel-ID und die exakte musikalische Gleichheit.
Regressionstests setzen das alte Ziel oder die fehlende Septime wieder ein
und erwarten FAIL. Eine technische Korrektur ist damit bestimmt;
eine unabhängige Fachabnahme oder Produktionsfreigabe ist nicht erteilt.

## Alle bisherigen 74 Restknoten bearbeitet

Die [Bearbeitungsliste](GRAPH_KNOTENBEARBEITUNG_2026-11-14.csv) führt
alle 74 IDs der vorherigen Restliste einzeln mit aktuellem Definitionsstand,
Belegart, fehlendem Nachweis und nächstem Schritt auf. **25 dieser IDs
sind jetzt einer begrenzten Definition zugeordnet; 49 bleiben offen.**
Hinzu kommt der neue, ausdrücklich benannte Korrekturknoten für CDR-010.
Es gibt keine stillschweigende Umbenennung historischer IDs.

Die 25 Zuordnungen verteilen sich auf drei Belegarten:

- **7 SOURCE_PAGE:** Definitionen unmittelbar aus einer benannten
  Originalseite, etwa deutsches H/B, mittleres C und MIDI 60 sowie
  die begrenzte Tempoabhängigkeit im Friberg/Sundström-Abstract.
- **9 COMPUTED_MODEL:** ausdrücklich begrenzte Modellableitungen,
  unter anderem Modulo 12, vier Familien mit 28 Rotationen,
  Tick-Rundungen und die vollständige theoretische maj13(#11)-Sammlung.
- **9 PROJECT_EXAMPLE:** Definitionen konkreter STEPS-Beispiele,
  unter anderem die A/B-Lagen aus CLAIM-021, der Son-Clave-Modellfall
  aus CLAIM-036, PROG-024/025, ERR-026 und der historische Zweidreiklang.

Projektbeispiele bestätigen weder eine externe Buchseite noch eine
universelle Genre-, Voicing- oder Lehrnorm. Die beiden Zahlen-IDs
`3_5_7_9_STACK` und `7_9_3_5_STACK` sowie `ERR-026` bleiben erhalten;
die Quellenvalidierung akzeptiert diese historischen Formen jetzt ausdrücklich.

## Originalquellen und Zugriffsgrenzen

| Gegenstand | Gelesene Originalfundstelle und Grenze |
| --- | --- |
| Deutsches H/B | [John Paul Ito, Notes on Transposition](https://www.andrew.cmu.edu/user/johnito/music_theory/transp/Transposition.pdf), PDF-Seite 4, Reading Note Names in Other Languages. Tonklassen werden zusätzlich im expliziten STEPS-Modell berechnet. |
| Mittleres C | [W3C, MusicXML octave](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/octave/) nennt Oktave 4; [Ithaca, MIDI Basics](https://musictech.ithaca.edu/MusicTech/pdf/MIDIChapter.pdf), PDF-Seite 14, nennt MIDI 60. Die DAW-Oktavbeschriftung bleibt konventionsabhängig. |
| Vier Skalenfamilien | [Oliver Prehn, The Modes](https://www.newjazz.dk/Compendiums/Major_Melmi_Harmmi_HarmMa_Modes.pdf), eine PDF-Seite. Die 28 Rotationen wurden selbst gerechnet; keine Vollständigkeitsbehauptung für sämtliche heptatonischen Skalen. |
| Tempoabhängiger Swing | [Friberg und Sundström, Originalabstract](https://doi.org/10.1525/mp.2002.19.3.333). Keine universelle Zerfallsformel, kein neuer Volltextnachweis und keine individuelle 57-Prozent-Zuschreibung. |
| Rootless A/B | Die konkreten Noten stammen aus CLAIM-021. Die historische Levine-Seite wurde nicht neu geprüft; ein zusätzlich gefundener Lehrer-PDF-Link lieferte 404. A/B wird daher nur als STEPS-Beispieldefinition geführt. |
| Son-Clave | Das Rechenraster ist aus CLAIM-036 reproduziert. Der direkte Abruf der dortigen Columbia-Originalquelle wurde durch Zugriffsschutz abgewiesen. Keine erneute Originalseitenabnahme behauptet. |

## Die verbleibenden 49 Definitionen

Die [neue Restliste](GRAPH_RESTKNOTEN_2026-11-14.csv) ist gegen die
tatsächlichen Endpunkte des Registers getestet. Sie enthält:

| Gruppe | Anzahl | Fehlender Nachweis |
| --- | ---: | --- |
| Historische Mxx-xx-IDs | 41 | Definierender Originaltext oder versionierte Originalzuordnung. Die aktive Ablage und die erreichbare lokale Git-Pfadliste enthalten Verweise auf MUSIC_KNOWLEDGE_ONTOLOGY.md, aber keinen lokalisierten definierenden Text. Kantenbeschreibungen ersetzen ihn nicht. |
| MODAL_SHIFT_TO_II7 | 1 | Die historische Großschreibung II7 kollidiert mit ii7/Dm7 in PROG-024. Beabsichtigte Bedeutung und Migration festlegen. |
| PIANO_MONTUNO_GUAJEO | 1 | Konkrete Tonhöhen-/Rhythmusdefinition. Das zitierte Rhythmusbeispiel legt die separate STEPS-Harmonie nicht fest. |
| Bossa-Herkunftspaar | 2 | Historische Primärbelege und genaue Begleitfigur für die behauptete Tamborim-/Surdo-Synthese. Rhythmische Ähnlichkeit belegt keine Entstehungsgeschichte. |
| Surdo-/Akzentpaar | 2 | Abgegrenzter Samba-/Aufführungskontext und Primärbeleg oder dokumentierte praktische Prüfung für die Akzentnorm. |
| Bass-/Höranker-Paar | 2 | Operationalisierte Höraufgabe, Zielgruppe und externe Kriterienbewertung für die didaktische Empfehlung. |

Auch eine zugeordnete Definition ist keine Fachabnahme der betreffenden
Kante. Die Bearbeitungsliste markiert sämtliche Fachabnahmen als ausstehend.

## Technischer Prüfstand und offene Freigaben

Lokal unter Windows/Python 3.14.7: **174 Kerntests und 36 Skilltests
bestanden**. Referenzintegrität, Golden-Spiegel, API-Abgleich, Struktur,
Pilot-Abnahmeliste und generiertes Lernmaterial sind geprüft. Die
aktualisierte Matrix besteht `--check` einschließlich aller vorhandenen
fachlichen und formalen Befunde.
Die Pfadprüfung von 785 internen Dateiverweisen in 137 aktiven README-
und betroffenen Markdown-Dateien meldet keine fehlenden Zielpfade.
Anker, Archivvollständigkeit und externe Erreichbarkeit sind davon ausgenommen.

Der Benchmark umfasst jetzt 95 Fälle: **68 PASS, 0 FAIL, 27 PENDING**.
Zwölf neue Prüfungen sind hinzugekommen; keine offene Fachabnahme wurde
geschlossen. Der erwartete Exit 1 wegen offener Pflichtfälle bleibt erhalten.

Die Graphmatrix führt **14 bestätigte Stichproben, 1 beanstandete
Stichprobe und 82 fachlich offene Kanten**. Keine Kante ist vollständig
fachlich abgenommen. CDR-010 bleibt historisch FAIL; die bestandene
Prüfung seines Korrekturvorschlags färbt die alte Aussage nicht grün.
Alle 97 Originalkanten behalten `REVIEW_REQUIRED`.

```sh
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/audit_knowledge_coverage.py --check --details coverage.csv
python -B scripts/verify_reference_integrity.py
```

Ein Regressionstest vergleicht aktuelle Graphendpunkte, beide Arbeitslisten
und die offene manuelle Benchmarkaufgabe miteinander. Weitere negative
Prüfungen verändern die deutsche Notenkonvention, eine Skalenfamilie,
einen Rootless-Grundton, den Swinganteil und die Clave-Onsets.

Die CSS-Herkunftsergebnisse aus PR #52 werden nicht verändert.
**Rechte am vollständigen CSS-Bundle, dauerhafte Archivzuordnung sowie
Hör-, Spiel-, Coach- und sonstige fehlende Fachabnahmen bleiben offen.**
Nächste Schritte sind das menschliche Review des konkreten CDR-010-
Vorschlags und die Beschaffung der Originalontologie für die 41 Mxx-xx-IDs.

# Graphnachweise · Modi, Drop-2 und Polychord-Gegenprobe

Ausgangsstand: `9c7b8eb3fabdf09e41f26d589a892c25bc051f87` nach dem
freigegebenen Merge von PR #51. Die Fortsetzung ergänzt Belege und
automatisierte Gegenprüfungen. Die 97 historischen Kanten behalten ihre
IDs, Endpunkte, Beschreibungen und `REVIEW_REQUIRED`.

## Sechs zusätzliche Knotendefinitionen

Das [musikalische Knotenregister](../../../knowledge/relations/MUSIC_NODE_EVIDENCE.csv)
ergänzt die vier bereits belegten Formatknoten.

| Knotenpaar | Begrenzte Definition und Fundstelle |
| --- | --- |
| ALTERED_SCALE / MELODIC_MINOR_MODE_7 | Alterierte Skala und siebte Rotation des aufsteigenden melodischen Moll. [Oliver Prehn, The Modes](https://www.newjazz.dk/Compendiums/Major_Melmi_Harmmi_HarmMa_Modes.pdf), PDF-Seite 1, Zeilen Ascending mel. minor und Altered / Super Locrian. |
| LYDIAN_DOMINANT / MELODIC_MINOR_MODE_4 | Lydisch dominant und vierte Rotation desselben Ausgangsmusters. Dieselbe PDF-Seite, Zeile Lydian dominant. |
| DROP_2_VOICING / SECOND_VOICE_LOWERED_OCTAVE | Zweithöchste Stimme einer vierstimmigen engen Lage eine Oktave abwärts. [John Thomas / Berklee Online](https://online.berklee.edu/takenote/voice-leading-for-guitar/), Drop-2 Voicings und Abbildung 18. |

Die Rotationszuordnung ist eine eigene Gegenrechnung gegen Prehns
notierte Intervallfolgen. Sie ist keine Behauptung, dass die Reihenfolge
der PDF-Tabelle selbst die Modusnummerierung darstellt. Der aktuell
abgerufene PDF-Stand hat eine Seite; ältere Verweise auf S. 1–2 sind
keine neue Seitenprüfung. Für Drop-2 gilt die enge vierstimmige
Ausgangslage; Spielbarkeit, Fingersatz und Hörwirkung bleiben offen.

Nach diesen Ergänzungen bleiben **74 eindeutige Endpunkt-IDs** ohne
kanonische Definition. Die [vollständige Liste](GRAPH_OFFENE_KNOTEN_2026-11-14.csv)
ordnet jede offene ID den betroffenen Kanten zu. IDs werden nicht allein
aufgrund ihres Namens auf andere Begriffe abgebildet.

## Vier konkrete Kantenproben

[RELATION_EVIDENCE.csv](../../../knowledge/relations/RELATION_EVIDENCE.csv)
enthält Quellen-URL, Locator, gegebenenfalls Claim-ID, Prüfumfang und
Grenze je Kante. Die Validierung lehnt doppelte/unbekannte Kanten,
fehlende Grenzen, unbekannte Claims und nicht vorgesehene Freigabestatus ab.

| Kante / Benchmark | Rechnerisches Ergebnis | Bedeutung für den Graphen |
| --- | --- | --- |
| CDR-005 / KB-GRAPH-CDR-005 | Rotation 7 ergibt 1–2–1–2–2–2–2 Halbtöne. | Quellenbelegte Stichprobe, keine vollständige Fachabnahme. |
| CDR-006 / KB-GRAPH-CDR-006 | Rotation 4 ergibt 2–2–2–1–2–1–2 Halbtöne. | Quellenbelegte Stichprobe, keine vollständige Fachabnahme. |
| CDR-009 / KB-GRAPH-CDR-009 | C4–E4–G4–B4 → G3–C4–E4–B4; MIDI 60/64/67/71 → 55/60/64/71. | Die zweithöchste Stimme wird gesenkt; keine Spielabnahme. |
| CDR-010 / KB-GRAPH-CDR-010-COUNTEREXAMPLE | Der Test bestätigt die unten beschriebene Nichtidentität. | Gegenprobe PASS, ursprüngliche Zuordnung in der Matrix FAIL. |

## CDR-010 bleibt beanstandet

Die historische Kante verbindet `POLYCHORD_D_OVER_C` mit
`C_MAJ13_SHARP11` über den unbestimmten Typ `EXPRESSES`. Der bereits
korrigierte CLAIM-022 unterscheidet zwei Dreiklänge vom Slashbass.
Die [Originalreferenz zu Akkordsymbolen](https://viva.pressbooks.pub/openmusictheory/chapter/chord-symbols/)
trennt Bassangaben und Erweiterungen einschließlich ihrer Septime.
Der eigene Tonmengenvergleich ergibt in 12-TET:

| Lesart | Tonklassen mit C = 0 |
| --- | --- |
| D-Dur-Dreiklang über C-Dur-Dreiklang | 0, 2, 4, 6, 7, 9 |
| Slashbass D/C | 0, 2, 6, 9 |
| Vollständiges theoretisches Cmaj13(#11) | 0, 2, 4, 6, 7, 9, 11 |

Den zwei Dreiklängen fehlt H, Tonklasse 11. Eine mögliche kontextuelle
Voicing-Deutung mit Auslassungen ist damit nicht ausgeschlossen; sie
ist in der Kante aber nicht definiert. Eine unqualifizierte Gleichsetzung
als vollständige Tonmengen ist nicht belegt. Knoteninterpretation,
Auslassungen und Kantenbedeutung müssen geklärt oder versioniert korrigiert
werden. Es wird keine unabhängige Fachfreigabe behauptet.

Der Parser unterstützt `Cmaj13(#11)` nicht als direktes Symbol. Die
Gegenprobe bildet die theoretische Sollmenge ausdrücklich aus Cmaj7
und den geschriebenen Erweiterungen D, F♯ und A. Eine neue Parserfähigkeit
wird dadurch nicht behauptet.

## Prüfergebnis und Reproduktion

Die lokale Suite besteht **169 Kerntests und 36 Skilltests** unter
Windows/Python 3.14.7. Der Benchmark hat jetzt 83 Fälle:
**56 PASS, 0 FAIL, 27 PENDING**. Vier zusätzliche bestandene Prüfungen
sind hinzugekommen; keine der 27 offenen Abnahmen wurde geschlossen.

Die Graphzeile der Matrix lautet dagegen: **3 bestätigte Stichproben,
1 beanstandete Stichprobe, 93 fachlich offene Einträge, 0 vollständig
fachlich abgenommene Kanten**. Alle 97 Kanten haben weiterhin formalen
Klärungsbedarf. Diese beiden Zählungen messen unterschiedliche Aussagen.

```sh
python -B -m unittest tests.test_knowledge_benchmark tests.test_css_provenance -v
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/audit_knowledge_coverage.py --check --details coverage.csv
```

Regressionstests verändern Kantenendpunkte, Modusnummer und Drop-2-
Ausgangslage. Ein separater Test stellt sicher, dass eine bestandene
Gegenprobe den beanstandeten Graphclaim nicht grün färbt.
Die Prüfung von 780 internen Dateiverweisen in 138 aktiven README- und
betroffenen Markdown-Dateien fand keine fehlenden Zielpfade. Anker,
Archiv-Vollständigkeit und externe Erreichbarkeit sind davon ausgenommen.
Nächster fachlicher Schritt: die historische Bedeutung von CDR-010
einschließlich erlaubter Auslassungen klären und die verbleibenden
Knotendefinitionen mit Originalfundstellen zuordnen.

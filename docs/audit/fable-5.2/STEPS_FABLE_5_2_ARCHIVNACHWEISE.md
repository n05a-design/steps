# Fable-Audit · Archivnachweise für CSS und MIDI

Geprüfter Ausgangsstand `01d718b9825e6570350376ccb79f09ee736e2a0b`.
Die technische Prüfung bezieht sich auf die konkreten Git-Objekte und
die im historischen Dateiregister eingetragenen Vergleichswerte.

## F00412, F00571, F00704, F00768, F00937 und F01002

Die sechs CSS-Pfade in den Git-Ständen `b42a990`, `a14c3f3`,
`22f3f5f` und `01d718b` führen jeweils auf dieselben 63.109 Bytes.
Der SHA-256 lautet
`34f603614eae19caed79c0c752d7cc6a823707bc66c2fad4c72446dffea485fc`.
In den lokalen Checkout-Kopien fand sich außerdem die 64.902 Byte große
CRLF-Fassung mit SHA-256
`0a89d0e334f0c764a19383396e928ae7460d125a26b055943f166918fd8fbbec`.
Sie ergibt sich auch bei der Umwandlung der Git-Version von LF in CRLF.

Der historische Registerwert
`32289d8747feddbc21cccedc6522f0f1ab2b18bf2a0c5d9a65356f8fdc9f5f29`
bei 63.332 Bytes blieb in diesen Beständen ohne Treffer. Die abweichenden
Dateien sind eindeutig identifiziert. Die Registerfassung und ihre
Herkunft bleiben offen.

## PPR-MIDI-01 bis PPR-MIDI-04

Das [MIDI-Inventar](PPR_MIDI_ARCHIVINVENTAR.csv) nennt Pfad, Git-SHA,
Größe, SHA-256, SMF-Format, Auflösung, Tempo, Taktart und Dauer.
Alle 36 MIDI-Pfade (33 verschiedene SHA-256-Werte) wurden aus
`b42a990681ce5fd12c7756fb2ada962e01474521` gelesen und mit Mido 1.3.3
geparst. Die Prüfung zählt Note-On und Note-Off pro Spur, Kanal und Ton.
Ein Note-On mit Velocity null gilt als Note-Off. Es gab keine
ungepaarten Notenereignisse. Die vier README-Fingerabdrücke stehen in
den [Fachnachweisen](../../../research/gaps/FABLE_FACHNACHWEISE.md#historische-dateizuordnung).
[The MIDI Association, Standard MIDI Files](https://midi.org/standard-midi-files)

| Paket | MIDI-Pfade | Unterschiedliche SHA-256 | SMF / PPQ | Zeit pro Viertel |
| --- | ---: | ---: | --- | ---: |
| PPR-MIDI-01 · Boom-Bap | 18 | 15 | 0 / 480 | 666.667 µs |
| PPR-MIDI-02 · UK Garage | 10 | 10 | 0 / 480 | 454.545 µs |
| PPR-MIDI-03 · Techno | 5 | 5 | 0 / 480 | 461.538 µs |
| PPR-MIDI-04 · 174-BPM-Übung | 3 | 3 | 1 / 960 | 344.828 µs |

Alle Dateien enthalten 4/4. Die geraden und geswingten
Drums-Main-Dateien der ersten beiden Pakete zeigen unterschiedliche
Timingvarianten. Bezugspunkt ist der zweite Sechzehntel-Onset eines
240-Tick-Paares. Die Zahl bezeichnet seine Position innerhalb des Paars.

| Beispiel | Gerade | Archivdatei mit Swing | Offset im Archiv | Rechnerischer Zielwert |
| --- | ---: | ---: | ---: | --- |
| Boom-Bap | 120 | 145 | +25 Ticks, 34,72 ms bei 90 BPM | 61 % → 146, +26 Ticks |
| UK Garage | 120 | 155 | +35 Ticks, 33,14 ms bei 132 BPM | 64 % → 154, +34 Ticks |

Bei Techno liegt der wiederkehrende Side-Stick auf Kanal 10 bei
einem Abstand von 360 Ticks, entsprechend drei Sechzehnteln.
Im 174-BPM-Paket enthält die Sub-Spur Ton 27 (E♭1, rund 38,89 Hz bei
A4 = 440 Hz). Die Abstände von 480 Ticks entsprechen bei 960 PPQ
einem Achtel. Der 14-Takt-Build endet bei 53.760 Ticks.

Die historischen Registerfelder haben Platzhalter statt Lieferhashes.
Herausgeber und Rechtebelege ließen sich den vier Paketen nicht
eindeutig zuordnen. Das Inventar dokumentiert Git-Funde. Eine
Originalzuordnung oder Weiterverwendung in der App erfordert einen
separaten Provenienz- und Rechtebeleg.

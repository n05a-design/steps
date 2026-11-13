# Fachnachweise aus dem Fable-Audit

Stand 13.11.2026. Geprüfter Ausgangscommit
`7fde80efcb09a99f74669aac128dae84a3e63843`. Die Belege ergänzen die
Maßnahmen M6 und M9. Die Antworten sind Entwürfe für die menschliche
Coach-Abnahme. Fälle und Kriterien stehen im
[Benchmark](../../knowledge/benchmark/cases.json).

## Entwürfe für die Coach-Abnahme

| Fall | Antwortentwurf | Prüfbasis |
| --- | --- | --- |
| COACH-01 | In C-Dur ist Dm7 ein Mollseptakkord (ii⁷), G7 ein Dominantseptakkord (V⁷) und Cmaj7 ein Durseptakkord mit großer Septime (Imaj7). C4 ist die Septime von Dm7 und sinkt um einen Halbton zu H3, der Terz von G7. F4 als Septime von G7 sinkt zu E4, der Terz von Cmaj7. | [Open Music Theory, ii–V–I, Key Takeaways](https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/) |
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

## Kataloge und Claims

- Im [Latin-Katalog](../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md)
  ist PROG-024 als Übungsschema beschrieben. In C-Dur bleibt D im
  Übergang D7 → Dm7 liegen, während F♯ zu F sinkt. D7 ist V7/V, A7
  wäre V7/ii. Die Partiturangabe ist auf das Arrangement und die Takte
  begrenzt. PROG-025 verwendet in C-Moll die Stufen i–iv–V7–iv.
- Bei [PAT-031](../../knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md)
  sind Taktgrenzen, Puls und Glockenschläge in Ticks angegeben. Die
  Entscheidung über die metrische Lesart benötigt eine Hörprobe.
- Bei P12 ist die rechte Hand relativ zu D grundtonlos. Bei P19 sind
  C♯→C→H zwei Halbtonschritte und H→A→G zwei Ganztonschritte. Die
  Spielprüfung für P02 bleibt offen.
- `KB-CLAIM-032-MINOR` prüft Akkordzugehörigkeit und Halbtonabstände in
  den Beispielen zu CLAIM-032. Die akkordischen Kadenztypen sind in
  Beispiel 2 von Open Music Theory belegt. Die Bewegungen sind aus den
  Akkordtönen hergeleitet. Die im historischen Datensatz SRC-020
  hinterlegte Levine-Seite bleibt ungeprüft.
  [Open Music Theory, ii–V–I](https://viva.pressbooks.pub/openmusictheory/chapter/ii-v-i/)

## Historische Quellenangabe SRC-033

Die Titelsuche im DNB-SRU-Dienst mit
`tit="Systematische Taxonomie der Heptatonik"` lieferte 0 Datensätze.
Eine Websuche nach Titel und Autor ergab keinen bibliografischen Treffer.
WorldCat war über den verwendeten Zugriff nicht auswertbar. Für Robert
Prehn, das Jahr 2017 und die Seitenangaben liegt damit kein Beleg vor.
Für CLAIM-003 bis CLAIM-006 liegen inzwischen getrennte Fundstellen
zu den einzelnen Stimmungsmodellen vor. Die alten Seitenangaben bleiben
als historische Zuschreibungen in den Zeilen erhalten. Die Nachweise zu
den ersetzten Fundstellen stehen im [Quellenabgleich](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_QUELLENABGLEICH.md).

Oliver Prehns Lehrmaterial ist unter SRC-0003 verzeichnet. Die vier
ausgewählten Familien liefern jeweils sieben Rotationen der Intervallfolge,
insgesamt 28 verschiedene Folgen. Die Ausgangsfolgen in Halbtönen sind
Dur (2,2,1,2,2,2,1), aufsteigendes melodisches Moll (2,1,2,2,2,2,1),
harmonisches Moll (2,1,2,2,1,3,1) und harmonisches Dur (2,2,1,2,1,3,1).
Die beiden harmonischen Familien enthalten einen Dreihalbtonschritt.
Die Grenze des Modells steht im korrigierten CLAIM-016. Rechte für eine
Weiterverteilung der Quelle wurden nicht ermittelt.
[Oliver Prehn, The Modes, S. 1–2](https://newjazz.dk/Compendiums/Major_Melmi_Harmmi_HarmMa_Modes.pdf)

## Wissensgraph

Weiterführung nach PR #52: 25 weitere historische Restknoten haben eine
begrenzte Definition; 49 bleiben offen. CDR-010 besitzt einen präzisen
Korrekturvorschlag zur sechstönigen Sammlung, bleibt aber historisch FAIL.
Quellen-, Modell- und Projektbelege sind getrennt gekennzeichnet; keine
neue menschliche Abnahme. [Aktueller Einzelstand](../../docs/audit/fable-5.2/GRAPH_KLAERUNG_CDR010_2026-11-14.md).
Die folgenden Absätze halten die früheren Zwischenstände fest.

Aktualisierung vom 14.11.2026: Nach vier Formatknoten und sechs weiteren
musikalischen Definitionen fehlen 74 kanonische Endpunktdefinitionen.
Vier Kanten haben jetzt ein ergänzendes Quellen-/Claim-Register; drei
Stichproben sind bestätigt, CDR-010 ist beanstandet. Alle Kanten bleiben
`REVIEW_REQUIRED`. [Aktuelle Graphnachweise](../../docs/audit/fable-5.2/GRAPH_NACHWEISE_2026-11-14.md).
Die nachfolgende Zählung beschreibt die frühere Gegenprobe ohne diese Ergänzungen.

Im Relationsregister stehen 97 Kanten (38 CR, 36 REL, 23 CDR), alle
mit `REVIEW_REQUIRED`. Der Abgleich beider Endpunkte mit den Katalogen
PROG, PAT, P und den Domänen M01–M12 ergibt 86 unterschiedliche
offene Knoten-IDs in 61 Kanten. Die übrigen 36 Kanten haben auf beiden
Seiten einen auflösbaren Endpunkt. Für alle 97 fehlt ein direktes
Feld mit Quellen- oder Claim-ID. Der Detailbericht aus
`python -B scripts/audit_knowledge_coverage.py --check --details /tmp/steps-coverage.csv`
nennt pro Kante die offenen Endpunkte. Kantenidentität und formale
Katalogzuordnung sind damit prüfbar. Richtung, Beziehungstyp und
fachliche Gültigkeit benötigen einen Einzelnachweis.

## Historische Dateizuordnung

Die [Archivnachweise](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_ARCHIVNACHWEISE.md)
dokumentieren zusätzliche CSS-Vergleichsstände und die technische Prüfung
aller 36 MIDI-Dateipfade.

Alle zehn Registerpfade sind unter einem anderen Wurzelordner in der
Git-Historie auffindbar. Für die Gegenprobe
`research/STEPS_Bibliothek/` im Registerpfad durch
`00_Arbeitsvorbereitung/` ersetzen. Die Dateien per
`git show <Commit>:<historischer Pfad>` aus dem Commit
`b42a990681ce5fd12c7756fb2ada962e01474521` lesen und die ausgegebenen
Bytes mit SHA-256 prüfen.

- F00412, F00571, F00704, F00768, F00937 und F01002 teilen dort eine
  identische CSS-Version mit 63.109 Bytes und SHA-256
  `34f603614eae19caed79c0c752d7cc6a823707bc66c2fad4c72446dffea485fc`.
  Das Register nennt je 63.332 Bytes und
  `32289d8747feddbc21cccedc6522f0f1ab2b18bf2a0c5d9a65356f8fdc9f5f29`.
  Eine spätere lokale Suche fand die exakte Registerfassung in Codex-
  Sicherungsbäumen wieder: 63.332 Bytes, SHA-256 wie im Register.
  [Reproduzierbarer Hashabgleich](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_ARCHIVNACHWEISE.md#ergänzung-exakte-registerfassung-lokal-wiedergefunden-13112026).
  Externe Herkunft, Rechte und öffentliche Archivzuordnung bleiben offen.
  Die [Fortsetzung vom 14.11.2026](../../docs/audit/fable-5.2/CSS_PROVENIENZ_2026-11-14.md)
  belegt inzwischen die technische Herkunft über 17 gespeicherte
  Bandcamp-Player und sechs Live-CDN-Vergleiche. Rechte am vollständigen
  Bundle und dauerhafte Archivzuordnung sind weiterhin nicht abgenommen.
- Bei PPR-MIDI-01 bis -04 enthält das Register 0 Bytes und den Platzhalter
  `PHYSICAL_MIDI_CORPUS_REVIEW` im Hashfeld. Der historische Commit
  enthält unter den jeweiligen Paketpfaden 18, 10, 5 und 3 MIDI-Dateien.
  Die Prüfsummen unten identifizieren die jeweiligen README-Dateien.
  Herkunft, Spielinhalt und Nutzungsrechte der MIDI-Dateien sind separat zu
  prüfen. Die Prüfung bezieht sich auf die historischen Dateien in der Git-Historie.

| Register-ID | Bytes README | SHA-256 README im historischen Commit |
| --- | ---: | --- |
| PPR-MIDI-01 | 1221 | `9310d394969958035f660f0fa2f944b9197577bd57e2c9e262dfcf83c38cecb2` |
| PPR-MIDI-02 | 1072 | `505bda9badf9f9e993ef800c1f7cb748e34f84c09cd684cfaf7c737b429718e2` |
| PPR-MIDI-03 | 1128 | `3f3e49784c6829cb552a876ca855f59e17841ef6939d189b1a089a55080c433d` |
| PPR-MIDI-04 | 1504 | `fb4b73c952fed48e209595c1f8d314a600f20265e8a8646741be14c014e59e83` |

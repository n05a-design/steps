# Gemeinsame RWC-/Swing-Komponenten und neuer Garcia-Originalbeitrag

Verifizierte Basis: `main` **6f79c4e86468d2d860e6c71622b93394a41992ce**, nach externem Merge von PR #61. Der Arbeitsbaum war sauber. Fortsetzung auf `codex/audit-korpus-evidenzgrenzen-20261114`; kein direkter Merge. Die bisherigen technischen und historischen Nachweise bleiben erhalten.

## Ergebnis und klare Statusgrenzen

Erstmals liegt in dieser Fortsetzung eine tatsächlich untersuchte Lieferung mit **100 gemeinsamen Harmonie-, Beat- und MIDI-Stückidentitäten** vor. Sie verbessert den bisherigen Stand aus getrennten Harmonie- und Drumdatensätzen. Die [14-Fälle-Matrix](GRAPH_KORPUS_14_2026-11-14.csv) unterscheidet nun explizit zwischen Popular-Teilstichprobe und fehlendem Nachweis des jeweils behaupteten Subgenres. **Alle14 historischen Korpusbehauptungen bleiben OPEN.**

Zu CDR-019 wurde ein **Originalbeitrag von Walter Garcia aus2023** zugänglich und begrenzt visuell geprüft. Das ist ein zusätzlicher quellengebundener Analysebeleg. Reily1996, Cabral, Garcia1999 und die konkrete Schreiner-Stelle bleiben als angeforderte ältere Originalseiten ungeprüft; der neue Beitrag ersetzt sie nicht.

## CDR-019: Originalbeitrag gelesen, ältere Quellen bleiben getrennt

[Garcia2023, Iberic@l24](https://dialnet.unirioja.es/descarga/articulo/10358444.pdf), PDF7/gedruckte S.6, Abschnitt4 Absätze21–27, unterscheidet die Gitarrenbasis von ihren Varianten und deren Ähnlichkeit zu Tamborim- oder Caixa-Phrasierung. Auch die Basswirkung wird differenziert analysiert. Dies präzisiert den Vergleich und widerspricht einer unkommentierten Gleichsetzung von Ähnlichkeit, Synthese und eindeutiger historischer Ursprungsrichtung.

Titelseite und maßgebliche Seite wurden gerendert und visuell gelesen. Der PDF-Export weist fehlerhafte Textglyphen auf; eine automatische Textextraktion wurde deshalb nicht als verlässliche Inhaltsabnahme ausgegeben. [Quellenprotokoll](CDR019_GARCIA_2023_QUELLENBEFUND_2026-11-14.json): PDF15 Seiten, SHA-256 `5f659a994bcf07c95adbde4fbec83352e56992fc987664325cc09954cee523d7`. Die Titelseite nennt2023 als Publikationsjahr und2024 als Exportzeitpunkt sowie CC BY-NC-ND4.0 für den Text. PDF und Bilder bleiben lokal.

Die direkte OpenEdition-Seite bot einen Challenge-Bildschirm; die regulär erreichbare Dialnet-Kopie wurde über die Windows-Zertifikatsprüfung geladen. Ein zunächst gescheiterter Python-Zertifikatsabruf wurde nicht durch Abschalten der TLS-Prüfung umgangen. Ein neuer Scribd-Treffer zum Garcia-Buch zeigt nur Metadaten für41 Seiten statt221 im Werkdatensatz; das ist kein Nachweis des vollständigen Buches oder seiner benötigten Seiten. Cabral war weiterhin nicht als gelesener Originaltext zugänglich.

CDR-019 bleibt OPEN. Der Gesamtgraph kennzeichnet nun den neuen begrenzten Autorenbeleg und zugleich die ungelesenen älteren Originale. Weder historische Kausalität noch die sechs historischen Definitionslücken werden damit als freigegeben markiert.

## RWC2.0: wirklich gemeinsame symbolische Zeitachsen

Die [RWC-Annotationssammlung](https://github.com/rwc-music/rwc-annotations/tree/0a1a6c31dbe73a7f5d44f7caef8cd0999402a4c2) wurde auf Commit `0a1a6c31dbe73a7f5d44f7caef8cd0999402a4c2` festgelegt. Lokaler Lieferhash: `27bc4da9c8730b143b2dacb4495c92bb45a00e0cf7d7b385d51203fc6055d534`; eigener Hash, kein veröffentlichter Herausgeber-Referenzhash. Das [Autorenpaper2026](https://transactions.ismir.net/articles/10.5334/tismir.326) und die Repository-Dokumentation beschreiben die symbolischen Rekonstruktionen und überarbeiteten Alignments. Dies ist keine neue unabhängige Audioabnahme durch dieses Audit.

Der Prüfer verbindet für jedes RWC_P001–RWC_P100 ausschließlich die identischen Dateistämme von Akkord-CSV, Beat-CSV und ausgerichteter MIDI-Datei. Akkord- und Beatzeiten sind Sekunden; MIDI-Ticks werden mit der tatsächlichen Tempokarte umgerechnet. Die unter MIDI_aligned abgelegte README enthält eine offenbar unpassende CSV/F0-Formatbeschreibung. Diese wurde nicht blind als Dateischema benutzt: Tatsächlich vorliegende MIDI-Dateien wurden als SMF geparst; Akkord-/Beat-Header separat geprüft. Keine fremden Repository-Skripte wurden ausgeführt.

Der untersuchte RWC-P-Rahmen ist **Popular mit Unterlabels Pop/J-pop**. Daraus werden keine Jazz-, Funk-, House-, Liquid-, Jump-Up-, UKG- oder Latin-Labels konstruiert. Noten auf MIDI-Kanalindex9 sind zunächst symbolische Perkussionskanal-Ereignisse. Eine vollständige instrumentenspezifische Belegung und die Identität mit einem STEPS-PAT wurden nicht verifiziert.

| Harmonieform, strenge Akkordqualität | Gefundene Zeitfenster | Davon mit Kanal9-Einsätzen | Stück-IDs mit beidem | Stück-IDs mit kombiniertem deklariertem Notenklassen-Teilmuster |
| --- | ---: | ---: | ---: | ---: |
| PROG-001 | 35 | 35 | 6 | 1 |
| PROG-002 | 22 | 22 | 3 | 1 |
| PROG-003 | 18 | 17 | 8 | 0 |
| PROG-007 | 128 | 101 | 27 | 2 |
| PROG-017 | 1 | 1 | 1 | 0 |
| PROG-023 | 0 | 0 | 0 | 0 |
| PROG-025 | 0 | 0 | 0 | 0 |
| PROG-028 | 0 | 0 | 0 | 0 |

Die [Messdatei](KORPUS_RWC_GEMEINSAME_ZEITACHSE_2026-11-14.json) enthält alle100 Stück-IDs, drei Originaldateihashes je Stück, tatsächliche Fenster und getrennte strenge/auf Dreiklänge projizierte Ergebnisse. Die Erkennung ist bewusst begrenzt: unbekannte Akkordsymbole und Lücken unterbrechen die Folge; transpositionsgleiche Root-/Quality-Folgen sind keine Tonika-/Kadenzanalyse. Überlappende Fenster sind keine unabhängigen Stücke. Null Treffer bedeuten im begrenzten Prüfer keine Abwesenheit im Repertoire.

## Deklarierte rhythmische Teilmuster statt falscher Patternfreigabe

In annotierten vollständigen4/4-Takten werden zusätzlich folgende **Notenklassen** geprüft:35/36 an1/3,38/40 an2/4 und42 an den acht Achtelpositionen, jeweils mit±0,1 lokaler Vierteldauer. Die Zuordnung zu Kick/Snare/Closed-Hat ist eine hier **nicht für die konkrete RWC-Quelle verifizierte GM1-Annahme**. Zusätzliche Noten sind erlaubt; PAT-001-Synkope, Tempo, Dynamik und vollständige Patternidentität werden nicht geprüft. Die Ergebnisse bleiben als Teilmuster und ohne Freigabe gekennzeichnet.

Über alle100 Stücke liegen10744 vollständige4/4-Takte vor;3589 erfüllen das deklarierte35/36-plus38/40-Teilmuster,2153 das42-Achtelteilmuster,1095 beide. Das sind weder Genreanteile noch unabhängige Songbeobachtungen. Für die strenge PROG-001-Harmonieform liefert **RWC_P084** ein gemeinsames Zeitfenster mit diesem kombinierten Teilmuster. Es ist ein konkreter prüfbarer Kandidat für REL-001, kein Nachweis einer häufigen oder exakten PROG-001/PAT-001-Paarung.

Die [separate Gegenprüfung](KORPUS_RWC_GEGENPRUEFUNG_2026-11-14.json) kontrolliert RWC_P084, RWC_P001 und RWC_P002: zwei Routen der MIDI-Zeitumrechnung stimmen überein, und21 gespeicherte Fensterzählungen stimmen mit einer direkten Ereignissuche statt der produktiven Binärsuche überein. Der Mido-Parser wird geteilt; eine unabhängige Audioprüfung wird nicht behauptet.

## Auswirkungen auf die14 Korpusfälle

| Fallgruppe | Neu verfügbar | Tatsächlich noch fehlend |
| --- | --- | --- |
| CR-029 | Gemeinsame Popular-IDs und deklarierte rhythmische Teilmuster in RWC-P | Instrumentmapping, vollständige Zieldefinition und repräsentativer Geltungsbereich |
| CR-031 | Zeitlich verortete Harmonieformen im selben Popular-Rahmen | Kadenz-/Funktionsdefinition und Prüfung der Notwendigkeitsbehauptung |
| REL-001 | Konkreter gemeinsamer Kandidat RWC_P084 | Vollständiges PAT-001-Matching, Tempo-/Klang-/Spielkontext, Häufigkeitsnenner und Fachabnahme |
| REL-005 | Zusätzlich18 bevorzugte asynchrone Swing-Takes aus JazzSAMBA, mit gemeinsamem Chart-/Drum-Zeitfenster | Gespielte Harmonie statt Leadsheet, Instrumentmapping, exaktes Ride-/Pedalpattern und repräsentativer Nenner |
| REL-006,007,014,015,026,032,035 | Zusätzliche gemeinsame Harmonie-/Perkussionskomponenten, soweit die jeweilige Form vorkommt | Passendes historisch behauptetes Subgenre und Zielpattern; Popular/J-pop ist kein Ersatz |
| CR-030,032 und REL-017 | Neue Kandidatenprüfung mit ausdrücklich unpassendem RWC-P-Genreumfang | House-/Jump-Up-spezifische gemeinsame Annotationen; bisherige GiantSteps-Teilbelege bleiben getrennt |

## JazzSAMBA: veröffentlichte Alternative nach fehlerhaftem Projektlink

Der zunächst gelesene Codepfad lieferte404. Die anschließende alternative Suche fand jedoch den [veröffentlichten Zenodo-Datensatz](https://zenodo.org/records/22943963). Der13,8-kB-Katalog stimmt mit dessen publizierter MD5-Prüfsumme überein. Er erlaubt die vollständige Auswahl von18 bevorzugten asynchronen Takes mit Genre `swing`, Swing-Flag und4/4 aus76 Katalogstücken. Die archivierte Erlaubnisnotiz und die gesonderten Copyright-Angaben zu den zugrundeliegenden Standards wurden getrennt gelesen; keine universelle Kompositionsrechtefreigabe wird abgeleitet.

Aus dem10,8-GB-Archiv wurden ausschließlich54 kleine Dateien zu diesen18 Takes abgerufen: jeweils Takt-CSV, Akkord-CSV und bevorzugte originale Drum-MIDI-Spur laut Datensatzbeschreibung. Begrenzte normale HTTP206-Bereichsabrufe, ZIP-CRC und eigene Datei-SHA256 sichern den selektiven Abruf. Das Gesamtarchiv und Audio wurden nicht geladen; seine veröffentlichte Gesamt-MD5 wurde folglich **nicht** als verifiziert markiert. Eine429-Antwort unterbrach den Abruf nach15 vollständigen Takes. Nach Pause und reduzierter Abfragerate wurden die drei übrigen Takes aus dem gesicherten Zwischenstand ergänzt; keine Zugriffssperre wurde umgangen.

Die [Messdatei](KORPUS_JAZZSAMBA_SWING_2026-11-14.json) zeigt für die PROG-003-Form:

| Modellansicht | Zeitfenster der Chartform | Davon mit Drum-Note-ons | Ausgewählte Stücke mit beidem |
| --- | ---: | ---: | ---: |
| Strenge Akkordqualität | 373 | 373 | 14 |
| Getrennte Dreiklangprojektion | 689 | 688 | 18 |

Die Sekundenwerte stimmen mit den jeweiligen Takt-/Bruchteilkoordinaten überein, geprüft mit maximal2ms erlaubter Abweichung. Sechs endständige Akkordzeilen haben Dauer0. Sie bleiben in der Quelle erhalten und werden explizit als nicht klingende positive Intervalle ausgeschlossen; nichtterminale Null-/Negativintervalle und Überlappungen werden zurückgewiesen.

Eine zusätzliche lokale technische Gegenprobe bestätigt die beiden MIDI-Zeitumrechnungsrouten und120 direkte Fensterzählungen der Stück-IDs1,3 und4. Der Parser ist geteilt; das ist keine unabhängige musikalische Abnahme. Das lokale Gegenprüfprotokoll bleibt im Übergabeordner erhalten.

**Die Akkordlabels stammen laut Projektbeschreibung aus zeitlich verorteten Leadsheets, nicht aus einer Transkription der tatsächlich gespielten Harmonie.** Drum-Originalspuren und automatische Transkriptionen werden getrennt. Die einheimischen MIDI-Notennummern werden nicht ungeprüft als General-MIDI-Ride-/Pedalrollen interpretiert. Chartform plus Drum-Einsätze sind deshalb noch kein Nachweis der historischen ii–V–I/Spang-a-lang-Paarung. Die gewählte Repertoirestichprobe eines Ensembles ist auch kein repräsentativer Swing-Korpus.

## Rechte, Reproduktion und Abschlussgrenzen

Das festgelegte RWC-Repository trägt **CC BY-NC4.0**. Original-MIDIs, Rohannotationen, Audio und Drittanbieter-Code bleiben lokal. Die versionierten Dateien enthalten die eigenen Auditberechnungen, Metadaten und Hashes mit Herkunfts-/Lizenzhinweis; sie werden nicht als kommerziell freigegebene STEPS-Produktdaten behandelt. Die Lizenz des Autorenpapers ist von der Datenlizenz getrennt. CSS-Bundle-Rechte bleiben hiervon unberührt und offen.

```text
python -B scripts/audit_rwc_joint.py --check
python -B scripts/audit_rwc_joint.py --rwc-archive <lokales-verifiziertes-ZIP> --check
python -B scripts/audit_graph_corpus.py --check
python -B scripts/audit_jazzsamba_components.py --check
python -B scripts/audit_jazzsamba_components.py --selection-manifest <lokales-Quellenmanifest> --check
python -B -m unittest discover -s tests -p 'test_*.py'
```

Die Archiv-/Manifestläufe benötigen das vorhandene Audit-Mido; normale CI prüft die versionierten Beobachtungen ohne Netzwerkdownload. Der [RWC-Prüfer](../../../scripts/audit_rwc_joint.py), [Swing-Prüfer](../../../scripts/audit_jazzsamba_components.py) und ihre Regressionstests sichern ID-Mengen, Zeitachsen, Intervallgrenzen, unbekannte Harmonien, vollständige Takte, Notenklassen, Nenner und fehlende Freigaben ab. Die endgültigen Test-, Git- und CI-Ergebnisse werden im Übergabenachweis festgehalten.

Lokal bestanden315 Kern- und36 Skilltests. Der Benchmark bleibt92 PASS/0 FAIL/27 PENDING, erwarteter Exit1. Sechzehn zusätzliche Integritäts-/Generatorprüfungen bestehen. Der vollständige Secret-Scan meldet0 quarantänisierte und0 neue Befunde; die historische Sicherheitsfreigabe bleibt offen. Die Linkprüfung erfasst951 interne Verweise ohne neue aktive Fehler neben25 bekannten historischen Archivverweisen.

Der Graph bleibt97 Originalkanten,41 begrenzte Stichproben/1 FAIL/55 OPEN,73 technische Kantengegenprüfungen und58 Graphproben. CDR-010 bleibt FAIL; sechs historische Definitionslücken sowie27 Benchmark-PENDING-Fälle bleiben offen. **Keine neue unabhängige Fach-, Hör-, Spiel-, Coach-, CSS-Rechte- oder Sicherheitsfreigabe. Gesamtaudit: NICHT_ABGESCHLOSSEN.**

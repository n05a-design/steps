# Korpusfälle und Quellenprüfung nach PR #58

Verifizierte Basis: `main` **cedcaaf55d85f57e3b5cd71c090f237d4b4e517b**, nach externem Merge von PR #58. Arbeitsbranch: `codex/audit-korpus-quellen-20261114`. Alle 14 bisherigen Korpusfälle sind einzeln untersucht und maschinenlesbar präzisiert. Ihre historischen Aussagen bleiben `OPEN`; eine geprüfte Datenlücke ist kein positiver Häufigkeitsnachweis.

## Ergebnis

Die [Korpusmatrix](GRAPH_KORPUS_14_2026-11-14.csv) und das [Prüfmodell](../../../knowledge/relations/GRAPH_CORPUS_REVIEW.json) verbinden jede Original-ID mit Originalzeilenhash, Sampling-Rahmen, erforderlichen Annotationen, tatsächlichen Fähigkeiten der geprüften Kandidaten und konkreter Restanforderung. Projektkatalogzeilen werden separat durch Dateihash und Zeileninhalt gebunden. Gemeinsame Instrumentation ist keine Drum-Ereignisannotation; zwei unterschiedliche Datensätze sind keine gemeinsame Aufnahme.

| Kante | Individuelles Ergebnis / noch fehlende Evidenz |
| --- | --- |
| CR-029 | GMD-Pop-Beat-Teilmenge tatsächlich gemessen. Beauftragte Takes sind keine repräsentative Stichprobe veröffentlichter Popsongs. |
| CR-030 | House-Untergenre und Kick-/Offbeat-Hat-Muster brauchen gemeinsame Annotation; GMD `dance` wird nicht zu House umetikettiert. |
| CR-031 | Kadenz und Akkordschleife getrennt. Billboard ist ein möglicher Harmonieanker, beweist aber keine allgemeine Notwendigkeit prägnanter Kadenzen. |
| CR-032 | House-Tempogrenzen120–128 bleiben unbelegt; Tempo-, Halb-/Doppeltempo- und Kickentscheidungen gemeinsam erforderlich. |
| REL-001 | PROG-001/PAT-001 im Projekt verankert; gemeinsame Pop-Aufnahmen und definierter Häufigkeitsnenner fehlen. |
| REL-005 | PROG-003/PAT-012 im Projekt verankert; ii–V–I und Ride-Swing müssen in derselben Aufnahme annotiert werden. |
| REL-006 | PROG-007/PAT-007 im Projekt verankert; Dorian-Vamp/Funk-Paarung benötigt gemeinsame Harmonisierung und Drumannotation. |
| REL-007 | PROG-017/PAT-013 im Projekt verankert; Backdoor/Linear-Ghost-Textur benötigt gemeinsame Aufnahme und Genreabgrenzung. |
| REL-014 | PROG-002/PAT-018 im Projekt verankert; Liquid-DnB-Taxonomie und gemeinsame Harmonie-/Breakbeat-Annotation fehlen. |
| REL-015 | PROG-007/PAT-020 im Projekt verankert; UKG-Subgenre, Vamp und tatsächliches Timing gemeinsam prüfen. |
| REL-017 | PAT-022 allein belegt keine Jump-Up-Zugehörigkeit; Bassereignisse und Subgenreannotation fehlen. |
| REL-026 | PROG-023/PAT-018 ist eine Projektpaarung; Liquid-Ästhetik benötigt gemeinsame Fassung und unabhängige Bewertung. |
| REL-032 | PROG-025/PAT-028 im Projekt verankert; Montuno-/Cha-Cha-Kontext ist ohne gemeinsame Aufnahme kein Typizitätsbeleg. |
| REL-035 | PROG-028/PAT-030 im Projekt verankert; gemeinsame Aufnahmen fehlen, historische57-Prozent-Zuschreibung bleibt gesondert offen. |

Die offiziellen Dokumentationen von [GMD](https://magenta.tensorflow.org/datasets/groove), [McGill Billboard2.0](https://ddmal.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/) und [GiantSteps](https://www.cp.jku.at/datasets/giantsteps/) wurden auf Eignung geprüft. Billboard-Annotationen und GiantSteps-Audio wurden in dieser Sitzung nicht heruntergeladen oder quantitativ ausgewertet. Billboard bietet Harmonie-/Strukturinformationen, GiantSteps Tempo-/Tonartaufgaben. Daraus folgen keine gemeinsamen Akkord-/Drum-Paare. Kandidatenrechte gelten nur für die jeweils bezeichneten Daten, nicht automatisch für Tonaufnahmen oder das STEPS-CSS-Bundle.

## Tatsächliche Korpusmessung

Google LLCs **Groove MIDI Dataset v1.0.0**, CC BY4.0, wurde als MIDI-only-Archiv lokal geladen. Der SHA-256 entspricht exakt dem auf der Herausgeberseite angegebenen Wert `651cbc524ffb891be1a3e46d89dc82a1cecb09a57c748c7b45b844c4841dcc1e`. Attribution: Google LLC; Gillick et al., *Learning to Groove with Inverse Sequence Transformations* (2019). Das Archiv wird nicht erneut veröffentlicht.

Von1150 Metadatenzeilen tragen27 das primäre Stilwort `pop`. Der vorab festgelegte Filter `pop` + `beat` + `4-4` ergibt **15 Takes von vier Schlagzeugern**. Der Nenner sind306 vollständige Takte vor dem MIDI-Ende, mit Tick0 als angenommener Taktphase. Jeder Rolle entsprechen612 Zielgelegenheiten. Gezählt wird das Vorhandensein mindestens eines passenden positiven Note-on im Fenster; doppelte Treffer zählen nicht doppelt, Note-on mit Velocity0 zählt nicht. Die quellenspezifischen Notennummern werden deklariert.

| Zeitfenster um die Zielposition, in Viertelnoten | Kick36 auf1/3 | Snare37/38/40 auf2/4 |
| --- | ---: | ---: |
| ±0,05 | 218/612 | 273/612 |
| ±0,10, Hauptmessung | **331/612** | **366/612** |
| ±0,15 | 359/612 | 385/612 |

Die [Messdaten](GRAPH_KORPUS_GMD_2026-11-14.json) führen alle15 Aufnahme-IDs, MIDI-Dateihashes und Einzelergebnisse. Die [Gegenprüfung](GRAPH_KORPUS_GMD_GEGENPRUEFUNG_2026-11-14.json) vergleicht Ziel-Fensteriteration mit einer separaten Zuweisung von Ereignissen zu Viertelpositionen. Beide Berechnungen stimmen für alle15 Takes überein; sie teilen den Mido-Parser. Die zweite Methode verwendet exakte Tickarithmetik, damit inklusive Fenstergrenzen nicht durch Gleitkommaumrechnung verschoben werden.

Dies sind **keine Songhäufigkeiten**, keine repräsentativen Genreanteile und keine unabhängigen612 Songbeobachtungen. Beauftragte Klick-Aufnahmen, mehrere Takes desselben Spielers, Beat-/Fill-Auswahl und unbestätigte Taktphase begrenzen die Aussage. Die starke Fensterabhängigkeit wird ausgewiesen; ein Konfidenzintervall für die Popmusik-Population wäre hier nicht gerechtfertigt.

## CDR-019: analytische Quellenkette, Herkunft weiterhin offen

Ghezzi2009, PDF9–10, wurde im [Originalbeitrag des Historikerkongresses](https://anpuh.org.br/uploads/anais-simposios/pdf/2019-01/1548772191_92b37c846f0c683a26fa7f6e60e6d08a.pdf) gelesen und Seite9 visuell kontrolliert. Der Beitrag ordnet Gitarrenbass und Akkordanschläge analytisch Surdo-/Tamborim-Funktionen zu, beschreibt veränderte Akzente und variable Figuren. Seine konkrete Kette führt zu **Garcia1999, S.21–22,25–38,45–49**. Das ist keine neue Prüfung von Garcia selbst oder der früher zitierten Schreiner-Stelle. Der institutionelle Reily1996-Werkdatensatz ist bibliografisch bestätigt; Cabral-/Baden-Powell-Originalinterview bleibt ungelesen.

Die zusätzliche Kette verbessert den Locator, bestätigt aber keine eindeutige historische Kausalität. Eine spätere Analyse ist kein zeitgenössischer Entstehungsbeleg. CDR-019 bleibt `OPEN`; die historische Definition wird nicht ersetzt.

## CDR-021: neue Feldstudienfundstelle, Onset ist kein dynamischer Akzent

[Marcelino2010, UDESC](https://sistemabu.udesc.br/pergamumweb/vinculos/000000/000000000019/00001934.pdf), untersucht Baterias in Florianópolis aus der Perspektive ihrer Mestres. PDF34 / gedruckte S.33, Fig.3–4 wurde visuell geprüft: primeira setzt auf2, segunda auf1 im binären Modell ein. Die Noten zeigen **keine dynamischen Akzentzeichen**. Fußnote14 nennt abweichende Stimmungen und einen fehlenden segunda-Part außerhalb der untersuchten Region; daraus wird kein heutiger universeller Rio-Befund abgeleitet.

Der neue Prüfentwurf bildet ausschließlich diese Rollen und Einsatzpositionen ab. Er bestätigt weder die historische allgemeine `PERFORMANCE_NORM` noch die dynamische Akzentbehauptung. Die beiden Surdo-Definitionsvorschläge verweisen jetzt auf den konkret gelesenen Beleg; die historische Definitionslücke und praktische Fachabnahme bleiben offen. [Quellenprotokoll mit Hashes und Umfang](GRAPH_CDR019_CDR021_QUELLEN_2026-11-14.json). PDFs und gerenderte Seiten bleiben lokal. Bei der Extraktion gemeldete Fontwarnungen wurden nicht als Inhaltsprüfung gewertet; maßgebliche Notation wurde visuell gelesen.

## Reproduktion und Statusgrenzen

```text
python -B scripts/audit_graph_corpus.py --check
python -B scripts/audit_graph_corpus.py --gmd-zip <lokales-verifiziertes-Archiv> --check
python -B scripts/audit_graph.py --check
python -B scripts/audit_graph_semantics.py --check
python -B -m unittest discover -s tests -p 'test_*.py'
```

Der optionale Archivlauf benötigt Mido; normale CI prüft versionierte Identitäten, Nenner, Vertragsgrenzen, Quellenmetadaten und aktuelle Matrizen ohne Netzwerkdownload. Die Aufnahme eines echten neuen Korpus muss anschließend neu ausgewertet werden; ein vollständiger Kandidat wird nicht automatisch freigegeben.

Die Gesamtmatrix bleibt bei97 Kanten: **41 begrenzte Stichproben /1 FAIL /55 OPEN**. Technische Gegenprüfungen steigen72→73, Graphproben57→58. Die Semantikmatrix hat jetzt17 begrenzte Modellprüfungen und eine nicht ausgeführte Herkunftsprüfung. Das ist keine Statusänderung des historischen CDR-021. CDR-010 bleibt `FAIL`, sechs historische Definitionslücken bleiben offen, vollständige unabhängige Fachabnahmen bleiben0.

Lokal bestanden263 Kern- und36 Skilltests. Der Benchmark bleibt92 PASS/0 FAIL/27 PENDING mit erwartetem Exit1. Der erneute vollständige Secret-Scan meldet0 quarantänisierte/0 neue Befunde; die unveränderte Baseline und38 bereinigten Dateien sind erneut geprüft. Zwölf Integritäts-/Generatorprüfungen bestehen. Die Linkprüfung erfasst930 interne Verweise ohne neue aktive Fehler, neben25 bekannten historischen Archivverweisen. Der optionale GMD-Archivlauf reproduziert die gespeicherten15 Einzelmessungen. GitHub-Ergebnisse und Git-Zuordnung werden im Übergabenachweis festgehalten; diese lokalen Ergebnisse sind keine vorweggenommene CI-Freigabe.

**Bearbeitungsstand:** Alle14 Korpusfälle dieses Pakets sind untersucht und spezifiziert; nur die ausdrücklich abgegrenzte GMD-Teilfrage wurde tatsächlich gemessen. Weitere gemeinsame Korpusannotationen und Quellenoriginale fehlen. Das Gesamtaudit bleibt `NICHT_ABGESCHLOSSEN`; Fach-/Hör-/Spiel-/Coach-Abnahmen, CSS-Rechte und Sicherheitsfreigaben bleiben `OFFEN`.

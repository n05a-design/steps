# STEPS V4 – Qualitätsstatus, tatsächlich ausgeführte Tests und Restlücken

## 1. Gesicherte strukturelle Befunde

Am **8. November 2026** wurde `python 08_Validierung/validate_v4.py` auf der erzeugten V4-Dateistruktur ausgeführt. Das maschinenlesbare Ergebnis befindet sich in `MECHANISCHER_PRUEFBERICHT_V4.json` und enthält den Status `pass`, **20.099 bestandene Einzelassertions und 0 gemeldete Probleme**. Diese Zahl ergibt sich aus vielen wiederholten Feld-/Event- und Strukturprüfungen. Sie bedeutet nicht 20.099 fachlich unabhängige musiktheoretische Tests. Die 30 MIDI-Dateien wurden dabei einschließlich gültiger Events, Zeitpositionen und 16-Takt-Ende geprüft. Die JSON-Schemata und verknüpften Identitäten wurden mechanisch kontrolliert.

Ein Katalog mit **180 Testfall-Records** beschreibt weitere Sollprüfungen. **Nicht alle 180 wurden als eigenständige wissenschaftliche Evaluierungen ausgeführt**. Formal geprüfte JSON-/MIDI-Konsistenz ist von tatsächlicher Satzlehre-, Stimmführungs-, Stil- oder Hörvalidierung zu unterscheiden.

## 2. Sichtbare Abdeckungszahlen

| Eintragstyp | V3 | Neu V4 | Gesamt in V4/Archiv | Statusbewertung |
|---|---:|---:|---:|---|
| Konzeptkarten | 142 | 49 neue Research-Module, aber anderer Datentyp | 142 historische Karten + 49 neue Fachmodule | nicht ohne Review aufaddieren |
| Themen-Unterbereiche | – | 163 | 163 | Taxonomie, keine 163 voll begutachteten Kapitel |
| Regel-/Interpretationsentwürfe | 77 | 59 | 136 | typisiert, Quellen-/Fachreview offen |
| Progressionsfälle | 95 | 131 | 226 | inkludiert Varianten und illustrative Fälle |
| Composing Methods | 69 | 65 | 134 | Methodenentwürfe, nicht Validierung eines künstlerischen Ergebnisses |
| Etüden | 19 historische Skizzen | 30 vollständige 16-taktige MIDI-Studien | 30 zusätzlich abspielbare Stücke | didaktische Vorfassungen, Hören/Review nötig |
| Quellen-/Editionseinträge | 47 | 30 | 77 | nicht 77 verschiedene voll gelesene Werke |
| Testfall-Spezifikationen | nicht vergleichbar | 180 | 180 V4-Records | nicht jeder Fall ausgeführt |
| Mechanische Einzelassertions | – | 20.099 bestanden | 20.099 | keine musikästhetischen Gutachten |

## 3. Kritische offene wissenschaftliche Fragen

**P0 – Quellen und Claims.** Die meisten V4-Fachmodule geben Quellfamilien statt direkt überprüfter Aussage-zu-Ausgabe-zu-Passage-Verknüpfungen an. Pro fachlicher Kernthese prüfen: tatsächliche Edition, Zugriff, konkrete Passage, Kontext, Zitierfähigkeit, Gültigkeitsgrenze und Peer-Review-Stufe. Zusätzlich V1- und V3-Chatmarker in dauerhafte Bibliografien übersetzen. Eine konkrete Lese-/Review-Tiefe darf nicht aus `metadata_checked` konstruiert werden.

**P0 – Musiktheoretische Einzelkontrolle.** Vollständige Stufenanalyse, enharmonische Schreibung, lokale Tonika und chord symbol grammar aller 226 Progressionsfälle fachlich kontrollieren. Viele sind eigene Exemplifizierungen und keine belegt typischen Songprogressionen. Dazu Gegenbeispiele und wiederholbare Tests mit wirklich festem Erwartungswert formulieren. 59 neue Regelentwürfe einschließlich Ausnahmen und Stilkontext pro Einzelobjekt prüfen, bevor sie produktive Einschränkungen steuern.

**P0 – Composing-Review.** Die 30 MIDI-Miniaturen bestehen Event- und Datenprüfungen. Sie sind **keine professionell arrangierten oder vollständig transkribierten Werke**. Besonders wichtig: motivische Entwicklung, Phrasenführung, Satzdichte, Bassführung, melodische Plausibilität, instrumentale Idiomatik und stilistische Merkmale durch Musikerinnen/Musiker überprüfen; Hörprotokolle und Bearbeitungen mit Datenrevision festhalten. Die benannten Genres sind zunächst didaktische Arbeitsrahmen. Bei komplexen Akkorden und chromatizitätsbetonten Etüden volle Harmonie- und Melodiekompatibilität prüfen. MIDI-Notation ist nicht garantiert enharmonisch korrekt.

**P0 – Lizenz und Berechtigung.** Das Quellenregister prüft keine pauschale Wiederverwendungsfreigabe aller Titel. Die 20 ursprünglichen PDF/TXT-Quellen, die ältere Forschung erwähnt, wurden in dieser V4 nicht alle als Originaldateien neu eingelesen. Die tatsächlichen Lizenz-/Bild-/Audio-/Score-Rechte bleiben pro Quelle zu klären; keine unzulässige Raw-Source-Publikation.

**P0 – Repository.** Es fand in diesem Dokumentationslauf **keine technische Prüfung eines konkreten Steps-Repositories** statt. Git-Branch, vorhandene Dateien, Programmfunktionen, bereits implementierte Skills, Tests und Mergefähigkeit sind nicht bekannt; Codex muss read-only beginnen.

**P1 – Stiltraditionen und Fremdmodelle.** Pop/Rock, Blues, Jazz, Gospel, Neo-Soul und elektronische Musik brauchen jeweils passende primärwissenschaftliche Originalbelege, nicht allein plausibel klingende Akkordnamen. Nichtwestliche Systeme nur traditionssensitiv erweitern und von sachkundigen Reviewern prüfen, keine automatische I–IV–V-Übertragung.

**P1 – Wissenschaftliche Vertiefung.** Werktreue formanalytische Untersuchungen mit tatsächlich zugänglichen Notentexten, Gegenlesen von Fachliteratur, Corpus-Checks mit Stichprobenprotokoll sowie konkrete Notenbild- und MusicXML-Roundtrips fehlen noch. Die V4 ist ein großer Lehr- und Arbeitskorpus, aber keine abgeschlossene Universal-Enzyklopädie.

## 4. Klare Abnahmegrenzen

- **Bestanden:** Dateien vorhanden, strukturelle Organisation, 30 MIDI-Dateien technisch lesbar, JSON-Identitäten und maschinelle Datenprüfungen.
- **Teilweise erledigt:** Fachtext, Quellenmetadaten, Regeltypen, Progressions- und Composing-Studien, Querverweise.
- **Noch nicht bestanden/nicht durchgeführt:** unabhängige vollständige Fachbegutachtung, Einzelclaim-Quellenkontrolle, Lizenzfreigabe der externen Quellen, Review der musikalischen Qualität, echte Steps-Repo-Integration, produktives Skill-/UI-Verhalten.

Die V4 ist deshalb **für einen systematischen, konkreten Codex-Aufbau nutzbar**, aber **nicht als unfehlbare, fertige wissenschaftliche Musiktheorie-Engine freigegeben**.

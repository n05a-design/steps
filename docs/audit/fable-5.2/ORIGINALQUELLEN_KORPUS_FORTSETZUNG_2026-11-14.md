# Originalsuche und weitere Korpuskomponenten nach PR #59

Verifizierte Basis: `main` **d734fef579d0b921d64a96de35b7702c034ef088**, nach externem Merge von PR #59. Die vier main-Workflows Python#168, Secret#181, Struktur#318 und Pilot#153 waren erfolgreich. Neues Paket auf `codex/audit-originalquellen-korpus-20261114`; kein direkter Merge.

## Tatsächlicher Fortschritt

Zwei zuvor nur anhand ihrer Dokumentation betrachtete Lieferungen wurden lokal quantitativ untersucht: **890 Billboard-Harmonieannotationen** sowie **664 GiantSteps-Genre-/Tempoeinträge** mit getrennten Tempo-Fassungen. Die aktuelle [14-Fälle-Matrix](GRAPH_KORPUS_14_2026-11-14.csv) führt die neuen Teilbeobachtungen je Kante. Die historischen Aussagen bleiben offen: Harmonie allein ist keine gemeinsame Harmonie-/Drumaufnahme, und Tempo-/Genremetadaten enthalten keine Kick-/Hat-Ereignisse.

CDR-019 hat jetzt eine genauer eingegrenzte Beschaffungskette. **Keiner der benötigten Originalvolltexte wurde in dieser Sitzung vollständig zugänglich.** Verlagsreferenzen, Inhaltsverzeichnis, Katalogeinträge und Suchindexauszüge werden ausdrücklich getrennt. [Maschinenlesbares Suchprotokoll](CDR019_ORIGINALSUCHE_2026-11-14.json).

## CDR-019: Originalsuche und Grenzen

| Gesuchtes Original | Tatsächlich eingesehen | Noch erforderlich |
| --- | --- | --- |
| Reily1996, Popular Music15(1), S.1–16 | [Verlagsseite mit Referenzen](https://www.cambridge.org/core/journals/popular-music/article/abs/tom-jobim-and-the-bossa-nova-era/D61EFEFEF21863C86C31477EDCD12FF9), DOI10.1017/S0261143000007935. PDF-Link lieferte HTML. | Autorisierter Volltext, besonders gedruckte S.5/Fig.1. Die Online-Veröffentlichung2008 ersetzt nicht das Heftjahr1996. |
| Cabral, Essay im Songbook Bossa Nova Band2 | Verlagsreferenzliste nennt S.10–17; visuell gelesener Preview bestätigt Essay und englische Fassung im Band2. | Essayoriginal, insbesondere der indirekt/indexiert bezeichnete p.12-Beleg. Der Preview enthält nur vier Inhaltsverzeichnisseiten, keine Essayseite. |
| Garcia, Dissertation1998 | [USP-Verzeichnis](https://dlcv.fflch.usp.br/book/export/html/359): Titel, Verfasser, Betreuung und Verteidigung7.10.1998. | Thesis-Datei und Editionsvergleich; keine Übernahme der Buchseitenzahlen auf die Dissertation. |
| Garcia, Buch1999 | Werk-/Autorenkataloge bestätigen Buch, Verlag und Jahr. | Originalseiten21–22/25–38/45–49 nach Ghezzi2009; noch keine eigene Seitenprüfung. |
| Schreiner1993 | Bibliografischer Werkdatensatz; keine einschlägige Seite eingesehen. | Genaue Ausgabe und tatsächlicher historischen Aussagebeleg. |

Academia bot im direkten Abruf nur Metadaten, Scribd einen JavaScript-Challenge-Bildschirm. Indexierter Text hilft bei der Suche, gilt aber nicht als gelesene Originalseite. Es wurden keine Zugriffssperren umgangen, Kontakte angeschrieben oder Käufe getätigt. Der irreführend benannte Songbook-Preview ist lokal gehasht und auf PDF1–2 visuell kontrolliert; Rechte zur Weiterveröffentlichung werden daraus nicht abgeleitet.

Zusätzlich wurden die60 vorhandenen PDFs unter research/knowledge anhand Dateinamen, Metadaten und jeweils der ersten vier Seiten auf die gesuchten Werke/Autoren geprüft: kein passender Treffer, zwei nicht lesbare Dateien. Das ist ausdrücklich keine Volltextsuche aller Buchseiten und kein Nachweis einer globalen Abwesenheit. Das lokale Suchprotokoll erhält Dateihashes, Umfang und Fehler; bestehende beschädigte Quellen bleiben unangetastet.

Der konkrete nächste Beschaffungsschritt ist nun eingegrenzt: **Cabral-Essay Band2 S.10–17, besonders S.12, sowie Reily1996 S.5/Fig.1**. Auch ein zugänglicher späterer Originalartikel würde die historische Kausalität nicht automatisch abschließen. CDR-019 bleibt `OPEN`, seine Quellenstatusspalte lautet `REFERENCE_CHAIN_IDENTIFIED_BODY_UNVERIFIED`.

## Billboard2.0: tatsächlich gemessene Harmoniekomponenten

Die [offizielle DDMAL-Seite](https://ddmal.ca/research/The_McGill_Billboard_Project_(Chord_Analysis_Dataset)/) verlinkt das geladene Annotationsarchiv und bezeichnet die Annotationen als CC0. Audio wurde nicht geladen; dessen Rechte werden nicht aus CC0 der Annotationen abgeleitet. Der eigene Lieferhash lautet `a22e32bf24c8a18859ce18427c6501a7a72520185cddd6d882ceb3c61d02ec75`; er ist kein veröffentlichter Herausgeber-Referenzhash.

Der eng begrenzte Prüfer akzeptiert genau einen unterstützten Akkord pro vollständig begrenztem Notationstakt. Mehrfachakkorde, Slash-/Zusatznotation, N und andere nicht unterstützte Inhalte brechen die Kontinuität. Exakte aufeinanderfolgende Wiederholungen werden zusammengefasst. Zeitmarken müssen endlich, nicht negativ und geordnet sein. Metadatenwechsel und nichttaktige Abschnitte bilden Grenzen. Damit ist dies **kein vollständiger Billboard-Parser**; ausgeschlossene Bereiche bleiben unbekannt.

Gesucht werden die tatsächlichen Root-/Quality-Folgen von acht STEPS-Progressionen, transpositionsunabhängig. Die strenge Fassung behält die Akkordqualität; die zweite reduziert deklarierte Erweiterungen auf Dur-/Molldreiklänge. Diese Reduktion ist eine gesonderte Modellansicht, kein Beleg für den Originalvierklang und keine Tonika-/Kadenzanalyse.

| STEPS-Ziel | Slots mit strenger Form | Slots mit Dreiklangprojektion |
| --- | ---: | ---: |
| PROG-001 | 3 | 3 |
| PROG-002 | 3 | 3 |
| PROG-003 | 8 | 86 |
| PROG-007 | 47 | 167 |
| PROG-017 | 0 | 3 |
| PROG-023 | 0 | 9 |
| PROG-025 | 0 | 0 |
| PROG-028 | 0 | 7 |

PROG-001/002 sind zyklisch verwandte Formen; ihre Treffer sind keine unabhängigen Beobachtungen. Die890 Dateien ergeben739 normalisierte Künstler-/Titel-Schlüssel. Diese Schlüssel sind **keine verifizierten739 Aufnahmeidentitäten oder Songs**; die Herausgeberbeschreibung nennt andere Song-/Slot-Einheiten. Treffer je Slot, Schlüssel und Fenster stehen getrennt in den [Messdaten](KORPUS_BILLBOARD_KOMPONENTEN_2026-11-14.json), einschließlich aller Datei-Hashes und konkreter Trefferzeilen. Null Treffer im partiellen Parser bedeuten keine Abwesenheit im Repertoire.

Drei echte Positivstellen wurden zusätzlich direkt mit der gelieferten Annotation abgeglichen: Slot0188, Zeile13, PROG-001-Form; Slot0326, Zeile11, PROG-003-Form; Slot0004, Zeile9, PROG-007-Form. Das sind keine Hör- oder Genreabnahmen. Der [technische Bericht der Datensatzautoren](https://pure.uva.nl/ws/files/2014167/149124_TR_BBParser.pdf) erklärt die umfangreichere Syntax und die fehlende durchgängige Modusinformation; sein Quellcode wurde nicht übernommen.

## GiantSteps: tatsächliche Genre-/Tempokomponenten

Das Repository wurde auf Commit `d51ab2422e76abacfaa86616a57054bc222ec9fd` festgelegt. Der lokale ZIP-Lieferhash ist `05b908c799be0e616e0632d7019228fc0e424c106c1873c822fa12957d7f0a87`. Genre und Tempo werden ausschließlich über dieselbe Aufnahme-ID verbunden, Tempo-v1 und Tempo-v2 getrennt. Keine fremden Skripte wurden ausgeführt, kein Audio geladen. Mangels gefundener allgemeiner Repositorylizenz werden Roharchiv, Skripte und Originalannotationstexte nicht erneut publiziert; versioniert werden eigene Kategorien, Identitäten, Hashes und Auswertung.

| Abgrenzung | Fassung | 120–128 BPM einschließlich | Außerhalb | Gesamt |
| --- | --- | ---: | ---: | ---: |
| Exaktes Label `house` | v1 | 9 | 14 | 23 |
| Exaktes Label `house` | v2 | 9 | 14 | 23 |
| Fünf deklarierte House-Labels | v1 | 75 | 35 | 110 |
| Dieselben fünf Labels | v2 | 66 | 44 | 110 |

Die Familienmenge ist explizit: house, deep-house, progressive-house, tech-house und electro-house. Sie wird nicht mit dem exakten House-Label gleichgesetzt. Tempo0 ist fehlend, nicht außerhalb des Bandes. Halb-/Doppeltempo wird nicht automatisch normalisiert. Die [Auswertung](KORPUS_GIANTSTEPS_TEMPO_2026-11-14.json) enthält getrennte Fassungen und Dateihashes. Die [Projektbeschreibung](https://github.com/GiantSteps/giantsteps-tempo-dataset/tree/d51ab2422e76abacfaa86616a57054bc222ec9fd) erklärt den korrekturorientierten Erhebungskontext; daraus folgt keine repräsentative Verteilung sämtlicher House-Musik. Die Daten erlauben keine Prüfung des Viertelkicks oder der Offbeat-Hat. Das vorhandene Elternlabel drum-and-bass wird nicht zu Jump-Up, Liquid oder UKG umgedeutet.

## Umsetzung, Reproduktion und verbleibende Aufgaben

Die Prüfer [Billboard-Komponenten](../../../scripts/audit_billboard_components.py) und [Genre-/Tempo-Metadaten](../../../scripts/audit_edm_tempo.py) reproduzieren ihre Ergebnisse aus den lokal erhaltenen Lieferungen. Normale CI validiert strukturierte Beobachtungen ohne Netzwerkabruf. [Regressionstests](../../../tests/test_corpus_components.py) sichern unter anderem Qualitätsverlust, Brücken über unbekannte Takte, Zeitreihenfolge, doppelte Slots, getrennte Tempofassungen, falsche Nenner und vorgetäuschte Freigaben ab.

```text
python -B scripts/audit_billboard_components.py --check
python -B scripts/audit_billboard_components.py --billboard-archive <lokales-Archiv> --check
python -B scripts/audit_edm_tempo.py --check
python -B scripts/audit_edm_tempo.py --giantsteps-zip <lokales-ZIP> --check
python -B scripts/audit_graph_corpus.py --check
```

Lokal bestehen279 Kern- und36 Skilltests. Benchmark:92 PASS/0 FAIL/27 PENDING, Exit1 wegen ausstehender Pflichtnachweise. Vierzehn Integritäts-/Generatorprüfungen bestehen. Der vollständige Secret-Scan meldet0 quarantänisierte und0 neue Befunde; die bestehende Bereinigung und unveränderte Baseline sind erneut geprüft. 939 interne Verweise wurden ohne neue aktive Fehler geprüft, neben25 bekannten historischen Archivverweisen. GitHub-Ergebnisse werden im Übergabenachweis festgehalten. Die historischen97 Kanten, Golden-Master/-Mirror und Secret-Baseline werden nicht verändert.

**Alle14 Korpusbehauptungen bleiben offen.** Die Harmoniekomponente ist jetzt für neun Paarungskanten sowie CR-031 tatsächlich untersucht, die Genre-/Tempokomponente für weitere Fälle konkretisiert. Gemeinsame Drum-/Harmonieannotationen, passende Subgenre- und Samplingentscheidungen sowie unabhängige fachliche Bewertung fehlen weiterhin. CDR-010 bleibt FAIL; der Graph bleibt41 begrenzte Stichproben/1 FAIL/55 OPEN,73 technisch gegengeprüfte Kanten,58 Proben und0 vollständige menschliche Fachabnahmen. CDR-021 wird nicht durch diese neuen Korpora freigegeben. Fach-, Hör-, Spiel-, Coach-, CSS-Rechte- und Sicherheitsfreigaben bleiben ausdrücklich offen; das Gesamtaudit ist `NICHT_ABGESCHLOSSEN`.

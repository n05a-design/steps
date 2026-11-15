# Funk-Pattern und Reily-Originaltext nach PR #79

## Ausgangsstand und erhaltene Grenzen

PR #79 ist extern gemergt; GitHub-main und sauberer lokaler Ausgangsstand
wurden auf `266d652753f69b0efadfee2ade11f1500be7f43f` abgeglichen.
Branch dieses Pakets: `codex/audit-pattern-funk-20261115`.
Die Pop-/Swing-Messungen sind vorhanden und werden nicht neu als offene
Implementierung behandelt. Dieses Paket ergänzt REL-006/PAT-007 und
REL-007/PAT-013 sowie einen direkt zugänglichen Reily-Quellentext.

## Neue Patternmessung

Die [maschinenlesbare Beobachtung](GMD_FUNK_PATTERN_2026-11-15.json)
enthält alle **53** GMDv1.0.0-Performances mit primärem Stil `funk`,
`beat_type=beat` und 4/4: **vier Drummer,2.560 vollständige Takte**.
Alle Substile einschließlich `funk/purdieshuffle` bleiben sichtbar;
ein Genrelabel ist keine Bestätigung gerader Sechzehntel. Unterschiedliche
Tempi werden nicht auf die Katalogwerte105/100BPM umgerechnet.
Das [GMD-Herausgeber-Mapping](https://magenta.tensorflow.org/datasets/groove#drum-mapping)
gilt nur für diese Lieferung. Literal42 und Closed-Hat-Familie42/22,
Snare-Head38 und andere Artikulationen bleiben getrennt.

| Teilprüfung, Anzahl Takte | ±0,04 Viertel | ±0,1 Viertel |
| --- | ---: | ---: |
| Kick36 auf der Eins | 523 | 608 |
| Snare38 auf2 und4 | 400 | 578 |
| Hat42 auf allen16 Sechzehnteln | 2 | 6 |
| Closed-Hat-Familie42/22 auf allen16 Sechzehnteln | 12 | 26 |
| PAT-013-Kickraster0/360/1200/1560 bei480PPQ | 7 | 40 |
| Mindestens eine Snare38 mit Velocity25–45 außerhalb der Backbeatfenster | 1415 | 1405 |
| Kick auf der Eins erreicht taktweises Kick-Velocitymaximum, Gleichstand erlaubt | 260 | 284 |
| PAT-007-Teilraster gemeinsam: Eins, Backbeat, Hat-Familie, Velocitykandidat | 0 | 0 |
| PAT-013-Teilraster gemeinsam: Kickraster, Backbeat, Hat-Familie | 0 | 0 |

Die gemeinsamen Teilraster prüfen weder vollständige historische
Patternidentität noch Harmoniepaarung. GMD liefert hier keine Akkordlabels
und keine repräsentative Songstichprobe. REL-006 und REL-007 bleiben OPEN.
Fehlende Treffer sind keine Genre- oder Harmoniewiderlegung.

Velocity25–45 wird nur als expliziter Katalogbereich geprüft; mindestens
ein Ereignis ist keine Definition von „dicht“, MIDI-Velocity keine akustische
Lautstärke und ein Kick-Maximum keine Fachabnahme von „The One“.
Die kleinere Anzahl off-backbeat-Kandidaten bei größerer Toleranz ist
erwartbar: Das Ausschlussfenster um2/4 wächst. Solche Zählungen sind nicht
monoton und werden nicht als technische Regression missdeutet.

**881 Takte** besitzen mindestens zwei verschiedene positive Drum-Noten
auf exakt demselben Tick. Das beschreibt das MIDI dieser Stichprobe,
keine allgemeine Funk-Norm. Die Bezeichnung „Linear“ von PAT-013 gegenüber
durchgehenden Hats plus Kick/Backbeat benötigt eine explizite fachliche
Definition. Mikrozeitversatz darf umgekehrt nicht automatisch als Beleg
musikalischer Linearität gelten. „Open Hat Release“ hat im Katalog keine
vollständige prüfbare Zeit-/Controllerdefinition und bleibt ungeprüft.
Historische Katalogzeilen werden nicht umbenannt oder überschrieben.

## CDR-019: Originalprosa gefunden, Aussage enger zugeordnet

Die [Autorenseite](https://www.researchgate.net/publication/231840415_Tom_Jobim_and_the_Bossa_Nova_Era)
führt zum [Reily-PDF](https://www.researchgate.net/profile/Suzel-Reily-2/publication/231840415_Tom_Jobim_and_the_Bossa_Nova_Era/links/56b4865308ae2f3201126ab7/Tom-Jobim-and-the-Bossa-Nova-Era.pdf).
Die [Zugriffs- und Aussagematrix](CDR019_REILY_ORIGINALTEXT_2026-11-15.json)
trennt den erfolgreichen Web-Textzugriff vom gescheiterten lokalen Download.

Reily1996, gedrucktS.5/PDF6, schreibt die Tamborim-/Surdo-Deutung Baden
Powell zu und verweist auf Cabral n.d.a,S.12. Kontext ist João Gilbertos
Gitarrenbegleitung von *Chega de Saudade*. Die Bibliografie S.16/PDF17
identifiziert Cabral als Essay im Bossa-Nova-Songbook Band2,S.10–17.
Dies bestätigt die Zuschreibung in Reilys eigenem Artikel, nicht Cabrals
ungelesene Originalseite oder eine unabhängig gesicherte Entstehungsursache.

Die PDF-Textextraktion besitzt verschobene beziehungsweise beschädigte
Fontzeichen; die Prosa wurde anhand Zeichenentsprechungen und Kontext
gelesen. Die Notenabbildung wurde **nicht visuell verifiziert**: Die
Screenshot-Aufrufe lieferten in diesem Werkzeugkanal keine prüfbare
Bildansicht. Der lokale Download meldete eine Zugriffsbeschränkung; kein
vollständiger lokaler PDF-Hash, kein Umgehungsversuch und keine Kopie in Git.
Der Seitenkopf datiert das Werk1996; die2008-Anzeige der Plattform ist
kein Ersatz für das Publikationsjahr. Schreiners1992-Eintrag im Original
ändert den historischen1993-Projekteintrag nicht rückwirkend.

Noch erforderlich: ReilyFig1 visuell, Cabral insbesondereS.12 und seine
Beleggrundlage, Garcia1999 sowie Schreiner-Ausgabe und konkrete Originalstelle.
Die Graphmatrix führt die neue begrenzte Textprüfung; CDR-019 bleibt OPEN,
beide Knotendefinitionen bleiben ungelöst und historische Kausalität bleibt
unbestätigt. Frühere erfolglose Zugriffe bleiben historische Nachweise.

## Dauerhafte Prüfung und Übergabe

```powershell
python -B scripts/audit_gmd_funk.py --check
python -B scripts/audit_gmd_funk.py --gmd-zip <lokales-GMD-ZIP> --check
python -B -m unittest discover -s tests -p test_gmd_funk.py
python -B scripts/audit_graph.py --check
python -B scripts/audit_graph_corpus.py --check
```

Zwölf neue Regressionen sichern Tickpositionen, Instrumenttrennung,
Einmalzuordnung, Velocitygrenzen, verbotene Backbeatfenster, exakte
Gleichzeitigkeit, inklusive Toleranzgrenzen, Quellentausch und gesperrte
Statusaufwertungen. Die Gegenrechnung verwendet Einzelspur-Ticks und exakte
Bruchzahlen für lokale Phasen; derselbe Mido-Parser ist eine gemeinsame
Abhängigkeit. 51.200 boolesche Einzelvergleiche stimmen überein. Ein anfänglicher
Float-Grenzunterschied bei1,1 Vierteln wurde mit exakter Bruchrechnung
untersucht; inklusive Fenstergrenzen sind jetzt auch bei normalisierten
Eingaben konsistent. Rohdaten und vollständige lokale Prüfprotokolle bleiben unter
`Auditnachweise-2026-11-15/funk-originale/` außerhalb von Git.

Vorher/Nachher: zwei weitere Korpusfälle besitzen jetzt konkrete Drum-
Komponenten; eine ältere Artikelprosa ist neu direkt zugeordnet.
Alle14 historischen Korpusbehauptungen bleiben OPEN; Graph41 begrenzte
Stichproben/1FAIL/55OPEN, sechs historische Definitionslücken und27 Benchmark-
Pflichtfälle bleiben bestehen. CDR-010 bleibt FAIL. Neue unabhängige
Fachvollabnahmen: **0**. Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen,
CSS-Rechte samt Archivzuordnung und Sicherheitsfreigaben **OFFEN**.
Gesamtaudit **NICHT ABGESCHLOSSEN**; keine automatische Integration in main.

## Abschlussvalidierung des lokalen Pakets

391 Kerntests und36 Skilltests bestehen;23 zusätzliche Integritäts-/Generator-
prüfungen bestehen. Der Benchmark bleibt92PASS/0FAIL/27PENDING, Exit1 ist
wegen fehlender Pflichtnachweise erwartet und kein uneingeschränktes PASS.
1.048 interne Links in170 Markdown-Dateien geprüft: keine neuen aktiven
Fehler,25 bekannte eingefrorene Archivfehler. Rohmessung erneut identisch
reproduziert. Historische97 Kanten, Golden-Originale und Secret-Baseline
wurden nicht verändert.

Der erste Gesamtlauf erkannte die nach dem Quellenupdate noch veraltete
58-Kanten-Folgematrix. Nach Neuberechnung bestehen Gesamtlauf und Generator-
prüfungen. Rote Erstprotokolle bleiben in `validation/`, der korrigierte Lauf
in `validation-final/`. Abschließender Vollscan, exakter Commit und Remote-CI
werden im lokalen Abschlussnachweis und PR getrennt dokumentiert.

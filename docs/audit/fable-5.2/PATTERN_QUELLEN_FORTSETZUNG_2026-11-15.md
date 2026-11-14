# Pattern- und Quellenfortsetzung nach dem autorisierten Push

Der geprüfte Audit-Commit `0c21191bd71f9aaa6c13b2647a33321d19fbb3d3`
wurde auf ausdrücklichen Auftrag nach GitHub gepusht. Remote-Branch
`codex/audit-abgleich-pattern-20261114` und lokale Revision wurden verglichen.
Die Basis `main` war weiterhin `cda6cb99bf3d4c6bc1bde29c4ffef1405a117c0f`.
Kein Merge, kein Force-Push und keine Historienänderung.

## Nachweisvalidator korrigiert

Bei der weiteren Patternprüfung wurde ein technischer Fehler reproduziert:
Der Validator prüfte Anzahl und Einzigartigkeit der 24 Aufnahmen, aber weder
deren konkrete Identität noch ihre MIDI-Quelldateihashes. Eine fremde ID bei
gleichbleibender Anzahl und ein ausgetauschter Hash wurden zuvor akzeptiert.
Das war ein Validierungsfehler; es wurde kein tatsächlicher Austausch in der
versionierten Beobachtung festgestellt.

Jetzt werden alle sechs RWC- und 18 Jazz-IDs samt ihren MIDI-Hashes gegen die
bestehenden Komponentennachweise abgeglichen. Boolesche Werte gelten nicht
als Taktnenner; eine Beobachtung mit null Takten darf keine Tempoangabe oder
versteckte Zählung enthalten. Vier neue Regressionen sichern diese Grenzen.
Die 24 ursprünglichen Messzeilen und ihre Ergebnisse sind unverändert.
Die Offline-Prüfung sichert die interne Beweiskette. Ein gemeinsames Verändern
aller Dateien wird dadurch nicht zu einer kryptografisch signierten externen
Quellenauthentifizierung; dazu dient die getrennte Originalreproduktion.

## Drum-Quellen weiter untersucht

Über die offizielle [PyPI-Veröffentlichung](https://pypi.org/project/jazzsamba/)
wurde zusätzlich das Loader-Paket JazzSAMBA **0.1.1** statisch untersucht:
17.105 Bytes, SHA-256
`0f417a587adb6ec831eb4c4920614cc92b82d7467f970b1238e75891ffaa2b79`,
gegen die veröffentlichte PyPI-Prüfsumme bestätigt. Das Paket wurde weder
installiert noch ausgeführt oder in Git übernommen.

`jazzsamba/constants.py` Zeilen 85–87 bestätigt die Unterscheidung zwischen
asynchronem Original-Drum-MIDI und den anderen Lieferarten;
`jazzsamba/stem.py` Zeilen 89–106 unterscheidet Original/AMT/derived bei der
Dateiauswahl. Die gelesenen Python-Dateien enthalten keinen gefundenen
Drum-Notennummernplan. Eine zusätzliche Suche nach deklarierten Mapping- und
Hardwarebegriffen ergab ebenfalls keinen Treffer. Das ist auf diese konkrete
Lieferung und diese Suchbegriffe begrenzt, kein Nichtexistenzbeweis für alle
Hardwareunterlagen.

Die Herkunft der MIDI-Spur ist damit erneut auf Quellenebene gestützt,
die Zuordnung etwa von Note45 oder51 zu einem tatsächlich gespielten
Ride-Instrument bleibt offen. Die MIT-Lizenz des Loaders ist keine
Rechtefreigabe für Datensatz, Kompositionen, Audio oder CSS.
Die [strukturierte Quellenprüfung](PATTERN_QUELLEN_NACHPRUEFUNG_2026-11-15.json)
nennt Lieferung, Fundstellen und Aussagegrenzen.

## CDR-019: Editionsfrage präzisiert, keine Originalseite fingiert

Die öffentliche [Reily-Verlagsseite](https://www.cambridge.org/core/journals/popular-music/article/abs/tom-jobim-and-the-bossa-nova-era/D61EFEFEF21863C86C31477EDCD12FF9)
bietet weiterhin Auszug und Referenzen mit Zugangshinweis, nicht die benötigte
S.5/Fig.1. Ihre Referenzliste belegt Cabral Band2 S.10–17 bibliografisch.
Sie nennt Schreiner **1992**, während der historische Projektkatalog
die **1993er** Ausgabe führt. Das erfordert einen Vergleich von Titelblatt,
Impressum, ISBN und Seitenzählung; keine der Jahreszahlen wurde stillschweigend
ersetzt. Der Distributorabruf war mit403 gesperrt, ein Bibliothekskatalog bot
eine JavaScript-/Robotprüfung; keine Zugriffssperre wurde umgangen.

Weiter erforderlich sind berechtigte Originalseiten von Reily1996,
Cabral Band2, Garcia1999 und der konkret identifizierten Schreiner-Ausgabe.
CAPH4195N bleibt eine Beschaffungsspur für Garcias Dissertation1998.
**Null ältere Originalseiten wurden neu als inhaltlich verifiziert eingestuft.**

## Prüfung und weiterhin offene Grenzen

333 Kerntests und36 Skilltests bestehen. Die15 Rastertests umfassen nun die
vier neuen Negativfälle. Alle18 zusätzlichen Integritäts-/Generatorprüfungen
bestehen; die lokalen Einzelprotokolle und der abschließende Vollscan
liegen unter `Auditnachweise-2026-11-15/pattern-quellen/`.
Der Wissensbenchmark bleibt92 PASS/0 FAIL/27 PENDING; Exit1 wegen Pflichtnachweisen.
Die Messungen zu REL-001/REL-005 werden nicht als Instrument-, Genre- oder
Häufigkeitsabnahme umgedeutet. Alle14 Korpusbehauptungen bleiben OPEN.
Graph97/41 begrenzte Stichproben/1 FAIL/55 OPEN, CDR-010 weiterhin FAIL.

Fach-, Hör-, Spiel-, Didaktik- und Coach-Abnahmen, CSS-Bundle-Rechte samt
dauerhafter Archivzuordnung und Sicherheitsfreigaben bleiben **OFFEN**.
Gesamtaudit **NICHT ABGESCHLOSSEN**. Dieser Bericht erweitert den bestehenden
Evidenzindex; das lokale OA-Register bleibt der einzige Aufgabenmaster.

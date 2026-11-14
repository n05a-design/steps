# Nacht-Audit: Secret-Scanner-Gegenprüfung

Basis: `5d2d09cfba22fa137ef65da5ffcc31bcadf5194a`.

Zwei reproduzierte Schutzlücken sind korrigiert: Teilzeichenfolgen wie
`.git` schlossen auch `.github` aus; `re.search` erfasste pro Muster und
Zeile nur den ersten Treffer. Verzeichnisnamen werden jetzt exakt
ausgeschlossen, Auditarchive mitgescannt und alle Treffer geprüft.
Die GitHub-Action verwendet denselben getesteten Scanner statt einer
zweiten, abweichenden Inline-Implementierung.

Der erweiterte Scan findet **48 quarantänisierte historische, vier erlaubte synthetische und sechs
zusätzliche Vorkommen**. Die sechs zusätzlichen Vorkommen haben denselben
AWS-Key-Fingerprint und stehen bytegleich bereits im Basiscommit.
Sie sind weder neue Einfügungen des Nacht-Branches noch als harmlos
bestätigt. Keine Schlüsselwerte wurden in diesen Bericht übernommen.
Die [strukturierten Befunde](NACHT_SECURITY_BEFUNDE_2026-11-14.json)
nennen ausschließlich Pfade, Zeilen, Hashes und den Ausgangscommit.

**Scanstatus: FAIL wegen sechs nicht freigegebener historischer Funde.**
Die bestehende Baseline wird nicht automatisch erweitert. Rechteinhaber
beziehungsweise zuständige Kontoinhaber müssen die Schlüssel prüfen und
gegebenenfalls sperren/ersetzen; die Projektverantwortlichen müssen die
Behandlung vorhandener öffentlicher Archivkopien festlegen. Eine
quarantänisierte Ausnahme wäre keine Sperrung oder Bereinigung des
Schlüssels. History-Rewrite, Löschen der historischen Beweise und
verdecktes Redigieren wurden nicht vorgenommen.

Regressionen prüfen den zweiten Treffer desselben Musters sowie Treffer
unter `.github`, `Auditpakete`, `StepsAudit` und Namen mit `.git` als
Teilzeichenfolge. Die vorhandenen 15 Tests und die drei neuen
Gegenproben bestehen. Ein grüner Unit-Test hebt den roten Bestandsscan
nicht auf.

```sh
python -B -m unittest discover -s tests -p 'test_secret_scanner.py'
python -B scripts/pre-commit-secret-check.py --scan-all
```

Die frühere Scanner-Summe 52 vermischte 48 historische und vier erlaubte synthetische Treffer. Die Zählung ist getrennt; ein eigener Regressionstest verhindert die Vermischung.

## Nachtrag: Sicherheitskorrektur und Golden-Fortsetzung

Die vorstehenden roten Sicherheitswerte dokumentieren den früheren Prüfstand. Die [vollständige Bereinigung](SECRET_GUARDRAIL_166_2026-11-14.md) schließt auch 15 zusätzliche Vorkommen in zuvor übergangenen Dateitypen ein; GitHub-Lauf #168 besteht. Die [Fortsetzung über alle 64 Golden-Beispiele](GOLDEN_64_QUELLENPRUEFUNG_2026-11-14.md) enthält den aktuellen Stand. Historische Protokolle bleiben erhalten.

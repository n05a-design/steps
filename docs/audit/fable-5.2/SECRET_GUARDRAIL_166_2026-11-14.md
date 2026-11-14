# Sicherheitskorrektur – Secret Scanning Guardrail #166

Stand: 14.11.2026. Ausgangscommit `349e343b1405543ceb7810d16720827b9d9d3afe`; separater Arbeitsbranch `codex/security-guardrail-166-20261114`. Kein Merge nach main.

## Ursache und vollständige Bestandsprüfung

Der fehlgeschlagene [Lauf #166](https://github.com/n05a-design/steps/actions/runs/43551564219) meldete 48 quarantänisierte und sechs blockierende Vorkommen. Die [strukturierte Evidenz](SECRET_GUARDRAIL_166_EVIDENCE.json) enthält alle 69 Vorkommen, 38 Dateipfade, Zeilen und ausschließlich SHA-256-Fingerprints; keine Schlüsselwerte.

Die sechs Ableton-Artikel enthalten dieselbe gültig Base64-dekodierbare JPEG-Datei (JPEG-Signatur und Abschlussmarker geprüft). Darin liegen zwei unterschiedliche Zeichenfolgen, die zufällig dem AWS-Access-Key-ID-Muster entsprechen. Beide erscheinen in jedem der sechs Artikel. Der ältere Scanner betrachtete nur den ersten Treffer pro Muster und Zeile. Die bestehende Baseline bindet deshalb nur dessen Fingerprint. Die Korrektur auf `finditer` deckte den zweiten Treffer auf; dieser kollidiert mit demselben Baseline-Schlüssel aus Pfad, Zeile und Musterklasse. Die Fehlerklasse beschreibt diesen Vergleich, keinen nachgewiesenen Austausch eines Zugangsschlüssels. Die zunächst zwölf AWS-Mustervorkommen werden anhand ihres eindeutig abgegrenzten JPEG-Kontexts als Bilddaten-False-Positives bewertet. Keine neue Scanner-Ausnahme wurde eingeführt.

Die übrigen 42 Baseline-Vorkommen sind drei unterschiedliche Google-Browser-API-Schlüssel in gespeicherten Web-/YouTube-Assets: 30, sechs und sechs Wiederholungen. Öffentliche Browser-Verfügbarkeit beweist weder Geheimhaltung noch harmlose Berechtigungen. Nutzung, Einschränkungen, Gültigkeit und Eigentümerfreigabe wurden nicht mit fremden Zugangsdaten geprüft und bleiben offen.

Die 33 Baseline-Einträge sind nicht mit der Vorkommenszahl gleichzusetzen: Mehrfachtreffer derselben identischen Google-Zeichenfolge erklären weitere Wiederholungen. Sämtliche 48 bisher quarantänisierten Vorkommen wurden erfasst: sechs Bilddaten-Treffer und 42 Google-Schlüssel.

## Zusätzlich entdeckte Dateityp-Lücke

Eine unabhängige byteweise Prüfung aller 4.305 damals versionierten Dateien fand 15 zusätzliche Vorkommen außerhalb der bisherigen Dateiendungsliste: sieben Google-Schlüssel in endungslosen JavaScript-Downloads und acht AWS-Mustervorkommen in vier SVG-Dateien. Auch diese SVGs enthalten exakt dasselbe JPEG. Insgesamt wurden 20 Bilddaten-False-Positives und 49 Google-Schlüsselvorkommen in 38 Dateien bereinigt. Es gibt weiterhin drei unterschiedliche Google-Fingerprints; die endgültigen Häufigkeiten stehen maschinenlesbar in der Evidenz.

Der Scanner prüft nun sämtliche Dateien statt einer begrenzten Endungsliste; die bestehenden Verzeichnisausschlüsse bleiben unverändert. Eine neue Regression verlangt Erkennung in endungslosen Dateien, SVG, TOML und Binärdaten. Das ist eine Verschärfung der Abdeckung, keine Ausnahme für grüne CI.

## Bereinigung und Quellenerhalt

In sechs Artikeldateien und vier SVG-Dateien wurde ausschließlich das betroffene Inline-JPEG durch einen dokumentierten fragmentbasierten Platzhalter ersetzt. Die Bilddarstellung entfällt; die Originalquelle bleibt über den Artikelverweis zugänglich. In 28 zugehörigen Web-Asset-Dateien wurden ausschließlich die 49 Google-Schlüsselwerte durch `REDACTED_THIRD_PARTY_GOOGLE_API_KEY` ersetzt. Artikeltext, übriges HTML, Quellen- und Medienreferenzen bleiben außerhalb dieser Payloads unverändert.

`verify_secret_remediation.py` rekonstruiert die zulässigen Ersetzungen aus unveränderlichen historischen Git-Blobs, prüft jeden Vorher-/Nachher-Hash, die JPEG-Identität und die vollständige Vorkommensliste. Git-LF und Windows-CRLF werden getrennt dokumentiert und für plattformübergreifende Prüfung normalisiert. Die historische Baseline, Erkennungsmuster und Fixture-Allowlist bleiben unverändert; die Dateiabdeckung wurde erweitert. Baseline-Fingerprints werden nicht auf die neuen Vorkommen erweitert.

## Historische Exposition und verbleibende Sicherheitsfreigabe

Die Dateihistorie wurde für jeden der 38 Pfade mit Verfolgung der früheren Verzeichnisnamen geprüft: 76 historische Pfad-/Revisionskombinationen in zwei Commits, `b42a990` und `a14c3f3`. Keine zusätzlichen Schlüssel-Fingerprints wurden in diesen Fassungen gefunden. Die Schlüssel bleiben in der vorhandenen Git-Historie und möglicherweise in Forks, lokalen Kopien, PR-Diffs und Server-Caches rekonstruierbar. Es gab keinen History-Rewrite und keine Verwendung oder Rotation fremder Zugangsdaten.

**OFFEN:** Ein autorisierter Sicherheitsverantwortlicher muss Eigentümer, Einschränkungen und möglichen Missbrauch der drei Google-Schlüssel bewerten; erforderlichenfalls dürfen ausschließlich Berechtigte sperren/rotieren und über einen gesondert autorisierten historischen Bereinigungsplan entscheiden. Gelöschte Remote-Refs und externe Kopien sind nicht vollständig erfasst. Der begrenzte Vier-Muster-Scanner ist kein Beweis für die Abwesenheit aller denkbaren Credential-Typen. Menschliche Sicherheitsfreigabe bleibt OFFEN.

Die [AWS-Dokumentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/id_credentials_access-keys.html) unterscheidet Access-Key-ID und Secret-Access-Key. Die [Google-Empfehlungen](https://docs.cloud.google.com/docs/authentication/api-keys-best-practices) und [Einschränkungsregeln](https://docs.cloud.google.com/api-keys/docs/add-restrictions-api-keys) begründen die konservative Behandlung der browserseitigen Werte. Es wurden keine Berechtigungen aus bloßem Dateibesitz abgeleitet.

## Reproduzierbare Validierung

- `python -B scripts/pre-commit-secret-check.py --scan-all`: nach Bereinigung 0 quarantänisierte / 0 neue Treffer, Exit 0.
- `python -B scripts/verify_secret_remediation.py`: 38 Dateien, 69 ursprüngliche Vorkommen, 0 verbleibende Vorkommen; unveränderte Baseline.
- 19 Scanner-Regressionstests einschließlich der erweiterten Dateiabdeckung bestanden; sechs zusätzliche Regressionen prüfen vollständigen Payload-Erhalt, fehlende Fundstellen, manipulierte Baseline-/Bild-Hashes und fingierte Sicherheitsfreigabe sowie Linux-LF-/Windows-CRLF-Kompatibilität.
- Referenzintegrität: Exit 0, weiterhin 198 Golden-Beispiele und 97 Originalkanten.
- Skilltests: 36 bestanden.

Der erste Gesamt-Testlauf während der Erstellung des Evidenzschemas scheiterte an drei fehlenden Metadatenfeldern. Dieser Entwicklungsfehlstand wird nicht als bestandene Prüfung gewertet; endgültige Gesamtprüfung und Remote-CI werden nach dem Commit separat ergänzt.

Fach-, Hör-, Spiel-, Didaktik- und Coach-Abnahmen sowie CSS-Bundle-Rechte bleiben OFFEN. Ein grüner Secret-Scan schließt diese Abnahmen und die historische Sicherheitsbewertung nicht.

Endgültige lokale Gegenprüfung nach Erweiterung der Dateiabdeckung: 201 Kerntests bestanden; anschließend wurde zusätzlich die plattformübergreifende LF-Regression ergänzt und gezielt geprüft. Unabhängige Prüfung aller 4.305 zuvor versionierten Dateien: 0 unautorisierte Muster, vier zugelassene Fixture-Vorkommen. Der letzte Stand des vollständigen Secret-Scans lautet 0/0, Exit 0. Remote-CI ist zum Zeitpunkt dieses Sicherheitscommits noch nicht neu gelaufen.

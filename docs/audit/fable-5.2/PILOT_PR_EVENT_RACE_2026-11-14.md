# Nachlaufender PR-Check nach externem Merge von PR #60

PR #60 wurde am14.11.2026 um16:09:33UTC durch `timvontrostorff` in `main` gemergt. Mergecommit: `a9f0faed1aec26f85255f6c42a9b0912dce2abdf`; Implementierung: `dacffa31ddbbb485cee77a69ffc8483b6bf575cd`. Der Dateibaum des Mergecommits entspricht exakt dem geprüften Implementierungsstand.

Der später gestartete [Pilot-Eventlauf](https://github.com/n05a-design/steps/actions/runs/43614054942/job/132505131411) scheiterte um16:09:46UTC mit `fatal: couldn't find remote ref refs/pull/60/merge`, Exit128. Das flüchtige PR-Merge-Ref existierte nach dem externen Merge nicht mehr. Dieser rote historische Lauf wird nicht als bestanden umgeschrieben. Der vorherige PR-Lauf war erfolgreich; die anschließenden main-Läufe Python#170, Secret#183, Struktur#321 und Pilot#156 waren ebenfalls erfolgreich. Dies sind verschiedene geprüfte Ereignisse.

## Begrenzte Korrektur

Der [Resolver](../../../scripts/resolve_pilot_review_revision.py) versucht zunächst das bisherige Merge-Ref. Nur nach dessen Fetch-Fehler darf ein frischer API-Nachweis desselben PRs eine Alternative liefern: PR-Nummer, geschlossener/gemergter Zustand sowie Base- und Head-SHA müssen exakt dem Event entsprechen. Der echte Mergecommit wird separat geladen und muss genau die beiden erwarteten Eltern in der richtigen Reihenfolge besitzen. Bei offenen, ungemergt geschlossenen, veränderten, nicht erreichbaren oder abweichend gemergten PRs bleibt das Gate geschlossen. Squash-/Rebase-Merges werden dadurch nicht neu freigegeben.

Der Workflow lädt den Resolver und den eigentlichen Evidenzprüfer weiterhin aus dem vertrauenswürdigen Base-Checkout. Die Zielrevision liefert ausschließlich Daten; PR-Code wird nicht ausgeführt. Statusberechtigungen, eigentliche Evidenzprüfung und Fach-/Rechtefreigaben werden nicht erweitert. Authentifizierte Fehlermeldungen oder API-Payloads werden nicht ausgegeben.

## Gegenprüfung

Acht [Regressionstests](../../../tests/test_pilot_review_revision.py) prüfen das vorhandene Ref, den exakten abgeschlossenen Merge, falsche PR-/Base-/Head-Identitäten, offene/ungemergte PRs, fehlende API-Antworten, vertauschte/falsche Eltern und abweichende geladene Objekte.

Zusätzlich wurde der tatsächlich verschwundene Merge-Ref von PR #60 erneut angefragt. Nach dessen Fehler wurde die frische PR-API gelesen und der reale Mergecommit geladen; die Eltern `d734fef579d0b921d64a96de35b7702c034ef088` und `dacffa31ddbbb485cee77a69ffc8483b6bf575cd` wurden exakt verglichen. Dieser technische Nachweis ist im lokalen Übergabeordner als `pilot-race-live-reproduction.json` erhalten. Die eigentliche Pilot-Evidenzprüfung wird danach weiterhin separat ausgeführt.

Beim ersten lokalen Versuch scheiterte der depth2-Abruf des vorhandenen Windows-Checkouts an `mmap failed: Invalid argument`. Ein normaler Abruf desselben Objekts gelang; der lebende Fallback-Nachweis verwendet deshalb diesen Abrufmodus. Das ist keine identische Ausführung des frischen Linux-Runners. Der Fehler wird nicht als erfolgreicher erster Versuch ausgegeben und es wurden keine Objekte gelöscht oder Historien umgeschrieben. Die separate Prüfung der echten main-Revision bestätigt die acht bereits vorhandenen Pilotfreigaben; sie erteilt keine neue Abnahme dieses Audits.

Der vollständige lokale Lauf besteht mit287 Kern- und36 Skilltests. Der Benchmark bleibt92 PASS/0 FAIL/27 PENDING mit erwartetem Exit1. Die übrigen Integritäts- und GitHub-Prüfungen werden im Übergabenachweis festgehalten.

Diese Korrektur ist ein technischer Folgefund des Korpuspakets. Sie ist keine menschliche Fachabnahme und schließt keine der14 Korpusbehauptungen, Quellenoriginale, CSS-Rechte oder Sicherheitsfreigaben. Das Gesamtaudit bleibt nicht abgeschlossen. Die vollständigen Test-/CI-Ergebnisse und die Integration dieses Folgepakets werden im Git-Übergabenachweis dokumentiert.

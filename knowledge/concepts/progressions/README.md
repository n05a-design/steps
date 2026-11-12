# Progressionen und Pilotfreigabe

PROG-001, PROG-003 und PROG-009 sind die drei Pilotbeispiele.
Die [Kandidaten](../../../src/steps/progression/reviewed_progressions.json)
enthalten acht einzeln identifizierte Aussagen mit Typ, Wortlaut,
Gültigkeitsbereich, Gegencheck und konkreter Fundstelle im
[Produktquellenregister](../../sources/registry.yaml).
Der [Bestandskatalog](CHORD_PROGRESSION_REFERENCE_LIBRARY.md) dient der
allgemeinen Progressions-API und bleibt als Forschungs- und
Kompatibilitätsbestand erhalten.

## Menschliche Fachabnahme

Eine fachkundige Person prüft je Aussage Wortlaut, Gültigkeitsbereich,
Gegencheck und Fundstelle. Sie hält im GitHub-Review oder PR-Kommentar
die freigegebenen Claim-IDs mit ihren vollständigen Fassungsfingerabdrücken
fest. Der folgende Befehl zeigt den Review-Stand aus dem aktuellen Checkout.

```sh
python -B -m src.steps.progression.reviewed --review-manifest
```

Nach belegter Abnahme wird für jede freigegebene ID ein Eintrag im
[Freigaberegister](../../../src/steps/progression/reviewed_progression_approvals.json)
ergänzt. Die Felder sind `fingerprint`, `reviewer` (GitHub-Konto),
`reviewed_on` (ISO-Datum) und `evidence_url` (Permalink zum Review oder
Kommentar). Beim Code-Review des Registereintrags sind Konto, Beleg
und im Beleg genannter Fingerabdruck zu vergleichen. Die lokale
Validierung prüft das Register und die Form des Permalinks offline.
Die Prüfung, wer die Erklärung tatsächlich abgegeben hat, erfolgt
beim Review auf GitHub.

Der Fingerabdruck bindet die Freigabe an Text, Typ, Gültigkeitsbereich,
Gegencheck, Quellenmetadaten, Fundstellen und die Daten des betreffenden
Beispiels. Die Schreibkonvention ist eine Abhängigkeit aller Beispielaussagen.
Eine Änderung an einer einzelnen Aussage lässt die übrigen Freigaben
gültig, soweit deren eigene Daten und Abhängigkeiten unverändert bleiben.

## Veröffentlichung

Erst nach allen acht gültigen Freigaben werden die drei Beispiele
gemeinsam zugänglich. App-Adapter, Renderer und CI verwenden denselben
Validator. Nach Eintrag der belegten Freigaben das
[Lernmaterial](REVIEWED_PROGRESSIONS.md) erzeugen und prüfen.

```sh
python -B scripts/render_reviewed_progressions.py
python -B scripts/render_reviewed_progressions.py --check
```

Der erzeugte Datenversionswert erscheint im App-Objekt und im Lernmaterial.
Bei fehlenden Quellen, Platzhaltern oder ungültigen Freigaben beendet sich
der Renderer vor dem Schreiben. Die CI-Prüfung für die Veröffentlichung
bleibt bis zur vollständigen Abnahme und Regeneration gesperrt.

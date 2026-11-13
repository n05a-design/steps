# Progressionen und Pilotfreigabe

PROG-001, PROG-003 und PROG-009 sind die drei Pilotbeispiele.
Die [Kandidaten](../../../src/steps/progression/reviewed_progressions.json)
enthalten acht einzeln identifizierte Aussagen mit Typ, Wortlaut,
Gültigkeitsbereich, Gegencheck und konkreter Fundstelle im
[Produktquellenregister](../../sources/registry.yaml).
Die Belegkette für die Pilotbeispiele verwendet die folgenden Claim-IDs.
Die Quellenkennungen und Fundstellen stehen in den Kandidatendaten.

| Beispiel | Claims | Fachliche Quellenkennungen |
| --- | --- | --- |
| PROG-001 | PROG-001-HARMONY, PROG-001-TONAL-CENTER | omt-roman-numerals, omt-four-chord-schemas, mto-richards-axis-progressions |
| PROG-003 | PROG-003-HARMONY, PROG-003-VOICE-II-V, PROG-003-VOICE-V-I | omt-ii-v-i |
| PROG-009 | PROG-009-HARMONY, PROG-009-VOICE-LEADING | omt-blues-based-schemas |

`PILOT-NOTATION-001` verwendet `yale-key-names` für alle drei Beispiele.
Die Bestandsrelationen REL-003 bis REL-005 beschreiben mögliche Klavier-
und Drum-Zuordnungen zu PROG-003. Ihre Verwendung als Empfehlung braucht
eine eigene fachliche Prüfung. PROG-009 benötigt für die Pilotlektion
keine zusätzliche Graphkante.

Der [Bestandskatalog](CHORD_PROGRESSION_REFERENCE_LIBRARY.md) dient der
allgemeinen Progressions-API und bleibt als Forschungs- und
Kompatibilitätsbestand erhalten.

## Menschliche Fachabnahme

Die [Abnahmeliste](../../benchmark/PILOT_ABNAHME.md) enthält je Aussage
Wortlaut, Fingerabdruck, Fundstelle, Gegencheck und Prüffrage mit Sollantwort.

Eine fachkundige Person prüft je Aussage Wortlaut, Gültigkeitsbereich,
Gegencheck und Fundstelle. Sie dokumentiert jede Freigabe mit `STEPS-APPROVED <claim-id> <fingerprint>`
in einem GitHub-PR-Kommentar. Die vorhandenen Pilotbelege behalten ihre Formate. Der folgende Befehl zeigt den Review-Stand aus dem aktuellen Checkout.

```sh
python -B -m src.steps.progression.reviewed --review-manifest
```

Nach belegter Abnahme wird für jede freigegebene ID ein Eintrag im
[Freigaberegister](../../../src/steps/progression/reviewed_progression_approvals.json)
ergänzt. Die Felder sind `fingerprint`, `reviewer` (GitHub-Konto),
`reviewed_on` (ISO-Datum) und `evidence_url` (Permalink zum PR-Kommentar). Beim Code-Review des Registereintrags sind Konto, Beleg
und im Beleg genannter Fingerabdruck zu vergleichen. Anschließend die
[Abnahmeliste und Abdeckungsmatrix](../../benchmark/README.md) aktualisieren. Die lokale
Validierung prüft das Register und die Form des Permalinks offline.
Der [Online-Prüfer](../../../scripts/verify_pilot_review_evidence.py) prüft
zusätzlich GitHub-Konto, Kommentar und Fingerabdruck. Der Katalog prüft die
Übereinstimmung der Stufen, Akkordsymbole und Halbtonpfade.

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

# Pop-Pattern und Originalquellen nach PR #77

## Geprüfte Basis und abgegrenzte Fortsetzung

PR #77 wurde extern mit `4feb3dbae07dd5575b46a4f65d74ba748bda64ff`
gemergt. Der saubere Checkout wurde gegen GitHub verifiziert und der neue
Branch `codex/audit-pattern-pop-20261115` beginnt auf diesem main.
Die beiden Ride-/Dynamikstellen aus #77 bleiben unverändert dokumentiert.
Dieses Paket bearbeitet zusätzlich die Pop-Patternfrage zu REL-001/CR-029.

## Tatsächliche Messung statt weiterer Annahmen über PAT-001

Alle GMDv1.0.0-Aufnahmen mit primärem Stil `pop`, `beat_type=beat` und
`time_signature=4-4` wurden aus der bereits publisher-hashgeprüften Lieferung
selektiert: **15 Performances, vier Drummer,306 vollständige Takte**.
Die Auswahl ist identisch zur früheren begrenzten GMD-Pop-Komponente, jetzt
werden aber zusätzlich Snare-/Hat-Originalnoten und die Synkope geprüft.
Dateien mit `beat_type=fill` sind ausgeschlossen; interne Variationen oder
Fills in langen Beat-Performances besitzen hier keine eigene Segmentannotation.
Metadaten-Tempi:83,132,138 und142BPM; keine
stillschweigende Umrechnung auf die115BPM-Katalogangabe.

REF-0030 liefert bereits den Projekt-Tickanker1320/480PPQ für „3e+“.
Wie der Klammerzusatz von PAT-001 die Kick auf Schlag3 ergänzt oder ersetzt,
ist damit noch nicht fachlich entschieden. Deshalb gibt es zwei klar
getrennte **Prüfvorschläge**:

- **Zusatz:** Kick auf nullbasierten Viertelpositionen0,2 und2,75.
- **Verschiebung:** Kick auf0 und2,75, ausdrücklich keine Kick nahe2.

Keiner ersetzt die historische Katalogdefinition. Zusätzlich bleiben
Original-Hat42 und die vom GMD-Herausgeber dokumentierte Closed-Hat-Familie
42/22 getrennt. Die Paper-Sammelklasse wird nicht mit den Originalnoten
gleichgesetzt. Snare38 wird nicht stillschweigend durch Rim40 oder X-Stick37
ersetzt. [Herausgeber-Mapping](https://magenta.tensorflow.org/datasets/groove#drum-mapping).

| Taktweise Teilprüfung | ±0,04 Viertel | ±0,1 Viertel |
| --- | ---: | ---: |
| Kick36 auf1 und3 | 8 | 11 |
| Kick-Zusatzraster mit REF-0030-Synkope | 0 | 0 |
| Verschobenes Kickraster ohne Kick auf3 | 0 | 0 |
| Original-Snare38 auf2 und4 | 19 | 38 |
| Original-Hat42 auf allen Achteln | 0 | 4 |
| Closed-Hat-Familie42/22 auf allen Achteln | 0 | 11 |
| Gemeinsames Zusatz- oder Verschiebungsraster mit Snare und Hat | 0 | 0 |

Die [vollständige Beobachtung](GMD_POP_PATTERN_2026-11-15.json) bindet alle
15 IDs, Dateihashes, Metadaten und Nenner an den vorhandenen Quellennachweis.
Das Ausbleiben gemeinsamer Treffer gilt ausschließlich für die gewählten
Raster, diese kontrollierten Performances und die deklarierten Toleranzen.
Es ist keine Widerlegung einer allgemeinen Pop-/Rock- oder Harmoniekopplung.
GMD enthält für diese Aufnahmen keine Akkordannotation und keine repräsentative
Songstichprobe; REL-001 und CR-029 bleiben OPEN.

Eine wichtige Negativregel wird getestet: Bei einem verbotenen Schlag kann
eine größere Toleranz einen zuvor akzeptierten Verschiebungskandidaten
verwerfen. Daher werden solche Muster nicht fälschlich als monoton behandelt.
Positive Teilraster ohne Verbotsbedingung behalten ihre Monotonieprüfung.

## CDR-019: neuer Originalartikel-Kandidat, keine fingierte Inhaltsprüfung

Die [USP-Verlagsseite](https://revistas.usp.br/celeuma/en/article/view/68015)
identifiziert Walter Garcias **Radicalismos à brasileira**, Celeuma1(1),2013,
S.20–31, DOI10.11606/issn.2318-7875.v1i1p20-31. Das ist ein eigenes Werk
dieses Autors, kein Ersatz für das weiterhin benötigte Bim-Bom-Buch von1999.
Nur die Publikationsmetadaten wurden gelesen.

Die [Zugriffsmatrix](CDR019_GARCIA2013_ZUGRIFF_2026-11-15.json) hält die
konkreten Grenzen fest:

- Die sprachneutrale Artikelseite löste die anfangs fehlerhafte Locale-
  Weiterleitung auf und zeigte die bibliografischen Angaben.
- Der verlinkte PDF-Viewer lief in ein Timeout. Zwei reguläre Downloadwege
  lieferten nur unvollständige Übertragungen; der erste wurde nach ausbleibendem
  Fortschritt abgebrochen, der zweite erreichte die explizite Operationsfrist.
- Eine begrenzte öffentliche Range-Probe scheiterte ebenfalls an der
  Verbindung; kein erfolgreicher Content-Range-Beleg und keine rekonstruierte
  Gesamtdatei. Keine Authentifizierung oder Umgehung.
- Die beiden Teildateien (15.892 und65.044 Bytes) bleiben lokal als `.partial`
  erhalten. Ihre Hashes sind ausdrücklich **Teildateihashes**, keine Hashes
  vollständiger Originale. Der Parserversuch an einer unvollständigen Datei
  ist kein Nachweis eines beschädigten Verlagsoriginals.

**Keine neue Originalseite wurde als gelesen oder visuell geprüft markiert.**
Der Text dieses Artikels ist nicht inhaltlich verifiziert. Weiter erforderlich
sind die ursprünglichen Reily-/Cabral-/Garcia1999-/Schreiner-Fundstellen und
die dokumentierten Editionsvergleiche. Die bisherigen Sperren werden nicht
durch immer gleiche Abrufe umgangen oder als gelöste Quellenfälle ausgegeben.
Volltexte, PDF-Teildateien und Bilder wurden nicht in Git übernommen.

## Reproduktion und technische Gegenprüfung

```powershell
python -B scripts/audit_gmd_pop_pattern.py --check
python -B scripts/audit_gmd_pop_pattern.py --gmd-zip <lokales-GMD-ZIP> --check
python -B -m unittest discover -s tests -p 'test_gmd_pop_pattern.py'
python -B scripts/audit_graph_corpus.py --check
```

Acht neue Regressionen sichern Zusatz/Verschiebung, Verbotsbedingung,
Original-/Familieninstrumente, positive Kandidaten, Quellenaustausch und die
gesperrte Statusaufwertung. Die unabhängige technische Gegenrechnung über
direkte Einzelspur-Ticks und lineare Ereignisfenster bestätigt **6.120
boolesche Einzelvergleiche**. Mido-Parser gemeinsam; keine menschliche
Fachabnahme. Die normale CI braucht keine Roh-MIDIs oder neue Laufzeitpakete.

Die vollständigen lokalen Prüfprotokolle liegen unter
`Auditnachweise-2026-11-15/pop-originale/validation/`; Teildateien und
Gegenrechnung außerhalb von Git im übergeordneten Nachweisordner.
Historische97 Kanten, Golden-Originale und Secret-Baseline bleiben erhalten.
Alle14 Korpusbehauptungen, sechs historische Definitionslücken und27
Benchmark-Pflichtfälle bleiben offen. Graph41 begrenzte Stichproben/1 FAIL/
55 OPEN; CDR-010 bleibt FAIL. Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen,
CSS-Rechte samt Archivzuordnung und Sicherheitsfreigaben **OFFEN**.
Gesamtaudit **NICHT ABGESCHLOSSEN**. Das lokale OA-Register bleibt Aufgabenmaster.

## Lokale Abschlussvalidierung

379 Kerntests und36 Skilltests sowie22 zusätzliche Integritäts-/Generator-
prüfungen bestehen. Der Benchmark bleibt92 PASS/0 FAIL/27 PENDING mit
begründet erwartetem Exit1.1044 interne Links in169 Markdown-Dateien sind
geprüft, keine neuen aktiven Fehler;25 bekannte Archivfehler bleiben erhalten.
Die erneute Originalmessung stimmt mit dem versionierten Befund überein.
Vollständiger abschließender Secret-Scan und Remote-CI werden mit der exakten
Revision im lokalen Abschlussnachweis getrennt gesichert.

# Pattern-Synkope und Originalquellensuche nach PR #71/#72

## Ausgangsstand

PR #71 ist mit `e7d483b60dfd2e6b41e109eaceb2fbdd8f9dbe3c` und PR #72
mit `69627ec7f7ec7fadd02046a32d5d8c400a637d6a` extern gemergt.
Die saubere Arbeitskopie wurde vor Änderungen gegen GitHub geprüft und ein
neuer Branch `codex/audit-pattern-originale-20261115` von diesem main angelegt.
Keine alten lokalen Änderungen überschrieben, kein Merge oder Rewrite.

## Übersehenen Timinganker gefunden und tatsächlich gemessen

Die frühere Aussage, zu PAT-001s „3e+“ fehle ein eindeutiger Projekt-Tickwert,
war zu weitgehend. Der erhaltene historische Golden-Fall **REF-0030** nennt
bereits **1320 Ticks bei480 PPQ**, also nullbasiert **11/4 Viertel**.
Er steht in `knowledge/research/golden_cases/golden_reference_cases.json` und
wird im Golden-Mirror sowie im bestehenden Timingtest nachvollzogen.
Dies ist ein Projektbeleg; seine Verknüpfung mit PAT-001 wird als expliziter
Querverweis dokumentiert, nicht als unabhängige Stilabnahme.

`scripts/audit_pattern_syncopation.py` bindet sich an Case-ID und Case-Hash
dieses Originals und misst die zuvor ausgelassene Kick-Synkope aus derselben
hashgebundenen RWC-Lieferung. Alte14.11.-Messungen und ihr damaliger Umfang
bleiben unverändert. Der neue Nachweis steht separat in
[PAT001_SYNKOPE_2026-11-15.json](PAT001_SYNKOPE_2026-11-15.json).

| Beobachtung in sechs RWC-Stücken /64 eindeutigen vollständigen Takten | ±0,04 lokale Viertel | ±0,1 lokale Viertel |
| --- | ---: | ---: |
| Kick35/36 nahe der REF-0030-Synkope | 0 | 8 |
| Kick35/36 auf1,3 und der Synkope | 0 | 1 |
| Keine weiteren Kick35/36-Ereignisse bei diesem Kickraster | 0 | 0 |
| Gemeinsames Kickraster plus Snare38 auf2/4 und Hat42 auf allen Achteln | 0 | 0 |

Die unterschiedliche Trefferzahl zeigt die Toleranzabhängigkeit. Eine ideale
Triolenposition bei2+2/3 liegt nur1/12 Viertel vom Ziel2,75 entfernt: Die alte
Toleranz0,1 kann sie einschließen, die engere0,04 trennt die idealen Positionen.
Ein eigener Positiv-/Negativtest belegt das. Daraus folgt nicht, dass sämtliche
acht breiten Treffer tatsächlich Triolen sind; dafür fehlen eigene
Performance-/Messfehlerbelege. Die engere Schwelle ist eine ausgewiesene
Sensitivitätsanalyse, keine fachlich genehmigte Quantisierungsnorm.

Instrumentmapping,115BPM-Identität, Dynamik, tatsächliche Audioausrichtung,
Genre und repräsentative Häufigkeit bleiben offen. Die gemeinsame Paarung wird
weder bestätigt noch widerlegt. REL-005 behält seinen getrennten begrenzten
Notenrasterbefund; eine häufige native Note wird nicht als Ride umbenannt.

Eine getrennte technische Gegenrechnung prüfte alle sechs Quelldateien mit
Sekundeniterator statt eigener Tick-/Temporekonstruktion und direkter
Intervallsuche statt Bisektion: **512 boolesche Einzelvergleiche** stimmen
überein. Der Mido-Parser ist gemeinsam; das ist keine unabhängige Fachabnahme.

Zusätzlich wurde die gesamte Jazz-Abteilung derselben Lieferung inventarisiert:
**50 MIDI-/Beat-Paare, null Jazz-Harmonie-CSVs**, ein ausdrücklich als Swing
markierter Datensatz **RWC_J038**. Der
[Inventarnachweis](RWC_JAZZ_INVENTAR_2026-11-15.json) hält den Auswahlrahmen fest.
Eine lokale explorative Prüfung seiner94 vollständigen Takte liefert keine
vollständige51/44-Kernrasterpaarung. Ohne Harmonieannotation und authentifizierte
Instrumentzuordnung wird daraus kein gemeinsamer REL-005-Nachweis. Andere
RWC-Jazz-Stücke ohne explizites Swing-Label werden nicht nachträglich als
Swing-Sampling-Rahmen ausgegeben.

## CDR-019: Originalzugänge erneut bis zur Evidenzgrenze geprüft

Die [strukturierte Abrufmatrix](CDR019_ORIGINAL_RETRIEVAL_2026-11-15.json)
trennt fünf Quellenzugänge und ihre konkreten Grenzen:

- Der [Academia-Autorenbeitrag](https://www.academia.edu/5555299/Tom_Jobim_and_the_bossa_nova_era)
  liefert im direkt lesbaren Abruf nur Archiv-/Copyrightinformationen; die
  benötigte Originaldarstellung von S.5/Fig.1 fehlt.
- Der dadurch zugeordnete [JSTOR-Eintrag931201](https://www.jstor.org/stable/931201)
  liefert keinen lesbaren fachlichen Haupttext. Kein Login, Kauf oder
  Umgehen einer Zugriffssperre.
- Der bekannte Cabral-Kandidat bleibt ein Inhaltsverzeichnis; er wurde nicht
  erneut als angeblicher Volltext geladen. Weiter benötigt: Band2 S.10–17,
  besonders S.12, mit nachvollziehbarer Sprach-/Ausgabenzuordnung.
- Schreiner1992 wird im Bibliotheks-Suchindex genannt; das klärt nicht den
  Originalseitenbezug zur1993er Projektausgabe. Der anonyme Google-Books-
  Metadatenabruf schlug fehl; kein API-Schlüssel beschafft oder verwendet.
- Garcia1999 bleibt als berechtigte Originalausgabe erforderlich. Die bekannte
 1998er Dissertation unter CAPH4195N und der2023er Autorenbeitrag werden nicht
  mit ihr gleichgesetzt.

**Keine ältere Originalseite ist neu als inhaltlich geprüft markiert.** Die
historische Herkunftsthese wird nicht aus Rhythmusähnlichkeit oder der
Existenz bibliografischer Datensätze abgeleitet. Fremde Volltexte/Bilder
bleiben außerhalb von Git. Ein weiterer offizieller AIST- Quellenabruf schlug
technisch fehl; daraus wurde ebenfalls keine gelesene Quellenabnahme gemacht.

## Reproduktion und offene Abnahmen

```powershell
python -B scripts/audit_pattern_syncopation.py --check
python -B scripts/audit_pattern_syncopation.py --rwc-archive <lokales-RWC-ZIP> --check
python -B -m unittest discover -s tests -p 'test_pattern_syncopation.py'
python -B scripts/audit_graph_corpus.py --check
```

Die Quellenmessung benötigt das vorhandene Auditpaket Mido; CI prüft den
versionierten Befund offline. Neun neue Regressionen sichern die Position,
Triolenabgrenzung, gemeinsame Muster, Provenienz und Toleranzmonotonie.
Die lokalen Abschlussprotokolle liegen unter
`Auditnachweise-2026-11-15/synkope-originale/`.

Alle14 Korpusbehauptungen bleiben OPEN; die historische Graphbilanz bleibt
97 Kanten/41 begrenzte Stichproben/1 FAIL/55 OPEN, CDR-010 bleibt FAIL.
Sechs historische Definitionslücken,27 Benchmark-Pflichtfälle, Fach-/Hör-/
Spiel-/Didaktik-/Coach-Abnahmen, CSS-Rechte samt Archivzuordnung und
Sicherheitsfreigaben bleiben **OFFEN**. Gesamtaudit **NICHT ABGESCHLOSSEN**.
Das bestehende lokale OA-Register bleibt die einzige Aufgabenautorität.

## Abschlussvalidierung

- 342 Kerntests und36 Skilltests bestanden, darunter neun neue Regressionen.
- 19 zusätzliche Integritäts-/Generatorprüfungen erfolgreich.
- Wissensbenchmark92 PASS/0 FAIL/27 PENDING, Exit1 wegen offener Pflichtnachweise.
- 986 interne Links in166 Markdown-Dateien geprüft; keine neuen aktiven Fehler,
 25 bekannte historische Archivfehler bleiben erhalten.
- Quellenmessung separat reproduzierbar; die ursprünglichen Golden-Fälle,
 97 historischen Kanten und Secret-Baseline wurden nicht verändert.

Remote-CI und genaue Commit-/PR-Zuordnung werden im lokalen Abschlussnachweis
festgehalten; ein lokaler Testlauf wird nicht als bereits erfolgter Remote-Test
oder Fachfreigabe dargestellt.

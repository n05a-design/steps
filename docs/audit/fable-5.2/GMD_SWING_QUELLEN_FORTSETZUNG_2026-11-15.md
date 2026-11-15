# Swing-Pattern und Editionsnachweis nach PR #73

## Tatsächliche Basis

PR #73 wurde extern mit `e9d15dd6291e9bd420d042fee2998f07fc511b0b`
gemergt. GitHub und die saubere lokale Arbeitskopie wurden vor Änderungen
abgeglichen; der neue Branch `codex/audit-swing-quellen-20261115` beginnt dort.
Die Ergebnisse aus #73 einschließlich REF-0030 werden nicht erneut implementiert.

## Eine bisher offene Quellinstrumentzuordnung begrenzt belegt

Die [Originaldokumentation des Groove MIDI Dataset](https://magenta.tensorflow.org/datasets/groove#drum-mapping)
enthält einen ausdrücklichen Tabellenvergleich der verwendeten Roland-TD-11-
Belegung mit GM und der vereinfachten Paper-Belegung. Für diese Quelle sind
51 als Ride-Bow und44 als Pedal-Hi-Hat dokumentiert;53 und59 sind weitere
Ride-Spielweisen. Das ist eine gegen die Herausgebertabelle geprüfte
Quellendeklaration, keine unabhängige Hörabnahme.

Die Zuordnung wird ausschließlich auf GMD angewendet. Sie authentifiziert
keine Notennummern in RWC oder JazzSAMBA. Auch die vereinfachte Paper-Belegung
wird nicht mit den Originalereignissen verwechselt: Sie fasst Spielweisen
zusammen und legt die Pedal-Hi-Hat in eine andere Sammelklasse.

## Tatsächlich ausgeführte Swing-Messung

Die bereits lokal vorhandene GMDv1.0.0-MIDI-Lieferung wurde erneut gegen den
veröffentlichten SHA-256-Wert geprüft. Vorab ausgewählt wurden sämtliche
Datensätze mit `style=jazz/swing`, `beat_type=beat`, `time_signature=4-4`:
**11 Performances, zwei Drummer,702 vollständige Takte**. Untersucht wird das
Klick-/Viertelraster ab Tick0; keine Harmonieannotation oder kommerzielle
Songpopulation. Alle Splits werden für dieses Audit gemeinsam betrachtet,
nicht für eine behauptete Modell-Evaluation.

| Komponente / Anzahl Takte | ±0,04 Viertel | ±0,1 Viertel |
| --- | ---: | ---: |
| Originalnote51 auf allen Vierteln | 8 | 21 |
| Ride-Familie51/53/59 auf allen Vierteln | 8 | 23 |
| Originalnote44 auf2 und4 | 58 | 214 |
| Gemeinsame Originalnoten51/44-Komponenten | 2 | 12 |
| Gemeinsame Ride-Familien-/Pedalkomponenten | 2 | 13 |

Die enge Originalnotenprüfung liefert zwei konkrete Prüfstellen:

| Aufnahme | Nullbasierter Takt | Ticks bei480PPQ | Metadaten-Tempo |
| --- | ---: | --- | ---: |
| drummer1/session3/2 | 75 | 144000 bis145920, Ende exklusiv | 185BPM |
| drummer10/session1/3 | 1 | 1920 bis3840, Ende exklusiv | 215BPM |

Die [generierten Prüfstellen](GMD_SWING_PRUEFSTELLEN_2026-11-15.csv) binden
Aufnahme, Originaldateihash und Tickposition und lassen die menschliche Abnahme
AUSSTEHEND. Es wird jeweils die erste enge Originalnoten-Prüfstelle pro
Performance ausgegeben. Für eine Abnahme sind Original-MIDI samt Kontext
einzusehen und bei berechtigtem Zugriff mit dem zugehörigen TD-11-Syntheseaudio zu
vergleichen. Es wurde kein Audio heruntergeladen oder stellvertretend abgehört.

Die [maschinenlesbare Gesamtmessung](GMD_SWING_PATTERN_2026-11-15.json) enthält
alle elf Aufnahmen, ihre Quellenhashes, Nenner und Toleranzvarianten. Ein eigener
Validator bindet die konkrete Auswahl statt nur ihre Anzahl. Originalnoten
und Familienaggregation bleiben getrennt. Eine Gegenrechnung über direkte
Einspur-Ticks und gerundete Viertel-Slotmengen bestätigt **7.020 boolesche
Einzelvergleiche**. Der Mido-Parser ist gemeinsam; keine unabhängige Fachabnahme.

Diese Teilmuster belegen weder vollständiges PAT-012 noch130BPM-Identität,
Swing-Verhältnis, Feathering/Dynamik oder die Kopplung an PROG-003. Die beiden
engen Kandidaten liegen ausdrücklich bei185/215BPM. Zusätzliche Ereignisse
sind bei den Teilmusterprüfungen erlaubt. Separate Harmonie-/Drumdatensätze
werden nicht nachträglich zu einer gemeinsamen Performance verbunden.
REL-005 und alle14 historischen Korpusbehauptungen bleiben deshalb OPEN.

## CDR-019: konkrete Ausgabe zum Beschaffen eingegrenzt

Ein neu gelesener [Open-Library-Katalogdatensatz](https://openlibrary.org/books/OL22283469M)
nennt für Schreiner: **Marion Boyars1993, ISBN071452946X,306 Seiten,
Übersetzung Mark Weinstein**. Die Antwort wurde lokal mit Größe und Hash
gesichert. Der [strukturierte Editionsnachweis](CDR019_EDITION_ANCHOR_2026-11-15.json)
trennt diese Metadaten von Originalseiten. Der zusätzliche DNB-SRU-Abruf
schlug technisch fehl und liefert keinen weiteren Inhaltsbeleg.

Reilys1992er Literaturangabe wird nicht stillschweigend auf1993 umgeschrieben.
Titelblatt, Impressum, Ausgabe und tatsächliche Herkunftsaussage müssen weiter
am Original verglichen werden. Ein Katalogdatum klärt weder Seiteninhalt noch
die kausale Tamborim-/Surdo-These. **Null ältere Originalseiten wurden neu
inhaltlich verifiziert.** Reily1996 S.5/Fig.1, Cabral Band2 S.10–17 insbesondere
S.12 sowie die dokumentierten Garcia1999-Seiten bleiben erforderlich.
Die bereits dokumentierten gesperrten Zugänge wurden nicht in Endlosschleifen
wiederholt; kein Login, Kauf, Kontakt oder Umgehen von Zugriffssperren.

## Reproduktion, Rechte und Prüfgrenzen

```powershell
python -B scripts/audit_gmd_swing.py --check
python -B scripts/audit_gmd_swing.py --gmd-zip <lokales-groove-v1.0.0-midionly.zip> --check
python -B -m unittest discover -s tests -p 'test_gmd_swing.py'
python -B scripts/audit_graph_corpus.py --check
```

Die optionale Originalmessung nutzt das vorhandene Auditpaket Mido; normale
CI prüft Metadaten und Regressionen offline. Acht neue Tests prüfen unter
anderem Original-/Familienabgrenzung, falsche Instrumentnoten, Taktgrenzen,
Quellenaustausch und unzulässige fachliche Statusänderungen.

350 Kerntests und36 Skilltests sowie20 zusätzliche Integritäts-/
Generatorprüfungen bestehen.991 interne Links in167 Markdown-Dateien sind
geprüft, ohne neue aktive Fehler;25 bekannte historische Archivfehler bleiben.
Die Einzelprotokolle und Remote-CI-Zuordnung stehen im lokalen Abschlussnachweis
unter `Auditnachweise-2026-11-15/gmd-swing-originale/`.
Der Benchmark bleibt92 PASS/0 FAIL/27 PENDING mit erwartetem Exit1.
Roh-MIDIs und Audio werden nicht in Git übernommen; die GMD-Zuordnung und
CC-BY4.0-Datenlizenz ersetzen weder andere Quellenrechte noch CSS- oder
Sicherheitsfreigaben. Quelle: Google LLC; Gillick et al., Learning to Groove
with Inverse Sequence Transformations,2019.

Historische97 Kanten, Golden-Originale und Secret-Baseline bleiben erhalten.
Graph41 begrenzte Stichproben/1 FAIL/55 OPEN; CDR-010 bleibt FAIL.
Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen, CSS-Bundle-Rechte samt
Archivzuordnung und Sicherheitsfreigaben **OFFEN**. Gesamtaudit
**NICHT ABGESCHLOSSEN**. Das lokale OA-Register bleibt die Aufgabenautorität.

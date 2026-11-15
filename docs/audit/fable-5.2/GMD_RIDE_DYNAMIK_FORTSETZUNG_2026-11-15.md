# Ride-Zwischenanschläge und MIDI-Dynamik nach PR #74

## Geprüfte Basis und Arbeitskontext

PR #74 wurde extern mit `ca69c16998b1e74e717ce7ede55208e3b4b172b5`
gemergt. Während der Prüfung kamen PR #75 (Markenassets) und #76
(Projektseite) hinzu. Die finale Basis ist deshalb
`7c8d73a1bd55a23b3ae6d4cb9bfdca0d4f4f33a9` auf dem Branch
`codex/audit-ride-dynamik-20261115`. Der eigene Auditpatch wurde auf diese
neue Basis übertragen; Markenassets und Projektseite bleiben erhalten.
Der vorbereitende Commit `6e3498fc3873a37108415230990c5dd96db8043e`
bleibt auf seinem früheren Auditbranch erhalten; kein Rewrite oder Force-Push.
Die elf GMD-Swing-Performances und deren Auswahl wurden nicht neu definiert;
dieses Paket untersucht die zwei bereits belegten engen Prüfstellen genauer.

Der zusätzlich eingefügte Tätigkeitsbericht zu zehn Buchzusammenfassungen
wurde als Kontext berücksichtigt. Das genannte lokale Fable-Prüfpaket samt
Gesamtübersicht existiert; der Bericht und sein Hash sind lokal verzeichnet.
Die berichtete Einarbeitung bleibt eigene Vorarbeit dieses anderen Pakets.
Dessen Zusammenfassungen und Sicherungen wurden hier nicht verändert oder
als neue Fachabnahmen gewertet. Die aktuelle Aufgabe betrifft GMD und CDR-019.

## Tatsächliche Ride-Zwischenintervalle

`scripts/audit_gmd_swing_detail.py` liest die zwei durch Quellhash und Takt
gebundenen Original-MIDIs. Jeweils auf Schlag2 und4 werden die tatsächlichen
Ride-Bow-Viertelanschläge innerhalb±0,04 Metronomvierteln lokalisiert.
Nur bei eindeutigen Endpunkten und genau einem strikt dazwischenliegenden
positiven Note-on wird ein Intervallverhältnis berechnet. Fehlende Endpunkte,
fehlender Zwischenanschlag und mehrdeutige Anschläge erhalten getrennte
Statuswerte. Note-ons mit Velocity0 gelten nicht als Anschläge.

| Quelle / nullbasierter Takt | Abschnitt | Erstes/zweites Intervall in Ticks | Tatsächliches Verhältnis |
| --- | --- | --- | ---: |
| drummer1/session3/2 /75 | Schlag2→3 | 338/151 | 2,2384 |
| dieselbe Quelle | Schlag4→nächster Taktanfang | 317/171 | 1,8538 |
| drummer10/session1/3 /1 | Schlag2→3 | 349/139 | 2,5108 |
| dieselbe Quelle | Schlag4→nächster Taktanfang | 324/157 | 2,0637 |

Die vollständigen Brüche und Werte stehen im
[maschinenlesbaren Detailbefund](GMD_SWING_DETAIL_2026-11-15.json).
Vier deskriptive Intervallmessungen sind keine universelle Swing-Norm oder
Bestätigung einer historischen Prozentzuschreibung. Beim zweiten Abschnitt
darf der nächste Taktanfang ausschließlich als zeitlicher Endpunkt dienen;
er wird nicht als zusätzlicher Anschlag im aktuellen Takt gezählt.

Die vorherigen 51/44-Teilrasterkandidaten besitzen damit tatsächlich
Ride-Zwischenanschläge. Die Zeitschwankungen werden erhalten, statt sie auf
eine feste Triolenposition zu quantisieren. Tempo185/215BPM und die zwei
ausgewählten Takte sind keine130BPM-Identität oder repräsentative Population.

## Was die Dynamikdaten belegen

| MIDI-Beobachtung im aktuellen, halb offenen Takt | drummer1/Takt75 | drummer10/Takt1 |
| --- | --- | --- |
| PAT-012-Originalnote35 auf Viertelpositionen | 0 von4 | 0 von4 |
| Herausgeberzugeordnete GMD-Kick36 auf Viertelpositionen | 2 von4 | 0 von4 |
| Positive Kick36-Anschläge im Takt | 2 | 0 |
| Kick36-Velocity: Minimum/Median/Maximum | 86 /94,5 /103 | keine Werte |
| Ride51-Velocity: Minimum/Median/Maximum | 40 /54 /82 | 46 /62 /127 |
| Pedal44-Velocity: Minimum/Median/Maximum | 70 /71 /72 | 57 /58,5 /60 |

Die [Herausgebertabelle](https://magenta.tensorflow.org/datasets/groove#drum-mapping)
bezeichnet GMD-Note36 als Kick. Sie wird getrennt von der historischen
PAT-012-Originalnote35 geführt; keine stillschweigende Umbenennung.
Auch mit der rollenbezogenen GMD-Kick ist an diesen zwei Stellen kein
durchgehendes Viertel-Kickraster nachgewiesen.

MIDI-Velocity ist keine akustische Lautheit. Andere Instrumente und Patches
können andere Anschlags-/Klangkennlinien haben. Deshalb gibt es weder einen
erfundenen Schwellenwert für „sehr leise“ noch eine positive oder negative
akustische Feathering-Abnahme allein aus diesen Zahlen. Eine Prüfung braucht
den gehörten beziehungsweise kalibriert gemessenen Klang und eine unabhängige
Bewertung. Es wurde kein Audio geladen oder stellvertretend hörabgenommen.

## CDR-019: institutionelle Originalspur sauber abgegrenzt

Die neue [Archiv-Prüfmatrix](CDR019_JOBIM_ARCHIV_2026-11-15.json) führt die
Ergebnisse aus dem Jobim-Archiv mit Aussagegrenzen:

- Der Eintrag [2010/8376](https://www.jobim.org/jobim/handle/2010/8376?show=full)
  beschreibt eine Interviewveranstaltung1960, ist laut `dc.type` aber eine
  **Fotografie**, Serie `p11f017`. Der benötigte Artikeltext ist nicht darin
  verifiziert. Das Foto wurde nicht heruntergeladen oder übernommen.
- Die Metadaten verweisen auf den O-Cruzeiro-Artikel vom13.04.1960 mit Kennung
  `pim079` und auf ein anderes Cabral-Buch von1986 S.124. Diese Referenzen sind
  präzise neue Beschaffungsspuren; sie ersetzen nicht Cabral Band2 S.10–17.
- Der Suchtreffer [2010/9164](https://jobim.org/jobim/handle/2010/9164) nennt
  **Mário Cabral**. Eine Identität mit dem benötigten Werk von Sérgio Cabral
  ist damit nicht belegt; Volltextzugriff wurde nicht als erfolgt gewertet.
- Die regulären Archivsuch-URLs zu `pim079` und dem Essaytitel waren über den
  verwendeten Abruf nicht erreichbar. Keine Authentifizierung oder Umgehung.

**Null ältere Originalseiten wurden neu inhaltlich verifiziert.** Weiter
benötigt werden Reily1996 S.5/Fig.1, Cabral Band2 S.10–17 insbesondere S.12,
Garcia1999 an den dokumentierten Seiten und Schreiners tatsächliche Ausgabe
samt Herkunftsaussage. Fototitel, ähnliche Autorennamen und bloße Archiv-
Referenzen werden nicht als gelesene Primärtexte ausgegeben.

## Reproduktion und Gegenprüfung

```powershell
python -B scripts/audit_gmd_swing_detail.py --check
python -B scripts/audit_gmd_swing_detail.py --gmd-zip <lokales-GMD-ZIP> --check
python -B -m unittest discover -s tests -p 'test_gmd_swing_detail.py'
python -B scripts/audit_graph_corpus.py --check
```

Zehn neue Tests sichern eindeutige/mehrdeutige Endpunkte, Zwischenanschläge,
Velocity0, korrekte/endliche Verhältnisse, strikt typisierte Quellenidentität und
die gesperrte akustische Statusaufwertung.
Eine getrennte Rechnung aus der originalen Einzelspur verifiziert vier
Verhältnisse, acht Velocity-Zusammenfassungen und vier Viertel-Präsenzwerte,
insgesamt16 Diagnosevergleiche. Parser gemeinsam; keine unabhängige Fachabnahme.
Die Original-Messung benötigt nur das vorhandene Auditpaket Mido, normale CI
prüft den versionierten Befund offline.

Vollständige technische Prüfung und Remote-CI werden mit Revision/Exitcodes
im lokalen Nachweisordner `Auditnachweise-2026-11-15/ride-dynamik-originale/`
erfasst. Alle14 Korpusbehauptungen bleiben OPEN. Historische97 Kanten und
Golden-Originale unverändert, CDR-010 bleibt FAIL. Sechs Definitionen,
27 Benchmark-Pflichtfälle, Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen,
CSS-Bundle-Rechte samt Archivzuordnung und Sicherheitsfreigaben **OFFEN**.
Gesamtaudit **NICHT ABGESCHLOSSEN**; lokales OA-Register bleibt Aufgabenmaster.

## Lokale Abschlussvalidierung

371 Kerntests und36 Skilltests sowie21 zusätzliche Integritäts-/Generator-
prüfungen bestehen. Die Originalmessung ist erneut reproduziert.
Wissensbenchmark92 PASS/0 FAIL/27 PENDING, erwarteter Exit1.1040 interne Links
in168 Markdown-Dateien geprüft, keine neuen aktiven Fehler;25 bekannte
Archivfehler bleiben dokumentiert. Der abschließende vollständige Secret-Scan
und die Remote-CI-Zuordnung werden im lokalen Abschlussnachweis getrennt
festgehalten. Diese Ergebnisse erteilen keine Fach-/Rechte-/Sicherheitsfreigabe.

Die finale Wiederholungsprüfung auf7c8d73a berücksichtigt die elf zusätzlichen
Marken-/Projektseitentests der neuen Basis. Die frühere360-Test-Prüfung auf
ca69c16 bleibt als separater lokaler Nachweis erhalten; keine rückwirkende
Änderung ihrer Revision oder Ergebnisse. Finale Protokolle liegen im
Unterordner `current-main/` des lokalen Nachweisordners.

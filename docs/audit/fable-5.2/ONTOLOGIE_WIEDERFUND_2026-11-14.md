# Originalontologie wiedergefunden · Windows-Gegenprüfung

Geprüfte Basis: `66117368ec0b677c9bf95293dea01e264bce23ac`.
[PR #53](https://github.com/n05a-design/steps/pull/53) ist seit
14.11.2026, 02:04:43 Europe/Berlin gemergt. Die elf gemeldeten
GitHub-Checks dieses Main-Commits sind erfolgreich.

## Fund und Beweiskette

Der vom Nutzer übergebene Mac-Suchbericht lokalisierte die Ontologie
in seinem untersuchten Bestand nicht und benannte Windows als nächste
Spur. Seine 14 Archive und rund 23.000 Git-Blobs wurden hier nicht erneut
auf dem Mac geprüft. Eine globale Nichtexistenz folgt aus diesem Bericht
nicht. Ebenso bezog sich die frühere Windows-Suche nur auf die damals
benannten Projekt-, Dokument- und Git-Bestände; `AppData/Local/StepsAudit`
war darin noch nicht erfasst.

Die gezielte Windows-Suche fand die gesuchte Datei unmittelbar unter:

```text
%LOCALAPPDATA%/StepsAudit/20261110T2330_Phase4_Master/MUSIC_KNOWLEDGE_ONTOLOGY.md
%LOCALAPPDATA%/StepsAudit/20261111T0105_Phase4_9/MUSIC_KNOWLEDGE_ONTOLOGY.md
```

Die ältere Fassung enthält **90 explizite Mxx-xx-Definitionen**, darunter
**alle 41 bislang fehlenden historischen Graphkennungen**. Ihr SHA-256:
`27194b90681b23cc6b6ee6f49d4f2240190b4e9ec3cf57086accee7c404d54cc`.
Auch die auf dem Mac fehlenden Schwesterdateien zum Genre-Atlas,
Klavier-Lernpfad, Klaviermodulen und Korrekturen liegen dort vor.

Zwölf relevante, projekterzeugte Originaldateien wurden unter
[ontology-recovery-2026-11-14](../../../archive/audit-history/ontology-recovery-2026-11-14/README.md)
bytegleich gesichert. Das Manifest verzeichnet Pfade, Größen und Hashes;
eine lokale `.gitattributes` schützt die Original-Zeilenenden. Die
ursprünglichen Dateien, der lokale Aufgabenmaster und andere Checkouts
wurden nicht verändert. Der historische Generator wurde nicht ausgeführt.

Die drei vom Mac-Bericht genannten Commits wurden lokal gegengeprüft:

- `a4b87f6028399be0a8751ea0cd0fce664047442a` bringt Verweise und den
  nichtkanonischen Aufgaben-Snapshot ein; `%LOCALAPPDATA%` betrifft den
  Aufgabenmaster und beweist für sich keinen Ontologiepfad.
- `88c506a6e08645c72aee3603e2212de2d50b6aca` rekonstruiert den
  Konzeptgraphen. Die nun gefundene ältere Ontologie belegt die
  Definitionstexte; welche Datei der damalige Generator tatsächlich las,
  ist damit noch nicht nachgewiesen.
- `fe6663747250bf73ff28f4b7c591e8cf42f799d0` erweitert den Musikkern;
  sein Commitinhalt liefert selbst keine zusätzliche Originalontologie.

## Historische Definition ist keine heutige Fachfreigabe

[HISTORICAL_NODE_EVIDENCE.csv](../../../knowledge/relations/HISTORICAL_NODE_EVIDENCE.csv)
verzeichnet die 41 wörtlichen Definitionen mit Originalpfad, SHA-256 und
Zeilennummer. Der Namensraum heißt ausdrücklich
`PHASE4_MASTER_20261110`; sämtliche Zeilen bleiben `REVIEW_REQUIRED`.

Das ist wegen erheblicher Versionsunterschiede notwendig: Der Master
nennt M03 Intervalle/Tonleitern, M04 Akkordtheorie, M07 Rhythmik und
M10 Klavierpraxis. Der Phase-4.14-Bericht nennt dagegen unter anderem
M04 Skalen, M07 Stimmführung und M10 Genre-Systeme. Die Phase-4.9-Datei
nutzt wiederum Themenabschnitte ohne die alten Unterkennungen.
Es erfolgt **keine automatische Migration der alten IDs** und keine
Übernahme historischer Statusbehauptungen als heutige Wahrheit.

Der [Validator](../../../scripts/verify_historical_ontology.py) prüft
Originalbytes, exakten Definitionswortlaut, Zeilenanker, Namensraum,
ausstehende Review und Vollständigkeit gegenüber den tatsächlichen
historischen Graphendpunkten. Negative Tests verändern Originalbytes,
Definitionswortlaut, Namensraum oder Reviewstatus. Diese Prüfung bestätigt
Dokumentidentität; die einzelnen theoretischen Aussagen brauchen weiterhin
ihre eigenen Quellen- und Fachprüfungen.

## Die acht übrigen Knoten einzeln bearbeitet

Der wiedergefundene Phase-4.12-Generator führt die CDR-Vorläufer als
Tripel auf. Er ergänzt keine versteckten Definitionen oder Notendaten.
Die folgenden Grenzen gelten daher auch nach dem Originalfund:

| Knoten | Konkreter Fund und Ergebnis | Weiterhin offen |
| --- | --- | --- |
| `MODAL_SHIFT_TO_II7` | Phase-4.10-Latintext beschreibt G7 → Gm7 in F-Dur, also II7 → ii7; der Generator nennt dagegen ein Ziel **TO_II7**. Die Richtung ist widersprüchlich. Historische Benennung bleibt unaufgelöst. | Beabsichtigte Richtung/Bezeichnung fachlich klären und gegebenenfalls separaten Korrekturvorschlag erstellen. Keine stille Umbenennung. |
| `PIANO_MONTUNO_GUAJEO` | Phase-4.10-Latintext nennt synkopierte Oktav-/Terzenbrechungen und 2:3 Son-Clave über Cm–Fm–G7–Fm. Es fehlen konkrete Tonhöhen, Dauern und Onsets einer vollständigen Figur. | Notiertes oder MIDI-Ereignisbeispiel, Quellenabgleich und Spiel-/Hörabnahme. Keine erfundene historische Figur. |
| `BOSSA_BATIDA` | Latintext und P14 zeigen ein STEPS-Begleitmodell. Der ältere Genre-Atlas behandelt nur Pop/House und definiert diese ID nicht. | Gemeinte Gitarren-/Begleitfigur bestimmen und von Cross-Stick- und Klavierübungen abgrenzen. |
| `BRAZILIAN_TAMBORIM_SURDO_SYNTHESIS` | Generatortripel und historische Paraphrasen liefern keine geprüfte Entstehungsquelle. Die rhythmische Ähnlichkeit der Projektübungen ist kein historischer Beweis. | Konkrete historische Primärfundstelle und genaue Reichweite der Herkunftsthese; Schreiner-Zuschreibung nicht neu abgenommen. |
| `SURDO_PULSE` | Latintext/P14 beschreiben ein 4/4-Pendelmodell; sie legen keine bestimmte Samba-enredo-Surdo-Rolle für die 2/4-Kante fest. | Kontext und Rolle, etwa primeira/marcação gegenüber segunda/resposta, mit belastbarer Fundstelle bestimmen. |
| `ACCENT_ON_BEAT_2_IN_2_4` | Das vorhandene 4/4-Bossa-Modell ist kein Beleg für die als PERFORMANCE_NORM gespeicherte 2/4-Samba-Aussage. | Kontextgebundener Quellen- und Aufführungsnachweis. Keine allgemeine Akzentpflicht für alle Surdos. |
| `BASS_FIRST_AURAL` | Vollständige P10-Fassung aus Phase 4.8 gefunden: Bass zuerst, dann Umkehrungscheck, Terz/Oberstimmen und Kontext. Als begrenzte **Projektstrategie** definiert. | Konkrete Höraufgabe, Leistungsmaß und unabhängige Bewertung des Lernerfolgs; keine Coker-Buchseitenabnahme. |
| `LOWEST_PITCH_ANCHOR` | Derselbe P10-Text nennt den tiefsten Ton als ersten Suchhinweis und grenzt C/E, Em und Am/E voneinander ab. Als Projektbegriff definiert, nicht als Universalgesetz. | Empirische Ankerwirkung und didaktische Eignung im benannten Lernkontext. |

Die zwei P10-Begriffe sind in
[MUSIC_NODE_EVIDENCE.csv](../../../knowledge/relations/MUSIC_NODE_EVIDENCE.csv)
als `PROJECT_EXAMPLE` verzeichnet. Das belegt, was das historische Projekt
damit meint, und weder eine richtige Funktionsanalyse jedes Beispiels noch
eine externe Fach-, Hör- oder didaktische Abnahme.

## Aktueller Definitions- und Prüfstand

Von den ursprünglich 74 offenen IDs sind nun **68 Definitionen begrenzt
zugeordnet**: 25 aus PR #53, 41 historische Originaldefinitionen und zwei
P10-Projektbegriffe. **Sechs Definitionen bleiben offen**. Die alten Listen
mit 74 beziehungsweise 49 offenen IDs bleiben als frühere Stände erhalten.

- [Aktualisierte Bearbeitungsliste](GRAPH_KNOTENBEARBEITUNG_NACH_ORIGINALFUND_2026-11-14.csv)
- [Sechs verbleibende Definitionen](GRAPH_RESTKNOTEN_NACH_ORIGINALFUND_2026-11-14.csv)

Die Definitionsermittlung schließt keine Kantenabnahme. Alle 97 Originalkanten
bleiben unverändert, CDR-010 historisch FAIL und dessen Korrekturvorschlag
ohne Produktionsfreigabe. Die Matrix weist weiterhin 14 bestätigte
Stichproben, eine beanstandete Stichprobe und 82 offene Kanten aus;
vollständige Fachabnahmen: null.

Der neue Benchmarkfall prüft ausschließlich die Wiederherstellungsidentität.
Fehlende Fach-, Hör-, Spiel- und Coach-Abnahmen sowie Rechte am vollständigen
CSS-Bundle und dessen dauerhafte Archivzuordnung bleiben ausdrücklich offen.

Reproduzierbare Befehle:

```sh
python -B scripts/verify_historical_ontology.py
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/audit_knowledge_coverage.py --check --details coverage.csv
python -B scripts/verify_reference_integrity.py
```

Eine fehlende menschliche Abnahme wird durch den Fund, einen Hashvergleich
oder einen grünen Test nicht ersetzt.

Lokaler Prüfstand: **178 Kerntests und 36 Skilltests erfolgreich**.
Der Benchmark umfasst jetzt 96 Fälle: **69 PASS, 0 FAIL, 27 PENDING**;
Exit 1 bleibt wegen offener Pflichtfälle erwartet. Coverage `--check`,
Referenzintegrität, Golden-Spiegel (198 Fälle), API-Referenz und
Pilot-Lernmaterial sind erfolgreich geprüft. 754 interne Dateilinks in
136 aktiven README/betroffenen Markdown-Dateien haben keine fehlenden
Zielpfade; Anker, externe Erreichbarkeit und die vollständige historische
Archivnavigation sind davon ausgenommen. Die zwölf im Git-Index
gespeicherten Originale stimmen ebenfalls mit den Manifest-Hashes überein.
Historische Leerzeichen und alte Statusbehauptungen wurden nicht bereinigt.

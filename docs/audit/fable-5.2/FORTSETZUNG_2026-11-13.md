# STEPS · Auditfortsetzung nach PR #50

Geprüfte öffentliche Basis: `93edcb84d892219f4541adaeac9a46212f21a14c`.
Die Bestandsaufnahme wurde am 13.11.2026 nach dem Merge von PR #50
durchgeführt. Der OneDrive-Hauptcheckout wurde weder zurückgesetzt noch
synchronisiert. Änderungen dieser Fortsetzung liegen auf einem eigenen Branch.

## Integration und technische Nachweise

Die Übergabe um 22:49 Uhr ist hinsichtlich der offenen Integrationen überholt:

| PR | Inhalt | Verifizierter Merge auf main |
| --- | --- | --- |
| [#47](https://github.com/n05a-design/steps/pull/47) | Vier Formatknoten mit GM-/MusicXML-Fundstellen | `dee6666495862a26176d73fa03353fc00e70c261` |
| [#48](https://github.com/n05a-design/steps/pull/48) | Zehn Swing-Rechenfälle | `cfb2faceeaa0659a79aa89f084b41feff77aa9f4` |
| [#49](https://github.com/n05a-design/steps/pull/49) | Zwölf Skalen-/Modusfälle | `4c7dac97bcc8a00638229933c7189348f8dc77f7` |
| [#50](https://github.com/n05a-design/steps/pull/50) | Vollständige Aggregation für Claims und Progressionspositionen | `93edcb84d892219f4541adaeac9a46212f21a14c` |

Zum Zeitpunkt der Abfrage: keine offenen PRs und nur `main` als Remote-Branch.
Auf dieser SHA waren folgende vier Workflows abgeschlossen und erfolgreich:

- [Python-Matrix, Skill-Plattformen, Pilot und Wissensabdeckung](https://github.com/n05a-design/steps/actions/runs/43520315086)
- [Repositorystruktur](https://github.com/n05a-design/steps/actions/runs/43520315136)
- [Pilot-Freigabebelege](https://github.com/n05a-design/steps/actions/runs/43520315188)
- [Secret-Scanner](https://github.com/n05a-design/steps/actions/runs/43520315211)

Lokale Wiederholung auf sauberer Basis, Windows/Python 3.14.7:
159 Kerntests und 36 Curation-Skilltests bestanden. Der Benchmark liefert
52 PASS, 0 FAIL und 27 PENDING. Sein Exit 1 ist die erwartete Sperre für
offene Pflichtfälle. Die versionierte Abdeckungsmatrix besteht `--check`.
Ihre formalen Befunde und ungeprüften Inhalte bestehen weiterhin.
Golden-Spiegel, API-Referenz, Referenzintegrität, Struktur,
Pilot-Abnahmeliste und generiertes Lernmaterial bestanden die Prüfungen.

Die Aggregation aus #43/#50 erfasst Klaviermodule, Drum-Pattern,
Forschungsclaims und Progressionspositionen. FAIL hat Vorrang; PASS mit
PENDING bedeutet eine Stichprobe und keine vollständige Fachabnahme.
Die vorhandenen Tests decken die Reihenfolge der Ergebnisse sowie
Positions-PASS mit Progressions-FAIL ab. Es war keine erneute Reparatur nötig.

## Quellengegenprüfung und Grenzen

Die [W3C-pitch-Referenz](https://www.w3.org/2021/06/musicxml40/musicxml-reference/elements/pitch/)
bestätigt die beiden MusicXML-Knotendefinitionen: `pitch` unter `note`
mit `step`, optionalem `alter` und `octave` in dieser Reihenfolge.
Das bestätigt keine beliebige Graphkante.

Die [MIDI-Association-Seite](https://midi.org/general-midi-level-1)
verlinkt weiterhin genau das im Knotenregister benannte GM1-Dokument.
Die PDF-Tabelle war über den verwendeten Webzugriff in dieser Sitzung
nicht lesbar; die zweite Downloadroute lieferte 404. Eine erneute
inhaltliche Abnahme der Tabelle wird hier deshalb nicht behauptet.
Der frühere Tabellenabgleich aus #46/#47 bleibt als historischer Nachweis erhalten.

[Open Music Theory, Collections and Scales](https://openmusictheory.github.io/scales2.html)
bestätigt die Zuordnung der diatonischen Modi, die pentatonische
Tonkollektion und die Ganztonkollektion. Dies ist eine Quellenstichprobe,
keine vollständige neue Abnahme sämtlicher Skalenfälle. Der
[Originalabstract von Friberg und Sundström](https://doi.org/10.1525/mp.2002.19.3.333)
bestätigt tempoabhängige Swingverhältnisse. Er belegt keine individuelle
57-Prozent-Zuschreibung. Dieser Wert bleibt als STEPS-Übungswert ausgewiesen.
Die erneute Titelsuche zu SRC-033 ergab keinen geeigneten bibliografischen
Beleg; daraus folgt kein Nachweis der Nichtexistenz.

## Wiedergefundene CSS-Registerfassung

Die Suche über 6.178 von lokalen Refs erreichbare Git-Objekte fand einen
Blob mit der gesuchten Größe. Dessen SHA-256 stimmt exakt mit dem
historischen Register überein. Der lokale Sicherungsbaum
`5f1dea83c437aa54267e5f2ca9259a196f141852` führt den Blob an allen sechs
Registerpfaden. Die ursprüngliche Zeilenendenhypothese erklärt den
Registerwert nicht: vollständiges LF→CRLF ergibt 64.902 statt 63.332 Bytes.

Der neue [Prüfer](../../../scripts/verify_registered_git_files.py) liest
die Rohblobs und vergleicht Pfad, Größe und SHA-256. Vier neue Tests
prüfen exakte und gemeinsam genutzte Blobs, falsche Größe/Prüfsumme,
fehlende Pfade, Platzhalter, doppelte IDs und fehlende Bäume.
Der [konkrete Lauf](CSS_REGISTER_HASHABGLEICH_2026-11-13.json) ergibt sechs MATCH.
Der CSS-Inhalt wurde ausschließlich lokal gesichert; veröffentlicht
werden Metadaten und Prüfroutine. Externe Herkunft, Rechte und eine
dauerhaft zugängliche Archivzuordnung bleiben offen.

Der Fortsetzungskandidat besteht lokal 163 Kerntests (159 bestehende +
4 neue) und 36 Skilltests. Sein Benchmark bleibt bei 52/0/27; die
Abdeckungsmatrix bleibt unverändert und besteht `--check`.
Eine Pfadprüfung über 134 aktive README-/Berichtsdateien fand bei
743 internen Dateiverweisen keine fehlenden Ziele. Ausgenommen waren
Archiv-READMEs, Glide und das Quellenarchiv. Anker und externe
Erreichbarkeit wurden bei dieser Pfadprüfung nicht bewertet.

## Alle offenen Benchmarkfälle

Die [Einzelfallliste](OFFENE_BENCHMARKFAELLE_2026-11-13.csv) nennt alle
27 IDs mit jeweils konkretem nächsten Schritt. Kein Fall wurde als
Fachabnahme geschlossen. Die sechs CSS-Schritte berücksichtigen den neuen Fund.

| Fälle | Anzahl | Verbleibender Nachweis |
| --- | ---: | --- |
| COACH-01 bis COACH-12 | 12 | Isolierter Lauf mit Modell-/Skillrevision, Rohantwort und menschlicher Quellen-/Kriterienbewertung. Vorhandene Entwürfe ersetzen ihn nicht. |
| KB-M08-METER, KB-M12-PLAYABILITY, KB-M09-LOOP-HEAR | 3 | Hör-/Spielabnahmen zu PAT-031, P02 und den zwei PROG-001-Fassungen. |
| KB-SRC-033-PROVENANCE | 1 | Belastbarer Katalog- oder Originalnachweis für die angegebene Publikation. |
| KB-GRAPH-NODES | 1 | Definition der weiterhin offenen Knoten und fachliche Fundstelle je Kante; vier belegte Formatknoten reichen nicht aus. |
| KB-HISTORY-F00412/F00571/F00704/F00768/F00937/F01002 | 6 | Byteidentität lokal geklärt; Herkunft, Rechte und zugängliche Archivzuordnung fehlen. |
| KB-HISTORY-PPR-MIDI-01 bis -04 | 4 | Originallieferung und Rechtebeleg; das bestehende Inventar der 36 MIDI-Pfade ist keine Herkunftsabnahme. |

Der Benchmark umfasst 79 Fälle. Die Abdeckungsmatrix erfasst deutlich
mehr Inventareinträge; ihre offenen Befunde sind zusätzlich zu beachten.
Insbesondere bleiben alle 97 Graphrelationen fachlich offen. Nach den
vier Formatknoten fehlen 80 eindeutige Endpunktdefinitionen.

## Lokale Vollständigkeit und Bestandsschutz

Im OneDrive-Hauptcheckout steht `main` noch auf
`22f3f5f348d060abfd4e2ffc917d0c95a639441e`. Die detaillierte Inventur
erfasst 1.580 fehlende versionierte Pfade unter `src/glide-v3.53`
(in der Momentaufnahme ein Indexeintrag und 1.579 Arbeitsbaum-Löschungen)
und 1.546 nicht versionierte Dateien: 1.508 unter `src/glide-3.55.1`
und 38 unter `src/GLIDE_STEPS_GESAMTAUDIT_V2_2026-11-10`.
Sie wurden weder entfernt noch pauschal veröffentlicht. Die neue Glide-
Kopie ist damit ausdrücklich kein nachgewiesenes Dateifürdatei-Abbild
des alten Verzeichnisses oder des öffentlichen Referenzstands.

Die drei in der Übergabe genannten lokalen Spitzen sind keine Vorfahren
der geprüften Main-SHA. Ein fehlender Merge ist allein daraus nicht ableitbar:

- `d574acc`: Alle 16 hinzugefügten Dateien sind als identische Git-Blobs
  unter heutigen Archiv-/Dokumentationspfaden auf `main` vorhanden.
- `6194355`: Die beiden exklusiven Commits `44a318d` und `6194355`
  entfernen ausschließlich versehentlich abgelegte Terminalausgaben:
  einen eingefärbten Git-Diffstat und eine `less`-Hilfe. In diesen beiden
  Diffs liegt kein zusätzlicher fachlicher Inhalt zur Übertragung vor.
- `ae374c0`: Historische Lockerung einer Prüfung eines optionalen lokalen
  Produktionsregisters auf mindestens 21 Aufgaben. Die aktuelle Curation-
  Suite hat diese Prüfung durch isolierte Register-/Evidenztests ersetzt.
  Der alte Diff wird daher nicht blind in die heutige Suite übernommen.

Der frühere Audit-Checkout ist für diese Fortsetzung sauber auf die
öffentliche SHA gewechselt worden. Der zweite lokale Audit-Checkout und
die zahlreichen fremden beziehungsweise nicht vorhandenen Worktree-
Registrierungen wurden erhalten. Die macOS-Pfade aus der Übergabe sind
auf diesem Windows-Rechner nicht verfügbar; ihre Restbestände sind damit
nicht als vollständig abgeglichen bestätigt.

## Reproduktion und nächster Schritt

```sh
python -B -m unittest discover -s tests -p 'test_*.py'
python -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
python -B scripts/run_knowledge_benchmark.py --scope all --json-out benchmark.json
python -B scripts/audit_knowledge_coverage.py --check --details coverage.csv
python -B scripts/build_unified_golden_cases.py --check
python -B scripts/render_api_reference.py --check
python -B scripts/verify_reference_integrity.py
python -B tools/validation/check_structure.py
python -B scripts/run_knowledge_benchmark.py --check-review-sheet knowledge/benchmark/PILOT_ABNAHME.md
python -B scripts/render_reviewed_progressions.py --check
```

Als Nächstes den lokalen CSS-Fund dauerhaft archivieren und Herkunft/
Rechte klären, danach die noch fehlenden Graphdefinitionen sowie die
nicht zugänglichen macOS-Restbestände und lokalen Glide-Kopien abgleichen.
Menschliche Abnahmen bleiben bei ihren jeweiligen Fällen separat stehen.
Das Gesamtaudit ist weiterhin offen.

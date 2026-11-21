# Offene Evidenz und historische Bestandsaufnahme

## Fachliche Gesamtfreigabe (21.11.2026)

[Der Gesamtaudit](../../docs/audit/2026-11-21/README.md) belegt offene Fehler
bei Slash-Bass, Akkordreduktion, Drop-2, Stilprofilen und Wissensabruf.
Der Kurations-Skill akzeptiert geänderte musikalische Identitäten trotz
aktiver Baseline. Die strengere Repository-Prüfung erkennt das Gegenbeispiel.
Für die Gesamtfreigabe fehlen 27 Benchmark-Abnahmen, darunter alle zwölf
Coach-Bewertungen. Die acht Pilotfreigaben haben einen engeren Geltungsbereich.
Die [Gegenproben](../../docs/audit/2026-11-21/NACHPRUEFUNG.md) belegen
außerdem falsche Stufen nach Desktop-Transposition und Abweichungen bei
16 der 25 erwarteten Antwortstatus des Knowledge-Skills.

## Ganzheitlicher Bestandsaudit (18.11.2026)

[Der Auditbericht zu Ablage, Recherche, Skills und Wissensbasis](GESAMTAUDIT_ABLAGE_RECHERCHE_SKILLS_WISSENSBASIS_2026-11-18.md)
fasst den geprüften `origin/main`-Stand zusammen. Die formalen Tests bestehen,
aber 27 Benchmarkfälle bleiben offen; 47 PDF-Extrakte sind weiterhin als
`REVIEW_REQUIRED` versioniert. Die Rechte-, Quellen-, Adapter- und
Archivbefunde sind im Bericht mit Aussagegrenzen und priorisierten nächsten
Schritten dokumentiert. Es wurden keine Forschungsdaten oder historischen
Versionen entfernt.

## Nachtstand nach PR #54

[Aktueller Nachtbericht](../../docs/audit/fable-5.2/NACHT_AUDIT_2026-11-14.md)
und [priorisierte Restblocker](../../docs/audit/fable-5.2/NACHT_RESTBLOCKER_2026-11-14.md)
ersetzen keine Fachfreigabe. 97 Kanten einzeln eingeordnet; 38 begrenzte
Stichproben gestützt, CDR-010 beanstandet, 58 weiterhin offen. Sechs
Definitionsvorschläge sind nicht als historische Originaldefinitionen
anerkannt. 27 Pflichtfälle bleiben PENDING. Sechs neu erkannte historische
AWS-Mustervorkommen blockieren den verschärften Secret-Scan; keine
automatische Erweiterung der Baseline. Die folgenden Abschnitte halten
frühere Auditstände fest.

## Originalfund nach PR #53 (14.11.2026)

Unter `%LOCALAPPDATA%/StepsAudit` sind die Originalontologie und ihre Schwesterdateien wiedergefunden. Alle 41 historischen Graphkennungen sind mit Originalwortlaut, Zeile und Hash im eigenen Namensraum zugeordnet. Zwei Bass-/Höranker-Begriffe sind als historische P10-Projektstrategie definiert. Sechs Definitionen bleiben offen; alle fehlenden Fachabnahmen und CSS-Bundle-Rechte bleiben offen. Die spätere Domäneneinteilung ist nicht mit dem historischen Namensraum gleichgesetzt.
[Fundauswertung und Einzelbefunde](../../docs/audit/fable-5.2/ONTOLOGIE_WIEDERFUND_2026-11-14.md).
Am 16.11.2026 hat der Inhaber die Bedeutung von `MODAL_SHIFT_TO_II7` (CDR-012) als II7 → ii7 festgelegt; der Name gilt als historische Fehlbenennung. Die Fachabnahme bleibt offen, ebenso die fünf übrigen Restknoten ([Entscheidung](../../docs/audit/fable-5.2/ENTSCHEIDUNG_CDR012_2026-11-16.md)).
Für CDR-021 hat der Inhaber am selben Tag den Geltungsbereich festgelegt: Akzent auf der Zwei nur für den Surdo de primeira in der Bateria einer Escola de samba, gestützt auf vier neu gelesene Sekundärquellen. Dynamikmessung sowie Fach- und Spielabnahme bleiben offen; CDR-014 und CDR-019 sind unverändert offen ([Entscheidung](../../docs/audit/fable-5.2/ENTSCHEIDUNG_CDR021_2026-11-16.md)).
Ebenfalls am 16.11.2026 hat der Inhaber CDR-014 (Montuno als eigene STEPS-Übung ohne historischen Anspruch) und CDR-019 (Bossa-Batida als Begleitfamilie, Tamborim-/Surdo-These als zugeschriebene Deutung) festgelegt. Damit haben alle sechs Restknoten eine Inhaberentscheidung; Fach-, Spiel- und Hörabnahmen sowie die Beschaffung von Cabral, Garcia 1999 und Schreiner bleiben offen ([Entscheidungen](../../docs/audit/fable-5.2/ENTSCHEIDUNG_CDR014_CDR019_2026-11-16.md)).
Die nachfolgenden Abschnitte dokumentieren frühere Prüfstände.

## Weiterführung nach PR #52 (14.11.2026)

PR #52 ist auf `19f3fee` nach menschlicher Freigabe gemergt. Der neue
Korrekturvorschlag für CDR-010 benennt die exakte sechstönige Sammlung
C6 plus D und F♯. Der ursprüngliche FAIL bleibt erhalten, der Vorschlag
ist nicht fachlich oder für Produktion freigegeben. Nach Bearbeitung
aller bisherigen 74 Restknoten sind 25 Definitionen begrenzt zugeordnet;
49 bleiben offen: 41 historische Mxx-xx-Definitionen und acht
kontext-/abnahmeabhängige Knoten. Die
[Bearbeitung mit Einzelgründen](../../docs/audit/fable-5.2/GRAPH_KLAERUNG_CDR010_2026-11-14.md)
trennt Quellenlesen, Projektbeispiele und eigene Modellrechnung.
Benchmark: 68 PASS, 0 FAIL, 27 PENDING. Keine neue Fachabnahme;
CSS-Bundle-Rechte und dauerhafte Archivzuordnung bleiben offen.

## Fortsetzung vom 14.11.2026

- PR #51 ist nach menschlicher Freigabe auf `9c7b8eb` gemergt.
- Die sechs CSS-Registerfassungen sind über gespeicherte Bandcamp-Player
  bis zur live bytegleichen CDN-Datei technisch zugeordnet. Die bisherige
  Eigenautorschaftsannahme wurde berichtigt; Bundle-Rechte und dauerhafte
  Archivzuordnung bleiben offen. [CSS-Provenienz](../../docs/audit/fable-5.2/CSS_PROVENIENZ_2026-11-14.md).
- Der Graph hat nach sechs zusätzlichen Definitionen noch 74 offene
  Endpunkt-IDs. Drei Kanten haben bestätigte Stichproben; CDR-010 bleibt
  wegen der unbestimmten Polychord-Zuordnung beanstandet. Alle 97 Kanten
  bleiben `REVIEW_REQUIRED`, keine ist vollständig fachlich abgenommen.
  [Graphnachweise](../../docs/audit/fable-5.2/GRAPH_NACHWEISE_2026-11-14.md).
- Der neue Benchmarkstand hat 56 PASS, 0 FAIL, 27 PENDING. Eine bestandene
  Gegenprobe der beanstandeten Graphaussage wird in der Matrix als FAIL
  dieser Aussage geführt. Hör-, Spiel-, Coach- und sonstige offene
  Fachabnahmen werden dadurch nicht geschlossen.

Die folgenden datierten Abschnitte beschreiben frühere Prüfstände.

## Repository-Bestandsaufnahme vom 10.11.2026

- Projektkonsolidierung nennt sechs Originaldokumente, im Originalarchiv liegt derzeit kein `Glide Kontext für Fable(2).md` (5 Markdown-Originale vorhanden); Nachweis/Fundort prüfen. **Erledigt 16.11.2026:** Seit `954cc4c` (11.11.2026) liegen alle sechs Originaldokumente einschließlich `Glide Kontext für Fable(2).md` unter `archive/audit-history/earlier-audits/Gesamtpruefung_V4_mit_Originalquellen_2026-11-10/private_sources/`. Von den zehn Einträgen des historischen Manifests [`HISTORIC_SHA256SUMS.txt`](../../docs/project/provenance/HISTORIC_SHA256SUMS.txt) stimmen neun per SHA-256 überein, teils erst nach Umstellung der Zeilenenden (Glide-Kontext: CRLF, `8349fd43…`). Die Paket-`README.md` (`bd607d59…`) ist im Repository nicht per Hash auffindbar; sie ist eine Begleitdatei, kein Originaldokument.
- Kein ausführbarer `app/`- oder `src/steps/`-Musikcode im analysierten `main`-Baum. **Überholt seit 11.11.2026:** `src/steps/` und `app/` liegen im Repository vor; die offenen Fach- und Grenzwertprüfungen stehen unten unter „Fachprüfung des Progressionskerns“ und „Restprüfung nach dem Fable-Audit“.
- Urheberrechte zahlreicher Fach-PDFs, heruntergeladener Web-Seiten und Drittanbieterbilder offen. **Teilweise eingeordnet 14./16.11.2026:** Siehe [Rechteinventar der Volltext-Extrakte](RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md), [CSS-Provenienz](../../docs/audit/fable-5.2/CSS_PROVENIENZ_2026-11-14.md) und den Abschnitt zur PDF-Konvertierung unten (Klasse E lokal unter `restricted_local` mit eigenen Zusammenfassungen; Klassen A–D und gespeicherte Webseiten auf Inhaberentscheidung weiter versioniert; Einzelrechte und CSS-Bundle-Rechte weiter offen).
- V6.6/V6.7: mehrere Versionen, Fachordner 21 und 39 doppelt benannt; unterschiedliche Struktur-/Zählmodelle. **Erledigt 16.11.2026:** Die [Struktur- und Zählmodellprüfung](../../docs/audit/BIBLIOTHEK_V6_6_V6_7_STRUKTUR_UND_ZAEHLMODELLE_2026-11-16.md) klärt den rechnerischen Zusammenhang aller Indizes von V5.0 bis V6.7 (`1.145 − 148 + 3 = 1.000` Dateien im heutigen V6.6-Ordner; 7 neue URLs aus 30 Kandidaten plus 12 Originalmodule im V6.7-Delta) und belegt, dass `21_AUDIO_EDITING_RESTORATION` / `21_EDITING_RESTORATION` sowie `39_INTEROPERABILITY_FORMATS` / `39_AUDIO_FORMATS_INTEROPERABILITY` keine Datei- oder Inhaltsüberschneidung haben.
- Historische JSON-/CSV-Indizes benötigen Pfad- und Hashrevalidierung. **Teilweise erledigt 16.11.2026:** Das [Bestandsinventar vom 11.11.2026](../../docs/audit/BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.md) ist nachgeprüft; alle 3.947 Zeilen sind wiedergefunden oder erklärt, kein ungeklärter Verlust. Am selben Tag sind 14 weitere Indizes mit Pfad und Hash [nachgeprüft](../../docs/audit/INDIZES_NACHPRUEFUNG_2026-11-16.md) und in der [JSON/TXT-Nachprüfung](../../docs/audit/INDIZES_JSON_TXT_NACHPRUEFUNG_2026-11-16.md) die 14 Navigationsmanifeste analysiert: Auf Repository-Ebene ist alles erklärt. **Offen:** 148 Markdown-Dateien, die die Indizes der V6.6-Bibliothek (V6.0–V6.6) nennen, waren nie im Repository und sind auf diesem Mac nicht auffindbar ([Liste](../../docs/audit/BIBLIOTHEK_V6_6_FEHLENDE_DATEIEN_2026-11-16.csv)). Die erweiterte Mac-Suche (Benutzerverzeichnis, ZIP-Archive) blieb ohne Treffer; für den Windows-Rechner liegt ein [Suchauftrag](../../docs/audit/SUCHAUFTRAG_BIBLIOTHEK_V6_6_WINDOWS_2026-11-16.md) bereit.
- Externe Integration von Glide nur Vorschlag, konkrete Code-/Lizenzübernahme nicht geprüft. **Stand 16.11.2026:** Der frühere Glide-Prototypbestand (1.580 Dateien) wurde bereits am 10.11.2026 mit `37e691b` entfernt ([Bestandsinventar-Nachprüfung](../../docs/audit/BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.md)); im aktuellen `main`-Baum liegt kein Glide-Code. Eine spätere Übernahme bleibt an Lizenz- und Architekturprüfung nach `AGENTS.md` (Regel 9) gebunden.
- Die bestehenden Bibliotheks-Generatoren wurden nicht ausgeführt und ihre Seiteneffekte sind nicht analysiert. **Erledigt 16.11.2026 (statisch, ohne Ausführung):** Die [Analyse](../../docs/audit/GENERATOREN_SEITENEFFEKTE_2026-11-16.md) der 17 Skripte zeigt: kein Löschen, Netzzugriff nur beim Ableton-Indexer; die V6.7-Generatoren überschreiben gleichnamige ZIPs im Arbeitsverzeichnis, fünf V5-Werkzeuge schreiben neben sich ins Repository, mehrere passen nicht mehr zum heutigen Ordneraufbau. `Ordnerliste.py` ist PowerShell.

## Fachprüfung des Progressionskerns (2026-11-11)

- Der App-Katalog umfasst die einzeln geprüften PROG-001, PROG-003 und
  PROG-009. Weitere Beispiele brauchen eine eigene Prüfung und Quellenreferenz.
- PROG-020 und PROG-027 enthalten im Bestandskern vereinfachte Dominanten.
  Für eine Freigabe die konkrete Alterationskombination und die beabsichtigte
  Realisierung ausweisen. Das mehrdeutige Stufensuffix `alt` benötigt dafür
  eine ausdrückliche Interpretation.
- Der Voicing-Solver prüft Tonklassen, Bass, MIDI-Grenzen, Stimmenreihenfolge und
  im strikten Modus parallele Quinten und Oktaven. Eine vollständige
  kontrapunktische Prüfung und stilbezogene Spielbarkeitsprüfung bleiben offen.

## Aufgabenregister nach dem Fable-Audit (2026-11-13)

Der vom Nutzer benannte Repository-Snapshot enthält 33 Aufgaben.
Restore und Rücksicherung wurden mit einer Kopie bytegleich geprüft.
Eine lokale Migrationskopie ergänzt die strukturierten Abschlussbelege
für OA-0002, OA-0011 und OA-0013. Die strikte Validierung besteht.
Die Übernahme in ein produktiv genutztes Register und ein Abgleich mit
etwaigen neueren Einträgen stehen aus. Historische Backups ohne Manifest
bleiben für eine gesonderte Wiederherstellung erhalten.
[Nachweis zur Registermigration](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_QUELLENABGLEICH.md#m2--registermigration-aus-dem-bereitgestellten-snapshot)

## Offene Fachnachweise (Stand 2026-11-13)

- Für [PAT-031](../../knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md) liegen zwei Taktvarianten vor. Die Hörprüfung steht aus.
- Die [Fachnachweise](FABLE_FACHNACHWEISE.md) halten den geprüften Stand für Coach, Latin-Katalog, SRC-033, Graph und historische Dateien fest.
- Für die [198 Golden Cases](../../knowledge/research/GOLDEN_DATA_SOURCE_OF_TRUTH.md#2-bestandsübersicht-phase-415) fehlt eine dokumentierte fachliche Einzelabnahme. Die Test- und Integritätsnachweise liegen vor.

## Restprüfung nach dem Fable-Audit (2026-11-13)

Die [Nachprüfung](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_NACHPRUEFUNG.md)
trennt bestätigte Abweichungen von Konventionsfragen. Die Umsetzung und Abnahme
der Befunde sind im [Maßnahmenplan](../../docs/audit/fable-5.2/STEPS_FABLE_5_2_MASSNAHMENPLAN.md) beschrieben.

| Prüfgebiet | Offene Evidenz und nächster Nachweis |
| --- | --- |
| K01/K03/K06/K07/K10/K13, A01/A02 | Typen, Fehlerhierarchie und Grenzwerte vollständig inventarisieren. 15.312 Layoutkombinationen und fünf konkrete Slash-Bass-Beispiele sind automatisiert geprüft. Die Hör-/Spielbarkeit braucht eigene Abnahmen. Notations-/Moll- und Stilentscheidungen dokumentieren. Zeitmodell und Serialisierung getrennt bewerten. |
| K11, T02/T06 | Auf `7fde80e` sind alle acht GitHub-Freigabebelege und der verpflichtende Online-Check belegt. CI meldet erfolgreiche Läufe für Python 3.11–3.14 und den Skill auf macOS und Windows. Für künftige Freigaben bleiben Quellenrelevanz und menschliches Review erforderlich. |
| S01/S03/S04 | Echtes externes Register nicht verfügbar; End-to-End-Abnahme für Backup/Restore und Registermigration offen. Für zwölf Coach-Fälle liegen Antwortentwürfe vor. Isolierter Lauf, Modell-/Skill-Revision und menschliche Kriterienbewertung stehen aus. |
| W01/W02/W03 | Kanonische Quellen und genaue Fundstellen je Pilotclaim abgleichen. 14 der 35 historisch als VERIFIED bezeichneten Claims lagen außerhalb der Fable-Stichprobe. Alle 66 Einträge mit Evidenzstatus inventarisieren, Buchseiten nur bei berechtigtem Zugriff bewerten. Historische Quellenmetadaten einschließlich der doppelten Titel nach Autor, Ausgabe, Locator und Rechteklasse auflösen. **Nachgeprüft 16.11.2026:** Alle neun lokalen Buch-Fundstellen sind am Original-PDF [gegengeprüft](../../docs/audit/fable-5.2/CLAIM_BUCHFUNDSTELLEN_2026-11-16.md); die acht Pilotclaims, alle 66 Forschungsclaims, die doppelten Titelpaare in `curated_sources_registry.yaml` sowie Autor, Jahr, Herkunft und Lizenzhinweise aller 30 PDFs der Klassen A–D sind im [Quellenmetadaten- und Claim-Bericht](../../docs/audit/fable-5.2/QUELLENMETADATEN_UND_CLAIMS_W01_W03_2026-11-16.md) einzeln aufgeschlüsselt. Menschliche Fachabnahmen und die Beschaffung externer gedruckter Bücher (Kostka/Payne, Levine, Coker, Mauleón-Volltext, Schreiner) bleiben offen. |
| W04 | P01–P19, PAT-001–031 und [Latin-Katalog](../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md) nachprüfen: Akkordtöne/Bass/Rollen, Taktart/Taktgrenzen/PPQ, Eventraster, stilistische Aussagen und ggf. Hörbeleg. PROG-024 ist ein Übungsschema. Die verlinkte Jobim-Partitur belegt die Variante mit ♭II7. **Nachgeprüft 16.11.2026:** In der [Katalog-Stichprobenprüfung](../../docs/audit/fable-5.2/KATALOG_STICHTEST_W04_2026-11-16.md) vollständig aufgeschlüsselt (19 Klaviermodule, 31 Drum-Patterns, 28 Progressionen); 480-PPQ-Metren, Stimmführung und GM-Zuordnung rechnerisch bestätigt; 10 P, 5 PAT und 11 PROG im Benchmark getestet; menschliche Spiel-, Hör- und Groove-Abnahmen bleiben ausstehend. |
| W05/W08 | 97 Relationen stehen auf REVIEW_REQUIRED. Zwei historische Aliasse sind aufgelöst. Für 84 Knoten-IDs fehlt die kanonische Definition. Richtung, Typ, Gültigkeitsbereich und Claim-Bezug je Kante prüfen. Historische Literatur und Pilotprovenienz trennen. |
| W06/W07, T01/T03–T05/T07 | 132 Golden Cases außerhalb der Fable-Stichprobe; auch die 66 Stichprobenfälle brauchen individuelle, versionierte Evidenz. Verbleibende Evaluatorzweige und Fixture-Sollwerte klassifizieren. Die gelesenen Renderer-/Benchmark-/Coverage-Pfade mit Negativkontrollen absichern; Hash-Identität und Generatorgleichheit gelten als formale Nachweise. |
| H01/H02 | Sechs Gegenproben für den OpenAI-Übergabebericht sind dokumentiert. Historische Statuslabel und archivierte Tests bleiben auf ihren Quellstand bezogen. |
| Abnahmebogen A1–A6, B1–B9 (16.11.2026) | Vom Inhaber entschieden, siehe [Abnahmebogen](../../docs/audit/fable-5.2/ABNAHMEBOGEN_2026-11-16.md): 12 freigegeben, A1 und B1 mit Korrektur, B2 mit fehlendem Beleg. **Offen:** A1 Umbenennung des Knotens in `SAME_ROOT_DOMINANT_TO_MINOR_SEVENTH` in `knowledge/relations/` übernehmen; B2 Kap. XIII bei Hindemith (S. 88–90) im Original-PDF sichten; A6 Hörprobe; B1 ist als Deutung nach Konvention entschieden, nicht durch Hindemiths Text belegt. Übernahme aller Entscheidungen in Graph-Status und Vorschlagsdatei in eigenem PR. Inhaberentscheidung ersetzt keine unabhängige Fachabnahme. |
| Richtungs- und Fachentscheidungen (17.11.2026) | Entschieden: v0.1 = Akkorde + MIDI-Export, Drums in v2, Zielgruppe Produzierende ([ADR-013](../../decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md)); Perspektivenmodell statt Quellenrangfolge ([ADR-014](../../decisions/ADR-014-theorie-perspektiven-und-kontext.md)); Kernverträge zu Intervallen, add2/add9, DROP2 und deutschen Namen ([ADR-015](../../decisions/ADR-015-kernvertraege-intervalle-voicing-notation.md)); `V7alt` ([ADR-016](../../decisions/ADR-016-v7alt-alterierte-dominante.md)); 25 Graphkanten ([`GRAPH_HUMAN_REVIEW_v1.csv`](../../knowledge/relations/GRAPH_HUMAN_REVIEW_v1.csv)). **Offen:** Umsetzung von ADR-014 bis ADR-016 im Kern mit Tests; Hindemith-Untergruppe des Quartsextakkords (am 17.11.2026 als I,2 entschieden); Übernahme der Graph-Abnahme in `GRAPH_AUDIT_PLAN.json`/Generator; 72 Kanten weiter `AUSSTEHEND` (u. a. 14 Korpusfälle). |
| v0.1-Spezifikation und Graph-Abnahme v2 (17.11.2026) | Entschieden: MIDI-Export ([ADR-017](../../decisions/ADR-017-midi-export-v01.md)), nur Dateiexport ([ADR-007](../../decisions/ADR-007-audio-nur-dateiexport-v01.md)), ein Fenster mit zwei Bereichen ([ADR-001](../../decisions/ADR-001-ein-fenster-zwei-bereiche.md)), Glide nur als Shell ([ADR-003](../../decisions/ADR-003-glide-nur-shell-und-infrastruktur.md)), MPL-2.0/CC BY 4.0 ([ADR-004](../../decisions/ADR-004-lizenz-und-marke.md)), JSON mit ganzzahliger Version ([ADR-006](../../decisions/ADR-006-json-mit-schema-version.md)), Hindemith I,2 in ADR-014. Alle 97 Kanten bewertet ([`GRAPH_HUMAN_REVIEW_v2.csv`](../../knowledge/relations/GRAPH_HUMAN_REVIEW_v2.csv)): 41 im Geltungsbereich freigegeben, 40 mit Patch, 14 bis zum Korpus zurückgestellt, 2 abgelehnt. **Offen:** SMF-Writer mit 10 Golden-Exportfällen und DAW-Abnahme (Reaper, MuseScore 4); Umsetzung ADR-014 bis ADR-016; Übernahme der Graph-Abnahme in `GRAPH_AUDIT_PLAN.json`/Generator; Lizenzkennzeichnung je Ordner; Kap. XIII bei Hindemith (B2) und Montuno-Hörprobe (A6) nach v0.1. |
| Werkzeug Golden-Suite (16.11.2026) | `knowledge/research/run_golden_test_suite.py` überschreibt bei jedem Lauf fünf versionierte Berichte unter `knowledge/research/` mit Zeitstempel, Laufzeiten, Plattform, Commit-SHA und LF-Zeilenenden; der Arbeitsbaum ist danach nicht mehr sauber. **Behoben am 16.11.2026:** Ein einfacher Lauf schreibt keine Dateien mehr; Exporte gehen mit `--output-dir <Pfad>`, die versionierten Berichte werden nur mit `--update-baseline` erneuert. `tests/test_golden_runner_outputs.py` sichert das ab. Details in der [Master-Übergabe](../../docs/handover/MASTER_UEBERGABE_2026-11-16.md), Abschnitt 3.8. |

## PDF-Konvertierung mit Docling (2026-11-14)

- Neben 58 PDF-Kopien (40 eindeutige Dateien) liegen jetzt gleichnamige Docling-Extrakte (`.md`). Zuordnung und Hashes: [`manifests/pdf_docling_markdown_2026-11-14.csv`](../../manifests/pdf_docling_markdown_2026-11-14.csv). Alle Extrakte sind `REVIEW_REQUIRED`, ohne OMR und ohne fachliche Freigabe.
- `research/STEPS_Bibliothek/MakingMusic.pdf` und die Kopie in `Dokumentation (unsortiert)/` bestanden vollständig aus Null-Bytes (SHA-256 `dba9fb9e…3a21`). Am 14.11.2026 hat der Inhaber eine intakte Datei bereitgestellt; sie ist bytegleich mit `MakingMusic_DennisDeSantis.pdf` (SHA-256 `4c6ba38b…c11a`, gleiche Größe von 23.100.686 Bytes). Beide Pfade sind damit repariert (OA-0017) und haben einen Docling-Extrakt. Im Dateiregister (`MUSIC_SOURCE_REVIEW_PROGRESS.csv`, F01046 und F00626) ist der reparierte SHA-256 (`4c6ba38b…c11a`) am 16.11.2026 nachgezogen; die kanonische Aufgabenliste unter `%LOCALAPPDATA%` auf Windows ist noch nachzuziehen.
- Der Inhaber hat am 14.11.2026 entschieden, die Extrakte wie die Original-PDFs in Git zu versionieren. Damit weicht der Bestand von `knowledge/sources/RIGHTS_POLICY.md` ab, nach der fremde Volltexte lokal und per `.gitignore` geschützt bleiben. Die Rechteprüfung je Quelle bleibt offen. Das Repository ist öffentlich, die Extrakte sind also bereits frei abrufbar.
- 82 Markdown-Dateien (78 in `STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials`, 4 in `source_archive`) konnten lokal nicht gelesen werden (`Errno 22`). Wahrscheinlich hängt das mit OneDrive zusammen. Derselbe Fehler bricht `git status` ab. **Nachprüfung 16.11.2026:** In der OneDrive-Ablage sind alle 2.928 versionierten Dateien lesbar und inhaltlich identisch mit Git (500 davon nur mit Windows-Zeilenenden). Die Lesefehler waren vorübergehend, vermutlich nicht lokal vorgehaltene OneDrive-Dateien.
- Neben 26 gespeicherten HTML-Seiten (18 eindeutige Dateien: Ableton-Artikel, Chord-Wheel-, Modewheel- und Chordfiles-Seiten, eine Reddit-Diskussion) liegen jetzt gleichnamige Markdown-Extrakte. Sie wurden mit `html_extract` aus dem früheren Referenzexport neu aus dem versionierten Stand erzeugt, weil sechs Ableton-Seiten nach dem ersten Export durch die Secret-Bereinigung geändert wurden. Medienverweise zeigen relativ auf die `_files`-Begleitordner. Zuordnung: [`manifests/html_markdown_2026-11-14.csv`](../../manifests/html_markdown_2026-11-14.csv). Status `review_required`. **Nachgeprüft 16.11.2026:** Alle 18 eindeutigen HTML-Extrakte (26 Pfade) und die zwei Vollseiten-OCR-Neuläufe (`Music_Theory_Advanced_Level.md` und `Understanding_Basic_Music_Theory.md`) sind im [HTML- und OCR-Prüfbericht](../../docs/audit/HTML_EXTRAKTE_UND_OCR_NACHPRUEFUNG_2026-11-16.md) strukturell und quellenkritisch nachgewiesen (Hauptinhalt, Tabellen, Duplikate im responsive DOM, Werbe-Posts, OCR-Auslassungen sowie Entlarvung des AI-SEO-Textes `The Chord Wheel.html`).
- Ein [Rechteinventar der Volltext-Extrakte](RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md) ordnet alle PDFs und gespeicherten Webseiten nach Lizenzlage ein und nennt Entscheidungsoptionen. Es ist eine Arbeitsgrundlage, keine Rechtsprüfung. Zwei Extrakte (`Understanding_Basic_Music_Theory`, `Music_Theory_Advanced_Level`) lagen zunächst nur als Zeichensalat vor; die Neuläufe per Vollseiten-OCR und Direkt-OCR sind nun im obigen Bericht dokumentiert.

### Ausschluss der Klasse E und Zusammenfassungen (14.11.2026)

- Für die zehn Werke der Rechteklasse E sind Original-PDFs und Volltext-Extrakte (13 Dateipfade, 26 Dateien) per `.gitignore` ausgeschlossen. Sie liegen nur noch lokal, eine Sicherung liegt außerhalb des Repositorys. Die Git-Historie enthält sie weiterhin.
- Stattdessen stehen ausführliche [Zusammenfassungen in eigenen Worten](../STEPS_Bibliothek/Zusammenfassungen/README.md) im Repository. Sie sind nicht fachlich freigegeben.
- Im Dateiregister (`MUSIC_SOURCE_REVIEW_PROGRESS.csv`) und im kuratierten Quellenregister stehen die Dateinamen weiter. Die lokal geführten Pfade sind in [`manifests/restricted_local_2026-11-14.csv`](../../manifests/restricted_local_2026-11-14.csv) gekennzeichnet (Pfad, SHA-256, Zusammenfassung, Entscheidung). Die Coverage-Auswertung führt sie als `restricted_local` statt als fehlenden Pfad; `tests/test_restricted_local.py` prüft, dass jeder gelistete Pfad ausgeschlossen und nicht versioniert ist und eine versionierte Zusammenfassung hat.
- Im kuratierten Quellenregister (`knowledge/sources/curated_sources_registry.yaml`) passten zwei freigegebene Einträge nicht zur Datei. Nach Prüfung der Extrakte am 14.11.2026 korrigiert: SRC-0010 verweist auf `Schachter_Aldwell-Harmony_Voice_Leading.pdf`, laut Titelblatt und Vorwort die 3. Auflage von Edward Aldwell und Carl Schachter (Thomson/Schirmer, Wadsworth Group), nicht die 4. Auflage mit Cadwallader. SRC-0012 beschrieb Hindemiths *The Craft of Musical Composition*; das Buch selbst grenzt sich im Vorwort davon ab und verbietet Parallelen mit benannten Ausnahmen. SRC-013 beschreibt unabhängig davon die 4. Auflage und bleibt unverändert.
- In 47 PDF-Extrakten verwiesen 280 Links mit absolutem lokalem Pfad (Benutzerverzeichnis) auf die Original-PDFs, dazu 2.562 Verweise auf nicht versionierte Seitenbilder. Sie sind durch relative PDF-Links bzw. einen Hinweis ersetzt. Die Docling-Rohausgaben liegen lokal unter `STEPS_Konvertierung_Rohdaten/PDF-Dateien-konvertiert`. In `knowledge/research/03_FACHLICHE_FEHLER.md` und `14_ABSCHLUSSBERICHT.md` sind 17 Repo-Links mit lokalem Pfad auf relative Pfade umgestellt. Historische Archivdateien und der Generator `scripts/handover/generate_core_registers.py` enthalten weiterhin lokale Pfade und sind bewusst unverändert.
- Für `Music_Theory_Advanced_Level.pdf` wurde Docling mit erzwungener Vollseiten-OCR (RapidOCR, Torch) erneut ausgeführt; der Extrakt ist lesbar (Herkunft: Forenbeiträge auf mysongbook.com, 2005). Bei `Understanding_Basic_Music_Theory.pdf` blieb auch dieser Lauf leer; der Extrakt stammt deshalb aus einer Direkt-OCR (Seitenrendering mit pypdfium2, RapidOCR). Beide Extrakte enthalten OCR-typische Fehler; Methode und Status stehen im Frontmatter.
- **Entscheidungen des Inhabers (14.11.2026):** Git-Historie bleibt unverändert; Klassen A–D und gespeicherte Webseiten bleiben als öffentlich zugängliche Inhalte versioniert; Arbeitsablage bleibt im OneDrive-Ordner. Wegen der gemeinsamen `.git`-Synchronisation über OneDrive (Windows und Mac) können weiterhin `mmap`-Fehler und Konflikte auftreten; vor Git-Arbeiten auf einem Rechner sollte die Synchronisation abgeschlossen sein.

### Maschinelle Prüfung der Zusammenfassungen (15.11.2026)

- Claude Fable 5.2 hat die zehn Zusammenfassungen gegen die Extrakte geprüft und korrigiert ([Prüfprotokoll](../STEPS_Bibliothek/Zusammenfassungen/PRUEFPROTOKOLL_FABLE_2026-11-15.md)). Alle zehn: Freigabe nach Korrektur; `fachliche_freigabe` bleibt `false`, bis eine Abnahme am gedruckten Original erfolgt. Die je Werk offenen Fragen am Original, die Befunde zu den Quelldateien und die Entscheidung zu zwei strukturnahen Stellen (16.11.2026: gekürzt) stehen in der [Prüfung der Zusammenfassungen](PRUEFUNG_ZUSAMMENFASSUNGEN_2026-11-15.md).
- Befunde zu den Quelldateien: Dem PDF von Aldwell/Schachter fehlen Anhang II und die Register, gedruckte Seitenzahlen und PDF-Seiten laufen auseinander (vermutlich fehlen auch Seiten im Buchinneren). Das Stuart-Heft enthält 1.270 statt der im Titel genannten 1.500 Folgen (10 × 78 + 7 × 70), ist laut Inhaltsverzeichnis aber vollständig (am Original-PDF nachgeprüft am 16.11.2026).
- Die unbelegten Rechtsangaben bei Schönberg und Hindemith (Schutzfristen, Gemeinfreiheit des deutschen Originals) sind am 16.11.2026 auf Entscheidung des Inhabers gestrichen. Müller (Z-Library) wird nach Entscheidung vom selben Tag normal weiterverwendet.
- Für STEPS relevant: Hindemith lockert mehrere Satzverbote ausdrücklich (Terzverdopplung ab Kap. IV, Quintparallelen bei Nebenseptakkorden, Leitton per übermäßigem oder vermindertem Schritt). Wer daraus Constraints für den Voicing-Solver ableitet, muss diese Ausnahmen mitführen. DeSantis (D♯ = E♭ in der Piano-Roll) und Müller (Akkorde bis auf enharmonische Verwechslung) ebnen die Enharmonik bewusst ein; das widerspricht der STEPS-Vorgabe und ist bei Übernahmen zu beachten.

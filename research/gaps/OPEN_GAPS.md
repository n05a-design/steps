# Offene Evidenz und historische Bestandsaufnahme

## Repository-Bestandsaufnahme vom 10.11.2026

- Projektkonsolidierung nennt sechs Originaldokumente, im Originalarchiv liegt derzeit kein `Glide Kontext für Fable(2).md` (5 Markdown-Originale vorhanden); Nachweis/Fundort prüfen.
- Kein ausführbarer `app/`- oder `src/steps/`-Musikcode im analysierten `main`-Baum.
- Urheberrechte zahlreicher Fach-PDFs, heruntergeladener Web-Seiten und Drittanbieterbilder offen.
- V6.6/V6.7: mehrere Versionen, Fachordner 21 und 39 doppelt benannt; unterschiedliche Struktur-/Zählmodelle.
- Historische JSON-/CSV-Indizes benötigen Pfad- und Hashrevalidierung.
- Externe Integration von Glide nur Vorschlag, konkrete Code-/Lizenzübernahme nicht geprüft.
- Die bestehenden Bibliotheks-Generatoren wurden nicht ausgeführt und ihre Seiteneffekte sind nicht analysiert.

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
| W01/W02/W03 | Kanonische Quellen und genaue Fundstellen je Pilotclaim abgleichen. 14 der 35 historisch als VERIFIED bezeichneten Claims lagen außerhalb der Fable-Stichprobe. Alle 66 Einträge mit Evidenzstatus inventarisieren, Buchseiten nur bei berechtigtem Zugriff bewerten. Historische Quellenmetadaten einschließlich der doppelten Titel nach Autor, Ausgabe, Locator und Rechteklasse auflösen. |
| W04 | P01–P19, PAT-001–031 und [Latin-Katalog](../../knowledge/concepts/styles/GENRE_RESEARCH_LATIN.md) nachprüfen: Akkordtöne/Bass/Rollen, Taktart/Taktgrenzen/PPQ, Eventraster, stilistische Aussagen und ggf. Hörbeleg. PROG-024 ist ein Übungsschema. Die verlinkte Jobim-Partitur belegt die Variante mit ♭II7. |
| W05/W08 | 97 Relationen stehen auf REVIEW_REQUIRED. Zwei historische Aliasse sind aufgelöst. Für 84 Knoten-IDs fehlt die kanonische Definition. Richtung, Typ, Gültigkeitsbereich und Claim-Bezug je Kante prüfen. Historische Literatur und Pilotprovenienz trennen. |
| W06/W07, T01/T03–T05/T07 | 132 Golden Cases außerhalb der Fable-Stichprobe; auch die 66 Stichprobenfälle brauchen individuelle, versionierte Evidenz. Verbleibende Evaluatorzweige und Fixture-Sollwerte klassifizieren. Die gelesenen Renderer-/Benchmark-/Coverage-Pfade mit Negativkontrollen absichern; Hash-Identität und Generatorgleichheit gelten als formale Nachweise. |
| H01/H02 | Sechs Gegenproben für den OpenAI-Übergabebericht sind dokumentiert. Historische Statuslabel und archivierte Tests bleiben auf ihren Quellstand bezogen. |

# Offene Evidenz und historische Bestandsaufnahme

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

- Projektkonsolidierung nennt sechs Originaldokumente, im Originalarchiv liegt derzeit kein `Glide Kontext für Fable(2).md` (5 Markdown-Originale vorhanden); Nachweis/Fundort prüfen.
- Kein ausführbarer `app/`- oder `src/steps/`-Musikcode im analysierten `main`-Baum.
- Urheberrechte zahlreicher Fach-PDFs, heruntergeladener Web-Seiten und Drittanbieterbilder offen.
- V6.6/V6.7: mehrere Versionen, Fachordner 21 und 39 doppelt benannt; unterschiedliche Struktur-/Zählmodelle.
- Historische JSON-/CSV-Indizes benötigen Pfad- und Hashrevalidierung. **Teilweise erledigt 16.11.2026:** Das [Bestandsinventar vom 11.11.2026](../../docs/audit/BESTANDSINVENTAR_NACHPRUEFUNG_2026-11-16.md) ist nachgeprüft; alle 3.947 Zeilen sind wiedergefunden oder erklärt, kein ungeklärter Verlust. Weitere historische Indizes sind offen.
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

## PDF-Konvertierung mit Docling (2026-11-14)

- Neben 58 PDF-Kopien (40 eindeutige Dateien) liegen jetzt gleichnamige Docling-Extrakte (`.md`). Zuordnung und Hashes: [`manifests/pdf_docling_markdown_2026-11-14.csv`](../../manifests/pdf_docling_markdown_2026-11-14.csv). Alle Extrakte sind `REVIEW_REQUIRED`, ohne OMR und ohne fachliche Freigabe.
- `research/STEPS_Bibliothek/MakingMusic.pdf` und die Kopie in `Dokumentation (unsortiert)/` bestanden vollständig aus Null-Bytes (SHA-256 `dba9fb9e…3a21`). Am 14.11.2026 hat der Inhaber eine intakte Datei bereitgestellt; sie ist bytegleich mit `MakingMusic_DennisDeSantis.pdf` (SHA-256 `4c6ba38b…c11a`, gleiche Größe von 23.100.686 Bytes). Beide Pfade sind damit repariert (OA-0017) und haben einen Docling-Extrakt. Im Dateiregister (`MUSIC_SOURCE_REVIEW_PROGRESS.csv`, F01046 und F00626) steht noch der Hash der genullten Fassung; die kanonische Aufgabenliste unter `%LOCALAPPDATA%` ist nachzuziehen.
- Der Inhaber hat am 14.11.2026 entschieden, die Extrakte wie die Original-PDFs in Git zu versionieren. Damit weicht der Bestand von `knowledge/sources/RIGHTS_POLICY.md` ab, nach der fremde Volltexte lokal und per `.gitignore` geschützt bleiben. Die Rechteprüfung je Quelle bleibt offen. Das Repository ist öffentlich, die Extrakte sind also bereits frei abrufbar.
- 82 Markdown-Dateien (78 in `STEPS_Bibliothek_V6_6_Ableton_Blog_Archiv_und_Tutorials`, 4 in `source_archive`) konnten lokal nicht gelesen werden (`Errno 22`). Wahrscheinlich hängt das mit OneDrive zusammen. Derselbe Fehler bricht `git status` ab. **Nachprüfung 16.11.2026:** In der OneDrive-Ablage sind alle 2.928 versionierten Dateien lesbar und inhaltlich identisch mit Git (500 davon nur mit Windows-Zeilenenden). Die Lesefehler waren vorübergehend, vermutlich nicht lokal vorgehaltene OneDrive-Dateien.
- Neben 26 gespeicherten HTML-Seiten (18 eindeutige Dateien: Ableton-Artikel, Chord-Wheel-, Modewheel- und Chordfiles-Seiten, eine Reddit-Diskussion) liegen jetzt gleichnamige Markdown-Extrakte. Sie wurden mit `html_extract` aus dem früheren Referenzexport neu aus dem versionierten Stand erzeugt, weil sechs Ableton-Seiten nach dem ersten Export durch die Secret-Bereinigung geändert wurden. Medienverweise zeigen relativ auf die `_files`-Begleitordner. Zuordnung: [`manifests/html_markdown_2026-11-14.csv`](../../manifests/html_markdown_2026-11-14.csv). Status `review_required`; Hauptinhalt, Tabellen und Listen sind nicht manuell abgenommen.
- Ein [Rechteinventar der Volltext-Extrakte](RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md) ordnet alle PDFs und gespeicherten Webseiten nach Lizenzlage ein und nennt Entscheidungsoptionen. Es ist eine Arbeitsgrundlage, keine Rechtsprüfung. Zwei Extrakte (`Understanding_Basic_Music_Theory`, `Music_Theory_Advanced_Level`) sind wegen fehlender Unicode-Zuordnung unbrauchbar und brauchen einen OCR-Lauf.

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

# Fortsetzung: 64 Golden-Beispiele, Quellen und Sicherheitskorrektur

Stand: 14.11.2026. GitHub-main wurde unverändert als `5d2d09cfba22fa137ef65da5ffcc31bcadf5194a` geprüft. Bearbeitung im bestehenden Nachtbranch `codex/audit-nacht-20261114`, Draft [PR #55](https://github.com/n05a-design/steps/pull/55). Sicherheitskorrektur separat in `codex/security-guardrail-166-20261114`, Commits `b250418` und `c4cf228`; anschließend ohne Änderung von main in den Nachtbranch übernommen.

## Tatsächliche Ergebnisse

Alle 64 zuvor nur strukturell erfassten Golden-Spezifikationsbeispiele besitzen jetzt eine individuelle, gegen den Originalfall per SHA-256 gebundene Untersuchung: [maschinenlesbare Vorschläge](../../../knowledge/research/golden_cases/REMAINING_64_AUDIT.json) und [vollständige Prüfmatrix](GOLDEN_64_PRUEFMATRIX_2026-11-14.csv). Kein Originalfall, Testspiegel, historisches Tripel oder historische Definition wurde nachträglich korrigiert.

43 getrennte typisierte Modellprüfungen bestehen; 21 Fälle haben bewusst keinen neuen Modelltest. Darunter sind sechs bereits vorhandene konkrete GM-Tabellenchecks. Die verbleibenden 15 Fälle enthalten fehlenden Kontext, Quellenlücken, eine nicht definierte Stilregel oder erforderliche menschliche Hör-/Spiel-/Didaktikprüfung. Die Zahl 43 zählt separate Auditmodelle, keine 43 uneingeschränkt bestandenen historischen Originalfälle.

Zwölf wiedergefundene historische Projekttexte sind bytegleich und mit überprüfbaren Hashes [gesichert](../../../archive/audit-history/golden-source-recovery-2026-11-14/README.md). Die neue Quellenprüfung unterscheidet Originalnoten, Primärtext, Abstract, Inhaltsverzeichnis, frühere Prüfung und nicht verifizierte Zitate. Fremde PDFs und Notenbilder bleiben außerhalb des veröffentlichten Änderungsbestands.

## Vorher / Nachher

| Prüfbestand | Vorher | Nachher |
| --- | ---: | ---: |
| Verbleibende Golden-Beispiele individuell untersucht | 0 / 64 | 64 / 64 |
| Neue getrennte typisierte Rechnungen für diese 64 | 0 | 43 PASS / 0 FAIL / 21 nicht ausgeführt |
| Vorhandene GM-Tabellenchecks innerhalb der 64 | 6 | 6 erhalten |
| Originalkonflikte in den 64 explizit gebunden | nicht vollständig einzeln erfasst | 7 Konflikte sowie 1 offene Stilentscheidung |
| Golden-Gesamtbestand / unveränderter Testspiegel | 198 / 198 | 198 / 198 |
| Bereits zuvor ergänzte Golden-Rechnungen | 14 | 14 erhalten; zusammen 57 begrenzte zusätzliche Modellrechnungen |
| Graphkanten inventarisiert | 97 | 97 |
| Graphstatus | 38 Stichproben / 1 FAIL / 58 OPEN | unverändert; CDR-010 bleibt FAIL |
| Neue Graphproben im Nachtpaket | 23 | 24 PASS |
| Kanten mit technischen Gegenprüfungen | 45 | 45; CDR-018 hatte bereits einen bestehenden Benchmarkcheck |
| Neue direkte Primärnotenkontrolle | 0 in dieser Fortsetzung | CDR-018 / REF-0075 / CLAIM-036 |
| Vollständige unabhängige Fachabnahmen | 0 | 0 |
| Knowledge-Benchmark | 92 PASS / 0 FAIL / 27 PENDING | 92 PASS / 0 FAIL / 27 PENDING |
| Aktuelle Secret-Muster außerhalb erlaubter Fixtures | 54 bekannte + 15 zusätzlich entdeckte | 0 nach Bereinigung |

## Sieben Originalkonflikte und eine offene Stilentscheidung

- **REF-0016:** Titel/Erwartung beschreiben zwei Dur-Dreiklänge D und C, Eingabe dagegen `root=C, quality=Minor`. Getrennte Vereinigungsrechnung zweier benannter Dreiklänge; keine Gleichsetzung mit einem Slash-Bass. CDR-010 bleibt FAIL.
- **REF-0017:** `V -> I` in C ergibt G nach C. Erwartetes G7 setzt eine zusätzliche Septime voraus. Korrekturvorschläge sind ausdrücklich getrennte neue Fallversionen.
- **REF-0051:** Erwartetes A nach G unterschlägt die vollständige mögliche Linie A–G#–G–F# über Am–Am(maj7)–Am7–Am6.
- **REF-0052:** Neo-Soul-Titel Fm7–Bb7–Cmaj7–Abmaj7 und Andalusische Eingabe/Erwartung Am–G–F–E7 sind verschiedene Fallidentitäten.
- **REF-0062:** Wiedergefundene PAT-021-Fassung hat 174 BPM und andere Kick-/Ghost-Einsätze als die heutige 168-BPM-Fassung. Beide bleiben als Versionen getrennt.
- **REF-0063:** Historische PAT-022-Fassung hat 174 BPM, heutige Erwartung 175 BPM. Gleiche Kickpositionen beweisen keine identische Fassung.
- **REF-0073:** Ein LH-Grundton plus grundtonlose RH ist im Gesamtklang nicht grundtonlos. Die Rechnung belegt den tatsächlich vorhandenen Grundton.
- **REF-0176, Stilentscheidung OFFEN:** Die angegebenen Stimmen erreichen in gleicher Richtung eine Quinte mit Sopranterzsprung. Ob dies im gemeinten Basso-continuo-Profil verboten ist, ist nicht aus der Intervallrechnung entscheidbar. Keine Umdeutung in ein beliebiges Jazz-/Pop-Profil.

Die Validatoren verhindern, dass grüne Modellrechnungen diese sieben Konflikte oder die offene Stilentscheidung ausblenden. Original-Hashes, Vollständigkeit, menschliche Abnahmegrenzen und Archivbytes sind durch positive und negative Regressionen geschützt.

## Quellenprüfung und Graphfortsetzung

Die [zehn Quellenprüfungen](GOLDEN_SOURCE_REVIEW_2026-11-14.json) dokumentieren genaue Fundstellen, Reichweite und Restblocker.

**Mauleón / CDR-018:** Die [offizielle Sher-Music-Seite](https://www.shermusic.com/products/salsa-guidebook-for-piano-ensemble) verlinkt eine zweitseitige Notenprobe. Gedruckte Seite 48, Abbildung 3.3a wurde nach lokalem Rendern visuell geprüft: 3:2-Son-Clave, erster Takt 1/2+/4, zweiter Takt 2/3. Eigene Umrechnung bei 480 PPQ ergibt `[0,720,1440,2400,2880]`. PDF-SHA-256: `88a08b6dd81d5195f1341ab7960b290ebd651c10895644fc8ab9279b276fcae4`. Diese begrenzte Quellenaussage und Rechnung stehen jetzt in Graphmatrix und Claim-Register. Die historische Seitenangabe 52 bleibt ausdrücklich ungeprüft; keine historische Datei wurde verändert.

**Swing / REF-0044:** Friberg/Gulz/Wettebrandt (2023), gedruckte Seiten 92–93, PDF-Seiten 8–9, wurden visuell geprüft. Gleichung (1) verwendet ein begrenztes lineares Regressionsmodell mit Untergrenze und benannten Standardparametern; der Text begrenzt seine Interpretation auf durchschnittliche Tendenzen und nennt Daten-/Auswahlabhängigkeit. Das neue Modell prüft ausschließlich diese Version. Der [Primärabstract von 2002](https://doi.org/10.1525/mp.2002.19.3.333) war zugänglich, dessen Volltext nicht. Weder die alte Projektformel noch ein universelles lineares Aufführungsgesetz oder eine 57%-Zuschreibung sind damit freigegeben.

**MusicXML:** Der [W3C-Abschnitt zur Tonhöhe](https://www.w3.org/2021/06/musicxml40/tutorial/midi-compatible-part/) belegt die getrennten step/alter/octave-Felder. Die eigene C#4-/Db4-Rechnung prüft nur die begrenzte Pitch-Repräsentation, keinen vollständigen Konverter. Der pauschale historische DTD-Verweis ersetzt keine genaue MusicXML-4.0-Schemafundstelle.

**Übrige Quellen:** Das offizielle Mauleón-Inhaltsverzeichnis lokalisiert Brazilian Clave auf S.57, Conga ab S.64 und Klavier ab S.117; die Inhalte dieser Seiten wurden nicht aus dem Inhaltsverzeichnis abgeleitet. Die erreichbare Levine-Probe gehört zum Jazz Piano Book und belegt keine Kapitelbehauptung aus dem Jazz Theory Book. DIN-1317-Zitat und Robert-Prehn-Identität bleiben unbestätigt. Bestehende sechs GM-Primärtabellenchecks bleiben erhalten; ein aktueller Spiegel wurde nicht als neue Primärquelle ausgegeben.

## Sechs Definitionslücken bleiben präzise offen

| Knoten | Bearbeiteter Vorschlag / Beleggrenze | Noch erforderlich |
| --- | --- | --- |
| MODAL_SHIFT_TO_II7 | REF-0077 rechnet D7 nach Dm7; die Zielrichtung widerspricht weiterhin dem historischen Namen. | Autorisierte fachliche Klärung von Richtung und Knotenidentität. |
| PIANO_MONTUNO_GUAJEO | Neue Modellereignisse bleiben eigene Übungen; offizielle Clave-Noten sind keine historische Klavierfigur für PROG-025. | Originalfigur mit Tonhöhen, Onsets, Dauern, Harmonie und Clave-Zuordnung; Fach-/Spielprüfung. |
| BOSSA_BATIDA | REF-0076 ist ein abgegrenztes Cross-Stick-Projektbeispiel. | Gemeinte Gitarren-/Klavier-/Schlagzeugfigur, Aufnahme und genaue Quelle. |
| BRAZILIAN_TAMBORIM_SURDO_SYNTHESIS | Rhythmische Ähnlichkeit und eine Inhaltsverzeichnisüberschrift beweisen keine Herkunftsthese. | Belastbarer historischer Text/Archivbeleg, insbesondere bisher nur paraphrasierte Literatur. |
| SURDO_PULSE | P14-Klavierpendel und REF-0190 sind keine vollständige Samba-Ensemblerolle. | Samba-/Bossa-Kontext, Instrumentrolle und primeira-/segunda-Zuordnung. |
| ACCENT_ON_BEAT_2_IN_2_4 | Eine 4/4-Beatliste bestimmt keine 2/4-Akzentnorm. | Konkrete Rolle, Taktart, Velocity und nachgewiesene Ensemblepraxis. |

Alle sechs Vorschläge bleiben `REVIEW_REQUIRED`, ohne Produktionsfreigabe. Der Graph enthält weiterhin null vollständige unabhängige Fachabnahmen.

## Sicherheitskorrektur und Remote-Nachweis

Der [Sicherheitsbericht](SECRET_GUARDRAIL_166_2026-11-14.md) dokumentiert 49 Google-Schlüsselvorkommen und 20 AWS-Muster innerhalb desselben eingebetteten JPEG. 38 Dateien wurden ausschließlich an den betroffenen Payloads bereinigt. Baseline, Erkennungsmuster und synthetische Allowlist bleiben unverändert; Dateityp-Abdeckung wurde verschärft.

Am geprüften Sicherheitsstand `c4cf228` bestehen [Secret Guardrail #168](https://github.com/n05a-design/steps/actions/runs/43584230387), [Python Suite #155](https://github.com/n05a-design/steps/actions/runs/43584230346) und [Struktur #296](https://github.com/n05a-design/steps/actions/runs/43584230377). Ein vorheriger Strukturlauf scheiterte an fehlenden historischen Git-Objekten; beide Testworkflows holen jetzt die für die Byte-Erhaltungsregression nötige Historie. Es gab keinen Merge nach main.

Historische Google-Schlüssel bleiben in alten Git-Objekten und gegebenenfalls externen Kopien rekonstruierbar. Berechtigungen, mögliche missbräuchliche Verwendung, erforderliche Rotation und eine gesondert autorisierte historische Bereinigung müssen Berechtigte beurteilen. Fremde Zugangsdaten wurden nicht verwendet oder rotiert. Sicherheitsfreigabe bleibt OFFEN.

## Validierung und unabhängige Gegenprüfung

- 215 Kerntests bestanden, darunter elf neue Golden- und zwei zusätzliche Graphregressionen sowie die sechs Sicherheitsbereinigungsregressionen.
- 36 Skilltests bestanden.
- Knowledge-Benchmark: 92 PASS / 0 FAIL / 27 PENDING. Exit 1 ist wegen fehlender Pflichtabnahmen erwartet und ausdrücklich kein uneingeschränkter PASS.
- Ontologiearchiv: zwölf frühere Originale und 41 Definitionen unverändert; zwölf zusätzliche Golden-Quelltexte bytegleich.
- Alle 97 Graphkanten weiterhin originalgebunden; Matrix reproduzierbar. CDR-010 bleibt FAIL.
- Golden-Master und Testspiegel: weiterhin 198 Fälle bytegleich; API-Referenz und Referenzintegrität geprüft.
- Abdeckungsmatrix mit Detailausgabe: `--check`, Exit 0; keine nachträgliche Umklassifizierung von Fachabnahmen.
- Eigene Modell-Gegenproben mutieren Eingaben, Erwartungen, XML-Schreibweisen, Quellpfade/-bytes, Abnahmeflags und Originalidentitäten. Alte und neue widersprüchliche Quellenstände bleiben sichtbar.
- Unabhängiger Secret-Gegenlauf über alle zuvor versionierten Dateien ergänzte die Dateityp-Lücke; nur vier autorisierte Fixture-Vorkommen bleiben. Vollständiger Scanner und Payload-Erhaltungsprüfung bestehen am Sicherheitscommit.

Die Schlussprüfung ist eine separate technische Gegenprüfung desselben Agenten, keine unabhängige menschliche Fachabnahme. Finaler Secret-/Linklauf und Remote-CI des Golden-Commits werden im Git-Übergabenachtrag mit tatsächlichem Ergebnis festgehalten.

## Status und verbleibende Maßnahmen

**OPERATIV ABGESCHLOSSEN für dieses Teilpaket:** Sicherheitsbereinigung, Einzeluntersuchung der 64 Beispiele, 43 begrenzte Modellrechnungen, Wiederherstellung der zwölf Projektquellen, Quellengrenzen und zusätzlicher CDR-018-Originalnotenbeleg.

**TECHNISCH BESTANDEN:** die oben tatsächlich ausgeführten Prüfungen; Benchmark-Pflichtfreigaben und historische CDR-010-Wertung bleiben davon getrennt.

**FACHLICH / RECHTLICH OFFEN:** sämtliche fehlenden Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen, sechs historische Definitionslücken, CSS-Bundle-Rechte, Quellen-/Autorenidentitäten und historische Sicherheitsbewertung.

**NICHT ABGESCHLOSSEN für das Gesamtaudit:** Vollfreigabe aller Graphkanten, Abnahme/Migration der konflikthaften neuen Golden-Versionen, abschließende Rechte-/Sicherheitsentscheidungen und vollständige kontrollierte Übernahme relevanter lokaler Restbestände. Die [priorisierte Restliste](NACHT_RESTBLOCKER_2026-11-14.md) nennt konkrete Voraussetzungen; alle 27 PENDING-Fälle bleiben einzeln dokumentiert. Eine grüne CI allein schließt das Gesamtaudit nicht.

## Zusätzlicher Navigationsbefund

Der erweiterte Linklauf über 157 Markdown-Dateien und 917 interne Links fand 25 bereits zuvor defekte relative Verweise in eingefrorenen README-Dateien unter `archive/v1_docs`. Alle tatsächlichen Zieldateien wurden im bestehenden Bestand lokalisiert. Eine [separate aktuelle Navigation](../../../archive/v1_docs/LINK_RESOLUTION_2026-11-14.md) und [maschinenlesbare Zuordnung](LEGACY_LINK_RESOLUTION_2026-11-14.csv) sichern den Einstieg, ohne historische Originale umzuschreiben. Die 25 alten Links bleiben als historische Defekte sichtbar; sie werden nicht als bestandene Originalverweise gezählt. Die neuen und geänderten aktiven Links werden separat überprüft.

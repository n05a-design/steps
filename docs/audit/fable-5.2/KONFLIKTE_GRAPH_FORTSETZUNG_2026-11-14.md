# Fortsetzung nach PR #56: Golden-Konflikte und offene Graphnachweise

Stand: 14.11.2026. PR #56 ist nachweislich gemergt; aktueller geprüfter Ausgangs-main: `9afaf33eaeec332a3d19b4e30d05b1902234936f`. Neuer Branch: `codex/audit-konflikte-graph-20261114`. Kein automatischer Merge nach main.

## Ergebnis und Grenzen

Die sieben historischen Golden-Konflikte sind durch 15 konkrete, ausführbare Korrekturvorschläge und Gegenproben präzisiert. Original-ID, ursprüngliche Eingaben/Erwartungen und SHA-256 bleiben unverändert. Neue Vorschläge besitzen eigene Unterkennungen und sind kein zweiter Golden-Master. Sie sind `REVIEW_REQUIRED`, ohne Produktionsfreigabe und ohne menschliche Fachabnahme.

Alle 58 zuvor offenen Graphkanten sind in einer gesonderten Fortsetzungsmatrix berücksichtigt. Für 16 davon liegen ausführbare Vorschläge oder Gegenproben vor: 16 neue Modellproben und eine ausdrücklich wiederverwendete vorhandene Qualitätswechselprobe. 18 Kanten benötigen genaue Quellen-/Semantikentscheidungen, 14 einen nachvollziehbar annotierten Korpus und zehn eine externe praktische/didaktische Prüfung. Diese Kategorien zählen Bearbeitungswege, keine erteilten Freigaben.

Ein neues Versionsregister und dessen Validator verhindern im Audit die unqualifizierte Gleichsetzung der zwei Bedeutungen von ERR-026. Die 97 Originalkanten, 198 Golden-Originale und ihr Spiegel, historische Dateien, Secret-Baseline und Scannerregeln wurden gegenüber main nicht geändert.

## Vorher / Nachher

| Bestand | Vorher | Nachher |
| --- | ---: | ---: |
| Sieben Golden-Konflikte: konkrete getrennte ausführbare Revisionen | 0 in diesem Revisionsregister | 15 PASS / 0 FAIL |
| Historische Golden-Konflikte geschlossen | 0 | 0; Gegenbefunde erhalten |
| Gesamte zusätzliche Graphproben des Nacht-Audits | 24 | 40 PASS |
| Kanten mit technischen Gegenprüfungen | 45 | 59 |
| Begrenzte Graphstichproben | 38 | 39 |
| Historische Graphkanten FAIL | 1 | 1; CDR-010 bleibt FAIL |
| Offene Graphkanten | 58 | 57 |
| Vollständige unabhängige Graph-Fachabnahmen | 0 | 0 |
| Knowledge-Benchmark | 92 PASS / 0 FAIL / 27 PENDING | unverändert |
| Kerntests | 215 | 235 bestanden |
| Skilltests | 36 | 36 bestanden |

Die zusätzliche gestützte Graphstichprobe ist CR-026: Zweier- und Dreierunterteilungen eines ausdrücklich festgelegten 480-PPQ-Pulses sind gerechnet. Das bestätigt keine Wahrnehmungsnorm und keine universelle Typisierung. Die 15 Revisionsmodelle überlappen inhaltlich mit früheren Golden-Gegenproben; sie werden nicht als 15 zusätzliche ursprüngliche Golden-Fälle gezählt.

## Sieben Golden-Konflikte einzeln

| Original | Konkrete getrennte Vorschläge | Ergebnis / Restentscheidung |
| --- | --- | --- |
| REF-0016 | D-Dur über C-Dur als zwei Dreiklänge; D/C als D-Dur mit C-Bass; Cm als ursprüngliche root/quality-Eingabe. | Drei verschiedene Eingaben/Identitäten gerechnet. D/C enthält nicht automatisch E und G eines unteren C-Dur-Dreiklangs. Variante/Benennung reviewen; CDR-010 nicht umschreiben. |
| REF-0017 | V→I in C ergibt G→C; V7→I ergibt G7→C. | Septime muss in der neuen Eingabe ausdrücklich stehen. Zwischen den beiden klaren Fallversionen entscheiden. |
| REF-0051 | Vollständige Linie A–G#–G–F# über Am–Am(maj7)–Am7–Am6; separat ein verkürzter Ausschnitt A→G über Am→Am7. | Der alte Zweiton-Solltext beschreibt nicht das vollständige viergliedrige Cliché. Register und Umfang sind jetzt explizit. |
| REF-0052 | Fm7–Bb7–Cmaj7–Abmaj7 nach dem Titel; Am–G–F–E7 nach ursprünglichem Input/Ergebnis. | Zwei separate typisierte Akkordfolgen, keine automatische Werk-/Genre-/Transkriptionsabnahme. |
| REF-0062 | Historische PAT-021-Version: 174 BPM, Kicks 0/360/1200/1800 und Ghosts 120/840/1080/1320; aktuelle Kurzfassung: 168 BPM, Kicks 0/600/1200/1560 und Ghosts 360/840/1080. | Werte direkt aus getrennten quellhashgebundenen Texten extrahiert. Historisches Dokument benennt einen Zweitakt-Anspruch, zeigt hier aber ausdrücklich nur einen Auszug des ersten Takts. Kein zweiter Takt erfunden. |
| REF-0063 | PAT-022 historisch 174 BPM, aktuell 175 BPM; beide Kickpositionen aus der jeweiligen Quelle geprüft. | Aktuelle Tabelle nennt GM40 für die Snare; die geprüfte historische Kurzzeile legt hier keine entsprechende GM-Notennummer fest. Nicht ergänzen oder gleichsetzen. |
| REF-0073 | RH F–A–C–E ohne D; Gesamtklang mit LH D und derselben RH. | Die RH ist grundtonlos, der Gesamtklang enthält D. Zwei getrennte Beschreibungen statt pauschalem Rootless-Solltext. |

[Revisionsvorschläge mit Quellenhashes](../../../knowledge/research/golden_cases/CONFLICT_REVISION_PROPOSALS.json) · [15 Einzelprüfungen](GOLDEN_KONFLIKTREVISIONEN_2026-11-14.csv)

Originalklassen und frühere Konfliktbewertungen bleiben erhalten. Der vorhandene 64-Fälle-Prüfplan und das 198-Fälle-Inventar verweisen jetzt auf die konkreten Revisionen.

## Graph: überprüfbare Gegenbeispiele und Entwürfe

- **CR-001:** Das Oktavverhältnis bleibt bei verschiedenen ausdrücklich gesetzten Referenzfrequenzen gleich. Die Abhängigkeit von einer konkreten Referenz gehört an die benannte Umrechnung, nicht pauschal an jeden Frequenzbegriff.
- **CR-008:** Ein konstruiertes 150-Cent-Intervall ist nicht als ganzzahlige 12-TET-Halbtonzahl darstellbar. Die historische REQUIRES-Aussage braucht den Modellgeltungsbereich.
- **CR-015:** C/E hat einen akkordeigenen Bass, C/F# nicht. Nicht jeder Slashbass ist eine Umkehrung.
- **CR-024 / CR-026:** Tonhöhe und Pulsperiode sind getrennte Ereignisparameter; explizite Zweier-/Dreierunterteilungen sind unterschiedliche Raster desselben Pulses.
- **REL-003:** Neuer vollständiger Shell-Satz F4/C5 → F4/B4 → E4/B4 über Dm7/G7/Cmaj7; absolute RH-Bewegung 1 und 1 Halbton. Kein MANDATORY_JAZZ-Nachweis.
- **REL-004:** Unabhängige kartesische Vollsuche bei ±12 Halbtönen pro Stimme, streng aufsteigenden Stimmen und vollständigem Zieltonvorrat. Aus `[62,65,69,72]` nach G7 kostet das unbeschränkte Minimum 3, das Drop-2-beschränkte Minimum 7. Aus einer bereits vorgegebenen Drop-2-Dm7-Lage können beide Minima 3 sein. Der Produktoptimierer stimmt mit dem unabhängigen Suchergebnis überein; es wurde kein Produktfehler behauptet oder hierfür künstlich geändert.
- **REL-008:** Neuer dreigliedriger Drop-2-Satz für PROG-017, auf tatsächliche Drop-2-Form und Akkordtöne geprüft. Keine Klangadjektiv-/Spielabnahme.
- **REL-022 / CR-038:** Neue explizite LH/RH-Lagen für sämtliche Akkorde von PROG-021 und PROG-028. RH ohne Grundton ist vom grundtonhaltigen Gesamtklang getrennt; die Dm9-Ausgangslage benötigt zum Em9-Start eine explizite Transposition.
- **REL-002 / REL-012 / REL-018:** Neue 32-Ereignis-Arpeggiofassung und explizite Zweitakt-Überlagerung. Gemeinsame Tickachsen und Gleichzeitigkeit sind geprüft, Stilpassung und praktische Ausführung nicht.
- **CDR-012 / CDR-017:** Vorhandene D7→Dm7-Qualitätswechselprobe wiederverwendet; 2023-Swing-Regression getrennt vom universellen historischen Decay-Anspruch gerechnet. Historische Zielrichtung und Urheberschaft bleiben getrennt.

[Fortsetzungsmatrix aller ursprünglich 58 offenen Kanten](GRAPH_FORTSETZUNG_58_2026-11-14.csv) enthält Original-ID und Hash, ursprünglichen Relationstyp, Vorschlag, Proben und Restaktion. Vorschläge für geänderte Relationstypen sind reviewpflichtige Alternativen, keine nachträglich als historisch richtig ausgegebenen Tripel.

## ERR-026: Versionsidentität statt stiller Alias

`ERR-026@PHASE4_8_ARCHIVE` bezeichnet die historische Bass-First-Präzisierung; `ERR-026@REGISTER_9AFAF33` bezeichnet die L1-Distanz-Korrektur. Jede Bedeutung ist an ihren tatsächlichen Quellpfad und dessen Hash gebunden. `resolve_error('ERR-026')` verweigert die mehrdeutige Auflösung. Quellenvertauschung, Aliasfreigabe und fingierte Abnahme werden abgewiesen.

Auch die vollständige Graphmatrix führt REL-020 jetzt mit `AMBIGUOUS_VERSIONED_IDENTITY` und beiden Nachweisketten. Die bloße Existenz eines heutigen ERR-026-Eintrags gilt nicht länger als eindeutige Bindung der historischen Kante. Dies ist ein Audit-Prüfpfad, keine neue produktive Graph-API oder automatische Umleitung von P11 zu P10.

[Versionsregister](../../../knowledge/relations/VERSIONED_ERROR_IDENTITIES.json)

## Quellenstand

Die [neue Quellenprüfung](KONFLIKTE_GRAPH_QUELLEN_2026-11-14.json) unterscheidet sieben Abrufe/Prüfumfänge. Die geschriebenen Definitionen für Guide Tones im [Hutchinson-Lehrtext, §31.7.1](https://musictheory.pugetsound.edu/mt21c/JazzChordVoicings.html) und in [Smithers eigener Untersuchung, Absätze 1.6 und 2.1–2.2](https://mtosmt.org/issues/mto.19.25.2/mto.19.25.2.smither.php) stützen den begrenzten Terz-/Septimbegriff. Unsere konkreten Lagen sind eigene Entwürfe.

Der [Lehrtext zu Quartsextakkorden, §26.11](https://musictheory.pugetsound.edu/mt21c/TypesOfSixFourChords.html) nennt Pedal-, Durchgangs- und Kadenzfälle getrennt. Damit wird keine automatische didaktische Wirksamkeit von P11 freigegeben. Aus den Abbildungen wurde keine neue Transkription abgeleitet.

UNIRIO- und UFMG-Surdo-PDFs blieben beim Direktabruf 403. Beim Cristal-Artikel war Einleitungstext zugänglich, die relevante spätere Stelle und PDF dagegen nicht zuverlässig abrufbar. Suchindexauszüge und nicht eingesehene Noten wurden nicht als neue Vollprüfung ausgegeben. CDR-019/CDR-021 und die sechs historischen Definitionslücken bleiben ausdrücklich offen. Es wurden keine Fremd-PDFs oder Notenbilder neu veröffentlicht.

## Konkretes Hör-/Spielmaterial, ohne fingierte Abnahme

Sieben neue Übungen liegen lokal als sieben WAV- und sieben MIDI-Dateien im Nachweisordner `Auditnachweise-2026-11-14/konflikte-graph-hoerproben/`. Die Quellplanfassung ist dort zusätzlich gesichert. Der versionierte [Materialnachweis](GRAPH_PRUEFMATERIAL_2026-11-14.json) enthält Ereignisse, Tempo, Ticks, Dateihashes und Prüfstatus.

Die MIDI-Ereignisse wurden mit Mido unabhängig zurückgelesen und mit dem Ereignisplan verglichen; Note-offs und Zyklusende sind geprüft. WAV-Format, Dauer und Spitzenpegel sind gegengeprüft. Die WAVs sind sinusförmige Tonhöhenkontrollen, keine akustische Klaviersimulation oder Genreaufnahme. Kein menschliches Hören/Spielen wurde behauptet.

```powershell
python -B scripts/render_graph_followup_examples.py <neuer-lokaler-Ausgabeordner> --midi
```

Mido ist nur für die optionale Audit-MIDI-Erzeugung erforderlich und war bereits in der Audit-Umgebung installiert. Ausgabeordner mit vorhandenen Zieldateien werden nicht überschrieben. Ohne `--midi` benötigt der Renderer nur die Standardbibliothek.

Für 14 empirische Kanten liegt eine [leere Korpus-Prüfvorlage](GRAPH_KORPUS_PRUEFVORLAGE_2026-11-14.csv) mit Stichprobenrahmen, Aufnahme-/Quellen-ID, Lizenzfundstelle, Genre-/Harmonie-/Drumannotation, Nennerdefinition und unabhängiger Bewertung vor. Es sind keine Aufnahmen, Annotatoren oder Ergebnisse erfunden. Die Vorlage ist ein Nachweisformat, kein konkurrierender Aufgabenmaster.

## Validierung und Re-Audit

Ausgeführt: 235 Kerntests, 36 Skilltests, Benchmark 92 PASS / 0 FAIL / 27 PENDING. Der Benchmark-Exit 1 ist wegen fehlender Pflichtabnahmen erwartet, kein uneingeschränkter PASS. Der abschließende CI-Stand wird im PR mit dem tatsächlich geprüften Commit dokumentiert.

Zusätzlich: Ontologiehashes und 41 historische Definitionen, Referenzintegrität, Golden-Mirror, API-Referenz und bestehende Sicherheitsbereinigung geprüft. Die 97 Originaltripel, beide Golden-JSONs und die Secret-Baseline/-Regeln sind gegen main unverändert. Die Abdeckungsmatrix wird erst nach Aufnahme aller neuen Dateien in Git mit dem bestehenden Generator aktualisiert und danach geprüft.

Negative Regressionen verändern Sollwerte und Eingaben aller 15 Varianten, Quellenhashes/-pfade, Originalidentitäten, Namespace-Zuordnung, Abnahmeflags, Overlaygrenzen und Voicingtöne. Ein absichtlich falsches Produktoptimierer-Ergebnis mit passender numerischer Distanz wird vom unabhängigen Oracle wegen falschem Zieltonvorrat verworfen. Die technische Schlussprüfung erfolgt durch denselben Agenten; sie ist keine unabhängige menschliche Fachabnahme.

## Restgrenzen und Übergabe

**OPERATIV ABGESCHLOSSEN für dieses Paket:** sieben Konflikte mit 15 prüfbaren Varianten, 16 neue Graphproben, explizite Wiederverwendung einer vorhandenen Probe, Versionsauflösung für ERR-026 und praktische Prüfunterlagen. Keine historischen Gegenbefunde entfernt.

**TECHNISCH BESTANDEN** gilt nur für die tatsächlich dokumentierten Modelle, Tests und Format-/Integritätsprüfungen. Die neue Probe CR-026 erhöht die begrenzte Stichprobenabdeckung; sie ist keine Vollabnahme.

**FACHLICH / RECHTLICH OFFEN:** menschliche Fach-/Hör-/Spiel-/Didaktik-/Coach-Abnahmen, sämtliche sechs historischen Definitionslücken, CSS-Bundle-Rechte und Archivautorität, historische Google-Schlüsselexposition und autorisierte Sicherheitsfreigabe.

**NICHT ABGESCHLOSSEN:** Gesamtaudit, fachliche Annahme/Migration der vorgeschlagenen neuen Fall-/Relationsversionen, Korpusnachweise und die weiterhin unbestätigte Gesamtkonsolidierung des älteren OneDrive-Bestands. [Priorisierte Restblocker](NACHT_RESTBLOCKER_2026-11-14.md) und kanonischer lokaler Aufgabenmaster bleiben maßgeblich.

# STEPS – Research Library V4 · Enzyklopädie und Codex-Fundament

**Stand:** 8. November 2026  
**Version:** `4.0.0-research-draft`  
**Status:** erweiterte, strukturell geprüfte Forschungs- und Lehrmaterialsammlung; **keine vollständig fachbegutachtete Enzyklopädie und kein fertig integriertes Steps-Repository**.  
**Leitbild:** *Steps – An independent, open-source chord progression app for exploring harmony & learning music theory.*

## Was V4 tatsächlich leistet

Die neue Bibliothek bewahrt die vollständige frühere V3 mit den sieben vorherigen V1-Dokumenten und erweitert sie **inhaltlich** um vier gleichberechtigte Säulen: **Music Theory**, **Harmony**, **Chord Progressions** und **Composing**. Anders als die V3 enthält sie 49 neue ausgearbeitete Fachmodule, 15 vertiefte Werkstattanalysen, 131 weitere Progressionsstudien und 30 eigene **16-taktige, mehrspurige, abspielbare MIDI-Lehrminiaturen** mit maschinenlesbaren Note Events. Sie schließt zusätzliche Literaturrecherche, typisierte Regeln, ein eigenes Validierungsskript und einen Codex-Masterauftrag mit 20 Arbeitspaketen an.

**Die Größenordnungen richtig lesen:** 77 Quellen-/Editions-/Metadateneinträge sind **keine** 77 vollständig gelesenen Primärwerke; 226 Progressionsdatensätze enthalten Varianten und eigene illustrative Studien; 30 MIDI-Etüden sind geprüfte Datenstrukturen, keine professionell komponierten oder musikfachlich begutachteten fertigen Werke. Die V4 enthält **20.099 bestandene mechanische Einzelprüfungen**, nicht 20.099 unabhängige wissenschaftliche Experimente.

## Einstieg und Lesereihenfolge

1. **Gesamtbild:** `RESEARCH_SYNTHESIS_V4.md`, `VERSION.md`, `CHANGELOG.md`.
2. **Fachliche Grundlage:** die fünf thematischen Bände in `01_Studienbaende/`; danach die **15 vertiefenden Werkstattanalysen**.
3. **Konkretes Fachmaterial:** `02_Fachlexikon/` (163 Themen, 136 typisierte Regelentwürfe inklusive Historie); `03_Progressionsatlas/` (226 Fälle inklusive Historie).
4. **Composing mit abspielbaren Daten:** `04_Kompositionslabor/README.md`, `TECHNIKEN_V4.md` und die 30 Studien `Partituren/ETUDE-V4-xxx.md`, `*.json` und `MIDI/*.mid`.
5. **Quellen und Verifikation:** `05_Quellen/QUELLENKOMMENTAR_V4.md`, `QUELLENREGISTER_V4.json` und `09_Governance/CLAIM_PROVENANCE_AND_LEGAL_GATE.md`.
6. **Technischer Datenvertrag:** `06_Datenmodelle/*.schema.json`.
7. **Für Codex:** zuerst `07_Codex/PROJECT_CONTEXT_HANDOVER_V4.md`, dann **`07_Codex/CODEX_MASTER_EXECUTION_V4.md`**, dazu das V1-Handover in `00_HISTORISCH_V3/00_Archiv_V1/`.
8. **Abnahme:** `08_Validierung/STATUS_UND_OFFENE_LUECKEN.md`, `MECHANISCHER_PRUEFBERICHT_V4.json`, `TESTFALLKATALOG_V4.json`; den Validator selbst mit Python ausführen.

## Fachbereichs- und Dateikarte

| Abschnitt | Inhalt | Was bereits vorliegt | Was noch fehlt |
|---|---|---|---|
| `01_Studienbaende/01_MUSIC_THEORY_V4.md` | Tonhöhe, Intervall, Tonsysteme, Notation, Skalen, Metrik, Form, Kognition | contextualisierte Fachkapitel und Beispiele | Exakte Fachquellen-Locators pro Claim, Fachreview |
| `01_Studienbaende/02_HARMONY_V4.md` | Klassik, modal, chromatisch, Jazz, Pop, Blues, Transformation | mehrere Analyse-Lenses und Gegenbeispiele | stilbezogene Expertenprüfung, Quellenarbeit |
| `01_Studienbaende/03_CHORD_PROGRESSIONS_V4.md` | Progressionstypen, Harmonic Rhythm, Bass, Mehrdeutigkeit, Ranking | analysierte Varianten, neue Atlas-Objekte | externe Repertoire-Belege, kanonische statistische Frequenzen |
| `01_Studienbaende/04_COMPOSING_V4.md` | Motiv, Melodie, Kontrapunkt, Form, Arrangement, Instrumentation, Verfahren | eigene fachliche Kompositionssäule | tiefes Form-/Orchestrierungsreview an realen Scores |
| `01_Studienbaende/05_KONTEKSTE_KOGNITION_STANDARDS_V4.md` | Psychologie, Kulturgrenzen, Standards und Datensysteme | Querschnittsmodelle und Einschränkungen | traditionsspezifische Fachstudien |
| `01_Studienbaende/06_VERTIEFENDE_WERKSTATTANALYSEN_V4.md` | 15 längere Originalfälle | praktische Analysen und Prüfvorschläge | musikalische externe Begutachtung |
| `02_Fachlexikon/` | Regeln, Taxonomie | 163 Themen, 136 Regeln inkl. V3 | Claim-Prüfung bis auf Passagebene |
| `03_Progressionsatlas/` | Akkordfolgen | 226 Datenfälle inkl. V3 | jede Tonart-/Stufen-/Stilzuordnung reviewen |
| `04_Kompositionslabor/` | Techniken, Etüden | 134 Methoden inkl. V3, 30 MIDI-Lehrstücke | qualitative Revision, echtes Notenbild/MusicXML |
| `05_Quellen/` | Literatur und technische Standards | 77 Quellen-/Editionsdatensätze | eindeutige Deduplikation, exakte bibliografische Einzelnachweise |
| `08_Validierung/` | Code, Tests und Report | ausgeführter mechanischer Validator | Peer Review und belastbare Regressionstests an externer Musik |

## Musiktheoretische Leitplanken

- **Deutsches `H` = internationales `B`; deutsches `B` = internationales `Bb`**. Die tonal begründete Schreibweise bleibt neben MIDI-Pitch Class erhalten.
- *Rule*, *tendency*, *heuristic* und *interpretation* sind unterschiedliche Kategorien. Ein atypischer harmonischer Übergang ist nicht automatisch ein Fehler.
- Eine Akkordfolge ohne Melodie, Bass, zeitliche Gewichtung, Form und Stil darf mehrere plausible Tonika- und Funktionsanalysen behalten.
- Blues, Gospel, Rock, Jazz, Klassik, modale Musik und nichtwestliche Traditionen dürfen nicht in eine angeblich universelle klassische Funktionstheorie gezwungen werden.
- Der gegenwärtige Schwerpunkt umfasst **Rhythmus, Metrum und Zeit als kompositorische Theorie**. Eine produktive Drum-Engine, Genre-Drum-Grooves und deren Korpora sind weiterhin **deferred**.
- Externe Fachbücher und geschützte Noten-/Audio-Beispiele **nicht** ohne geklärte Nutzungsrechte in ein öffentliches Git-Repository übernehmen.

## Sofortiger Codex-Start

Importiere das Paket nach einem **read-only Repo-Audit** in eine nachvollziehbare bestehende Steps-Dokumentationsstruktur. Führe `python 08_Validierung/validate_v4.py` aus, prüfe dann zunächst echten Quellennachweis, Akkordsymbol-, Stufen- und Zeitmodelle, die 30 Etüden und das bestehende `SKILL.md`. Fülle die Knowledge Base tatsächlich mit geprüften Objekten; ein weiterer leerer Ordnerbaum oder bloße Architekturpapier-Neufassung reicht nicht. **Kein Merge ohne gesonderten Auftrag.**

## Versionshistorie

`V1` = ursprüngliche sieben Markdown-Dokumente; `V3` = vorherige breitere Bibliothek mit 142 Konzeptentwürfen, 77 Regeln, 95 Progressionen, 69 Composing-Techniken und 19 Skizzen; `V4` = eigenständiger inhaltlicher Ausbau plus vollständiges V3-Archiv. Eine unabhängige V2-Quelldatei wird nicht als in diesem Paket verfügbar behauptet. Die tatsächlichen 20 ursprünglichen Musikbuch-PDF/TXT-Anhänge und ein separates finales älteres Deep-Research-Paper sind in diesem ZIP **nicht als Originaldateien nachgewiesen**.

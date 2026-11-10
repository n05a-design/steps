# Research-to-Knowledge-to-Codex – Nachverfolgungsmatrix V5

Diese Matrix verknüpft die **bestehenden** Forschungsanker mit aktuellen Lehrbeispielen und noch zu implementierenden Prüfungen. Ein „source-ID“ ist nur dann ein fachlicher Beleg, wenn im Quellenregister eine tatsächlich eingesehene Stelle hinzukommt; er kann auch ein Forschungsanker sein. Die Matrix ist als Migration-/Reviewhilfe für Codex gedacht.

| Thema und Claim | Forschungsanker / Status | V5-Artefakt | Geplanter ausführbarer Test | Fallstrick / Gegenbeispiel | Codex-Arbeitspaket |
|---|---|---|---|---|---|
| Tonklasse ≠ Notenschreibung | V5-001, Textabschnitt | `01_MUSIKTHEORIE_V5.md`; V5-CASE-001–003 | `F#` vs `Gb` pc6 und korrektes Intervall | C→Fb ist verminderte Quarte, nicht große Terz | P07–P08 |
| Lokale Tonika vs globale Tonart | V5-001, didaktische Synthese | `02_HARMONIE_V5.md`; V5-CASE | Sekundärdominante V/ii ohne Tonartwechsel | Nicht jede Applied Dominant moduliert | P10–P12 |
| Function vs progressional tendency | V5-001, V5-002 teilgelesen | `02_HARMONIE_V5.md` | typed rules, exceptions | V7 muss nicht zwingend I erreichen | P11/P13 |
| Phrase vs song form | V5-002 und V5-003, verschiedene Stile | `04_COMPOSING_V5.md` | `classical_sentence` nicht auf Rock-Verse ohne Beweis anwenden | Acht Takte ≠ automatisch Periode | P22–P24 |
| Abwesende/fragile Tonika | V5-005, offener Text | `03_CHORD_PROGRESSIONS_V5.md` | fehlende Tonika zulassen | automatische I-Erfindung | P14/P19 |
| Korpus und Stichprobe | V5-009, thematischer Bezug; V5-011 Choco | `06_COMPUTATIONAL_MUSIC_V5.md` | ranker reports corpus/sampling N | absolute Richtigkeitsbehauptung | P29 |
| Chromatische Voice Leading | V5-015, Verlagsseite | `02_HARMONIE_V5.md` | pc shared / semitone voice metrics | geringster Distanzwert ≠ musikalische Qualität | P18 |
| Pop-Form/Harmony | V5-003, Abstract/Buchindex | `03_CHORD_PROGRESSIONS_V5.md` und `04_COMPOSING_V5.md` | sectional harmonic intent contract | Songtitel/-Textebene ≠ Harmonieanalyse | P19/P24 |
| Musiknotation auf Austausch | V5-024, offizieller Standard | `04_Kompositionslabor/*.musicxml` | XML durations / Instrument voices | MIDI allein erhält Enharmonik nicht | P30 |
| Musikalische Ereignisse und Audio | V5-025, offizieller MIDI-Standard | `04_Kompositionslabor/*.mid` | note-on/off balances, ticks | Valid MIDI ≠ idiomatische Komposition | P30 |
| Open Source vs Corpus-Reuse | V5-011, V5-013 | `06_Quellen_und_Rechte/` | per-subset rights flag | software license ≠ score redistribution | P02–P04 |
| Maqam/Raga-Domäne | V5-020/021, partiell gelesen | `05_KOGNITION_KULTUR_STIL_V5.md` | tradition tag, scope/review flags | westliche Triadenlogik wird auf fremde Praxis projiziert | P28 |
| Motivvariation | pedagogical_synthesis, eigene Originalstudien | `04_COMPOSING_V5.md`, `04_Kompositionslabor/` | rhythm/pitch transformation trace | Sequenz ≠ Umkehrung | P22 |
| Arrangement/Instrument | didaktische Synthese | `04_COMPOSING_V5.md` | voice range constraints | korrekte Tonklasse ≠ spielbares Voicing | P26 |
| 53 Progressionsfamilien | eigene redaktionelle Lehrfälle | `05_Wissensobjekte/KURATIERTE_PROGRESSIONSFAMILIEN_V5.json` | key/chord/degree id integrity | didaktische Muster sind keine gezählten Corpusfrequenzen | P16/P20 |
| 1.378 Varianten | programmgeneriert | `05_Wissensobjekte/TRANSPONIERTE_PROGRESSIONSVARIANTEN_V5.json` | transposition + duration sums | Varianten ≠ unabhängige empirische Belege | P16 |
| 16 × 32-Takt-Etüden | originale Algorithmik, ohne Expertenreview | `04_Kompositionslabor/Partituren/` | timed voice count, MIDI/XML parsing | syntaktisch gültig ≠ kompositorisch überzeugend | P25/P27 |
| 60 positive/negative Fälle | Theorie-Entwürfe ohne Testausführung | `08_Validierung/CONCEPTUAL_GOLDEN_AND_NEGATIVE_CASES_V5.json` | Implementierung in `pytest` nach Klärung | Label-only ≠ Test bestanden | P31 |

## Pflege und Fortschrittsmatrix

Jede Matrixzeile sollte im echten Steps-Repository zu einem Eintrag werden mit `trace_id`, `finding_id`, `source_id`, `locator`, `review_status`, `object_ids`, `test_ids`, `code_paths`, `risk_id`, `last_checked`, `owner`, `version`. Das Quellenregister darf den exakten Locator nur dann eintragen, wenn der Abschnitt tatsächlich gesehen wurde. Fehlende Beweise bleiben `unverified`, ohne Zahlendruck auf `reviewed` zu ändern.

**Ablauf:** Erst P00–P05 (Reality/Source), dann P06–P21 (Domain/Progressions), dann P22–P27 (Composing), danach P28–P34 (Interoperabilität/Evaluation/Skill/PR). Die P-IDs beziehen sich auf `07_Codex/CODEX_MASTER_EXECUTION_V5.md`.

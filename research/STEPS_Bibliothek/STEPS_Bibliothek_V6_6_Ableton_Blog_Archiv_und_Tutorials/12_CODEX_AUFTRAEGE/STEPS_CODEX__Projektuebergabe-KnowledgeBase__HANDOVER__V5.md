# STEPS — PROJECT_CONTEXT_HANDOVER V5

**version:** `5.0.0-research-draft` · **date:** `2026-11-08` · **status:** `draft` · **project:** Steps.

## 1. Bindendes Projektbild

Steps ist eine unabhängige Open-Source-Anwendung für die Erforschung von Harmonielehre und Akkordfolgen und das Erlernen von Musiktheorie. Die Forschungs-/Wissensgrundlage wird jetzt ausdrücklich auf **vier gleichberechtigte Säulen** erweitert: **Music Theory, Harmony, Chord Progressions, Composing**. Composing ist nicht eine bloße Funktion des Akkordgenerators. Melodie, Motive, Form, Kontrapunkt, Arrangement, Instrumentation und Revision gehören zu seiner eigenen Domäne. Die frühere Beschränkung „drums/grooves nur spätere Roadmap“ bleibt bestehen; Rhythmus, Metrum und Harmonic Rhythm werden jetzt als Musik- und Kompositionskontext behandelt.

## 2. Maßgebliche Zeitfolge und Paketrealität

- V1: sieben ursprüngliche historische Markdown-Dateien, darunter ein vollständiger `Master-Research-Prompt.md` und ein damals ausgearbeitetes `PROJECT_CONTEXT_HANDOVER.md`. Eine ältere README, die das Handover für noch ausstehend erklärt, ist **historisch** und kein aktueller Sachstand.
- V3: frühere Theorie-/Progression-/Composing-Kataloge und Codex-Prompt; inzwischen im V4-Archiv enthalten.
- V4: umfangreichere Text-/Daten-/MIDI-Sammlung mit 30 Lehr-Etüden, 20 Codex-Paketen und mechanischem Prüfbericht; **nicht** unabhängig vollständig fachbegutachtet. In diesem V5-Archiv als `00_ARCHIV_V4_Unveraendert/` in seinem Dateistand erhalten.
- V5: zusätzliche neue externe Quellenabgleiche, sechs neue Studienbände, zwölf neu vertiefte Werkstattfälle, 53 handkuratierte neue Progressionsfamilien, 1.378 aus diesen abgeleitete transponierte/timierte Varianten und 16 neue originale maschinenlesbare Lehrstudien zu je 32 Takten. Diese Datensätze sind technisch geprüft, aber musikfachlich noch nicht umfassend freigegeben.

**Nicht nachgewiesen:** Ein Git-Repository-/Branchzustand von Steps, CI, tatsächlich implementierte Module, vollständige Rechte für die 20 ursprünglichen Bücher/PDFs/TXT-Dateien, vollständiger textbasierter Zugriff auf alle wissenschaftlichen Primärbücher, unabhängige Fachreviews sämtlicher Theorie- und Kompositionsdaten. Eine Darstellung als „fertige App/Knowledge Base“ ist unzulässig.

## 3. Eingaben für Codex

1. Aktuelle V5-README und die sechs V5-Studienbände.
2. `01_Neuforschung/00_FORSCHUNGSSTAND_V5.md`.
3. `03_Analysewerkstatt/01_ZWOELF_VERTIEFTE_WERKSTATTFAELLE.md`.
4. `05_Wissensobjekte/` mit originalen Familien und ausführlichen Transpositionsvarianten.
5. `04_Kompositionslabor/` mit MIDI, MusicXML, JSON, Kompositionsabsichten und Prüffällen.
6. `06_Quellen_und_Rechte/` mit genauem Web-Prüfstatus.
7. `08_Validierung/` und ausgeführter Validator.
8. Historisch: unveränderte V4, darin V3 und die sieben V1-Dateien, einschließlich bereits erstelltem `PROJECT_CONTEXT_HANDOVER_V1.md`.
9. Echte angehängte Originalquellen und das echte Steps-Git-Repository, **nur sofern im konkreten Codex-Lauf zugänglich**.

## 4. Statushierarchie

`CONFIRMED`: user decisions/project scope; `EXISTING_HERE`: Datei in dieser V5-Archivkopie; `TECHNICALLY_VALIDATED`: syntaktische/arithmetische Tests; `SOURCE_METADATA_CHECKED`: verifizierte Landingpage; `SOURCE_SECTION_CHECKED`: konkreter zugänglicher Textabschnitt; `RESEARCH_SUPPORTED`: enger Quellenbezug; `PEDAGOGICAL_SYNTHESIS`: eigenes Lehrbeispiel; `PROPOSED`: Architektur-/Produktvorschlag; `REVIEW_REQUIRED`: fachlicher Prüfschritt offen; `UNKNOWN`: nicht nachgewiesen; `DEFERRED`: spätere Erweiterung.

Die Projektleitung hat **nicht** allgemein alle analytischen Modelle, Akkordrankings, GUI-Entwürfe oder Imports freigegeben, nur weil diese in den Research-Dokumenten stehen.

## 5. Wichtigste fachliche Erkenntnisse und Konflikte

- Key-Spelling, Tonklasse und Stimmung müssen separierbar sein; Deutsch H/B beachten.
- Ein akkordischer Ausschnitt kann mehrere Funktions- und Tonikaanalysen besitzen.
- Klassische Kadenzkriterien sind nicht automatisch auf Blues, Poploops, Jazz oder modal zentrierte Musik übertragbar.
- Sekundärdominante und Modulation sind nicht gleichbedeutend.
- Transformation/Voice Leading ist von funktionaler Grundtonbewegung getrennt.
- Motiv, Melodie, Form und Arrangement sind zuerst eigene Composing-Objekte, nicht Spalten einer Progression-Tabelle.
- Empirische Korpusfrequenzen sind von Stichprobe, Segmentierung und Genre abhängig; „wahrscheinlich“ bedeutet nicht „musikalisch richtig“.
- Maqam/Raga/afrikanische Musiktraditionen erfordern traditionsspezifische Theorie, Quellen und Reviews, nicht ein allgemeines westliches Skalen-Overlay.
- `Source Access` ≠ `Source Read` ≠ `Claim Verified` ≠ `Reuse Allowed`.

## 6. Besonders wichtige V5-Quellen

[V5-001] Open Music Theory: offenes Lehrmaterial; [V5-003] Nobile: form-harmony Pop/Rock; [V5-005] Spicer: fragile/emergente/fehlende Tonika; [V5-007] Temperley: Rock-Kadenzen und Korpusgrenzen; [V5-010] DCML: komplexe Tonart-/Harmonieannotation; [V5-011] ChoCo: heterogene Korpora und Lizenzunterschiede; [V5-012] When in Rome: Funktionsanalysen und Lizenzherkunft; [V5-013] music21: Quellcode-/Corpus-Lizenz-Trennung; [V5-020] Maqam; [V5-021] Raga; [V5-022] Agawu zu Kontext/Representation. Der genaue Prüftyp je Quelle steht im JSON, nicht in dieser Zusammenfassung.

## 7. Daten und Qualitätszahlen – korrekt interpretiert

V5 bietet **53 neu handdefinierte** didaktische Progressionsfamilien und **1.378 algorithmische Varianten** aus 13 Tonarten × zwei Dauerschemata. Die Varianten sind nicht 1.378 empirisch unterschiedliche Songs. Es gibt **16 neue** 32-taktige Lehrskizzen mit MIDI, MusicXML und JSON; nicht 16 vollständig manuell komponierte/extern begutachtete Werke. Die technische Validierung ist von einer musikalischen Prüfung zu unterscheiden. V4 bleibt separat und darf hinsichtlich Alter/Status nicht stillschweigend zur geprüften V5-Forschung hochgestuft werden.

## 8. Noch offene Aufgaben – Prioritätsliste

**P0:** Echter Repo-/License-Audit, source locator mapping, richtige H/B-Schreibweise, exakte Erfassung bereits vorhandener Module, mechanische Regressionen. **P1:** Konzept-/Rules-Review auf Anspruch und Quellenstelle; Composing/Motif/Section-Schema und 16 neue Etüden durch Musiker prüfen; MusicXML-Enharmonik; Mehrdeutigkeit/Style Lenses. **P2:** repräsentative Corpus-Validierung, lizenzierte Beispielauswahl, instrumentengerechte Voicings und umfangreiche echte Kompositions-Revisionen. **P3:** Skill-Referenzen und erklärbare UI/API. **Later:** ML/korpusbasierte Rankings, Drum-Engine und Genre-Drum-Datensätze.

## 9. Erster Codex-Arbeitsschritt

Den tatsächlichen Repository-Zustand **read-only** prüfen; vorhandene Struktur, AGENTS, Skills, Dokumentation, Tests, Lizenz und Builds erfassen; vorhandene KB-Objekte und V5-Objekte deduplizieren. Danach neuen Branch für dokumentierte, inkrementelle Änderungen; ohne Auftrag weder main aktualisieren noch mergen. Ein Reviewbericht muss ausdrücklich `implemented`, `tested`, `review_required`, `blocked`, `not_started` unterscheiden.

## 10. Entscheidungs- und Risikoregister (Kurzform)

| ID | Status | Sachverhalt |
|---|---|---|
| V5-DEC-001 | CONFIRMED | Vier gleichrangige Säulen einschließlich Composing |
| V5-DEC-002 | CONFIRMED | Wissensbasis vor endgültiger Skill-Verdichtung |
| V5-DEC-003 | CONFIRMED | Drum-Datensätze/-Engine deferred, Kompositionsrhythmik im Scope |
| V5-DEC-004 | PROPOSED | Multi-Lens-Analyse, getrennte Grammatik- und Corpus-Scores |
| V5-DEC-005 | PROPOSED | Neue V5-Objekte als kanonischen Importstandard adaptieren – erst nach Repo-/Schema-Check |
| V5-RISK-001 | OPEN | Patent-/Copyright-/Dataset-Source-Redistribution |
| V5-RISK-002 | OPEN | `landing_page_checked` fälschlich als vollständigen Buchreview interpretieren |
| V5-RISK-003 | OPEN | Mechanische Midi-/MusicXML-Prüfung fälschlich als musikalische Validierung darstellen |
| V5-RISK-004 | OPEN | Erweiterte Beispiele nutzen enharmonisches Exportspelling ohne Kontextreview |
| V5-RISK-005 | OPEN | Unterschiedliche historische Dokumentversionen als gleichzeitig aktuelle Fakten behandeln |

## 11. Nächster Hauptauftrag

`07_Codex/CODEX_MASTER_EXECUTION_V5.md` ist die verbindliche Arbeitsvorlage für den **konkreten Ausbau im Repository**. Dieses Handover ist die Kontextübergabe, kein Ersatz für V1-Handover, Forschung, Quellen und Tests.

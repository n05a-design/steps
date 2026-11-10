# STEPS – Qualitäts-, Evidenz- und Forschungs-Gap-Register V3

**Warnhinweis:** Strukturvollständigkeit, Fachrichtigkeit, Quellenbeleg und Veröffentlichungserlaubnis sind vier unabhängige Prüfschichten. Eine JSON-Datei kann strukturell valide sein und dennoch musiktheoretisch einen Fehler enthalten. Das Paket ist als erweitertes Seed-Fundament und neuer Codex-Auftrag geeignet, **nicht** als fertig peer-reviewte Enzyklopädie.

| ID | Priorität | Offener Befund | Nächster überprüfbarer Schritt | Gate |
|---|---|---|---|---|
| GAP-V3-001 | P0 | Steps-Repo/Branch/Tk-Code nicht eingesehen | Read-only Git- und Dateibaum-Audit | Bestand separat dokumentieren |
| GAP-V3-002 | P0 | 20 Original-PDF-/TXT-Quellen nicht im Paket | Verfügbarkeit, SHA, Lese-/Lizenzstatus prüfen | Keine stillschweigenden Exzerpte |
| GAP-V3-003 | P0 | V2-Archiv nicht physisch in dieser Session gemountet | Bei Verfügbarkeit Inhaltsvergleich | Keine behauptete V2-Dateiintegration |
| GAP-V3-004 | P0 | Alte Handover-Behauptung Master-Prompt fehlt, inzwischen falsch | V3-Handover als aktuell ausweisen | V1 unverändert archivieren |
| GAP-V3-005 | P0 | Monografien meist nur per Landing-Page/Abstract erfasst | Legalen Volltext/Originalabschnitte lesen | Kein exakter Claim ohne Locator |
| GAP-V3-006 | P0 | Ungeprüfte bibliografische Kandidaten | 50 Kandidaten einzeln verifizieren | Kein DOI/ISBN erfinden |
| GAP-V3-007 | P0 | 142 Konzeptkarten nur redaktionelle Drafts | Claim-Level Source Evidence und Review | `reviewed` erst nach Prüfung |
| GAP-V3-008 | P0 | 95 Progression-Drafts benötigen Harmoniesymbol-/Stufenprüfung | Symbolische + fachliche Golden Cases | Alle Korrekturen versionieren |
| GAP-V3-009 | P0 | 19 Composing-Studien sind nur Skizzen | Vollständig notierte Original-Miniaturen erzeugen | Vor Score-Behauptung MIDI/MusicXML prüfen |
| GAP-V3-010 | P0 | Testfälle sind großenteils nur spezifiziert | Validierung in Repo ausführen | `executed/pass/fail/skipped` belegen |
| GAP-V3-011 | P1 | Jazzharmonik inkl. Voicings unterrepräsentiert | Fachtext-/Musikbeispiele samt Guide-Tones | Stilkontext prüfen |
| GAP-V3-012 | P1 | Gospel/Neo-Soul/R&B vorläufig und ohne spezifische Primärliteratur | Historisch/ethnomusikalisch recherchieren | Keine pauschalen Genreschemata |
| GAP-V3-013 | P1 | Pop-Form und Rhythmik brauchen mehr annotierte Beispiele | Songform-/Hypermetrik-Forschung eingliedern | Lizenz- und Corpus-Gate |
| GAP-V3-014 | P1 | Nichtwestern Musiksysteme nur vorsichtig gesichtet | Traditionsexperten/Originalquellen und eigenständige Modelle | Kein 12-TET-Zwang |
| GAP-V3-015 | P1 | Tonale Spannung ist nicht objektiv ein Einheitswert | Hörer-/Stilmodelle getrennt evaluieren | Hypothesenkennzeichnung |
| GAP-V3-016 | P1 | Chromatische P/L/R-Transformationen nur Seed-Beispiele | Mathematisch korrekte Formale Tests | Enharmonik/Voicing trennen |
| GAP-V3-017 | P1 | Pitch-Class-Set-/Seriell-/Algorithmic-Domänen noch grob | Primärliteratur, ausführbare Transformationsregeln | Tradition kennzeichnen |
| GAP-V3-018 | P1 | Instrumentenrange und idiomatische Orchestration nicht formalisiert | Bibliografie + registrierte Instrumentenprofile | Spielbarkeitstests |
| GAP-V3-019 | P1 | Rechte von Korpora/Noten und CC-SA-Textadaptationen | Legal-/License-Review pro Ressource | Keine unberechtigten Reuploads |
| GAP-V3-020 | P1 | ML und Corpus-Statistik als künftige Option | Bias-/Scoring-Benchmarks nach deterministischer Prüfung | Kein erfundener Probability Score |
| GAP-V3-021 | P2 | Kompositions-UX noch nicht getestet | Nutzerworkflows und A/B-Aufgaben pro Stil | Produktentscheidung gesondert |
| GAP-V3-022 | P2 | Angewandte Pädagogik/Kompetenzstufen offen | Pre-requisite graph und Aufgaben-Evals | Fachliche Didaktikreviews |
| GAP-V3-023 | P2 | Drum-/Groove-Engine absichtlich ausgeschlossen | Zukunfts-Roadmap führen | Scope respektieren |
| GAP-V3-024 | P1 | Chord Symbol/Score/MIDI/MEI-Roundtrips ungeprüft | Abhängigkeits-/Formatvergleich und Tests | Loss Report je Konversion |

## Reviewverfahren

1. **Citation Review:** Verifizierte Titel/Edition/Autor/URL reichen für Bibliografie, nicht für eine exakte fachliche Behauptung. Ergänze `source_id + chapter/page/section + access proof`.
2. **Music Review:** Stimmen/Bass/Pitches/Chords/Keys im konkreten Kontext prüfen. Bei Pop-/Modal-/Blues-Lenses alternative Erklärungen zulassen.
3. **Composing Review:** Jede konkrete Studie muss rhythmisch zugeordnet, motivisch kohärent, harmonisch erklärbar, instrumental spielbar und rechtlich originär sein.
4. **Technical Review:** IDs/JSON-Validität, Schemas, Referential Integrity und Versionsfelder prüfen; Testläufe protokollieren.
5. **Governance Review:** Entscheidung, Interpretation, Hypothese, Forschungsstand und Nutzerfreigabe getrennt halten.

## Warnung vor Zahlenspielerei

95 Prog-Records umfassen verwandte Transpositions-/Rotations-Varianten, 47 Quellenrecords enthalten Editionen/Metadaten und Rezensionen, 110 QA-Records enthalten vorgeschriebene manuelle sowie maschinelle Fälle. Diese Zahlen dürfen **nicht** mit 95 unabhängigen akademischen Befunden, 47 vollständig gelesenen Primärwerken oder 110 bestandenen Engine-Tests verwechselt werden.

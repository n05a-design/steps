# STEPS V5 – dauerhafter Gap-, Risiko- und Entscheidungsbestand

**Statuscodes:** `CONFIRMED` = vom Nutzer als Projektrichtung bestätigt; `EXISTING_HERE` = nur in der Forschungssammlung vorhanden; `PROPOSED` = fachliche/technische Empfehlung; `REVIEW_REQUIRED` = inhaltlich nicht freigegeben; `UNKNOWN` = noch nicht nachgewiesen; `DEFERRED` = bewusst spätere Entwicklungsphase.

## Bestätigter Scope und Nichtentscheidungen

**CONFIRMED:** Steps = unabhängige Open-Source-Anwendung; vier gleichberechtigte Säulen Music Theory, Harmony, Chord Progressions und Composing; auf Dauer erweiterbare wissensbasierte Forschung; nachvollziehbare, zitierbare Fachquellen; ursprüngliche Materialien erhalten; Umsetzung durch Codex auf Grundlage des tatsächlichen Repositories. **DEFERRED:** Drum-Groove-Engine und Drum-Korpora, auch wenn Rhythmus, Metrik und Harmonic Rhythm fachlich jetzt zur Komposition gehören.

**Nicht bestätigt:** konkrete Auswahl einer Musikbibliothek, Host-/Plugin-Technik, App-UI, Engine-Algorithmus, öffentliche Softwarelizenz, Skill-Pfad, Genre-Priorität, MVP-Scope, CI-Konfiguration oder Merge. Eine V5-Rechercheempfehlung ist kein Nutzerbeschluss.

## Fachliche und technische Prioritätslücken

| ID | Priorität | Problem / Risiko | Warum relevant | Nächste evidenzbasierte Maßnahme | Fertig, wenn ... |
|---|---|---|---|---|---|
| G-V5-01 | P0 | Echtes Steps-Repository nicht gesehen | Bestandsfiktion / Duplikate | Git-/Test-/Architektur-Audit durch Codex | Commit, Branch, vorhandene Module und Tests belegt |
| G-V5-02 | P0 | Keine wissenschaftliche Einzelquellenbelegung für alle Theoriekarten | Falsche Autoritätsbehauptung | Claim-zu-Locator-Mapping | Claim mit wirklich gelesenem Abschnitt nachweisbar |
| G-V5-03 | P0 | Unterschied `metadata_checked` vs `fulltext_read` | Inhaltsüberdehnung | Evidenzstatus pflegen | Kein Abstract als Volllektüre bezeichnet |
| G-V5-04 | P0 | Original-PDFs nicht automatisch zugänglich | Nicht haltbare Leseclaims | Eingangsmaterial erfassen | read_status je Datei echt belegt |
| G-V5-05 | P0 | Quell- und Musikrechte unklar | Unzulässiger öffentlicher Import | License-Gate, getrennte Rohdaten | Klare Redistribution/Attribution je Objekt |
| G-V5-06 | P0 | Eng/deutsch H/B/Enharmonik | Falsche Schreibweise, Intervallqualität | Spelling Tests | Musikalisch richtige Noten-/Intervallnamen für Testfälle |
| G-V5-07 | P0 | Quell-zu-Claim-Status nicht produktiv durchgängig | Scheinsicherheit | Provenienzindex und Resolver | Alle freigegebenen Claims rückverfolgbar |
| G-V5-08 | P0 | Schema-Duplikate aus V1/V4/V5 | Langfristige Inkonsistenz | Content-/Schema-Migrationsvergleich | IDs/Versionen synchron, Altdaten nicht verloren |
| G-V5-09 | P1 | Formkategorien nicht genreübergreifend gültig | Classical-overgeneralization | Caplin vs Nobile getrennt annotieren | Formbegriff besitzt Schule/Scope und Gegenbeispiel |
| G-V5-10 | P1 | Tonalität aus Akkorden allein überdeterminiert | Erfundene Tonika und Modulation | Multi-key-/absent-tonic-Test | Unsicherheit zulässig, begründet |
| G-V5-11 | P1 | Sekundärdominanten vorschnell als zwingende Auflösung | Falsche Regeln | Typisierung `tendency` statt `invariant` | Gegenbeispiel und Auflösungstest |
| G-V5-12 | P1 | Pop-/Rock-Modelle mischen Harmonie und Textetikett | Strukturfehler | Eigenständige Song-Form-Fälle | Vor-/Refrainfunktion vs tatsächliche Harmonik getrennt |
| G-V5-13 | P1 | Jazz/Blues-Harmonik inadäquat klassisch generalisiert | Falsch klassifizierte Dominantqualitäten | Jazz-/Blues-Lens mit Review | Zwei alternative, stilbezogene Lesarten testbar |
| G-V5-14 | P1 | Voice-leading-Metrik verwechselt Geometrie mit Ästhetik | Schädliche Rankings | Ranking-Layers und Registertests | Metrik transparenter Hilfsindikator, nicht Qualitätsbeweis |
| G-V5-15 | P1 | 16 neue algorithmische Etüden nicht musikalisch begutachtet | Falscher Qualitätsanspruch | Musiker reviewt Form, Klang, Satz, Kontrapunkt | Review-Status explizit mit Problemen/Fixes |
| G-V5-16 | P1 | MusicXML und MIDI nicht auf volle musikalische Semantik roundtrip geprüft | Verlorene Enharmonik / Voicing | Symbol-/Noten-/Roundtrip-Tests | Abweichungen bekannt und akzeptiert |
| G-V5-17 | P1 | Composing-Techniken nur partiell als Operationen formalisiert | App nicht generatorfähig | Motivtransformationen + Constraints | Beispiele mit Original-, Resultat-, Transformationsnachweis |
| G-V5-18 | P1 | Instrumentenbesonderheiten unvollständig | Unspielbare Voicings | Instrument-Ranges/Techniques ergänzen | Instrumental-Voice Testfälle |
| G-V5-19 | P1 | Rhythmus und Harmonic Rhythm in Daten ungleich erfasst | Fehlende formale Wirkung | Time-signature/phrase-boundary schema | 3/4/4/4/6/8 und Harmonie-Ereignisse testbar |
| G-V5-20 | P1 | Traditionelle Maqam/Raga-Systeme unterrepräsentiert | Ethnozentrische Fehlmodellierung | Expert*innen mit traditionsspezifischem Corpus | Kein fremdes System auf westlichen Dreiklang reduziert |
| G-V5-21 | P2 | ChoCo/When-in-Rome Lizenz/Annotator-Bias | Unzulässiger Import oder falsche Statistik | Dataset-Permissions/Mappings | Datensatzsubset, Bias, Attribution dokumentiert |
| G-V5-22 | P2 | Originalquellen enthalten temporäre Chat-Quellenmarker | Zitate nicht langlebig | Quellenparser und Bibliografie | Stable URL/DOI/Locator oder `unresolved` |
| G-V5-23 | P2 | Kompositionsformen/Produktideen nicht nutzergeprüft | Feature Overreach | UX-Versuche mit Lernenden/Musikern | Dokumentierte Nutzertests und Entscheidungen |
| G-V5-24 | P2 | Kein Crossstyle-Expert-Consensus | Unangemessene Universalregeln | Genrebezogene Peer Reviews | Mehrperspektivische Reviews dokumentiert |
| G-V5-25 | P3 | ML-Modelle fehlen | Zukunftsoption; aktuell kein Defizit | Erst nach deterministischem Test- und Datenbestand | Forschungsprotokoll und Baseline |
| G-V5-26 | Later | Drum-Engine/Dataset | Nicht im aktuellen Scope | Nur Roadmap dokumentieren | Nutzer beauftragt spätere Phase explizit |

## Risikosteuerung und Review-Gates

**R1 Recht:** urheberrechtlich geschütztes Buchmaterial kann Forschungsreferenz sein, aber darf nicht ohne Rechtsgrundlage öffentlich mitgeliefert werden. **R2 Fachlichkeit:** ein korrekter YAML-/MIDI-Parser prüft keine harmonische Stimmigkeit. **R3 Repräsentation:** gleiche Tonklassen können unterschiedliche Schreibweisen, Funktionen und modale Zentren haben. **R4 Auslegung:** eine Theorieanalyse aus einer Stiltradition ist nicht zwingend in einer anderen angemessen. **R5 Datenqualität:** 1.378 automatisierte Varianten sind keine 1.378 empirischen Fälle. **R6 Pflege:** Code-/Skill-/KB-Versionen dürfen nicht stillschweigend gekoppelt werden.

**Freigabekette:** `raw → access_checked → metadata_checked → source_section_checked → claim_mapped → mechanically_tested(if formal) → theory_reviewed(if interpretive) → publish_approved`. Jeder Übergang benötigt Datum/Beleg/Verantwortung. Ein unzugängliches Buch kann höchstens `metadata_checked` erhalten.

## Entscheidungsmatrix für den nächsten Codex-Lauf

| ID | Frage | Derzeitiger Status | Wer darf entscheiden? | Verbindlicher Default |
|---|---|---|---|---|
| D-V5-01 | Welches Steps-Repo/Branch? | UNKNOWN | Code-/Git-Nachweis | Erst read-only prüfen |
| D-V5-02 | KB-Pfad im Projekt | PROPOSED | Maintainer auf Basis Repo | bestehende Struktur bevorzugen |
| D-V5-03 | Quelle-IDs und Schemas | PROPOSED | im PR durch Fach-/Entwicklungsreview | parallel versionieren |
| D-V5-04 | music21 als Benchmark? | PROPOSED | technisch/rechtlich prüfen | keine Installation erzwingen |
| D-V5-05 | Deterministische Regeln zuerst? | PROPOSED | Architekturentscheidung (ADR) | prüfbare Regeln priorisieren |
| D-V5-06 | Umgang mit Traditionsmusik? | RESEARCH_REQUIRED | Vertreter fachlicher Praxis | separate Domain und Review |
| D-V5-07 | Was heißt `reviewed`? | PROPOSED | Review-Governance | Source+Claim+Tests, Mensch wenn Musikurteil |
| D-V5-08 | Neue Etüden in Produktion? | REVIEW_REQUIRED | Musikfach-Reviewer | nur Laborbestand |
| D-V5-09 | Open-Source-/Datenlizenzen | UNKNOWN | Projektverantwortlicher | kein öffentlicher Rohdatenimport |
| D-V5-10 | UX-Erklärungsmodell | PROPOSED | Produkt-/UX-Tests | Alternativanalysen nicht verbergen |
| D-V5-11 | Drum-Modul | DEFERRED | ausdrücklich Nutzer | nur Roadmap |
| D-V5-12 | Git Merge | NICHT AUTORISIERT | ausdrücklich Nutzer | kein Merge |

**Referenzen:** Fachbände, `06_Quellen_und_Rechte/`, `08_Validierung/` und der archivierte V4-Stand.

# STEPS – CODEX MASTER EXECUTION V4.0
## Wissenschaftliche Knowledge Base für Music Theory, Harmony, Chord Progressions und Composing

**Status:** ausführbarer, umfangreicher Entwicklungsauftrag. **Nicht** als Nachweis schon implementierter Repository-Arbeit zu behandeln. **Primäres Ergebnis:** tatsächlich erschlossene, zitierbare und überprüfbare Wissensdatenbank im *realen* STEPS-Projekt, nicht ein weiterer bloßer Plan. **Versions- und Freigaberegel:** V4 ist Forschungs-Draft; keine Annahme einer veröffentlichten stabilen KB.

### 0. Rolle, Projekt und Ausgangslage

Arbeite als interdisziplinäres Team aus Music Theorist, Jazz/Popular-Music Analyst, Composition Teacher, Computational Musicologist, Software/Knowledge Architect, Research Librarian, Software QA und Licensing Reviewer. Das Projekt **Steps – An independent, open-source chord progression app for exploring harmony & learning music theory** benötigt eine langfristig erweiterbare, eigenständige Wissensinfrastruktur, die vier **gleichberechtigte** Domänen abdeckt:

1. Music Theory: akustische, notierte, mathematische und historische Grundlagen;
2. Harmony: verschiedene tonale, modale, chromatische, transformationale, jazz-, blues- und populäre Theoriesysteme;
3. Chord Progressions: zeitliche harmonische Muster, Analyse, Transformation, Stimmführung, Reharmonisierung, Korpora;
4. Composing: Motiv und Thema, Melodie, Bass, Form, Kontrapunkt, Harmonisierung, Arrangement, Instrumentation, dramaturgische Entwicklung und Revision.

**Nicht verwechseln:** Die vier Domänen sind keine vier Namen für denselben Chord Generator. Komposition ist eine eigenständige strukturelle, zeitliche und handwerkliche Ebene. Allgemeine Rhythmus-, Metrik- und Formanalyse gehört dazu; produktive Drum-/Groove-Engine und große Drum-Datensätze sind ausdrücklich *deferred*.

### 1. Materialien und Prüfreihenfolge

1. Dieses V4-Paket: `00_START_HERE.md`, vier Fachbände unter `01_Studienbaende/`, die umfangreiche Werkstattanalysedatei, Taxonomie, neue und ältere Register, 30 Etüden mit JSON/Markdown/MIDI, neu recherchierte Quellen und Freigaberegeln.
2. Historisches `00_HISTORISCH_V3/`: V3-Monografie, V3-Daten, V3-Codex und die sieben damaligen V1-Unterlagen einschließlich tatsächlichem `Master-Research-Prompt.md` und dem fertigen V1-Handover. V3 ist **nicht** automatisch peer-reviewed.
3. Tatsächlich vor Ort vorhandene Schritte/Skills, Originalbücher, PDFs, PDFs mit unterschiedlichem Zugriff, TXT/HTML, Testfälle, Dokumentation, ältere Forschungsexporte und Original-Research-Paper, **soweit tatsächlich zugänglich**.
4. Das reale STEPS-Repository. Verwende **nur dessen tatsächlichen Pfad/Branch**, nicht spekulativ einen Pfad aus einem Forschungsbericht. Bewahre Eigentümeränderungen. Die Tatsache, dass ein Dokument eine Architektur empfiehlt, belegt keine bereits existierende Umsetzung.

**Quellenhierarchie:** explizite Nutzerentscheidung > real nachgewiesener Projektzustand für Bestandsfragen > selbst überprüfter Primär-/Fachquelleninhalt für wissenschaftliche Claims > durch Quellen beurteilte Research-Synthese > eigene Hypothese. Herkunft und Status bleiben getrennt.

### 2. Verbindliche Arbeitsprinzipien

- **Do actual work**: nach Audit reale Source Cards, Concepts, Claims, Rules, Reharmonization Examples, Composing Patterns, Test Cases und Indizes anlegen. Ein leerer Baum ist kein Abschluss.
- **Source-first**: eine `source_candidates`-Liste ist kein Einzelbeleg; der Übergang zu `verified` erfordert reale Textstelle, Ausgabe/Abschnitt, Kontext und Reviewer.
- **No invented facts**: niemals Seitenzahlen, ISBN/DOI, Zugriff, musiktheoretischen Konsens, Korpusfrequenzen, Git-Tests oder Toolausgaben erfinden.
- **Context before function**: derselbe Akkord kann mehrere Rollen besitzen; Unterschiede zwischen Stufe, Funktion, Voice Leading, Set Relationship und Corpus Usage bewahren.
- **Scope-specific rules**: nicht Klassiknormen als universelles Kompositionsverbot auf Jazz, Gospel, Pop, Blues oder modale Traditionen übertragen.
- **Respect copyright**: rechtsgeschützte Bücher, Scores, Aufnahmen, Transkripte und fremde Produkt-Designs nicht ohne Lizenz öffentlich committen.
- **Reproducibility**: jeder deterministische Test hat Input, Expected, Tool, Version und Ergebnis; jeder kreative Review hat nachvollziehbare qualitative Kriterien.
- **No merge without approval**: nutze vorhandene Projektregeln und stelle diffbare Änderungen/PR bereit; nicht automatisch nach main mergen.

### 3. Arbeitspakete – ausführungssicher und priorisiert

#### AP-00 / Repository Read-only Baseline (P0)

Prüfe `git status`, Branch/HEAD, README, Python-, Tkinter- und Dokumentationsstruktur, existierende `AGENTS.md`/`SKILL.md`, Konfiguration, Versionen, Tests, Lizenzen, offene Änderungen und vorherige KB-Prototypen. Erzeuge `EXISTING_STATE_AUDIT.md` mit beobachteten Fakten und Belegpfaden. Vermeide die Übernahme einer vorgeschlagenen V4-Verzeichnisstruktur, wenn bereits eine gleichwertige Projektstruktur existiert. Stoppe bei nicht zugänglichem Repository den produktiven Repo-Teil, aber dokumentiere eine importierbare KB-Arbeitskopie.

#### AP-01 / Dokument- und Versionsmanifest (P0)

Erhalte V1 und V3 als historische Versionen; identifiziere in V3 die sieben ursprünglichen Dokumente und die korrigierte Tatsache, dass der Master-Prompt heute vorhanden ist. Prüfe die tatsächliche Verfügbarkeit eines *separaten finalen* ursprünglichen Deep-Research-Papers – nicht aus einer neuen V3/V4-Synthese rückwärts erfinden. Erzeuge ein Current Manifest für V4; pflege Original-Dateinamen, Hashes, Änderungsdatum, Versionsbeziehung, superseded_by und Zitierpfade.

#### AP-02 / Vollständige Source Registry (P0)

Nutze historische Initial Sources v1.0 (20 PDF/TXT-Kandidaten) und die neuen 30 extern geprüften Fundstellen **nur als Ausgangsinventar**. Ermittle wirklich verfügbare Original-Dateien, Lesbarkeit, DOI/ISBN, Metadaten, Copyright, Attribution und Dubletten. Beachte defekte oder schlecht extrahierte Dateien, insbesondere das historisch gemeldete `MakingMusic.pdf`; prüfe den tatsächlichen Status erneut, bevor 'defekt' als aktuelle Tatsache gilt. Führe separate States `named`, `metadata_checked`, `local_access`, `read_section`, `claim_located`, `reviewed`, `approved_for_public_reuse`.

#### AP-03 / Bibliografieausbau mit fachlichem Mapping (P0)

Beschaffe legal zugängliche, zitierfähige Primärquellen und wissenschaftliche Sekundärliteratur zu allen vier Domänen. Beginne mit Open Music Theory (richtige Edition), Rubin, Caplin, Gjerdingen, Belkin, Nobile, Lerdahl/Jackendoff, Huron, Meyer, London, Cohn, Rings, Lewin, de Clercq/Temperley, Rohrmeier, Harte, DCML, ChoCo und When in Rome. Ergänze insbesondere Quellen zu Kompositionsmethodik, Melodik, Kontrapunkt, Instrumentation, posttonaler Komposition, Film/Game-Music, Pop-/Jazz-/Bluesform sowie musiktheoretischer Diversität. Jeder neue Titel bekommt tatsächlichen Zugriffsstatus und Style-/Epoche-/Fachscope, nicht bloße hohe Priority.

#### AP-04 / Ontologie und Begriffskonkordanz (P0)

Überprüfe die 163 V4-Unterthemen sowie 142 historischen V3-Concept-Cards und 49 V4-Forschungsmodule. Trenne `Topic`, `Concept`, `Claim`, `Rule`, `Technique`, `Progression`, `Score/Study`, `Analysis`, `Source`, `Decision`, `Test`, `Feature`. Erkenne Synonyme, aber verschmelze stiltheoretische Gegenpositionen nicht. Für *jedes* validierte Concept benötigst du Definition, Voraussetzungen, Beispiele, Grenzen, analytische Linsen, Terminologie Deutsch/Englisch, belegte Quellenstellen und Reviewstatus. Mach den erlaubten `unknown`-Status selbstverständlich.

#### AP-05 / Notation, Pitch und Spelling (P0)

Erstelle getestete Repräsentationen für Tonhöhe versus Pitch Class, enharmonisches Spelling, deutsche H/B-Namen, Intervalldiatonik/Chromatik, Tonarten, Dur/Moll, Modi, Akkordqualitäten, Extensions, Alterationen, Slash-Bass, Inversion und Stimmungssystem. Für Standard-MIDI darf 12-TET als Ausgangsfassung dienen, aber Tuning-ID ist explizit. Golden Cases: F#-Dur mit E#, C–F# als A4 gegen C–Gb als d5, C7 vs Cmaj7 vs Cadd9, I7 im Blues gegen V7/IV in tonalem Kontext.

#### AP-06 / Tonale, modale und chromatische Harmonik (P1)

Fülle Fachmodule für Diatonik, Funktionen, Kadenzen, Sekundärdominanten und -leittonakkorde, Modulation, mixture, Neapolitaner, übermäßige Sextakkorde, chromatische Medianten, PLR, Tonnetz und transformatorische Relationen. Markiere Formfunktionen und Regeltypen. Bei einer `G7–C`-Verbindung muss Satz-/Phrasenkontext vorliegen, bevor ein konkreter Kadenztyp als geprüft gilt. Bei `C–Ab` muss eine Common-Tone-Deutung neben einer möglichen chromatischen Analyse stehen können. Kein falscher Universalismus.

#### AP-07 / Jazz, Pop/Rock, Blues, Gospel, Neo-Soul und stilistische Reichweite (P1)

Belege ii–V–I und Guide-Tone-Bewegung, alterierte Dominanten, Tritone/Backdoor-Substitution, Blues-I7, modale Loops, Pop-Axis und Hybrid-Tonicity. Prüfe die besondere Relevanz von Songform, Riff, Groove und Hypermetrum; behaupte keine einheitliche Harmoniegrammatik für unterschiedliche kulturelle Repertoires. Inhalte zu Gospel/R&B/Neo-Soul brauchen spezifische Originalquellen; eine interessante Akkordfolge allein belegt keine kulturelle Stilzugehörigkeit.

#### AP-08 / Progression Library (P1)

Nutze das V4-Gesamtregister mit 226 strukturierten Progressionsfällen als Rohmaterial (95 historische + 131 neue). **Prüfe die Stufenlabels einzeln.** Manche Fälle sind Varianten, Transpositionen oder absichtlich deskriptive/nicht-funktionale Analysen, nicht unabhängige wissenschaftliche Befunde. Ergänze Timing, Tonart, lokale Tonika, Stil, reale musikalische Beispiele, Melodie-/Bassbindung und Gegenfälle. Übertrage keine unbestätigten Häufigkeiten. Entwickle eigene Canonical Cases für Chord Parsing und Reharmonization, die durch exakte Transformations-Constraints bewertet werden.

#### AP-09 / Composing-Kern: Motiv, Melodie, Form, Dramaturgie (P1)

**Eigenständiger Schwerpunkt mit mindestens gleichwertigem Dokumentationsanteil zu Harmony.** Baue Module für Motiverfindung, Kontur, Rhythmuszelle, Sequenz, Variation, Augmentation/Diminution, Inversion/Retrograde, Fragmentierung, Fortspinnung, Thema, Satz, Periode, Songform, formalen Kontrast, Textprosodie, Hook, Motivwiederkehr, Bass-first/Melody-first/Counterpoint-first. Verknüpfe jede Technik mit konkretem Input, Operation, Output, musikalischer Absicht, Gegenfall und Reviewaufgabe. Nutze das V4-Technikregister mit 134 Einträgen (69 historisch + 65 neu) als Seed, nicht als automatisches Endergebnis.

#### AP-10 / Composing-Kern: Kontrapunkt, Arrangement, Instrumentation (P1)

Trenne strengen Kontrapunkt mit Stilkontrakt von freier Mehrstimmigkeit. Ergänze weitere eigenständige Subsysteme für Register, Instrumentenidiomatik, spielbare Voicings, Texturdichte, Basslinien, Tasten-/Gitarren-/Streicher-/Bläserarrangements, orchestrale Dramaturgie und Instrumententransposition. Baue Counterpoint-Fälle mit zwei tatsächlichen notierten Stimmen, nicht bloß Akkordsymbolen. Fachliche Orchestration-Aussagen erfordern nachprüfbare Quellen und gegebenenfalls Spielpraktiker-Review.

#### AP-11 / Original-Kompositionslabor (P1)

Prüfe die 30 neuen, jeweils vollständig getakteten 16-Bar-MIDI-Etüden mit Melodie/Bass/Harmoniespur; sie haben **mechanisch prüfbare** Dauer, Tonhöhen und Chord-Subsets. Bewerte musikalisch und überarbeite konkret: Ist die Melodie sinnvoll? Ist die B-Phrase kontrastierend? Sind stärkere und schwächere Schlüsse zu erkennen? Sind die Voicings idiomatisch? Sind Stilbezeichnungen gerechtfertigt? Wo wurden bloß Akkordtöne aneinandergereiht? Wenn nötig komponiere die Stimme neu und dokumentiere den Unterschied. Keine pauschale 'fertige Stücke'-Freigabe nur wegen eines gültigen MIDI-Headers. Ergänze Notationsausgabe erst, wenn das Notenmodell sie korrekt unterstützen kann.

#### AP-12 / Interkulturelle und kognitive Fachperspektiven (P1/P2)

Trenne globale westliche Unterstellungen von traditionsspezifischer Musiktheorie. Eine Rāga oder ein Maqam ist nicht lediglich ein umbenannter westlicher Modus. Verwende `unknown/unsupported` statt fingierter Akkordfunktionen, solange geeignete Fachquellen und Reviewer fehlen. Ergänze Modelle zur Musikpsychologie und Erwartung nur mit kontrollierten Geltungsbedingungen; keine absoluten Emotions-Scores.

#### AP-13 / Daten- und Formatinteroperabilität (P1)

Implementiere klar abgegrenzte JSON-/YAML-Schemas und Parser/Serializer für Ton, Intervall, ChordSymbol, ChordEvent, MelodyEvent, BassEvent, FormSection, ComposingTechnique, MIDI-Study, AnalysisLens und EvidenceClaim. Vergleiche `music21`, Harte-Notation, DCML, RomanText, JAMS, MusicXML und MEI, bevor ein interchange format als kanonisch behauptet wird. Führe Loss Reports für MIDI→Notation durch, da Enharmonik aus reinem MIDI nicht rekonstruiert werden kann. Keine große App-Neuentwicklung im Wissensprojekt.

#### AP-14 / Korpora und empirische Validierung (P2)

Prüfe ChoCo, When in Rome, DCML und andere Quellen auf Edition, Lizenz je Partition, Annotationseinheit, Dubletten, Genre/Epoche, Tonartenheuristik, Metadaten und Reproduzierbarkeit. Importiere nur zulässige Subsets. Korpus-Frequenzen nur aus tatsächlicher Abfrage mit Zähler, Nenner, Filter und Versionsangabe. Unterscheide Stilwahrscheinlichkeit von musiktheoretischer Möglichkeit.

#### AP-15 / Wissensbeziehung und Traceability (P1)

Setze Beziehungen um: `Source → supports/contradicts Claim → models Rule/Concept → exemplifies Progression/Study → evaluated_by Test → used_by Feature/Skill`. Beziehungen können `proposed` oder `verified` sein. Die ursprünglichen Register und IDs dürfen beim Umzug nicht verlorengehen; erstelle Migrations-/Alias-Tabelle. Führe die `CLAIM_PROVENANCE_AND_LEGAL_GATE.md` als verpflichtendes Review-Gate ein.

#### AP-16 / Automatisierte QA (P0/P1)

Führe das mitgelieferte `08_Validierung/validate_v4.py` aus; bereinige reale Fehler statt Statusmeldungen zu überschreiben. Prüfe danach im echten Projekt: JSONSchema, ID-Uniqueness, referenzierte Quellen, interne Links, verwaiste Objekte, Akkordbestandteile, Enharmonik, Modi, Zeitvalidität, MIDI-Parsing, Stimmen-On/Off-Matching, statische Dokumentationsqualität, Projekt-Tests und eventuell Linux-CI. Ungetestete Komponenten **ungetestet** nennen. Kein Report darf 'musikalisch validiert' sagen, wenn nur Parsing geprüft wurde.

#### AP-17 / Hör- und Fachreview (P1)

Entwickle einen reproduzierbaren Reviewer-Prozess. Pro Etüde/Regel: kurzer musikalischer Kontext, Notenauszug, Tonmaterial, Stilkontrakt, alternative Deutungen, Gutachter, Datum, Review-Urteil und konkrete Korrekturen. Für schwierige Bereiche (Jazz, Blues/Gospel, historische Gegenpunktnormen, nichtwestliche Systeme, Instrumentenidiomatik) geeignete Fachkompetenz einplanen. Ohne Reviewer `pending_human_review` erhalten.

#### AP-18 / Dokumentationspflege und Codex-Skill-Anbindung (P1)

Erzeuge einen kurzen Navigationseinstieg für `SKILL.md`: Aufgabe klassifizieren → relevantes Wissensmodul laden → Input normalisieren → analytische Linsen wählen → Prüfung und Quellenlimits anwenden → Ausgabe formulieren → Tests/Citations prüfen. Theorie selbst bleibt in einer versionierten Referenzbibliothek, nicht im Skill-Prompt. Aktualisiere bestehende `SKILL.md` nur nach Sichtung und ohne Verweise auf fehlende Dateien.

#### AP-19 / PR, Versionierung und Übergabe (P0)

Wenn Repository verfügbar: arbeite konfliktbewusst auf separatem Branch, liefere nachvollziehbare Commits/PR, Changelog, Coverage-Matrix, Source-/License-Report und Tests. Erhalte bestehende Änderungen. Ohne ausdrücklichen Auftrag nicht mergen. Wenn der Arbeitsumfang zu groß für eine einzelne Umsetzung ist, schließe ein echtes inhaltliches Arbeitspaket nach Abnahme ab und dokumentiere die restlichen Pakete statt einen Plan als erledigt zu präsentieren.

### 4. Zielobjekte und Minimalverträge

**Theory Concept:** `id`, `canonical_term_de/en`, `definition`, `prerequisites`, `analytical_lenses`, `style_scope`, `original_example`, `counterexample`, `evidence[]`, `review_status`, `version`.

**Chord Progression:** `id`, `chord_events` mit Offset/Dauer, `global_tonal_context`, `analysis_candidates[]`, `bass_line`, `melody_notes`, `style_scope`, `reference_cases`, `uncertainty`, `version`.

**Composition:** `id`, `brief`, `motifs[]`, `form_sections[]`, `melody_events[]`, `bass_events[]`, `chord_events[]`, `instrumentation`, `tempo/meter`, `transformations[]`, `revisions[]`, `playback_export`, `source_provenance`.

**Rule:** `id`, `type=constraint|tendency|convention|transformation|interpretation|heuristic|empirical_observation`, `antecedent`, `scope`, `consequent`, `exceptions`, `counterexamples`, `sources`, `tests`.

**Claim Evidence:** `source_id`, `source_edition`, `access_status`, `exact_locator`, `claim_text`, `claim_type`, `verification_date`, `reviewer`, `license_gate`, `conflict_ids`.

### 5. Nicht zu verwechselnde Qualitätskennzahlen

Die V4 enthält 77 Quellen-/Editions-/Metadateneinträge, nicht 77 vollständig bearbeitete Primärwerke. Die V4 enthält 226 Progressionsdatensätze, aber auch Varianten/Transpositionen. Die 134 Composing Techniques sind Arbeitsverfahren, keine bewiesenen Gesetze. Die 30 MIDI-Etüden sind abspielbare Übungsmaterialien, keine nach künstlerischem Maßstab abgeschlossenen Werke. Die 180 Testfall-Records bestehen teilweise aus automatisierbaren Vorgaben und teilweise aus noch nicht ausgeführten Referenz-/Review-Cases. **Erfasse deshalb zusätzlich belastbare Coverage-Metriken:** tatsächlich geprüfte Originalpassagen, claims_with_exact_locator, music_reviewer_approved, unit_tests_passed, style_modules_with_authoritative_evidence, studies_with_compositional_review.

### 6. Explizite Stop- und Review-Grenzen

- Nicht existent oder nicht lesbar → `unavailable`, nicht 'fertig geprüft'.
- Nur Abstract → `metadata/abstract reviewed`, nicht `full_text_reviewed`.
- Kommerzielle Partitur → kein Public Commit ohne Rechte.
- Behauptete Stiltypik ohne musikalische Daten → `illustrative`, nicht `empirically_common`.
- Falsche oder unklare Roman Numeral → im Draft korrigieren und Änderungsgrund angeben.
- Unterschiedliche Tonikakandidaten → dokumentieren, nicht eine Zwangsentscheidung fällen.
- Fehlende Codex-Rechte/fehlender Repo-Zugriff → blockierte Umsetzung präzise ausweisen, keine erfundenen Commits.

### 7. Definition of Done (inhaltlich, nicht nur formal)

- Echte Repo-Baseline; Dokumente und V1/V3/V4-Versionen abgeglichen.
- Quellenregistry nach Zugriff, Metadaten, Lizenz, lokaler Lesbarkeit und konkret bearbeiteten Passagen gepflegt.
- Substantielle vierdomänige Wissensobjekte, nicht nur Platzhalter.
- Korrekt klassifizierte Theory Rules und mehrere analytische Perspektiven.
- Progressions mit fachlich vertretbaren Kontexten, realen Durations und prüfbarem Chord Parsing.
- Kompositionsobjekte mit echten Note Events, Form/Motiv/Voice Leading und durchgeführtem musikalischem Review an mindestens einem explizit dokumentierten Teilbestand.
- Source/Claim/Rule/Test-Traceability und dokumentierte Evidenzlücken.
- Wiederverwendungs-/Lizenzprüfung vor öffentlicher Publikation.
- Tatsächlich ausgeführte automatisierte Prüfungen und ein getrennter menschlicher Review-Status.
- Changelog, Gap Register, Coverage Matrix, präzise nächste Arbeitspakete, PR/diff, **kein ungefragter Merge**.

### 8. Reporting Format am Ende jedes Arbeitspakets

**A. Tatsächlicher Bestand:** Branch, neue/geänderte Dateien, erhaltene Originale, Diff-Umfang.  
**B. Quellenarbeit:** neu beschafft, nur Metadaten, tatsächlich gelesene Abschnitte, bestätigte Claims, Lizenzdefizite.  
**C. Fachinhalt:** nach Domäne und Thema differenziert; Anzahl neuer geprüfter Konzepte/Rules/Studies und konkrete Beispiele.  
**D. Kompositionsqualität:** mechanische Validität getrennt von hör-/fachlich bewertetem Material.  
**E. Tests:** konkrete Befehle und Ausgaben; fehlgeschlagene Tests und Nicht-Ausführbarkeit.  
**F. Konflikte:** fehlende/mehrdeutige Quellen, offene architektonische Entscheidungen, schwerwiegende Restlücken.  
**G. Abnahme:** Erfüllung der Definition of Done, aktueller Branch/PR, kein automatischer Merge.  
**H. Nächste Pakete:** priorisierter Restbacklog mit Abhängigkeiten.

### 9. Startanweisung

**Beginne jetzt** mit AP-00, AP-01 und AP-02 am tatsächlich zugänglichen STEPS-Projekt. Anschließend priorisiere echte fachliche Erschließung in allen vier Hauptdomänen statt bloßer Strukturarbeit. Nutze die V4-MIDI-Etüden, den Progressionsatlas und die 49 Fachmodule als nachprüfbare Rohsubstanz, nicht als autoritative unfehlbare Canon. Behauptete Quellenbelege werden nur nach Überprüfung in `verified` überführt. Führe Tests aus; sichere deine Ergebnisse diffbar; gebe eine präzise Abdeckung mit offener Restarbeit aus.

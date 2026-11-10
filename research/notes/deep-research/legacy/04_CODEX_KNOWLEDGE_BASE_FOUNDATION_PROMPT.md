# STEPS – CODEX KNOWLEDGE BASE FOUNDATION & EXPANSION
## Master Execution Prompt V1.0

> **Anwendung:** Diesen Prompt in Codex/Work mit Zugriff auf das echte Steps-Repository, die Originalquellen, das fertige Research Paper und das aus dem Research-Chat erzeugte `PROJECT_CONTEXT_HANDOVER.md` ausführen. Nicht bereits mit diesem Prompt als erledigt zu betrachten sind der Knowledge-Base-Aufbau und die Quellenerschließung.

### 1. Rolle und Gesamtauftrag

Übernimm die Rolle eines interdisziplinären Teams aus Senior Software Architect, Music Theory Researcher, Computational Music Theory Specialist, Knowledge Engineer, Research Librarian, Scientific Documentation Engineer, Data & Schema Architect, Quality Assurance Engineer und Open-Source Maintainer.

Bearbeite das vorhandene Projekt **Steps**.

**Steps – An independent, open-source chord progression app for exploring harmony & learning music theory.**

Dein Auftrag besteht darin, bisherige Forschungsergebnisse, bestehende Dokumentation und verfügbare Fachquellen in eine **umfangreiche, strukturierte, belegbare, versionierbare und langfristig erweiterbare Music Theory Knowledge Base** zu überführen.

Die Wissensbasis soll die Steps-Anwendung und einen zukünftigen spezialisierten Codex-/AI-Skill unterstützen.

**Dies ist ein konkreter Umsetzungsauftrag, kein Auftrag zu einem weiteren reinen Konzeptpapier.** Erzeuge tatsächliche Repository-Inhalte, ausgefüllte Wissensobjekte, Quellenverzeichnisse, fachliche Referenzen, Verknüpfungen, Validierungsdaten und Dokumentation.

**Discover → Inventory → Preserve → Verify → Extract → Normalize → Connect → Validate → Document → Version → Expand**

### 2. Maßgebliche Eingaben

Untersuche alle tatsächlich verfügbaren Materialien:

1. `PROJECT_CONTEXT_HANDOVER.md` (erst nach Abschluss des Research-Chats erzeugt)
2. Das abschließende Deep-Research-Paper zu Steps
3. `Master-Research-Prompt.md`
4. `01_STEPS_Research_Foundation.md`
5. `02_STEPS_Knowledge_Base_Product_Blueprint.md`
6. Verbundenes Steps-Repository bzw. Projektordner
7. Bestehende Projekt- und Architekturdokumentation
8. Vorhandene `AGENTS.md` und `SKILL.md`
9. Lokal gespeicherte Bücher, wissenschaftliche PDFs, TXT- und HTML-Dateien
10. Bereits existierende Forschungen, Literaturverzeichnisse, Daten, Beispiele und Tests

Die Dateinamen sind erwartete Eingaben, keine Garantie ihrer Verfügbarkeit. Prüfe Zugriff und Pfade. Erfinde keine Dateipfade und behaupte keinen Zugriff, den du nicht hast.

Nutze bei vorhandener Verbindung das tatsächliche Steps-Repository; verwechsle es nicht mit einem anderen Projekt.

### 3. Informationshierarchie

- Ausdrückliche Nutzeranforderungen und bestätigte Entscheidungen bestimmen die Ziele.
- Der überprüfte Repository-Zustand bestimmt den Bestand.
- Überprüfte Primärquellen und Fachliteratur begründen wissenschaftliche Aussagen.
- Das Research Paper liefert Forschung, Quellenkandidaten und Architekturvorschläge.
- Das Project Context Handover sichert Geschichte, Anforderungen und Entscheidungen.
- Frühere Entwürfe liefern weiteren Kontext und Alternativen.

Keine Quelle darf andere stillschweigend überschreiben. Widersprüche sind in Conflict Records zu dokumentieren.

### 4. Verbindliche Projektgrenzen

**Aktueller Schwerpunkt:** Musiktheorie, Harmonielehre, Akkordtheorie, Chord Progressions, Reharmonisierung, Voice Leading, modale/chromatische sowie Jazz-/Blues-/Popularmusik-Harmonik, Computational Music Theory, wissenschaftliche Wissensorganisation und Qualitätssicherung.

**Nicht Teil dieses Auftrags:** vollständige App-Neuentwicklung, größere GUI-Änderungen, vollständige Progression Engine, produktives ML-Modell, endgültiger Skill, Drum-Progressions/Drum-Datensätze, unkontrollierter Download riesiger Korpora, Verwendung ungeprüfter oder rechtlich problematischer Inhalte.

Rhythmus, Metrum und Harmonic Rhythm sind als Harmoniekontext zulässig; Drum-/Groove-Funktionen gehören nur in die langfristige Roadmap.

### 5. Phase 0 – Repository Discovery & Baseline Audit

Prüfe vor Änderungen:

- Git-Status, aktiven Branch und vorhandene Änderungen
- Verzeichnisstruktur und Python-/Tkinter-Projekt
- Dokumentation, Skills, AGENTS-Anweisungen
- Forschungsunterlagen und Quellen
- Implementierte Theorieobjekte und Datenmodelle
- Test- und Validierungsinfrastruktur
- Dokumentationsduplikate und bestehende Knowledge-Base-Strukturen

Erstelle einen dokumentierten Ausgangsstand.

**Regeln:** Nichts unkontrolliert ersetzen oder löschen; Projektkonventionen respektieren; keine Duplikate erzeugen; fremde Änderungen nicht zurücksetzen; nicht nach `main` mergen ohne Auftrag. Falls geeignet, in eigenem Branch arbeiten.

### 6. Phase 1 – Research Material & Source Inventory

Inventarisiere alle auffindbaren Forschungsunterlagen. Berücksichtige `Initial Sources v1.0` als ursprüngliche Kandidatenliste und prüfe jede Originaldatei auf tatsächliche Existenz und Lesbarkeit.

Erfasse auch die im Research Paper empfohlenen Quellen und Korpora, soweit belegt: Open Music Theory; *A Generative Theory of Tonal Music*; *Tonal Pitch Space*; *A Geometry of Music*; *Audacious Euphony*; generative Syntax tonaler Harmonik; Rock- und Popularmusik-Harmonik; Harte chord-symbol notation; DCML; ChoCo; When in Rome und weitere überprüfte Literatur.

Die bloße Nennung bedeutet nicht, dass eine Quelle verfügbar, gelesen, validiert oder frei wiederverwendbar ist.

Jede Quelle erhält eine stabile ID, zum Beispiel `SRC-0001`.

```yaml
id: SRC-0001
title: ""
authors: []
year: null
edition: null
source_type: ""
publisher: ""
doi: null
isbn: null
canonical_url: null
local_path: null
topics: []
theoretical_traditions: []
access_status: unknown
reading_status: not_reviewed
verification_status: unverified
license: unknown
redistribution: unknown
citation_locations: []
related_concepts: []
notes: ""
```

Unterscheide: identifiziert, Metadaten geprüft, verfügbar, lesbar, inhaltlich ausgewertet, extrahiert, fachlich validiert. Erfinde keine DOI-, ISBN- oder Seitenangaben. Prüfe zuvor gemeldete Lesefehler, darunter `MakingMusic.pdf`, falls zugänglich.

### 7. Phase 2 – Knowledge Base Architecture

Nutze zuerst vorhandene Projektstrukturen. Falls noch keine passende Struktur existiert, ist folgende modulare Organisation eine Orientierung:

```text
knowledge-base/
├── README.md
├── VERSION.md
├── CHANGELOG.md
├── manifests/
│   ├── sources.yaml
│   ├── licenses.yaml
│   ├── coverage.yaml
│   └── knowledge-index.yaml
├── sources/
│   ├── registry/
│   ├── bibliography/
│   └── links/
├── theory/
│   ├── foundations/
│   ├── notation/
│   ├── scales-and-modes/
│   ├── chords/
│   ├── functional-harmony/
│   ├── modal-harmony/
│   ├── chromatic-harmony/
│   ├── jazz-harmony/
│   ├── popular-harmony/
│   ├── blues-harmony/
│   ├── voice-leading/
│   ├── reharmonization/
│   └── computational-theory/
├── rules/
├── progressions/
├── examples/
├── analytical-lenses/
├── relationships/
├── research/
│   ├── findings/
│   ├── gaps/
│   └── conflicts/
├── product-inspiration/
├── decisions/
├── schemas/
├── validation/
│   ├── theory-cases/
│   ├── counterexamples/
│   └── reports/
└── skill-references/
```

Sicherstellen: Theorie unabhängig von GUI; Quellen getrennt von Derivaten; Regeln getrennt von Interpretationen; Beispiele mit Begründung; Forschung getrennt von Produktideen; Skill-Referenzen ableitbar; stabile IDs, Git-Wartbarkeit, erweiterbare Taxonomie, nutzbare Suche/Indizes.

### 8. Phase 3 – Music Theory Knowledge Extraction

**Erstelle keine leere Wissensdatenbank. Fülle sie mit tatsächlich aus zugänglichen Quellen abgeleiteten, belegbaren Inhalten.**

Extrahiere Begriffe, Definitionen, Modelle, Regeln, Konventionen, Tendenzen, formale Zusammenhänge, Berechnungsverfahren, Anwendungen, Beispiele, Gegenbeispiele, Alternativinterpretationen, stilistische Besonderheiten, Streitfragen und Querverbindungen.

Verwende möglichst atomare, referenzierbare Objekte.

Mindestens folgende Bereiche sind systematisch zu erschließen oder als Lücke zu dokumentieren:

- **A Grundlagen:** Notation, Tonhöhen, Intervalle, Enharmonik, Stimmungssysteme, Tonarten, Skalen, Modi, Tonstufen, Quintenzirkel
- **B Akkordtheorie:** Dreiklänge, Septakkorde, Extensions, Alterations, Inversions, Slash Chords, Voicings, Chord Symbols
- **C Funktionale Harmonik:** Stufenharmonik, Funktionen, Kadenzen, Zwischendominanten, Tonicization, Modulation
- **D Modale Harmonik:** Modi, Zentren, Progressionsmodelle, Modal Interchange
- **E Chromatische Harmonik:** Borrowed Chords, Chromatic Mediants, Tritone Substitution, Neapolitan, Augmented Sixth
- **F Jazzharmonik:** ii–V–I, Altered Dominants, Chord-Scale Theory, Extended Harmony, Substitutions, Turnarounds
- **G Pop/Rock:** Loops, nichtfunktionale Beziehungen, Power Chords, modale Progressions
- **H Blues:** Bluesformen, tonikale Dominant-Seventh-Chords, Blues-Skalen, stiltypische Harmonik
- **I Progressions:** Progression Families, Harmonic Rhythm, Cadences, Sequences, Tension & Release, Bass Motion, Mehrdeutigkeit
- **J Reharmonization:** Substitutions, Secondary Dominants, Modal Mixture, Passing Chords, Melody Harmonization
- **K Voice Leading:** Common Tones, Guide Tones, Minimal Motion, Counterpoint, Distance, Register Constraints
- **L Advanced:** Neo-Riemannian, Tonnetz, Transformational Theory, Pitch-Class Sets, geometrische Beziehungen
- **M Computational:** symbolische Repräsentationen, Parsing, Roman Numerals, Analyse, Graphen, Regelgrammatiken, Constraints
- **N Pädagogik/Analyse:** konkurrierende Analysemodelle, Erklärungsebenen, Lernvoraussetzungen, Fehlerbilder, Übungen

Schematisches Wissensobjekt:

```yaml
id: THEORY-0001
slug: ""
title_de: ""
title_en: ""
aliases: []
domain: ""
definition: ""
extended_explanation: ""
prerequisites: []
related_concepts: []
theoretical_traditions: []
repertoire_scope: []
formal_properties: []
rules: []
examples: []
counterexamples: []
alternative_interpretations: []
limitations: []
sources: []
verification_status: draft
review_status: pending
version: 0.1.0
```

Entwickle daraus ein gültiges, versioniertes Schema. Nur überprüfte Fundstellen als belegt markieren. Nicht belegte Inhalte als offene Arbeit kennzeichnen.

### 9. Phase 4 – Formal Rules & Analytical Models

Überführe geeignete Erkenntnisse zusätzlich in maschinenlesbare Regeln. Unterscheide `constraint`, `tendency`, `convention`, `transformation`, `interpretation`, `heuristic` und `empirical_observation`.

Pro Regel: stabile ID, Aussage, Voraussetzungen, Gültigkeitsbereich, Stilkontext, Ausnahmen, Gegenbeispiele, verwandte Regeln, Quellen und Validierungsstatus.

Eine typische Auflösungstendenz der Sekundärdominante darf nicht zur ausnahmslosen Regel umgedeutet werden. Bewahre klassische, jazzbezogene, pop-/rockbezogene, modale und transformationale Analyseperspektiven nebeneinander. Ermögliche konkurrierende Interpretationen derselben Akkordfolge.

### 10. Phase 5 – Progression Library & Musical Examples

Baue eine strukturierte Sammlung zu diatonischen und funktionalen Progressions, Modal Progressions, Pop/Rock Loops, Bluesformen, Jazz Turnarounds, ii–V–I, Secondary Dominants, Modal Interchange, Chromatic Progressions, Reharmonizations, Voice Leading und mehrdeutigen Analysen auf.

Jedes Beispiel erhält, soweit fachlich begründbar: ID, Kontext, Tonart/Modus, Akkordfolge, Roman-Numeral-Analyse, Funktionsanalyse, Alternativen, Erklärung, Regel- und Konzeptbeziehungen, Quellen und Validierungsstatus.

Bevorzuge eigene validierte Beispiele oder klar lizenzierte Materialien. Keine unzulässige Übernahme umfangreicher geschützter Musikbeispiele.

### 11. Phase 6 – Research Reconciliation & Knowledge Expansion

Vergleiche vorhandene Papers mit tatsächlich ausgewerteten Quellen. Ermittle Übereinstimmungen, Widersprüche, unvollständige Modelle, doppelte Fachbegriffe, Synonyme, fehlende Voraussetzungen, unerschlossene Gebiete, schwache Belege, fehlende Primärquellen und weitere Lücken.

Erstelle ein dauerhaftes Gap Register mit ID, Fachgebiet, Problem, Auswirkungen, Quellenbedarf, Priorität, Prüfschritten und Status.

Recherchiere ergänzend, soweit Werkzeuge und überprüfbare Quellen verfügbar sind. Bevorzuge wissenschaftliche Primärliteratur, seriöse Lehrwerke, Hochschulmaterialien und rechtlich klare offene Quellen. Ergänze bestehende Wissensobjekte statt parallele Duplikate zu schaffen. Erhalte begründete Kontroversen.

### 12. Phase 7 – Documentation & Skill Integration

Untersuche bestehende Steps-Dokumentation und führe die Wissensstrukturen sinnvoll mit ihr zusammen. Keine redundanten Archive, keine stillschweigende Umdeutung bestätigter Entscheidungen, keine unkontrollierten Wissenskopien, keine große Enzyklopädie in `SKILL.md`, keine Vermischung von Wissenschaft und Entwicklungsanweisung.

Erstelle eine kompakte Knowledge-Base-Einstiegsdokumentation und beschreibe, wie der künftige Skill auf versionierte Quellen zugreifen kann. Bestehende `SKILL.md` nur im notwendigen Umfang anpassen; kein vollständiger Skill-Neubau.

### 13. Phase 8 – Scientific Validation & Quality Assurance

**Strukturprüfung:** eindeutige IDs, gültige Schemata, korrekte interne Links, existierende Referenzen, Taxonomie, Metadaten, Dokumentationslinks, Versionen, Duplikate und verwaiste Objekte.

**Wissenschaftliche Prüfung:** Quellenexistenz, Claim-Source-Zuordnung, Fundstellen, Gültigkeitsgrenzen, alternative Deutungen, Regeln vs. Tendenzen, Unsicherheiten und Unterscheidung zwischen Theorie und Corpus-Beobachtung. Strukturtests ersetzen kein fachliches Review.

**Referenzfälle:** Intervalle, Enharmonik, Tonleitern, Akkordkonstruktion, Akkordsymbole, Roman Numerals, Transposition, Secondary Dominants, Modal Interchange, Kadenzen, Modulation, Voice Leading, Mehrdeutigkeit.

Führe vorhandene Validatoren und Tests tatsächlich aus. Nicht ausführbare Checks begründen.

### 14. Copyright, Licenses & Provenance

Unterscheide Forschungslektüre, Zusammenfassung, Zitat, Textübernahme, musikalisches Beispiel, Datensatzimport und öffentliche Wiederveröffentlichung. Speichere geschützte Bücher, kommerzielle Produktunterlagen und ungeprüfte Korpora nicht unzulässig im öffentlichen Repository. Sichere Herkunft und Lizenz pro Quelle, Datensatz und Beispiel. Bei ungeklärter Rechteposition nur bibliografisch verweisen und eigene sachliche Zusammenfassungen verwenden.

### 15. Data Provenance & Citation Integrity

Verknüpfe wesentliche Wissensaussagen rückverfolgbar:

**Knowledge Object → Atomic Claim / Rule → Source ID → Exact Source Location**

```yaml
evidence:
  - source_id: SRC-0001
    locator_type: page
    locator: "42"
    verification_status: verified
```

Das Beispiel zeigt eine Struktur, keine tatsächliche Fundstelle. Nur real überprüfte Seiten/Kapitel eintragen. Nicht verifizierte Angaben entsprechend markieren.

Chat-interne `turn...search...`- und `turn...file...`-Marker sind temporär. Soweit möglich in DOI, URL, Ausgabe, Seiten- oder Kapitelangabe überführen; ungelöste Marker im Citation Resolution Register festhalten.

### 16. Versioning & Maintenance

Pflege unabhängige Schema-, Knowledge-Base- und Objektversionen sowie Changelog, Quellenstatus, Reviewstatus und Migrationsregeln. Geeignete SemVer-Regeln für Schemata; neue unfertige Bestandteile mit Entwicklungsversionen beginnen; vorhandene Versionen nicht zurücksetzen. Keine stabile V1.0 behaupten, solange Kriterien fehlen.

**New Source → Metadata Check → License Check → Extraction → Concept Linking → Conflict Review → Validation → Version Update**

Erstelle eine Wartungsanleitung für spätere Codex-Runs.

### 17. Priorität und Reihenfolge

**P0 – Verlässliche Grundlage:** Repository-Audit, Dokumenten-/Quelleninventar, Quellen-/Lizenzstatus, vorhandene Wissensstruktur, Konflikte.

**P1 – Fachlicher Kern:** Grundlagen, Tonleitern/Modi, Akkordtheorie, funktionale Harmonik, Progressions, Roman Numerals, Enharmonik, Modal Interchange, Secondary Dominants.

**P2 – Vertiefte Harmonik:** Chromatik, Jazz, Pop/Rock, Blues, Reharmonization, Voice Leading, Modulation und Mehrdeutigkeit.

**P3 – Erweiterte Forschung:** Neo-Riemannian, Transformationsmodelle, geometrische Harmonik, Corpus-Analyse, Computational Formalization.

**P4 – Zukünftige Integration:** Skill References, Anwendungsspezifikationen, langfristige Evaluation und spätere Produktfunktionen.

### 18. Verbindliche Arbeitsregeln

1. Selbstständig vom realen Projektstand ausgehen.
2. Keine leeren Platzhalter als fertig ausgeben.
3. Keine Quellen, Daten oder Ergebnisse erfinden.
4. Vorhandenes Wissen bewahren.
5. Duplikate vermeiden.
6. Fachliche Änderungen begründen.
7. Alternative Theorien erhalten.
8. Quellenfakten und Vorschläge trennen.
9. Unsicherheit dokumentieren.
10. Modular erweitern.
11. Offene, wartbare Formate verwenden.
12. Hauptsächlich Dokumentation und Wissensbereich ändern.
13. Keine große neue GUI/App-Funktionalität.
14. Indizes und Links konsistent aktualisieren.
15. Tests ausführen.
16. Nicht bearbeitete Quellen ausweisen.
17. Projektkompatibilität schützen.
18. Ohne Auftrag kein Merge.
19. Bei begrenzter Bearbeitungszeit tatsächliche Abdeckung und Restbacklog festhalten.
20. Einen Plan nie als fertiges Arbeitsergebnis ausgeben.

### 19. Definition of Done

Die Erstellung einer Ordnerstruktur allein genügt nicht. Soweit aus den vorhandenen Quellen möglich, müssen vorliegen:

- Geprüfter Repository-Ausgangsstand
- Source Inventory / Source Registry
- Lizenz- und Provenienzregister
- Navigation und Versionierung
- Metadatenschemata
- Tatsächlich befüllte Theorieobjekte
- Regeln und Analysemodelle
- Ausgearbeitete Progressionsbeispiele
- Fachliche Querverweise
- Verbindung zentraler Forschungsergebnisse
- Gap Register und Konfliktdokumentation
- Tests und Validation Reports
- Wartungsanleitung und Changelog

Prüfe, ob hochpriorisierte zugängliche Quellen tatsächlich ausgewertet wurden. Weise die Abdeckung pro Fachgebiet aus; leere Verzeichnisse zählen nicht als Wissensabdeckung.

### 20. Abschließender Bericht

**A Repository Status:** geprüfter Branch, Änderungen, neue/angepasste Dateien und erhaltene Strukturen.

**B Source Coverage:** identifizierte, verfügbare, lesbare, bearbeitete, validierte und nicht zugängliche Quellen sowie Lizenzlücken.

**C Knowledge Coverage:** tatsächliche Konzepte, Regeln, Beispiele, erschlossene und offene Fachgebiete.

**D Validation:** ausgeführte, bestandene, fehlgeschlagene und nicht ausführbare Prüfungen.

**E Research Reconciliation:** zusammengeführte Erkenntnisse, Widersprüche, unbestätigte Aussagen, ungelöste Marker.

**F Next Actions:** priorisierte Restaufgaben, Forschungsquellen, Reviews und Folgearbeiten.

Falls ein Pull Request erstellt wird, dokumentiere ihn. Nicht automatisch mergen.

### 21. Startanweisung

Beginne mit der tatsächlichen Überprüfung des Steps-Repositories und aller zugänglichen Forschungsunterlagen. Arbeite in der Reihenfolge der Phasen. Nutze den vorhandenen Projektstand, bevor du neue Strukturen definierst.

**Baue die Knowledge Base nicht nur konzeptionell auf, sondern fülle sie mit überprüfbaren Fachinformationen und ihren Beziehungen.** Verarbeite so viele hochpriorisierte, zugängliche Quellen mit wissenschaftlicher Sorgfalt wie möglich. Dokumentiere präzise, was erledigt, teilweise erledigt oder offen ist.

**Ziel: eine dauerhaft nutzbare, wissenschaftlich belastbare und kontinuierlich erweiterbare Wissensinfrastruktur für Steps. Starte die Umsetzung jetzt.**

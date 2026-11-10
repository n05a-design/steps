# STEPS – Computational Knowledge Specification V3

## 1. Ziel: ein typisiertes Multi-Representation-System

Die Knowledge Base hält Quellwissen und überprüfte fachliche Aussagen; die Engine konsumiert normierte Symbolik; ein späterer Agent-Skill erklärt/prüft diese. `SKILL.md` ist ein Workflow-Router, nicht der einzige Speicher für Regeln und Beispiele. Startkonvention für die V3-Seed-Dateien: internationale Akkordnamen `B=H`, `Bb=B`, explizit `tuning=12-TET` soweit Pitch Classes genutzt werden. Andere Tunings/Traditionen erfordern separate Model Providers.

### 1.1 Objektfamilien

- **SourceRecord**: stabile Source-ID, Version/Edition, DOI/URL, Autorenschaft, Metadaten-Prüfstatus, tatsächlicher Lese-/Locator-Status, Nutzungsrechte, Reuse-Gate.
- **EvidenceClaim**: atomare Behauptung, `source_id`, exakter Abschnitt/Seite nur wenn gelesen, Stil-/Zeit-Scope, Gegenquellen, Status, Reviewer.
- **TheoryConcept**: Name DE/EN, Aliase, Definition, vorausgesetzte Begriffe, konkurrierende Schulen, Querverweise, Claim-IDs.
- **TonalContext**: Tonic candidates, global/local key, mode candidates, enharmonic conventions, notation locale, tunings and style.
- **ChordSymbol**: root+spelling, quality, seventh/extensions, alterations, omission, suspension, bass, symbol dialect.
- **Voicing**: tatsächliche `SpelledPitchEvents` mit Oktave, Register, Stimme, Instrument, Dauer.
- **Progression**: Event-IDs mit onset/duration, chord reference, context, analysis-lens candidates, phrase positions, possible melody constraints.
- **Rule**: `constraint | tendency | convention | transformation | interpretation | heuristic | empirical_observation`, conditions/scope, exceptions, countercases, evidence, tests.
- **Motif/Phrase/Form**: motivische Gestalt, Referenznoten, Rhythmus, Transformationsketten, Formrelationen, Abschnitte mit Ziel/Kontrast.
- **CompositionPlan**: Brief, Originalmaterial, tonaler/harmonischer Plan, Entwurfsschritte, Instrumentation, Iterationen, Reviews, Rechte.
- **EvaluationCase**: gegebenes Ausgangsobjekt, explizit erwarteter Befund oder Interpretationsspielraum, maschinenprüfbar/menschlich, Reviewer.

### 1.2 Prüfbares Beispiel

```json
{
  "id": "EXAMPLE-V3-001",
  "tuning": "12-TET",
  "symbol_dialect": "international_leadsheet",
  "tonal_context": {
    "tonal_center_candidates": ["C major", "A Aeolian"],
    "uncertainty": "needs_melody_meter_context"
  },
  "meter": "4/4",
  "events": [
    {"start_beats": 0, "duration_beats": 4, "chord": "Am"},
    {"start_beats": 4, "duration_beats": 4, "chord": "F"},
    {"start_beats": 8, "duration_beats": 4, "chord": "C"},
    {"start_beats": 12, "duration_beats": 4, "chord": "G"}
  ],
  "analysis_candidates": [
    {"lens": "roman_major", "context": "C major", "degrees": ["vi", "IV", "I", "V"]},
    {"lens": "modal_aeolian", "context": "A Aeolian", "degrees": ["i", "bVI", "bIII", "bVII"]}
  ],
  "status": "original_example_draft"
}
```

### 1.3 Datenintegrität

`source_claim` darf nie allein aus einem URL-Text automatisch `reviewed` werden. `edition` muss ein Primär-/Sekundärwerk von einem bloßen Verlags-Eintrag unterscheiden. Eine Harmonie- und eine Kompositionsregel dürfen gemeinsame Wissensobjekte verwenden, ohne auf Dateiduplikate angewiesen zu sein. Transposition muss Tonhöhen- und Intervallrelationen unter expliziter Stimmung bewahren, während eine nachfolgende Schreibfunktion die Enharmonik innerhalb der neuen Tonart neu herstellt. Konvertierung in MIDI/MusicXML/MEI kann informationelle Verluste besitzen; diese sind als Mapping-Report nachzuweisen.

## 2. Technische Arbeitsbibliotheken und Standards

`music21` ist ein Referenzkandidat für `RomanNumeral` und Musiknotation, `Harte` ein Syntaxreferenzkandidat für lead-sheet chord labels, `DCML` für analytische Chord-Lenses, `JAMS/ChoCo` für zeitbezogene Chord-Annotation, `MusicXML` und `MEI` für Partitur-/Editorformate. Kein Standard wird blind zur universellen STEPS-Definition. Bibliotheken erst nach echtem Repository-Audit und Lizenz-/Kompatibilitätsentscheidung installieren; keine ungeprüfte neue Runtime-Dependency als harte Voraussetzung.

## 3. Skill-Ausgabeformen

1. `explanation`: knappe Erklärung mit Source/Status.
2. `analysis`: mehrere Lenses mit Tonikakandidaten, Akkorden, Formhinweisen.
3. `progression_explorer`: mögliche harmonische Nachbarn, warum und unter welchen Annahmen.
4. `composition_planner`: Motive, Phrase/Form, Harmonic Plan, Bass, Instrumentation, Varianten.
5. `reharmonization`: feste Melodie und mehrere begründete Änderungen.
6. `formalization`: Schema/Rule/Test oder Nachweis einer offenen Evidenzlücke.

Der Agent muss jeweils explizit zwischen `verified`, `research_supported`, `draft`, `hypothesis` und `unsupported` unterscheiden. Keine erfundenen Seitenzahlen, Recording-Analysen oder Corpus-Zahlen.

## 4. Datenbank vor Produktfunktion

Die V3-Konzepte sind maschinenlesbare redaktionelle Seeds, keine ausführbare Harmony Engine. Erstes Codex-Arbeitspaket ist deshalb Importierung, Normalisierung und Validation plus kleine Read-only Queries. Kein umfangreicher UI-/Generationsneubau und kein ungefragter Merge nach main. Musiktheoretische Erklärungen sind erst nach fachlicher Prüfung als kanonisch auslieferbar.

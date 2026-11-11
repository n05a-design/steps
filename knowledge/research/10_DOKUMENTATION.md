# STEPS – Dokumentationskonsolidierung & Kanonische Hierarchie (Phase J Audit)

**Dokumenttyp:** SYSTEMATISCHE DOKUMENTATIONSHIERARCHIE & STATUSREGISTER  
**Projekt:** STEPS – Musikalische Wissensbibliothek & Theorie-Kern  
**Geltungsbereich:** Gesamte Repository-Dokumentation, Handover-Protokolle, ADRs & Spezifikationen  
**Status:** `AUDITED & CONSOLIDATED`  

---

## 1. Kanonische Dokumentationshierarchie (Single Source of Truth)

Um Widersprüche und parallele Scheinwahrheiten dauerhaft zu verhindern, gilt im STEPS-Projekt eine strikte Dokumentationsordnung nach fünf Vertrauensebenen:

```mermaid
graph TD
    subgraph Level1 ["Ebene 1: Verbindliche Beschlüsse & Primärregeln"]
        AGENTS["AGENTS.md<br>(Arbeitsvertrag & Qualitätsregeln)"]
        ADR["decisions/DECISION_REGISTER.md<br>(ADR-001 bis ADR-012)"]
        OA["%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md<br>(Zentrale Masterdatei der Aufgaben)"]
    end

    subgraph Level2 ["Ebene 2: Kanonische Fachbibliothek & Datenmodelle"]
        PROG["knowledge/concepts/progressions/<br>(CHORD_PROGRESSION_REFERENCE_LIBRARY.md - 28 Progressionen)"]
        DRUM["knowledge/concepts/styles/<br>(DRUM_GROOVE_REFERENCE_LIBRARY.md - 31 Grooves)"]
        PIANO["knowledge/concepts/chords/<br>(PIANO_PRACTICE_REFERENCE_LIBRARY.md - 19 Module)"]
        REL["knowledge/relations/<br>(MUSIC_CONCEPT_RELATIONS.csv - 94 Kanten)"]
    end

    subgraph Level3 ["Ebene 3: Technische Soll-Spezifikationen & Architektur"]
        ENG_MUSIC["docs/engineering/MUSIC_DOMAIN_AND_MIDI.md<br>(5 Musiktheorie-Axiome & Datenmodelle)"]
        ENG_SHELL["docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md<br>(UI-Entkopplung & Tk-Free Core)"]
        PROD_STRAT["docs/product/PRODUCT_STRATEGY_AND_MVP.md<br>(v0.1 Chords Scope vs. v0.2 Drums)"]
    end

    subgraph Level4 ["Ebene 4: Verifikations- & Auditnachweise (Aktuelle Phase)"]
        BASELINE["knowledge/research/REFERENCE_IDENTITY_BASELINE.json<br>(Baseline v1.2.0)"]
        ERR_REG["knowledge/research/MUSICAL_ERROR_REGISTER.csv<br>(ERR-001 bis ERR-037)"]
        GOLDEN["knowledge/research/golden_cases/golden_reference_cases.json<br>(198 Referenzfälle)"]
        AUDIT_PKG["knowledge/research/master_audit/<br>(14 nummerierte Lieferartefakte)"]
    end

    subgraph Level5 ["Ebene 5: Forschungsarchive & Historische Bestände (Read-Only)"]
        BIB["research/STEPS_Bibliothek/<br>(V6.6 Ableton Blog Archiv & Forschungsnotizen)"]
        ARCHIVE["archive/ & source_archive/<br>(Unveränderte historische Ausgangsstände)"]
    end

    Level1 --> Level2
    Level2 --> Level3
    Level3 --> Level4
    Level4 -.-> Level5
```

---

## 2. Abgrenzung & Zuständigkeiten

| Fachbereich | Kanonischer Fundort (Einzige verbindliche Wahrheit) | Abgeleitete / Sekundäre Dokumente |
|---|---|---|
| **Aufgaben & Arbeitsaufträge** | `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md` | `OWNER_TASK_AND_ADR_MAPPING.csv`, `EXECUTION_BACKLOG.md` |
| **Architekturentscheidungen** | `decisions/DECISION_REGISTER.md` (ADR-001..012) | `ADR_HISTORICAL_IDENTITY_MATRIX.csv`, `ADR_IDENTITY_LOCK_REPORT.md` |
| **Akkordprogressionen** | `knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md` (PROG-001..028) | `PROG021_HISTORICAL_RECONCILIATION.md`, `REFERENCE_IDENTITY_BASELINE.json` |
| **Rhythmen & Drum Grooves** | `knowledge/concepts/styles/DRUM_GROOVE_REFERENCE_LIBRARY.md` (PAT-001..031) | `DRUM_PATTERN_VALIDATION.csv`, `GENRE_RESEARCH_*.md` |
| **Klavierpraxis-Module** | `knowledge/concepts/chords/PIANO_PRACTICE_REFERENCE_LIBRARY.md` (P01..019) | `07_DIDAKTISCHE_PRUEFUNG.md`, `LEARNING_AND_EXPERIENCE.md` |
| **Wissensgraph & Taxonomie** | `knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv` (94 Kanten) | `06_KATEGORISIERUNG.md`, `KNOWLEDGE_GRAPH_IDENTITY_AUDIT.md` |
| **Wissenschaftliche Quellen** | `knowledge/sources/curated_sources_registry.yaml` & `MUSIC_SOURCE_CLAIM_REGISTER.csv` | `05_QUELLENREGISTER.md`, `MUSIC_SOURCE_REVIEW_PROGRESS.csv` |
| **Fehler- & Korrekturstand** | `knowledge/research/MUSICAL_ERROR_REGISTER.csv` (ERR-001..037) | `03_FACHLICHE_FEHLER.md`, `MUSICAL_CORRECTION_REPORT.md` |
| **Referenz- & Testfälle** | `knowledge/research/golden_cases/golden_reference_cases.json` (REF-0001..0198) | `FINAL_REFERENCE_CASE_VALIDATION.csv`, `tests/golden_cases/` |

---

## 3. Konsolidierungsmaßnahmen & Bereinigungen

1. **Header- und Zähler-Synchronisation:** Alle Diskrepanzen zwischen Bibliotheks-Headern, Dokumenttiteln und Zeilenanzahlen (PROG-028, PAT-031, P19) wurden in den Primärdateien und Metadatenmatrizen bereinigt (`ERR-035`, `ERR-036`, `ERR-037`).
2. **Historische Bewahrung (Preservation-First):** Veraltete Berichte früherer Phasen (z. B. Phase 4.10, Phase 4.15, Phase 4.16) werden nicht gelöscht, sondern als historische Audit-Meilensteine in `knowledge/research/` und `%LOCALAPPDATA%\StepsAudit\` erhalten.
3. **Klare Trennung zwischen App- und Forschungsversionen:** Die Bezeichnung `V6.6 / V6.7` gilt ausschließlich für das Archiv der Ableton-Blog-Forschungskarten in `research/STEPS_Bibliothek/`; die STEPS-Kernsoftware befindet sich in Phase-5-Vorbereitung (MVP v0.1).

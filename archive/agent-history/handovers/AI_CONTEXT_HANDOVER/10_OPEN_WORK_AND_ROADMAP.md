# 10 – Offene Arbeiten & Roadmap (OPEN_WORK_AND_ROADMAP)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Stand:** Nach Abschluss von Phase 5.1 (Headless Music Theory Core Hardening)  

---

## 1. Register offener Aufgaben (NEXT-001 bis NEXT-010)

| Task-ID | Bereich | Bezeichnung & Ziel | Voraussetzungen | Priorität |
|---|---|---|---|:---:|
| `NEXT-001` | Architektur | Formale Entscheidung zu **ADR-001** (Desktop GUI Framework) | Owner-Entscheidung | **P1 (Entscheidung)** |
| `NEXT-002` | Core (M03) | **Phase 5.2:** Skalen- und Modus-Engine (`src/steps/theory/scale.py`) | Phase 5.1 Kern (fertig) | **P1 (Funktional)** |
| `NEXT-003` | Audio (M01/M08) | **Phase 5.3:** Headless MIDI- & Audio-Synthese (`src/steps/audio/`) | Phase 5.1 Kern (fertig) | **P2 (Funktional)** |
| `NEXT-004` | Recommender (M05) | **Phase 5.4:** Graph-basierte harmonische Pfadsuche & Substitutionen | 97 Graph-Relationen (fertig) | **P2 (Algorithmus)** |
| `NEXT-005` | UI-Entwicklung | **Phase 6.0:** Desktop-Interface-Scaffolding (`app/ui/`) | ADR-001 Freigabe | **P3 (Gated)** |
| `NEXT-006` | Didaktik (M10) | Interaktive Lernmodule basierend auf Didaktik-DAG (ADR-010) | Phase 5.2 | **P3 (Erweiterung)** |
| `NEXT-007` | Import/Export | MusicXML und MIDI-File Parser/Generator (`src/steps/io/`) | Phase 5.1 Kern (fertig) | **P2 (Integration)** |
| `NEXT-008` | Genre-Engine | Automatisierte Stilerkennung basierend auf 9 Genre-Profilen | Phase 5.4 | **P3 (Feature)** |
| `NEXT-009` | Dokumentation | Sphinx/MkDocs API-Referenz für `src/steps/` | Phase 5.1 Kern (fertig) | **P2 (Doku)** |
| `NEXT-010` | CI-Monitoring | Überwachung der GitHub Actions Runner-Zyklen auf `origin` | Push `fe66637` (fertig) | **P1 (Monitoring)** |

---

## 2. Detaillierte Spezifikation von Phase 5.2 (Skalen- & Modus-Engine)

- **Modulpfad:** `src/steps/theory/scale.py`
- **Inhalte:**
  - Diatonische Modi: Ionisch, Dorisch, Phrygisch, Lydisch, Mixolydisch, Äolisch, Lokrisch.
  - Harmonisch & Melodisch Moll Modi: Alteriert, Lydisch Dominant, Phrygisch Dominant, etc.
  - Symmetrische Skalen: Ganztonskala, Halbton-Ganzton (HTGT), Ganzton-Halbton (GTHT), Chromatik.
  - Pentatonik & Blues-Skalen: Dur- und Moll-Pentatonik, Blues-Skala (mit Blue Notes).
  - Skalen-Akkord-Kompatibilitätsmatrix (Chord-Scale-Theory nach Levine 1995 und Russell 2001).
- **Testabdeckung:** Mindestens 25 neue Unittests für Skalenkonstruktion, Modi-Transposition und Akkord-Skalen-Matching.

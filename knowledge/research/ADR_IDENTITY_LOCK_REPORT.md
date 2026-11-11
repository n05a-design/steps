# STEPS – ADR Identity Lock & Historical Reconstruction Report (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** FULLY RECONSTRUCTED & LOCKED (Gate 1 Passed)  
**Autor:** Leitender Software-Architekt & QA-Auditor  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil I  

---

## 1. Problemstellung & Befund (Kritischer ADR-Identitätskonflikt)

In Phase 4.16 wurde im Rahmen des `OWNER_DECISION_BRIEF.md` eine folgenschwere semantische Fehlzuordnung vorgenommen:
1. **ADR-002** wurde als *„Aufbewahrungs- versus Löschrichtlinie historischer Web- und MIDI-Dateien“* bezeichnet.
2. **ADR-005** wurde als *„Release-, Packaging- und Auslieferungsmodell mit PyInstaller“* bezeichnet.

Diese Bezeichnungen standen in direktem Widerspruch zu den kanonischen Primärquellen des STEPS-Repositories:
- **`decisions/DECISION_REGISTER.md` (Commit `7e9b66b`):**
  - **ADR-002:** *Vision und MVP Chords/Drums* (Phasen-Splitting: Chords zuerst im testbaren Kern, Drums für v0.2+ zurückgestellt).
  - **ADR-005:** *Fachmodell* (Pitch-Class vs. Spelling, deutsches H/B vs. internationales B/Bb, funktionale Enharmonik).
- **`%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`:**
  - **OA-0004 & OA-0012:** Ausdrücklich an **ADR-002** (MVP-Umfang: Phasen-Splitting Harmonik vs. Drums) gekoppelt.
  - **OA-0005:** Ausdrücklich an **ADR-005** (Notationskonventionen & Enharmonik) gekoppelt.

Die willkürliche Umwidmung bestehender Architektur-IDs als Platzhalter für neue Themen verletzt den Arbeitsvertrag (Regel 2: *Preservation-first* und Regel 3: *Verifikation*).

---

## 2. Revisions- & Korrekturregel

Gemäß Abschnitt 1.2 des Phase-4.17 Master Prompts gilt ab sofort verbindlich:
1. **Identitätsschutz:** Eine bestehende ADR-ID darf **niemals** für eine andere Architekturentscheidung recycelt oder umgewidmet werden.
2. **Historische Gültigkeit:**
   - **ADR-001:** STEPS-Fensterarchitektur (1 Root, 2 Panes vs. 2 Toplevel).
   - **ADR-002:** MVP-Umfang (Phasen-Splitting: Chords v0.1 vs. Drums v0.2+).
   - **ADR-005:** Fachmodell Harmonielehre (Notationskonventionen: H/B vs. B/Bb und Enharmonik).
3. **Freie Neuzuweisung für neue Themenbereiche:**
   - Das Thema *Release-Packaging und Auslieferung* erhält die bisher ungenutzte freie ID **ADR-011**.
   - Das Thema *Aufbewahrungs- und Bereinigungsrichtlinie für historische Web- und MIDI-Dateien* erhält die bisher ungenutzte freie ID **ADR-012**.

---

## 3. Vollständige Kanonische ADR-Übersicht (ADR-001 bis ADR-012)

| ADR-ID | Kanonischer Titel | Thema / Tragweite | Zugeordnete OA-ID | Status |
|:---:|---|---|:---:|:---:|
| **ADR-001** | Zwei Fenster / Shell-Layout | 1 Root mit 2 Panes (Harmonik links, Visualisierung rechts) vs. 2 Toplevel-Fenster | `OA-0003` | `PROPOSED` |
| **ADR-002** | Vision und MVP Chords/Drums | Phasen-Splitting: Harmonielehre-Kern für v0.1; Drums explizit auf v0.2+ zurückgestellt | `OA-0004`, `OA-0012` | `PROPOSED` |
| **ADR-003** | Glide-Code-Quelle | Technischer Reuse: Glide 3.53.0-Stand nur nach Commit/Backup und QA | `OA-0007` | `PROPOSED` |
| **ADR-004** | License / Brand | Lizenzierung unter MPL 2.0 für eigene Dateien; Fremdassets separat auditieren | `OA-0001` | `PROPOSED` |
| **ADR-005** | Fachmodell & Notationskonventionen | Mathematische Trennung Z12-Pitch-Class vs. Spelling; deutsches H/B vs. int. B/Bb | `OA-0005` | `PROPOSED` |
| **ADR-006** | Datenhaltung & Schemavalidierung | JSON-Dateien mit formalen Schemata und atomaren Schreibern; SQLite/DB erst bei Bedarf | `OA-0006`, `OA-0008` | `PROPOSED` |
| **ADR-007** | Audio / MIDI Engine | Abstrakte Port-Architektur zuerst; plattformspezifische Backends nach Benchmark | `OA-0028`, `OA-0029` | `PROPOSED` |
| **ADR-008** | KI-Skill-Architektur | Router + indexierte Originalreferenzen + Claim-Registry; keine unzulässigen Volltextkopien | `OA-0011` | `PROPOSED` |
| **ADR-009** | Historische 21/39-Verzeichnisse | Preservation-First: Strukturierte Beibehaltung und schrittweise Migration | `OA-0008` | `PROPOSED` |
| **ADR-010** | Public-Repository-Medien | Veröffentlichungspolitik: Keine neuen urheberrechtlich geschützten Medien im Repo | `OA-0001` | `PROPOSED` |
| **ADR-011** | Release-Packaging & Auslieferung | Hybride Distribution: Python Core auf PyPI; Standalone-Desktop-Bundle via PyInstaller | `OA-0013` | `PROPOSED` |
| **ADR-012** | Aufbewahrungsrichtlinie Web/MIDI | Strategie für historische Drittanbieter-Scrapes (Option A Privat vs. B/C Purge) | `OA-0001`, `OA-0033` | `PROPOSED` |

---

## 4. Technischer ADR-Identity-Lock

Zur dauerhaften Absicherung gegen künftige Umwidmungen wurde das Prüfwerkzeug `scripts/verify_reference_integrity.py` erweitert:
1. **Kanonische Prüfung:** Liest `decisions/DECISION_REGISTER.md` und vergleicht die Einträge gegen die deterministische Matrix `knowledge/research/ADR_HISTORICAL_IDENTITY_MATRIX.csv`.
2. **Fail-Closed Verhalten:**
   - Abweichungen im Thema oder in der ID lösen einen Validierungsfehler aus.
   - Statuswechsel erfordern explizite Autorisierung.
3. **Negative Gegenproben:** In `tests/test_reference_integrity.py` implementiert (z. B. Mutation von ADR-005 auf 'PyInstaller' schlägt sofort mit Exit-Code != 0 fehl).

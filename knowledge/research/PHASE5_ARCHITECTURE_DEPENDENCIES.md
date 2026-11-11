# STEPS – Phase 5 Architecture Dependencies & Gating Analysis (Phase 4.17)

**Datum:** 2026-11-11  
**Status:** ARCHITECTURALLY GATED (Gate 10 Assessed)  
**Autor:** Leitender Software-Architekt  
**Referenzdokument:** Phase 4.17 Master Prompt, Teil VIII  

---

## 1. Grundsatz des verantwortungsvollen Entwicklungsübergangs

Gemäß Abschnitt 8.1 des Master Prompts und Regel 3 (*Verifikation*) darf **keine produktive Implementierung begonnen werden, die unbestätigte oder offene Architekturentscheidungen vorwegnimmt**.

Die Erklärung der "Phase-5-Readiness" im Phase-4.16-Bericht bedarf einer präzisen Differenzierung:
- **Fachlich & Test-technisch:** Das Fundament ist zu 100 % bereit (`KNOWLEDGE_FOUNDATION_READY`, `TEST_INFRASTRUCTURE_READY`).
- **Architektonisch:** Bestimmte Entwicklungsbereiche sind durch noch offene Eigentümerentscheidungen strikt **blockiert** (`ARCHITECTURE_APPROVED` = `BLOCKED_PENDING_OWNER`).

---

## 2. Gating-Matrix: Freigegebene vs. Blockierte Entwicklungspfade

| Entwicklungsbereich | Geplante Module | Abhängige ADR / Task | Status für Phase 5 | Begründung & Schutzgrenze |
|---|---|:---:|:---:|---|
| **Headless Core Harmonielehre** | `src/steps/theory/pitch.py`<br>`src/steps/theory/interval.py`<br>`src/steps/theory/triad.py`<br>`src/steps/theory/seventh.py` | `ADR-002` (MVP Scope)<br>`ADR-005` (Fachmodell) | **VORBEREITET / BEREIT NACH ADR-005 ZEICHNUNG** | Reines Python-Modell ohne GUI- oder Audio-Abhängigkeiten. Benötigt formelle Bestätigung von ADR-005 (Trennung Z12 vs. H/B-Spelling). |
| **Akkordprogressions- & Kadenzen-Engine** | `src/steps/progression/cadence.py`<br>`src/steps/progression/circle.py`<br>`src/steps/progression/voice_leading.py` | `ADR-002` (MVP Scope) | **VORBEREITET / BEREIT NACH ADR-002 ZEICHNUNG** | Baut auf 28 Progressionen auf; implementiert Stimmführungsmetriken (Tymoczko Metric). |
| **Desktop-GUI & Visualisierungs-Shell** | `app/ui/main_window.py`<br>`app/ui/chord_selector.py`<br>`app/ui/voicing_roll.py` | `ADR-001` (Fensterarchitektur)<br>`ADR-003` (Glide Reuse) | **STRIKT BLOCKIERT** | Darf keinesfalls vor der Zeichnung von ADR-001 (1 Root mit 2 Panes vs. 2 Toplevel) begonnen werden, um irreversible UI-Fehlentwicklungen zu verhindern. |
| **Audio-Synthese & MIDI-Engine** | `src/steps/midi/smf_parser.py`<br>`src/steps/midi/ports.py` | `ADR-007` (Audio/MIDI)<br>`ADR-002` (MVP Scope) | **ZURÜCKGESTELLT FÜR v0.2+** | Gemäß ADR-002 nicht Bestandteil von v0.1. |
| **Schlagzeug- & Drum-Groove-Engine** | `src/steps/rhythm/groove.py`<br>`src/steps/rhythm/dilla_swing.py` | `ADR-002` (MVP Scope) | **ZURÜCKGESTELLT FÜR v0.2+** | Explizit aus v0.1 ausgegliedert. |
| **Public GitHub Release / Packaging** | `setup.py`, Standalone Bundle | `ADR-011` (Packaging)<br>`OA-0001` (Rechte-Triage) | **STRIKT BLOCKIERT** | Öffentliche Auslieferung blockiert, bis OA-0001 durch den Owner entschieden wurde (Option A Privat vs. C Purge). |

---

## 3. Handlungsempfehlung für den kontrollierten Einstieg in Phase 5

1. **Schritt 1 (Owner-Aktion):** Zeichnung von `ADR-001`, `ADR-002` und `ADR-005` im `ADR_OWNER_DECISION_BRIEF.md`.
2. **Schritt 2 (Entwicklungsfreigabe Phase 5.1):** Nach Zeichnung von ADR-005 und ADR-002 kann unmittelbar mit der Implementierung des reinen Headless-Theoriekerns in `src/steps/theory/` begonnen werden.
3. **Schritt 3 (Entwicklungsfreigabe Phase 5.2):** Nach Zeichnung von ADR-001 kann die Entkopplung der UI-Shell in `app/ui/` erfolgen.

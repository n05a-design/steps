# STEPS – PRIORISIERTER MASSNAHMENPLAN
## Konkrete Roadmap für Phase 5.2, Phase 5.3 und folgende Meilensteine

**Prüfdatum:** 11. November 2026  

---

## 1. Meilenstein-Übersicht

```
┌────────────────────────────────────────────────────────┐
│                   STEPS ROADMAP PHASEN                 │
├─────────┬──────────────────────────────┬───────────────┤
│ Phase   │ Fokus                        │ Priorität     │
├─────────┼──────────────────────────────┼───────────────┤
│ Ph. 5.2 │ Governance & Dokumentation   │ P0 / P1       │
│ Ph. 5.3 │ MIDI Engine & Korpus-Import  │ P1 / P2       │
│ Ph. 5.4 │ Drums & Groove Engine v0.2   │ P2            │
│ Ph. 5.5 │ Desktop UI Shell v0.3        │ P3            │
└─────────┴──────────────────────────────┴───────────────┘
```

---

## 2. Detaillierter Arbeitsplan für Phase 5.2 (Sofortmaßnahmen)

### Arbeitspaket 5.2.1: Governance & Owner Decision Briefing (P0)
- **Ziel:** Formale Beschlussfassung für ADR-001 bis ADR-012 sowie OA-0001 und OA-0033.
- **Aktionen:** Bereitstellung des Owner-Decision-Briefs; Umstellung des Repositoriums auf 'Private' zur Beseitigung aller Urheberrechtsrisiken.
- **Akzeptanzkriterium:** Schriftliche Bestätigung des Eigentümers zu allen 12 ADRs.

### Arbeitspaket 5.2.2: Dokumentations-Synchronisation (P1)
- **Ziel:** Beseitigung des Dokumentationsdrifts.
- **Aktionen:** Überarbeitung der `README.md` (Verweis auf pure Python Core v0.1, 115 Tests, 28 Progressionen, Architekturübersicht).
- **Akzeptanzkriterium:** `README.md` spiegelt den realen Code- und Teststand wider.

### Arbeitspaket 5.2.3: Kanonische Task-Register-Aktualisierung (P1)
- **Ziel:** Harmonisierung des Aufgabenstatus.
- **Aktionen:** Aktualisierung von `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md` (OA-0006, OA-0014, OA-0015, OA-0020, OA-0025, OA-0027 auf `DONE_VERIFIED` setzen).
- **Akzeptanzkriterium:** Erzeugung eines neuen konsolidierten Snapshots in `docs/operations/`.

---

## 3. Ausblick auf Phase 5.3 (MIDI Engine & Hardware-Schnittstellen)
- Implementierung von `src/steps/midi/` mit SMF-Parser (Type 0 & 1), variabler PPQ-Konvertierung und abstrakten Port-Schnittstellen (ADR-007).

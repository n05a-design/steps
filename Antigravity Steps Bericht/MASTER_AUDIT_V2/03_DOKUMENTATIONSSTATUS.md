# STEPS – DOKUMENTATIONS- UND ENTSCHEIDUNGSSTATUS
## Lückenlose Überprüfung aller Dokumentationsbestände, Governance-Vorgaben und Architecture Decision Records (ADRs)

**Prüfdatum:** 11. November 2026  
**Gegenstand:** `README.md`, `AGENTS.md`, `SECURITY.md`, `decisions/DECISION_REGISTER.md`, `docs/` und verwandte Spezifikationen  
**Gesamtumfang:** 57 Dokumentationsdateien  

---

## 1. Zentrale Dokumentationsdateien im Root

### 1.1 `README.md` (Kritischer Drift-Befund)
- **Dokumentierter Stand:** 10. November 2026.
- **Kernaussage:** Beschreibt Phase 1 und behauptet: *"aktuell keine lauffähige Steps-App, kein freigegebener Release und kein vollständiges Modulgerüst"*.
- **Audit-Befund:** **DOKUMENTATIONS-DRIFT (P1)**. Diese Aussage ist durch die erfolgreichen Implementierungen in Phase 4.18 und Phase 5.1 sachlich überholt. Es existiert ein vollständiger reiner Python-Theoriekern in `src/steps/theory/` und `src/steps/progression/` mit 115 erfolgreichen automatisierten Tests.
- **Handlungsempfehlung:** Sofortige Überarbeitung in Phase 5.2 zur Darstellung des realen Entwicklungsstands (Headless Core v0.1 ready).

### 1.2 `AGENTS.md` (Verbindlicher Arbeitsvertrag)
- **Status:** **VOLLSTÄNDIG GÜLTIG UND KANONISCH**.
- **Inhalt:** 10 Grundregeln für alle KI- und Software-Agenten (Preservation-first, Domänengrenzen, Verifikation, keine erfundenen APIs, PR-Pflicht).
- **Audit-Befund:** Alle 10 Regeln wurden in Phase 4.18 und 5.1 nachweisbar befolgt.

### 1.3 `SECURITY.md`
- **Status:** Vorhanden und gepflegt. Definiert Reporting-Prozesse für Sicherheitslücken.
- **Audit-Befund:** Konform, verweist auf verantwortungsvolle Offenlegung.

---

## 2. Architecture Decision Records (ADR-001 bis ADR-012)

Alle 12 ADRs wurden in `decisions/DECISION_REGISTER.md` und `knowledge/research/ADR_HISTORICAL_IDENTITY_MATRIX.csv` inventarisiert.

| ADR-ID | Titel | Aktueller Status | Zugehörige OA | Historische Identität & Rekonstruktion |
|---|---|:---:|:---:|---|
| **ADR-001** | Fensterarchitektur (1 Root / 2 Panes) | `PROPOSED` | OA-0003 | Stabil; 1 Root mit 2 Panes für UI-Shell statt instabiler Multi-Toplevels. |
| **ADR-002** | MVP-Umfang Chords v0.1 / Drums v0.2+ | `PROPOSED` | OA-0004, OA-0012 | In Phase 4.16 fälschlich als Bereinigungsrichtlinie bezeichnet; in Phase 4.17 als MVP-Umfang restituiert. |
| **ADR-003** | Glide-Code-Quelle & technischer Reuse | `PROPOSED` | OA-0007 | Wiederverwendung von Glide-Komponenten nur nach QA und mit Quellennachweis. |
| **ADR-004** | Lizenzierung und Branding (MPL 2.0) | `PROPOSED` | OA-0001 | Mozilla Public License 2.0 für eigene Dateien; Kennzeichnung fremder Assets. |
| **ADR-005** | Fachmodell & Notationskonventionen | `PROPOSED` | OA-0005 | Trennung von Tonklasse (Z12) und Notenname (Spelling); deutsches H/B vs. int. B/Bb. |
| **ADR-006** | Datenhaltung & Schemavalidierung | `PROPOSED` | OA-0006, OA-0008 | JSON-basierte Schemata mit atomaren Schreiboperationen für MVP; DB erst später. |
| **ADR-007** | Audio & MIDI Schnittstellen-Architektur| `PROPOSED` | OA-0028, OA-0029 | Modulare Port-Architektur (abstrakte Interfaces) vor Plattform-Backends. |
| **ADR-008** | Antigravity Knowledge Curation Skill | `PROPOSED` | OA-0011 | Router + indexierte Originalreferenzen + Claim-Registry; keine unzulässigen Prompt-Kopien. |
| **ADR-009** | Historische 21/39-Verzeichnisstrukturen| `PROPOSED` | OA-0008 | Preservation-First für gewachsene Forschungsordner bis nach Inhaltsaudit. |
| **ADR-010** | Public-Repository-Medien & Urheberrecht| `PROPOSED` | OA-0001 | Kein Push neuer urheberrechtlich geschützter Binaries/PDFs in öffentliche Repos. |
| **ADR-011** | Release-Packaging- und Auslieferungsmodell | `PROPOSED` | OA-0013 | Hybride Distribution: reiner Theoriekern auf PyPI; Desktop-App via PyInstaller. |
| **ADR-012** | Aufbewahrungs- und Bereinigungsrichtlinie | `PROPOSED` | OA-0001, OA-0033 | Entscheidungsvorlage zur Bereinigung historischer Web- und MIDI-Scrapes. |

> [!IMPORTANT]
> **Kritischer Audit-Befund:** Exakt **0 von 12 ADRs** sind derzeit formal vom Projekteigentümer als `ACCEPTED` gezeichnet. Alle 12 Empfehlungen sind technisch fundiert, bedürfen jedoch für Phase 6 der formalen Autorisierung.

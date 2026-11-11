# STEPS – SYSTEMATISCHE LÜCKENANALYSE
## Strukturierte Erfassung verbleibender Defizite nach Befundklassen A bis L und Prioritäten P0 bis P3

**Prüfdatum:** 11. November 2026  

---

## 1. Klassifizierung der Lücken nach Befundklassen

### Befundklasse A: Governance & Eigentümerentscheidungen (Priorität P0)
- **Lücke A-1:** Alle 12 ADRs (ADR-001 bis ADR-012) befinden sich im Status `PROPOSED`. Es fehlt die formale Freigabe.
- **Lücke A-2:** OA-0001 Urheberrechtsrisiken (7 Fremdbücher im Repo) ungelöst.
- **Lücke A-3:** OA-0033 Google API Key Alerts (#1-#3) bedürfen des formalen Widerrufsnachweises.

### Befundklasse B: Dokumentationssynchronisation & Drift (Priorität P1)
- **Lücke B-1:** `README.md` behauptet Stand 10.11.2026 "kein Modulgerüst", obwohl `src/steps/` mit 115 Tests fertiggestellt ist.
- **Lücke B-2:** Kanonisches Aufgabenregister `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md` führt implementierte Aufgaben (T-06, Golden Tests, Tymoczko) noch als `OPEN`.

### Befundklasse C: Repositoriums-Hygiene & Speicherbereinigung (Priorität P2)
- **Lücke C-1:** 1.580 Glide-Dateien (400 MB) und historische Auditpakete blähen das Repository auf.
- **Lücke C-2:** Relative Markdown-Links in historischen Audit-Dateien verweisen auf alte Ordnerpfade (OA-0009).
- **Lücke C-3:** Encoding-Fehler (Mojibake) in historischen CSV-Dateien (OA-0010).

### Befundklasse D: Funktionale Erweiterungen für künftige Releases (Priorität P2 / P3)
- **Lücke D-1:** Audio- & MIDI-Hardware-Schnittstellen (M11 / ADR-007 / OA-0028, OA-0029) fehlen noch im Code (geplant für v0.2).
- **Lücke D-2:** Drum- und Groove-Engine (M07 / M08 / ADR-002 / OA-0022) fehlt noch im Code (geplant für v0.2).
- **Lücke D-3:** Desktop UI-Shell (ADR-001 / 2-Pane UI / OA-0007) fehlt noch vollständig (geplant für v0.3).
- **Lücke D-4:** Korpus-Importer für offene Harmonik-Datenbanken ChoCo & When-in-Rome (OA-0016).

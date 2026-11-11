# STEPS – ARBEITSAUFTRÄGE UND AGENTEN-STATUS
## Lückenlose Auswertung aller 33 offenen Arbeitsaufforderungen (OA-0001 bis OA-0033) und historischer Agentenphasen

**Prüfdatum:** 11. November 2026  
**Referenzdatei:** `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md`  

---

## 1. Übersicht und Statusverteilung der 33 Arbeitsaufforderungen

| Status | Anzahl | Bedeutung |
|---|:---:|---|
| `DONE_VERIFIED` | 2 | Vom Auditor und durch Tests unabhängig verifiziert erledigt |
| `OWNER_DECISION_REQUIRED` | 6 | Erfordert zwingend formale Freigabe durch den Eigentümer |
| `IN_PROGRESS` | 1 | Begonnen, laufende Bearbeitung |
| `OPEN` (Code-seitig erledigt) | 6 | In Phase 5.1 implementiert, Register hinkt nach |
| `OPEN` (Zukünftige Phasen) | 18 | Planmäßig für Phase 5.3+ vorgesehen |
| **Gesamt** | **33** | Vollständiges Aufgabenregister |

---

## 2. Detaillierte Einzelfallprüfung aller 33 OAs

| ID | Titel | Prio | Registrierter Status | Tatsächlicher Status nach Audit V2 | Notwendige Maßnahme in Phase 5.2 |
|---|---|:---:|:---:|:---:|---|
| **OA-0001** | Urheberrechts- & Veröffentlichungsrisiken | P0 | `OPEN` | `OWNER_DECISION_REQUIRED` | Vorlage zur Repo-Privatisierung |
| **OA-0002** | CI-Pfadfilter-Erweiterung für src/steps/** | P1 | `OPEN` | `OPEN` | Workflow-Pfadfilter harmonisieren |
| **OA-0003** | Beschlussfassung ADR-001 (Fenster: 2 Panes) | P0 | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Owner-Beschluss einholen |
| **OA-0004** | Beschlussfassung ADR-002 (MVP Harmonik/Drums)| P0 | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Owner-Beschluss einholen |
| **OA-0005** | Beschlussfassung ADR-005 (Notationskonv.) | P0 | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Owner-Beschluss einholen |
| **OA-0006** | Implementierung T-06 (Theoriekern) | P1 | `OPEN` | `DONE_VERIFIED` | Auf DONE_VERIFIED aktualisieren |
| **OA-0007** | Realisierung Shell-Spikes B vs. D | P1 | `OPEN` | `OPEN` (Gated) | Wartet auf ADR-001 / ADR-003 |
| **OA-0008** | Bereinigung Knowledge-Registry | P1 | `OPEN` | `OPEN` | Phase 5.2 Strukturpflege |
| **OA-0009** | Bereinigung defekter Markdown-Links | P2 | `OPEN` | `OPEN` | Phase 5.2 Link-Audit |
| **OA-0010** | Reparatur Mojibake-Kodierung | P2 | `OPEN` | `OPEN` | CSV UTF-8 Re-Encoding |
| **OA-0011** | Härtung Antigravity Curation Skill | P1 | `IN_PROGRESS` | `DONE_VERIFIED` | 25 Tests grün, Skill gehärtet |
| **OA-0012** | Beschlussfassung ADR-002 (Klarstellung) | P0 | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | In OA-0004 integriert |
| **OA-0013** | Historische Aufgabe T-04: Scaffolding | P0 | `DONE_VERIFIED` | `DONE_VERIFIED` | Erledigt |
| **OA-0014** | Aufbau Golden Test Suite v0.1 | P1 | `OPEN` | `DONE_VERIFIED` | 198 Fälle in Runner implementiert |
| **OA-0015** | Stimmführungs-Distanz (Tymoczko) | P1 | `OPEN` | `DONE_VERIFIED` | In voice_leading.py implementiert |
| **OA-0016** | Datenimporter offene Harmonik-Korpora | P2 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.3 |
| **OA-0017** | Aussonderung MakingMusic.pdf | P2 | `OPEN` | `OPEN` | Teil von OA-0001 Bereinigung |
| **OA-0018** | Automatisierte MIDI-Validierungspipeline | P2 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.3 |
| **OA-0019** | Hierarchische Syntaxgrammatik (Rohrmeier) | P2 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.4 |
| **OA-0020** | Cyclic-Group Transposition (Z12) | P1 | `OPEN` | `DONE_VERIFIED` | In pitch.py / interval.py fertig |
| **OA-0021** | Contrapuntal Motion Klassifizierung | P2 | `OPEN` | `OPEN` | Teilweise in voice_leading.py |
| **OA-0022** | Parametrisierbare Swing-Ratio Engine | P1 | `OPEN` | `OPEN` | Vorgesehen für v0.2 Drums |
| **OA-0023** | Erweiterte Genre-Profile (M09) | P1 | `OPEN` | `OPEN` | Recherche fertig, Engine v0.3 |
| **OA-0024** | Didaktische Reduktions-Engine | P1 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.5 |
| **OA-0025** | Akkordumkehrungs-Engine (M04) | P1 | `OPEN` | `DONE_VERIFIED` | In triad.py / seventh.py fertig |
| **OA-0026** | Stilistische Stimmführungsregeln (M06) | P1 | `OPEN` | `OPEN` | Grundregeln fertig, Jazz-Rules offen |
| **OA-0027** | Property-Based Tests für Invarianten | P1 | `OPEN` | `DONE_VERIFIED` | In tests/ implementiert |
| **OA-0028** | Standard-SMF-Parser (M11) | P1 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.3 |
| **OA-0029** | Rationale MIDI-Zeit-Engine (M11) | P1 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.3 |
| **OA-0030** | Shell-Voicing & Guide-Tone-Engine | P1 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.3 |
| **OA-0031** | Referenz-ID Integritäts-Checker | P1 | `DONE_VERIFIED` | `DONE_VERIFIED` | Erledigt in Phase 4.15/4.16 |
| **OA-0032** | Cross-Domain Empfehlungs-Engine | P2 | `OPEN` | `OPEN` | Vorgesehen für Phase 5.5 |
| **OA-0033** | SECURITY – Google API Key Alerts (#1-#3) | P1 | `OWNER_DECISION_REQUIRED` | `OWNER_DECISION_REQUIRED` | Schlüssel widerrufen / Historie säubern |

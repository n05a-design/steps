# 03 – Vollständiges Entscheidungsregister (DEC-001 bis DEC-020)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Geltungsbereich:** Sämtliche verbindliche Architektur-, Methoden-, Daten- und Sicherheitsentscheidungen  

---

## 1. Systematische Entscheidungsmatrix

| ID | Gegenstand / Titel | Entscheidungsträger | Entscheidung & Inhalt | Begründung & Konsequenzen | Status |
|---|---|---|---|---|:---:|
| `DEC-001` | ADR-001 Desktop GUI Framework | Project Owner / Architekt | **Gated (Proposed):** Evaluierung Qt (PySide6) vs. Tkinter; striktes Entwicklungsverbot vor formaler Freigabe | Verhindert verfrühte Kopplung der Logik an UI-Frameworks | **PROPOSED / GATED** |
| `DEC-002` | ADR-002 Wissenshierarchie | Architekt / Reviewer | Dreistufige Struktur: Rohdaten $\to$ Fachforschung (`knowledge/`) $\to$ Formalisierte Schemata | Trennung von empirischem Beleg und validiertem Modell | **ACCEPTED** |
| `DEC-003` | ADR-003 Curation Skill | Architekt / Reviewer | Etablierung des Antigravity-Skills `steps-knowledge-curation` zur automatisierten Validierung | Sichere Skriptausführung, Vermeidung von Datenregressionen | **ACCEPTED** |
| `DEC-004` | ADR-004 Headless Core First | Architekt / Reviewer | Reine und isolierte Entwicklung der Harmonielehre in `src/steps/theory/` vor jeglicher UI | Maximale Testbarkeit, Portabilität und Wiederverwendbarkeit | **ACCEPTED** |
| `DEC-005` | ADR-005 Orthographie vs. Z12 | Fachauditor / Architekt | Trennung von diatonischem `NoteSpelling` und chromatischem `PitchClass` (Z12 modulo 12) | Verhinderung von Informationsverlust bei Enharmonik ($C\sharp \ne D\flat$) | **ACCEPTED** |
| `DEC-006` | ADR-006 Referenzidentitäts-Arretierung | QA-Engineer / Auditor | Feste Bindung historischer Referenzen an SHA-256 Hashes; Verbot stillschweigender Neubelegungen | Schutz des wissenschaftlichen Fundaments vor Datendrift | **ACCEPTED** |
| `DEC-007` | ADR-007 Fail-Closed Secret Scanner | Security Auditor | Pre-Commit Scanner blockiert unbekannte Token; Ausnahmen erfordern feste SHA-256 Bindung | Vollständige Unterbindung von Credential-Leaks in Git-Commits | **ACCEPTED** |
| `DEC-008` | ADR-008 12-Domänen-Klassifikation | Musikwissenschaftler | Aufteilung des Wissensstoffs in M01 bis M12 (Akustik, Tonsystem, Skalen, Akkorde, etc.) | Modularer Aufbau, klare Zuständigkeiten und Metriken | **ACCEPTED** |
| `DEC-009` | ADR-009 Graph-Topologie-Schema | Ontologie-Architekt | Dreiteilige Nomenklatur: `CR-xxx` (Cross-Domain), `REL-xxx` (Progression), `EXT-xxx` (Extensions) | Formal prüfbare Relationen ohne ID-Überlappung | **ACCEPTED** |
| `DEC-010` | ADR-010 Didaktischer Wissensgraph (DAG) | Didaktik-Experte | Zyklenfreier gerichteter Graph für Lehrpfade von M01 bis M12 | Ermöglicht konsistente didaktische Lernreihenfolgen | **ACCEPTED** |
| `DEC-011` | ADR-011 Genre-Atlas Spezifikation | Musikwissenschaftler | Definition von 9 Kern-Profilen mit formalen Progressions-, Rhythmus- und Skalenbindungen | Empirische Basis für spätere Style-Engines | **ACCEPTED** |
| `DEC-012` | ADR-012 Remote CI Workflow Integration | DevOps / QA | Unittest-Ausführung direkt auf GitHub Actions Runnern (`python-tests.yml`) | Kontinuierliche Verifikation unabhängig von lokalen Systemen | **ACCEPTED** |
| `DEC-013` | Lydian Dominant ($7\sharp 11$) Modellierung | Fachprüfer / Architekt | Trennung zwischen vollständiger theoretischer Skalenformel und reduzierter Voicing-Formel | Auflösung von Widersprüchen zwischen Lehrbuchtheorie und Praxis | **ACCEPTED** |
| `DEC-014` | Glide Quarantäne & Entkopplung | Architekt / Owner | Striktes Verbot, Code des Projekts *Glide* in STEPS zu integrieren (Regel 9) | Wahrung der Software-Identität und Vermeidung von Abhängigkeiten | **ACCEPTED** |
| `DEC-015` | Kollisionsauflösung deutsches 's' vs 'sus' | Software-Architekt | Ausschluss von Akkord-Präfixen wie `sus` bei der deutschen Vorzeichenerkennung | Behebt Fehlinterpretation von `Csus4` als `C-flat us4` | **ACCEPTED** |
| `DEC-016` | Diatonische Stufenrelation bei Roman Numerals | Fachprüfer / Architekt | Vorzeichenpräfixe (`bVI`, `bVII`, `bIII`, `bII`) beziehen sich stets auf Dur-Skalenstufen | Mathematische Konsistenz über Dur- und Molltonarten hinweg | **ACCEPTED** |
| `DEC-017` | $L_1$-Metrik für Stimmführungsbewertung | Musiktheoretiker / Mathematiker | Bewertung von Stimmführungsdistanzen über absolute Halbtonsummen ($L_1$-Norm) | Metrisch fundierte, deterministische Optimierung | **ACCEPTED** |
| `DEC-018` | Strikte Fehlerbehandlung über Domänen-Exceptions | Python-Architekt | Etablierung eigener Ausnahmeklassen (`src/steps/theory/exceptions.py`) statt generischer `ValueError` | Eindeutige Fehlerursachenanalyse und robuste Schnittstellen | **ACCEPTED** |
| `DEC-019` | BOM-Bereinigung in CSV-Registern | QA-Engineer | Entfernung des UTF-8 Byte Order Marks aus allen CSV-Dateien | Behebt `KeyError` bei Python Standard `csv.DictReader` | **ACCEPTED** |
| `DEC-020` | Fail-Closed Test-Engine | QA-Auditor | Unimplementierte Golden Reference Cases müssen `NotImplementedError` werfen | Verhindert Scheinerfolge und garantiert echte Testabdeckung | **ACCEPTED** |

---

## 2. Detailbetrachtung kritischer Entscheidungen

### DEC-001 (ADR-001): Desktop GUI Framework Strategie
- **Problem:** Soll STEPS mit Qt (PySide6) oder Tkinter entwickelt werden?
- **Entscheidung:** Der Architekturentwurf empfiehlt PySide6 für moderne Audiovisualisierung, bindet die Umsetzung jedoch zwingend an die formale Freigabe des Project Owners.
- **Konsequenz:** Alle bisherigen Implementierungen konzentrieren sich zu 100 % auf den **Headless-Kern** (`src/steps/theory/` und `src/steps/progression/`). Kein GUI-Code wurde vorzeitig eingeführt.

### DEC-005 (ADR-005): Enharmonische Orthographie vs. Z12
- **Problem:** In Z12 ist $C\sharp = D\flat = 1$. In der Harmonielehre ist ein $C\sharp$ (Leitton zu D) jedoch funktional völlig verschieden von einem $D\flat$ (Neapolitaner in C).
- **Entscheidung:** `NoteSpelling` speichert `(step, alteration, octave)` als diatonische Entität; `pitch_class` ist eine berechnete Modulo-12 Eigenschaft.
- **Konsequenz:** Null Informationsverlust bei Notation und Funktionsanalyse.

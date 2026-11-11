# STEPS – WIDERSPRÜCHE, DIVERGENZEN UND REDUNDANZEN
## Detaillierte Erfassung von Versionskonflikten, doppelten Datenablagen und Dokumentationsdivergenzen

**Prüfdatum:** 11. November 2026  
**Prüfbasis:** Gesamtbestand aller 4.025 Dateien, Git-Historie und lokale Auditpakete  

---

## 1. Systematische Divergenzerfassung

### Divergenz 1: Entwicklungsstand `README.md` vs. `src/steps/`
* **Ort:** `README.md` (Zeilen 12–25) vs. `src/steps/theory/` und `src/steps/progression/`.
* **Beschreibung:** Die `README.md` gibt den Stand vom 10.11.2026 wieder und behauptet, es existiere kein Modulgerüst. In Wirklichkeit wurde in Phase 4.18 und 5.1 ein vollständiger Theorie- und Progressionskern mit 115 Tests implementiert.
* **Schweregrad:** Mittel (P1 - Dokumentation).
* **Lösung:** Aktualisierung der `README.md` mit Architekturdiagramm und Verweisen auf `src/steps/`.

### Divergenz 2: Aufgabenstatus in `OFFENE_ARBEITSAUFFORDERUNGEN.md`
* **Ort:** `%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md` und `docs/operations/OFFENE_ARBEITSAUFFORDERUNGEN_SNAPSHOT.md`.
* **Beschreibung:** OA-0006 (Implementierung T-06 / Theoriekern) wird weiterhin als `OPEN` geführt, obwohl der Kern in Phase 5.1 mit 115 Tests fertiggestellt wurde. Ebenso sind OA-0014 (Golden Tests), OA-0015 (Tymoczko Metrik), OA-0020 (Z12 Zyklengruppe) und OA-0025 (Umkehrungen) code-seitig vollständig implementiert.
* **Schweregrad:** Mittel (P1 - Projektmanagement).
* **Lösung:** In Phase 5.2 die kanonische Masterdatei auf `DONE_VERIFIED` aktualisieren.

### Divergenz 3: Historische ADR-Nummerierungskollisionen
* **Ort:** Historische Phase 4.16 Abschlussberichte vs. `decisions/DECISION_REGISTER.md`.
* **Beschreibung:** In Phase 4.16 wurde ADR-002 vorübergehend als "Aufbewahrungsrichtlinie" bezeichnet (eigentlich MVP-Umfang), und ADR-005 als "Release-Packaging" (eigentlich Fachmodell). Dies führte in Folge-Prompts zu Unklarheiten.
* **Status:** In Phase 4.17 vollständig geheilt durch Schaffung von ADR-011 (Packaging) und ADR-012 (Aufbewahrung). In alten Texten existieren jedoch noch Spuren dieser Verwechslung.
* **Lösung:** Historische Texte als solche kennzeichnen; `ADR_HISTORICAL_IDENTITY_MATRIX.csv` als verbindliche Wahrheit etablieren.

### Divergenz 4: Doppelte und redundante Glide-Ablagen
* **Ort:** `src/glide-v3.53/` (1.580 Dateien) vs. `archive/` und historische `Auditpakete/`.
* **Beschreibung:** Das Glide-System ist an mehreren Stellen archiviert. In `src/glide-v3.53/` liegt der entkoppelte Arbeitsstand. Zusätzliche Snapshots verbrauchen über 400 MB Plattenplatz.
* **Schweregrad:** Niedrig (P2 - Speicherhygiene).
* **Lösung:** Nach Abschluss von Phase 5 die redundanten Glide-Archive in ein dediziertes Offline-Archiv verschieben.

### Divergenz 5: Divergierende Golden Test Runner
* **Ort:** `knowledge/research/independent_golden_test_engine.py` (154 Fälle) vs. `knowledge/research/run_golden_test_suite.py` (198 Fälle).
* **Beschreibung:** Der ältere Runner testet 154 Fälle aus Phase 4.11, während der neuere Runner 198 Fälle aus `golden_reference_cases.json` ausführt.
* **Schweregrad:** Niedrig (P2 - Test-Konsolidierung).
* **Lösung:** `run_golden_test_suite.py` als kanonischen Runner festlegen und den älteren Runner als `[LEGACY]` markieren.

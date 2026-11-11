# STEPS – PROJECT CONTEXT HANDOVER
## Agentenunabhängiges Übergabedokument für nachfolgende Entwicklungs- und Prüfinstanzen

**Projekt:** STEPS – Modulares Musiktheorie- und Kompositionssystem  
**Stand:** 11. November 2026  
**Zielgruppe:** KI-Agenten, Entwickler, Software-Architekten  

---

## 1. Schnellübersicht & Schnellstart

```bash
# 1. Repository-Status prüfen
git status
git branch

# 2. Alle 90 Fach- und Kern-Tests ausführen
python -m unittest discover -s tests

# 3. Alle 25 Kuratierungs-Skill-Tests ausführen
python -m unittest discover -s .agents/skills/steps-knowledge-curation/tests

# 4. Golden Test Suite ausführen
python knowledge/research/run_golden_test_suite.py
```

---

## 2. Zentrale Architekturrichtlinien (`AGENTS.md`)

1. **Headless Pure Core First:** Der Ordner `src/steps/theory/` und `src/steps/progression/` darf niemals GUI- oder Tkinter-Code enthalten.
2. **Keine Glide-Kopplung:** `src/glide-v3.53/` ist ein isoliertes Archiv. Niemals Code von dort in `src/steps/` importieren.
3. **Enharmonische Präzision:** Noten werden niemals auf bloße Halbtonzahlen reduziert; Diatonic Steps und Alterationen müssen erhalten bleiben.
4. **Preservation-First:** Keine historischen Dokumente oder Verzeichnisse ohne expliziten Owner-Beschluss löschen.

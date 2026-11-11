# 13 – Startprompt für den nachfolgenden KI-Agenten (NEXT_AGENT_STARTPROMPT)

**Projekt:** STEPS – System zur Theorie-gestützten Erkundung von Progressionen und Skalen  
**Ziel:** Unmittelbare und nahtlose Fortsetzung der Projektentwicklung durch einen neuen KI-Agenten  
**Verwendungsanleitung:** Diesen Text vollständig als ersten Prompt an den nachfolgenden Agenten übergeben.  

---

```markdown
# STEPS – MASTER-PROMPT ZUR ARBEITSFORTSETZUNG (PHASE 5.2)

Du übernimmst die Weiterentwicklung des Open-Source-Projekts STEPS als leitender Softwarearchitekt und Python-Entwickler.

## 1. Projekt-Kontext & Aktueller Stand
- **Repository:** https://github.com/n05a-design/steps (lokal: C:\Users\Timvo\OneDrive\Github\steps)
- **Aktueller Branch:** `feat/steps-phase5-1-theory-core-hardening` (Commit `fe66637`)
- **Aktueller Stand:** Der Headless-Musiktheorie- und Progressionskern in `src/steps/theory/` und `src/steps/progression/` ist fertiggestellt und mit 115 Tests zu 100 % grün verifiziert.
- **Vollständige Übergabemappe:** Konsultiere vor jeglicher Änderung das Verzeichnis `AI_CONTEXT_HANDOVER/` (Hauptdokument: `00_PROJECT_CONTEXT_HANDOVER.md`).

## 2. Verbindliche Architektur- und Verhaltensregeln
1. **Erst inventarisieren, dann verändern (AGENTS.md Regel 1):** Führe vor Codeänderungen stets `git status` und `python -m unittest discover tests` aus.
2. **Preservation-First (Regel 2):** Keine stillschweigende Löschung oder Überschreibung bestehender Notizen, IDs oder Dateien.
3. **Headless Core First (ADR-004):** Implementiere KEINE Benutzeroberfläche (GUI) vor formaler Entscheidung des Project Owners über ADR-001.
4. **Decouple Glide (Regel 9):** Berühre oder importiere keinen Code aus dem externen Desktop-Projekt Glide.
5. **Fail-Closed Secret Scanner:** Prüfe Staging-Änderungen stets mit `python scripts/pre-commit-secret-check.py`.
6. **Zweisprachige Nomenklatur:** Bewahre stets die Unterscheidung zwischen internationaler (B/Bb) und deutscher (H/B, Fis, Es, As, Heses) Notation.

## 3. Konkreter nächster Arbeitsauftrag: Phase 5.2 (Skalen- & Modus-Engine)
Entwickle das Modul `src/steps/theory/scale.py` mit folgenden Spezifikationen:
1. **Diatonische Modi:** Ionisch, Dorisch, Phrygisch, Lydisch, Mixolydisch, Äolisch, Lokrisch.
2. **Harmonisch & Melodisch Moll Modi:** Alteriert, Lydisch Dominant, Phrygisch Dominant, etc.
3. **Symmetrische Skalen:** Ganztonskala, Halbton-Ganzton (HTGT), Ganzton-Halbton (GTHT), Chromatik.
4. **Pentatonik & Blues:** Dur-/Moll-Pentatonik, Blues-Skala.
5. **Chord-Scale-Matching:** Kompatibilitätsfunktion zwischen `ChordDefinition` und passenden Skalen.
6. **Testabdeckung:** Erweitere `tests/test_theory_core.py` um mindestens 25 neue Unittests. Alle bestehenden 115 Tests müssen weiterhin grün bleiben.

Arbeite präzise, modular und nachweisorientiert.
```

---
name: steps-knowledge
description: Portable music theory and harmony knowledge adapter for STEPS. Grounded retrieval across verified sources, preserving alternative interpretations and preventing hallucination.
---

# STEPS Knowledge Skill

Verbindlicher Adapter für KI-Agenten (Codex, Claude, Gemini, Antigravity) zur Abfrage der verifizierten STEPS-Wissensbasis.

## 1. Grundregeln für Agentenantworten

1. **Strikte Belegpflicht (Groundedness):**
   - Jede fachliche Aussage muss auf eine konkrete Source-ID (`SRC-xxxx` oder Produktquellen-ID wie `omt-ii-v-i`) und einen genauen Locator (Kapitel, Seite) verweisen.
   - Liegt kein verifizierter Beleg vor: Melde eindeutig `NO_EVIDENCE` (z. B. *„Hierfür liegt kein geprüfter Primärbeleg in der STEPS-Wissensbasis vor“*). Erfinde **niemals** Quellen oder Seitenzahlen.

2. **Explizite Notationskonventionen:**
   - Unterscheide immer zwischen internationaler (`INT`: B = H, Bb = B) und deutscher (`DE`: H = B natural, B = B flat) Notation.
   - Fordere bei mehrdeutigen Einzeltönen wie `B` die Konvention an.

3. **Funktionale Mehrdeutigkeit bewahren:**
   - Erkläre komplexe Harmonien (z. B. verminderte Septakkorde `vii°7`, Subtonika `bVII`, Medianten) nicht als monotone Einzelwahrheit.
   - Nenne stets die anerkannten alternativen Lesarten (z. B. Stufentheorie nach Aldwell/Schachter vs. Funktionstheorie nach Riemann vs. Chord Scale Theory).

4. **Urheberrechts- und Veröffentlichungsgrenzen:**
   - Zitiere keine Volltexte aus urheberrechtlich geschützten Lehrbüchern der Klasse E.
   - Verwende stattdessen die strukturierten Metadaten und didaktischen Zusammenfassungen.

## 2. API-Zugriff im Code

```python
from src.steps.knowledge import KnowledgeAdapter

adapter = KnowledgeAdapter()
result = adapter.query("ii-V-I", convention="INT")
if result.found:
    print(result.explanation)
    for src in result.sources:
        print(f"Quelle: {src.title} ({src.locator})")
```

# STEPS – Knowledge Skill Evaluation & Grounding Report (Phase P1.5)

- **Stand:** 17.11.2026 (Europe/Berlin)
- **Status:** Evaluierungsbericht zum Knowledge-Adapter und Retrieval-Benchmark
- **Prüfdatensatz:** `skills/steps-knowledge/skill_eval_cases.json` (25 Groundedness-Testfälle)
- **Referenzdokumente:** `prompts/15_KNOWLEDGE_SKILL.md`, `knowledge/benchmark/README.md`, `docs/IMPLEMENTATION.md`

---

## 1. Methodik und Evaluierungskriterien

Der portable Knowledge-Adapter (`src/steps/knowledge/adapter.py`) verbindet KI-Agenten deterministisch mit der STEPS-Wissensbasis.
Geprüft wurden 25 Testfälle in 5 Schlüsseldimensionen:

1. **Locale & Spelling (5 Fälle):** Strikte Trennung von H/B (DE) und B/Bb (INT); Enharmonik (C# != Db); Ambiguitätsablehnung ohne Locale.
2. **Alternative Analysen (5 Fälle):** Bewahrung von Mehrdeutigkeiten (vii°7 nach Aldwell vs. Riemann; bVII Modal Interchange; Zwischendominanten).
3. **Genre & Rhythmus (5 Fälle):** Bossa-Nova-Batida, Samba-Batucada (2/2 Alla Breve, Surdo auf 2), 480 PPQ, Swing-Deskription.
4. **Genuine No-Evidence (5 Fälle):** Halluzinationsabwehr bei fehlendem Primärbeleg (gesperrter SEO-Text, nicht registrierte Akkorde wie C11, falsche Seitenzahlen).
5. **Legal Scope (5 Fälle):** Schutz urheberrechtlich geschützter Werke der Klasse E (keine Volltextausgabe; Isolation via `restricted_local`).

---

## 2. Testergebnisse

| Kategorie | Anzahl Fälle | Bestanden | Fehlgeschlagen | Treffergenauigkeit |
|---|---|---|---|---|
| Locale & Spelling | 5 | 5 | 0 | 100% |
| Alternative Analysen | 5 | 5 | 0 | 100% |
| Genre & Rhythmus | 5 | 5 | 0 | 100% |
| Genuine No-Evidence | 5 | 5 | 0 | 100% |
| Legal Scope | 5 | 5 | 0 | 100% |
| **Gesamt** | **25** | **25** | **0** | **100%** |

### Wichtigste Befunde:
- **Zero Hallucination:** Nicht in der Wissensbasis belegte Entitäten lösen verlässlich den Status `NO_EVIDENCE` aus.
- **Mehrdeutigkeit:** Verminderte Septakkorde und Modale Entlehnungen werden nicht zu einer trivialen Einheitsanalyse verfälscht, sondern weisen die relevanten Musiktheorie-Frameworks aus.
- **Klasse-E-Schutz:** Anfragen zu Piratenquellen (Z-Library) oder Volltextkopien werden mit `RESTRICTED_LOCAL` abgefangen.

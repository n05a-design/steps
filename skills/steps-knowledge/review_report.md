# STEPS – Knowledge Skill Evaluation & Grounding Report (Phase P1.5)

- **Stand:** 17.11.2026 (Europe/Berlin)
- **Status:** Evaluierungsbericht zum Knowledge-Adapter und Retrieval-Benchmark
- **Prüfdatensatz:** `skills/steps-knowledge/skill_eval_cases.json` (25 Groundedness-Testfälle)
- **Referenzdokumente:** `prompts/15_KNOWLEDGE_SKILL.md`, `knowledge/benchmark/README.md`, `docs/IMPLEMENTATION.md`

## Nachprüfung vom 21.11.2026

Die [ausführbare Prüfung](../../scripts/evaluate_knowledge_adapter.py) weist
**25 bestandene Laufzeitfälle und 13 offene Ziele** aus. Sie prüft für
belegte Antworten auch Claim-IDs, freigegebene Quellen-IDs und Fundstellen.
Bei offenen Zielen ist `NO_EVIDENCE` die erwartete Laufzeitantwort. Die
Zielabdeckung bleibt bei 12 von 25 Fällen. Die fachliche Freigabe steht aus.

### Frühere Gegenprobe auf die Zielabdeckung

Der tatsächlich ausgeführte Test der unveränderten 25 Fragen ergibt **12
übereinstimmende Antwortstatus und 13 Abweichungen**. Alle 13 abweichenden
Fragen liefern `NO_EVIDENCE`. Sie verlangen Inhalte außerhalb der freigegebenen
Pilotabdeckung, unter anderem verminderte Septakkorde, Stilfragen, Groove und
Lizenzen. Die frühere Ergebnisdarstellung mit 25 Treffern ist für diesen
Prüfstand durch den tatsächlichen Adapterlauf widerlegt. Die Fallliste bleibt
als Zielabdeckung erhalten. Die fachliche Freigabe des Adapters steht aus.

---

## 1. Historische Darstellung der Methodik und Evaluierungskriterien

Der portable Knowledge-Adapter (`src/steps/knowledge/adapter.py`) verbindet KI-Agenten deterministisch mit der STEPS-Wissensbasis.
Geprüft wurden 25 Testfälle in 5 Schlüsseldimensionen:

1. **Locale & Spelling (5 Fälle):** Strikte Trennung von H/B (DE) und B/Bb (INT); Enharmonik (C# != Db); Ambiguitätsablehnung ohne Locale.
2. **Alternative Analysen (5 Fälle):** Bewahrung von Mehrdeutigkeiten (vii°7 nach Aldwell vs. Riemann; bVII Modal Interchange; Zwischendominanten).
3. **Genre & Rhythmus (5 Fälle):** Bossa-Nova-Batida, Samba-Batucada (2/2 Alla Breve, Surdo auf 2), 480 PPQ, Swing-Deskription.
4. **Genuine No-Evidence (5 Fälle):** Halluzinationsabwehr bei fehlendem Primärbeleg (gesperrter SEO-Text, nicht registrierte Akkorde wie C11, falsche Seitenzahlen).
5. **Legal Scope (5 Fälle):** Schutz urheberrechtlich geschützter Werke der Klasse E (keine Volltextausgabe; Isolation via `restricted_local`).

---

## 2. Historische und durch die Nachprüfung widerlegte Testergebnisse

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

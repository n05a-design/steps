---
name: steps-knowledge
description: Portable music theory and harmony knowledge adapter for STEPS. Exact retrieval of approved pilot claims with source locators and explicit notation projection.
---

# STEPS Knowledge Skill

Der Adapter liefert fachlich freigegebene Aussagen aus der
[Pilotbibliothek](../../knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md).
Er verwendet dieselbe Freigabeprüfung wie die App. Für eine Abfrage verwende
eine exakte Claim-ID, Progressions-ID, Akkordfolge oder ein ausdrücklich
unterstütztes Stichwort wie `ii-V-I`, `axis` oder `minor plagal`.
Der [Index](index.json) weist außerdem Bestands- und Forschungsthemen aus.
Diese Themen benötigen eigene Freigaben für die Ausgabe als Lerninhalt.

## 1. Grundregeln für Agentenantworten

1. **Strikte Belegpflicht (Groundedness):**
   - Jede fachliche Aussage muss auf eine konkrete Source-ID (`SRC-xxxx` oder Produktquellen-ID wie `omt-ii-v-i`) und einen genauen Locator (Kapitel, Seite) verweisen.
   - Liegt kein verifizierter Beleg vor: Melde eindeutig `NO_EVIDENCE` (z. B. *„Hierfür liegt kein geprüfter Primärbeleg in der STEPS-Wissensbasis vor“*). Erfinde **niemals** Quellen oder Seitenzahlen.

2. **Explizite Notationskonventionen:**
   - Unterscheide immer zwischen internationaler (`INT`: B = H, Bb = B) und deutscher (`DE`: H = B natural, B = B flat) Notation.
   - Fordere bei mehrdeutigen Einzeltönen wie `B` die Konvention an.

3. **Funktionale Mehrdeutigkeit bewahren:**
   - Erkläre komplexe Harmonien (z. B. verminderte Septakkorde `vii°7`, Subtonika `bVII`, Medianten) nicht als monotone Einzelwahrheit.
   - Erhalte die alternative Lesart, soweit sie im freigegebenen Claim belegt
     ist. Verwende für weitergehende Aussagen den jeweils belegten Rahmen und
     behandle unfreigegebene Deutungen als `NO_EVIDENCE`.

4. **Urheberrechts- und Veröffentlichungsgrenzen:**
   - Zitiere keine Volltexte aus urheberrechtlich geschützten Lehrbüchern der Klasse E.
   - Verwende stattdessen die strukturierten Metadaten und didaktischen Zusammenfassungen.

## 2. API-Zugriff im Code

`query("B")` liefert ohne Notationsangabe `AMBIGUOUS_REJECTION`. Die
geprüfte Notationsaussage ist über `query("notation")` abrufbar. Erfasste
Stimmführungstöne erscheinen in der gewählten Schreibweise. Die freigegebenen
deutschen Erklärtexte und Fundstellen behalten ihre Sprache. Bei einer
allgemeinen, nicht exakt zugeordneten Frage liefert der Adapter `NO_EVIDENCE`.
Die beiden exakten englischen Fragen `What note is B in German notation?`
und `What note is B in international notation?` führen zur gleichen geprüften
Notationsaussage. Die Antwort behält ihre freigegebene Sprache.

```python
from src.steps.knowledge import KnowledgeAdapter

adapter = KnowledgeAdapter()
result = adapter.query("ii-V-I", convention="INT")
if result.found:
    print(result.explanation)
    for src in result.sources:
        print(f"Quelle: {src.title} ({src.locator})")
```

## 3. Laufzeitprüfung

`python -B scripts/evaluate_knowledge_adapter.py --json` führt die 25 Fragen
gegen den Adapter aus und zeigt Antwortstatus, Claim-IDs und Fundstellen.
`runtime_status` in den [Prüffällen](skill_eval_cases.json) hinterlegt für
offene Inhalte die erwartete sichere Antwort `NO_EVIDENCE`.
`expected_status` beschreibt weiterhin die Zielabdeckung. Offene Zielinhalte
und die unabhängige Fachprüfung sperren die Freigabe des Adapters.

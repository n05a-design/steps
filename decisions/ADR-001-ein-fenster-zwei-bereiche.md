# ADR-001: Zwei Fenster – ein Hauptfenster mit zwei Bereichen

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Gesamtspezifikation vom 17.11.2026; bestätigt den Vorschlag im [Register](DECISION_REGISTER.md) (OA-0003)

## Kontext
„Zwei Fenster“ konnte zwei Bereiche in einer Tk-Root oder zwei unabhängige Toplevel-Fenster bedeuten ([`PRODUCT_STRATEGY_AND_MVP.md`](../docs/product/PRODUCT_STRATEGY_AND_MVP.md) §5).

## Entscheidung
Ein Hauptfenster (eine Tk-Root) mit zwei Bereichen als Split-View bzw. angedocktem Inspector:
- **links:** Eingabe, Progression, Graph
- **rechts:** Voicing, Tick-Timeline, Export

Separate Dialoge nur bei Bedarf (z. B. Exporteinstellungen).

## Auswirkungen
- Kein Fokusverlust und keine Zustandsfehler zwischen mehreren Fenstern.
- Einklappen, kompakte Leiste und Rücksprung müssen per Tastatur erreichbar sein (§5).
- Rückfall: Der rechte Bereich lässt sich später als eigenes Toplevel lösen, ohne das Datenmodell zu ändern.

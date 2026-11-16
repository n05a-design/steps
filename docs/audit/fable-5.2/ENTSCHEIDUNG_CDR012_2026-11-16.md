# Entscheidung zu CDR-012 / `MODAL_SHIFT_TO_II7` (16.11.2026)

**Status:** Entscheidung des Inhabers über die Bedeutung des historischen Knotens. Keine Fachabnahme, keine Produktionsfreigabe. Die Kante CDR-012 bleibt `OPEN`.

## Frage

Der historische Knoten heißt `MODAL_SHIFT_TO_II7`, also „Wechsel hin zu II7“. Alle Belege im Projekt beschreiben dagegen den Wechsel **von** II7 **zu** ii7.

## Belege

| Beleg | Fundstelle | Aussage |
| --- | --- | --- |
| ERR-033 | [`knowledge/research/03_FACHLICHE_FEHLER.md`](../../../knowledge/research/03_FACHLICHE_FEHLER.md) | PROG-024 korrigiert auf `Cmaj7 – D7 – Dm7 – G7 – Cmaj7`, also V7/V (= II7) → ii7, Stimmführung F♯ → F. |
| Original-Latintext | [`GENRE_RESEARCH_LATIN.md`, Phase 4.10, Abschnitt 3.A](../../../archive/audit-history/ontology-recovery-2026-11-14/originals/20261111T0130_Phase4_10/GENRE_RESEARCH_LATIN.md) | F-Dur: G7 → Gm7. |
| REF-0077 | Golden Case | Prüft D7 → Dm7 und besteht (`PASS`). |
| Knotenname | `MODAL_SHIFT_TO_II7` | Nennt die umgekehrte Richtung. |

## Entscheidung

- Der Knoten bedeutet den Wechsel **II7 → ii7 auf gleichem Grundton**: Die große Terz des Dur-Septakkords sinkt um einen Halbton, Grundton, Quinte und Septime können liegen bleiben.
  - C-Dur: D7 → Dm7 (F♯ → F)
  - F-Dur: G7 → Gm7 (international B → Bb, deutsch H → B)
- `TO_II7` gilt als **historische Fehlbenennung**. Der Knoten wird nicht umbenannt und keine alte ID migriert.
- Als Nachfolgebezeichnung dient der vorhandene Vorschlag `SAME_ROOT_MAJOR_TO_MINOR_SEVENTH` in [`NODE_DEFINITION_PROPOSALS.json`](../../../knowledge/relations/NODE_DEFINITION_PROPOSALS.json). Er bleibt `REVIEW_REQUIRED`.

## Weiterhin offen

- Fachliche Abnahme der neuen Benennung und der Kante CDR-012 durch eine Fachperson.
- Die übrigen fünf Restknoten (CDR-014, CDR-019, CDR-021) brauchen weiterhin Quellen oder Fachentscheidungen; siehe [Restknoten nach Originalfund](GRAPH_RESTKNOTEN_NACH_ORIGINALFUND_2026-11-14.csv). Diese Liste bleibt als Stand vom 14.11.2026 unverändert.

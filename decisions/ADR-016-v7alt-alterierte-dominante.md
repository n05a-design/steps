# ADR-016: `V7alt` als Skalen-Akkord-Einheit

**Status:** accepted (Umsetzung offen)
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, schriftliche Spezifikationsentscheidung vom 17.11.2026; betrifft PROG-020 und PROG-027 ([`OPEN_GAPS.md`](../research/gaps/OPEN_GAPS.md), „Fachprüfung des Progressionskerns“)

## Kontext
PROG-020 und PROG-027 verwenden im Katalog konkrete Formen (`Db7(#11)`, `G7(#11)`); historische Varianten nennen `G7alt`. Der Parser weist die offene Kurzform `7(alt)` bisher ab, weil sie weder Alterationen noch Voicing festlegt ([Referenzbibliothek](../knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md)).

## Entscheidung
`V7alt` ist eine fest definierte Skalen-Akkord-Einheit: die **alterierte Skala** (7. Modus von Melodisch Moll, Superlokrisch), wie in der Jazzlehre (Berklee, Levine, Sikora).
- **Gerüst:** 1, 3, ♭7.
- **Alterationen im Tonvorrat:** ♭9, ♯9, ♭5/♯11, ♯5/♭13.
- **Ausgeschlossen:** reine Quinte, große None (9), große Tredezime (13).
- **Knoten:** repräsentiert die gesamte Tonmenge `{1, 3, ♭7, ♭9, ♯9, ♭5/♯11, ♯5/♭13}`; für G: G, A♭, B♭, B, C♯, E♭, F.
- **Voicing:** Ein gespieltes `V7alt` schlägt nicht alle Alterationen an. Typisch ist eine alterierte Quinte (♭5 oder ♯5) plus eine alterierte None (♭9 oder ♯9), z. B. `G7(#5,#9)` oder `G7(b5,b9)`.
- **Abgrenzung:** `G7(♭9,13)` ist kein `G7alt`; es gehört zur Halbton-Ganzton-Skala. (Präzisierung zur Vorlage, die zusätzlich „Mixolydisch ♭9 ♭13“ nennt: Diese Skala enthält ♭13, nicht 13.)

## Auswirkungen
- PROG-020 und PROG-027 behalten ihre konkreten `#11`-Formen als Katalogbeispiele. Die historische `G7alt`-Variante wird als `V7alt`-Knoten modellierbar.
- Parser: `7alt` darf künftig als Tonvorrat akzeptiert werden, aber nicht als konkretes Voicing; ein Voicing braucht eine ausdrückliche Auswahl. Umsetzung mit Tests in eigenem PR.
- Rückfall: Solange nicht umgesetzt, bleibt die Abweisung von `7(alt)` bestehen.

## Links
- [Open Music Theory, Altered and Extended Chords](https://viva.pressbooks.pub/openmusictheory/chapter/altered-and-extended-dominant-chords/)
- [ADR-014](ADR-014-theorie-perspektiven-und-kontext.md) (Paradigma `jazz_functional`)

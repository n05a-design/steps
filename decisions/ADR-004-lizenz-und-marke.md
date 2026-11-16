# ADR-004: License/Brand – Code MPL-2.0, eigene Wissensdaten CC BY 4.0

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Gesamtspezifikation vom 17.11.2026 mit Korrektur aus dem Repository-Abgleich (kein Lizenzwechsel)

## Kontext
Das Repository steht unter MPL-2.0 (`LICENSE`); Glide ebenfalls. MPL-2.0 ist ein dateibezogenes Copyleft: Geänderte MPL-Dateien bleiben offen, die Kombination mit anderem, auch proprietärem Code ist erlaubt. Ein Wechsel zu MIT oder Apache-2.0 bräuchte die Zustimmung aller Rechteinhaber, und aus Glide übernommene Dateien müssten trotzdem MPL-2.0 bleiben. Im Repository liegen außerdem fremde PDFs und Extrakte, deren Rechte das [Rechteinventar](../research/gaps/RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md) einzeln führt.

## Entscheidung
- **Code und Engine:** bleiben unter **MPL-2.0**. Kein Lizenzwechsel.
- **Eigene Wissensdaten und Kataloge** (eigene Texte, Zusammenfassungen in eigenen Worten, eigene Kataloge wie `PROG`, `PAT`, `P`, Graphentscheidungen): **CC BY 4.0**.
- **Fremde Inhalte** (PDFs, Volltext-Extrakte, gespeicherte Webseiten, Zitate): behalten ihren Status laut Rechteinventar; sie werden nicht neu lizenziert.
- **Marke:** Arbeitstitel „STEPS“ bis zu einer Markenprüfung (DPMA/EUIPO); eigenes Logo, keine Fremdassets.

## Auswirkungen
- Je Datei klar kennzeichnen, welche Lizenz gilt (SPDX für Code; Kennzeichnung für Wissensdaten). Die genaue Abgrenzung je Ordner ist ein eigener Schritt.
- Der offene Namenskonflikt D5 (verschiedene STEPS-Akronyme) bleibt bis zur Markenprüfung offen.
- Rückfall: Eine spätere Doppellizenzierung eigener Dateien bleibt möglich; ein Rückzug von MPL-2.0 für veröffentlichte Versionen nicht.

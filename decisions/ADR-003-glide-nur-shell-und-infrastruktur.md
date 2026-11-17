# ADR-003: Glide-Code-Quelle und Umfang der Wiederverwendung

**Status:** accepted
**Datum:** 2026-11-17
**Entscheidungsträger / Beleg:** Inhaber, Gesamtspezifikation vom 17.11.2026 mit Präzisierung aus dem Repository-Abgleich

## Kontext
Glide ist ein Python/Tkinter-Aufgabenplaner unter MPL-2.0 ([`RIGHTS_SECURITY_AND_RELEASE.md`](../docs/governance/RIGHTS_SECURITY_AND_RELEASE.md)). Es hat kein Musik-Datenmodell und keinen Akkord-Parser. `AGENTS.md` Regel 9 erlaubt Glide nur als technischen Reuse, mit Lizenzprüfung und Verweis statt unkontrollierter Kopie. Der bisherige Vorschlag regelte nur die Quelle: lokaler Stand 3.53.0 erst nach vollständigem Commit/Backup und QA (OA-0007).

## Entscheidung
- **Umfang:** Wiederverwendung nur für UI-Shell und Infrastruktur: Theme, Sidebar, Fokus, Einstellungen und vergleichbare Querschnittstechnik. Keine Todo-Fachlogik.
- **Herkunft:** Jede übernommene Datei bekommt einen Herkunftsnachweis (Glide-Commit, Pfad, Lizenzhinweis, Änderungen) gemäß `AGENTS.md` Regel 9. Übernommene Dateien bleiben unter MPL-2.0 ([ADR-004](ADR-004-lizenz-und-marke.md)).
- **Quelle:** weiterhin nur ein verifizierter, committeter Glide-Stand (bisheriger Vorschlag, OA-0007).
- **Trennung:** Musiktheorie, PPQ-Zeitmodell und MIDI-Writer bleiben als reine Bibliothek in `src/steps/`, ohne Abhängigkeit von `app/`.

## Auswirkungen
- Shell-Spikes gemäß [`SHELL_EXTRACTION_DEEP_SPEC.md`](../docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md) prüfen nur Shell-Fähigkeiten.
- Rückfall: Eine Datei ohne sauberen Herkunftsnachweis wird nicht übernommen, sondern neu geschrieben.

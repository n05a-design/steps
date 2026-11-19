# STEPS Gemini Knowledge Pack – deutsche Zusammenfassung

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — deutsche Zusammenfassung; die englischen Einzelartikel sind der primäre Inhalt des Pakets.
**Status key:** IMPLEMENTED = umgesetzt; TESTED = automatisiert belegt; PARTIAL = unvollständig; PLANNED = geplant; BLOCKED = blockiert; HISTORICAL = historisch; NOT_EVIDENCED = nicht belegt.

## Zweck

Dieses Paket gibt Gemini eine quellengebundene Orientierung zum STEPS-Repository am genannten Commit. Es ist keine Produktfreigabe und ersetzt weder Code, Tests, akzeptierte ADRs noch menschliche Fach-, Übersetzungs- oder Rechteprüfung. Die bestehende deutsche historische Dokumentation bleibt unverändert.

## Projektstand

STEPS umfasst einen Python-Musiktheoriekern, eine Tkinter-Desktop-Vorschau, Projekt-Speicherung und Standard-MIDI-Dateiexport. Die akzeptierte v0.1-Richtung umfasst Akkorde und MIDI-Export; Drums sind laut ADR-013 auf App v2 verschoben. Nur v0.1.0 ist als Release belegt. Ein vollständiger Installer, plattformübergreifende Barrierefreiheit, DAW-Interoperabilität, Nutzerstudien oder 1.0-Freigabe sind hier nicht nachgewiesen.

## Belegter Testumfang

Die aktuelle Evidenz berichtet 746 bestandene Unittests, 119 Benchmarkfälle (8 Pilot, 25 Katalog, 51 Stichprobe, 12 Coach, 3 Veröffentlichung, 7 API, 13 Backlog) und einen Pilotlauf mit 8 PASS / 0 FAIL. Das beweist weder eine vollständige Fachabnahme noch Übersetzungs-, Rechte- oder Produktreife.

## Unverhandelbare Fachunterscheidungen

- Klingende Tonhöhe, Tonklasse (0–11) und Notenschreibweise sind verschieden.
- Akkordidentität, Symbol, Voicing, Umkehrung und Funktion im Kontext sind verschieden.
- Deutsche Notation: H = internationales B, B = internationales Bb. Internationale Notation: B = B; Bb = B♭.
- UI-Sprache und Notationskonvention sind unabhängig.
- Theoriefakt, Korpusstatistik und kreative Heuristik nicht vermischen.
- Notation, MIDI-Export und Audiowiedergabe nicht gleichsetzen.

## Statusvokabular

**IMPLEMENTED** umgesetzt; **TESTED** automatisiert geprüft; **PARTIAL** mit offenen Lücken; **PLANNED** geplant; **BLOCKED** durch fehlende Entscheidung/Abhängigkeit; **HISTORICAL** nur für einen früheren Stand; **NOT_EVIDENCED** nicht belegt. Keine Statusangabe darf aus einer anderen abgeleitet werden.

## Einstieg

Beginne mit dem [Knowledge Index](00_KNOWLEDGE_INDEX.md). Für Gemini-Regeln siehe [19_GEMINI_INSTRUCTIONS](19_GEMINI_INSTRUCTIONS.md), für Quellenbelege [17_SOURCE_EVIDENCE_REGISTER](17_SOURCE_EVIDENCE_REGISTER.md) und für offene Prüfungen [21_FINAL_AUDIT_REPORT](21_FINAL_AUDIT_REPORT.md).

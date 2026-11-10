# Glide – Übergabe von VS-Code-Copilot an Antigravity

**Zweck:** Den laufenden **lokalen** Glide-Stand ohne Verlust fortführen, den 3.53.0-Freigabestatus korrekt prüfen und erst danach das Zweifenster-Grundgerüst zur späteren Wiederverwendung vorbereiten.

## Reihenfolge

1. `STATUS_UND_ABGLEICH.md`: unterschiedliche Git-/Versions-/QA-Achsen.
2. `ANTIGRAVITY_STARTPROMPT.md`: **dieser Prompt ist der erste Schritt in Antigravity**; zunächst Diagnose und Prüfplan, nicht sofort Refactoring.
3. `QA_GATE.md`: verbindliches Freeze-/Prüf-/Freigabe-Gate.
4. `MODULE_EXTRACTION_PLAN.md`: Kandidaten, Schichten, Eigentum, Rückwärtskompatibilität.
5. `PROMPT_SHELL_ISOLATION.md`: erst nach gesichertem Gate ausführen, auf eigener Kopie/Branch.
6. `PROMPT_SHARED_COMPONENTS.md`: nur für einen kleinen entkoppelten Pilot, nicht für 94 Module auf einmal.
7. `HANDOVER_TEMPLATE.md`: eindeutige Übergabe zwischen Agenten.

**Kanonische Ausgangsdokumente nicht duplizieren:** `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md` ist die Aufgaben-Roadmap, `01_Repository/Glide/src/glide/README.md` das vollständige Systeminventar, `docs/07_QA_BERICHT.md` der Befundnachweis. Die Unterlagen hier sind **Ergänzung** für das Projekthandling, nicht eine weitere aktuelle Wahrheit über jeden Änderungsstand.

## Wichtigste Scope-Grenze

Glide und Steps haben getrennte Daten, Modelle, Versionsnummern, Releases und Releasesicherheit. Eine technische Gemeinsamkeit entsteht erst, wenn **mindestens zwei echte Verbraucher** denselben Schnittstellenvertrag separat testen. Vorher ist es ein Kandidat, kein freigegebenes SDK.

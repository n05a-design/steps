---
trigger: always_on
description: Glide-Erhalt, lokaler Agentenwechsel und geprüfte Extraktion von Komponenten
---
# Antigravity-Arbeitsregeln für Glide

Diese Regeln **ergänzen**, ersetzen aber nicht `01_Repository/Glide/AGENTS.md`. Vor jeder Änderung lesen: `00_Arbeitsvorbereitung/Glide_Uebergabe.md`, `00_Arbeitsvorbereitung/Glide_Entwicklungsplan.md`, `01_Repository/Glide/docs/07_QA_BERICHT.md`, `01_Repository/Glide/src/glide/README.md` und die Design- und Architekturverträge.

1. Den **lokalen** Arbeitsbaum mit `git status`, Branch, vollständigem SHA, `VERSION` und `GLIDE_SYSTEM_VERSION` prüfen; der öffentliche Snapshot ist keine Garantie für die lokale Version.
2. Keine destruktiven Git-Kommandos und keine Arbeit in fremden Projektordnern. Kein Merge, Tag, Release, Push oder Datenmigration ohne explizit freigegebenes Gate.
3. Keine zweite aktive Roadmap oder zweite vollständige Modulliste erzeugen. Diese Regeln ergänzen den bestehenden kanonischen Plan und das Systemregister.
4. Erst Diagnose/Abnahme auf eingefrorenem Commit, danach Änderungen. Eine neue Codeänderung entwertet alte QA-Nachweise für die betroffenen Bereiche.
5. Glide produktiv nicht durch Steps ersetzen oder umrüsten. Schritte zur Wiederverwendung in neuem Projekt getrennt und rückwärtskompatibel prüfen.
6. Haupt-/Nebenansicht, Seitenleiste, einklappen/ausblenden, Einstellungen, Logo/Title/Toolbar/Buttons, Suche/Fokus, alle gewählten Themen und Schriftarten, Verhalten bei Fensterwechsel und Speicher-/Undo-Verträge beim Shell-Schnitt schützen.
7. Fremd-/Lizenzmaterial, Nutzerdateien, E:/C:/OneDrive-Archive, Git-Stashes und historische Logs nicht ohne schriftliche Zustimmung verändern.
8. Ein Tk-freies Modul ist **nicht** automatisch produktneutral. Integration erfordert vollständige Import-, Ressourcen-, Zustands- und GUI-Lebenszyklustests.
9. Tests mit isoliertem `GLIDE_DATA_DIR`, synthetischen Daten, echten Negativfällen und commitbezogenen Befunden durchführen. Fehlende Plattformen als `NICHT GETESTET` benennen.
10. KI-Hinweis, menschliche Abnahme, Source-Provenienz, MPL-2.0 und alle verwendeten Fremdlizenzen dokumentieren. Schlechte oder rote Ergebnisse nicht glätten.

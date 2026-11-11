# Meta-Prompt V5: unabhängige Verbesserung des STEPS-Antigravity-Master-Prompts

## Zweck

Dieser Prompt richtet sich **nicht** an Antigravity zur Ausführung der Analyse, sondern an einen weiteren unabhängigen KI-Client, der den bereits erstellten Master-Prompt V5 kritisch verbessern soll. Wenn das Ziel die **sofortige lokale Prüfung** ist, stattdessen direkt `30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md` nutzen.

## Auftrag an den unabhängigen Prompt-Architekten

Du bist Lead Auditor für Softwarearchitektur, Forschung, Dokumentenintegrität, IT-Security, wissenschaftliche Quellenprüfung und agentische Entwicklungsworkflows. Lies die **vollständige** beigefügte Datei `prompts/30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md`. Vor der Überarbeitung prüfe den tatsächlichen aktuellen STEPS-GitHub-Stand und die einschlägigen Projektunterlagen, besonders `AGENTS.md`, `docs/project/PROJECT_OVERVIEW.md`, `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, `docs/audit/`, `docs/quality/`, `prompts/README.md`, `src/steps-0.00/README.md`, `tools/validation/check_structure.py`, `source_archive/` und `src/glide-v3.53/`.

**Verbindlicher Nutzerbeschluss:** Glide 3.53.0 ist der grün geprüfte Ausgangsstand; dessen UI-/Infrastrukturfundament soll kontrolliert neutralisiert und als Basis für die eigenständige STEPS-App verwendet werden. Behandle diese Zielrichtung als vorgegeben; analysiere Alternativen für den sicheren technischen Weg, ohne die Nutzerentscheidung zu überschreiben.

Prüfe den Master-Prompt auf mindestens diese Fehlerklassen:

1. Fehlende Dateien, falsch benannte neue Pfade, veraltete Remote-/lokale Snapshots und unterschiedliche Git-Branch-Stände.
2. Scheinvollständigkeit bei 3.000+ Dokumenten/Code-/Binärdateien, nicht skalierbare Leseanweisungen und fehlende Coverage-Nachweise.
3. Ausgelassene originale Quellen, Research-Handover, alle alten Konflikt-/REQ-/Audit-IDs, V4- und V1-Doppelpakete, 29+ aktuelle Arbeits-Prompts.
4. Fehlende Validierung von Glide-3.53.0-Freeze, 94 Modul-/25 Paketkandidaten, AST-/Callback-Kopplung, Lizenz-/Assetfragen, UI-/Dateisystem-Isolation und negativer Testfälle.
5. Verwechslung `src/steps-0.00` (Versions-/Arbeitsordner) mit normal importierbarem Python-Paket `src/steps`; veralteter Strukturcheck und nicht nachgewiesene grüne STEPS-CI.
6. Unzureichende musikwissenschaftliche Verträge (DE-/internationales B/H, Enharmonik, alternative Harmonieanalysen, Timeline, MIDI/SMF, Drums, Education/Explanation).
7. Fehlende Trennung von Forschung, bibliografischem Metadatennachweis, tatsächlicher Wissens-Ingestion, Runtime-Logik und Skill.
8. Fehlende Git-Forensik und Rechte-/Security-Vorkehrungen für öffentlich eingebundenes Fremdmaterial, PDFs, Webcaches, Audio/Fonts/Assets.
9. Fehlende prüfbare Outputs, IDs, Zustands-Persistenz, harte Stoppgates und saubere Freigabetrennung von Analyse und produktivem Rückbau.
10. Überflüssige Prompt-Wiederholungen, unnötiger Tokenverbrauch und nicht abarbeitbare oder unklare Teilaufträge.

### Verlangtes Ergebnis

Erzeuge (A) einen komplett überarbeiteten Antigravity-Direktprompt als einzelne kopierbare Markdown-Datei; (B) eine lückenlose Änderungs-/Verbesserungsmatrix `old_requirement → revised_requirement → reason → verification`; (C) eine unabhängige, maschinenprüfbare Abnahmeliste; (D) einen kurzen Bericht offener Grenzen/fehlender Quellen und der zum Bearbeitungszeitpunkt verifizierten HEAD-SHAs.

**Nicht zulässig:** Nutzerentscheidungen erfinden, Code ohne Freigabe ändern, historische Belege löschen, „alles gelesen“ ohne Abdeckungsregister behaupten, Glide-grüne CI in STEPS-grün umdeuten oder konkrete Skriptläufe fingieren. Fertige die neue Datei erst aus, wenn jede dieser Prüfklassen mit Nachweis bearbeitet ist.

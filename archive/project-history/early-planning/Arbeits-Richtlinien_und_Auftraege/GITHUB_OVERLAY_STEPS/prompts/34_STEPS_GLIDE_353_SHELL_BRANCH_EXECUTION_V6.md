# Ausführbarer Folgeprompt – Glide-3.53-Shell → STEPS (nur nach Architektur-Freigabe)

**NICHT während des Read-only-Audits ausführen.** Dieser Prompt ist für einen später ausdrücklich autorisierten, isolierten STEPS-Implementierungsbranch.

Voraussetzungen: `docs/project/antigravity-handover/SHELL_AND_REUSE_CONTRACT_V6.md`, `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`, `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`, 30 Shell-Szenarien, eingefrorenes Hash-/Lizenz-/Reuse-Manifest, Owner-ADR und aktuelle `STATE.json`/Outputregister. `src/glide-v3.53/` bleibt als Vergleichsquelle erhalten. Ursprungsrepository `n05a-design/glide-to-do` bleibt unberührt.

1. Echten STEPS-Laufzeitpfad, Datenroot, Konfig, IDs und neutralen UI-Shell-Entry Point festlegen, `src/steps-0.00/` nicht als importierbares Python-Package behaupten.
2. Minimalen, revertierbaren Schritt in einer neuen STEPS-Datei implementieren; keine großflächige `ListApp`-Kopie und keine unkontrollierten Import-Seiteneffekte.
3. Erhalte Gesamtoberfläche außerhalb der künftig zwei Bereiche; Header, Logo/Brand, Iconbuttons, Einstellungen, Themes/Fonts, Sidebar/Seitenpunkte samt Hide/Collapse, Menüs, Fokus/Keyboard/Tooltips, Suche als neutrales Eingabeelement, Rendering/Layout, Resize/DPI, Error-/After-Lifecycle.
4. Alte Task-Aktionen in Seitenliste/Hotkeys/Timer/Background/Undo/Persistenz vollständig isolieren; alle nicht implementierten Steps-Aktionen als nachweisbar sichere No-ops mit klarer Anzeige. Kein Zugriff auf Glide-UserData, dessen Locks/Caches/Backups.
5. `component_id`/API-/Lifecycle-/Version-/Lizenz-/Origin-SHA-/Consumers-/Migrationstest-Verträge anlegen, bevor Shared-Code als allgemeines Framework beworben wird.
6. Ein Delta, konkrete Regressionstests und native/synthetische Datenprüfungen; No-Glide-Write-/Read-Negativtests, 30 UI-Szenarien nach Gate, dann menschliche Sichtprüfung. Teststatus nachweisbar und commitgebunden.
7. Jede Analyse, jedes Ergebnis, jeder Fehler, jeder generierte Vorschlag und alle allgemeinen Projektausgaben in `OUTPUT_REGISTER`/Sessionlog/Handover schreiben. Vorarbeiten V1–V5 erhalten, keine ungesicherten Änderungen überschreiben.

**Abgabe:** Code-Diff/Source-Map, Testreport, UI-/Asset-Paritätsbelege, Architekturdokument-Nachtrag, Reuse-Changelog, Outputregister, aktualisierte `STATE.json`, `NEXT_SESSION_HANDOVER.md`, PR-Entwurf und Rollback. Keine automatische Merge-/Release-Freigabe.

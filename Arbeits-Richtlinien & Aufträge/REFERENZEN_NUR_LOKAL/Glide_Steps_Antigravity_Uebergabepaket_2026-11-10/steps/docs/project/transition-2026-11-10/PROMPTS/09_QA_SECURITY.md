# P09 – Steps Teststrategie, Security und GitHub CI

## Direkt nutzbarer Prompt

Du bist unabhängiger QA-/Security-Engineer für `n05a-design/steps`. Lies zuerst `.github/workflows/structure-check.yml`, `tools/validation/check_structure.py`, `pyproject.toml`, vorhandene Tests/Fixtures und den tatsächlichen Code. Der bestehende GitHub-Strukturcheck ignoriert reine `app/**`- und `src/**`-Änderungen durch `paths:`-Filter und führt keine Domain-Tests aus. Eine grüne Strukturprüfung ist **keine** Produktfreigabe.

Arbeite auf isoliertem Branch. Baue einen **unbedingt auf Pull Requests laufenden** Python-Workflow mit syntax/compile, Unit-/Golden-/Negativtests für Domain, Schema, MIDI, Save/Load, Rechte-/Pfadvalidierung und (wenn vorhanden) separaten Tk-Tests. Prüfe `pytest`-Verfügbarkeit/Abhängigkeitspins anhand `pyproject.toml`; keine Pakete ohne nachvollziehbare Entscheidung. Prüfe Required-Status-Check-Namen im tatsächlichen GitHub-UI – nicht vorher erfinden. Führe bewusst einen defekten Testlauf vor Änderung als negative Kontrolle aus und verifiziere, dass CI bei `src/steps`-only-Änderungen startet.

Security-Tests: ZIP-Traversal, Symlinks/Junctions, Archive Bombs, übergroße MIDI/Events, fehlerhafte MusicXML/DTD, path traversal, falsche Settingsversionen, konkurrierende Save/Lock-Zugriffe, Permission denied, Disk full, Crash-Recovery, nicht verfügbare Audio-Devices, native Tk-Interpreter-/Callback-Leaks, Datenpfad-Isolation zu Glide. **V2 `safe_install_v2.py --apply` ist gesperrt:** dokumentierter Symlink-Escape. Fremddownloads/alte Generatoren vor Ausführung lesen und nur in kontrollierter Testumgebung verwenden.

Schreibe eine echte Testpyramide mit `PASS/FAIL/SKIPPED/NOT_TESTED`, festem SHA, Python/Tk/OS und reproduzierbarem Aufruf; End-to-End nur dort behaupten, wo es wirklich durchgelaufen ist. Kopple Security-Funde an Issues/ADR und Priorität; keine automatische Datenbereinigung und kein Force Push.

## Akzeptanz

PR-Workflow triggert bei Domain-Änderungen, reale Tests laufen, provozierter Fehler bricht Job ab, Security-Fälle mit dokumentierten Ergebnissen und Restgrenzen, kein unberechtigtes Release-Siegel.

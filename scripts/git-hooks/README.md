# Lokale Git-Hooks

Der Pre-Commit-Hook ruft den STEPS-Secret-Scanner auf.

| Einstieg | Inhalt |
| --- | --- |
| [Pre-Commit-Hook](pre-commit) | Einstieg beim Commit. |
| [Installationsskript](../install-git-hooks.py) | Optionale lokale Hook-Installation. |
| [Secret-Scanner](../pre-commit-secret-check.py) | Prüflogik für gestagte Änderungen. |

Der Hook ergänzt den [CI-Workflow](../../.github/workflows/secret-scan.yml).

[Zur Bereichsübersicht](../README.md)

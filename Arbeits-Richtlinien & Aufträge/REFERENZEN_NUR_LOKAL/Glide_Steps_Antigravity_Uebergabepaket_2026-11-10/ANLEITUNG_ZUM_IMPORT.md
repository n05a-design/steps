# Übergabepaket: Glide → Antigravity und Steps

**Erstellt:** 10.11.2026 · **Format:** ausschließlich Markdown + Prüfsummen · **Status:** Dokumentationsvorschläge, kein App-Release, kein Code-Refactoring, keine automatische Migration.

## Zwei unabhängige Zielrepositories

- `glide-to-do/` enthält **neue** Dateien relativ zum Repository-Wurzelordner `n05a-design/glide-to-do`. Glide bleibt die bestehende Aufgaben-/Planungs-App.
- `steps/` enthält **neue** Dateien relativ zum Repository-Wurzelordner `n05a-design/steps`. Steps wird eine eigenständige Musik-App.
- Die ZIP-Struktur ist **keine neue gemeinsame Monorepo-Struktur**. Die beiden Verzeichnisse dienen nur der Zuordnung beim manuellen Import.
- Keine bestehenden Dokumente überschreiben; keine alte Projekt-Overview löschen; keine alten Git-Verläufe umschreiben.

## So verwendest du die Übergabe ohne Datenverlust

1. Copilot in VS Code beenden bzw. Schreibzugriffe stoppen. Lokale Änderungen im **richtigen Repository** erfassen: `git status --short`, `git branch --show-current`, `git rev-parse HEAD`, `git remote -v`. Uncommittete Dateien *nicht* durch Checkout, Pull oder Reset verlieren.
2. Im lokalen Glide-Ordner den aktuellen Arbeitsstand sichern und einen separaten Themenbranch anlegen. Falls der Arbeitsbaum nicht sauber ist, zuerst den tatsächlich vorhandenen Zustand prüfen und bewusst committen oder eine überprüfte Kopie anfertigen; **kein automatisches `git stash`, `git reset --hard`, `git clean -fd`, `git pull --rebase`**.
3. ZIP **außerhalb** der beiden Repositories entpacken. `MANIFEST_SHA256.txt` vor dem Import prüfen. Dateien nach Sichtprüfung **einzeln** in die jeweiligen Zielpfade kopieren; es werden ausschließlich neue Pfade vorgeschlagen.
4. Pro Repository: `git status --short`, `git diff --check`, Verweise und bestehende Agentenregeln prüfen, Commit nur auf dem neuen Branch und Pull Request zum Review erstellen. Niemals ungeprüft beide Projekte in ein Git-Repository kopieren.
5. Antigravity: lokalen Ordner des tatsächlichen Glide-Checkouts öffnen, Agent in der lokalen Workspace-Ansicht starten, Prompt `glide-to-do/docs/transition/2026-11-10/ANTIGRAVITY_STARTPROMPT.md` vollständig einfügen. Entscheidend ist der lokale Stand, nicht die hier eingefrorene GitHub-SHA.
6. Steps: die vorhandene `AGENTS.md` und die bestehende Konsolidierung zuerst lesen. Mit dem neuen Steps-README und anschließend genau **einem** fachbezogenen Prompt weiterarbeiten.

## Bestätigte Remote-Snapshots (nicht als lokale HEADs missverstehen)

| Repository | main-SHA am Prüfzeitpunkt | Beobachtung |
|---|---|---|
| Glide | `9e767bea5e21063466a28ac3a679406484ad5d5f` | Version 3.53.0; PR #75 gemergt; lokale und Remote-Tests streng commitbezogen beurteilen |
| Steps | `75329fef46878a5ac816cef3690e612a9e8fe52c` | Forschungsarchiv und Scaffold; keine geprüfte Musik-App |

**Wichtige Korrektur:** Glide-Übergabe/Entwicklungsplan/QA sprechen historisch noch davon, dass `main` auf 3.50.7 steht. Der Remote-Branch ist weiter. Diese Aussage nicht in den Quelltext übernehmen, ohne die tatsächlich veränderten Dokumente zu aktualisieren. PR #75 führt 3.53.0 auf `main`; der danach gestartete Glide-Prüflauf war zum Untersuchungszeitpunkt noch nicht vollständig abgeschlossen. Ein grüner Paketjob beweist nicht die gesamte Plattform-/Releasefreigabe.

**Rechte:** GitHub-Verbindung in dieser Unterhaltung `pull=true`, `push=false`. Es wurden **keine** Remote-Dateien geschrieben. Dieses ZIP ist zur manuellen, selektiven Übernahme bestimmt.

## Grenzen der Quellenprüfung

GitHub-Verzeichnisbäume wurden vollständig inventarisiert (Dateipfade). Ein großer Teil des Steps-Bestands besteht aus PDFs, Bildern, Audio/MIDI, Webarchiven und Fremdmaterial, die hier **nicht vollständig inhaltlich gelesen, lizenzrechtlich freigegeben oder ausgeführt** wurden. Vorhandenes Review V3 dokumentiert 26 Prüfungsdimensionen, 40 alte Widersprüche, 34 Lücken und 26 Entscheidungspositionen (100 historische IDs); diese bleiben unverändert erhalten und werden nicht durch diese Zusatzdokumente überschrieben. Andere lokale Copilot-Dateien sind aus dem Chat heraus nicht einsehbar.

## Kontrolle der ZIP-Integrität

`MANIFEST_SHA256.txt` listet die SHA-256-Werte **aller enthaltenen Projektdateien**. Unter PowerShell nach Entpacken beispielsweise:

```powershell
Get-FileHash '.\glide-to-do\docs\transition\2026-11-10\ANTIGRAVITY_STARTPROMPT.md' -Algorithm SHA256
Get-FileHash '.\steps\docs\project\transition-2026-11-10\README.md' -Algorithm SHA256
```

Diese Prüfsummen belegen Dateigleichheit, nicht die fachliche Korrektheit oder Authentizität einer externen Downloadquelle. Manuelle Sichtprüfung bleibt erforderlich.

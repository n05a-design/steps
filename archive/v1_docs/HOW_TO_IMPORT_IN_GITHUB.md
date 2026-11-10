# STEPS – GitHub-Übernahme aus dem ZIP (ohne automatische Überschreibung)

**Stand 10.11.2026.** Der direkte Branch-Schreibversuch über die GitHub-Integration scheiterte mit `403 Resource not accessible by integration`; auf `main` wurden **keine Änderungen** vorgenommen. Die folgende lokale Alternative führt nur eine reversible Dokumentationsänderung aus.

1. ZIP in einen **anderen Ordner** als das Steps-Repository entpacken, beispielsweise `C:\Temp\STEPS_Projektpaket_2026-11-10`.
2. Schritte aus PowerShell in einem bereits lokal vorhandenen und **sauberen** `n05a-design/steps` Checkout ausführen:

```powershell
cd "C:\PFAD\ZU\steps"
git fetch origin
git status
# nach Sichtprüfung und Sicherung aller lokalen Änderungen
git switch -c docs/steps-overview-2026-11-10 origin/main
python "C:\Temp\STEPS_Projektpaket_2026-11-10\tools\safe_stage_steps_docs.py" --repo "C:\PFAD\ZU\steps"
# Liste aller Dateien / Konflikte prüfen; nur danach
python "C:\Temp\STEPS_Projektpaket_2026-11-10\tools\safe_stage_steps_docs.py" --repo "C:\PFAD\ZU\steps" --apply
git status
git diff --stat
git diff --check
```

Das Skript **kopiert nur neue Markdown-/JSON-/CSV-Dateien** in die dafür vorgesehenen Fachordner und **überschreibt nichts**. Existierende `knowledge/README.md`, `design/README.md` usw. werden übersprungen und müssen gezielt geprüft/integriert werden; kein stilles Ersetzen.

3. Von den neuen Dateien ausschließlich freigegebene Projektdokumentation stagen – **keine `source_archive/`-Dateien**, keine fremden PDFs und keine vollständige lokale Glide-Datei in einen öffentlichen PR aufnehmen. Vor einem Git-Commit aktuelle Coderegeln, License Notices, interne Links und ggf. den Inhalt eines veröffentlichten Dokumentes auf private Informationen prüfen. Die tatsächliche Git-Integration, `commit`, `push` und `draft PR` sind bewusste menschliche Schritte.

**Hinweis:** Das Downloadpaket selbst ist eine Auditkopie und enthält den vollständigen lokalen Glide-Quellstand. Darum nicht einfach das gesamte entpackte Verzeichnis ins öffentliche Repository pushen. Sicheres Staging-Skript und Vorbereitungsprompts erlauben eine manuelle Umsetzung, ohne Originaldaten oder fremde Bücher unkontrolliert zu veröffentlichen.

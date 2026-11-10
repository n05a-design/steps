# Steps – sichere lokale GitHub-Übernahme der geprüften Dokumentation

**Status 10.11.2026.** Der GitHub-Connector erlaubte zwar das Lesen, verweigerte bei einem früheren Branch-Erstellungsversuch jedoch mit HTTP 403 die tatsächliche Schreibaktion. Daher **kein** Commit/PR und **keine Änderungen an `main`**. Dieses ZIP ist eine Auditkopie; sie enthält Nutzer-Originaldateien sowie ein separat archiviertes altes ZIP und darf nicht vollständig in ein öffentliches Git-Repository kopiert werden.

## Die zwei Bereiche des Pakets

1. **Vollständiges Audit (privat):** `source_archive/`, `archive/`, 29 Prompts, Source- und Auditberichte, Quell-/Git-Metadaten. Hier liegen auch der hochgeladene Glide-Hauptcode und alte Chat-/Planungstexte. **Nicht automatisch veröffentlichen.**
2. **Geprüfter Kandidat zur Dokumentationsübernahme:** `publish_overlay/` enthält ausschließlich ausgewählte Markdown-/CSV-/JSON-/YAML-Dateien mit umgeschriebenen Paket-only-Links. Enthält **keine** Original-Uploads, Bücher, MIDI, Fontdateien oder historischen ZIPs. Auch dieser Teil braucht vor Veröffentlichung eine menschliche Review auf vertrauliche Inhalte und Rechtsstatus.

## Variante A – lokal mit nicht-destruktivem Skript

1. ZIP **außerhalb** des Steps-Repositories entpacken, z. B. `C:\Temp\STEPS_Audit`.
2. Im lokalen Steps-Checkout den aktuellen Stand überprüfen, Änderungen sichern und dann neuen Branch erstellen:

```powershell
cd "C:\PFAD\ZU\steps"
git fetch origin
git status
# nur nach Sicherung eigener Änderungen, nicht auf dirty working tree
# und nur bei vorheriger Prüfung der aktuellen main-Basis
git switch -c docs/steps-audit-reconciliation-2026-11-10 origin/main
```

3. Dry-run und vorsichtige Übernahme **nur der noch fehlenden Dateien**:

```powershell
python "C:\Temp\STEPS_Audit\tools\safe_stage_steps_docs.py" --repo "C:\PFAD\ZU\steps"
# liste NEW, SKIP, collision und SHA prüfen
python "C:\Temp\STEPS_Audit\tools\safe_stage_steps_docs.py" --repo "C:\PFAD\ZU\steps" --apply
```

Das Staging-Skript benutzt **ausschließlich `publish_overlay/`**, erstellt keine Git-Commits und überschreibt weder gleiche noch abweichende Dateien im Repo. Es listet bestehende Pfade als Kollisionen, deren mögliche inhaltliche Integration der Owner/Reviewer separat entscheidet. Ein zweiter Lauf auf bereits gestagten Dateien ist nur ein Statusbericht, kein Beweis für fachliche Tests. Den mitgelieferten Overlay-Kandidaten nicht vor Review manuell regenerieren.

4. Im Feature-Branch den Diff, alle neuen internen Links, Lizenzen und Textinhalte prüfen. Nur ausdrücklich freigegebene Dateien stagen/commiten, Push/PR manuell:

```powershell
git status --short
git diff --check
# ggf. Link-/Schema-/Testläufe und Unterschiede zu vorhandenen Docs
# git add <ausschließlich geprüfte Dateien>
# git commit -m "docs: add evidence-based STEPS audit and roadmap"
# git push -u origin docs/steps-audit-reconciliation-2026-11-10
```

**Nie** `source_archive`, `archive`, private Bücher, fremde Downloads/Assets, persönliche Daten oder das unkontrolliert extrahierte ganze Glide-Repositorium in `main` übernehmen. Nicht automatisch Force-Push, History-Rewrite, Merge oder Delete ausführen.

## Einschränkungen dieser Übernahme

- `publish_overlay/` ist **kein** vollständiger Ersatz bestehender Steps-Dokumentation; existierende `knowledge/README.md`, `design/README.md`, originaler Research-Handover und weitere kanonische Inhalte werden nicht überschrieben. Konflikte müssen per Dokument- und Source-ID-Abgleich zusammengeführt werden.
- Die eingebetteten alten Snapshots stammen aus `main`-Ständen vom 10.11.2026. Vor Push erneut `origin/main` lesen: bei verändertem Repo eine neue Snapshot-Evaluation durchführen.
- Sicherheits-/Urheberrechtsscan für jede geplante öffentliche Datei vor Veröffentlichung. Die Dokumentation ist **keine** Freigabe sämtlicher vorhandener Archiv-PDFs.
- `tools/verify_package_audit.py` validiert die lokale Auditkopie; seine grüne Ausgabe beweist *keine* bestandenen Steps-Produkt-, Musik-, OS- oder Rechte-Tests.

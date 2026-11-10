# STEPS – Repository-Strukturierung (Vorbereitungspaket)

**Bestandsbasis:** `n05a-design/steps`, `main` bei `b42a990681ce5fd12c7756fb2ada962e01474521`, 10. November 2026. Die GitHub-Verbindung ist aktuell lesend; `push: false`.

Das Paket enthält eine **voll ausgearbeitete Architekturgrundstruktur** (103 neue Textdateien), fünf JSON-Schemata, Dokumentation, KI-Agentenregeln, CI-Strukturprüfung sowie ein **lokales, nicht destruktives Audit- und Migrationsskript**. Es enthält keine kopierten Bücher, PDFs, Website-Assets oder fremde Medien. Die vorhandene `LICENSE` wird **nicht** überschrieben.

## Unter Windows (PowerShell)

1. ZIP **außerhalb** des STEPS-Repositories entpacken, z. B. nach `C:\Temp\STEPS-Reorganisation`.
2. Powershell öffnen und den Pfad zur vorhandenen lokalen Git-Arbeitskopie übergeben:

```powershell
python "C:\Temp\STEPS-Reorganisation\bootstrap_steps.py" --repo "C:\Users\Timvo\OneDrive\Github\steps" --audit
```

3. `reports/summary.json`, `inventory.json`, `exact_duplicates.csv`, `migration_plan.csv` prüfen. Die CSV listet **für alle getrackten Dateien** außerdem den unverbindlichen `review_candidate_path`; nur `proposed_path` wird automatisiert ausgeführt. Der aktuelle Git-Stand muss sauber sein.
4. Falls die Mappings, Rechte und Verzeichnisnamen passen:

```powershell
python "C:\Temp\STEPS-Reorganisation\bootstrap_steps.py" --repo "C:\Users\Timvo\OneDrive\Github\steps" --apply
cd "C:\Users\Timvo\OneDrive\Github\steps"
python tools/validation/check_structure.py
git status
git add -A
git diff --cached --stat
# nach Sichtprüfung:
git commit -m "refactor: introduce STEPS architecture with preservation-first migration"
git push -u origin refactor/steps-architecture-preservation
```

Der Push erstellt noch keinen Pull Request. Nach dem Push auf GitHub **Compare & pull request** wählen. **Nicht direkt auf `main` arbeiten.**

### Sicherheitsgrenzen

- Die Migration verschiebt nur ausgewählte, textbasierte Projektartefakte. Die große Bibliothek (1.000 historische V6.6-Dateien), fremde PDFs/Downloads, Konkurrenz-Screenshots, Design-Inspirationen und alle potentiellen Duplikate werden **bewusst nicht automatisch gelöscht oder verschoben**.
- Auch ein `git rm` entfernt Inhalte **nicht aus alten öffentlichen Commits**. Wenn Rechte fehlen, ist eine separate History-Rewrite-Strategie mit Backups und abgestimmtem Force-Push erforderlich.
- Exakte SHA-256-Duplikate sind nur physisch identische Kandidaten; historische Versionsunterschiede dürfen nicht zusammengeführt werden. Redundante Pfade sparen beim Löschen nicht automatisch das gleiche Volumen im Git-Objektspeicher.
- Der generierte App- und `src/steps`-Baum enthält erklärende READMEs und **keinen fiktiven ausführbaren Code**. `VERSION` ist ein ausdrücklich deklarierter Platzhalter.
- Die zuvor existierenden Pfadreferenzen in den konsolidierten historischen Dokumenten können durch das Verschieben ungültig werden; der PR braucht einen separaten Link-/Provenienz-Review.

## Paketinhalt

- `STEPS_Zielstruktur.md` – vollständige vorgeschlagene Repository-Architektur.
- `scaffold/` – alle neu vorgeschlagenen strukturierenden Dateien (vollständige Dokumentationen, fünf JSON-Schemas, CI).
- `bootstrap_steps.py` – Audit und ausgewählte `git mv`-Operationen, jeweils mit Hash-/Statuskontrolle.
- `reports/` entsteht erst nach lokalem Audit und enthält quellbasierte Inventare (nicht mit dem ZIP ausgeliefert).

**Keine automatischen Commits, Merges, Löschungen oder History-Rewrites.**

# STEPS – Installations- und Einspielanweisung des Auditpakets V5

## 1. Inhalt und Gültigkeitsbereich

Das Paket enthält neue Dokumentationsdateien in `prompts/`, `docs/project/review/`, `docs/architecture/`, `docs/operations/` sowie eine **inhaltlich ersetzende Fassung** der bereits bestehenden `src/steps-0.00/README.md`. `optional_fix/src/steps/README.md` ist **nur** ein optionaler Architekturvorschlag und darf nicht blind in `src/steps/` übernommen werden. Ein `changes.patch` liegt separat im Paketroot.

Es wurden **keine produktiven Glide-/STEPS-Pythonquellen und keine Tests geändert**. Es gibt keine automatischen Löschungen, Umbenennungen oder Änderungen an Git-Historie. Die mitgelieferte Markdown- und Word-Fassung des Master-Prompts ist als Prüfanweisung zu verstehen, nicht als bereits ausgeführtes Audit.

## 2. Voraussetzungen

- Vor dem Einspielen das lokale STEPS-Checkout sichern und sämtliche bereits vorhandenen uncommitted Änderungen unverändert lassen.
- Nach Möglichkeit auf einem neuen Feature-/Dokumentationsbranch arbeiten, nicht auf `main`.
- Vor jeder Anwendung mit dem aktuellen Remote vergleichen: Das für die Patchdatei verwendete STEPS-Snapshot ist `1fc07e230dc6a2fe92fd6662da43e332d596b376`.
- Die bestehende `src/steps-0.00/README.md` hatte beim Snapshot Git-Blob-SHA `0fcd773d1f4c847fbeac608e4696e487b6450028`. Bei neuerem Inhalt muss der Patch als Konflikt behandelt, nicht erzwungen werden.

## 3. Empfohlene Windows-PowerShell-Einspielung

```powershell
# 1. Repository öffnen und Status prüfen
Set-Location 'C:\Pfad\zu\steps'
git status --short
git fetch origin

git rev-parse HEAD
# Änderungen außerhalb eines eigenen Branches nicht überschreiben

git switch -c docs/antigravity-master-audit-v5

# 2. ZIP in einen getrennten Ordner entpacken (nicht direkt auf das Repo)
# Beispiel: C:\Temp\STEPS_Antigravity_Auditpaket_2026-11-10

# 3. Zuerst nur Diff-Kompatibilität prüfen
$package = 'C:\Temp\STEPS_Antigravity_Auditpaket_2026-11-10'
git apply --check "$package\changes.patch"

# 4. Vor jeder tatsächlichen Anwendung den Patch manuell lesen
Get-Content "$package\changes.patch" -TotalCount 90

# 5. Nur nach erfolgreich kontrolliertem Diff und eigener Freigabe anwenden
git apply "$package\changes.patch"
git status --short
git diff --check
git diff --stat

# 6. Neuer Validator-Lauf: vorhandenes Problem ist noch nicht behoben
python tools/validation/check_structure.py

# 7. Getestete Dokumentänderungen nach Review committen
# git add <explizit geprüfte Dateien>
# git commit -m "docs: document Glide 3.53 baseline and Antigravity audit V5"
# git push -u origin docs/antigravity-master-audit-v5
# Danach manuellen Pull Request anlegen.
```

`git apply --check` ist eine **Kompatibilitätskontrolle**, keine Freigabe durch ChatGPT. Insbesondere bei neuerem STEPS-HEAD nach dem Audit ist manuelles Drei-Wege-/Datei-Diff nötig. `git apply` schreibt produktive Dokumentdateien und darf nicht parallel mit anderen Agenten auf denselben Pfaden erfolgen.

## 4. Erster Antigravity-Aufruf

1. Lokales STEPS-Checkout in Antigravity als Workspace öffnen.
2. Den kompletten Inhalt von `prompts/30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md` kopieren.
3. Der Prompt beginnt im **Read-only-Audit-Modus** und schreibt seine Prüfergebnisse nur in einen gesonderten Output-Ordner außerhalb des Repositorys.
4. Sobald Antigravity einen neuen aktuellen lokalen Git-Snapshot ermittelt hat, die historischen Werte aus dem Prompt **nicht** als aktuelle Tatsache wiederholen.
5. Erst nach nachweislich abgeschlossener Coverage neue Struktur-/Rückbau-Freigaben erteilen.

## 5. Warum `src/steps-0.00` noch nicht automatisch korrigiert wird

Der frühere Strukturcheck schlägt fehl, weil er `src/steps` verlangt. Ein reines Anlegen von `src/steps/README.md` könnte den **Strukturtest** vorübergehend erfüllen, würde aber die wichtige Paketstrukturentscheidung vorwegnehmen und **keine** importierbare STEPS-Engine belegen. Darum ist `optional_fix/` getrennt, und der Audit-Prompt fordert erst eine belastbare ADR-Entscheidung mit Referenz-/Testprüfung.

## 6. Abschluss-Checkliste zur Einspielung

- [ ] `changes.patch` mit `git apply --check` geprüft.
- [ ] Bestehende `src/steps-0.00/README.md` nicht gegen neuere Änderungen überschrieben.
- [ ] Neue Audit- und Promptdateien besitzen keinen bereits existierenden Zielpfad.
- [ ] README und Architekturvermerk unterscheiden Glide-3.53-CI von STEPS-Tests.
- [ ] `git diff --check` erfolgreich und keine unbeabsichtigte Binär-/Historienänderung.
- [ ] Validator-Ergebnis ehrlich dokumentiert; rote Struktur-CI nicht vertuscht.
- [ ] Keine V4-/V1-/Research-/Glide-Archivdateien entfernt.
- [ ] Kein öffentlicher Upload fremder PDFs, Assets oder Secrets durch das Einspielen.
- [ ] Commit/PR nur nach menschlicher Prüfung.

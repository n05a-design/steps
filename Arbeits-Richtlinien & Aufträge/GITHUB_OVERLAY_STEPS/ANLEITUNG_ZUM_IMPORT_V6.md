# Import – V6 ist ein STEPS-Paket, kein Glide-Checkout-Update

## Welcher Ordner wird geöffnet?

**Antigravity-Workspace:** `C:\Users\Timvo\OneDrive\Github\steps`. **Eingebettete Glide-3.53-Quelle:** `C:\Users\Timvo\OneDrive\Github\steps\src\glide-v3.53`. Ursprung `n05a-design/glide-to-do` bleibt unberührt. Kein Import in den separaten `glide-to-do`-Repositoryroot!

Das ZIP enthält unter `01_GITHUB_OVERLAY_STEPS/` ausschließlich neue Pfade relativ zur STEPS-Wurzel. Die zwei anderen Hauptteile (`02_REFERENZEN_NUR_LOKAL/`, `MANIFEST_SHA256.txt`, Einspielanleitung) sind *nicht* automatisch für öffentliches GitHub bestimmt. In `02_REFERENZEN_NUR_LOKAL/` liegen Originalanhänge und die historische V1-ZIP als Prüfmaterial; dort können absolute lokale Windows-Pfade und ungesichtete Quellenbezüge vorkommen.

## Sicherer Ablauf unter Windows (Beispiele, keine bereits ausgeführten Aktionen)

1. ZIP **außerhalb** des Repos entpacken, z. B. `C:\Temp\STEPS-Antigravity-V6`. Nichts vorher nach `src/glide-v3.53` kopieren.
2. In PowerShell `Set-Location 'C:\Users\Timvo\OneDrive\Github\steps'`, `git rev-parse --show-toplevel`, `git rev-parse HEAD`, `git status --short` – Ergebnis dokumentieren. Falls `git status` ungeklärte Änderungen zeigt, nicht überschreiben.
3. Im entpackten `01_GITHUB_OVERLAY_STEPS/` nur neue Zusatzdateien gegen vorhandene Namen prüfen. Keine automatische Gesamtüberschreibung. Vorläufige Dokumente in einem separaten Branch nach Sichtprüfung hinzufügen; nicht `main` ändern, keine automatischen PR/Pushs.
4. **Zuerst** `docs/project/antigravity-handover/00_START_IN_ANTIGRAVITY.md` und `prompts/32_STEPS_ANTIGRAVITY_MASTER_AUDIT_V6.md` für Antigravity benutzen. Beigefügte Original-Anhänge der lokalen Sitzung verfügbar machen, aber private/lizenzgeschützte Daten nicht unkontrolliert ins öffentliche Repo hochladen.
5. `OUTPUT_REGISTER.csv`, `SOURCE_COVERAGE.csv`, `STATE.json`, `NEXT_SESSION_HANDOVER.md` werden zur **Laufzeit** in einem neuen externen Auditordner angelegt. Die Templates unter `docs/project/antigravity-handover/` sind Vorschläge und keine schon gelaufene Auditreihe.
6. Nach Review und ausdrücklicher Genehmigung kuratierte Auditoutputs in STEPS projektintern übernehmen. Git-Änderungen nur auf STEPS-Branch, `src/glide-v3.53` als eingefrorene Quelle behandeln.

## Verifikation

`MANIFEST_SHA256.txt` enthält die SHA-256-Werte aller Paketdateien (außer dem Manifest selbst). Hashprüfung vor Import nach `Get-FileHash`. Der Hash besagt Byteintegrität, **nicht** Urheberschaft, Lizenzstatus oder tatsächliche Programmfunktion. Aus dem Upload abgeleitete Inhalte im Referenzordner sind nur für lokale Prüfung, nicht als für die Veröffentlichung autorisiert markiert.

## Grenzen der aktuellen Arbeit

Kein lokaler STEPS-Build, kein Upstream-vs-Copy-Komplettdiff, keine Ausführung der 30 Shell-Tests, keine Prüfung aller PDF/MIDI/HTML/Assets, keine vollständige Historienindexierung, kein GitHub-Push. Diese Aufgaben stehen im Masterprompt und der Requirements-Matrix mit expliziten Gates.

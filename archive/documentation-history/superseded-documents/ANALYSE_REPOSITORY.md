# STEPS – Verifiziertes Bestandsaudit und Migrationskonzept

**Quelle:** GitHub-Repository [`n05a-design/steps`](https://github.com/n05a-design/steps), `main`-Commit [`b42a990681ce5fd12c7756fb2ada962e01474521`](https://github.com/n05a-design/steps/commit/b42a990681ce5fd12c7756fb2ada962e01474521), geprüft am 10.11.2026. Auf dem verbundenen Konto sind `pull: true` und `push: false` ausgewiesen. **Keine Änderungen am Remote erfolgt.**

## Quantitatives Inventar

- 2.043 Git-Tree-Einträge (1.827 Dateien, 216 Verzeichnisse).
- Summe der unkomprimierten Dateiinhalte im HEAD: ca. **673 MB** (kein Git-Pack-/Transfermaß).
- **160 Gruppen** identischer Git-Blob-Inhalte; **426 zusätzliche identische Dateipfade**; ca. **115,7 MB** zusätzliche logische Kopien. Git kann identische Objekte bereits intern deduplizieren. Das Entfernen identischer Pfade spart deshalb nicht notwendigerweise 115,7 MB Repository-Objektspeicher.
- 60 PDFs mit zusammen ca. **452 MB**. Viele sind Fremdwerke und benötigen ein Rechteaudit. Eine bereits veröffentlichte Datei bleibt auch nach `git rm` in früheren Commits erreichbar.

| Wurzelbereich | Dateien | Unkomprimierte MB | Audit-Einschätzung |
| --- | ---: | ---: | --- |
| `00_Arbeitsvorbereitung` | 720 | 590,53 | Größtes Risiko: Fremd-PDFs, HTML-Caches, Webassets, Drum-/Ableton-Daten; konservieren, Rechte prüfen |
| `01_Projektkonsolidierung` | 10 | 0,30 | Gezielte Migration nach `docs/project/`, alle Originaltexte erhalten |
| `02_Bibliothek` | 1.026 | 60,36 | V6.6/V6.7-Legacy, ca. 1.000 Dateien unter V6.6-Themenbaum; Inventar-/Linkreview erforderlich |
| `03_Konkurrenz` | 47 | 11,54 | Fremde Wettbewerber-Screenshots und HTML, teils bitidentisch mit `00_Arbeitsvorbereitung` |
| `20_Grafik_Master` | 21 | 9,83 | UI-Inspiration; Herkunft und Assets prüfen |
| Wurzeldateien | 3 | 0,02 | `README.md`, `.gitignore`, `LICENSE` |

## Einzelfunde

1. Die Root-README besteht aus zwei kurzen Zeilen; `&amp;` ist HTML-escaped. Der neue Entwurf trennt Produkt-/Archivstatus und enthält DE/EN-Grundinformationen.
2. Eine vollständige **MPL-2.0-Lizenz** ist bereits vorhanden. Sie kann nicht pauschal auf PDF-Bücher, Screenshots, Webarchive und Musik-/MIDI-Fremdmaterial übertragen werden.
3. In `01_Projektkonsolidierung/README.md` ist von **sechs Originalen** die Rede. Tatsächlich liegen in `04_Originaldokumente/` nur **fünf Markdown-Dateien**. Im aktuellen Git-Baum fehlt speziell `Glide Kontext für Fable(2).md`, obwohl es als Quelle C genannt wird. Fehlenden Beleg separat nachreichen oder kenntlich machen.
4. Die Bibliotheks-README dokumentiert **49 Hauptordner** (teils aus Screenshots abgeleitet), die tatsächliche V6.6-Fachablage enthält unter anderem zwei `21_*`- und zwei `39_*`-Bereiche. Diese Konflikte benötigen inhaltlichen Abgleich; kein pauschales Zusammenlegen.
5. Das Repository enthält **keine** im aktuellen HEAD nachgewiesene App-Implementierung unter `app/` oder `steps/`. Es sind eigene Quellen zu Musiktheorie, Datenmodellen, historischen Python-Generatoren und Skill-Vorarbeiten vorhanden. Keine App-/Testfreigabe aus der Bibliotheksversion V6.7 ableiten.
6. Ein einzelnes PDF ist rund **52,93 MB** groß (`Fundamentals of Music Proce_ (Z-Library).pdf`); weitere Bücher liegen bei ca. 51,58 MB, 47,49 MB, 37,90 MB. Das ist sowohl ein Rechts- als auch Repository-Größenproblem. Die Herkunft der Dateien ist zunächst nur über Dateinamen erkennbar, nicht rechtlich bewertet.
7. Wiederkehrende Dateien innerhalb der gespeicherten Ableton-Webseiten (`*.js.download`, `ns.html`, `*.css`) sind vielfach identisch. Auch Dateien aus `00_Arbeitsvorbereitung/Dokumentation (unsortiert)` tauchen identisch unter `02_Bibliothek/STEPS_Bibliothek` oder `03_Konkurrenz` auf.
8. Die README der Projektkonsolidierung sagt ausdrücklich, dass die konsolidierten Originalaussagen **nicht vollständig extern verifiziert** wurden. Die hier vorgenommene Git-Inventur belegt nur den aktuellen Baum, nicht alle Behauptungen über Funktionalität, Vollständigkeit und Validierung.

## Architekturentscheidung als Vorschlag

- **`src/steps/`** statt zwei paralleler Domain-Engines unter `app/theory` und `steps/`: künftig kanonisches Importpaket für reine Musiklogik.
- **`app/`** für Desktop-Einstieg, GUI, Lebenszyklus und Port-Adapter. In der gelieferten Baseline nur Dokumentationsplatzhalter; kein erfundener lauffähiger `__main__.py`.
- **`knowledge/`** für mit Quellen-IDs gesicherte Fachkonzepte und maschinenlesbare Kontrakte, **`research/`** für Forschungsdiskurs, Marktbegleiter und außerhalb des MVP liegende Produktion.
- **`design/`** als zusätzlicher Hauptbereich, da im Repository echte UI-/Design-Inspiration liegt.
- **`skills/`** zusätzlich zu Root-`SKILL.md`, damit der vorhandene Harmony-Coach-Entwurf seinen eigenen Dokument- und Asset-Scope behält.
- **`docs/project/`** für die überprüfbare Migration der historischen Konsolidierung.
- **`decisions/`, `schemas/`, `tests/`, `tools/`** als auditierbare Governance-, Daten- und Prüfstruktur.

## Umsetzung des mitgelieferten Tools

`bootstrap_steps.py --audit` liest alle **lokal getrackten Dateien**, berechnet SHA-256 und schreibt `inventory.json`, `migration_plan.csv`, `exact_duplicates.csv` und `summary.json` **außerhalb** des Repos. Der `review_candidate_path` in der Bestandsliste ist für alle nicht migrierten Dateien lediglich ein **Vorschlag**, kein automatischer Move oder Rechtsnachweis. `--apply` erfordert einen sauberen Stand auf `main` und den genannten Base-SHA (abweichende Stände nur mit `--allow-newer` nach Review). Der Modus legt einen neuen Branch an, migriert ausgewählte **kleine Text-/Projektartefakte** per `git mv`, verifiziert Content-Hashes und fügt das Struktur-Scaffold hinzu. Änderungen werden nicht automatisch committed oder gepusht.

### Separat und zwingend nachgelagert

- Rechte und gegebenenfalls Git-Historie (separater Backup-/Rewrite-Prozess).
- Prüfen relativer Links, CSV-Registerpfade, JSON-Manifeste und konsolidierter SHA256SUMS auf alte Pfade.
- Eigenständige V6.6/V6.7-Fachmigration nur nach vollständigem Provenienz- und Versionsabgleich.
- Fachliche Tests und App-Code erst nach der Schema-/Modellfreigabe.

**Ergebnisstatus:** Architektur und konservative Migration lokal vorbereitet, **GitHub-Repository unverändert**.

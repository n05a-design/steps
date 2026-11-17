# STEPS – Git-Historien- und Lizenzfolgen-Audit (Phase P0.1 / Prompt 27)

- **Stand:** 17.11.2026 (Europe/Berlin)
- **Status:** Vollständiger Auditbericht zur Repository-Historie, Fork-Lage und MPL-2.0-Rechtsgrenzen
- **Geprüfter Commit:** HEAD (`autonomous_backlog_execution` auf `d717cec`, Remote `origin/main`)
- **Referenz-Commits:** `75329fef` (Initialer Audit-Snapshot), `a14c3f3` (Upload der 40 PDFs am 10.11.2026), `37e691b` (Entfernung des Glide-Prototyps am 10.11.2026), PR #63 (Docling-Extrakte am 14.11.2026)

---

## 1. Einordnung der Mozilla Public License 2.0 (MPL-2.0)

Das Repository `n05a-design/steps` führt die Datei `LICENSE` unter der **Mozilla Public License Version 2.0 (MPL-2.0)**.
Aus der Existenz der Root-Lizenzdatei folgt jedoch **keine** automatische Freigabe für alle darin abgelegten Fremd-Binärdaten:

1. **File-Level Copyleft:** Gemäß Ziffer 1.7 („Larger Work“) und Ziffer 3.1 („Availability of Source“) der MPL-2.0 gilt das Copyleft ausschließlich für „Covered Software“ – d. h. Quellcodedateien, die unter MPL lizenziert wurden oder Modifikationen daran darstellen.
2. **Keine Befreiung fremder Werke:** Fremde PDF-Lehrbücher, Notenscans, geschützte Audioaufnahmen oder fremde Web-Caches werden durch die bloße Ablage in einem MPL-2.0-Repository rechtlich **weder** zu freier Software noch gemeinfrei. Die MPL-FAQ von Mozilla stellt dies explizit klar: Eine Lizenzierung erfordert die wirksame Einräumung von Nutzungsrechten durch den jeweiligen Urheber.
3. **Schlussfolgerung:** Das STEPS-Projekt unterscheidet strikt zwischen:
   - Eignem Code (`src/steps/`, `app/`): MPL-2.0.
   - Fremden Dokumenten (`research/`, `archive/`): Individuelle Rechteklassen A bis E.

---

## 2. Historische Git-Commits und Blob-Präsenz

### 2.1 Git-Objektmodell und Persistenz
In Git ist jeder Commit ein unveränderlicher Snapshot eines Baumobjekts (`tree`). Wird eine Datei im aktuellen Arbeitsverzeichnis oder per `.gitignore` gelöscht/ausgeschlossen (wie am 14.11.2026 für die 10 Werke der Rechteklasse E umgesetzt), verbleiben die zugrundeliegenden Blob-Objekte in allen früheren Commits der Git-Objektdatenbank (`.git/objects/`).

### 2.2 Relevante historische Meilensteine:
- **10.11.2026 (`a14c3f3`):** Ursprünglicher Commit der 40 Forschungs-PDFs (inkl. der 10 Klasse-E-Werke) in den Pfad `research/STEPS_Bibliothek/`.
- **10.11.2026 (`37e691b`):** Bereinigung des früheren Glide-Prototypbestands (1.580 Dateien entfernt).
- **14.11.2026 (PR #63 / `9c7b8eb`):** Hinzufügung der Docling-Markdown-Extrakte (`.md`) und Web-Caches.
- **14.11.2026 (Inhaberentscheidung):** Ausschluss aller 10 Werke der Rechteklasse E (13 Dateipfade, 26 Dateien inkl. Extrakten) aus dem Working Tree per `.gitignore` und Ersetzung durch eigene Zusammenfassungen (`research/STEPS_Bibliothek/Zusammenfassungen/`).

---

## 3. GitHub History Rewriting Guidance & Fork-Risiko-Bewertung

### 3.1 Risiken eines Force-Push / History-Rewrites (`git filter-repo` / `bfg`)
GitHub dokumentiert in seinen Sicherheitsrichtlinien (*Removing sensitive data from a repository*), dass das Umschreiben der Git-Historie gravierende Seiteneffekte hat:
- **Zerstörung aller SHA-Referenzen:** Jeder Commit erhält einen neuen SHA-1 / SHA-256 Hash. Sämtliche in `docs/`, `manifests/` und Prüfberichten dokumentierten Hash-Ketten und Audit-Nachweise würden ungültig.
- **Bruch offener Pull Requests:** Alle bestehenden Branches und PRs basieren auf den historischen Commits und können nicht mehr sauber gemergt werden.
- **Kollision mit Synchronisationspfaden (OneDrive):** Da die lokale Entwicklungsumgebung teils über geteilte Verzeichnisse synchronisiert wird, führt ein Force-Push zu massiven Dateikonflikten und Index-Korruptionen (`index (<Datum>)`).
- **Forks und Caches:** Ein History-Rewrite im Upstream-Repository entfernt Blobs nicht automatisch aus existierenden Forks oder lokalen Klonen anderer Mitwirkender.

### 3.2 Explizite Entscheidung des Inhabers (14.11.2026 & 16.11.2026)
Der Projektinhaber hat die Risiken abgewogen und folgende **verbindliche Richtlinie** festgelegt:
1. **Kein Force-Push und kein History-Rewrite:** Die historische Commit-Historie bleibt unberührt, um die wissenschaftliche und forensische Nachvollziehbarkeit aller Audit-Schritte (Preservation-First) zu gewährleisten.
2. **Arbeitshygienische Isolation im HEAD:** Der aktuelle `main`-Zweig und künftige Releases enthalten im Arbeitsbaum **keine** urheberrechtlich geschützten Volltexte (Klasse E) mehr.
3. **Müller / Z-Library:** Die Herkunft der Forschungsdatei wird transparent dokumentiert; es erfolgt keine weitere Verfolgung oder Anschaffung, sondern die Arbeit stützt sich auf die eigens erstellte Zusammenfassung.

---

## 4. Release- und Distributionsgrenzen

Für die Veröffentlichung von STEPS (Phase 5 MVP v0.1) gelten folgende strikte Grenzen:
- **PyPI / Quellcode-Release (`steps`):** Enthält ausschließlich `src/steps/`, `pyproject.toml`, `README.md` und `LICENSE`. Keinerlei Research-PDFs, keine Web-Caches, keine fremden MIDI-Dateien.
- **Desktop-App Bundle (PyInstaller):** Enthält die UI-Shell (`app/`), pure Musiktheorie (`src/steps/`), eigene Brand-Assets (`app/assets/brand/`) und kuratierte, validierte Daten (`knowledge/concepts/`).
- **Research Archive:** Verbleibt als Entwicklungs- und Dokumentationsbereich im Git-Quellbaum unter strikter Einhaltung der Rechteklassen A–D; Klasse E bleibt lokal per `.gitignore` gesperrt.

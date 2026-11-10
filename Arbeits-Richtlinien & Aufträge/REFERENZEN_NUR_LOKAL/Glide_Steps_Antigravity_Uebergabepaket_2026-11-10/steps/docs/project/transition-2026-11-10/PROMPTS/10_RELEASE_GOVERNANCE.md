# P10 – GitHub-Governance, Lizenz und Releasemodell

## Direkt nutzbarer Prompt

Du koordinierst die Governance zweier **getrennter** MPL-2.0-Repositories: Glide (bestehendes Produkt) und Steps (in Entwicklung). Basis sind aktuelle `LICENSE`, `AGENTS.md`, Sicherheits-/Lizenztexte, die Glide-MPL-Provenienz, das V3-Rights-Audit und native Build-/CI-Nachweise. Vor jeglicher Release-/Write-Operation den Repo-Owner und die Berechtigung prüfen; hier wurde ursprünglich nur `pull:true`, `push:false` nachgewiesen.

Erstelle eine **read-only Release-/Contribution-Checkliste**: `main`-Schutz durch Pull Requests, erforderliche Statuschecks, reviews, keine Force-Push-/History-Änderungen, Commit-SHA pro Release, signierte Artefakte falls beschlossen, OS-Matrix, SBOM, Third-Party-Lizenzen, Soundfont/Samples/Rechercheinhalte, Source-Download, Datenschutzhinweise, Vulnerability-/Incident-Prozess, Versionen und Migrationspfade. Die MPL erlaubt Weitergabe/Forks nach Lizenz; ein technisches Framework kann keine exklusive Kontrolle über fremde Forks versprechen. Marke, Copyright und Drittmaterial separat behandeln.

Teile Steps-Status nach Dokumentation / Engineering / Produkt-Release. Definiere `app_version`, Save-/Domain-Schema, Knowledge-/Skill-Release und getrackten Glide-Source-SHA unabhängig. Keine automatisch erhöhte Produktversion, weil Dokumente geändert wurden. Lege für Fremd-PDFs/Webarchive/MIDI oder Sampleresourcen den Status `review_required` fest, bis konkrete Nutzungsrechte belegt sind; beurteilt Rechte nicht allein aus Dateinamen.

Falls Zugriffe bestehen und der Owner freigibt, technische Änderungen in einem PR mit diff/CI vorbereiten. Andernfalls nur Vorschlag/Anleitung, keine Behauptung geänderter GitHub-Einstellungen oder veröffentlichter Artefakte.

## Akzeptanz

Nachweisbare Reviewer-/Merge-/Release-Regeln, dokumentierte Drei-Gate-Freigabe, eindeutige Versionsachsen, transparente Assets-/Rights-Matrix und keine unbelegte rechtliche oder Produktfreigabe.

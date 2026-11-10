# Konservative Migration – zwei Stufen

## Stufe 1: Baseline (automatisiert, reversibel)

- Prüft **sauberes Working Tree, Repository-Remote und Referenz-Commit**; legt separaten Branch an.
- Erstellt vollständige, kommentierte Zielstruktur samt Doku, CI-Strukturcheck, JSON-Schemata und leeren Fachplatzhaltern.
- Verschiebt ausschließlich ausgewählte *bereits vorhandene eigene Projekttexte*: Projektkonsolidierung, Deep-Research-Paket, Harmony-Skill-Entwurf, Bibliothek-README und historische V6.7-Generatoren.
- Behält `LICENSE` unverändert; bewahrt die alte Root-README separat auf.
- Verändert `00_Arbeitsvorbereitung` (sonst), das große `02_Bibliothek`-Archiv, `03_Konkurrenz`, `20_Grafik_Master` **nicht** automatisch.
- Protokolliert alte/neue Pfade und SHA-256; keine automatische Deduplizierung, keine Änderungen an Git-Historie.
- Prüft nach der Migration Dateihashes und Dateianzahlen; anschließend sind referenzielle Link-/Indexkorrekturen separat erforderlich.

## Stufe 2: Fachliches Review (nicht automatisch)

- Bibliothek V6.6/V6.7 inklusive History/Gaps/Indizes thematisch zuordnen und versionierte Primärquelle für Konzepte festlegen.
- 426 SHA-identische zusätzliche Pfade als mögliche, nicht zwingend löschbare Duplikate prüfen. Verweise und Provenienz vorher aktualisieren.
- Volltexte, Website-Caches, Bilder, Musik-/MIDI-Material rechtlich bewerten; fremde Medien nicht einfach nach `knowledge/sources/raw` in Git verschieben.
- Öffentliche Git-Historie gesondert auf potenziell unzulässige Inhalte prüfen. Aktuelles Löschen entfernt die Commits nicht.
- Historische Quellregister, Links und Zählungen nach Änderung abgleichen. Fehlende sechste Originalquelle der Konsolidierung untersuchen.
- App-Code, Tests und Packaging erst nach geklärtem Scope und Datenkontrakten implementieren.

## Einmalig lokal ausführen

Das Begleitpaket enthält `bootstrap_steps.py`. Paket **neben** und nicht **in** das vorhandene Repo entpacken. Zuerst `python bootstrap_steps.py --repo C:\...\steps --audit`; dann erst `--apply` für die in der Konsolenausgabe aufgeführten kontrollierten Änderungen. Anschließend `git status`, `git diff --stat` und Strukturcheck prüfen, committen und Branch pushen. `main` bleibt unverändert, solange kein PR gemergt wird.

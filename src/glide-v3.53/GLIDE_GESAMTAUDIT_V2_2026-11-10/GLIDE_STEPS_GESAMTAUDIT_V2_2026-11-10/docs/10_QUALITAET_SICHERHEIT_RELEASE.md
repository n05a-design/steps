# 10 — QA, Release, Performance, Sicherheit und echte Nutzbarkeit

## Testzustände nicht zusammenziehen

**Glide:** `VERSION=3.53.0` auf `main` ist am SHA nachgewiesen. Dokumentierter lokaler Windows-Volltest: 130/131 Schritte, separate Bildsichtung übersprungen; `release_ready=false` im archivierten QA-Bericht. GitHub-Actions-Snapshot: `Glide-Prüfung` für Main SHA `9e767bea...` zum Abrufzeitpunkt noch `in_progress`, macOS-arm64-Paketjob `success`. Ein anderslaufender Job auf dem alten Branch kann nicht als zusätzliche Bestätigung für den Main-SHA addiert werden. Erfolgreiches Packaging allein ≠ native UI-Vollmatrix ≠ menschliche Abnahme ≠ veröffentlichtes Release.

**Steps:** einzige nachgewiesene standardmäßige GitHub-CI `Repository structure` am SHA `75329fef...` erfolgreich. Das Codeziel `tools/validation/check_structure.py` prüft Verzeichnisse, Pflichtdateien und parsebare JSON-Schemas mit nichtleeren Required-Arrays. Es prüft nicht MIDI, musikalische Korrektheit, Runtime, GUI-Rendering, Datensicherheit, Rechtskonformität oder Packagebildung.

## Risikobasierte Testpyramide

| Ebene | Solltests | Nicht ersetzbar durch |
|---|---|---|
| Static/Contract | AST-Importgraph, `src/steps` ohne Tk/Glide, gesetzte Produkt-/Source-IDs, JSON-Schema, Lizenz-/Asset-Check, Linkprüfer | erfolgreichen App-Start |
| Unit | Musiknote/Tonart/Enharmonik/Duration/Tick, Sidebar-Zustandsautomat, Theme-Resolver, Settings/Undo pure functions | Snapshot-Ästhetik |
| Integration | Shell + CommandRegistry + App-DataAdapter, Undo/Save/Restart, FileLock/AtomicCommit, MIDI-Parser/-Writer, Skill-Registry-Crossref | einzelne Unit-Tests |
| UI/Accessibility | realer Tk-Root und Widget-Lifecycle, 2 Flächen, Key-only, Focus, Hover/Selected, Scale, Screenreader begrenzt | Testinfrastruktur ohne echte Widgets |
| Daten/Migration | Version alt→neu, unvollständige Schreiboperation, Recovery/Backup/Restore, vollständige Datensätze und Assets | `json.loads` |
| Performance | Start, Memory/Callbacks/Widget counts, Render/Suche/Save auf identischem synthetischem Bestand; median/p95, Vorher-/Nachher | isolierter schneller Einzellauf |
| Plattform | Win/macOS/Linux, Python/Tk-Build, DnD/Fonts/Icon/Titlebar, Full-screen/DPI/Mehrmonitor | gehostete CI eines anderen Betriebssystems |
| Packaging/Release | Source zu Artefakt SHA/Commit, Build reproducibility, SBOM/Lizenz, nativer Start, Offlinebetrieb, Nutzerabnahme | erfolgreicher Zip-/Wheel-Bau |

## Getrennte Gates: keine falsche Blockierung

- **F0 `BASELINE_SELECTED`**: verifizierter Git-SHA, dokumentierte Checks/Gaps, saubere isolierte Arbeitskopie und keine echten Nutzerdaten. Genügt für read-only Analyse, Stub-/Prototyp-Spikes und experimentelle Shell in Steps-Branch.
- **F1 `CORE_EXTRACTION_CANDIDATE`**: System-/Domain-Abhängigkeiten verstanden, ausgewählter Port mit negativen Tests, lokaler Glide-/Steps-Integrationslauf am dokumentierten SHA. Genügt nur für Draft-PR und weitere kontrollierte Entwicklung.
- **F2 `SHARED_CORE_APPROVED`**: eindeutige Public API, Version, Backward Compat und zwei reale Consumer; keine kritische Regression, Lizenz/BOM, OS-Matrix für gewählte Komponenten und Datenisolation.
- **F3 `PRODUCT_RELEASE_APPROVED`**: jeweilige Produkt-Testmatrix und Packaging-/menschliche Freigaben mit identischem Commit und Buildhash. Eine Freigabe in Glide ist nicht automatisch eine Freigabe in Steps.

## Technische Fehler und Security-Threat-Model

**T1 Cross-Product Data Corruption:** Gleiches Dateinamen-/Settings-/Lockschema oder unbeabsichtigter Import von Glide-Pfaden kann echte Nutzerdaten öffnen. *Test:* injizierter RuntimeRoot, Guard-Sentinel für fremde Pfade, Modul-Import ohne Seitenwirkungen, zweite Instanz simulieren.

**T2 Save/Undo-Split Brain:** UI schreibt direkt, Undo verändert Modell ohne Save, oder Cache/Views behalten alte Objektinstanzen. *Test:* alle Mutationseinstiege über denselben transaktionalen Apply/Undo/Persistenzport, ID-stabile Projektion, Fault Injection vor/nach `os.replace`.

**T3 Tk-Memory-/Callback Leak:** ausgetauschte Slot-Views behalten `.after`-Callbacks, Bild-/Menüobjekte oder Eventbindings; Blockieren des Eventloops. *Test:* 100 Wechsel, Root vor Worker-Ende zerstören, `after_info`/Widget-/Handle-Abgleich, keine Worker-Tk-Aufrufe.

**T4 Untrusted Source/Archive:** externe ZIP-, HTML-, MusicXML-/MIDI-/JSON-Inputs können Traversal, unvollständige oder riesige Daten, Symlink/Pfadüberschreitung, unzulässige ZIP-Verhältnisse oder bösartige Metadaten enthalten. *Test:* Pfadnormalisierung, maximale Bytes/Tiefe/Objektzahl, no code execution, read-only parse/explicit confirm, CPU-/Deadline-Budget.

**T5 External Assets & Supply Chain:** Schriften, Icons, native DLLs, MIDI-Libraries und Dokumentenassets benötigen Herkunft/Hashes/Lizenzen; Bibliotheksdateien dürfen nicht einfach in einen Installer. *Test:* SBOM, Manifest, allowed files, Installer start ohne Netzwerk.

**T6 Incomplete QA / Performance Regression:** schwankende Bild-/Kartenrender-Tempos bei neuen Fonts, OS-Unterschiede und eine rote historische Gegenprobe. *Test:* identische Umgebung/Eingaben, aufgewärmte Paare, vorab definierte Grenze, 5+ Messungen und p95, Rotfälle nicht durch Wiederholen bis Grün wegwischen.

**T7 Public Privacy:** Logs/Screenshots/README-Setup-Pfade enthalten möglicherweise lokale Benutzernamen; AI-Tools geben private Pfade oder Forschungsoriginale aus. *Test:* Review-Check auf absolute Home-/OneDrive-Pfade, Token/Keys, Quelltext-Vollzitate und versteckte Dokumentreferenzen.

## Desktop-Shell Pflichtmatrix

Ein Einstieg auf Windows, Linux und Mac wird nur dann positiv ausgewertet, wenn die **betreffende** Plattform plus Python-/Tcl-/Tk-Version, Bildschirmmodus und App/Core-/Design-SHA erfasst sind. Jede Plattform braucht: `launch`, `sidebar visible/collapsed/hidden`, `2 views attach/replace/close`, `focus/escape`, `theme/font`, `save/settings/restart`, `exit during async action`, `no data folder crossover`, `small/large window`. Accessibility: alle Buttons namentlich ansteuerbar, Key-only-Workflow und Screenreader-Reichweite pro OS. Mindestfenster 860x700 / 480x560 sind vorhandene Glide-Policy-Werte und dürfen **nicht** still zu Steps-Produktmaßen werden.

## Testdatensicherheit

Automatisierte Tests nur in eigenem Tempdir; für Glide vor Import `GLIDE_DATA_DIR` setzen. Für Steps eigener injizierter Testroot, dessen Zuverlässigkeit vor jeder Testausführung verifiziert wird. Kein Import der echten Nutzerdaten aus Home/OneDrive, keine Breakpoint-Logs mit privaten Pfaden, keine unkontrollierten Testläufe im produktiven Repository. Fault Injection benutzt künstliche Snapshots und keine echten Dateisystemlocks.

## Lieferung und Freigabe als Achsen

Dokumentation `DRAFT / REVIEWED / APPROVED`; Source `COMMITTED`; Prüfstand `UNIT / INTEGRATION / NATIVE / HUMAN`; App-Version und Schema-Version; gebaute Artefakte SHA/BOM; Release `UNPUBLISHED / RC / APPROVED`. Diese Felder separat halten. Wer auf Mac ein Paket bauen kann, hat nicht automatisch den auf der gleichen Device-/Tk-Kombination getesteten UI-Status. Historische Gleiche-Branchnamen helfen nicht: Commit-SHA muss gleich sein.

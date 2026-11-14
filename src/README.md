# Quellcode und technische Referenzen

| Ordner | Rolle im Checkout |
| --- | --- |
| [steps](steps/README.md) | Aktiver Python-Kern für Theorie, Progressionen und kuratiertes Lernmaterial. |
| [steps-0.00](steps-0.00/README.md) | Dokumentarisches Scaffold aus der frühen Planung. |
| [glide-v3.53](glide-v3.53/README.md) | Versionierter Glide-Referenzstand mit eigener Lizenz und Dokumentation. |

Die [App-Schicht](../app/README.md) bindet Pilotbeispiele über einen Adapter
an. Der [Implementierungsstand](../docs/IMPLEMENTATION.md) beschreibt die
heutigen Funktionen und Laufzeitgrenzen. Der
[Glide-Reuse-Index](../docs/system_reuse/README.md) führt Herkunft und
Nachweise zur möglichen technischen Übernahme.

<details>
<summary>Historische Ausgangsdokumentation vom 10. November 2026</summary>

# STEPS 0.00 – Entwicklungs- und Übergabebereich

> Der [Implementierungsstand](../docs/IMPLEMENTATION.md) und die [generierte API-Referenz](../docs/theory/API.md) beschreiben den Code dieses Checkouts. Der folgende Text dokumentiert den Entwicklungsstand vom 10. November 2026.

**Projekt:** STEPS – eigenständige Musik-/Harmonieanwendung
**Status:** Vorbereitung und fachliche Zielarchitektur, **keine als funktionsfähig nachgewiesene STEPS-App**
**Dokumentationsstand:** 10.11.2026
**Ursprünglicher Verzeichnispfad:** `src/steps-0.00/` (zum dokumentierten Git-Snapshot vorhanden)
**Referenz-STEPS-Commit:** `1fc07e230dc6a2fe92fd6662da43e332d596b376`
**Glide-Referenz:** `n05a-design/glide-to-do@9e767bea5e21063466a28ac3a679406484ad5d5f`, App **3.53.0**.

## Verbindliche Richtung: Glide 3.53.0 → neutrales Grundgerüst → STEPS

Die Projektverantwortlichen haben die Richtung festgelegt: Der mit erfolgreicher CI geprüfte Glide-Stand **3.53.0** wird als technische Baseline genutzt. Auf einer **separaten STEPS-Arbeitskopie** werden die vorhandenen, für STEPS geeigneten Grundfunktionen kontrolliert herausgelöst beziehungsweise die Glide-Fachfunktionen aus der vorgesehenen Shell entfernt oder neutralisiert. Aus dem erhaltenen, entkoppelten GUI-/Infrastruktur-Fundament entsteht anschließend eine **eigenständige STEPS-Anwendung**.

Das bedeutet **nicht**, dass Glide als Task-Manager lediglich umbenannt wird. Die STEPS-Domäne (Akkorde, musikalische Ereignisse, Akkordfolgen, musiktheoretische Analyse, Timeline, MIDI/Drums) besitzt eigene Modelle, eigene Dateien und eigene Tests. Die bisherigen Glide-Aufgaben, -Listen, -Nutzerdaten, -Pfade, -Locks, -Caches und -Taskaktionen werden **nicht** ohne explizite Migrationsentscheidung übernommen.

Die genauen technischen Rückbauschritte müssen noch nach vollständigem Modulinventar, Abhängigkeitsanalyse, Lizenz-/Assetprüfung und vergleichbaren Shell-Tests freigegeben werden. Die Entscheidung für die Glide-3.53.0-*Ausgangsbasis* ist verbindlich; ihre sichere technische Umsetzung wird erst geplant und verifiziert.

## Quellenabgrenzung und Projektpfade

| Ort | Rolle | Status |
|---|---|---|
| `src/glide-v3.53/` | Lokale Aufnahme des Glide-3.53-Quell- und Dokumentationsbestands als Referenz / Rückbauquelle | **Quellbestand, keine STEPS-Implementierung** |
| `source_archive/` | Historische Glide-Appkopie und Forschungs-/Doku-Originale | Archiv-/Provenienzbestand |
| `src/steps-0.00/` | Dieser STEPS-Entwurfs- und Übergabebereich | Dokumentarisches Scaffold |
| `app/` | Geplante Desktop-App-Shell, Entry Point, UI, Adapter, Audio | Bisher als Scaffold dokumentiert |
| `knowledge/`, `schemas/`, `research/` | Fachwissen, Datenkontrakte und Forschungsquellen | Unterschiedliche Reifegrade; nicht mit Produkt-Implementierung gleichsetzen |
| `tests/` | Zukünftige Fach-, UI- und Integrationstests | Keine abgeleitete STEPS-Freigabe aus Glide-CI |

**Verwechslung vermeiden:** `Glide 3.53.0` ist eine fertiger geprüfter *Glide*-Referenzstand, kein STEPS-Apprelease. Das STEPS-Root-`VERSION` führte bei der Prüfung `0.0.0-dev`; die historische STEPS-Bibliothek `V6.6/V6.7` ist wiederum keine Appversion.

## Technische Paketbenennung – offene Strukturentscheidung

`src/steps-0.00/` ist als **Versions-/Arbeitsordner** möglich, jedoch kein gültiger normaler Python-Importname wie `steps`: Ein Ausdruck `import steps-0.00` ist nicht gültig. Der importierbare STEPS-Code soll – vorbehaltlich eines separaten Architektur-ADRs – unter einem stabilen Paketpfad `src/steps/` liegen; die Appversion wird unabhängig davon in `pyproject.toml`/`VERSION` oder einem zentralen Versionsvertrag geführt.

**Bekannter Defekt:** Im betrachteten Snapshot verlangt `tools/validation/check_structure.py` das Verzeichnis `src/steps`. Ein früherer STEPS-Workflow `42842449461` schlug mit `Missing required paths: ['src/steps']` fehl. Der neue GitHub-Snapshot wurde nicht mit einem erfolgreichen *Struktur*-Workflow nachgewiesen; ein grüner Dependabot-Lauf ist kein Ersatz. Die passende Architektur muss geprüft werden, bevor der Validator einfach auf den Versionsordner umgestellt wird.

## Erhaltenswerte Shell-Fähigkeiten aus Glide

- Fensterlebenszyklus, Sidebar und Arbeitsbereich, Theme-/Typografie-/Iconsystem, Menüs, Header, Dialoge, Tastatur- und Fokusverhalten, Responsive-/Kompaktmodus, Accessibility und plattformübergreifende GUI-Prüfungen.
- Deterministische, robuste Grundkonzepte für Einstellungen, transaktionales Speichern, Backups, Fehlerbehandlung, Session-Management, atomare Writes und Test-/Packaging-Workflows – nur nach Isolation von Glide-Datenmodellen.
- Neutrale Navigation und Workspace-Container mit sicheren No-op-Status für noch nicht implementierte STEPS-Module; keinerlei versteckte Alt-Glide-Aktion über Suchfeld, Hotkey, Timer oder Sidebar.

Die vorgesehene Start-Shell ist ein Hauptfenster mit zwei Bereichen (Sidebar und Workspace) **als reversible Prototypannahme**. Sollten tatsächlich zwei unabhängige OS-Fenster beabsichtigt sein, wird dafür ein gesonderter ADR benötigt.

## Getrennte Implementierungsschichten

1. **Glide-Reuse-Layer:** Nur explizit vermessene und isolierte Module mit Herkunfts-/Lizenz-/Testnachweis.
2. **STEPS-App-Layer:** Window/Navigation/Workspace/Settings/Adapters, ohne Aufgaben-Fachlogik.
3. **STEPS-Domain-Layer:** UI-unabhängige, testbare Musiklogik für Pitch/Spelling/Intervals/Chords/Progressions/Time; keine Tk-Imports oder Glide-Datendateien.
4. **STEPS-Knowledge-Layer:** Quellenbelegte Concepts/Claims/Rules, nicht ungeprüfte PDFs als Runtime-Wissensspeicher.
5. **Quality/Release-Layer:** Eigene STEPS-Tests; Glide-CI darf nur als externe Baseline referenziert werden.

## Abnahme vor STEPS-Fachimplementierung

- [ ] Glide-3.53.0-Ursprungs-SHA, lokaler kopierter Baum, Module, Assets, Fonts und Tests in einem verifizierten Freeze-Manifest verglichen.
- [ ] Die Wiederverwendungsentscheidung pro Modul ist mit Dependencies, Side Effects, Lizenz, Zielpfad und Regressionstests dokumentiert.
- [ ] Eigener STEPS-Datenroot, Identifier, Lock, Cache, Settings und Backup sind nachweislich von Glide getrennt.
- [ ] Sidebar, Workspace, Theme, Navigation, Suche, Settings und Exit/Recovery funktionieren isoliert, ohne Glide-Taskdaten zu berühren.
- [ ] Python-Paketstruktur und importierbarer Modulname sind getrennt vom Versionsordner entschieden; Struktur-CI ist am aktuellen STEPS-Commit erfolgreich.
- [ ] Mindestens die dokumentierten 30 Shell-Akzeptanzszenarien wurden nachweislich bearbeitet; Skips/Not-Runs nicht als Pass gezählt.
- [ ] Musikmodelle, Quellenbezüge, Dateischemata, fachliche Golden-Tests und Migrationen sind unabhängig von Glide vorbereitet.
- [ ] Rechte-/Assetprüfung und menschliche native Sichtprüfung sind als eigene Freigabegates dokumentiert.

## Verweisbasis

- `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`
- `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`
- `docs/architecture/REUSE_AND_MIGRATION_MATRIX.md`
- `docs/project/PROJECT_OVERVIEW.md`
- `docs/quality/QUALITY_GATES.md`
- `prompts/02_GLIDE_FINISH_FREEZE.md`, `03_GLIDE_AUDIT_REUSE.md`, `04_GLIDE_TO_STEPS_SHELL.md`, `26_GLIDE_SHELL_COMPARE_SPIKES.md`
- Neuer Auditauftrag (in diesem Einspielpaket): `prompts/30_ANTIGRAVITY_MASTER_AUDIT_2026-11-10.md`

**Hinweis:** Diese README dokumentiert Ziel, Quellen und Abnahmekriterien. Sie behauptet keine bereits umgesetzten oder getesteten STEPS-Funktionen. Technische Rückbauten und Git-Änderungen erfolgen erst in einem gesondert freigegebenen Feature-Branch.

</details>

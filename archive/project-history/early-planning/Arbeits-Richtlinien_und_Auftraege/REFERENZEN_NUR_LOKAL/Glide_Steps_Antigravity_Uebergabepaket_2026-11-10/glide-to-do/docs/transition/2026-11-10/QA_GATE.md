# Glide 3.53.0 – Freeze- und Qualitäts-Gates

## Gate G0: Sichern und Zustand identifizieren

- [ ] Arbeitsbaum und alle Änderungen inventarisiert; keine ungesicherten Daten / nicht ausgeführten Copilot-Schreibaktionen
- [ ] Remote-Branch/Status und lokaler SHA explizit verglichen; `main` kann über historische Übergabetexte hinaus fortgeschritten sein
- [ ] Produktdateien von Daten, Archiven, Fremdassets und temporären Tests getrennt; Testdaten isoliert
- [ ] Unfertige Copilot-Arbeit als eigene offene Aufgabe dokumentiert

## Gate G1: Tests auf eingefrorenem Commit

- [ ] vollständiger Windows-Workflow, Linux-Matrix, nativer macOS-Vollmodus; keine verkappten `skip` als Erfolg
- [ ] native Windows- und macOS-Paket-/Startabnahme je Quell-SHA
- [ ] Quell-/Lieferhashes, SPDX, Fremdlizenzen, SBOM und erreichbarer Source-Ref
- [ ] Start, zwei Arbeitsflächen, Sidebar einklappen/ausblenden, Dialog/Fokus, Schriftwechsel, DPI/Mehrmonitor, Schreibsperre, Save/Backup/Restore, Undo/Redo
- [ ] Performance-Median/p95 mit **identischen** Daten und Systembedingungen; historische rote Nachweise bleiben erhalten
- [ ] manuelle Bild- und UX-Matrix dokumentiert; CI allein reicht nicht

## Gate G2: Separater Architekturbranch

Erst wenn G0/G1 geschlossen und die **Freigabe zur Extraktion explizit** ist: eine saubere Kopie/fester Source-SHA für `shell-refactor`. Keine Änderungen auf laufendem Releasebranch oder direkt in `main`. Zuerst nur `Shell`-Identifizierung und Sicherungstests, dann exakt ein Modul-Schnitt. Jeder Modul-Schnitt hat seine eigenen Tests und einen Rollback-Pfad.

## Gate G3: Unabhängige Übernahme

Ein Modul ist erst dann `ready_for_reuse`, wenn (1) kein Import der Glide-App nötig ist, (2) keine Glide-Nutzerdaten berührt werden, (3) es mit austauschbarem `AppContext` in Glide **und** in einem neutralen Testhost läuft, (4) native UI-/Lebensdauertests und Quell-/Lizenzbeleg vorhanden sind. Kein Paketstatus ohne Beleg.

## Zulässige Statuswerte

`NOT_STARTED`, `IN_PROGRESS`, `PASS`, `FAIL`, `SKIPPED`, `BLOCKED`, `NOT_TESTED`, `SUPERSEDED`; jede Prüfung mit Commit/Plattform/Artefakt/Log/Datum. `release_ready=true` nur nach bestehenden offiziellen Kriterien – **nicht** aus dem Wunsch der Entwicklungsfortsetzung ableiten.

# Nachgewiesener Stand und Widerspruchsregister – Glide

## Priorität P0: Remote und Übergabe weichen ab

| Kennung | Datei/Beobachtung | Widerspruch/Risiko | Korrekturauftrag |
|---|---|---|---|
| GL-01 | `00_Arbeitsvorbereitung/Glide_Uebergabe.md` nennt `main=61a2f3a` und 3.53.0 als lokalen Kandidaten | Remote `main=9e767bea`, PR #75 gemergt, `VERSION=3.53.0` | Statuspassage datiert fortschreiben; historischen Abschnitt erhalten, nicht nachträglich umdeuten |
| GL-02 | `01_Repository/Glide/README.md`, `docs/07_QA_BERICHT.md`, Plan §21.83 | Aussagen „main unverändert“, „Kandidat wird gepusht“ sind nicht mehr aktuell | neue Remote-Lage und zugehörige Laufnachweise separat ergänzen; nur auf sicher bestätigter Grundlage |
| GL-03 | GitHub Action auf 9e767bea zum Prüfzeitpunkt noch `in_progress` | Ein macOS-Paketjob `success` ist keine komplette Release-/Plattform-/Human-Abnahme | alle Jobs **genau zu dieser SHA** inklusive Auslassungen und Artefakthashes prüfen |
| GL-04 | 3.53.0 lokaler Freeze laut QA: Windows 130/131, Bildsichtung übersprungen, `release_ready=false` | „Windows grün“ bedeutet nicht „Release grün“; frühere instabile Performance-Werte bestehen als Evidenz | bekannte roten historischen Läufe erhalten, offenes Gate konkret schließen |
| GL-05 | `src/glide/README.md`: Systemversion 1.15, 94 Python-Dateien, 25 Paketkandidaten | keine neutral veröffentlichte Framework-API; `app.pyw`/`ListApp` sehr groß | Module erst kartieren, dann selektive Adapter und Tests; nicht komplette App kopieren |
| GL-06 | Versionsfamilien 3.50.5/3.50.7/3.51/3.52/3.53 | Testnachweis nicht über Versionsetiketten übertragen | App-SHA + Python/Tk/OS + Datenformat 26 + Systemversion 1.15 stets separat |
| GL-07 | Schrittfolge Copilot→Antigravity | nicht committete Arbeit, ungelesene Übergaben, zwei Agenten könnten gleichzeitig schreiben | vor Start exklusiver Schreibbesitz, Snapshot, Branch, Differenzliste und sichere Arbeitskopie |
| GL-08 | Nutzerwunsch zweier Arbeitsflächen | „zwei Fenster“ kann native Fenster oder Haupt-/Nebenbereich bedeuten | echte Hierarchie und Fensterhosts in `ListApp` inventarisieren; Layoutsemantik dokumentieren; keine Annahme erzwingen |
| GL-09 | Schrittfolge Glide→Steps | Steps-Daten- und Audiomodell nicht Glide-Aufgabenmodell | neue Steps-Projektidentität, eigene Domäne, Import nur gezielt und lizenziert |

## Tatsächlich aus den Quellen belegt

- Remote `main`: `9e767bea5e21063466a28ac3a679406484ad5d5f`; Merge PR #75, „Fix macOS license manifest staging“.
- `01_Repository/Glide/VERSION`: `3.53.0`; `GLIDE_SYSTEM_VERSION`: `1.15`; Datenformat laut Dokumentation `26`.
- Lokaler QA-Nachweis 10.11.2026: Windows 11, Python 3.14.7, Tk 9.0.4; finaler Windows-Vollmodus 130/131, ein Bildsichtungs-Schritt übersprungen, weitere Plattform- und manuelle Matrix offen.
- PR #71 historisch erfolgreich gemergt, sein Status ist **nicht** automatisch der Status von PR #75.
- Remote CI: `https://github.com/n05a-design/glide-to-do/actions/runs/42822511966` (zum Prüfzeitpunkt noch in progress); macOS-arm64-Paketjob `42822511486` auf gleicher SHA mit success. Bei späterer Verwendung erneut prüfen.

## Übergabeausgabe des neuen Agenten

`git status`, Branch, SHA, `VERSION`, Python/Tk/OS, laufender CI-SHA, `release_ready`, vollständige Liste offener Belege, explizite `NO-CHANGE`-Grenzen, Diffstat, ausgeführte Kommandos, Seiteneffekte, nächste **eine** Aufgabe. Ergebnisse nicht erraten.

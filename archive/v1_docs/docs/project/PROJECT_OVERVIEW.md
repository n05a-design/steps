# STEPS – Projekt-Overview und Entscheidungsbasis

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## 1. Kurzbild

**Produktvision:** unabhängige, quelloffene, lokal betreibbare Desktop-App zum Erstellen, Explorieren, Analysieren, Lernen und perspektivisch Anhören/Exportieren musikalischer Progressionen. `n05a-design/steps` beschreibt ausdrücklich *chord progression* und Musiktheorie; die aktuelle Nutzerbeschreibung ergänzt **drum progressions** und MIDI-Export. Daher gilt: Akkord-/Harmonie-Forschung als erster verifizierbarer Kern, Drum-/Groove-Arbeiten ausdrücklich als geplanter Produktzweig, dessen MVP-Zeitpunkt **offen** ist (im älteren Bericht deferred). Keine Features durch diese Priorisierung streichen.

**Technische Absicht:** Glide (Python/Tkinter) bietet eine bestehende produktive Shell, Design- und Qualitätssysteme. Steps soll ein eigenständiges Produkt mit eigener Identität, eigener Datenhaltung, eigenem Lern-/Harmoniemodell, aber maximal nutzbarem technischem Glide-Erbe werden. Nicht die Todo-Domäne zur Musiktheorie umetikettieren.

## 2. Fünf getrennte Arbeitsebenen

| Ebene | Bedeutung | Gegenwärtiger Nachweis | Ziel|
|---|---|---|---|
| P1 Steps-App | UI/Progressionen/MIDI/Musiklernen | `src/steps` und `app` auf GitHub derzeit Dokumentations-Scaffold, keine geprüfte App | eigenständiger funktionaler MVP |
| P2 Knowledge Base und Skill | musiktheoretische Kenntnisse mit Quelle, Rechten und Beispielen | 1.000 Legacy-V6.6-Fachdateien in Archivbaum, neue `registry.yaml` aktuell `sources: []` | prüfbare, inkrementelle Fachbasis |
| P3 Glide-Transfer | Shell, Ressourcen- und Eventverwaltung, Design, Speicherung, QA, Packaging | GitHub Glide 3.50.7; lokaler Einzelcode 3.53.0, großer `ListApp` | isolierte Adapter, keine Todo-Fachdaten |
| P4 Quellenforschung | 20 ursprüngliche Theoriequellen, später Literatur/Crawls/Corpora | 20 Namen im Bericht, 60 PDFs im Repository nur als Dateien inventarisiert; nicht vollvalidiert | Quellen- und Claim-Registry |
| P5 Breiter Produktionsbestand | 49 V6.6 Hauptordner, Ableton/Drums/DAW/Mixing/Produktion | tatsächlicher Archivbaum mit 1.000 Dateien; V6.7-Generatoren, aber kein unabhängiger fertiger Delta-Ingest nachgewiesen | bewahren, kuratieren, per Roadmap anschließen |

Die Bedeutungen von **STEPS** als Akronym widersprechen einander in älteren Texten; bis zu einer Owner-Entscheidung nur `Steps` als Eigenname verwenden. Versionen strikt trennen: Glide 3.53.0 lokal / 3.50.7 GitHub, Glide-System V1.15 / GitHub ggf. älter, Steps `VERSION=0.0.0-dev`, Bibliothek V6.6 / Erweiterung V6.7.

## 3. Zielgruppen und Nutzung

Anfänger, Musikschüler, Komponisten/Songwriter, Gitarristen/Pianisten, Produzenten und Lehrkräfte. Leitmotiv **Exploration – Explanation – Education**. Ein Benutzer kann eine Folge anlegen, Akkordrelationen sichtbar machen, transponieren, mit Kontext/Quellen eine Erklärung erhalten, lokal speichern und später mit MIDI arbeiten. Eine Erklärung wie `E7 → Am` darf nicht ohne Kontext als 'Zwischendominante' etikettiert werden: in a-Moll V7, in C-Dur V7/vi.

## 4. Geplanter Funktionskatalog (ohne Releasezusage)

| Cluster | Funktion | MVP-Gate |
|---|---|---|
| Editor | Progression anlegen, einfügen, ersetzen, löschen, Takt/Tempo, Undo | zuerst Datenvertrag und UI-Smoke |
| Harmonie | Akkordsymbol, Pitch/Spelling, Quality, Slash Bass, Umkehrung, Kontext | Golden-Theory-Tests |
| Explorer | diatonisch, Funktion, Borrowing, Dominanten, Voice Leading, alternative Lesarten | Quelle + Framework + Begründung |
| Learn | Begriffshilfen, Stufen, Beispiele, Gegenbeispiele, Übungen | validierte Claims |
| Dateien | lokale Steps-Projekte, Save/Load, Backup/Restore, Export | eigenständiges Schema + sichere IO |
| Audio | Vorschau, Playback, Loop, MIDI Export/Import, Tempo/Velocity | gesonderte Audio-/MIDI-Tests |
| Drums | Drum-Step-Sequencer, Patterns, Groove, Verbindung zu Akkorden | **Zeitpunkt offen**; Bestand nicht löschen |
| Erweiterung | MusicXML/JAMS, Korpora, Stilmodelle, Adaptivität | nach stabilem Kern |
| Projektbetrieb | Designsystem, Windows/Linux/macOS, Tastatur, A11y, CI, Installer | quellspezifische QA und Lizenz-BOM |

## 5. Das ist jetzt schon da

Das Steps-Repository hat `docs/project`, `docs/architecture`, `src/steps`, `app`, `knowledge`, `research`, `schemas`, `skills`, `tests`, `tools`, `design` und `decisions`. Dies sind **teilweise explizite Platzhalter**. Die Root-`README.md` hat nur 117 Zeichen und sogar ein `&amp;`. `knowledge/sources/registry.yaml` ist leer; fünf Schemas und ein einfacher Strukturtest existieren. `SKILL.md` ist ein Projekt-Routing-Skill; der konkrete Harmony-Coach liegt unter `skills/music-harmony-coach/2026-11-10 – music-harmony-coach/SKILL.md` und soll in seinen Workflow übernommen werden. `README_SETUP.md` behauptet historisch `push:false`, die aktuelle verknüpfte GitHub-Berechtigung weist `push:true` aus. Ein bestehendes Audit `ANALYSE_REPOSITORY.md` basiert auf älterem `b42a990...` und historischen Pfaden.

## 6. Arbeitsprinzipien

1. Bestehende Lösungen nicht wegwerfen, nur explizit de-aktivieren/adaptieren, mit Rückweg.
2. Zwei sichtbare Primärbereiche zunächst als **Sidebar + Workspace** modellieren; wenn tatsächliche zwei OS-Toplevel-Fenster gemeint sind, gilt das als offene UI-Entscheidung.
3. Bestehende Seitenleistenpunkte zunächst **anzeigbar, aber funktionslos**; ein späteres `route_registry` mappt sie auf Musikmodule. Die globale Suche, Eingabekomponente, Dialog-/Einstellungslayouts und Header sind technische Fähigkeiten, aber nicht zwingend ihre alte Todo-Aktion.
4. Skills sind Router, nicht die alleinige Wissensquelle. Knowledge-Claims und Tests gelten unabhängig vom KI-Anbieter.
5. Public Repository und private Lizenz-/Recherche-Dateien strikt trennen; fremde Werke nicht ungeprüft veröffentlichen.
6. Bei Konflikten: Behauptungen aus älteren Dokumenten datieren und belegen, aktueller Code + GitHub-SHA für Implementierungsstatus, explizite Entscheidung für Produktscope.

## 7. Weitere Navigationspunkte

- Konzepte und anstehende Entscheidungen: `docs/project/CONFLICTS_AND_GAPS.md` und `decisions/README.md`.
- Etappen & KI-Ressourcen: `docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md`.
- Glide-Rückbau: `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`.
- Forschung, Lizenzen und Skill: `knowledge/README.md`.
- Ungekürzte Originalvorlagen, 20 Quellen, 40 ältere Widerspruchsregister-Einträge, 34 Gaps und 39 Codebeispiele: `source_archive/Steps_Projekt_Overview_konsolidiert_2026-11-09.md`, `source_archive/Steps_Technischer_Anhang_und_Originalvorlagen_2026-11-09.md`.

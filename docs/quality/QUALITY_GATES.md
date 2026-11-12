# QA- und Abnahmevertrag – Steps als neue App

> Dieser datierte Abnahmevertrag enthält Zielkriterien für eine spätere App-Freigabe. Reproduzierbare Prüfungen des heutigen Kerns stehen in der [Testanleitung](../../tests/README.md).


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Qualitätsachsen

**Q0 Archiv/Quelle:** Git SHA, Manifest SHA256, Dokumentlink, Dateizahl, License status. **Q1 Domain:** Golden Tests, alternative Harmoniedeutungen, deutsche/internationale Notation, enharmonische Unterschiede, Transposition, negative Fälle. **Q2 GUI:** Tk Initialisierung, Seitenliste, Knöpfe, Theme/Font/Resize, Dialoge, Menüs, Accessibility, Suchfeld, Fokus und Cleanup. **Q3 Storage:** Settings, Save/Load/Roundtrip, Backup/Restore, Locks, defekte/neuere Dateien, kein Zugriff auf echte Glide-Userfiles. **Q4 Audio/MIDI:** Velocity/NoteOff/PPQ/Tempo/Timing, Plattform-Adapter, keine hängenden Töne. **Q5 Security/Legal:** Path Traversal, untrusted Markdown/HTML, Release-Assets, Provenienz, Quelltext/Build/SBOM. **Q6 Release:** Mac/Windows/Linux, Installer-Smoke, Signierung/Notarisierung je Ziel, Dokumentation und menschliche Sichtprüfung.

## Strenger erster S0-Testplan

| Fall | Erwartung |
|---|---|
| Startup mit temporärem Steps-Data-Dir | App startet; kein Glide-Pfad oder Glide-Lock wird angefasst |
| Sidebar offen/schmal/ausgeblendet/re-open | Position, Breite, Fokus und persistierter Modus korrekt |
| Navigation-Placeholder jedes Eintrags | keine mutierende Todo-Aktion, konsistentes No-op/Coming Soon |
| Header, Logo, 4 Schriften/2 Gewichte und Symbolfallback | lesbar/kontrastreich unter Light/Dark/System, kein kaputter Font |
| Suche: Tippen, Esc, Clear, Return | Widget funktioniert; kein Task-Suchdienst aktiv; klare Leermeldung |
| Kompaktmodus, Fenster 860x700/1280x800, DPI | keine abgeschnittenen Bedienelemente, keine Layout-Overlaps |
| Dialog + Menü auf macOS | `after_idle`/Modalitäts-Fokus funktioniert |
| Sitzung schließen mit ausstehenden Callbacks | keine ungefangenen TclError/Tk-Callback-Leaks trotz Exitcode 0 |
| Schreibschutz & Recovery | Crash/IO-Fehler weder alte Daten zerstören noch silent reset |
| HTML/URL/Asset-Zugriff | keine fremden Webseiten oder schützenswerte PDF-Inhalte in Release-Bundle |

Der ältere Glide-Designvertrag fordert eigene statt altstiliger nativer Tk-Kontrollen, 4,5:1 Kontrast, vertikale Fluchten, keine Doppelüberschrift, ruhige Flächen und einheitliche Symbolrollen. Für Steps als **separate** Designentscheidung prüfen, nicht unbesehen alle UI-Verbote übernehmen. Alle Testergebnisse immer mit Commit, Tk-/Python-/OS-Version, Skalierung, Testdaten-ID, Logdatei, Exitcode und manuell/automatisch differenzieren. Eine Linux/Xvfb-Probe ersetzt keine native Windows- oder macOS-Prüfung.

## Theorie-Golden-Tests (Seed statt 'fertig')

- `C major` → C D E F G A B im internationalen System; `a natural minor` → A B C D E F G.
- Deutsches `H` → B natural; deutsches `B` → Bb; internationale `B` → B natural.
- `C E G Bb` → C7, nicht Cmaj7; `C/E` → Bass E.
- `C-G-Am-F` +2 → `D-A-Bm-G`, Notennamen und Kontext erhalten.
- `C7 in F major` → V7; `E7 in C major` → V7/vi; `E7 in A minor` → V7; `A7 in C major` → V7/ii.
- Modal Interchange C Dur: `iv=Fm`, `bVI=Ab`, `bVII=Bb` nur bei geklärter Tonic-/Style-Deutung.
- Negative Tests: unmögliche Akkordsyntax, fehlende Quelle, mehrere plausible Analysen, importiertes MIDI mit Tempoänderungen, umbenanntes Settings-Schema.

**MVP-Qualitätsziel:** zuerst 30 explizit gereviewte Cases, danach ≥100 Golden-/Negativfälle als Gate vor gehaltvoller harmonischer Empfehlungs-Engine (Richtzahl vorgeschlagen, nicht als schon vorhanden ausgeben).

## Abschlussbericht je PR

`Base SHA`, `Head SHA`, betroffene Modul-/Funktions-IDs, neue/entfernte APIs, Tests (ausgeführt/nicht), Screenshots mit System, Design-/A11y-Sichtprüfung, Benchmark ohne unbegründete Optimierungsbehauptung, Lizenz-/Asset-Liste, bekannte Restrisiken, Rücknahmeplan, offene Owner-Entscheidungen. Rot = rot, Skip = Skip. Kein Merge ohne Review.

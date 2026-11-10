# Zwei-Fenster-UX: Alternativenvergleich und Shell-Verhaltensvertrag

**Prompt-ID:** `03_SHELL_TWO_WINDOWS_UX_RFC` · **Arbeitsart:** ANALYSE + Prototyp nur nach gesonderter Freigabe · **Roadmap:** P3

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Nutzeranforderungen dieses Audits; Glide `docs/DESIGN_RICHTLINIEN.md` D66–D77, `sidebar_policy.py`, `side_view.py`, `compact_mode.py`, aktuelle Screenshots/Widgetpfade und `docs/06_SHELL_UI_ZWEI_FENSTER.md`.

## Fachlich konkreter Arbeitsauftrag

Behaupte nicht, „zwei Fenster“ seien eindeutig zwei `Frame`-Slots. Entwickle drei Varianten: W1 Main+Secondary im Root, W2 zwei gleichwertige Split-Panes, W3 zwei OS-Fenster; jeweils mit Wireflow, Screenspace, State Ownership und Kosten/Risiken. Lass UI-Code bis zur Ownerentscheidung neutral. Für jeden sichtbaren Glide-Shellbestand führe eine Matrix `PRESERVE`, `ADAPT`, `REPLACE`, `EXCLUDE`, `UNKNOWN`: Sidebar hidden/collapsed/restored, Logo/Titel/Unterzeile, System-Menüs/Symbolbuttons, Suche/Editfelder, Settings, Fonts, Themes, Keyboard, sekundäre Ansicht, Toast/Failure, Scroll/Fokus, App-ID. Funktionslose Steps-Navigation heißt *ohne Glide-Taskcommands*, darf aber Selektions-/Expand-/Disabled-Interaktion besitzen. Entwickle eine Zustandsmaschine für Slot lifecycle `mount/activate/suspend/dispose` und Sidebar `expanded/collapsed/hidden`, UI-Fokus und `after_cancel`. Beschreibe auch, welches Verhalten bei Fensterbreite <980px, Mehrmonitor, hohe DPI, Fontwechsel, leerem Projekt, Hintergrund-Worker gilt.

## Reproduzierbare Abnahmen und Gegenproben

Paketunabhängige Proben: 3 Sidebarzustände × Maus/Tastatur; schnell 100× Panewechsel; Fokus zu Fremd-App und zurück; Root schließen während `after`; Schrift- und Symbolfallback; keine reservierte Restfläche und keine Task-/Notion-/ICS-Handler. Negative Probe: ein alter Glide-Befehl darf nicht durch Steps-Sidebar erreichbar sein.

## Ergebnis und Übergabeformat

`WINDOW_RFC.md`, `PRESERVATION_MATRIX.csv`, `COMMAND_OWNERSHIP.csv`, `VIEW_LIFECYCLE.md`, konkrete UI-Wireflows und priorisierte Akzeptanzliste. Alle W1/W2/W3 Entscheidungen ausdrücklich als `PROPOSED/REQUIRES_OWNER_DECISION` kennzeichnen.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Keinen internen Pane-Entwurf als bereits beschlossenen Zwei-OS-Fenster-Vertrag implementieren. An bestehendem Glide-Root/Windows-Fokus keine breitflächige Änderung ohne eigenen Regressionsplan.

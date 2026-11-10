# Glide-Design erhalten und Steps UX/A11y fachlich eigenständig machen

**Prompt-ID:** `08_STEPS_DESIGN_ACCESSIBILITY` · **Arbeitsart:** ANALYSE + UI-Implementierung nur nach ausgewähltem Fenstervertrag · **Roadmap:** P3/P6

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Glide `DESIGN_RICHTLINIEN.md` inklusive D66–D77, Schrift-/Symboltests, Steps `design/`, `research/UI-UX-Design/`, `docs/06_SHELL_UI_ZWEI_FENSTER.md`.

## Fachlich konkreter Arbeitsauftrag

Erstelle ein visuelles und semantisches Komponentenregister: Shell-Chrome, header, sidebar, selected/hover/focus, commands, search, settings, empty state, errors, scroll, progress, two slots. Verknüpfe jedes Element mit aktueller Glide-Rolle/Designregel und beantworte `preserve mechanism`, `replace copy/brand`, `defer`, `remove Task-domain`. Vergleiche Desktop-UX für Harmony Explorer + Drum Grid bei kleinen und großen Fenstern: Titel/Status, Symbolbeschriftung, Timeline-Koordinaten, Keyboard-Modell, Kontinuität zwischen Chord und Drum, Anordnung der Panels. Beachte DM Mono/DM Serif Display/Charis SIL/Rubik, DejaVu-Fallback, Schriftgewicht, CI-Fontmetriken, Theme-Kontrast. Keine alten native Controls, die den Projektstil oder Accessibility verschlechtern. Zeige Viewmodel-basierte Layoutänderung ohne globale `ListApp`-Funktionen. Entwirf einen präzisen manuellen QA-Plan für Mac Aqua, Windows und Linux, Screenreader-Grenzen und Mehrmonitor-Varianten.

## Reproduzierbare Abnahmen und Gegenproben

Maus/Tastatur und 100%/150%/200% Skalierung, kleines Fenster, lange/fehlende Titel, Tooltip, unsichtbare Seite, Disabled-Aktion, Dark/High-Contrast, Rückfokus nach Dialog, aggressive View-Switches; keine unerklärten Leerflächen. Negative Probe über `backspace` in Textfeldern darf keine Navigation löschen. PDF/Screenshot-Rendering nur als ergänzende Sicht, keine Nutzertest-Freigabe.

## Ergebnis und Übergabeformat

`DESIGN_PORT_MATRIX.csv`, `STATE_GALLERY_SPEC.md`, `A11Y_TEST_MATRIX.md`, `STEPS_UI_FLOWS.md` mit Wireframes (wenn beauftragt), präzise Design-ADRs und verbleibende manuelle Abnahmen.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Branding/Logo von Glide nicht heimlich für Steps verwenden, keine neue Widget-Bibliothek ohne Lizenz-/OS-Prüfung und kein stilles Abweichen von bestehenden Glide-Designrollen bei gemeinsamem Core.

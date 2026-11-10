# Auftrag 26 – Zwei konkurrierende STEPS-Shell-Architekturen als echte Spikes vergleichen

**Rolle:** unabhängiger Engineering-Agent, keine vorentschiedene Fork-Präferenz. **Quellen:** Glide `main 9e767bea`, lokaler `app.pyw 3.53.0`, `README-Glide-System.md`, `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`, `docs/audit/03_ALTERNATIVEN_UND_ENTSCHEIDUNGEN.md`, `manifests/GLIDE_94_MODULE_REUSE_AUDIT_V2.csv`, bestehende Designrichtlinien und die 30 S01–S30-Cases.

## Eingangsgate

Zuerst Source-/Asset-/License-Manifest, Working-Tree-Status und Branch sichern. Kein Import des Glide-Hauptscripts in den neuen Steps-Prozess, bevor seine Import-Nebenwirkungen und die Datenroot-Isolation kontrolliert sind. Keine Änderung am Original-Glide-Repo; bei Spikes synthetische und isolierte Nutzer-Settings.

## Zwei Varianten mit identischem Scope

**Spike B:** Selektive Extraktion der kleinsten nötigen Glide-UI-/Theme-/Font-/Navigation-Komponenten hinter Steps-eigenen Ports. **Spike D:** Unabhängige Tk-Shell, die dieselben dokumentierten UX-Verträge nachbaut, ohne Glide-Laufzeitmodule blind zu kopieren. Beide zeigen je einen Sidebar-Navigator (expanded/compact/hidden), Header (Logo, Titel, Unterzeile, Symbolaktionen), globales Suchfeld mit erklärtem leeren Zustand, Einstellungen, Theme-/Schriftwahl und zwei Mock-Workspaces. Beide führen bei nicht implementierten Navigationspunkten **keine** alten Todo-Aktionen aus. Die Fenstersemantik ist vorläufig eine Root mit Sidebar und Workspace; für separate `Toplevel`-Fenster nur einen Wireframe und technische Gegenbewertung erstellen, nicht stillschweigend entscheiden.

## Vergleich

Messe reale Zeit für Implementierung und wiederkehrende Änderungen, importierte Module/Transitiv-Abhängigkeiten, Codeumfang, Tests, Benutzer- und Dateipfade, Accessibility, Theme-Switch, Fontfallback, Cocoa-Menü-Focus und Packageability. In beiden Varianten gilt dieselbe Testliste S01–S30. Jeder Befund bekommt Screenshot/Trace, exakte OS-/Python-/Tk-Version, Commit, Fixture, Pass/Fail/NotRun und benannte Einschränkung. Führe No-Glide-Touch-Negativtests mit Vorher-/Nachher-Dateihashes durch. Kein durch Testgrenzen unsichtbares altes `ListApp`-Save/Undo/Task-Callback.

## Entscheidungsübergabe

Erstelle `ADR-SHELL-Comparison.md` mit Gewichten, konkreten Messwerten, Architekturaufwand, Lizenz-/Assetfolgen, Wartbarkeit, Rollback und Begründung der bevorzugten Variante. Ein Spike darf ausdrücklich verworfen werden. **Nicht** automatisch beide produktiv fortentwickeln und keine finale Architektur ohne menschliches Review festlegen.

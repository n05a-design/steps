# Eine wirklich neutrale Core-Schnittstelle extrahieren und in zwei Produkten prüfen

**Prompt-ID:** `04_SHARED_CORE_STRANGLER_SPIKE` · **Arbeitsart:** IMPLEMENTIERUNG NACH FREIGABE, nur kleiner isolierter Spike · **Roadmap:** P4/P9

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Ausgabe von Prompt 02 + gewählte Shell-RFC aus Prompt 03; Glide `src/glide/README.md` B01–B25 und `AGENTS.md`; Steps `docs/architecture/architecture.md`, `src/steps/`, `app/`.

## Fachlich konkreter Arbeitsauftrag

Vergleiche zuerst drei Distributionstechniken: lokales reines `desktop_core`-Package, vendor/source pin, Git subtree; begründe Kosten und Upgradefolgen für **beide** Produkte. Wähle **nur eine kleine reife Mechanik** (z. B. rein logische Appearance-/Sidebar-Zustandsfunktion, nicht `ListApp` in Gänze). Definiere minimalen Public API/Port und einen dünnen Glide-Adapter, ohne Glide-Nutzerverhalten zu verändern. Implementiere in separatem Branch einen Steps-Dummy-Consumer desselben Core-API-Vertrags; nur reine Daten, keine produktiven Task-Modelle. Dokumentiere Importfreiheit von Glide-/Steps-Domain im Core, Ressourcen-/Lizenzketten, Produkt-ID, Migration und Configuration injection. Wäge gegen eine Neuentwicklung dieser einen Komponente ab. Erst mit zwei realen geprüften Consumers eine semantische Core-API-Version vergeben. Kein automatischer Core-Updater oder Netzdownload.

## Reproduzierbare Abnahmen und Gegenproben

`import desktop_core` ohne `DISPLAY`, ohne Userdata; zur Laufzeit keine Home-/Glide-Pfadöffnung. `glide consumer baseline` muss unverändert bleiben; Steps Dummy Host auf synthetischer Root/Settings; negative Tests falscher Produkt-ID, doppelten Command-Handler, toten Widget, Unterbrechung der Speicherung; Python/Tk/OS-Matrix gezielt. Migrations- und Package-Roundtrip nur wenn betroffen.

## Ergebnis und Übergabeformat

Kleiner reviewbarer Diff, API-Dokument, Lizenz-/Source-Manifest, `compatible_consumers.csv`, Red/Green-Tests mit Kommandos/Hashes, Risikovergleich „shared library vs. vendoring“ und begründete Entscheidungsempfehlung.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Kein Framework-Big-Bang, kein Mergen in `main`, kein Paketrelease; bei absehbar hoher `ListApp`-Zerlegung einen kleineren Mechanismus auswählen oder den Spike abbrechen.

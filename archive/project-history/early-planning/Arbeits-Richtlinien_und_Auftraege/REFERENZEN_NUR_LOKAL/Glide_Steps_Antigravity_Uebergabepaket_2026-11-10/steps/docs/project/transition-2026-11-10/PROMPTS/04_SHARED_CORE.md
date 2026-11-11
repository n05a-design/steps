# P04 – Produktneutrales Shared-Core und Modulvertrag

## Direkt nutzbarer Prompt

Ziel: eine in Glide und Steps nutzbare **modulare Systembasis** entwickeln, ohne zunächst eine unbelegte Framework-Freigabe zu behaupten. Die bestehende Glide-Systemdoku `src/glide/README.md` ist das kanonische Inventar von 94 Quelldateien und 25 Paket-Kandidaten; verwende sie, aber untersuche vollständige transitive Python-/Tk-/Asset-/Storage-Kopplung.

1. Konzipiere eine gemeinsame Schichtung `neutral core -> contracts/ports -> Produktadapter -> Tk-Host -> Produktfunktionen`; vermeide zirkuläre Imports und `app.pyw`-Imports mit Startseiteneffekt.
2. Vergleiche Verteilwege mit ADR: `shared` im eigenen Versionsrepository (später möglicher Submodule/Subtree), dediziertes Python-Paket mit fixiertem Commit/Wheel, paketierter Quellcode unter MPL; **kein** unreflektiertes Kopieren per Cut/Paste in mehrere Repos. Es muss ohne Netzwerk im Runtime funktionieren.
3. Definiere versionierte Python-Protokolle für `AppContext`, `FeatureModule`, `PaneHost`, `NavigationEntry`, `Command`, `SettingsNamespace`, `ThemeTokens`, `StoragePort`, `Lifecycle`, `AsyncWorker`. Instanziierung durch Dependency Injection, Event-Lifecycle und Cleanup, keine Global-Singletons aus Glide.
4. Portiere als **einen** Pilot zuerst `persistence.py + save_result.py` **oder** eine klar abgrenzbare reine Theme-/Geometriefunktion, nicht beides gleichzeitig. Vollständigen transitive Importgraph erfassen. Nutze zwei Consumer-Tests (Glide-Adapter + neutraler Steps-Testhost) auf einem festen SHA. Cross-OS-Tests wo betroffen.
5. Entwerfe SemVer-/Kompatibilitätsmatrix: API-Version, Implementierungs-SHA, Mindest-Schema, Wechselstrategie, Migrationsnotizen, Deprecation und Rollback. Jede Übernahme muss Herkunft/Änderung der MPL-covered Files und Third-Party-Lizenzen korrekt behalten.
6. Prüfe, ob eine modulare Extraktion die App wirklich kleiner/robuster macht. Importzeit, Speicher, Startup, Geschwindigkeit, Testaufwand und Änderungsfolgen messen; keine Vorteile postulieren.

## Abbruchkriterien

App-Import ist nötig; reale Nutzerdaten würden berührt; mehrdeutiger State-/Undo-Eigentümer; nativ ungeprüfter Tk-Interpreter; Komponentenanforderung impliziert ein globales Rewriting; Lizenzherkunft unklar. In diesem Fall nur ein ADR mit konkreten Schnittstellen und gemessenem Prototypbedarf vorlegen.

## Akzeptanz

Ein getestetes Modul, zwei isolierte Konsumenten, Herkunft/Hash/Tests, API-Baseline, Upgrade-/Rollback-Anleitung. Erst danach weitere Pakete priorisieren.

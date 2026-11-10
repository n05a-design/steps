# 05 — Architektur-Optionen und begründete Empfehlung

## Ausgangsbefund

Glide verfügt laut kanonischem Systemregister über 94 Hauptquellen, 25 Reuse-Pakete B01–B25 und eine zentrale `ListApp`-Implementierung. Die Aussage '88 Dateien ohne direkten Tkinter-Import' ist nur ein schwacher Indikator für Entkopplung: `markdown_tree` importiert `object_references`, `page_markdown`, `drawing` und `task_references`; `notion_import` ruft weitere Glide-Prozess- und Datenpakete auf. `side_view` importiert `object_references`. Selbst scheinbar kleine Widgets können auf TaskIDs, Globals, Font-Dateipfade, Prozesszustände oder aktivierte Befehle zugreifen. Ein pauschales Verschieben von Python-Modulen würde das Verhalten nicht erhalten.

## Vergleich von fünf Lösungswegen

| Alternative | Nutzen | Kosten/Risiken | Urteil |
|---|---|---|---|
| A. Glide kopieren, Seiten-/Fachfunktionen löschen | Schnellste visuelle Demo; UI-Pixel können zunächst ähnlich aussehen | Riesiges `app.pyw`, versteckte Daten-/Event-/Fokus-Referenzen, regressionsanfälliger Rückbau; spätere Core-Updates kaum sicher portierbar | **Ablehnen als Dauerarchitektur**, höchstens temporäre isolierte Referenzkopie ohne Weiterentwicklung |
| B. Neue generische Desktop-Library aus allen B01–B25 vor Steps | Einheitliche API auf dem Papier; optimiert für viele Folgeprojekte | Vorzeitige Generalisierung, kein zweiter realer Kunde, große Projekt-/Release-/Testlast, monolithische Anteile nicht entkoppelt | **Nicht jetzt** |
| C. **Strangler + ports/adapters + Zwei-App-Validierung** | Erhält Glide-Funktionen, extrahiert kleine stabile Mechanismen, tatsächlicher Bedarf aus Steps bestimmt Abstraktion | Mehr Phasen, zunächst doppelte Adapter, API muss später nachgeschärft werden | **Empfohlen**, mit dokumentierter Rückfallstrategie |
| D. Glide-Kern als Git-Submodule/Subtree in Steps | Herkunft und Commit-Pin sehr sichtbar, ohne Package-Registry | Pfad-/Import-/Release-Grenzen, Konflikte bei Updates, bindet Projekt stark an Git-Vorgehensweise | Mögliche **Liefertechnik**, keine Ersatzarchitektur; erst nach API-Extraktion entscheiden |
| E. Produktunabhängige Neuimplementierung der Steps-Oberfläche | Keine Glide-Historie und Monolith-Refactoring in Steps; klarer Minimalumfang | Viel Wiederholungsaufwand, Verlust von Design-/QA-Arbeit und UX-Details, neues OS-Risikoprofil | **Fallback**, falls Extraktionskosten überschreiten und UI-Referenzrechte/Verhalten separat erhalten werden |

**Qualitative Empfehlung:** C ist beste Balance aus Risiko, Wartbarkeit, Wiederverwendbarkeit und Prüfbarkeit. Keine erfundenen gewichteten Scores: belastbare Kosten-/Komplexitätsmessung setzt einen Probe-PR mit echter Importgraph-/Testanalyse voraus. **Stop-Gate:** Wenn der kleinste funktionsfähige Schnitt nicht ohne breitflächige `ListApp`-Mutation gelingt, Option E für eine einzelne Komponente erneut prüfen statt die Architektur gewaltsam passend zu machen.

## Drei Schichten, strikte Richtung

```text
Glide-App (Glide-Domäne, Glide-Views)     Steps-App (Musik-Domäne, Musik-Views)
            |                                   |
        Glide-Adapter                       Steps-Adapter
            |                                   |
            +------ Desktop-Core-Ports ---------+
                        |       |
                 Shell/Theme    Filesystem-/Lifecycle-Abstraktion
                          [kein Import von Glide- oder Steps-Domain]

Steps-Domäne <-> deterministische Musikregeln (Tk-frei)
Knowledge-Registry -> nach Review fachliche Daten/Erklärungen; keine direkte Import-zu-Python-Logik
```

**Allowed dependency direction:** `products` → `adapters` → `shared_core`; `shared_core` → nur Python stdlib/optional abstrakte Ports, nicht `glide.*` oder `steps.*`. Musik-Domäne darf auf allgemeine Datentypen und explizite Ports zugreifen, aber nicht auf `tkinter`, Widgets, Produkt-Dateipfade oder Internet. UI-Fachansichten implementieren Ports und übersetzen ViewModels in Tk-Widgets.

## Kanonische Port-Verträge als **Entwürfe**, keine schon existierenden APIs

- `ProductIdentity`: Produkt-ID, Anzeigename, Paketname, erlaubte Dateiendungen, Icon-/Branding-Resolver, Quell-/Lizenzhinweis. Produkt-ID im Code/Build/OS eindeutig, keine Übernahme des Glide-Bundle-Identifier.
- `RuntimePaths`: `data`, `config`, `cache`, `log`, `backup`, `lock`, `temp`, `resources`, `test_root`; ein Root pro Produkt/Profil; alle **vor jedem Import mit Seiteneffekt** injizierbar; nur erlaubte Unterordner.
- `ThemeProvider`: rollenbasierte Palette + Font/Tk-Adapter getrennt. Kein Widget erzeugt seine eigenen unversionierten Farbkonstanten. Design-Vertrag aus Glide übernehmen, Schritte-spezifisches Branding nicht kopieren.
- `CommandRegistry`: ID, Rolle/Label/Shortcut, `enabled(context)`, Handler, Undo-/Write-/Network-Klasse, Tooltips, Fehlerroute; Menü, Seitenleiste, Suchpalette aus **einer** Registry, keine doppelten Aktionslisten.
- `NavigationModel`: stabile Element-ID und Kindtyp, order/parent/selected/visibility/fold/scroll; neutrale `Command`-Verweise, keine alte Task-ID-Pflicht; bei funktionslosen Einträgen `disabled_reason` oder reine Selektionswirkung.
- `WorkspaceHost`: Slot 1/2 optional austauschbar; `mount`, `activate`, `suspend`, `unmount`, `dispose`; eindeutiger Widget-/State-Owner, Fokuswiederherstellung und `after`-/Eventcleanup.
- `SettingsStore`: Schema-/Migrationsversion, Defaults, Konfliktstrategie, UI-Änderungskontext, atomare Speicherung; unknown fields nur nach dokumentierter Kompatibilitätsregel bewahren.
- `StoragePort`/`MutationPort`: Projekt-DataStore, validierte Änderungen, Undo/Redo-Transaktion, SaveResult (vor/nach Commit); keine UI-seitigen direkten Dateiänderungen.
- `Diagnostics`: datensparsame, optionale Fehlertypen, Tests mit injectierbaren Uhren/Reportern; keine persönlichen Verzeichnisse in öffentlichen Artefakten.

**Wichtig:** Diese Namen sind **Vorschläge**, kein Anspruch auf existente Klassen. Beim Refactor zunächst vorhandene Ports/Werkzeuge verwenden, nur zwingend fehlende abstrakte Grenzen einführen. Zu viele generische Klassen/Dependency Injection können die App schlechter verständlich machen als explizite dünne Adapter.

## Verteilung/Versionsupdate: drei realistische Wege

**Frühe Phase:** selektive direkte Module im Steps-Branch mit protokollierter Quelle/SHA und eigener Integration testen. Nur als *temporäre* Brücke. Niemals automatisches blindes `cp -r glide`.

**Nach 2 produktiven Integrationen:** eigenes kleines `desktop_core`-Paket mit `pyproject.toml`, `src/`-Layout, SPDX-/Lizenzhinweisen, klarer Public API, `CHANGELOG`, `compatibility.csv`, Tests. Ein lokales Workspace-Package oder versionierter Wheel-/Tarball-Installationspfad ist offline möglich. Keine neue Netzwerkabhängigkeit in der App. Anwendungsreleases pinnen auf konkrete Core-Version + Hash.

**Subtree/Monorepo-Variante:** falls Releases immer synchron und Team klein bleiben, kann ein Monorepo/Monorepo-ähnlicher Vendoring-Schritt unkomplizierter sein. Nachteil: Glide und Steps sind bereits eigenständige Repos und sollen unabhängige Releases behalten; ohne dringenden Vorteil nicht reorganisieren.

## Auswirkungsanalyse einer typischen Core-Änderung

*Beispiel Theme-Fontgröße:* (a) Shared Core API `font_scale` ändert → (b) Glide-Adapter und Steps-Adapter prüfen Constraints → (c) echte Widget-Geometrie, Icon- und Fontfallback messen → (d) Settings-Migration oder Defaultverhalten prüfen → (e) Keyboard/Reader/Textumbruch/Tooltips regressieren → (f) native Paketassets und Lizenzen prüfen → (g) unabhängige App-Releaseentscheidungen. **Eine neue Kernversion ist nicht automatisch eine neue App-Freigabe.**

*Beispiel Navigation:* neue `NavigationItem`-Art → kein Task-Domain-Typ im Core; vorhandene Glide-Tasks weiterhin über Glide-Adapter; Steps-Musikseiten über neue Provider. `Undo` betrifft nur Domain-Änderung, nicht reinen Seitenwechsel; begrenzte UI-Historie kann getrennt persistiert werden.

*Beispiel Datenvertrag:* neue Core-Save-Policy → jeder Produktadapter muss atomaren Commit, Lock, Recovery und verzögerte UI-Reaktion prüfen. Cross-Read von Glide-Produktion in Steps bleibt **explizit verboten**, selbst bei gleichem JSON-Basistyp.

## ADRs vor einer gemeinsamen Bibliothek

A01 Ein-/Zwei-Fenster-UX; A02 Shared-Core-Lifecycle vs. Projektcode; A03 Paketdistribution/Release; A04 Produkt-/App-/Datei-IDs; A05 Settings-/Datenmigration; A06 Fonts/Branding-/Ressourcenrechte; A07 Command- und Navigation-Port; A08 Schema-Versionen und Persistenz; A09 Python-/Tk-Zielmatrix; A10 öffentliche Knowledge-Rechte. Vor einem `ACCEPTED`-Status jeweils Belege, Alternativen, konkrete negative Tests und Entscheidung der Nutzerseite erforderlich.

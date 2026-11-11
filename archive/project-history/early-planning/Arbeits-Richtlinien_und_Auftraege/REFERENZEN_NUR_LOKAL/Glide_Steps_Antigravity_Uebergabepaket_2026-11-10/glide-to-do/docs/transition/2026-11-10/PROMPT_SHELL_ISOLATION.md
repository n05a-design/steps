# Prompt – Glide-Grundgerüst mit zwei Arbeitsansichten **isolieren**

**Vorbedingung:** G0/G1 abgeschlossen, Releasebasis fixiert, separater Architekturbranch freigegeben. Der Auftrag gilt nicht als Genehmigung, Glide-Features zu löschen.

Untersuche die aktuelle `ListApp` und die Module von Glide anhand des tatsächlichen lokalen Quellstands. Ziel: ein **neutrales Shell-Grundgerüst** mit zwei austauschbaren Inhalts-Hosts, jedoch **ohne Verlust aller bisherigen Bedieneigenschaften außerhalb dieser Inhaltsbereiche**. Prüfe zuerst, ob die „zwei Fenster“ im tatsächlichen Tk-Baum zwei Arbeitsbereiche, `Toplevel`-Fenster oder verschachtelte Ansichten sind. Keine voreilige Topologie annehmen.

**Unbedingt erhalten:** Rahmen, Fenstergeometrie/Restoration, Haupt-/Nebenansicht, Seitenleiste inklusive Einklappen/Ausblenden, Seitenliste mit sichtbaren neutralen Einträgen, Sidebar-Buttons, Titel/Kopf/Unterzeile, Logo, System-Menüs, alle Symbolbuttons/Tooltips, Sucheingabe und Editor-Hosts, Themes und Farbrollen, Schriftstile und Gewichte, Einstellungen, Fokus/Tastatur/Accessibility, Dialoge, Menüs, Aktionen-/Statusanzeige, Prozessen/Ladephasen, Save-/Undo-/Backup-/Lock-Lebenszyklen und ihre Fehlerreaktionen. Die Seitenliste selbst hat im **neutralen Testhost** zunächst keine Glide-Fachaktionen; die bestehende Glide-App behält ihre funktionalen Seitenaktionen.

**Vorgehensweise:**

1. Originale Visual-/Interaction-Baseline (synthetischer Zustand, alle Sidebar-/Pane-Zustände, 4 Schriftstile, Light/Dark/System, DPI/Fokus, Tastatur) sichern; Messpunkte und Widgets/Callback-Besitzer katalogisieren.
2. Schnittdiagramm mit `Shell`, `PrimaryPane`, `SecondaryPane`, `SidebarController`, `Header`, `Settings`, `AppContext`, `ActionPort`, `PersistencePort` **als Vorschlag** erstellen. Zustands- und Kontrollfluss exakt am Ist-Code abgleichen.
3. Nur eine intern verhaltensgleiche Schicht pro PR extrahieren. Nicht zuerst die große `ListApp` löschen, verschieben oder in neue Monolithdatei kopieren.
4. In einer gesonderten, minimalen Demo `NullNavigationProvider` und zwei Beispielansichten zeigen. Verbindliches Laufverhalten: Einträge anzeigen, keine Fachaktion ausführen, Pane-/Sidebar-Collapse und Header/Settings trotzdem funktionieren.
5. Glide-Produkt bleibt separat unverändert benutzbar. Ursprüngliche Tests plus neue unabhängige Tests für Nullprovider, Reload, Toggle, Fokus, Lifecycle, Editor-Flush, Dialog-Aufräumen, Start/Ende.
6. Jeden Schritt mit Änderungen, Diff, Testliste, Plattformen, Screenshots und Rollback dokumentieren. Erst nach bestandenem Zwei-Consumer-Test neue Schritte freigeben.

**Nicht ausführen:** pauschales Ausschlachten von Glide, globale Suche/Ersetze von `Glide`, direkte Steps-Datenmigration, Umbenennen von bestehenden Lizenz-/Historieneinträgen, Kopieren fremder Logos/Fonts ohne Lizenzprüfung, ungeprüfter Merge auf `main`.

**Abgabe:** Vorher-/Nachher-Widgetbaum, konkrete Files/Methoden, Dependency-Graph, Schnittstellen und jeweilige Zuständigkeiten, unveränderte Produktpfade, isolierter Demo-Test, Regressionen mit erwarteten/realen Ergebnissen, verbleibende UI-Kopplungen, fachliche „nicht extrahiert“-Liste.

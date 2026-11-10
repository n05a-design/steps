# P03 – Glide-Shell selektiv in Steps integrieren

## Direkt nutzbarer Prompt

Du sollst **nicht** Glide komplett kopieren oder seine fachliche Tasklogik in Steps umbauen. Ziel ist ein eigenständiger STEPS-Prototyp mit einem neutralen Zwei-Arbeitsflächen-Shell-Vertrag unter Erhalt der hochwertigen Glide-Interaktionsmechanik. Der ursprüngliche Glide-Quellstand muss als **Voll-SHA** und sein MPL-/Asset-Status dokumentiert sein.

**Vorbedingung:** Es liegt ein eingefrorener, gegen Tests abgeglichener Glide-Stand vor. Prüfe zuerst das gesamte `01_Repository/Glide/src/glide/README.md` besonders §9, die Shell-/Fensterhost-Implementierung in `app.pyw`, `AGENTS.md`, Design/QA und den Abnahmezustand. Wenn lokale Kopie/Quellen nicht vorhanden sind, **keinen fiktiven Code erzeugen**, sondern ein datiertes, nach Pfad belegtes Migrationsdesign ausgeben.

Ermittle das reale Modell von Hauptfenster, Nebenfenster und/oder Inhaltsbereichen und dokumentiere die Terminologie. Erhalte Window-Host, Fensterkopf, Logo-Platz, Titel/Untertitel, globalen Werkzeugknopfraum, Input-/Suchfläche, Seitennavigation, Ein-/Ausklappen/Ausblenden, Sidebar-Auswahl, Systemseiten, Design/Font, Focus/Scroll, Settings und native Bedienhinweise. Links bleiben zunächst inhaltslose, aber visuell und tastaturmäßig funktionierende Navigationspunkte. Die zwei Inhaltsflächen sind austauschbare Hosts für eigenständige später zu definierende Musikansichten, keine nachgebaute Glide-Liste.

**Rückbauverfahren:** Kandidaten klassifizieren `KEEP_SHARED`, `KEEP_VIA_ADAPTER`, `STEPS_REPLACE`, `GLIDE_ONLY`, `DEFER`, `REJECT`; Daten-/Abhängigkeitsgraph zeigen; zunächst UI-Verhalten mit synthetischen Fixtures testen. Task-/Reminder-/Planungs-/Pixel-Fachkomponenten nicht ungeprüft in den Steps-Startpfad ziehen. Unterschiede in Design, Branding und Dateipfaden explizit abbilden. Kein `Glide.DATA_DIR` / produktive Settings im Steps-Prozess. Alle Lifecycle-/Callback-/`after`-Tasks und UI-Update-Risiken identifizieren.

Arbeite in eigener Branch/Kopie, mit kleinen commits pro vertikaler Funktion. Nach jedem Schritt technische Unit-Tests und echte Tk-Integrations-/native Tests gegen Baseline; Fehler vor Performance-Optimierung beheben. Wenn die `ListApp`-Kopplung zu stark ist, statt globalem Rename den neutralen Testhost als Minimallösung bevorzugen und Abbruchkriterien benennen.

## Akzeptanz

Testbar neu startende Shell mit genau vereinbarter Haupt-/Nebenfenster-Semantik, funktionierender Sidebar-Sichtbarkeit/Fokus/Resize und zwei austauschbaren Hosts, **ohne Task-/Glide-Produktivdaten**, mit eigenen Steps-IDs; Quellzuordnung, Lizenz, Regressionsergebnisse und `NOT_TESTED` getrennt dokumentiert.

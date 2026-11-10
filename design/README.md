# Steps – Designübertragung aus Glide


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

Der verbindliche Glide-Originalvertrag liegt in `glide-to-do/01_Repository/Glide/docs/DESIGN_RICHTLINIEN.md` (in den GitHub-Quellen geprüft, **nicht** vollständig ins ZIP kopiert). Dazu `ARBEITSRICHTUNG.md` für D66–D77 und die hochgeladene Glide-System-Dokumentation. Nicht blind Markenidentität oder Eigentum von Glide übernehmen.

**Bleibt erkennbar:** hochwertiger heller/dunkler/automatischer Oberflächenmodus; eigenständige Widgets für Scrollbars, Optionen, Fortschritt, Buttons; klare Hierarchie Logo → view title (Akzentfarbe) → Subtitle/Status → Suche → Arbeitsfläche; Icons/Befehlsleisten, keyboard focus, Hover, symbol Fallback, Fenster-/Kompaktregeln, Notiz-/Textfläche, Dialoge, Notification- und Release-Card-Mechanismen, pixelgenaue Fluchten. Sidebareinträge müssen auch im deaktivierten Zustand sichtbar und erreichbar/erklärbar sein, ohne Todo-Aktionen auszulösen.

**Wird Steps-spezifisch entschieden:** Name, eigenes Logo/Icons, App-Bundle-ID, Default-Akzent, Wortwahl, Menügruppen, Seitenlistentaxonomie, Fach-Workspace, Status für Funktionen, Tooltips. Die lokale Glide 3.53-Schriftwahl Rubik, DM Mono, DM Serif Display, Charis SIL ist **nur Quellenstand**; Fontrechte, OS-Verfügbarkeit und realen Renderer prüfen, keine Fontdateien im ZIP.

**Abnahme:** Grundfarben/Kontrast ≥4,5:1 für normalen UI-Text, typografische Größen/Zeilenhöhen, 860×700 und 1280×800 sowie DPI-/Font-Skalierung, Dark/Systemwechsel, nur symbolische Werkzeuge mit Accessible Name, Mouse und Keyboard; Timing bei Animation/Tooltip, Windows/Mac/Linux. Manuelle Vorher-/Nachher-Freigabe bleibt separat. Keine 1:1-Bildpixel-Übernahme der Glide-Markenassets.

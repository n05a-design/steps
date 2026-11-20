# Desktop-Oberfläche

Die Tkinter-Oberfläche implementiert die zwei Bereiche aus ADR-001. Das Hauptfenster verkabelt Editor, Inspektor und Projektaktionen. Eigene Module enthalten die Bibliothek, das Stimmführungslabor und das MIDI-Exportstudio. Der [Harmonie-Inspektor](harmonic_inspector.py) formatiert Akkorddaten und Tastaturvoicings unabhängig von Tkinter. Der Controller vermittelt zwischen Widgets und Musikkern. Auf Aqua verwenden die Schaltflächen die native ttk-Palette. Die Glide-Roadmap beschreibt eine mögliche weitere Entwicklung.

[Dialog-Unterstützung](dialog_support.py) verwaltet Fokus, modalen Grab und
Escape für Bibliothek, Stimmführungslabor und MIDI-Export. Projektkürzel sind
an das Hauptfenster gebunden. Schreibgeschützte Vorschauen unterstützen
Tab, Umschalt+Tab sowie Bild auf und Bild ab.

| Einstieg | Inhalt |
| --- | --- |
| [Architektur-Übergabe & Glide-Roadmap](../../docs/architecture/APP_SHELL_HANDOVER_AND_GLIDE_ROADMAP.md) | Verbindlicher Übergabekontrakt und Status der Shell für alle KI-Agenten. |
| [Shell-Architektur](../../docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md) | Spezifikation des konservativen Rückbaus von Glide 3.53.0 zur 2-Bereiche-Shell. |
| [Gestaltung](../../design/README.md) | Design-Tokens (`design/tokens/tokens.json`) und Barrierefreiheits-Vorgaben (WCAG 2.1 AA). |
| [Native UI-Prüfung](../../tests/native_ui/README.md) | Geplante Bedien- und Plattformabnahme. |

[Zur Bereichsübersicht](../README.md)

# Desktop-Oberfläche

Vorgesehener Bereich für Ansichten, Navigation und Interaktion der STEPS-Desktop-Applikation.

> **Wichtiger Architektur-Hinweis für Entwickler & KI-Agenten:**  
> Die aktuelle Implementierung in `main_window.py` ist ein **vorläufiger, isolierter CI-/Referenz-Skeleton** (reines Tkinter ohne Glide-Code) zur Absicherung des Layout-Vertrags aus ADR-001 und des `--headless`-Modus.  
> Die finale Übernahme und Entkopplung der vollwertigen Desktop-Shell aus **Glide 3.53.0** erfolgt gemäß den Phasen R0 bis R4, sobald die Wissensbasis vollständig konsolidiert ist.  
> Siehe verbindliches Übergabedokument: [`docs/architecture/APP_SHELL_HANDOVER_AND_GLIDE_ROADMAP.md`](../../docs/architecture/APP_SHELL_HANDOVER_AND_GLIDE_ROADMAP.md).

| Einstieg | Inhalt |
| --- | --- |
| [Architektur-Übergabe & Glide-Roadmap](../../docs/architecture/APP_SHELL_HANDOVER_AND_GLIDE_ROADMAP.md) | Verbindlicher Übergabekontrakt und Status der Shell für alle KI-Agenten. |
| [Shell-Architektur](../../docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md) | Spezifikation des konservativen Rückbaus von Glide 3.53.0 zur 2-Bereiche-Shell. |
| [Gestaltung](../../design/README.md) | Design-Tokens (`design/tokens/tokens.json`) und Barrierefreiheits-Vorgaben (WCAG 2.1 AA). |
| [Native UI-Prüfung](../../tests/native_ui/README.md) | Geplante Bedien- und Plattformabnahme. |

[Zur Bereichsübersicht](../README.md)

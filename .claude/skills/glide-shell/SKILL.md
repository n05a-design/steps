---
name: glide-shell
description: Anleitung und Regeln für die Nutzung der Glide Shell in diesem Projekt. Verwenden bei UI-Entwicklung mit Tkinter, Dialogen, Tastaturkürzeln oder beim Aktualisieren der Shell.
---

# Glide Shell – Projektnutzung

Dieses Projekt verwendet die **Glide Shell** als UI-Fundament.

## Wichtige Referenzen

- Anleitung: [KI_ANLEITUNG_NEUE_PROJEKTE.md](../../../glide_shell/KI_ANLEITUNG_NEUE_PROJEKTE.md)
- Startprompt: [STARTPROMPT_KI.md](../../../glide_shell/STARTPROMPT_KI.md)
- Portabler Designvertrag: [DESIGN_RICHTLINIEN.md](../../../glide_shell/DESIGN_RICHTLINIEN.md)
- Manifest: [SHELL_MANIFEST.json](../../../glide_shell/SHELL_MANIFEST.json)

## Regeln

- Dateien in `glide_shell/` nicht manuell ändern.
- Vor und nach UI-Arbeiten: `python3 -m glide_shell.selftest` (Windows: `python -m glide_shell.selftest`).
- Designvertrag (P1–P6, B15, B11, Kontrast, Fokus) beachten.

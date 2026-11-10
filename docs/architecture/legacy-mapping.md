# Provenienz-Mapping der Altstruktur

| Alter Pfad | Schritt 1 | Ziel / Begründung |
| --- | --- | --- |
| `01_Projektkonsolidierung/01_Overview/` | Verschieben | `docs/project/overview/` |
| `01_Projektkonsolidierung/02_Technischer_Anhang/` | Verschieben | `docs/project/technical-appendix/` |
| `01_Projektkonsolidierung/03_Quellenabdeckung/` | Verschieben | `docs/project/provenance/` |
| `01_Projektkonsolidierung/04_Originaldokumente/` | Verschieben | `docs/project/originals/` |
| `01_Projektkonsolidierung/README.md` | Verschieben | `docs/project/ARCHIVE_README.md` |
| `01_Projektkonsolidierung/SHA256SUMS.txt` | Verschieben | `docs/project/provenance/HISTORIC_SHA256SUMS.txt`; *alte Pfadbezüge bleiben historisch* |
| `02_Bibliothek/README_STEPS_BIBLIOTHEK.md` | Verschieben | `knowledge/legacy/STEPS_BIBLIOTHEK_README.md` |
| `02_Bibliothek/create_steps_v6_7*.py` | Verschieben | `tools/legacy/generators/` |
| `00_Arbeitsvorbereitung/Steps_Deep_Research_Gesamtpaket/` | Verschieben | `research/notes/deep-research/legacy/` |
| `00_Arbeitsvorbereitung/Erster-Skill-Entwurf – music-harmony-coach/` | Verschieben | `skills/music-harmony-coach/` (bestehende Unterstruktur erhalten) |
| `02_Bibliothek/STEPS_Bibliothek/**` | **Unverändert** | komplexes Legacy-/Lizenz-/Linkaudit |
| `00_Arbeitsvorbereitung/**` (übrig) | **Unverändert** | externe PDFs, HTML-Caches, Audio, MIDI, unklare Rechte |
| `03_Konkurrenz/**` | **Unverändert** | zahlreiche bitidentische Kopien, Fremdmaterial |
| `20_Grafik_Master/**` | **Unverändert** | externe Inspirations-/Designrechte prüfen |

Hinweis: Alte Texte können interne relative Verweise enthalten, die nach `git mv` angepasst werden müssen. Phase 1 erhält die Belege und weist offene Verweise aus, behauptet aber keine abgeschlossene semantische Reorganisation.

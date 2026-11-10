# Automatisch erzeugter Python-AST-Index – lokaler Glide-Code 3.53.0


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

Quell-Datei: `source_archive/Glide-Aufgaben-und-Listen_v3.53.0.pyw` (69.015 Zeilen). Statisch geparst, **nicht ausgeführt**; alle Top-Level-Funktions-/Klassenmethoden sind vollständig mit Anfangs-/Endzeilen in `GLIDE_AST_METHOD_INDEX.csv` erfasst. **39 Top-Level-Klassen, 35 globale Funktionen, 2648 Klassenmethoden, davon 1866 direkte `ListApp`-Methoden**.

## Besonders relevanter Code

| Symbol / Aufgabe | definierte Zeile |
|---|---:|
| `defer_window_menu_commands` | 47 |
| `get_app_data_dir` | 387 |
| `ListApp` | 15533 |
| `toggle_sidebar_section` (`ListApp`) | 26358 |
| `show_settings_dialog` (`ListApp`) | 31172 |
| `create_list_sidebar` (`ListApp`) | 37695 |
| `sync_header_action_host` (`ListApp`) | 43761 |
| `update_header_title` (`ListApp`) | 44254 |
| `save_window_geometry` (`ListApp`) | 45312 |
| `set_search_placeholder` (`ListApp`) | 49373 |
| `clear_search` (`ListApp`) | 49636 |
| `focus_search` (`ListApp`) | 49644 |
| `sync_header_logo` (`ListApp`) | 53593 |
| `toggle_sidebar_narrow` (`ListApp`) | 66255 |
| `toggle_sidebar` (`ListApp`) | 66327 |
| `enter_compact_mode` (`ListApp`) | 66379 |
| `leave_compact_mode` (`ListApp`) | 66418 |

**Nicht** aus Methodennamen direkte Portierbarkeit ableiten; Referenzen/Datenpfade/Side Effects in vollem Repo prüfen.

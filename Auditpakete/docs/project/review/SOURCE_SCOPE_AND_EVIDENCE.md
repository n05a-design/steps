# Quelle, Verifikation und Untersuchungsgrenze – STEPS V5

**Prüfdatum:** 10.11.2026 · **Referenz-HEAD:** `1fc07e230dc6a2fe92fd6662da43e332d596b376`.

Diese Matrix grenzt den **wirklich durchgeführten Remote-Review** von der erst noch lokal auszuführenden Vollprüfung ab. Ein `read_excerpt` ist keine vollständige Lektüre. Git-Baum/Blob-Identität ist keine semantische Inhaltsprüfung.

| Evidenz | Referenz | Status des Reviews | Verifizierte Aussage bzw. verbleibende Grenze |
|---|---|---|---|
| STEPS Git-Tree | HEAD `1fc07e23`, `truncated=false` | `TREE_COMPLETE` | 3.768 Dateieinträge, 525 Verzeichnisse; keine Vollinhaltsprüfung |
| `AGENTS.md` | Blob `c26db85bb0b8a0c9f69a0f027d50e4952b26c03c` | `SELECTED_TEXT_REVIEW` | Preservation-first und differenzierte Produkt-/Fach-/Archivversionen |
| `README.md` | Blob `f6857cbfb3a7c8566574dff0e7a8ec889e4f89b6` | `SELECTED_TEXT_REVIEW` | Frühere Snapshot-SHA `75329fef` in gegenwärtig veröffentlichter Einleitung |
| `docs/project/PROJECT_OVERVIEW.md` | Blob `fcec8064f08f77218bc93c5b52aca5932353ad98` | `SELECTED_TEXT_REVIEW` | Umfangreiche V2-Prüfung, referenziert historischen STEPS-Snapshot |
| `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md` | Blob `b41ebac79770b1056fd72cfb97f436cd20a781fb` | `SELECTED_TEXT_REVIEW` | Glide-3.53-Shell-Spezifikation und konkrete Tests |
| `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md` | Blob `0c3ad3ffefe9d9372bb18d38f93a1b7a108826ae` | `SELECTED_TEXT_REVIEW` | Geplante zwei Bereiche; kein implementierter Port |
| `src/steps-0.00/README.md` | Blob `0fcd773d1f4c847fbeac608e4696e487b6450028` | `FULL_SHORT_FILE` | Noch historischer Titel `# src/steps`, Platzhalterbeschreibung |
| `tools/validation/check_structure.py` | Blob `ce873a440f9004cefde9734aa24624c732f16bbb` | `FULL_SHORT_FILE` | Verlangt weiterhin `src/steps` |
| `prompts/README.md` | Blob `3ae605d71a54548f7592ddf2f61704da629ea0cd` | `SELECTED_TEXT_REVIEW` | 29 Arbeitsaufträge mit 24+5-Fassung |
| `docs/project/Archiv/Projekt Overview.md` | Blob `da7e219d514d22c31eb1ce78e19d514dcc6d739b` | `HEADER_REVIEW` | Historische V6.6-/1.146-Dokumente-Behauptung, keine neue App-Zählung |
| `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` | Blob `f2b16e7e18c2f9f91b8c27003785d3bb78da3a8e` | `SELECTED_TEXT_REVIEW` | Historische Konsolidierung von sechs angehängten Dokumenten; keine vollständige Repo-Prüfung |
| Glide-Origin `main` | `9e767bea5e21063466a28ac3a679406484ad5d5f` | `COMMIT_AND_CI_METADATA` | Glide 3.53.0-CI-Erfolge gelten nur für Glide |
| STEPS CI Run `42842449461` | Commit `c0bceedc...` | `JOB_LOG_READ` | Strukturcheck scheiterte an `src/steps` |
| STEPS Run `42849387382` | Commit `1fc07e23...` | `WORKFLOW_METADATA` | Erfolgreicher Dependabot-/pip-Graph, **kein Strukturtest** |
| Doppelte Glide-Hauptdatei | Git-Blob `0fc522fb5faf9694dbd28d2ca43b1f415a010139` | `BLOB_IDENTITY` | Drei beobachtete Kopien bytegleich, keine Aussage über übrige Module |

**Unterscheidungsregel:** `TREE_COMPLETE`, `HEADER_REVIEW`, `SELECTED_TEXT_REVIEW`, `FULL_SHORT_FILE`, `JOB_LOG_READ`, `BLOB_IDENTITY` und `COMMIT_AND_CI_METADATA` sind **verschiedene Evidenzklassen**; keine wird zu `FULL_CONTENT_AND_SEMANTICS` hochgestuft, ohne dass die entsprechende Prüfung erfolgt.

Eine vollständige `SOURCE_REGISTRY` und per Datei belegte `DOCUMENT_COVERAGE` müssen erst in Antigravity lokal hergestellt werden. Die Begleitdokumente dieses Pakets sind damit eine belastbare **Arbeitsvorbereitung**, keine bereits abgeschlossene Gesamtrevision.

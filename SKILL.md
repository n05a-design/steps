---
name: steps-project
description: Einstieg und Arbeitsrouten für die STEPS-Entwicklung; kein eigenständiger musiktheoretischer Wissensspeicher.
---
# STEPS – Projekt-Workflow

1. **Kontext und Scope:** `README.md`, `docs/project/`, `docs/architecture/` prüfen.
2. **Fachliche Aussagen:** `knowledge/` und `knowledge/sources/registry.yaml` heranziehen; nur verifizierbare Belege nennen.
3. **Harmonieaufgaben:** Für freigegebene STEPS-Lerninhalte den Pilotkatalog über `app/knowledge.py` verwenden. Fachliche Aussagen mit den dort hinterlegten Fundstellen belegen. Forschungsdaten und historische Coach-Notizen als solche kennzeichnen.
4. **Migration:** `docs/architecture/migration.md` und das lokale Audit/Manifest verwenden.
5. **Umsetzung:** Die Musiklogik und ihre Tests in `src/steps/` weiterentwickeln. `app/` bindet sie an die Anwendung an.
6. **Abschluss:** Änderungen, Risiken, Quellen, Tests und nicht abgeschlossene Punkte übergeben.

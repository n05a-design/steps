# STEPS – ARCHIVE RESTORE GUIDE
## Anleitung zur revisionssicheren Wiederherstellung archivierter Dateien

Sämtliche im Rahmen der Konsolidierung nach `archive/` verschobenen Dateien sind in `ARCHIVE_MANIFEST.csv` mit ihrem ursprünglichen Pfad und SHA-256 Hash dokumentiert.

### Wiederherstellung einer einzelnen Datei
Um eine archivierte Datei an ihren ursprünglichen Speicherort zurückzuverschieben:

```bash
# Beispiel:
git mv archive/project-history/early-planning/bootstrap_steps.py ./bootstrap_steps.py
```

### Vollständige Wiederherstellung aller archivierten Dateien
Ein automatisiertes Rückrollskript kann die Spalten `source_path` und `target_path` aus `ARCHIVE_MANIFEST.csv` einlesen und mittels invertiertem `git mv <target_path> <source_path>` den exakten Ausgangszustand wiederherstellen.

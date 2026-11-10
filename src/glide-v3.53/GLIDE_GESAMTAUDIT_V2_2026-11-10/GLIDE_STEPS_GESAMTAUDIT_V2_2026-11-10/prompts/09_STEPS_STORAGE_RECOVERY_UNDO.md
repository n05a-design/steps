# Eigenständiger Steps-Datenpfad, Undo, Backup, Crash-Recovery

**Prompt-ID:** `09_STEPS_STORAGE_RECOVERY_UNDO` · **Arbeitsart:** ANALYSE; Implementierung nur für autorisierte Ports · **Roadmap:** P6

> Lies zuerst `00_AGENTENVERTRAG.md` und die aktuellen Projekt-`AGENTS.md`. Dieser Prompt ist nicht die Freigabe für Remote-Änderungen.

## Begründeter Eingang / Primärquellen

Glide `docs/06_DATA_BACKUP_MIGRATION.md`, `persistence.py`, `data_lock.py`, `session_guard.py`, `backup_snapshot.py`, `undo_history.py`, Steps `app/core/`, Schemas und geplante RuntimePaths.

## Fachlich konkreter Arbeitsauftrag

Definiere `STEPS_DATA_DIR`/RuntimePaths vor jedem Modulimport, getrennte App-ID, Lock-/Backup-/Log-/Cache-/Temp-Pfade, `read_only` bei neuer inkompatibler Schema-Version, atomare SaveResult-Grenze und Crash-Migration. Verfolge Save/Undo/Redo bei gleichzeitiger UI-Vorschau und zwei Views, stabile IDs und Cacheinvalidierung. Unterscheide fehlgeschlagene Serialisierung, ausfallende Sicherung, fehlerhaften Tempfile-Commit, verloren Lock, Erfolg mit späterer GUI-Exception und Hard-Exit beim OS-Flush. Führe Dateigröße, Pfadlängen, OneDrive-/Symlink-/ZIP-Importgrenzen und externe MIDI-Assets explizit. Definiere Recovery-Konflikte und menschliche Auswahl statt automatischer Datenüberschreibung. Keine angenommene Glide-kompatible JSON-Datei: separate Steps-Schema-/Migrations-Roundtrip-Tests erforderlich.

## Reproduzierbare Abnahmen und Gegenproben

Fault Injection vor/nach `os.replace`, zwei Prozesse auf identischer Steps-Datei, unbekannter zukünftiger Schema-Stand, zerbrochene Backupdatei, verwaiste Tempfiles, Snapshot während Undo, langer unicode Pfad, Neustart nach Crash. Negative Test: Steps beim Start darf selbst mit falschem Default keine Glide-Userdatei ändern. `NO_REAL_DATA` Verzeichnis-Spy vor Testlauf verifizieren.

## Ergebnis und Übergabeformat

`DATA_CONTRACT.md`, `SCHEMA_MIGRATION.md`, `FAULT_MATRIX.csv`, `BACKUP_RESTORE_PROOF.md`, `OWNERSHIP_MAP.csv`, genaue Testkommandos nach isolierter Reproduktion.

Nutze das exakt dokumentierte Format des Agentenvertrags mit `PASSED/FAILED/SKIPPED/NOT_RUN`, vollständigen Quell- und Laufzeitangaben. Weise zu jedem Blocker die kleinste mögliche Folgeprobe und das verantwortliche Gate aus.

## Grenzen und STOP

Fehlt die Sicherung, Datenmigrationsstrategie oder der einzelne Mutationspfad, keinen Datenformat-PR freigeben. Kein nicht rückgängig zu machendes Restore auf echten Benutzerdateien.

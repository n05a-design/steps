# Steps – Datenmodell, Persistenz, Recovery, Migration und Portabilität

**Status:** technische Soll-Definition und Prüfgates; weder lauffähiges Steps-Dateiformat noch Abnahme wurde nachgewiesen. Vorbilder: Glide-Daten-/Backup-/Undo-Architektur, aber nicht dessen Todo-Schema `Format 26` übernehmen.

## 1. Drei unterschiedliche Speichersphären

1. `AppSettings`: Steps-eigene Theme-, Font-, Fenster-, Notations- und Accessibility-Settings. Pfad unter `Steps`, eigene Applikations-/Bundle-ID; **niemals** `Glide`, `glide.lock`, `liste_speicher.json`, `settings.json` oder Glide-Nutzerdaten schreiben. Einstellungen getrennt vom Musikprojekt, optional auf Projekt überschreibbare Optionen explizit modelliert.
2. `StepsProject`: Nutzerkomposition, z.B. `project_id`, `schema_version`, `title`, `tracks`, `timebase`, `meter_map`, `tempo_map`, `chords`, `drum_events`, `analysis_overrides`, `source_refs`, `view_state`, `assets`. Musikzeit quantisiert in deklarierter PPQ; `Event` mit `start_tick`, `duration_tick`, Track, ID, Status und Content. Keine Einzelstrings als alleinige musikalische Wahrheit.
3. `Knowledge/Research`: geprüfte Fachobjekte, Roharchive und private Quellen mit eigenen Versions-/Rechte- und Zugriffspolicys; **keine** stille Einbettung geschützter Bücher in Nutzerprojekte oder exportierte `.zip`.

## 2. Entwurf eines transaktionsfähigen Speichervorgangs

`ViewState` → validiertes `DomainSnapshot` → schema-/reference-check → write temp same filesystem → flush + `fsync` abhängig von Plattform → atomarer Replace → Verzeichnis-Sync wo unterstützt → SaveResult/Backup Manifest → UI Status. Dies ist kein Beweis für vollständige Crash-Sicherheit auf beliebigen Netzwerk-/Sync-Dateisystemen. Beim Fehler bleibt die vorherige Hauptdatei lesbar, der `dirty`-Status unverändert und das UI meldet Ursache und Wiederholbarkeit. UI-Folgeeffekte dürfen nicht den Erfolg der Hauptdatei umetikettieren; `Undo`-Historie und Commitgrenzen getrennt definieren.

**Aus Glide zu prüfen, nicht blind zu übernehmen:** `persistence.py`, `save_result.py`, `backup_snapshot.py`, `schema_backups.py`, `data_lock.py`, `session_guard.py`, `runtime_diagnostics.py`, `load_phases.py`, `undo_history.py`. Diese Komponenten können Pfade, Begriffe und Datenformat implizit an Glide binden. Nur nach neutralen Ports und negativen Nichtzugriffs-Tests übernehmen.

## 3. Versionierung ohne Sackgasse

- Explizites `schema_version` **im** Projekt und unabhängig von `Steps.VERSION`.
- Read-only-Load neuer unbekannter Versionen oder klare Ablehnung **ohne automatisches Überschreiben**.
- Jede Migration `N→N+1`: deterministisch, dokumentiert, fixture-getrieben und mit Backups; ursprüngliche Datei bleibt als Referenz erhalten.
- Für importierte MIDI/MusicXML/JAMS: standardbedingte Informationsverluste `loss_report` erzeugen (z.B. Harmonieanalyse, ungewohnte MIDI-Metaevents, enharmonische Schreibweise).
- `source_id` ist kein eingebetteter Originaltext; bei fehlender Referenz wird das Projekt trotzdem geöffnet, mit sichtbarer Quellenlücke.
- User-Files und Installationspakete strikt getrennt; Systemdateiberechtigungen und portable Installation gegentesten.

## 4. Threat Model und Fehlerklassen

| Fehler | Erkennung | vorgeschriebene Reaktion |
|---|---|---|
| defektes JSON/Schema | Parserlimit, schema_version/required fields | nicht überschreiben; Restore-/Exportangebot |
| unbekannte neuere Version | Versionen vergleichen vor Mutation | read-only oder erklärtes Abbrechen |
| zerrissener Schreibvorgang | Temp-/Hauptdatei-Konsistenz, Hash | letzter valider Snapshot/Backup |
| paralleler Zugriff | PID/Session Lock, Alters-/Ownershipprüfung | kein blindes Lock-Stehlen; Konfliktdialog |
| extern synchronisierte Dateikopie | Content-Hash/ETag vor Commit | Seitendatei, Warnung, keine stille Zusammenführung |
| Pfad-Traversal im Import | Normalisierung, rooted paths, symlink | Reject/Quarantäne |
| ZIP-Bombe, Riesen-MIDI | Byte-, Event-, Expanded-Size-, Laufzeitgrenzen | bounded failure, keine UI-Blockade |
| fehlendes Font-/Audio-Gerät | Software-Fallback | Projekt bleibt lesbar und speicherbar |
| abgestürzter Plugin-/AI-Agent | Timeout, idempotent command | kein inkonsistenter Projekt-/Knowledgezustand |
| OS-/Tk-Lifecycle | Worker-Generation und UI-Root-Validierung | keine zerstörte Widget-Callbacks |

## 5. Beispiel einer minimalen Testmatrix (nicht ausgeführt)

`IO-01` frische Steps-Datenroot; `IO-02` zweimal speichern, gleiche Bytes nach Normalisierung; `IO-03` Schreibfehler vor Replace; `IO-04` Fehler nach Replace vor UI-Bestätigung; `IO-05` Reopen/Undo nach Crash; `IO-06` falsche `schema_version`; `IO-07` neuere Version nur lesend; `IO-08` 1000 Chords + MIDI + Drums mit künstlichen Zeiten; `IO-09` fremde `Glide`-Root bleibt SHA-identisch; `IO-10` `.mid`-Roundtrip und ausdrücklicher Verlustbericht; `IO-11` Pfad Traversal in ZIP und Assets; `IO-12` Backup/Restore mit inkompatibler Schema-Version; `IO-13` zwei Prozesse/Lock; `IO-14` ekliger synchronisierter Schreibkonflikt; `IO-15` kaputter Font und kein Sounddevice; `IO-16` Unsigned/Packaged Neuinstallation und Benutzerdatei außerhalb Programmpfad.

**Technische Alternative:** JSON-Datei für kleine offline Projekte und klaren Diff-Workflow, SQLite nur bei begründeter Performance-/Transaktionsanforderung oder großer Objektmenge. Eine SQL-Datenbank löst keine fehlerhafte Fachmodellierung oder unklare Datenmigration. Auswahl mit identischen Real-World-Fixtures und Performanceprofil.

## 6. Entscheidergebnis

**Vor Implementierung erforderlich:** schriftlich freigegebene Steps-Projektformat-Skizze, eigene `APP_ID`, `DATA_DIR` und `CACHE_DIR`, No-Glide-Touch-Test, golden IO-Fixtures und die Definition des Wiederanlaufs. Die bisherige Glide-Stabilität ist ein wertvoller Ausgangspunkt, aber keine Behauptung eines Steps-IO-Testpasses.

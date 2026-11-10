# Steps Qualität, Sicherheit, Rechtsgrenzen und CI

## Eigene Achsen für „grün“

| Gate | Nachweis | Nicht ausreichend |
|---|---|---|
| Dokumenten-Audit | Originalabdeckung, SHA, Links, Versionen, W/G/DEC-Crosswalk | README besteht |
| Domain | Python-Tests: Akkord-/Zeit-/Tempo-/Spelling-Modelle, Goldencases, Negativfälle | `app/`-Verzeichnisse existieren |
| MIDI | unabhängiger Parser/DAW; PPQ, Delta-Time, Note-Off, Tempo/Meter/Tracks | Dateiname `.mid` existiert |
| Persistenz | Roundtrip, atomarer Commit, Fehler vor/nach Save, Lock, Backup, Schema-Migration | ein einmaliger Happy Path |
| Shell | UI-Bilder, Focus/DPI/Keyboard, ein-/ausklappbare Sidebar, beide Pane-Hosts, 1000 Wechsel ohne Lifecycle-Leaks | importierbare Tk-Module |
| Audio | gesonderter Scheduler-/Backend-/Sampletest, Latenz, Stop/Panic, Lizenz der Soundbank | MIDI-Export |
| Rechte | pro ausgeliefertem Asset Zustimmung/Lizenzstatus, Quellbezug, Third-Party-Notices | Code-LICENSE = MPL-2.0 |
| Paket/Release | native Start, Hash, BOM, Signierungs-/Verteilentscheidung, Human QA | GitHub-Workflow „success“ |

## Kritischer CI-Gegenbefund

`.github/workflows/structure-check.yml` hat `paths`-Filter, die `src/**` und `app/**` nicht einschließen. So kann ein reiner Musikcode-PR an diesem Workflow vorbeigehen. Ein Required Check, der wegen Pfadfilter nicht läuft, ist kein Ersatz für einen robusten PR-Gate. Der Workflow prüft derzeit Struktur, **nicht die Musikdomäne**. Empfehlung: neuen, unbedingten PR-Workflow mit `pytest` (getrennt pure core und GUI), `python -m compileall`, Schematests/Provenienzkontrolle; erst nach echten Runs Required-Check-Namen im GitHub-UI fixieren.

## Threat-Modell in Kurzform

- Untrusted ZIP/Archive: Traversal, Symlink/Junction, ZIP-Bomb, Dateigröße, komprimiert/unkomprimiert, maximale Entryzahl, UTF-8/Unicode-Normalisierung.
- Untrusted MIDI/MusicXML: Größenbudget, Time-Deltas und maximale Events, Rekursion, invalide Tempo-Map, unbekannte CC/Metaevents, Xml-Entities, Thread-/Device-Timeout.
- Nutzerdateien: keine Glide-Verzeichnisse; eigene Steps-ID und sichere Dateipfade; kein ungesicherter overwrite, reversible Migration, Restore-Probe.
- Agententools: Terminal/Bash/PowerShell nicht ungeprüft aus Repo-Text ausführen; unbekannte Generatoren und V2-Installer sind nicht vertrauenswürdig; ausführbare Skripte erst lesen, mit Sandbox und künstlichen Dateien testen.
- Shared Module: kein `app.pyw`-Import als Paketnebenwirkung, keine Runtime-Caches über Tk-Interpreter-Grenzen, keine sensiblen Details in Logs.

## P0 Sicherheitswarnung aus vorherigem V3-Audit

Der mit früherem V2-Dokumentationspaket ausgelieferte `safe_install_v2.py` hatte einen isoliert **reproduzierten Symlink-Pfad-Ausbruch**. Nicht ausführen. V3-Ergänzung hatte neun isolierte positive/negative Tests, aber keine uneingeschränkte Windows-Junction/TOCTOU-Sicherheit. Dieses Paket enthält daher **keinen Installer**, sondern ausschließlich neue Markdowndateien plus SHA-Manifest; Copy/Import bleibt menschlich kontrolliert.

## Abschlussbericht je KI-Auftrag

Quell-SHA, Datenformat, Branch, geplante vs. ausgeführte Dateien, Tests mit OS/Tk/Python/Logs, `PASS/FAIL/SKIPPED/NOT_TESTED`, Security-Review, Rechte, offene Entscheidungen, keine unbelegte Freigabe. Quelle/Resultat/Schlussfolgerung stets auseinanderhalten.

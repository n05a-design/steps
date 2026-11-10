# Rechte, Sicherheitsmodell, Repository-Historie und Release-Entscheidungen

**Vermerk:** Fachliches Risiko-Audit, keine anwaltliche Beurteilung einzelner Werke. Im öffentlichen Steps-Git-Baum sind nach dem verifizierten Snapshot 60 PDFs und viele heruntergeladene HTML-, JavaScript-, CSS- und MIDI-Dateien vorhanden. **Aus bloßer Existenz folgt weder ein Rechtsverstoß noch ein Nutzungsrecht.** Priorisierte Originalprüfung erforderlich.

## 1. Fünf Rechteobjekte auseinanderhalten

| Objekt | Mögliche Rechtslage | Veröffentlichungs-Gate |
|---|---|---|
| eigener STEPS-Sourcecode | Repository `LICENSE` ist MPL-2.0 | Datei-SPDX und Abhängigkeiten prüfen |
| aus Glide kopierte eigene/mitwirkende Python-Dateien | in Glide MPL-2.0 und ggf. zusätzliche Drittbestandteile | Herkunft, Copyright, unveränderte Lizenzhinweise, Modifikationshistorie |
| externe Bücher/PDF-Scans/E-Books | oft Verlagscopyright, Editionen unterschiedlich | nur nach Einzelfallreview und ausreichender Erlaubnis distribuieren |
| Musik-/MIDI-/Drumloops/Soundfonts/Audio | Kompositions-/Aufnahme-/Sample-Rechte getrennt; Nutzungsbedingungen pro Asset | kein öffentliches Bundling ohne konkrete Rechtekette |
| Webseiten/Fonts/Icons/UX-Screenshots | Content, Code und Design können unterschiedliche Lizenzen haben | Asset-Manifest und Nachweis je Datei |

Mozilla erläutert ausdrücklich die *file-level copyleft*-Eigenschaft der MPL-2.0; sie befreit nicht fremde PDF-Inhalte: https://www.mozilla.org/en-US/MPL/2.0/FAQ/ . Das Projekt-`LICENSE` ist nicht automatisch ein Rechtebeleg für jede im Repository abgelegte Datei. Quellcode-Verbesserungen unter MPL haben eigene Distribution-/Sourcebereitstellungsregeln. Test-/Datenartefakte, proprietäre Testfonts und externes Demoaudio sind separat zu prüfen.

## 2. Sofortiges Audit des öffentlichen Repositories – ohne übereilten History-Rewrite

**P0:** verlässlichen aktuellen Git-Tree-, Branch-/Tag-/Release- und Fork-Snapshot erfassen, priorisierte 60 PDF-/Web-/Medien-Scope-Liste erzeugen; bei jeder externen Datei Titel, Autor/Publisher, Herkunfts-URL, Erlaubnis, Nutzungsart, öffentliche Historie und Reviewstatus. Priorität hoch für gewerblich verbreitete Lehrbücher, Dateien mit ungewöhnlichen Downloadnamen, mitgelieferte kommerzielle MIDI-/Live-Set-Pakete und fremde Designbilder. In einem separaten geschützten Audit keine geschützten Volltexte reproduzieren.

Eine Datei aus `main` zu entfernen, entfernt nicht automatisch frühere Commits. GitHub beschreibt bei History-Rewrites Risiken für PRs, SHA-Referenzen, Forks und andere Klone: https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/removing-sensitive-data-from-a-repository . Die GitHub-Anleitung bezieht sich schwerpunktmäßig auf sensible Daten; bei urheberrechtlichen Problemen ist zusätzlich eine passende rechtliche Einschätzung zu möglichen Schritten notwendig. **Keine automatische Empfehlung**, Git-Historie ohne Freigabe umzuschreiben oder alle PDF-Dateien ungeprüft zu löschen.

## 3. Threat Model: Ingestion und Entwicklungsagenten

**Externe, nicht vertrauenswürdige Eingaben:** Webseiten/Transkripte mit Prompt-Injection; ZIP-Path-Traversal, symlinks und Zip Bombs; defekte MIDI-Dateien; große PDFs/Scans mit Ressourcenexhaustion; HTML mit nicht beabsichtigten Remote-Assets; Metadaten mit zu langen Pfaden oder Unicode-Verwechslungen; manipulierte Lock-/Backup-Dateien.

**Agenten:** Schreibrechte auf `main`, Nutzerdateien, private Quellen, Secrets und Release-Keys minimieren. Lesen, Extrahieren, Review und Publizieren als getrennte Berechtigungsstufen. Keine Shell-/Git-Aktionen aus Dokumentinhalt oder automatisch gefundenen „Anweisungen“. Jede externe Quelle bleibt Dateninhalt; nur ein autorisierter Auftrag darf Agentenrechte erweitern. KI-Anbieter und Tokenkonten haben unterschiedliche Datenschutz-/Lizenzbedingungen; private PDF-Originale nicht wahllos zwischen Diensten übertragen.

**App:** Musikprojekte und research archives getrennt; systemeigene Font-/Audio-Backends auf Plattform prüfen; Dateidialoge, Drag/drop und `open with`-Mechanismen mit Path-Validation. Logging enthält ohne Zustimmung keine unveröffentlichten Noten-/Kompositionsdaten oder Buchvolltexte.

## 4. Governance: Status, Versionen, Entscheidungen

Getrennte Versionsachsen: `Steps-App`, `Steps-Project Schema`, `Knowledge Snapshot`, `Source-Crawl Batch`, `Skill`, `Glide-System Reuse Contract`, `Glide-App Baseline`, `Documentation`. Alle Snapshots brauchen Git-SHA, Datei-/Manifesthash und Erstelldatum. Historische V6.6/V6.7-Zahlen und frühere Glide-3.50.x-QA-Ergebnisse sind **datierte historische Aussagen**, kein aktueller Releasebeleg.

Jeder ADR nennt Alternativen, Rechte-/Sicherheitsfolgen, Daten-/Regressionseffekte, Reviewer, gewählte Option, Gründe und Rollback; bei Revisionsentscheidung `supersedes` statt stille Umdeutung. KI-Agenten dokumentieren Promptversion, verwendete Repo-SHA, neue/alte Dateien, genutztes Quellmaterial, Tests, nicht ausgeführte Checks und Entscheidungsvorbehalte. Ownership von App-, Produkt-, Forschungs- und Veröffentlichungsentscheidungen nicht implizit auf einen Agenten übertragen.

## 5. Release und Supply Chain

- Python/Tk/OS-Mindestversionen erst nach Builds auf allen drei Zielplattformen festlegen.
- Dependencies, tkinterdnd2, Fontdateien, Logo-Master, Soundbank, Packaging und Lizenz-BOM pro Release aus konkreten Files erzeugen; SBOM-Format und Abdeckung offenlegen.
- Getrennte binäre Builds und Smoke-Tests; notarisiert/signiert nur wenn nachgewiesen. Keine Glide-Bundle-ID, keine Glide-Userdatenpfade.
- Upgrade- und Rollback-Pfad mit künstlichen Projects, Settings, Backups und Zeit-/MIDI-Fixtures testen.
- Öffentliches GitHub-README, Release-Beschreibung und Screenshots nur für *tatsächlich* ausführbare, geprüfte Funktionen.

**Aktueller Gate-Status:** keine signierte Steps-Releasefreigabe, keine geprüfte Third-Party-Asset-Matrix, keine vollständige Historien-/Lizenzbereinigung. Zeitkritischer und vom App-UI unabhängiger P0-Strang.

# Quellen-, Widerspruchs- und Lückenregister

## Quellenhierarchie und Belegstatus

| Quelle | Typ | Geltung |
|---|---|---|
| `docs/project/Archiv/*` + originale A–F | HISTORISCH | Originale unverändert; damit jede historische Behauptung rückverfolgbar bleibt |
| `docs/project/overview/Steps_Projekt_Overview_konsolidiert_2026-11-09.md` | BESTEHENDER MASTER | konsolidiert sechs Originaltexte; dort W01–W40 und G01–G34; keine unabhängige Verifikation aller Quellen |
| `STEPS_Masterreview_V3_2026-11-10.md`, `STEPS_Historienregister_100_V3.csv` (Nutzerbibliothek) | NEUERES REVIEW, NICHT ALS REPO-MASTER BELEGT | 26 Dimensionen; 40 W + 34 G + 26 DEC mit Crosswalk; kein automatisches „closed“ |
| Steps GitHub SHA `75329fef...` | DIREKT VERIFIZIERTER REMOTE-SNAPSHOT | Baumstruktur, README, Lizenz, Workflow, Registry, Skill; nicht lokale Dateien |
| Glide GitHub SHA `9e767bea...` | DIREKT VERIFIZIERTER REMOTE-SNAPSHOT | App-Version 3.53.0, System 1.15, PR #75; nicht lokale Copilot-Dateien |
| Glide-Übergabe und QA | DOKUMENTIERTE LOKALE BEFUNDE | ein lokaler Windows-Freeze 130/131; bleibt SHA-/Plattformgebunden |

## Aktuelle Konflikte / Widersprüche (bestehende historischen 40 W separat aufbewahren)

| ID | Konflikt / Lücke | Bewertung | Handlung / Owner |
|---|---|---|---|
| C01 | Glide-Übergabe behauptet `main=61a2f3a`/3.50.7; Remote-`main=9e767bea`/3.53.0 | verifiziert, P0 für Agentenübergabe | Antigravity: HEAD/CI/Plan synchronisieren |
| C02 | 3.53.0 „lokaler Kandidat“ versus bereits gemergter PR #75 | verifiziert, P0 | datierten Status aktualisieren; vorheriges Statement als Historie belassen |
| C03 | Glide Windows-Freeze „grün“ versus `release_ready=false` | kein logischer Widerspruch, oft Missverständnis, P1 | getrennte Plattform-/Manual-/Packaging-/Lizenz-Gates schließen |
| C04 | 25 Glide-Pakete katalogisiert versus Framework angeblich verfügbar | unbelegte Entkopplung, P1 | zwei unabhängig getestete Verbraucher nachweisen |
| C05 | „zwei Fenster“ ohne Widgettopologie | Begriffs-/Architekturlücke, P1 | tatsächliche Tk-Hosts/Windows/Frames erfassen |
| C06 | Glide-Taskliste soll auf Steps-Seitenliste übertragen werden | Produktkopplungsrisiko, P1 | Seitenliste neutral darstellen, Fachaktionen ausschließlich Adapter |
| C07 | Steps-README beschreibt Chords, neuer Projektauftrag auch Drums | tatsächliche Scope-Differenz, P1 | PRD „M1 chord-only / M2 chord+drum“ festlegen |
| C08 | Steps-Struktur-CI erfolgreich, aber Musik-App nicht implementiert | Prüf-Scope-Missverständnis, P0 | ausführbare Domain-/Save-/MIDI-Gates und PR-CI aufnehmen |
| C09 | Steps-Workflow mit `paths`, `src/` und `app/` fehlen | verifiziert, P1 | unbedingte PR-Gate-Checks und echte Tests planen |
| C10 | Repository hat 1.931 Dateien, `knowledge/sources/registry.yaml` leer | Forschung ≠ kuratierte Knowledge-Claims, P1 | legaler Pilot Work/Edition/Asset/Claim; Import erst nach Review |
| C11 | Forschungsbibliothek V6.6/V6.7 mit wechselnden Zählungen | historisch ungeklärt, P1 | Population/Stichtag/Manifest getrennt verifizieren |
| C12 | öffentliche Dritt-PDFs, HTML/Webassets, Audio, Konkurrenzmaterial | Rechte offen, P0 für neue Veröffentlichung | keine weiteren Kopien; provenance- und rights-gesteuerte Triage |
| C13 | 426 zusätzliche SHA-identische Pfade (historisches Audit) | exakt gleich heißt nicht rechtlich löschbar; Zählung snapshotgebunden | vorsichtiges Inventar mit laufenden Git-Refs/Links; nichts automatisch entfernen |
| C14 | V2-Installer (`safe_install_v2.py`) hat dokumentierten Symlink-Escape | verifizierter alter Paketdefekt, P0 | nie ausführen; V3 nur nach Review/Hash/Windows-Check |
| C15 | GitHub-Regelschutz durch `protected`/Ruleset-Einzelergebnis interpretiert | Berechtigungs-/Governance-Lücke | Owner prüft reale Branchschutz-/Required-Check-UI |
| C16 | Steps-Rohmusiktimeline nicht fachlich spezifiziert | Schema-/Timing-Lücke | eigene ADR für PPQ, 4/4, Swing, Loop, Tuplet, Velocity |
| C17 | MIDI-Export als „abspielbar“ verstanden | Audioengine/SoundFont nicht beschlossen | Playback-ADR; reiner Export kein Audio-Test |
| C18 | H/B/Bb, Oktave, Slash-Chords, Harmoniefunktion | Notation/Modell unvollständig | Goldentests und fachlichen Review aufstellen |
| C19 | Glide-Lizenz MPL-2.0 und Steps-Lizenz MPL-2.0 = alle Quellen frei? | falsch | Drittassets je Werk/Asset und Nutzung prüfen; Marken trennen |
| C20 | „alles in Skill indexieren“ versus ungeklarte Rechte/Heterogenität | Prioritäts-/Compliance-Risiko | erst kuratierter Pilot und evaluiertes Retrieval |
| C21 | V3-Historienregister in Nutzerbibliothek, aber nicht als Repo-Master verifiziert | Provenienzlücke | V3 kontrolliert separat importieren, historische Master nicht überschreiben |
| C22 | lokaler Copilot-Stand möglicherweise abweichend vom GitHub-Stand | kritische Abweichung unbekannt | Antigravity liest echte `git status`, SHA und neue Dateien, synchronisiert nicht blind |
| C23 | Windows/Cloud-KI-Zugänge, Tokens, Modellversionen wechseln | Betriebsangabe, keine Architektur | Providerneutral, auf Testbeweise und Git-Artefakte setzen |
| C24 | Design aus Glide stammt aus bestimmter Marke | Urheber-/Branding-/Accessibilty-Risiko | neutrale UI-Tokens, eigenständige Steps-Assets, Credits |

## Nicht ausgelassene Quellen – Verfahren statt Dubletten

Die sechs Originale A–F behalten alle 2.612 Originalzeilen; 89 Bereiche wurden im Bestand kartiert. 40 historische W- und 34 G-Positionen sowie 26 DEC-Positionen bleiben im neueren V3-Registernachweis erhalten. Dieses additive Konfliktregister **ersetzt keine der 100 Positionen**, sondern verweist auf sie. Nur nach tatsächlich nachgewiesener Umsetzung + Test + Entscheidung `closed` setzen. Nicht erneut dieselben großen Übersichten kopieren und damit divergierende Wahrheitsquellen erzeugen.

## Noch unbelegte Bereiche

**Nicht semantisch vollständig auditiert:** sämtliche 1.931 Dateien, darunter große Teile von 840 Markdown-, 60 PDF-, 112 MIDI-, 16 MusicXML-, 87 HTML- und 262 Download-Dateien laut V3-Review. Der Bestand wurde auf Git-Pfadebene inventarisiert; tatsächliche Buch-/PDF-Inhalte, private Originalarchive, Quellrechte und lokaler Copilot-Stand bedürfen separater Prüfungen. Auch die bisherigen Werbe-/Marktangaben sind nicht auf 2026 aktualisiert.

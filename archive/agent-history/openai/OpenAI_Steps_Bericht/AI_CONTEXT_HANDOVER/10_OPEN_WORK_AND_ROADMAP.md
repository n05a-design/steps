# 10 – Offene Aufgaben und Roadmap
**Nachweislegende:** **G** = in dieser Sitzung über die GitHub-Verbindung direkt kontrolliert (nur ausdrücklich genannter Prüfgegenstand); **U** = Originalmeldung des Nutzers in der aktuellen Unterhaltung (meist Wiedergabe eines Antigravity-Abschlussberichts); **K** = eingeschränkte frühere Gesprächszusammenfassung; **A** = frühere Assistentenempfehlung/-auftrag; **D** = abgeleitete Bewertung, keine Repository-Verifikation; **X** = nicht zugänglich/nicht geprüft. Erfolgsmeldungen sind nicht automatisch unabhängig bestätigte Produkteigenschaften.

| ID | Prio | Arbeit | Maßnahme | Abnahme |
|---|---|---|---|---|
| NEXT-001 | P0 | OA-0001 Rechte-/History-Gate | Rechts- und Git-Blob-Fundorte auf redigierter Basis prüfen; Owner-Beschluss | keine produktive History-Operation ohne Freigabe |
| NEXT-002 | P0 | OA-0033 GitHub Alerts | Alerts #1–#3, AWS-Funde und Quarantäne-Baseline einzeln prüfen | nachweisliche Drittanbieter-/Eigentümer-/Expositionsbewertung |
| NEXT-003 | P0 | GitHub Stand aktualisieren | main @ 02f3776 und neueste Commits prüfen; PR #9 als merged berücksichtigen | kein Branch/Commit verwechseln |
| NEXT-004 | P1 | Remote Python CI abschließend prüfen | Runs 43097534590/43097015761 und Merge-Commit-Checks inkl. Jobs/Logs | Matrix 3.11/3.12 mit Resultaten und Testzähler |
| NEXT-005 | P1 | Core Tests unabhängig ausführen | Unit-/Integrationstests lokal und in CI reproduzieren | fehlerfreier ausführbarer Testnachweis auf Zielcommit |
| NEXT-006 | P1 | ADR-001 Fenster | Owner Option A/B entscheiden, Dokument signieren | kein GUI-Code vorher |
| NEXT-007 | P1 | ADR-002 MVP | Chords-only vs. Drums v0.2+ formell entscheiden | Scope/Tests/Roadmap abgeglichen |
| NEXT-008 | P1 | ADR-005 Notation | Pitch/Spelling und GUI-Darstellung formell abstimmen | EN/DE-Tests, DTO und Invarianten geklärt |
| NEXT-009 | P1 | Musiktheorie Grenzfallprüfung | Intervall, Enharmonik, Akkorde, Metrikraum, Counterpoint gegen Referenzen | konkrete unabhängige Assertions, keine Scheinbeweise |
| NEXT-010 | P1 | Claims-Quellen-Gap | 66 Claims mit Werken/Quellenbelegen crosswalken | keine unzugänglichen Quellen als vollgelesen ausgeben |
| NEXT-011 | P1 | Golden-Abdeckung | 198 Fälle getrennt von 28 Testmethoden auditieren | Testfall→Implementierung→Beleg-Matrix |
| NEXT-012 | P2 | 1.525 Metadata-Only-Quellen | risikobasierte Priorisierung für Core/Genre/Pädagogik | vollständige Prüfung nur für relevante Claims |
| NEXT-013 | P2 | Phase 5.2 spezifizieren | Chord-/Voicing-/Progression-Recommender mit Erklärung/Genreheuristiken | freigegebener Auftrag und belastbare Abnahmetests |
| NEXT-014 | P2 | Originaltranskripte liefern | fehlende alte Chats, Antigravity-Logs, lokale Audits exportieren | Rekonstruktions-Lücke schließen und Übergabestatus neu bewerten |
| NEXT-015 | P2 | Docs/Index aktualisieren | Kanonische Dokumentationslinks, Snapshot der Vollständigkeit | keine widersprüchlichen Einzelberichte |

## Keine stillschweigenden Entscheidungen
NEXT-006/007/008 erfordern formale Owner-Entscheidungen. NEXT-001/002 erfordern Sicherheits-/Rechtefreigaben. NEXT-013 ist ein **Vorschlag**, noch kein bereits erteilter Implementierungsauftrag.

## Empfohlene Fortsetzungssequenz
P0 Sicherheits- und Quellstand → P1 Remote-/lokale Tests und Fachgegenprüfung → Owner-Entscheidungen → P2 fachlich begründete Phase 5.2. Die Implementierung des schon vorhandenen Kerns darf nicht nochmals als unerledigt behandelt werden.

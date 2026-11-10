# Codex-Ausführungsauftrag – STEPS Ableton-Blog-Integration V6.6

## Unveränderliche Ausgangslage

Arbeite vom tatsächlichen STEPS-Repository aus. Vergleiche zuerst Arbeitsbaum, laufende Branches, Pfade, Lizenz- und Datenmodelle. **Nicht blind Dateien überschreiben oder mergen.** Dieses Paket ist Forschungsimport, keine Freigabe zur automatischen Repository-Mutation ohne Prüfung. Historische Versionen bleiben erhalten.

## Eingänge

- `10_QUELLEN_LIZENZEN/STEPS_QUELLEN__ABLETONBLOG_KUMULATIV_V6_2_BIS_V6_6__REGISTER__V6_6.csv` (262 Einträge)
- 63 Quellkarten im jeweiligen Fachbereich / `ABLETON_BLOG_V6_6`
- 12 originäre Transferlabor-Spezifikationen
- `10_QUELLEN_LIZENZEN/STEPS_ABLETONBLOG__V6_6-Downloads-Rechtepruefung__QUEUE__V6_6.md`
- `11_VALIDIERUNG_QUALITAET/STEPS_ABLETONBLOG__V6_6-Quellenabdeckung-Deduplikation-Rechte__AUDIT__V6_6.md`

## Arbeitspakete in Abhängigkeitsreihenfolge

1. Repository-Audit und Vergleich mit V6.5, Pfadnormalisierung, Rechte-/Lizenzanalyse.
2. Registrierung der Artikel als `source` mit stabiler ID, kanonischer URL, Zugriffs- und Rechte-Status.
3. Deduplikation auf normalisierter URL inkl. Sprachvarianten; ID niemals nachträglich recyceln.
4. Zuordnung jeder Quelle zu exakt einer Hauptdomäne und beliebigen Querdomänen.
5. Unterscheidung `metadata_verified`, `article_text_reviewed`, `embedded_media_unreviewed`, `asset_rights_unverified`, `peer_reviewed`.
6. Eigene Transferlabore als Experimente aufnehmen, NICHT als bereits validierte Produktionsregeln.
7. 4 exemplarische End-to-End-Workflows implementieren: MIDI-Swing, Kick-808-Envelope, Hocketing, Vocal-Mix. Nur eigene Testdaten benutzen.
8. Für Transformationsoperationen Seed/Provenienz/Parameterversion und reproduzierbare Ausgaben erzwingen.
9. Musiktheoretische Tests für Tonhöhen, MIDI-Zeitbasis, Grid-Schritte und Harmony-Parser getrennt.
10. Gegenprüfungen: gleiche Velocity != gleicher Groove; NoteOff != SoundEnd; Ducking != Basspause; Hocket != Harmonieanalyse.
11. Lizenzprüfung aller 10 neuen Download-Kandidaten, ohne automatischen Import fremder Assets.
12. `One Thing` und alte Tutorial-Jahrgänge systematisch über Archivseiten erfassen, mit Crawl-Fortschritt, Backoff und Rate-Limits.
13. Audiovisuelle Inhalte nur bei verfügbarer rechtmäßiger Quelle, mit tatsächlichem Reviewstatus auswerten.
14. Quellen->Konzept->Experiment->Test->optionale Produktfunktion als Traceability-Graph exportieren.
15. Parser-, Pfad-, Registry- und Rechtevalidatoren als CI-Tests; wissenschaftlicher Review bleibt eigene Freigabestufe.
16. Abschließender Bericht: Neue Artikel, doppelte Links, kaputte URLs, Quellenzugriff, Rechte, durchgeführte/fehlende Tests und konkrete Änderungen. Keine stille Merge-Aktion.

## Definition of Done

- Keine ungeprüften fremden Volltexte, Samples, Videos oder Live Sets im exportierten Wissenspaket.
- Für jede Quelle existiert Provenienz + transparenter Reviewstatus; jede URL ist eindeutig.
- Jeder Experiment-Claim verweist auf ein eigenes Testartefakt oder ist als Entwurf gekennzeichnet.
- Vorherige Bibliothek unverändert; alle tatsächlichen Repository-Diffs geprüft; keine ungenannten Behauptungen zu Kompatibilität.

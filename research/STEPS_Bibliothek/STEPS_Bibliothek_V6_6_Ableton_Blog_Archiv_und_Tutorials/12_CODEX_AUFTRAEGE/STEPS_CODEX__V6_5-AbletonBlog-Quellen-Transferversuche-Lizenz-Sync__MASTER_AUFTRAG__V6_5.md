# STEPS Codex – Ableton-Blog-Ingestion und Wissens-Transfer V6.5

**Grundlage:** `10_QUELLEN_LIZENZEN/STEPS_QUELLEN__ABLETONBLOG_KUMULATIV_199__REGISTER__V6_5.csv` mit 199 Artikeln; V6.4 vollständig unverändert; neue Quellenkarten und Transferstudien.

## Verbindlicher Arbeitsablauf

1. Repository, Branch, versionierten Bibliotheksstand und offene PRs feststellen; nichts ohne Test oder Freigabe überschreiben.
2. CSV-Register mit 199 Datensätzen einlesen und URL-Slugs sprachunabhängig normalisieren; vorhandene IDs nicht verändern.
3. Pro Artikellink HTTP-Status und canonical URL prüfen; bei nicht erreichbaren Seiten Status nachträglich ändern, niemals Link erfinden.
4. Die neuen 43 Karten nach den Bereichen und dem `entry_path` auffindbar machen.
5. Videos/Podcasts nur mit legalem Zugriff sichten; Hören/Transkribieren getrennt dokumentieren; keine unbelegte Volltextbehauptung.
6. Download-Queue abarbeiten: direkte Asset-URL, Lizenz, Urheber, kommerzielle Nutzung, Weitergabe, Version und Hash protokollieren.
7. Eigene Lehrbeispiele strikt von kommerziellen Samples/Live-Sets isolieren; keine Fremdinhalte in öffentliche Repo-Packages.
8. Für jedes der acht Transferstudien-Experimente ein eigenes Original-MIDI/Audio-Material erstellen und reale DAW-Testprotokolle erfassen.
9. Tests: CSV-Eindeutigkeit, link sanitizer, alle Quellenkarten existieren, 1:1 Zuordnung, Archiv-SHA-Vergleich, interne Querverweise und Lizenzstatus.
10. Technische und musikalische Review getrennt abzeichnen; keine rote Lücke durch künstlich erzeugte Beispielzahlen verdecken.
11. Wiederholbare Blog-Archiv-Pagination mit Rate Limits, robots.txt/ToS-Prüfung und Stopbedingungen implementieren; keinen Login-Scraper bauen.
12. Nach Abschluss nur PR mit Änderungsübersicht und Lizenzbericht vorbereiten; kein automatischer Merge.

## Akzeptanzkriterien

- Alle 156 V6.4-Blogeinträge vorhanden; 43 Ergänzungen mit Original-URL.
- Keine doppelten Canonical Slugs; Varianten /en/ und /de/ zusammengeführt.
- Alle neuen Quellenkarten sind parsebar und ihre Register-Pfade bestehen.
- Externe Kunst- und Musikmedien bleiben unter separaten Zugriffsregeln.
- Die Aussagen „technisch geprüft“, „theoretisch korrekt“, „klanglich bewertet“ sind strikt separat nachgewiesen.

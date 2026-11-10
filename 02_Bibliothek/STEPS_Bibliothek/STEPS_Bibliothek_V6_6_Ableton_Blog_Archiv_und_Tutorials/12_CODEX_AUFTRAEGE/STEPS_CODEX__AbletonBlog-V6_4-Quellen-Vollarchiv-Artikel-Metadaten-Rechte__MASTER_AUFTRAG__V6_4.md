# STEPS Codex Masterauftrag V6.4 – Ableton Blog: Bibliothek und Wissensobjekte

## Auftragsgrenze und Bestandsschutz

Die Nutzer-Bibliothek V6.3/V6.4 ist ein **externer Wissensbestand**, keine geprüfte Aussage über den Git-Repository-Status. Prüfe im jeweiligen STEPS-Arbeitsverzeichnis den realen Stand, bevor du Pfade setzt oder Dateien verschiebst. Kopiere/übernehme alte Versionen **nicht blind über bestehende Daten**. Keine urheberrechtlich geschützten Artikel, Podcasts, Samples oder Live-Projekte als reproduzierbare STEPS-KB importieren.

## Eingänge

- `10_QUELLEN_LIZENZEN/STEPS_QUELLEN__AbletonBlog-KUMULATIV-V6_2-V6_4__QUELLENREGISTER__V6_4.csv` mit 156 Quellen.
- Einzelne V6.4-Karten in `20` Fachbereichen.
- Download-Prüfqueue und QA-Audit.
- Ältere V6.3-Inventare und bestehende Research-/Composing-/Producer-Bände unverändert erhalten.

## Arbeitspakete und Tests

1. **Bestand:** Repository/Dateiindex, Versions- und Lizenzlage prüfen; echte README-/Modul-Pfade lokalisieren. Ergebnisse protokollieren.
2. **Source ingestion:** CSV/JSON mit Pydantic/JSON-Schema validieren; URLs nach Locale/Slug kanonisieren, separate Sprachvarianten und Titelmetadaten behalten.
3. **Crawling in genehmigter Umgebung:** Robots, Rate-Limit, Paginierung, Fehlerbehandlung, ETag/Cache und Terms beachten; keine Login-/Paywall-Umgehung.
4. **Parser:** Titel, Tags, Veröffentlichungsdatum, Kategorien, Artikellinks, Medien- und Downloadlinks getrennt extrahieren. Metadaten von Inhalt trennen.
5. **Claim-Layer:** Lernpunkt als Quelle+Abschnitt+Lizenz+Prüfstatus modellieren; abweichende Aussagen und stilabhängige Interpretationen erlauben.
6. **Rights gate:** Pro Asset Nutzungsbedingungen protokollieren; keine Speicherung/Weitergabe/ML-Verarbeitung vor Freigabe. Fallbeispiele Brikha und Bathe sind NEGATIVE Reuse-Tests.
7. **Research-to-KB:** Aus Quellenprotokollen eigenständige Begriffe, Methoden, Gegenbeispiele und Unterrichtseinheiten erzeugen; vom User bestätigte Regeln getrennt von Heuristiken.
8. **Deep review:** Mindestens drei Artikel zu den vier Kern-Domänen, Drum/Rhythm und Producer-Tools gezielt abschnittsweise prüfen, ohne Quellvolltext in KI-Ausgaben zu reproduzieren.
9. **Experimental lab:** Eigene MIDI-/Audio-Beispiele für Microtuning, polyrhythmisches Sequencing, Bass-/Kick-Envelope, Delay-Design, Reharmonisierung und Song-Arrangements bauen.
10. **Tests:** Reihenfolge/Uniqueness, 404-Erkennung, Locale-Dedup, Rest-APIs, schema validity, rights gate, candidate states, Quellen-Provenienz und Attributionsstatus automatisieren.
11. **UI-Integration:** Provenienz, Suchfilter, Tagging, Wiedervorlage und nur verifizierte KI-Zitate im STEPS-Frontend anzeigen.
12. **PR-Handover:** Änderungen mit Tests, ersten Fehlertraces und Reproduktionskommandos in einem PR vorlegen; nicht ohne ausdrückliche Freigabe mergen.

## Abnahmekriterien

- Import vorhandener 156 Quellen ohne Duplikat oder Datenverlust.
- Jede neue Quellenkarte kann über ID, Thema, Titel, URL und Rechte-/Review-Status gesucht werden.
- Für jeden wissensbasierten Claim ist erkennbar, ob Artikel, Video, Interview oder eigene Hypothese die Quelle ist.
- Kein unklar lizenziertes Asset gelangt in weitergebbares Material.
- Automatische Tests laufen lokal/CI reproduzierbar; Hör-, Stil- und Wissenschaftsreviews bleiben als eigene Aufgaben sichtbar.

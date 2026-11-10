# STEPS-Blog-Integration V6.3 – Methodik und Grenzen

## Quantitativer Stand

- Verifizierter V6.2-Bestand: 23 Einträge, unverändert übernommen.
- Neue Einträge nach URL-Abgleich: **74**.
- Kumulativ eindeutige URLs: **97**.
- Doppelt vorgeschlagene/verworfene Kandidaten: **6**.
- Neue, eigenständige Recherchekarten: **74**.
- Artikel-übergreifende vertiefte Praxis- und Forschungsverknüpfungen: **16**.
- V6.2-Dateien: **829**; deren SHA256 bleiben unverändert.

## Statusdefinitionen

- `article_page_opened`: Eine Artikel-Webseite wurde geöffnet, Autor/Fakten/Volltext/Video noch nicht vollständig unabhängig geprüft.
- `archive_listing_only`: Das Ableton-Archiv zeigte einen konkreten Link/Titel, aber die Artikelseite selbst war nicht abrufbar (Cache miss). Die Forschungsnotiz enthält daher nur indexgestützte Angaben.
- `asset_status=download_link_indicated_NOT_ACQUIRED`: eine Download-Rubrik bzw. entsprechende Angabe vorhanden; das Medium selbst wurde **nicht** abgerufen oder weiterverwendet.
- Alles darüber hinaus ist eigenes STEPS-Design, keine Ableton-Aussage.

## Lücken und weitere Erhebung

1. **Nicht vollständiger Crawl:** Es fehlen ältere Kategorieseiten, die vollständigen `One Thing`-Episoden, `Loop`- und Podcast-Archive sowie alle historischen Sprachalternativen; kein Gesamt-Nenner behauptbar.
2. **Download-Gates:** URLs, Dateiformate, Live-Versionen, Lizenzbelege und Drittanbieter-Weitergabe müssen je Asset ermittelt werden.
3. **Wissenschaftliches Review:** Künstler- und Herstellerinterviews liefern Praxisbeispiele, aber keine universellen Harmonielehren oder Normen.
4. **Medienreview:** Videos/Podcasts wurden nicht transkribiert; ausschließlich die verlinkten öffentlich sichtbaren Begleittexte flossen in diese Runde ein.
5. **Produktbezug:** Codex darf kein komplettes DAW-Produkt als gebilligte STEPS-Roadmap ableiten. Forschung und Umsetzung sind getrennte Entscheidungen.
6. **Aktualität:** ältere Blogeinträge können inzwischen veraltete Tools und kaputte Downloads enthalten. Historische Jahre nicht automatisch in die aktuellen Anforderungen übertragen.

## Reproduzierbarkeit

Die versionierten CSV/JSON-Dateien bilden den Literaturbestand ab; validierbare Tests müssen ID-/URL-Eindeutigkeit, Quelle-zu-Forschungsnotiz-Referenzen und Dateiintegrität prüfen. Für das Nachholen des Vollcrawls muss ein netzwerkfähiger Auftrag separat Artikel und Downloads anhand ihrer tatsächlichen Rechte prüfen.

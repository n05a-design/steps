# Codex-Auftrag — Ableton-Blog vollständig inventarisieren und STEPS integrieren / V6.2

**Ziel:** Von derzeit 23 nachvollziehbar indexierten Artikeln zu einer belastbaren und nachweisbar vollständigen **öffentlich zugänglichen Blog-Metadateninventur** gelangen. Texte und Assets nur nach Erlaubnis/ Lizenz übernehmen; niemals die komplette Website als geschützten Textbestand spiegeln.

1. Repository-Zustand und vorhandenes STEPS-Archiv prüfen. Die V6.1-Dateien sind immutable; nur additive V6.2-Änderungen. Keine automatischen Merges.
2. Netzwerk/robots.txt und ggf. Sitemap in der ausführenden Umgebung prüfen. Erlaubte Archivpaginierung von `/de/blog/` sowie alle `/de/blog/categories/` und relevante Collections durchlaufen; terminalen Pagination-Stop nachweisen (nicht bloß willkürlicher `max_pages`-Abbruch). Requests moderat limitieren und Fehlabrufe dokumentieren. Auth-Bereiche auslassen.
3. Canonical URLs, Sprachvarianten (de/en), Duplikate, Redirects und `?page=`-Artefakte normalisieren; Story-ID/URL als stabile Identität verwenden. Falsch positive News-Navigationslinks herausfiltern.
4. Jede Artikel-Metadatenseite: original URL, canonical, Titel, Autor, Datum, redaktionelle Kategorie, Tags, Stichworte, Genre, Live-Version, Art (Artikel, Tutorial, Video, Interview, Podcast, Download), Abgleich mit bestehenden V6.1-Bereichen; Zuordnung 1:n ermöglichen.
5. Prüfstufen `listing_only` / `article_html_seen` / `text_reviewed` / `video_transcript_reviewed` / `media_reviewed`, getrennt von QA-Freigabestufen. Fehlende Transkripte nicht als reviewed markieren.
6. Downloads ausschließlich auf **Metadatenebene** indexieren: Link, Dateityp, Lizenztext, kommerzieller Einsatz, Redistribution und Version/Kompatibilität; ohne ausdrückliche Lizenz niemals in den öffentlichen Bibliotheks-ZIP kopieren. Frei verfügbare Download-Links erlauben keine stillschweigende Übernahme.
7. Prioritäten für Fachannotation: Harmonie/Akkordfolgen; Composing/Arrangement; Drums/Groove/MIDI; Synthese/Sound Design; Mixing/Mastering; Vocals/Recording; Game/Live/Spatial; Product/Didaktik.
8. Aus Artikeln eigene, nachvollziehbare STEPS-Concept/Rule/Exercise/Validation-Objekte mit `source_id`, `source_locator` und `interpretation_type` erstellen; keine geschützten Langtextkopien und keine nicht nachvollziehbaren Autorenzitate.
9. Trainingsbeispiele nur selbst komponieren und MIDI/JSON mit golden tests gegenchecken. Bei konkreten Genre-BPMs historische und lokale Quellen statt universelle Norm behaupten.
10. Abnahmebericht: tatsächliche Anzahl Paginationseiten, Artikel pro Kategorie, Artikelgesamtzahl dedupliziert, Anzahl Fehler/retries, letzte erfolgreich gefundene Seite, Coverage-Zeitfenster, Stichprobenaudits, Revisionsdatum, Copyright/Freigabe und diff zur vorigen Version. Falls Abrufbarrieren bleiben: Status ausdrücklich `partial`.
11. Automatisierte Tests: URLs nur Ableton-Domain, eindeutige canonical, Datumsformat, dokumentierte Links, Zero-copy-Verbot, CSV/JSON-Konsistenz, SHA256 für V6.1, `robots.txt`-Konformität, Null-Fall für geschützte Assets. CI-Prüfungen; keine Schreibaktionen in Main ohne Review.

Startskript: `15_TOOLS_SKRIPTE/STEPS_TOOLS__AbletonBlog-metadaten-indexer__INDEXER__V6_2.py`.

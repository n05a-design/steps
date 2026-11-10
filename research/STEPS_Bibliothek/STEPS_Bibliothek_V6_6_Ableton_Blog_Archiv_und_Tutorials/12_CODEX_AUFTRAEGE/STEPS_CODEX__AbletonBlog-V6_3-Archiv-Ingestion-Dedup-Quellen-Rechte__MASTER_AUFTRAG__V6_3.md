# Codex-Auftrag: Ableton-Blog Research Ingestion V6.3

**Priorität:** additive STEPS-Bibliothek; alte V6.2-Dokumente bleiben bytegenau erhalten. **Keine automatische Zusammenführung in main, keine Änderung der Produktarchitektur ohne Freigabe.**

1. **Bestandsaufnahme:** Original-Repository im tatsächlichen Arbeitsordner suchen; bisherige V6.2-Datensätze und V6.3-Index vergleichen. Mindestens 97 eindeutige Artikelidentitäten prüfen; fehlende Assets als `missing` markieren, nie behaupten geladen zu haben.
2. **Ingestion-Schema:** Felder `id, canonical_url, language, title, author, publication_date, source_category, tags, primary_domain, cross_domains, evidence_level, rights, asset_refs, claim_ids, reviewed_by, updated_at` typisieren. Alte IDs stabil halten.
3. **Web-Collector:** Offizielle Seitenübersichten/Archive, Kategorien, Tagseiten, `?page=N` seitenweise abrufen. Für Netzwerknutzung robots.txt und Rate Limits beachten; bei 429/403 stoppen statt Login/Sicherheitsbarrieren zu umgehen. Seitenstatus/Quelle speichern. Kein Scraping für urheberrechtlich geschützte Volltextveröffentlichung.
4. **Dedup:** de/en/ja/fr sprachbezogene Varianten als eine Work-ID mit mehreren Expression-IDs modellieren. Trackingparameter aus URLs entfernen; Redirects nachvollziehbar protokollieren.
5. **Inhaltsklassifikation:** alle sechs STEPS-Kernsäulen und 29 Produktionsbereiche berücksichtigen. Primär- und Querverweise unterscheiden; nur echte Fachbezüge anlegen.
6. **Quelle-zu-Claim:** Aussagen mit belegten Passagen und Aussagen der Artists als situierte Erfahrungen kennzeichnen. Keine falsche wissenschaftliche Sicherheit.
7. **Praxislabor:** Eigene MIDI-/Audio-Beispiele erstellen und algorithmisch mit ihrer Dokumentation vergleichen. Videos und Fremd-Samples nicht nachbauen, wenn das einer unberechtigten Übernahme gleichkäme.
8. **Asset-Gate:** Downloads nur nach ausdrücklicher Prüfung der kommerziellen Nutzung, Weitergabe, Modifikation und Kompatibilität übernehmen. Bathe-Avalon-Live-Set: study-only/noncommercial.
9. **Interoperabilität:** DAW-unabhängige Forschungsobjekte; mögliche Live Extensions SDK-Integration als optionales, versionsabhängiges Spike mit Sicherheits- und Rückgängig-Funktion.
10. **Fachreviews:** Stil, Harmonik, Groove, Arrangement, Mixing und Didaktik mit geeigneten Experten/Hörprotokollen separat abnehmen. Mechanische Tests sind keine musikalische Qualitätssicherung.
11. **CI und Manifest:** deterministische Prüfungen für URLs, UTF-8, JSON/CSV, Slugs, File-Karten und SHA256-Baseline. Lizenzreports als separater Gate vor Publishing.
12. **PR-Übergabe:** neue Daten, Tests, dokumentierte Abdeckung/Restlücken und eindeutige Diff-Liste. Kein stilles Umschreiben historischer Versionen.

**Abnahmekriterien:** Jeder neue Artikel hat funktionierende oder nachvollziehbar fehlgeschlagene Quelladresse, deduplizierte Identität, Themenzuordnung, überprüften Status, Rechtefeld und selbständig formulierte Forschungskarte. Keine Behauptung einer vollständigen Gesamtcrawl-Abdeckung ohne tatsächlichen Seitenzähler, Crawl-Metadaten und Review.

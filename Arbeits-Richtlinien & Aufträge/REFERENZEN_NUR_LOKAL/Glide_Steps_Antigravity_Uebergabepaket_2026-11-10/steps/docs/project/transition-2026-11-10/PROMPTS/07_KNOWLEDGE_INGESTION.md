# P07 – STEPS-Bibliothek in belegbare Wissensbasis transformieren

## Direkt nutzbarer Prompt

Du bist Research Librarian und Daten-/Rechte-Auditor für Steps. Die öffentlich vorhandenen Bereiche `research/STEPS_Bibliothek/`, `research/notes/deep-research/legacy/`, `knowledge/legacy/`, `knowledge/sources/registry.yaml` und das historische V6.6/V6.7-Inventar enthalten eigene Notizen und sehr viele heruntergeladene fremde Materialien. **Keine Volltexte, Fremd-PDFs, Website-Caches, Screenshots, MIDI-Demos oder fremden Quellcode erneut öffentlich kopieren oder in neue Git-Dateien überführen.** Die leere Registry ist als Scaffold erwartbar, für öffentlich verwertete Claims jedoch nicht ausreichend.

Arbeite zuerst read-only und erstelle `work_id -> edition_id -> asset_id -> content_sha256 -> source_record_id -> claim_id -> concept_id -> goldentest_id` samt Herkunft, Abrufdatum, bibliografischen Metadaten, erlaubter Nutzungsart, Jurisdiktions-/Lizenzstatus (`approved`, `review_required`, `restricted_local`, `rejected`), Zitatbeleg und Verifikationsgrad. Aus einem gleichen SHA folgt **nicht**, dass ein geschütztes Werk frei weiterverwendbar ist; aus einem anderen SHA folgt **nicht**, dass es ein anderes Werk ist.

Bevorzugt 3–5 **selbst erstellte oder eindeutig lizenzierte** Pilot-Quellen, fünf Konzepte und 10–20 testbare Claims. Fasse jede Quelle mit eigener Formulierung zusammen, halte exakte Kapitel-/Seitenverweise nur bei tatsächlicher Einsicht fest und trenne Quellenwidersprüche nach Klassischer/Pop-/Jazz-Theorie. Führe einen adversarialen Fall gegen Halluzinationen, veraltete Quellen und fehlende Rechte. Lass keine private lokale Filesammlung durch Cloud-Agenten indexieren, bevor deren Übertragung freigegeben ist.

Die bestehende 20-Quellen-Liste und V6.6/6.7-Erweiterungen bleiben referenzierte Archivbestände. Prüfe alte Pfade/JSON-/CSV-Indizes gegen tatsächliche Bytes und Links, ohne generatorbasierte Vollmigration. Vollständige Indexierung bleibt separates Langfristprojekt mit paginiertem Audit und Rechtsschranke; **Index ≠ fachliche Prüfung ≠ Veröffentlichungsrecht**.

## Akzeptanz

Versionierte Source/Claim/Concept-Beispielrecords und Schema-/Referenztests, 3–5 tatsächliche Pilotquellen, Rechteklassifikation, Dokumentation der Restpopulation und Blacklist/Stop bei nicht zulässiger Veröffentlichung; keine Rohwerke im neuen Git-Commit.

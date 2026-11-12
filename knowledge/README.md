# STEPS – wachsende Knowledge Base und Literaturarchiv

> Der operative Einstieg führt zum [Quellenregister](sources/README.md), zur [Ingestion](INGESTION_PIPELINE.md) und zu den [einzeln geprüften App-Beispielen](concepts/progressions/REVIEWED_PROGRESSIONS.md). Die folgenden Projekt- und Glide-Angaben sind datierte Ausgangsnotizen.


> **Kritischer Aktualitätsnachtrag (10.11.2026, nach GitHub PR #75):** Der folgende Basisteil stammt aus dem früheren Paket und kann für Glide `main` noch den historischen Commit `61a2f3a`/Version 3.50.7 nennen. Der erneut verifizierte Stand ist **Glide `9e767bea` (3.53.0)**; der hochgeladene `app.pyw` ist blobgleich mit diesem HEAD, nicht aber bereits alle weiteren Module und Ressourcen unabhängig verifiziert. Aktuelle Bewertungen und Entscheidungsgates stehen in [`docs/project/PROJECT_OVERVIEW.md`](../docs/project/PROJECT_OVERVIEW.md) und [`docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md`](../docs/audit/04_VERGLEICH_V1_V2_RESTRISIKEN_MASSNAHMEN.md). Aussagen im folgenden Basisteil bleiben als **historisch datierte Ausgangsnotizen** erhalten, keine unmarkierte aktuelle Wahrheit.

**Stand:** 10.11.2026 (Europe/Berlin). **Status:** Entwurf und Prüfauftrag, keine Umsetzung/Freigabe. **Referenzstände:** Steps `main` `75329fef46878a5ac816cef3690e612a9e8fe52c`; Glide `main` `61a2f3ac2f0e1880e7fd8c0f3cfd9da0d0c9f16d`; lokal bereitgestellter Glide-Code `3.53.0`, SHA-256 `d7e19151eb0862a8ff58c4cc5e7d06a0452cde1daa73830ff97f54247bc75271`.

**Evidenz:** `UPLOAD` = bereitgestellte Datei, `GITHUB` = gelesener Remote-Stand, `BERICHTET` = in Unterlagen behauptet, `VORSCHLAG` = neue Empfehlung, `OFFEN` = unbestätigt. Kein dokumentierter Test bedeutet nicht bestanden.

## Zwei Speicherschichten

- **Unveränderter Forschungsbestand:** `research/STEPS_Bibliothek/...` auf GitHub mit 49 nummerierten V6.6-Hauptordnern, V6.7-Generatoren, historischen Fassungen, Web-/MIDI-/PDF-Belegen. Lokale Sicherung und datierte Snapshot-Manifeste statt automatische Umbenennung/Löschung.
- **Kuratierte Produktbasis:** `knowledge/sources/registry.yaml` plus `knowledge/concepts/{intervals,scales,chords,harmony,progressions,voice_leading,styles}`, `knowledge/relations`, `examples`, `glossary`, `schemas` und `tests`. Der Bestand ist noch weitgehend strukturell/leere Skeletons. Nur geprüfte eigenständig formulierte Inhalte dürfen als canonical veröffentlicht werden.

**Die Root-Skill-Datei** ist ein Arbeits-Router und ersetzt nicht die Fachbibliothek. Der existierende `music-harmony-coach`-Skill ist wertvoller Ausgangspunkt, aber die bisher verschachtelte Lage und seine Notizqualität müssen geprüft werden. Kein Skill trainiert ein Modell dauerhaft oder garantiert, dass ein weiteres Modell alle Quellen automatisch kennt.

## Fachliche Hauptbereiche (gleichrangig)

Musiktheorie (Intervalle, Skalen, Notation), Harmonik (Funktion/Modal/Jazz/Chromatik), Akkordfolgen (Cadences, Harmonic Rhythm, Reharmonization, Voice Leading), Komponieren (Melodie, Form, Motivik). Eigenständige Bibliotheksschienen: Drums/Rhythm/Groove, Producer Tools, Kognition/Stile/Kultur, Computational Music, MIDI/Produktion, Medien/Case Studies, Rechts-/Lizenzfragen. **Keine Bereiche streichen**, bloß Product-MVP begrenzen.

## Erweiterungssicherer Ordnungsvertrag

1. Keine `N_*`-Nummer als semantischer Primärschlüssel; dauerhaft `concept_id`, `source_id`, `topic_id`, `relation_id` verwenden.
2. Source-Registry speichert eine Quelle **einmal**; mehrere Themen nutzen Referenzen (Quellenkarten/Claims), keine unmarkierten Kopien.
3. Neue Themenordner zulässig nach Registry-Diff, Inhalts-/License-Check, Index-Rebuild und Changelog; keine starre Zahl von 49 erzwingen.
4. Bytegleichheit (`sha256`) und inhaltliche Doppelung unterscheiden. Unterschiedliche Ausgaben, Übersetzungen und Claims werden über `work_id`, `edition_id`, `translation_group_id` und `supersedes` verbunden.
5. Fremde Rohdateien unter nicht öffentlichem `raw_local/` oder externer privater Quelle. `knowledge/sources/raw/` nicht unüberlegt in public git committen. Keine Original-PDFs/Bücher in das Download-Paket.
6. Kein Eintrag behauptet `reviewed/approved`, wenn die Quelle nur erwähnt wurde. Parserstatus, fachlicher Review und Lizenzstatus sind **drei unabhängige Achsen**.
7. Jedes kanonische Concept: Definition, Theorieframework, Preconditions, Spelling, Beispiel/Gegenbeispiel, konkurrierende Deutungen, Quellen mit locator, Testfixture, Review-Version.
8. Für Produktabfragen nur geprüfte Claim-ID und passende Lizenz verwenden; Herkunft/Interpretationskonflikte im UI erhalten.

Siehe `INGESTION_PIPELINE.md`, `skills/SKILL_DESIGN.md`, `source_archive/README_STEPS_BIBLIOTHEK.md`, `prompts/14_SOURCE_INGESTION.md` und `prompts/15_KNOWLEDGE_SKILL.md`.

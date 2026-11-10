# Codex – STEPS V5.1 Research Integration & Real MIDI Verification

**Auftrag:** Die V5.1-Ergänzung zu Drum Programming und Producer Tools kontrolliert in die tatsächliche, bestehende Steps-Knowledge-Base überführen. V5 unverändert archivieren. Keine behauptete MIDI-Prüfung, bevor tatsächliche lokale Dateien geöffnet wurden. **Nicht** die historischen Python-/Tkinter-Dateien oder die Musik-Engine ohne getrennten Auftrag umbauen. Kein automatischer Merge.

## C0 – Read-only Repository-Baseline

Repository-Speicherort, Branch, Git-Status, bestehende Governance, Knowledge Base, Forschungsarchive, Lizenzfilter und AGENTS/SKILL-Dateien dokumentieren. Nicht voraussetzen, dass `/mnt/data` identisch mit dem lokal installierten Steps-Projektordner ist. Offene Änderungen nicht überschreiben.

## C1 – Quellenreferenzen kontrolliert übernehmen

Alle fünf `PPR-*`-Source-IDs als ergänzende Quelle aufnehmen; die zwei inhaltlich identischen D&B-HTMLs als Importvarianten derselben Quelle verlinken. `SOURCE_REGISTRY_V5_1.json` liefert Source-URL, Titel, Datei- und Text-Hash, Status und Lesson Headings. Das HTML kann private Account-/Trackinginformationen enthalten: **nicht ins öffentliche Git committen**. Original-Unterrichtstexte, Samples, geschützte Audios und proprietäre Kursgrafiken nicht übernehmen. Bei Quellen-Abweichungen konflikt-/versionierte Records anlegen.

## C2 – Tatsächlich vorhandene MIDI-Dateien suchen und inventarisieren

Nur berechtigte Projektordner durchsuchen, vorerst read-only. Kandidaten anhand von Dateinamen (UK garage, techno, rage, Sub Focus, drum and bass), Tempo-/Track-Metadaten und Herkunftsnotizen **zuerst identifizieren**, dann per SHA-256 und Dateityp eindeutig registrieren. ZIPs getrennt inventarisieren, nicht blind extrahieren; ZIP-Slip/Symlinks/verschachtelte Archive kontrollieren. MIDI-Kanäle (Standard: MIDI-Drumkanal 10, in manchen Libraries nullbasiert Index 9), Tempo-Events, PPQ, Time Signatures, Note On/Off, Velocities, Controllers, Metadaten und Trackanzahl erfassen. Kein automatisches Kopieren in öffentliches Repo.

## C3 – Source-versus-MIDI Vergleich

Pro eindeutiger Lektion: Quelle und konkreten MIDI-Dateinamen verknüpfen; unbelegte Zuordnungen als `unverified` belassen. Teste Tempo, Trackrollen, Takt-/Subdivisionspositionen, Velocity-Ranges, Fills, Arrangementlängen, Bassregister, eventuell CC7, Swing als feste Eventverschiebung versus DAW-Groove-Metadaten und Stopp-/Gate-Längen. Bei UK Garage gegebenenfalls `Straight/` und `Swung/`-Varianten und Unterschiede zwischen MIDI-Timing und DAW-Groove unterscheiden. Bei Miss the Rage: Fan-Remake-Status bewahren; Soundausgabe aus MIDI allein kann 808-Note-off-Verhalten nicht beweisen. Beim Sub Focus Beispiel darf ein originaler Songmix nicht ohne ausdrückliche Quelle oder Lizenz als private Stems behauptet werden.

## C4 – Zwei modulare Research-Domänen

`05 Drum Programming, Rhythm & Groove` umfasst Rhythmusgrundlagen, Genre-Patterns, Swing/Microtiming, Dynamik, Fills, Variation, Drum-Bass-Koordination und formale Modellierung. `06 Producer Tools & Production Techniques` umfasst zunächst den nachgewiesenen EQ-Kursartikel und danach separat zu recherchierende Synthese-, Sampling-, Arrangement-, EQ-/Dynamics-/Mixing- und Workflow-Themen. Beide Domänen bleiben unabhängig versionierbar und werden mit den vier Hauptsäulen verknüpft. Keine andere bestehende Fachsäule entfernen oder umnummerieren, wenn Repo-Konventionen abweichen; Mapping dokumentieren.

## C5 – Wissenschaftliches und fachliches Review

For each claim: `source_id → source_locator → claim → concept/rule → style_scope → uncertainty → test`. Faktische Timing-/MIDI-Aussagen maschinell validieren, Stil- und Klanginterpretationen als fachliche Bewertung behandeln. Nicht ungeprüfte, auf Kursüberschriften basierende Theorien als fertiges Wissen ausgeben. Ergänzende Primär-/Fachquellen pro Themenfeld sammeln und explizit zwischen `metadata_verified`, `excerpt_read`, `full_text_read`, `expert_reviewed` unterscheiden. Course video/Audio/DAW projects nicht als eingesehen behaupten, wenn nur der HTML-Text vorliegt.

## C6 – Auslieferungskriterien

1. Fünf Source-IDs, sechs Uploadvarianten und das inhaltliche D&B-Duplikat korrekt erfasst.
2. Musikdaten bleiben getrennt von den fachlichen Zusammenfassungen; Lizenz-/Public-Gate nachvollziehbar.
3. Tatsächlich gefundene MIDI-Dateien mit Pfad, Hash, Tracks und Tests beschrieben; nicht gefundene explizit benannt.
4. Drum-/Producer-Konzepte im echten KB-Index verlinkt und versioniert, keine Doppelobjekte.
5. Regeln gegen Positiv- und Negativ-Fälle getestet; ausgeführte Tests klar von geplanten unterschieden.
6. Keine externe Account- oder proprietäre Quelldatei öffentlich committed.
7. Ergebnisbericht mit geprüften Dateien, Code-/Dok-Diff, offenen Fragen, Quellenkonflikten und Restbacklog. Kein Merge ohne Freigabe.

Diese Ergänzung ersetzt **nicht** `07_Codex/CODEX_MASTER_EXECUTION_V5.md`, sondern wird als zusätzliches Arbeitspaket darin eingebunden.

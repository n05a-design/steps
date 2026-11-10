> **STEPS Research Library V5.3 · Stand 08.11.2026 · Status: Fachliche Arbeitsreferenz, nicht unabhängig peer-reviewed.** Eigene Synthese und eigene Beispiele; externe Quellen sind jeweils unter „Nachweise“ angegeben. Unterrichtsbeispiele sind keine genreuniversellen Vorschriften. Das Kapitel dokumentiert Wissen, nicht nachgewiesene Implementierung in Steps.

# Loudness, True Peak und Mastering: Standards von Stilentscheidungen trennen

## Was ist verbindlich – und in welchem Kontext?
ITU-R BS.1770 definiert Algorithmen zur Messung der Programmlautheit und des True-Peak-Levels. EBU R 128 (Version 5.0, 21.11.2023) empfiehlt **für den entsprechenden Broadcast-Kontext** eine durchschnittliche Programmlautheit von **−23 LUFS** und beschreibt Loudness Range und Maximum True Peak Level. **Das ist keine allgemeine Streaming-/EDM-/Mastering-Zielzahl.** Produktionsziele und Distribution-Plattformen unterscheiden sich; Steps darf keinen universellen LUFS-Wert als musikalische Richtigkeit ausgeben.

## Begriffstabelle
| Maß | beschreibt | darf nicht verwechselt werden mit |
|---|---|---|
| dBFS | digitaler Sample-/Full-Scale-Pegel | subjektiver Lautheit |
| LUFS / LKFS | gewichtete gemessene Programmlautheit nach Standard | beliebiger Spitzenpegel |
| True Peak | geschätzte Spitzen zwischen Samples im rekonstruierten Signal | Sample Peak allein |
| Loudness Range | Variation der gemessenen Programmlautheit | musikalische Phrasen- oder Dynamikqualität |
| Crest Factor | Spitze gegenüber mittlerem Signalmaß (Definition angeben) | automatisch „mehr Punch“ |

## Mastering-Workflow für eine eigene 30-Sekunden-Studie
1. Mix ohne Clipping exportieren, Sample-Rate/Bit-Tiefe dokumentieren. 2. Erst Lautheitsmessung ohne Limiter. 3. Zielmedium/Broadcast-/Plattformkontext festlegen. 4. Falls erforderlich kontrolliert Gain und Limiting anwenden. 5. True Peak und Loudness neu messen; nicht allein Sample Peak. 6. Gehörvergleich mit pegelangepasstem Original. 7. Artefakte (pumpende Kick, zerstörte Transienten, verzerrte S-Laute) auditieren. 8. Erst dann Ausgabeversion freigeben.

## Ein realistischer Negativtest
Eine Mixdatei mit Integrated Loudness −12 LUFS kann in einem konkreten ästhetischen Kontext bewusst gewollt sein. Das numerische Verhältnis zum Broadcast-Ziel −23 LUFS macht sie **nicht** musiktheoretisch falsch. Umgekehrt beweist ein gemessener Wert von −23 LUFS nicht, dass das Master korrekt, sicher oder stilistisch gelungen ist. Genreabhängige Lautheitsziele nicht als absoluten Standard kodieren.

## Steps-Objekt
`mastering_measurement_id`, `audio_hash`, `algorithm`, `standard_version`, `source_signal`, `integrated_lufs`, `short_term_lufs`, `true_peak_dbtp`, `lra`, `target_context`, `normalization_gain_db`, `measurement_tool`, `review`, `rights`. Ohne Audio-Datei/Toollauf nur ein konzeptionelles Arbeitsobjekt, keine erfundene Messung.

### Normative Nachweise
- EBU R 128 v5.0, EBU Technology & Innovation, 21.11.2023: https://tech.ebu.ch/publications/r128
- ITU-R BS.1770-5, 22.11.2023, Empfehlung zur algorithmischen Lautheits-/True-Peak-Messung: https://www.itu.int/rec/R-REC-BS.1770-5-202311-I/en
Bei Standards darf ein anderes Jahr bzw. eine neuere Ausgabe nicht ohne erneute Prüfung angenommen werden.

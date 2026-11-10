# CODEX – Integration der Quelle DeSantis *Making Music* (STEPS V6.1)

**Arbeitsziel:** Das Buch als bibliografisch referenzierte, bereichsübergreifende Quelle in die STEPS-Knowledge-Base integrieren – **ohne** das urheberrechtlich geschützte PDF in Repository, CI-Artifacts, Trainingskorpus oder öffentliches Release zu kopieren. Die vorhandene V6-Bibliothek nicht überschreiben oder pauschal reorganisieren.

## Reihenfolge / Arbeitspakete

1. **Repository-Audit:** tatsächliche STEPS-Ordner, branch, bestehende Quellenregister, Lizenzregeln und interne Wissensobjekte lesen. Keine Annahmen über lokale Pfade treffen.
2. **Verifikation:** Datei `MakingMusic_DennisDeSantis.pdf` nur in ausdrücklich zugänglichen lokalen Nutzerordnern suchen, ohne beliebige Verzeichnisse/Cloudspeicher zu scannen. Wenn gefunden, SHA-256 gegen Quellenkarte prüfen; bei Abweichung stoppen und dokumentieren.
3. **Schema-Mapping:** `source_id`, publication metadata, `chapters`, `topic_links`, `exercise_links`, `source_span` in aktuelles Knowledge-Base-Schema abbilden. Kapitelzahlen 25+37+12 = 74 sicherstellen.
4. **Primärquelle erhalten:** Original-PDF nur außerhalb Git im privaten Quellenbestand referenzieren; falls nötig lokale Git-Ignore-Einträge gezielt ergänzen. Keine Git-LFS-Einlagerung ohne Lizenzfreigabe.
5. **Abdeckungsanalyse:** bestehende STEPS-Komposition, Harmony, Drums, Producer Tools und Lernpfade mit 74 Kapitelankern verbinden; Doppelungen mit früheren Entwürfen erkennen; keine inhaltlichen Duplikate anlegen.
6. **Eigene didaktische Objekte:** zwölf STEPS-eigene Aufgaben mit Quellenanker und eigenem Copyright-Hinweis indexieren; vor unkontrollierter Generierung großer Sammlungen zunächst menschliche Freigabe einfordern.
7. **Evidence:** Eintrag `toc_verified` nicht in `full_text_reviewed` oder `scientifically_verified` umwandeln; nicht gelesene Kapitel nicht als vollständig validiert kennzeichnen.
8. **Richtige Trennung:** mathematisch/technisch deterministische Assertions (MIDI, Intervalle, Zeitachse) von hörbasierten, subjektiven Bewertungen trennen.
9. **Tests:** 74 eindeutige IDs, 25/37/12-Phasen, korrekte 1-basierte PDF-Seiten, keine defekten Fachbereich-Referenzen, Quellenhash-Länge, keine private Datei im öffentlichem Paket. Negative Tests für beschädigte Metadaten und doppelte IDs.
10. **Produktvorschläge, kein Scope-Creep:** mögliche Features etwa `Ideenstart`, `Motivvarianten`, `Songstruktur-Skizze`, `Arrangement-Reduktion`, `Fertigstellungs-Checkliste`; niemals aus bloßen Kapiteln einen kompletten DAW-Entwicklungsauftrag ableiten.
11. **Tests ausführen:** vorhandene STEPS-Tests plus Parser-/Schreibweisen-/MIDI-Regression auf relevanten Plattformen; Ergebnis und nicht ausführbare Fälle getrennt dokumentieren.
12. **Abgabe:** Quellenregister-Diff, Crosslink-Report, Dateimanifest, Lizenz-Check, Prüfresultate und prägnante PR-Beschreibung. Kein Merge ohne ausdrückliche Zustimmung.

## Abnahmekriterien

- Eindeutiger Quellenanker und **74/74** Indexeinträge referenzierbar.
- Kein Original-PDF, keine längeren Buchpassagen und keine geschützten Beispiel-Assets ins öffentliche Repo übernommen.
- Query `creative_block`, `drum_variation`, `voice_leading`, `arrangement_form`, `finish_track` findet die relevanten Kapitelanker.
- Jede materialisierte Quelle zeigt `verified_scope`, Rights-Flag, PDF-Seitenreferenz und STEPS-Anwendung.
- Beweissichere Angabe, was automatisch geprüft wurde und was nur menschlich-musikalisch geprüft werden kann.

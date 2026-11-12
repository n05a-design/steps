# STEPS · Prüfmatrix für das Fable-5.2-Audit

Revision `22f3f5f`. Prioritäten: P0 kritisch, P1 hoch, P2 mittel, P3 niedrig. Die Risikobewertung stammt aus der Vorbereitung und ist kein Befund.
„Tests vorhanden“ heißt: Es gibt Assertions. Ob sie die Eigenschaft unabhängig prüfen, ist selbst Prüffrage.

## Kern (`src/steps/`)

| ID | Gegenstand | P | Prüffragen | Erwarteter Nachweis | Tests vorhanden | Offen |
|---|---|---|---|---|---|---|
| K01 | `pitch.py` Tonklasse, MIDI, Frequenz | P0 | Stimmen `midi_number` und Oktavgrenzen bei Cb, B#, Cbb, B## (z. B. Cb4, B#3)? Lehnt `PitchClass` `bool` und Gleitkommazahlen ab? Sind `midi_to_frequency` und `frequency_to_midi` zueinander invers, und wie verhält sich das Rundungsverhalten? | Unabhängige Formel C4=60, A4=69, f=440·2^((m−69)/12), Gegenbeispiele | `test_theory_core.py` | Randoktaven −1/9, MIDI 0/127 |
| K02 | `parse_spelling` und `render` (INT/DE/AUTO) | P0 | Wie wird `B4` in AUTO gelesen, und ist das mit `AGENTS.md` Nr. 5 (H/B explizit) vereinbar? Werden Hes, Ases, Eses, Heses, His korrekt gelesen oder abgewiesen? Gilt der Round-Trip `parse(render(x)) == x` für alle 35 Schreibweisen × beide Konventionen? | Deutsche Notennamenkonvention aus belegter Quelle, Round-Trip-Tabelle | ja | Systematischer Round-Trip |
| K03 | `interval.py` | P0 | Qualität und Umkehrung für alle einfachen und zusammengesetzten Intervalle inklusive doppelt vermindert und übermäßig. Stimmen die Vorzeichenkonventionen von `directed_semitones` und `signed_semitones`? Ist `transpose_spelling` invers? | Definitionen diatonische Zahl × Halbtöne, Umkehrungsregel 9/Qualitätstausch | ja | Zusammengesetzte Intervalle |
| K04 | `triad.py`, `seventh.py` | P1 | Intervallstrukturen aller Qualitäten. Theoretische und gespielte Intervalle bei `SEVENTH_INTERVALS` gegenüber `THEORETICAL_INTERVALS`. Grenzen von Drop-2 und Shell | Terzschichtung | ja | – |
| K05 | `chord.py` Templates, `parse_chord`, Aliasse, Slash | P0 | Stimmt jedes `CHORD_TEMPLATES`-Rezept mit einer unabhängigen Definition überein? Groß- und Kleinschreibung bei M/m und Fallunterscheidung (`CM7`, `Cm7`, `CMaj7`). Werden mehrdeutige Symbole wie `Bm7`, `Bb`, `Hm7`, `Esus4`, `Asus2`, `As7` je Konvention richtig gelesen? Slash mit Nicht-Akkordton. Wird Unbekanntes abgewiesen statt umgedeutet? | Lead-Sheet-Konvention, Gegenbeispielliste | ja | Systematischer Templatevergleich |
| K06 | `ChordDefinition.to_voicing` | P1 | Liefern CLOSE, DROP2, SHELL und ROOTLESS mit und ohne Slash-Bass die zugesagten Töne, Lagen und den Bass? Gibt es Duplikate oder fehlende Töne? Ist die feste Lage `60 + pc` bei ROOTLESS gewollt? | Explizite Soll-Voicings für 5–10 Symbole | teilweise | Grenzlagen |
| K07 | `engine.resolve_roman_degree` | P0 | Dur und Moll (natürlich, Leitton bei V und vii°), `b`/`#`-Stufen relativ zu Dur, Zwischenfunktionen `V/x` und `vii°/x`, Generalbassfiguren 6, 64, 65, 43, 42, Qualitätssuffixe. Was ergibt `V/vi` in Moll? Wird `iv7` in Dur und `bVII7` korrekt aufgelöst? | Unabhängige Stufentabelle Dur/Moll, Fachquelle, mindestens 30 Fälle | ja | Moll-Zwischenfunktionen, Fehlerpfade |
| K08 | Bestandskatalog (28 PROG) und `CanonicalProgression.transpose` | P1 | Passen Stufen und Akkordspalte je PROG zusammen (`chords` gegenüber `resolve_roman_degree(roman)`)? Bleibt die Schreibweise bei Transposition erhalten (`transpose_chromatic` normiert enharmonisch)? | Paarweiser Vergleich aller 28 | `test_reviewed_progressions.py` (336 Fälle) | PROG-020/-027 `alt` |
| K09 | `voice_leading.py` | P1 | Optimalität und Determinismus von `optimize_smooth_voice_leading`. Stimmt der Docstring („within one octave“) mit dem Fenster ±12 überein? Unlösbare Vorgaben. Was erkennt `detect_parallel_fifths_octaves` (Gegenbewegung, Antiparallelen, Einklang)? | Brute-Force-Gegenrechnung bei kleinen Fällen | ja | Strikter Modus, Laufzeit |
| K10 | `generate_progression_voicings`, `analyze_progression_voice_leading` | P1 | Konsistenter Rückgabevertrag für 0, 1 und ≥2 Voicings. Startvoicing-Auffüllung. Bassfortschreitung ohne Slash | Vertragsvergleich mit `docs/theory/API.md` | teilweise | – |
| K11 | `reviewed.py` Publikationssperre und Freigaben | P0 | Was genau beweist eine Freigabe: Fingerabdruck, Link-Format, Reviewer-Name? Wird geprüft, ob der Link existiert und ob die Person freigegeben hat? Kann ein Agent eine formal gültige Freigabe selbst eintragen? Deckt der Fingerabdruck alle publizierten Felder ab (Quellen, Notation, `voice_path`)? | Codepfad, Mutationsversuch in Kopie | `test_pilot_publication.py`, `test_reviewed_progressions.py` | Vertrauensmodell |
| K12 | `app/knowledge.py` | P2 | Exportiert der Adapter nur geprüfte Inhalte? Fehlerverhalten bei Sperre | Import im Test | indirekt | – |
| K13 | `exceptions.py` | P3 | Wird die Hierarchie konsistent verwendet? Gibt es `Exception`-Fallbacks, die Fehler verschlucken (z. B. `parse_spelling` AUTO)? | Codeleseprüfung | – | – |

## Skills

| ID | Gegenstand | P | Prüffragen | Nachweis | Tests | Offen |
|---|---|---|---|---|---|---|
| S01 | `steps-knowledge-curation` | P1 | Fehlen Statusregeln wie `DONE_VERIFIED` oder wären sie mit unzureichendem Beleg erreichbar? Wo bleiben Datenverlust- und Überschreibrisiken (`backup_knowledge.py`, Register außerhalb des Repos)? Pfadgrenzen in `check_source.py`, Prompt-Injection über extrahierte Arbeitsanweisungen in `extract_instructions.py`. Stimmen Referenzen auf `docs/engineering/MUSIC_DOMAIN_AND_MIDI.md`? | Skriptlesung, Tests, Mutationsfall | 25 | E2E mit echten Pfaden |
| S02 | `SKILL.md` (Router) | P2 | Existieren alle Verweise (z. B. `skills/music-harmony-coach/` ohne Datumsordner, `docs/architecture/migration.md`)? Leitet der Router Fachfragen auf ungeprüftes Material? | Pfadprüfung | – | – |
| S03 | `music-harmony-coach` (historisch) | P2 | Anreize zu Halluzination? Quellenangaben in `references/sources.md` des Coach-Ordners (laut `THEMENSTICHPROBEN.md` mit Buchplatzhalter)? Konsistenz mit Kern und Notationskonvention? Darf er noch aktiviert werden? | 12 Fälle `COACH-*` in `knowledge/benchmark/cases.json` (PENDING) | – | Coach-Antworten fehlen |
| S04 | `skills/SKILL_DESIGN.md` | P3 | Verweist das Design auf veraltete Zustände (z. B. „registry.yaml leer“)? | Abgleich | – | – |

## Wissensbasis und Datenkette

| ID | Gegenstand | P | Prüffragen | Nachweis | Tests | Offen |
|---|---|---|---|---|---|---|
| W01 | `knowledge/sources/registry.yaml` | P0 | Belegen die 7 Quellen die zugeordneten Pilotaussagen an den angegebenen Locators? Ist die Rechteangabe begründet? | Quelle lesen (nur Metadaten und Passage, kein Volltext) | Sperre prüft Format | Inhaltliche Prüfung |
| W02 | `MUSIC_SOURCE_CLAIM_REGISTER.csv` | P1 | Ist `VERIFIED_TRUE` (35) bei nur 3 fachlich untersuchten Claims gerechtfertigt? Wer setzt den Status? Stichprobe von mindestens 8 Claims über M01–M12 | Primärquelle oder Herleitung | Benchmark-Stichprobe | Statusmodell |
| W03 | `curated_sources_registry.yaml` | P2 | Fehlen Duplikate oder Rechtefelder? Verhältnis zum Produktregister | Abgleich | Coverage | – |
| W04 | Kataloge PROG, P, PAT, Latin | P1 | Die in `THEMENSTICHPROBEN.md` als korrigiert gemeldeten Stellen (PROG-008, PROG-016, Commit `792b2dd`) und die Hinweise zu P12/P19 unabhängig nachrechnen. Gibt es weitere Fehler je Katalog? | Unabhängige Rechnung | Benchmark `catalog` | 95 Positionen fachlich offen |
| W05 | `MUSIC_CONCEPT_RELATIONS.csv` | P2 | Sind die Relationen fachlich sinnvoll oder nur syntaktisch? Stichprobe von 10 | Abgleich | Integrität | – |
| W06 | Benchmark (`cases.json`, `COVERAGE.csv`, `PILOT_ABNAHME.md`, `THEMENSTICHPROBEN.md`) | P1 | Stimmen Sollwerte? Ist der Status in `COVERAGE.csv` aus Daten abgeleitet oder handgepflegt (`scripts/audit_knowledge_coverage.py`)? FAIL `KB-M11-ALTER` einordnen | Skriptlesung | `test_knowledge_benchmark.py` | – |
| W07 | Golden Cases (198) | P1 | Sind Sollwerte unabhängig von STEPS-Code entstanden? Wie viele der 131 SPECIFICATION_EXAMPLE sind falsch? Stichprobe von mindestens 20 über alle Domänen | Unabhängige Herleitung | Referenz-Evaluator | 198 fachlich offen |
| W08 | Datenkette Quelle → Claim → Konzept → Relation → Skill → Algorithmus → Test → Ergebnis | P0 | Für PROG-003 und PROG-009 jede Station nachvollziehen. Brüche und Stellen, an denen syntaktische Auflösung als Wahrheit gilt | Kettenprotokoll | – | – |

## Tests, Werkzeuge und CI

| ID | Gegenstand | P | Prüffragen | Offen |
|---|---|---|---|---|
| T01 | `test_theory_core.py`, `test_progression_engine.py` | P1 | Haben die Erwartungswerte eine unabhängige Herkunft? Welche Fehlklassen aus K01–K10 würden unentdeckt bleiben? | Mutationsideen |
| T02 | `test_reviewed_progressions.py`, `test_pilot_publication.py` | P1 | Wird die Sperre negativ getestet (manipulierter Fingerabdruck, fremder Link, fehlende Freigabe)? | – |
| T03 | `test_golden_reference_cases.py` | P1 | Referenz-Evaluator und Laufzeitkern: Gibt es gemeinsame Fehlerquellen? Gibt es Assertions ohne Aussagekraft? | – |
| T04 | `test_reference_integrity.py`, `scripts/verify_reference_integrity.py` | P2 | Was sagt „100% … VERIFIED“ tatsächlich aus? | – |
| T05 | `scripts/run_knowledge_benchmark.py`, `scripts/render_reviewed_progressions.py` | P1 | Kann ein Fall PASS liefern, ohne die Eigenschaft zu prüfen (Methoden `manual`, `claim_sample`)? | – |
| T06 | `.github/workflows/*.yml` | P2 | Sind alle lokalen Gates in CI? `knowledge-coverage` installiert PyYAML separat. Ist `structure-check.yml` aktuell? | – |
| T07 | `test_secret_scanner.py`, `test_structure.py` | P3 | Nur Funktionsprüfung, keine Fixture-Werte lesen | – |

## Architektur (D6)

| ID | Gegenstand | P | Prüffrage |
|---|---|---|---|
| A01 | Eignung für Chord- und Progression-Editor | P2 | Sind Typen (Spelling, ChordDefinition, Voicing) unveränderlich, serialisierbar und eindeutig? |
| A02 | Drum/Rhythmus, MIDI, Piano | P2 | Fehlen Zeit- und Taktmodell, Ports? Das Ergebnis sind Lücken, keine Fehler |
| A03 | Wissensadapter und Harmony Coach | P1 | Kann ein Coach nur auf freigegebene Daten zugreifen? |
| A04 | Desktop-Integration | P3 | Grenze `app/` ↔ `src/steps/` gemäß `AGENTS.md` Nr. 4 |

## Historische Behauptungen (D7)

| ID | Gegenstand | P | Prüffrage |
|---|---|---|---|
| H01 | `docs/audit/00_…` bis `05_…` | P2 | Welche Gesamtaussagen („vollständig“, „verifiziert“, „bestanden“) gelten am Stand `22f3f5f`? |
| H02 | Master-Audit V2 und OpenAI-Prüfpaket (über `archive/INDEX.md`) | P2 | Drei bis fünf Kernaussagen stichprobenhaft prüfen |

## Ausgeschlossen, mit Grund

| Bereich | Grund |
|---|---|
| `src/glide-v3.53/` | Glide-Referenzcode, eigenes Projekt mit externer Lizenz. Nicht Teil des STEPS-Kerns |
| `src/steps-0.00/` | Nur README-Gerüst, kein Code |
| `app/ui`, `app/audio`, `app/core`, `app/adapters` | Nur README-Platzhalter |
| `research/` (außer `research/gaps/`) | Forschungsbibliothek mit Fremdmaterial (Rechte). Nicht produktiv eingebunden |
| `archive/`, `source_archive/` | Historisch. Nur für H01/H02 |
| Einmal-Generatoren in `scripts/` (`build_*`, `generate_*`, `export_*`, `execute_project_consolidation.py`, `handover/`) | Erzeugen Berichte, kein Laufzeitpfad. Nur prüfen, wenn ein Befund auf sie zurückführt |
| `knowledge/research/independent_golden_test_engine.py`, `run_golden_test_suite.py`, `verify_swing_math.py` | Legacy-Runner mit Abhängigkeit von lokalen Pfaden. Nur für T03 als Vergleich |

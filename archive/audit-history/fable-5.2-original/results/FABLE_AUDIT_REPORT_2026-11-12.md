# STEPS · Unabhängiges Gesamtaudit (Fable 5.2) · 2026-11-12

Prüfgegenstand: `n05a-design/steps` auf `22f3f5f348d060abfd4e2ffc917d0c95a639441e`. Keine Datei im Checkout wurde geändert. Dieser Bericht ist **keine vollständige Abnahme**: 20 von 38 Prüf-IDs sind `TEILWEISE`, innerhalb von H02 ist das OpenAI-Prüfpaket `NICHT_GEPRÜFT` (Abschnitte 5 und 8).

## 1. Managementzusammenfassung

- **Kern (K):** Rechenkern für MIDI, Frequenz, Intervallgrößen, Akkordrezepte und die 28 Katalogstufen stimmt mit unabhängigen Sollwerten überein. Fehler liegen an den Rändern: Konventionserkennung `AUTO`, Stufen mit expliziter Qualität, Figuren auf nicht terzgeschichteten Akkorden, Moll-Sonderstufen, Transpositions-Schreibweise.
- **Publikationssperre (K11):** Sie erkennt jede Änderung an freigegebenen Daten. Sie beweist aber nicht, dass ein Mensch freigegeben hat. Eine formal gültige Selbstfreigabe falscher Inhalte wurde in der Arbeitskopie akzeptiert.
- **Skills (S):** `steps-knowledge-curation` lässt `DONE_VERIFIED` ohne Nachweis zu, schreibt auf POSIX eine Seiteneffekt-Datei und stuft importierten Text als `EXPLICIT`-Anweisung ein. Router und Coach verweisen auf ungeprüftes Material.
- **Wissensbasis (W):** Die 7 Produktquellen belegen die Pilotaussagen an den genannten Stellen. Statuswerte `VERIFIED_TRUE` (35) und `VERIFIED_ACTIVE` (97) haben keinen Prüfprozess hinter sich. In Stichproben sind 1 von 21 Claims und 3 von 66 Golden Cases fachlich falsch, weitere sind aussagelos.
- **Tests (T):** 120 Kerntests grün auf 3.12, 3.13, 3.14. Der Golden-Evaluator vergleicht in mindestens 19 von 67 „berechneten“ Fällen ein fest eingetragenes Literal oder die Eingabe mit dem Sollwert.
- **Befunde:** P0 = 10 · P1 = 12 · P2 = 8 · P3 = 3 (gesamt 33). Gegenproben: 477 Fälle, 369 PASS, 108 Abweichungen.
- **Wichtigste Risiken:** (1) Freigabe ohne Identitäts- und Existenznachweis (F-K11-01). (2) Stille Fehldeutung von Notation: `B` in `AUTO`, deutscher Slash-Bass, Moll-Numeral mit Dur-Qualität (F-K02-01, F-K05-01, F-K07-01). (3) Statusfelder und Golden Cases täuschen geprüftes Wissen vor (F-W02-01, F-W07-01, F-T03-01).

## 2. Prüfbasis

Umgebung: macOS (Darwin 27.2), `PY=~/steps-fable-pack/.venv312/bin/python` (3.12.16, PyYAML 6.0.3). Alle Befehle aus `~/steps-fable-audit`. `git status --porcelain` war zu Beginn und nach jeder Phase bis auf nicht versionierte `.DS_Store`-Dateien leer. Diese stammen vom Finder, nicht vom Audit (Umgebungsvermerk, kein Befund).

| Befehl | Python | Exit | Ergebnis | Abweichung zu Kontextpaket Abschn. 3 |
|---|---|---|---|---|
| `git rev-parse HEAD` | – | 0 | `22f3f5f…441e` | keine |
| `-m unittest discover -s tests -p "test_*.py"` | 3.12 / 3.13 / 3.14 | 0 / 0 / 0 | je 120 Tests OK | keine. 3.11: `NOT_RUN` |
| `-m unittest discover -s .agents/skills/steps-knowledge-curation/tests` | 3.12 / 3.14 | 1 / 1 | 25 Tests, 1 FAIL (`test_03_exact_duplicate_identification`) | **ja**: Testbefund, siehe F-S01-03. `tests/README.md` nennt den Workaround `TMPDIR` |
| `scripts/render_api_reference.py --check` | 3.12 | 0 | – | keine |
| `scripts/run_knowledge_benchmark.py --scope pilot` | 3.12 | 0 | PASS 8 · FAIL 0 · PENDING 0 | keine |
| `… --scope publication` | 3.12 | 0 | PASS 3 · FAIL 0 · PENDING 0 | keine |
| `… --scope all` | 3.12 | 1 | PASS 37 · FAIL 1 · PENDING 32 (`KB-M11-ALTER`) | keine |
| `… --check-review-sheet knowledge/benchmark/PILOT_ABNAHME.md` | 3.12 | 0 | – | keine |
| `scripts/render_reviewed_progressions.py --check` | 3.12 | 0 | – | keine |
| `scripts/audit_knowledge_coverage.py --check` | 3.12 mit PyYAML / 3.14 ohne | 0 / 1 | ohne PyYAML Hinweis auf `requirements.txt` | keine |
| `scripts/verify_reference_integrity.py` | 3.12 | 0 | „100% … VERIFIED“ | keine |

Eigene Gegenproben: `~/steps-fable-pack/work/probes/*.py`, Rohausgabe `~/steps-fable-pack/results/GEGENPROBEN_ROHAUSGABE_2026-11-12.txt`. Sollwerte stehen im Skript vor der Ausführung. Mutationen nur in `~/steps-fable-pack/work/copy`. Fachquellen (W01) wurden im Browser gelesen. Der automatische Abruf der Pressbooks-Seiten lieferte HTTP 403.

## 3. Befunde

`test_status`: `RUN_FAIL` = Gegenprobe ausgeführt, Ist weicht vom Soll ab (Befund reproduziert). `NOT_RUN` = nur Codelesung. Präfix aller Reproduktionen: `cd ~/steps-fable-audit && PYTHONPATH=. $PY -B`, im Feld als `RUN` abgekürzt.

### P0

```yaml
- id: F-K11-01
  priority: P0
  severity: kritisch
  scope_id: K11
  location: src/steps/progression/reviewed.py:_approve (210–228), load_reviewed_catalog (231–253)
  revision: 22f3f5f
  description: Eine Freigabe gilt, sobald Fingerabdruck, Namensmuster, Datumsformat und Link-Muster passen. Existenz des Links, Identität und Rolle der Person werden nicht geprüft.
  reproduction: cd ~/steps-fable-pack/work/copy && PYTHONPATH=. $PY -B ~/steps-fable-pack/work/probes/K11_mutation.py
  actual: Geladen wurden (a) Link auf pull/999999#issuecomment-1, (b) Reviewer "x", (c) Datum 2099-12-31, (d) falsche Aussage "IV–V–vi" mit Akkorden "Dm7 - G7 - F#m7b5" nach selbst berechneter Freigabe, (e) voice_path-Note "Quatsch", (f) Aussage an themenfremde Quelle gehängt.
  expected: Sperre in allen sechs Fällen.
  rationale: Der Fingerabdruck bindet die Fassung, nicht den Urheber der Freigabe. `--review-manifest` und `_candidates()` liefern jedem Agenten den nötigen Fingerabdruck. Die Testfixture trägt selbst "fixture-reviewer" mit erfundenem Link ein (tests/test_pilot_publication.py:114–117).
  reference: Herleitung aus Codelesung und Mutation. AGENTS.md Nr. 7 verlangt Review durch Menschen.
  impact: app/knowledge.py, scripts/render_reviewed_progressions.py, CI-Job pilot-publication, jede Aussage "fachlich freigegeben".
  fix: Freigaben außerhalb des schreibbaren Arbeitsbaums verankern, z. B. CI-Schritt, der Kommentar-ID, Autor und Fingerabdruck im Kommentartext über die GitHub-API prüft, plus CODEOWNERS und Branch-Schutz für die Approvals-Datei. Zusätzlich reviewed_on ≤ heute, voice_path-Noten parsen und gegen Akkordtöne prüfen, Akkorde gegen Stufen prüfen.
  regression_test: Approvals-Datei mit korrektem Fingerabdruck, aber Kommentar-ID ohne passenden Fingerabdruck im Kommentartext → PublicationError.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K02-01
  priority: P0
  severity: hoch
  scope_id: K02
  location: src/steps/theory/pitch.py:parse_spelling (318–350), _is_german_string (353–367)
  revision: 22f3f5f
  description: Im Standardmodus AUTO wird "B4" still als internationales B (H) gelesen. Die deutsche Ausgabe von B♭ ("B4") ergibt beim Zurücklesen einen anderen Ton.
  reproduction: RUN -c "from src.steps.theory import parse_spelling as P; x=P('Bb4','INT'); print(x.render('DE'), P(x.render('DE')))"
  actual: B4 NoteSpelling(step='B', alteration=0, octave=4)
  expected: Ablehnung oder Ambiguitätsmeldung für unmarkiertes B. Round-Trip parse(render(x)) == x.
  rationale: DE "B" = INT B♭ (Tonklasse 10), INT "B" = DE H (Tonklasse 11). AUTO mischt im selben Aufruf deutsche Namen (Es, Fis, H) mit internationalem B. Betroffen sind auch parse_chord("Bm7") und resolve_roman_degree(…, key_root="B") im Standardmodus.
  reference: docs/engineering/MUSIC_DOMAIN_AND_MIDI.md T02 ("ohne Locale: Ablehnung/Ambiguitätsmeldung"), AGENTS.md Nr. 5, Yale University Library "The names of keys…", S. 1, Zeilen "B flat → B", "B → H".
  impact: Alle Aufrufer mit Default-Konvention: parse_chord, resolve_roman_degree, CanonicalProgression.chord_definitions.
  fix: In AUTO das unmarkierte B/b ablehnen (MusicTheoryError mit Hinweis auf INT/DE) oder Default auf INT setzen und AUTO nur explizit erlauben.
  regression_test: parse_spelling("B4") → Fehler. Für alle 35 Schreibweisen parse(render(x,'DE'),'DE') == x und parse(render(x,'DE')) wirft oder liefert x.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K05-01
  priority: P0
  severity: hoch
  scope_id: K05
  location: src/steps/theory/chord.py:parse_chord (443–450, 461–467)
  revision: 22f3f5f
  description: In AUTO wird ein als deutsch erkanntes Akkordsymbol mit einem international gelesenen Slash-Bass kombiniert.
  reproduction: RUN -c "from src.steps.theory import parse_chord as C; c=C('Esmaj7/B'); print(c.symbol, int(c.bass.pitch_class)); print(C('Hm7/B').symbol)"
  actual: Ebmaj7/B 11 und Bm7/B
  expected: Esmaj7/B deutsch gelesen = E♭maj7 mit Bass B♭ (Tonklasse 10, die Quinte). "Hm7/B" enthält H und B und kann nur deutsch gemeint sein (Bass B♭) oder ist abzuweisen.
  rationale: Der Bass wird getrennt mit AUTO geparst (parse_spelling(bass+'3')), bevor die Konvention des Akkordteils feststeht. Ergebnis ist E♭maj7 über H, ein Nicht-Akkordton im Halbtonabstand zur Quinte.
  reference: Herleitung aus der deutschen Tonnamenkonvention (siehe F-K02-01).
  impact: parse_chord, alle Slash-Akkorde aus deutschsprachiger Eingabe.
  fix: Konvention einmal für das ganze Symbol bestimmen und an den Bass weiterreichen.
  regression_test: parse_chord("Esmaj7/B").bass.pitch_class == 10. parse_chord("Esmaj7/B","DE") bleibt 10.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K07-01
  priority: P0
  severity: hoch
  scope_id: K07
  location: src/steps/progression/engine.py:_degree_quality (393–414)
  revision: 22f3f5f
  description: Explizite Qualitätssuffixe überschreiben die Groß-/Kleinschreibung des Numerals ohne Prüfung. Ein Moll-Numeral kann einen Dur-Akkord liefern.
  reproduction: RUN -c "from src.steps.progression import resolve_roman_degree as R; print([R(d).symbol for d in ('iadd9','ii13','IVm','Vb5')])"
  actual: ['Cadd9', 'D13', 'Fm', 'Gdim']
  expected: Fehler oder zur Schreibweise passende Qualität. "iadd9" = Cm(add9) oder Fehler, "ii13" Fehler (m13 nicht registriert), "IVm" Fehler (Widerspruch), "Vb5" = G–H–Des oder Fehler, nicht vermindert (G–B–Des).
  rationale: Großschreibung steht für Dur-, Kleinschreibung für Mollterz. Das Template "add9" und "13" enthält die große Terz. "b5" wird für jede Schreibweise auf "dim" abgebildet (Zeile 402).
  reference: Open Music Theory, Roman Numerals, Text zu Example 3 ("Uppercase Roman numerals denote major triads, and lowercase … minor triads"), https://viva.pressbooks.pub/openmusictheory/chapter/roman-numerals/
  impact: resolve_roman_degree, Benchmark-Methoden degree/degree_controls/catalog_position.
  fix: In _degree_quality die Terz des gewählten Templates gegen minor_triad prüfen und bei Widerspruch ProgressionParsingError werfen. "b5" nur für Kleinschreibung auf dim abbilden.
  regression_test: Für alle Suffixe in _EXPLICIT_QUALITIES mit Terz: R("i"+s) wirft oder liefert Intervall 3, R("I"+s) wirft oder liefert Intervall 4.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K02-02
  priority: P0
  severity: mittel
  scope_id: K02
  location: src/steps/theory/pitch.py:_parse_german_spelling (370–425)
  revision: 22f3f5f
  description: Der deutsche Parser akzeptiert Namen, die es im Deutschen nicht gibt, und deutet sie um.
  reproduction: RUN -c "from src.steps.theory import parse_spelling as P; print([(s,P(s+'4','DE').render('INT')) for s in ('Bis','Bes','Hes','Hses','Ees','Aes','Cn')])"
  actual: Bis→B#4, Bes→Bb4, Hes→Bb4, Hses→Bbb4, Ees→Eb4, Aes→Ab4, Cn→C4
  expected: Ablehnung. Vertretbar wäre allenfalls Hes als Nebenform von B.
  rationale: Deutsch B ist bereits erniedrigt. "Bis" wird zu His (Tonklasse 0). Der Akkord parse_chord("Bis7","DE") hat Grundton C. Regulär sind Es, As, Eses, Ases, Heses, His.
  reference: Yale University Library, a. a. O., S. 1 (as, es, B, H, Endungen -is/-es). Übrige Formen: Herleitung aus der Bildungsregel.
  impact: parse_spelling, parse_chord, resolve_roman_degree mit DE/AUTO.
  fix: Geschlossene Tabelle der 35 deutschen Namen statt Suffixregeln für B/H, E, A.
  regression_test: Für jeden der sieben Namen parse_spelling(name+"4","DE") → MusicTheoryError.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K05-02
  priority: P0
  severity: mittel
  scope_id: K05
  location: src/steps/theory/chord.py:parse_chord (461–467)
  revision: 22f3f5f
  description: In AUTO werden deutsche Dur-Dreiklänge mit Vorzeichen abgewiesen, dieselben Grundtöne mit Zusatz aber akzeptiert.
  reproduction: RUN -c "from src.steps.theory import parse_chord as C; print(C('Es7').symbol); C('Es')"
  actual: Es7 → Eb7. "Es", "Fis", "Des", "Cis" → ChordConstructionError. parse_spelling("Es4") in AUTO → E♭.
  expected: Gleiches Verhalten für "Es" und "Es7", konsistent mit parse_spelling.
  rationale: Das Erkennungsmuster verlangt nach dem Tonnamen ein weiteres Zeichen ([a-z0-9]).
  reference: Herleitung aus Codelesung. Der Benchmark führt denselben Punkt als PENDING (api_contract, Probe "auto").
  impact: parse_chord AUTO.
  fix: Muster um Symbolende ergänzen oder Erkennung an parse_spelling delegieren.
  regression_test: parse_chord("Es").symbol == "Eb", parse_chord("Fis").symbol == "F#".
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K05-03
  priority: P0
  severity: mittel
  scope_id: K05
  location: src/steps/theory/chord.py:_FOLDED_ALIASES (214–218)
  revision: 22f3f5f
  description: "CMmaj7" und "CMMAJ7" werden als C-Moll mit großer Septime gelesen. Ein großes M wird zu Moll umgedeutet.
  reproduction: RUN -c "from src.steps.theory import parse_chord as C; print(C('CMmaj7','INT').quality, C('CMMAJ7','INT').quality)"
  actual: m(maj7) m(maj7)
  expected: Ablehnung. IMPLEMENTATION.md sagt "CM7 ist Dur, Cm7 Moll".
  rationale: Der Alias "mmaj7" wird nicht von der Schutzregel für M/m erfasst (Regex verlangt Ziffer, Klammer oder Ende nach dem ersten Buchstaben) und daher ohne Rücksicht auf Großschreibung gefaltet.
  reference: docs/IMPLEMENTATION.md, Zeile "Akkordsymbole". Herleitung aus Codelesung.
  impact: parse_chord, ChordDefinition.
  fix: Aliasse, die mit M/m beginnen, grundsätzlich nicht falten.
  regression_test: parse_chord("CMmaj7","INT") → ChordConstructionError, parse_chord("Cmmaj7","INT").quality == "m(maj7)".
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K07-02
  priority: P0
  severity: mittel
  scope_id: K07
  location: src/steps/progression/engine.py:resolve_roman_degree (485–488)
  revision: 22f3f5f
  description: Generalbassfiguren nehmen an, dass theoretical_intervals terzgeschichtet und sortiert sind. Bei add9, sus4, 7sus4 und 7#11 entstehen falsche Basstöne oder ein fremder Fehlertyp.
  reproduction: RUN -c "from src.steps.progression import resolve_roman_degree as R; print(R('Iadd9(6)').symbol, R('V7sus4(65)').symbol); R('V7#11(42)')"
  actual: Cadd9/Ebb G7sus4/B# und InvalidAlterationError
  expected: Cadd9/E, Fehler für die Terzlage eines sus-Akkords, G7(#11)/F.
  rationale: Der Bass wird als transpose_diatonic(2·n, intervals[n]) gebildet. Bei (0,2,4,7) ist intervals[1] die None, bei (0,4,6,7,10) ist intervals[3] die Quinte.
  reference: Herleitung: Figur 6 = Terz im Bass, 4/2 = Septime im Bass.
  impact: resolve_roman_degree. IMPLEMENTATION.md nennt nur "V7(6)" als offenen Vertrag.
  fix: Akkordtöne nach Funktion (Terz, Quinte, Septime) im Template kennzeichnen und Figuren nur darauf anwenden, sonst ProgressionParsingError.
  regression_test: R("Iadd9(6)").bass.render() == "E4"-Tonklasse 4 mit step "E". R("V7sus4(65)") → ProgressionParsingError.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K07-03
  priority: P0
  severity: mittel
  scope_id: K07
  location: src/steps/progression/engine.py:resolve_roman_degree (471–477)
  revision: 22f3f5f
  description: In Moll gelten unversetzte Numerale relativ zu natürlich Moll, versetzte relativ zu Dur. Die erhöhte 6. Stufe als Grundton ist nicht korrekt erreichbar.
  reproduction: RUN -c "from src.steps.progression import resolve_roman_degree as R; print(R('#vi°','C',True).symbol, R('vi°','C',True).symbol, R('VI','C',True).symbol, R('bVI','C',True).symbol)"
  actual: A#dim Abdim Ab Ab
  expected: In c-Moll ist der verminderte Dreiklang auf der erhöhten 6. Stufe A–C–Es (Adim). Vertretbare Lesarten: "#vi°" → Adim (relativ zur Moll-Tonleiter) oder dokumentierte Ablehnung. A#dim ist keine vertretbare Lesart in c-Moll.
  rationale: Der Docstring nennt "accidentals are relative to major". Dadurch sind VI und bVI in Moll identisch, #VI liegt einen Halbton über der Dur-Sexte. "V/vi" in Moll ergibt Eb (Quinte über As), was konsistent ist, aber nirgends festgehalten wird.
  reference: Herleitung aus melodisch Moll (C D Es F G A H). Verhalten bestätigt, Konventionsfrage offen.
  impact: resolve_roman_degree mit is_minor_key=True.
  fix: Bezugssystem für Vorzeichen in Moll festlegen und dokumentieren. Empfehlung: Vorzeichen relativ zur gewählten Tonleiter, mit Testtabelle für c-Moll.
  regression_test: R("#vi°","C",True).symbol == "Adim" oder ProgressionParsingError. Nie "A#dim".
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-W08-01
  priority: P0
  severity: mittel
  scope_id: W08
  location: src/steps/progression/engine.py (_HISTORICAL_PROGRESSION_DEFINITIONS, 34–287), knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md, knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv
  revision: 22f3f5f
  description: Die Datenkette Quelle → Claim → Konzept → Relation ist für PROG-003 und PROG-009 an drei Stellen unterbrochen (siehe Kettenprotokoll in Abschnitt 4).
  reproduction: RUN ~/steps-fable-pack/work/probes/W08_kette.py
  actual: Für PROG-009 nennt get_progression "omt-roman-numerals, omt-chromatic-subdominants", die freigegebene Ausgabe "yale-key-names, omt-blues-based-schemas", die Bibliothek "de la Motte (1976)". Pilot-Claims stehen nicht im Claim-Register. PROG-009 hat keine Relation. REL-003/REL-004 zu PROG-003 tragen VERIFIED_ACTIVE ohne Prüfung.
  expected: Eine Quellenangabe je Progression-ID, Verknüpfung der Pilot-Claims mit dem Register, Relationen mit Beleg oder ohne Verifikationsstatus.
  rationale: Dieselbe ID liefert je nach Zugriffsweg andere Provenienz. Nur der Weg über app/knowledge.py ist an Belege gebunden.
  reference: Herleitung aus Datenvergleich.
  impact: get_progression, Bibliothek, Relationen, spätere Coach-Antworten.
  fix: Bestandskatalog aus einer Datenquelle erzeugen, Feld sources für ungeprüfte Einträge als "ungeprüft" kennzeichnen, Relationen ohne Beleg auf einen neutralen Status setzen.
  regression_test: Für jede Pilot-ID gilt set(get_progression(id).sources) ⊆ set(get_reviewed_progression(id).source_ids).
  evidence: CONFIRMED
  test_status: RUN_FAIL
```

### P1

```yaml
- id: F-K08-01
  priority: P1
  severity: hoch
  scope_id: K08
  location: src/steps/theory/pitch.py:transpose_chromatic (201–231), src/steps/progression/engine.py:CanonicalProgression.transpose (309–316)
  revision: 22f3f5f
  description: Transposition wählt die Schreibweise je Akkord einzeln. In 81 von 336 Fällen (28 Progressionen × 12) ändert sich der Stufenabstand benachbarter Grundtöne.
  reproduction: RUN -c "from src.steps.progression import get_progression as G; print([c.symbol for c in G('PROG-001').transpose(8)], [c.symbol for c in G('PROG-003').transpose(1)])"
  actual: ['Ab', 'Eb', 'Fm', 'C#'] und ['Ebm7', 'Ab7', 'C#maj7']
  expected: As-Dur: Ab Eb Fm Db. Des-Dur: Ebm7 Ab7 Dbmaj7. Vertretbar ist auch die durchgehend erhöhte Schreibweise, nicht die Mischung.
  rationale: IV in As-Dur ist Des (Quarte), nicht Cis (übermäßige Terz). Die 336 Bestandstests prüfen nur Tonklassen.
  reference: docs/engineering/MUSIC_DOMAIN_AND_MIDI.md T03 ("No spelling-loss bei round-trip"), AGENTS.md Nr. 5 (Enharmonik bewahren).
  impact: CanonicalProgression.transpose, auch für freigegebene Pilotbeispiele über .progression.transpose.
  fix: Mit DiatonicInterval transponieren (transpose_spelling) und die Zieltonart einmal wählen.
  regression_test: Für alle 28 × 12 bleibt (Stufenindex(b) − Stufenindex(a)) mod 7 für benachbarte Grundtöne erhalten.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-S01-01
  priority: P1
  severity: hoch
  scope_id: S01
  location: .agents/skills/steps-knowledge-curation/scripts/validate_register.py (5–38), references/work_instructions_protocol.md
  revision: 22f3f5f
  description: DONE_VERIFIED ist ohne Test- oder Commit-Nachweis erreichbar. Einträge ohne Statusfeld bestehen. Validator kennt 8 Zustände, Protokoll und Vorlage 6.
  reproduction: D=$(mktemp -d) && cd $D && $PY -B ~/steps-fable-pack/work/probes/S01_skill.py ~/steps-fable-audit/.agents/skills/steps-knowledge-curation/scripts
  actual: Register mit "Status DONE_VERIFIED", leeren Nachweisen und einem Eintrag ohne Status → errors_count 0.
  expected: Fehler für DONE_VERIFIED ohne gefüllte Felder "Erbrachte Nachweise" und "Abnahmekriterien" und für fehlenden Status.
  rationale: Das Protokoll definiert DONE_VERIFIED als "verified by tests and commit evidence". Geprüft werden nur ID-Duplikate, Titel und Statusvokabular.
  reference: references/work_instructions_protocol.md Abschnitt 3. README des Skills räumt ein, dass nur Struktur geprüft wird.
  impact: Master-Register, jede Auswertung "erledigt und verifiziert".
  fix: Je OA-Block Status verpflichtend. Für DONE_VERIFIED Commit-SHA und Testbefehl verlangen. Statusmengen angleichen.
  regression_test: validate_master_file auf dem Probe-Register liefert errors_count ≥ 2.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-S01-02
  priority: P1
  severity: hoch
  scope_id: S01
  location: .agents/skills/steps-knowledge-curation/scripts/backup_knowledge.py (6–7, 41–62)
  revision: 22f3f5f
  description: Auf macOS/Linux bleibt %LOCALAPPDATA% unaufgelöst. restore_master legt dann eine Datei mit diesem wörtlichen Namen im Arbeitsverzeichnis an. restore überschreibt den aktuellen Master ohne Sicherung und nimmt jede beliebige Datei als Backup an.
  reproduction: wie F-S01-01
  actual: Datei "%LOCALAPPDATA%\StepsKnowledge\OFFENE_ARBEITSAUFFORDERUNGEN.md" im Arbeitsverzeichnis. master.md nach restore_master("old.md","master.md") ersetzt, keine Kopie des Vorzustands. restore_master("reg.md", …) → RESTORE_SUCCESS.
  expected: Plattformgerechter Pfad oder klarer Fehler. Sicherung des Ziels vor dem Überschreiben. Annahme nur verifizierter Backups.
  rationale: os.path.expandvars löst %VAR% nur unter Windows auf. Der Hashvergleich nach dem Kopieren belegt nur den Kopiervorgang.
  reference: Herleitung aus Codelesung und Ausführung.
  impact: Datenverlust am einzigen kanonischen Aufgabenregister, Seiteneffekt-Datei im Checkout, wenn der Skill dort läuft. CI läuft auf Ubuntu.
  fix: Pfad über Umgebungsvariable mit Plattform-Fallback, Abbruch bei unaufgelöstem "%". Vor restore automatisches Backup. Backup-Manifest mit Hash prüfen.
  regression_test: Unter POSIX wirft restore_master ohne Ziel einen Fehler und erzeugt keine Datei. Nach restore existiert eine Kopie des alten Masters.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-W02-01
  priority: P1
  severity: hoch
  scope_id: W02
  location: knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv (Spalte validation_status), knowledge/relations/MUSIC_CONCEPT_RELATIONS.csv
  revision: 22f3f5f
  description: 35 Claims tragen VERIFIED_TRUE und 97 Relationen VERIFIED_ACTIVE, ohne dass ein Skript oder Protokoll den Status setzt. In der Stichprobe von 21 Claims ist einer falsch und einer fraglich.
  reproduction: cd ~/steps-fable-audit && grep -n "CLAIM-035\|CLAIM-038" knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv && grep -rn "VERIFIED_TRUE" scripts tests
  actual: CLAIM-035 nennt "5/8 … Take Five" und "7/8 … Money". CLAIM-038 ordnet den Akzent auf Zählzeit 2 dem "Surdo de resposta" zu. Einzige Skriptfundstelle für VERIFIED_TRUE ist die Vokabularprüfung in scripts/audit_knowledge_coverage.py:184.
  expected: "Take Five" steht im 5/4-Takt, "Money" im 7/4-Takt. Im Samba markiert die Surdo de primeira (marcação) die Zählzeit 2, die Surdo de resposta antwortet auf 1.
  rationale: 19 der 21 Stichproben-Claims sind rechnerisch oder aus Definitionen nachvollziehbar (z. B. CLAIM-017, -018, -036, -037, -044). Die Seitenangaben der Bücher sind nicht prüfbar. Der Status sagt also nichts über eine erfolgte Prüfung. knowledge/benchmark/README.md hält selbst fest, dass alte Statuswerte nicht als Fachprüfung zählen.
  reference: CLAIM-035: veröffentlichte Taktangaben der Stücke (Allgemeinwissen, keine Seitenangabe). CLAIM-038: Herleitung aus der Samba-Besetzung, nicht an einer Quelle geprüft.
  impact: Jede Auswertung, die VERIFIED_* als Wahrheitsbeleg liest. Relationen als Grundlage für einen Coach.
  fix: Status in LEGACY_UNREVIEWED umbenennen oder Spalten reviewer, reviewed_on, evidence ergänzen. CLAIM-035 korrigieren, CLAIM-038 an Quelle prüfen.
  regression_test: Coverage-Skript schlägt fehl, wenn VERIFIED_* ohne Prüfnachweis vorkommt.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-W07-01
  priority: P1
  severity: hoch
  scope_id: W07
  location: tests/golden_cases/golden_reference_cases.json (REF-0014, REF-0043, REF-0176, REF-0189, REF-0096, REF-0100, REF-0154)
  revision: 22f3f5f
  description: In einer Stichprobe von 66 Golden Cases (38 SPECIFICATION_EXAMPLE, alle Domänen M01–M12) sind drei fachlich falsch, einer begrifflich falsch und drei ohne Aussage.
  reproduction: cd ~/steps-fable-audit && $PY -B -c "import json; d={c['case_id']:c for c in json.load(open('tests/golden_cases/golden_reference_cases.json'))}; [print(k, d[k]['input_params'], '->', d[k]['expected_output']) for k in ('REF-0014','REF-0043','REF-0176','REF-0189','REF-0096','REF-0100','REF-0154')]"
  actual: REF-0014 Eingabe quality "Minor", Soll "Bass E, Töne [E, G, C]". REF-0043 "Drop-2 Dm7" = "LH [D3, A3], RH [F4, C5]". REF-0176 Sopran bewegt sich 2 Halbtöne, Soll true für verdeckte Quinte "im Sprung". REF-0189 Titel "Minimaler gemeinsamer Teiler" mit Soll 6. REF-0096 Soll = Eingabe. REF-0100 Soll true ohne Inhalt. REF-0154 Eingabe 5, Soll 5.
  expected: REF-0014: E–G–C ist C-Dur, c-Moll hätte Es. REF-0043: Drop-2 von D4–F4–A4–C5 ist A3–D4–F4–C5. D3–A3–F4–C5 ist Drop-2-und-4. REF-0176: Bei schrittweisem Sopran gilt die verdeckte Quinte im Außenstimmensatz als zulässig. REF-0189: 6 ist das kleinste gemeinsame Vielfache.
  rationale: Die übrigen 59 gelesenen Fälle stimmen mit eigener Rechnung überein (z. B. REF-0047, -0071, -0128, -0187, -0198). Zusätzlich liegen in Domäne M01 Fälle aus Rhythmik und Harmonik (REF-0055, -0062, -0070), die Domänenzuordnung ist also unzuverlässig.
  reference: Drop-2: Definition in CLAIM-042 desselben Repositorys und make_drop2_voicing. Übrige: Herleitung aus Intervall- und Satzlehre.
  impact: Golden Cases als künftiges Testorakel, COVERAGE-Zeile "Golden-Referenzfälle".
  fix: Die vier Fälle korrigieren, aussagelose Fälle streichen oder mit Eingabe und Rechnung versehen, Domänen neu zuordnen. Hochrechnung: bei 3 bis 7 von 66 Fehlern ist im Gesamtbestand mit rund 10 bis 20 betroffenen Fällen zu rechnen (Schätzung, nicht geprüft).
  regression_test: Für REF-0043 liefert make_drop2_voicing([62,65,69,72]) == [57,62,65,72] und stimmt mit dem Sollwert überein.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-T03-01
  priority: P1
  severity: mittel
  scope_id: T03
  location: tests/test_golden_reference_cases.py (139–316, 119–122, 318–328)
  revision: 22f3f5f
  description: Der Referenz-Evaluator vergleicht in 15 Zweigen (mindestens 17 Fälle) ein fest eingetragenes Literal mit dem Sollwert, reicht in einem Zweig die Eingabe durch, liefert in einem Zweig eine Konstante und prüft 131 Spezifikationsfälle nur auf "nicht None" und gültige Domäne.
  reproduction: cd ~/steps-fable-audit && sed -n 139,316p tests/test_golden_reference_cases.py | grep -nE "actual = ('|\"|\[[0-9]|[0-9]|True|False)"  # 16 Treffer, davon ist nur 60000.0 / p['bpm'] eine Rechnung
  actual: z. B. REF-0014 `actual = 'Bass E, Töne [E, G, C]'`, REF-0096 `actual = p['bass']`, verify_cross_domain_compatibility gibt für jede Liste der Länge 3 True zurück.
  expected: Berechnung aus input_params. Fälle ohne Berechnung als Dokumentation führen, nicht als Test.
  rationale: Der Evaluator importiert `src.steps` nicht. Er teilt also keinen Code mit dem Laufzeitkern, prüft ihn aber auch nicht. Die Aussage "67 vom unabhängigen Referenz-Evaluator berechnet" (tests/README.md) gilt für höchstens 48 Fälle.
  reference: Herleitung aus Codelesung.
  impact: Aussagekraft von test_golden_reference_cases.py. Fehler wie REF-0014 bleiben grün.
  fix: Literalzweige entfernen oder als SPECIFICATION_EXAMPLE führen. Berechenbare Fälle zusätzlich gegen `src.steps` laufen lassen.
  regression_test: Mutationstest: expected_output von REF-0014 ändern → der Test muss aus einer Berechnung heraus fehlschlagen, nicht aus einem Stringvergleich.
  evidence: CONFIRMED
  test_status: NOT_RUN

- id: F-A03-01
  priority: P1
  severity: mittel
  scope_id: A03
  location: src/steps/progression/__init__.py (Exporte), SKILL.md Zeile 3 des Workflows
  revision: 22f3f5f
  description: Ein Coach ist nicht auf freigegebene Daten beschränkt. Die allgemeine API liefert 28 Bestandsprogressionen mit ungeprüften Literaturangaben, und der Router schickt Harmonieaufgaben zum historischen Skill.
  reproduction: RUN -c "from src.steps.progression import get_progression as G; print(G('PROG-006').sources, '|', G('PROG-024').context)"
  actual: "Fux (1725), Rameau (1722)" für die Pachelbel-Sequenz. "Bossa Nova (Girl from Ipanema)" für Imaj7–V7/V–ii7–V7–Imaj7.
  expected: Zugriff für Lern- und Coach-Ausgaben nur über app/knowledge.py oder deutliche Kennzeichnung "ungeprüft".
  rationale: app/knowledge.py exportiert korrekt nur die drei Pilotbeispiele (Gegenproben K12 bestanden). Die Grenze ist aber nur Konvention.
  reference: Herleitung aus Exportliste. Zu PROG-024 siehe F-W04-01.
  impact: Künftiger Harmony Coach, Lernmodule.
  fix: Bestandskatalog in ein Modul mit Namen wie `unreviewed_catalog` verschieben oder sources/context dort leeren. Router auf app/knowledge.py verweisen.
  regression_test: Importtest: ein Coach-Modul darf `get_progression` nicht importieren (Strukturprüfung).
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K10-01
  priority: P1
  severity: mittel
  scope_id: K10
  location: src/steps/progression/engine.py:analyze_progression_voice_leading (539–589)
  revision: 22f3f5f
  description: Die Rückgabe hat für weniger als zwei Voicings andere Schlüssel als für zwei oder mehr. Stimmkreuzungen werden nie gezählt, weil vor der Prüfung sortiert wird.
  reproduction: RUN ~/steps-fable-pack/work/probes/K09_voiceleading.py
  actual: n<2: average_l1_step, circular_pc_distance. n≥2: average_l1_step_per_voice, total_circular_distance, max_single_voice_jump. Voicing((64,60,67)) → voice_crossings_count 0.
  expected: Ein Schlüsselsatz für alle Längen. Kreuzung auf der Stimmenreihenfolge des Voicings prüfen.
  rationale: Voicing.midi_notes sortiert. detect_voice_crossing auf einer sortierten Liste ohne Duplikate ist immer False.
  reference: Herleitung aus Codelesung. Der Benchmark führt den Schlüsselpunkt als PENDING (Probe "analysis").
  impact: Aufrufer der Analyse, künftige UI.
  fix: Rückgabetyp als Dataclass mit festen Feldern. Stimmenidentität in Voicing erhalten.
  regression_test: keys(analyze([])) == keys(analyze([v])) == keys(analyze([v, v])).
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K06-01
  priority: P1
  severity: mittel
  scope_id: K06
  location: src/steps/theory/chord.py:ChordDefinition.to_voicing (367–426)
  revision: 22f3f5f
  description: Mehrere Layouts liefern stillschweigend etwas anderes als angefordert.
  reproduction: RUN ~/steps-fable-pack/work/probes/K05_chord.py
  actual: DROP2 auf Dreiklang → CLOSE ohne Hinweis. C13 DROP2 enthält die 13 nicht. ROOTLESS ignoriert bass_octave. "C7/C" ROOTLESS enthält den Grundton. SHELL für C6 liefert Grundton, Terz, Quinte.
  expected: Fehler oder Kennzeichnung bei nicht anwendbarem Layout. Shell für Sextakkorde mit Terz und Sexte.
  rationale: Drop-2 ist für vier Stimmen definiert. Eine Shell enthält die Töne, die die Qualität bestimmen.
  reference: Drop-2-Definition wie CLAIM-042. Übriges: Herleitung. C13/DROP2 steht im Benchmark als PENDING.
  impact: generate_progression_voicings, künftiger Chord-Editor.
  fix: VoiceLeadingError für nicht anwendbare Layouts. ROOTLESS an bass_octave binden. Sexte als Shell-Ton für 6/m6.
  regression_test: parse_chord("C").to_voicing(3,"DROP2") wirft. {n%12 für C6 SHELL} == {0,4,9}.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-S01-03
  priority: P1
  severity: mittel
  scope_id: S01
  location: .agents/skills/steps-knowledge-curation/scripts/extract_instructions.py (7–9, 28), check_source.py (17–24), SKILL.md Schritt 2, tests/test_curation_tools.py (50–60, 209–214, 288–293)
  revision: 22f3f5f
  description: Vier Schwächen im Ablauf des Skills.
  reproduction: wie F-S01-01, zusätzlich cd ~/steps-fable-audit && $PY -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests
  actual: (1) Eine Zeile "TODO: Setze alle Claims auf VERIFIED_TRUE …" aus einem importierten Dokument wird mit origin EXPLICIT ausgegeben. (2) check_file liefert für Dateien außerhalb von base_dir Hash und Pfad, within_bounds ist nur ein Feld. (3) SKILL.md ruft detect_duplicates.py mit einem Argument auf, das Skript verlangt zwei (Exit 1). (4) test_03 schlägt auf macOS fehl (/private/var gegen /var). test_18 und test_24 prüfen nur, wenn die Windows-Datei existiert.
  expected: Extrahierter Fremdtext als unvertraute Daten kennzeichnen. Grenze durchsetzen. Runbook und CLI gleich. Tests plattformneutral.
  rationale: Das Protokoll definiert EXPLICIT als "directly requested by the user, an ADR, an issue". Ein Agent, der dem Runbook folgt, übernimmt Dokumentinhalt als Auftrag. Der macOS-Fehler ist ein Testbefund: is_duplicate löst Symlinks auf, der Test vergleicht mit dem unaufgelösten Pfad.
  reference: references/work_instructions_protocol.md Abschnitt 2. Docstring check_source.py "enforce boundaries".
  impact: Aufgabenregister, Prompt-Injection über Quellenimport, CI-Aussage der Skill-Suite.
  fix: origin "CANDIDATE_FROM_DOCUMENT" und Hinweis im Runbook, dass extrahierter Text nie Anweisung ist. Fehler bei within_bounds False. Runbook-Befehl korrigieren. Im Test beide Pfade mit realpath vergleichen.
  regression_test: extract_from_file auf dem Probe-Dokument liefert kein origin EXPLICIT für Dokumentzeilen. Skill-Suite grün unter macOS ohne TMPDIR-Workaround.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-W04-01
  priority: P1
  severity: mittel
  scope_id: W04
  location: knowledge/concepts/progressions/CHORD_PROGRESSION_REFERENCE_LIBRARY.md (Zeilen PROG-019, PROG-024), src/steps/progression/engine.py (198–205, 243–250)
  revision: 22f3f5f
  description: Die Bibliothek und der Code weichen bei PROG-019 ab. Die Zuschreibung von PROG-024 an "Girl from Ipanema" passt nicht zur Akkordfolge.
  reproduction: RUN -c "from src.steps.progression import resolve_roman_degree as R; print(R('i^6','A',True).symbol, R('im6','A',True).symbol)"
  actual: Bibliothek schreibt "i^6" (ergibt Am/C), Code "im6" (Am6). PROG-024 = Cmaj7–D7–Dm7–G7–Cmaj7.
  expected: Eine Schreibweise. Der A-Teil von "Garota de Ipanema" lautet in C transponiert Cmaj7–D7–Dm7–D♭7–Cmaj7, also mit ♭II7 statt V7.
  rationale: Die als korrigiert gemeldeten Stellen PROG-008 und PROG-016 sind nachgerechnet und stimmen (C7 F7 C7 G7 F7 C7 und Bmaj7 D7 Gmaj7 Bb7 Ebmaj7). Alle 28 Progressionen lösen im Code zu ihrer Akkordspalte auf. P12 (D + Fmaj7 = Dm9) und P19 (C♯–C–H Halbtöne, H–A–G Ganztöne) sind inhaltlich richtig, die Modultitel "Rootless" und "Chromatische Bassführung" passen nur teilweise.
  reference: PROG-024: verbreitete Lead-Sheet-Harmonik des Stücks (Allgemeinwissen, nicht an einer Ausgabe geprüft) → für diesen Teil STRONGLY_INDICATED. PROG-019: ausgeführt.
  impact: Bibliothek als "kanonische" Referenz, Kontextfeld von PROG-024.
  fix: Bibliothek auf "im6" ändern oder aus dem Code erzeugen. Kontext von PROG-024 auf "Take the A Train"-Typ ändern oder Akkord anpassen.
  regression_test: Für jede Bibliothekszeile gilt resolve(roman) == Akkordspalte.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K01-01
  priority: P1
  severity: mittel
  scope_id: K01
  location: src/steps/theory/pitch.py:PitchClass.__new__ (88–91), NoteSpelling.__post_init__ (118–126), midi_to_frequency (302–308), parse_spelling (318)
  revision: 22f3f5f
  description: bool und float werden als Tonklasse, Alteration, Oktave und MIDI-Nummer akzeptiert. None führt zu AttributeError statt Domänenfehler.
  reproduction: RUN ~/steps-fable-pack/work/probes/K01_pitch.py
  actual: PitchClass(True) = 1. NoteSpelling('C', True, 4) und ('C', 1.0, 4) gültig. NoteSpelling('C',0,4.5).midi_number = 66.0. midi_to_frequency(True) = 8.66 Hz, (60.5) = 269.29 Hz. parse_spelling("C10") liefert ein Objekt, dessen midi_number erst später wirft. parse_spelling(None), parse_chord(None), resolve_roman_degree(None) → AttributeError.
  expected: Ablehnung mit MusicTheoryError, wie es Voicing und optimize_smooth_voice_leading für bool bereits tun.
  rationale: Uneinheitliche Typprüfung im selben Paket. Halbe Oktaven erzeugen stille Falschwerte.
  reference: Herleitung. Vergleich mit chord.py:237 (Voicing prüft bool).
  impact: Alle Aufrufer, Serialisierung, künftige UI-Eingaben.
  fix: Gemeinsame Hilfsfunktion `_require_int` für alle öffentlichen Eingänge. MIDI-Bereich bei der Konstruktion von NoteSpelling prüfen oder dokumentiert offen lassen.
  regression_test: Jede der genannten Eingaben wirft MusicTheoryError.
  evidence: CONFIRMED
  test_status: RUN_FAIL
```

### P2

```yaml
- id: F-K03-01
  priority: P2
  severity: niedrig
  scope_id: K03
  location: src/steps/theory/interval.py:DiatonicInterval.__post_init__ (62–77), invert (129–144), interval_between_spellings (185–230)
  revision: 22f3f5f
  description: Randfälle der Intervallklasse sind inkonsistent.
  reproduction: RUN ~/steps-fable-pack/work/probes/K03_interval.py
  actual: DiatonicInterval(1,'d').semitones = −1. DiatonicInterval(8,'A').invert() ergibt −1 Halbtöne. Qualität 'X' und Zahl 2.5 werden bei der Konstruktion angenommen. C4→B#3 wirft, B#3→C4 liefert d2. Doppelt verminderte und doppelt übermäßige Intervalle sind nicht darstellbar (C4→Gbb4 wirft).
  expected: Negative Größen ausschließen, Eingaben bei Konstruktion prüfen, symmetrisches Verhalten, dokumentierte Grenze für dd/AA.
  rationale: Alle 38 Größen, die Umkehrregel und die Inverse der Transposition (35 Schreibweisen × 38 Intervalle) bestehen. Die Abweichungen betreffen nur die Ränder.
  reference: Herleitung aus Größentabelle (Dur/rein {0,2,4,5,7,9,11}).
  impact: interval.py, spätere Notationsfunktionen.
  fix: Validierung ergänzen, d1 abweisen, Grenze in API.md nennen.
  regression_test: DiatonicInterval(1,'d') wirft. interval_between_spellings(C4,B#3) liefert (2,'d',−1) oder dokumentierten Fehler in beiden Richtungen.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K09-01
  priority: P2
  severity: niedrig
  scope_id: K09
  location: src/steps/progression/voice_leading.py:detect_parallel_fifths_octaves (75–116), detect_voice_crossing (47–56)
  revision: 22f3f5f
  description: Antiparallelen werden nicht erkannt, und der Docstring zum Stil JAZZ_POP beschreibt eine Kennzeichnung, die nicht stattfindet.
  reproduction: RUN ~/steps-fable-pack/work/probes/K09_voiceleading.py
  actual: (48,67)→(55,62) und (48,60)→(55,55): keine Meldung. JAZZ_POP liefert immer []. Einklang zählt als Stimmkreuzung. Tonklasse 12 wird als 0 angenommen.
  expected: Im strengen Satz gelten Quinte→Quinte und Oktave→Einklang in Gegenbewegung ebenfalls als Fehler. Docstring und Verhalten gleich.
  rationale: Der Solver selbst ist korrekt: In 250 Zufallsfällen (3–4 Stimmen) stimmt seine L1-Summe mit einer Brute-Force-Suche überein, er ist deterministisch, und unlösbare Vorgaben werfen VoiceLeadingError. "Within one octave" entspricht dem Fenster ±12.
  reference: Herleitung aus der Satzlehre (Antiparallelen). Nicht an einer Quelle geprüft → für die Regel STRONGLY_INDICATED, Verhalten bestätigt.
  impact: Strikter Modus. IMPLEMENTATION.md grenzt vollständigen Kontrapunkt bereits aus.
  fix: Antiparallelen optional melden, Docstring korrigieren.
  regression_test: detect_parallel_fifths_octaves([48,67],[55,62]) meldet einen Eintrag im strengen Stil.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K07-04
  priority: P2
  severity: niedrig
  scope_id: K07
  location: src/steps/progression/engine.py:resolve_roman_degree (468–482)
  revision: 22f3f5f
  description: "vii" und "vii7" ohne Verminderungszeichen liefern in Dur die leiterfremden Akkorde Bm und Bm7. "I+" wird abgewiesen. Fehlerklassen sind uneinheitlich.
  reproduction: RUN -c "from src.steps.progression import resolve_roman_degree as R; print(R('vii').symbol, R('vii7').symbol); R('#VII','A#')"
  actual: Bm Bm7 und InvalidAlterationError
  expected: Vertretbar sind Bm (wörtliche Lesart) oder ein Hinweis auf vii°. Für nicht darstellbare Grundtöne ProgressionParsingError.
  rationale: Die diatonische VII. Stufe in Dur ist vermindert. I7 → Cmaj7 und IV7 → Fmaj7 folgen der diatonischen Lesart. Die Pop-Lesart als Dominantseptakkord ist nur über "dom7" erreichbar. Beides ist vertretbar und im Docstring angedeutet.
  reference: Open Music Theory, Roman Numerals (Sonderzeichen für vermindert). Herleitung.
  impact: resolve_roman_degree.
  fix: Dokumentieren. Fremde Fehlertypen in ProgressionParsingError einhüllen. "+" als Alias für aug zulassen.
  regression_test: R("I+").symbol == "Caug". R("#VII","A#") wirft ProgressionParsingError.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K05-04
  priority: P2
  severity: niedrig
  scope_id: K05
  location: src/steps/theory/chord.py:parse_chord (450, 481, 490)
  revision: 22f3f5f
  description: Nachsichtige Eingaben werden ohne Hinweis angenommen.
  reproduction: RUN -c "from src.steps.theory import parse_chord as C; print(C('C/E5','INT').bass.octave, C('bb','INT').symbol, C('C maj7','INT').symbol)"
  actual: 53 Bb Cmaj7
  expected: "C/E5" abweisen (Oktavziffer gehört nicht ins Symbol). Kleinbuchstaben und Leerzeichen dokumentieren oder abweisen. Unicode-Vorzeichen ("B♭maj7") werden dagegen abgewiesen.
  rationale: An "E5" wird "3" angehängt, daraus entsteht Oktave 53.
  reference: Herleitung aus Codelesung.
  impact: parse_chord.
  fix: Bass mit eigenem Muster ohne Ziffern prüfen.
  regression_test: parse_chord("C/E5") → ChordConstructionError.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-W01-01
  priority: P2
  severity: niedrig
  scope_id: W01
  location: knowledge/sources/registry.yaml, src/steps/progression/reviewed_progressions.json
  revision: 22f3f5f
  description: Vier der sieben Produktquellen verweisen auf die Buchinstanz "openmusictheorycopy". Eine registrierte Quelle wird von keinem Pilot-Claim zitiert. Ein Locator ist ungenau.
  reproduction: cd ~/steps-fable-audit && grep -n "openmusictheorycopy\|omt-chromatic-subdominants" knowledge/sources/registry.yaml src/steps/progression/reviewed_progressions.json
  actual: ii-v-i, 4-chord-schemas, blues-based-schemas und chromatically-altered-subdominant-chords liegen unter /openmusictheorycopy/. Das Kapitel ii–V–I existiert auch unter /openmusictheory/. "omt-chromatic-subdominants" (dort in der Sektion "Scrapyard") kommt in keinem Claim vor. PROG-001-TONAL-CENTER nennt "Absatz nach Example 4", der einschlägige Absatz steht vor der Legende zu Example 4.
  expected: Kanonische URL, nur genutzte Quellen, genaue Fundstelle.
  rationale: Inhaltlich belegen alle zitierten Stellen die Aussagen (siehe Abschnitt 4, W01). Die Kopie kann ohne Ankündigung verschwinden. Automatischer Abruf lieferte HTTP 403, eine Linkprüfung in CI ist so nicht möglich. rights_status "approved" betrifft nur Verlinkung. OMT steht unter CC BY-SA 4.0, der MTO-Artikel unter Copyright der Society for Music Theory.
  reference: Seiten am 2026-11-12 im Browser gelesen (Titel, Autoren, Key Takeaways).
  impact: Dauerhaftigkeit der Belege. Jede URL-Änderung macht alle abhängigen Freigaben ungültig (gewolltes Verhalten der Sperre).
  fix: URLs auf /openmusictheory/ umstellen und neu freigeben, ungenutzte Quelle entfernen, Locator korrigieren, Lizenzfeld ergänzen.
  regression_test: Jede Quelle im Register wird von mindestens einem Claim zitiert.
  evidence: CONFIRMED
  test_status: NOT_RUN

- id: F-S02-01
  priority: P2
  severity: mittel
  scope_id: S02
  location: SKILL.md (Workflow-Punkte 3 und 5), skills/music-harmony-coach/README.md
  revision: 22f3f5f
  description: Der Router leitet Harmonieaufgaben an den historischen Coach und beschreibt `src/steps/` als zukünftig. Die Coach-README beschreibt den Ordner als nur vorbereitet, obwohl SKILL.md und sechs Referenzdateien vorhanden sind.
  reproduction: cd ~/steps-fable-audit && sed -n 5,12p SKILL.md && cat skills/music-harmony-coach/README.md
  actual: "Harmonieaufgaben: historischen Skill … lesen", "zukünftige src/steps/-Module".
  expected: Verweis auf app/knowledge.py für geprüfte Inhalte und Kennzeichnung des Coachs als nicht aktivierbar.
  rationale: Alle neun Pfade im Router existieren. Der Coach selbst ist vorsichtig formuliert (verbietet erfundene Quellen, trennt H/B), sein Quellregister enthält nur den Platzhalter BOOK-001. Er erlaubt aber Ergänzung durch "allgemeines Wissen". Die zwölf COACH-Fälle im Benchmark sind PENDING.
  reference: Herleitung aus Lesung.
  impact: Agenten, die dem Router folgen.
  fix: Router-Punkte 3 und 5 aktualisieren, Coach-README an den Ist-Stand anpassen.
  regression_test: Strukturprüfung: Router enthält keinen Verweis auf skills/music-harmony-coach als Faktenquelle.
  evidence: CONFIRMED
  test_status: NOT_RUN

- id: F-A04-01
  priority: P2
  severity: niedrig
  scope_id: A04
  location: src/steps/progression/reviewed.py:20 (REGISTRY = DIRECTORY.parents[2] / "knowledge/sources/registry.yaml")
  revision: 22f3f5f
  description: Der Kern liest eine Datei außerhalb des Pakets über die Verzeichnislage des Repositorys. Ein installiertes Paket könnte die Pilotdaten nicht laden.
  reproduction: cd ~/steps-fable-audit && sed -n 17,21p src/steps/progression/reviewed.py
  actual: Pfad relativ zum Repository-Root.
  expected: Daten im Paket oder Pfad als Parameter des Adapters in app/.
  rationale: Die Importrichtung stimmt: app/ importiert src/steps, src/steps importiert weder app noch Glide noch tkinter (per grep geprüft). Die Datei-Kopplung widerspricht aber dem Ziel "pure und testbare" Domäne.
  reference: AGENTS.md Nr. 4.
  impact: Paketierung, Desktop-Integration.
  fix: Registerpfad über app/knowledge.py injizieren.
  regression_test: load_reviewed_catalog(registry_path=…) funktioniert aus einem temporären Verzeichnis ohne knowledge/.
  evidence: CONFIRMED
  test_status: NOT_RUN

- id: F-W06-01
  priority: P2
  severity: niedrig
  scope_id: W06
  location: knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv (CLAIM-011), scripts/run_knowledge_benchmark.py (250–266)
  revision: 22f3f5f
  description: Der Benchmark-FAIL KB-M11-ALTER ist berechtigt. CLAIM-011 behauptet weiter "<alter> (-2 to +2)". Die Prüfung selbst ist ein Stringvergleich.
  reproduction: cd ~/steps-fable-audit && $PY -B scripts/run_knowledge_benchmark.py --scope all | grep -v "^BLOCKED"; grep -n "^CLAIM-011" knowledge/sources/MUSIC_SOURCE_CLAIM_REGISTER.csv
  actual: FAIL. Der Fall würde PASS liefern, sobald der Text "decimal" enthält und "(-2 to +2)" fehlt.
  expected: Korrektur des Claims. alter ist in MusicXML 4.0 ein Dezimaltyp (semitones), der auch Vierteltöne wie 0.5 zulässt.
  rationale: Datenfehler, kein Fehler des Runners. Methoden `manual` und `coach` liefern PASS nur mit Person, Nachweis und Git-SHA aus einer übergebenen Datei, diese Angaben werden wie bei K11 nicht verifiziert. `api_contract` gibt immer PENDING zurück.
  reference: W3C MusicXML 4.0, Datentyp semitones (im Fall selbst verlinkt, nicht erneut abgerufen). Herleitung aus Kenntnis des Formats.
  impact: Benchmark-Gesamtstatus (Exit 1 bei --scope all, nicht in CI).
  fix: CLAIM-011 korrigieren. Für claim_sample strukturierte Felder statt Textsuche.
  regression_test: KB-M11-ALTER PASS nach Korrektur. Zusätzlicher Fall mit alter −0.5.
  evidence: CONFIRMED
  test_status: RUN_FAIL
```

### P3

```yaml
- id: F-K02-03
  priority: P3
  severity: niedrig
  scope_id: K02
  location: src/steps/theory/pitch.py:UNICODE_ACCIDENTALS (67–73), render (233–255), parse_spelling
  revision: 22f3f5f
  description: Die Unicode-Ausgabe ist nicht wieder einlesbar und setzt bei Stammtönen ein Auflösungszeichen. Unbekannte Konventionen werden still als INT behandelt.
  reproduction: RUN -c "from src.steps.theory import parse_spelling as P; x=P('C4','INT'); print(x.render('INT',unicode_accidental=True), x.render('FR')); P('C♯4','INT')"
  actual: C♮4 C4 und MusicTheoryError
  expected: "C4" ohne Zeichen. Einlesen von ♯/♭ oder dokumentierte Einbahnstraße. Fehler bei Konvention "FR".
  rationale: resolve_roman_degree übersetzt ♭/♯ bereits, parse_spelling und parse_chord nicht.
  reference: Herleitung.
  impact: Anzeige, Round-Trip.
  fix: Unicode-Vorzeichen vor dem Parsen normalisieren. Konvention validieren.
  regression_test: parse(render(x, unicode_accidental=True)) == x für alle 35 Schreibweisen.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-K04-01
  priority: P3
  severity: niedrig
  scope_id: K04
  location: src/steps/theory/triad.py:invert_triad_voicing (50–64), seventh.py:make_drop2_voicing (93–107), make_shell_voicing (110–124)
  revision: 22f3f5f
  description: Vorbedingungen werden nicht geprüft.
  reproduction: RUN ~/steps-fable-pack/work/probes/K09_voiceleading.py
  actual: Umkehrung 3 eines Dreiklangs ergibt Grundstellung, −1 die zweite Umkehrung. make_drop2_voicing([48,60,72,84]) = [48,60,60,84] mit Duplikat. make_shell_voicing(200, …) liefert Werte. ADD9 steht als Vierklang unter TriadQuality. #11 ist als 6 statt 18 notiert (auch in CHORD_TEMPLATES für add9 als 2 statt 14).
  expected: Fehler bei ungültiger Umkehrung, nicht enger Lage und MIDI außerhalb 0–127. Einheitliche Darstellung von Erweiterungen.
  rationale: Alle Intervallstrukturen der Drei- und Septakkorde stimmen mit der Terzschichtung überein. Die Tonklassenmengen aller 29 Templates stimmen mit unabhängigen Rezepten überein.
  reference: Herleitung.
  impact: Hilfsfunktionen, Figurenlogik (F-K07-02 hängt an der Darstellung).
  fix: Eingaben prüfen. Erweiterungen durchgehend über 12 notieren.
  regression_test: invert_triad_voicing([60,64,67],3) wirft.
  evidence: CONFIRMED
  test_status: RUN_FAIL

- id: F-S04-01
  priority: P3
  severity: niedrig
  scope_id: S04
  location: skills/SKILL_DESIGN.md:18
  revision: 22f3f5f
  description: Das Skill-Design nennt `knowledge/sources/registry.yaml` leer. Die Datei enthält sieben Quellen.
  reproduction: cd ~/steps-fable-audit && sed -n 18p skills/SKILL_DESIGN.md
  actual: "registry.yaml: leer"
  expected: Aktueller Stand oder Datumsvermerk.
  rationale: Veralteter Zustand. Dieselbe Aussage steht in docs/audit/05_VALIDIERUNGSBERICHT.md ("sources: []").
  reference: knowledge/sources/registry.yaml.
  impact: Orientierung für Agenten.
  fix: Satz aktualisieren.
  regression_test: nicht erforderlich.
  evidence: CONFIRMED
  test_status: NOT_RUN
```

## 4. Unabhängige Gegenproben

Vollständige Liste mit Soll, Ist und Status je Fall: `results/GEGENPROBEN_ROHAUSGABE_2026-11-12.txt`. Viele „Abweichungen“ sind strenge Erwartungen an Randfälle. Wo eine andere Lesart vertretbar ist, steht das im Skript und im Befund.

| Skript | IDs | Fälle | PASS | Abw. | Herkunft der Sollwerte |
|---|---|---|---|---|---|
| `K01_pitch.py` | K01 | 52 | 42 | 10 | C4 = 60, midi = (Oktave+1)·12 + Stammton + Alteration, f = 440·2^((m−69)/12) |
| `K02_spelling.py` | K02 | 42 | 24 | 18 | Tabelle der 35 deutschen Namen, Yale-Tabelle |
| `K03_interval.py` | K03 | 48 | 41 | 7 | Größentabelle, Umkehrregel 9 − n mit Qualitätstausch |
| `K05_chord.py` | K05, K06 | 110 | 88 | 22 | 29 eigene Rezepte, Lead-Sheet-Konvention, Definition Drop-2/Shell |
| `K07_stufen.py` | K07 | 117 | 102 | 15 | Stufentabellen Dur und natürlich Moll, Leitton, Quinte über Ziel |
| `W08_kette.py` | W08, K08, K12 | 30 | 24 | 6 | C-Dur-Skala, Akkorddefinitionen |
| `K09_voiceleading.py` | K04, K09, K10 | 45 | 32 | 13 | Brute-Force-Suche, Satzregeln |
| `K11_mutation.py` | K11, T02 | 20 | 14 | 6 | Anforderung an einen ausreichenden Nachweis |
| `S01_skill.py` | S01 | 13 | 2 | 11 | Protokoll des Skills |

Ausgewählte Einzelfälle:

| Fall | Soll | Herleitung | Ist | Status |
|---|---|---|---|---|
| Cb4 / B#3 / Cbb4 / B##3 MIDI | 59 / 60 / 58 / 61 | Formel | gleich | PASS |
| C-1, G9, Cb-1, G#9 | 0, 127, Fehler, Fehler | MIDI 0–127 | gleich | PASS |
| f(60), f(0), f(127) | 261,6256 / 8,1758 / 12543,854 Hz | Formel | gleich | PASS |
| frequency_to_midi ∘ midi_to_frequency | Identität für 0–127, keine Rundung (69,5 bleibt 69,5) | Logarithmus | gleich | PASS |
| 35 Schreibweisen: Render INT/DE, Round-Trip mit expliziter Konvention | identisch | Namenstabelle | identisch | PASS |
| DE-Render B♭ → AUTO-Parse | B♭ oder Fehler | T02 | H | FAIL (F-K02-01) |
| DE „Heses4“, „Ases4“, „Eses4“, „His4“ | B𝄫, A𝄫, E𝄫, H♯ | Bildungsregel | gleich | PASS |
| DE „Bis4“ | Fehler | B ist erniedrigt | H♯ | FAIL (F-K02-02) |
| 38 Intervallgrößen inkl. d7 = 9, A9 = 15, M13 = 21 | Tabelle | Größentabelle | gleich | PASS |
| Inverse der Transposition, 35 × 38 | Ausgangston | Definition | gleich | PASS |
| Gb4 + v5, E4 + ü6, B#4 − k2 | Dbb5, Cx5, Ax4 | Stufe + Halbtöne | gleich | PASS |
| 29 Templates, Tonklassenmengen | eigene Rezepte | Terzschichtung | gleich | PASS |
| INT „Bm7“ / DE „Bm7“ / DE „Hm7“ | 11 / 10 / 11 als Grundton | Konvention | gleich | PASS |
| „Esus4“, „Asus2“ in AUTO und DE | E sus4, A sus2 | sus ist kein deutsches Suffix | gleich | PASS |
| „C11“, „C7alt“, „Cmi7“, „CM7b5“, „C69“ | Fehler | nicht registriert | Fehler | PASS |
| AUTO „Esmaj7/B“ Bass | 10 | deutsch gelesen | 11 | FAIL (F-K05-01) |
| C-Dur: 55 Stufen inkl. V7/ii = A7, vii°7/ii = C#dim7, V65 = G7/B, V6/5/V = D7/F# | Tabelle | Stufenlehre | gleich bis auf 10 Fälle | 45 PASS, 10 FAIL |
| c-Moll: III7 = Ebmaj7, VII7 = Bb7, iiø7 = Dm7b5, V7/III = Bb7, vii°/V = F#dim, bII6 = Db/F | Tabelle | natürlich Moll, Leitton | gleich | PASS |
| c-Moll „#vi°“ | Adim | erhöhte 6. Stufe | A#dim | FAIL (F-K07-03) |
| Fis-Dur vii°, Des-Dur ♭II, Cis-Dur vii°7 | E#dim, Ebb, B#dim7 | Stufe + Halbtöne | gleich | PASS |
| 28 PROG: resolve(roman) = Akkordspalte | gleich | paarweise | gleich | PASS |
| 336 Transpositionen, Stufenabstand | erhalten | Schreibweisen-Invarianz | 81 Verstöße | FAIL (F-K08-01) |
| Solver gegen Brute-Force, 250 Fälle | gleiche L1-Summe | vollständige Suche | gleich | PASS |
| PROG-003/-009: Tonklassen, Stimmen 60→59, 65→64, 69→68→67 | Sollwerte | Akkordtöne | gleich | PASS |
| Sperre: 10 Mutationen an Daten und Quellen bei alter Freigabe | Sperre | Fassungsbindung | Sperre | PASS |
| Sperre: 6 Fälle ohne echten Nachweis | Sperre | Nachweisanforderung | geladen | FAIL (F-K11-01) |

**Kettenprotokoll (W08, D5)**

| Station | PROG-003 | PROG-009 | Ergebnis |
|---|---|---|---|
| Quelle | `omt-ii-v-i`, Key Takeaways: „ii7–V7–Ima7 in major“ gelesen | `omt-blues-based-schemas`, Key Takeaways: „plagal sigh … IV–iv–I … la–le–sol“ gelesen | belegt. URL liegt auf der Kopie-Instanz (F-W01-01) |
| Notationsquelle | `yale-key-names`, S. 1: as, B, H | gleich | belegt |
| Claim | 3 Claims in `reviewed_progressions.json`. Stimmführungs-Claims sind laut Locator „STEPS-Ableitung“ | 2 Claims | korrekt nachgerechnet. **Bruch:** kein Eintrag im Claim-Register |
| Konzept | Bibliothek nennt „Levine (1995), Nettles (1997)“, Code „omt-ii-v-i“ | Bibliothek „de la Motte (1976)“, Code „omt-roman-numerals, omt-chromatic-subdominants“ | **Bruch:** drei Provenienzen je ID (F-W08-01) |
| Relation | REL-003, REL-004, REL-005, alle `VERIFIED_ACTIVE` ohne Beleg | keine | **Bruch** |
| Skill | weder Curation-Skill noch Router nennen die Pilotdaten | gleich | Skill ist nicht Teil der Kette |
| Algorithmus | ii^7, V^7, I^maj7 → Dm7, G7, Cmaj7 | I, IV, iv, I → C, F, Fm, C | korrekt. Die Sperre selbst ruft den Algorithmus nicht auf, nur der Test |
| Test | `test_pilot_publication.py` mit literalen Tonklassen und MIDI-Werten | gleich | unabhängige Sollwerte, bestätigt |
| Ausgabe `app/knowledge.py` | 4 Claims, Quellen (yale, omt-ii-v-i), `catalog_version` 64 Hex, Datum 2026-11-12 | 3 Claims, Quellen (yale, omt-blues) | korrekt. Bei fehlender Freigabe wird der ganze Katalog gesperrt |
| Konkurrierende Deutung | nicht nötig (C als Tonika gesetzt) | nicht nötig | PROG-001 führt die Moll-Lesart III–VII–i–VI als eigenen Claim, per Test bestätigt |
| Notation der Töne | Countercheck nennt „G–H–D–F“. STEPS liefert nur Tonklassen, keine buchstabierten Akkordtöne | „F–As–C“ ebenso | Schreibweise der Akkordtöne ist nicht maschinell prüfbar (Lücke) |

## 5. Abdeckungsmatrix

| ID | Status | Grund |
|---|---|---|
| K01 | GEPRÜFT | 52 Gegenproben, Code gelesen |
| K02 | GEPRÜFT | Round-Trip 35 × 2, 42 Gegenproben |
| K03 | GEPRÜFT | 48 Gegenproben inkl. zusammengesetzter Intervalle |
| K04 | GEPRÜFT | Strukturen und Randfälle |
| K05 | GEPRÜFT | 29 Templates, 80 Symbole |
| K06 | TEILWEISE | 24 Voicings geprüft, Grenzlagen nicht systematisch |
| K07 | GEPRÜFT | 117 Gegenproben Dur und Moll |
| K08 | GEPRÜFT | 28 Paare, 336 Transpositionen |
| K09 | GEPRÜFT | Brute-Force 250 Fälle. Laufzeit nicht gemessen |
| K10 | TEILWEISE | Vertrag für 0/1/≥2 und vier Layouts geprüft, API.md nur Signaturen abgeglichen |
| K11 | GEPRÜFT | 20 Mutationen in der Kopie |
| K12 | GEPRÜFT | Exporte und Fehlerverhalten |
| K13 | TEILWEISE | Fehlerklassen in Gegenproben beobachtet, Hierarchie nicht vollständig durchgesehen |
| S01 | GEPRÜFT | Alle fünf Skripte gelesen, 13 Gegenproben. E2E mit echtem Register nicht möglich (liegt außerhalb des Repos) |
| S02 | GEPRÜFT | Alle Pfade geprüft |
| S03 | TEILWEISE | Skill und Referenzen gelesen. Keine Coach-Antworten erzeugt, 12 Fälle PENDING |
| S04 | TEILWEISE | Nur die Aussage zum Register geprüft |
| W01 | GEPRÜFT | Alle 7 Quellen im Browser gelesen. MTO-Absätze [29]–[30] nur über Zusammenfassung |
| W02 | TEILWEISE | 21 von 35 VERIFIED_TRUE-Claims, Buchseiten nicht prüfbar |
| W03 | TEILWEISE | Nur Struktur: 37 Einträge, 2 doppelte Titel, kein Lizenz- oder URL-Feld |
| W04 | TEILWEISE | Alle 28 PROG, P12, P19, 4 PAT. Latin-Katalog nicht geöffnet |
| W05 | TEILWEISE | 10 von 97 Relationen. Überwiegend plausibel, teils vage (CR-031, CR-017) |
| W06 | TEILWEISE | Runner und Fälle gelesen, COVERAGE.csv wird laut `--check` aus Daten erzeugt (Skript nicht im Detail gelesen) |
| W07 | TEILWEISE | 66 von 198 Fällen |
| W08 | GEPRÜFT | Kettenprotokoll für beide Progressionen |
| T01 | TEILWEISE | Stichproben. Nicht abgedeckt sind die Fehlklassen aus F-K02-01, F-K05-01 bis -03, F-K07-01 bis -03, F-K08-01 |
| T02 | GEPRÜFT | Negativtests vorhanden (fehlende Freigabe, Locator, falsche Lektion). Identität prinzipiell nicht testbar |
| T03 | GEPRÜFT | Evaluator gelesen |
| T04 | TEILWEISE | Kopfteil und Baseline-Logik gelesen: geprüft wird Identität gegen eine Baseline |
| T05 | TEILWEISE | Methoden `claim_sample`, `manual`, `coach`, `api_contract` gelesen. `render_reviewed_progressions.py` nur ausgeführt |
| T06 | TEILWEISE | Workflows gelesen. `--scope all` und 3.13+ laufen nicht in CI |
| T07 | TEILWEISE | Nur ausgeführt (grün), Fixture-Werte nicht gelesen (Vorgabe) |
| A01 | TEILWEISE | Typen sind eingefroren und hashbar. Es fehlt Serialisierung, Typprüfung (F-K01-01), Stimmenidentität in Voicing |
| A02 | TEILWEISE | Festgestellte Lücken: kein Zeit-, Takt- oder Tick-Modell, `models/` und `ports/` leer, keine buchstabierten Akkordtöne, kein Skalenmodul |
| A03 | GEPRÜFT | F-A03-01 |
| A04 | GEPRÜFT | Importrichtung per grep, F-A04-01 |
| H01 | TEILWEISE | 3 Aussagen aus `docs/audit/` |
| H02 | TEILWEISE | 4 Aussagen aus Master-Audit V2. OpenAI-Prüfpaket: **NICHT_GEPRÜFT** (nur Dateiliste) |

## 6. Historische Behauptungen

| Aussage | Fundort | Reichweite auf `22f3f5f` |
|---|---|---|
| „PASS: 195 interne Markdown-Links geprüft, 0 fehlende“ | `docs/audit/05_VALIDIERUNGSBERICHT.md`, Tabelle | Gilt für das Auditpaket vom 10.11.2026 auf Steps `75329fe`. Der Bericht begrenzt sich selbst auf Dateiexistenz. Die genannten Werkzeuge existieren noch, wurden hier nicht ausgeführt (`NOT_RUN`) |
| „`knowledge/sources/registry.yaml` … hat weiter `sources: []`“ | ebd., Abschnitt „Nicht ausgeführt“ | Überholt. Das Register enthält 7 Quellen |
| „Unabhängige Zweitprüfung … keine Releasefreigabe“ | `docs/audit/00_…`, Kopf | Zutreffend zurückhaltend. Betrifft Glide-Vergleich und Dokumentpaket, nicht den Theoriekern |
| „Testsuite Gesamt 115 Tests 100 % PASS“ | Master-Audit V2, `01_GESAMTBERICHT.md:35` | Heute 120 + 25 Tests. Kern grün, Skill-Suite unter macOS 24 von 25. „100 %“ belegt nur die Assertions |
| „28 Archetypen VALIDIERT … vollständig implementiert“ | ebd., Zeile 37 | Syntaktisch bestätigt (Stufen = Akkorde). Fachlich freigegeben sind 3. Schreibweise bei Transposition fehlerhaft (F-K08-01) |
| „Glide … exakt 0 Importe … in `src/steps/`“, „100 % headless“ | ebd., Zeilen 20–21 | Bestätigt per grep |
| „unabhängigen, evidenzbasierten und lückenlosen Gesamtrevision“ | ebd., Zeile 17 | Nicht haltbar. Die Befunde dieses Berichts lagen im geprüften Bereich |
| „100% CANONICAL REFERENCE & SCHEMA INTEGRITY VERIFIED“ | Ausgabe `scripts/verify_reference_integrity.py` | Identität von IDs, Schemata und Hashes gegen eine Baseline. Keine Aussage über musikalische Richtigkeit. Die fehlerhaften Golden Cases bestehen diese Prüfung |

## 7. Restrisiken und nicht prüfbare Bereiche

- **Buchquellen:** Seitenangaben im Claim-Register (Levine, Kostka/Payne, Mauleón u. a.) sind ohne die Bücher nicht prüfbar. Dasselbe gilt für die Literaturfelder der 25 nicht freigegebenen Progressionen.
- **Externes Register:** `OFFENE_ARBEITSAUFFORDERUNGEN.md` liegt außerhalb des Repositorys. Inhalt und Zustand sind nicht prüfbar.
- **GitHub-Belege:** Die acht Freigabelinks (PR #11, zwei Kommentar-IDs) wurden nicht abgerufen. Ob die Kommentare existieren und die Fingerabdrücke nennen, ist offen.
- **132 Golden Cases, 14 Claims, 87 Relationen, 27 PAT, 17 P-Module, Latin-Katalog** sind fachlich ungeprüft.
- **Rhythmus- und Stilwissen** (Swing-Verhältnisse, Genre-Patterns) wurde nur rechnerisch geprüft, nicht gegen Aufnahmen oder Quellen.
- **Python 3.11** und **Windows** wurden nicht ausgeführt. Die Vorbereitung lief laut Kontextpaket auf 3.15, CI auf 3.11/3.12.
- **Spielbarkeit und Klang** der erzeugten Voicings sind nicht bewertet.
- **Konventionsfragen** ohne eindeutige Norm: I7 als Imaj7, Vorzeichen in Moll, Antiparallelen. Hier braucht es eine Projektentscheidung, kein Audit.

## 8. Fortsetzung

| Offen | Grund | Nächster Schritt |
|---|---|---|
| H02 OpenAI-Prüfpaket | Budget | Drei Kernaussagen aus `OpenAI Steps Bericht.md` gegen `22f3f5f` halten |
| W07 Rest (132 Fälle) | Stichprobe | Alle UNIT-Fälle gegen `src.steps` rechnen, SPEC-Fälle domänenweise lesen |
| W02 Rest, Buchseiten | Quellen fehlen | Claims mit Seitenangabe gegen die Bücher prüfen oder Seitenangaben streichen |
| W04 P- und PAT-Kataloge, Latin | Budget | Drum-Ticks aller 31 PAT nachrechnen, P01–P19 Akkordtöne prüfen |
| W05 Rest (87) | Budget | Relationen ohne Beleg herabstufen, dann stichprobenhaft prüfen |
| S03 Coach-Antworten | keine Antworten vorhanden | Die 12 COACH-Fälle in isolierter Sitzung stellen und bewerten |
| K06 Grenzlagen, K10 API-Vertrag | Budget | Alle 29 Qualitäten × 4 Layouts × Oktaven −1…9 |
| T04, T05, W06 Skriptdetails | Budget | `audit_knowledge_coverage.py` und `render_reviewed_progressions.py` vollständig lesen |
| T06 | nicht ausführbar | CI-Lauf auf 3.11 abwarten, `verify_reference_integrity.py` und `--scope all` als Job erwägen |
| K11 GitHub-Belege | kein Abruf | Kommentar-IDs über die GitHub-API gegen Fingerabdrücke prüfen |
| A01, A02 | nur Lückenliste | Nach Entscheidung über Zeitmodell und Serialisierung erneut bewerten |

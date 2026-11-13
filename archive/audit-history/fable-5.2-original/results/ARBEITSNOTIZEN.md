# Arbeitsnotizen Fable-Audit (Lauf 2026-11-12)

## Phase 1 erledigt
- HEAD 22f3f5f, status: nur untracked .DS_Store (Finder, nicht vom Audit) -> Umgebungsvermerk
- 3.12: Root 120 OK; Skill 25/1 FAIL (test_03 /private/var vs /var, macOS-Symlink, Testbefund); api --check 0; bench pilot 8/0/0, publication 3/0/0, all 37/1/32 exit1; review-sheet 0; render --check 0; coverage --check 0 (mit PyYAML); integrity 0
- 3.13 Root 120 OK; 3.14 Root 120 OK; 3.14 Skill 1 FAIL gleich; 3.14 coverage ohne PyYAML exit 1; 3.11 NOT_RUN

## Phase 2 Stand
- Probes: work/probes/K01_pitch.py (52/10 FAIL), K02_spelling.py (42/18), K03_interval.py (48/7), K05_chord.py inkl. K06 (110/22), K07_stufen.py (117/15)
- Befundkandidaten: AUTO B4 -> INT B, DE-Render B -> AUTO-Parse B natur (Round-Trip-Bruch); DE Bis/Bes/Hses/Ees akzeptiert; Unicode render nicht parsebar, C♮4; bool/float akzeptiert;
  AUTO 'Es'/'Fis'/'Des' Akkord abgewiesen, 'Es7' ok; AUTO 'Esmaj7/B' Bass = INT B (pc 11); CMmaj7 -> m(maj7); C/E5 akzeptiert;
  iadd9 -> Cadd9, ii13 -> D13, IVm, Vb5 -> Gdim, vii -> Bm; Figuren auf nicht-terzgeschichteten Templates (Iadd9(6) -> /Ebb, V7sus4(65) -> /B#, V7#11(42) Fehler);
  Moll: #vi° -> A#dim, vi° -> Abdim, Adim unerreichbar; analyze_progression Rückgabeschlüssel inkonsistent; transpose_chromatic mischt Schreibweisen
- offen P0: K11 Mutation, W01, W08
- K11 Mutation (work/probes/K11_mutation.py, 20/6 FAIL): Sperre erkennt veraltete Fingerabdrücke, fehlende/unbekannte Freigaben, fremdes Repo, Quellenänderung; erkennt NICHT: nicht existierenden Link, beliebigen Reviewer, Zukunftsdatum, Selbstfreigabe falscher Inhalte, voice_path-Unsinn, thematisch fremde Quelle. Testfixture trägt selbst 'fixture-reviewer' ein.
- W01: alle 7 Quellen im Browser erreichbar (WebFetch 403 bei pressbooks). Locator bestätigt: yale (As/B/H), omt-ii-v-i Key Takeaways (ii7–V7–Ima7), 4-chord (I–V–vi–IV; Absatz steht VOR Example-4-Legende), blues (IV–iv–I, la–le–sol), roman-numerals (Example 3, Groß/Klein), MTO [1],[9]-[11] ok, [29]-[30] nur Zusammenfassung. 4 URLs zeigen auf /openmusictheorycopy/ (Kopie; kanonisch /openmusictheory/ existiert). omt-chromatic-subdominants von keinem Pilot-Claim zitiert (Sektion SCRAPYARD).
- W08 (work/probes/W08_kette.py 30/6): Kette ok bis auf: Bestandskatalog PROG-009 nennt andere Quellen als Freigabe; Bibliotheks-MD nennt Levine/Nettles bzw. de la Motte; Claim-Register CSV nicht mit Pilot-Claims verknüpft; PROG-009 ohne Relation; REL-003/004 VERIFIED_ACTIVE ungeprüft; Transposition mischt Schreibweise (81/336)
- K08: 28 PROG resolve==chords PASS

## Phase 2 abgeschlossen. Phase 3 offen: K04 K06(teilw. erledigt in K05_chord.py) K09 K10 S01 W02 W04 W06 W07 T01 T02 T03 T05 A03

## Phase 3-5 erledigt (Stichworte)
- K09 Solver == Brute-Force 250/250; Antiparallelen nicht erkannt; K10 Rückgabeschlüssel inkonsistent, Kreuzung nie erkannt (sortiert); K04 Randfälle
- S01 (work/probes/S01_skill.py 13/11 FAIL): DONE_VERIFIED ohne Nachweis; %LOCALAPPDATA% wörtlich auf POSIX -> Seiteneffektdatei; restore ohne Sicherung; EXPLICIT-Injection; CLI-Mismatch detect_duplicates
- W07: 66 Golden Cases gelesen (38 SPEC): fehlerhaft REF-0014, REF-0043, REF-0176, REF-0189 (Begriff); aussagelos REF-0096, REF-0100, REF-0154; 16 Literalvergleiche im Evaluator
- W02: 21 VERIFIED_TRUE-Claims: CLAIM-035 falsch (Take Five 5/4, Money 7/4), CLAIM-038 Surdo-Begriff fraglich; kein Skript setzt Status
- W04: Bibliothek PROG-019 'i^6' != Engine 'im6'; Quellenangaben divergieren; PROG-024 Ipanema-Zuschreibung
- W06: KB-M11-ALTER FAIL berechtigt (CLAIM-011 weiter falsch)
- S02/S03/S04, W03, W05, T03-T06, A01-A04, H01/H02 stichprobenhaft
- Rohausgabe: results/GEGENPROBEN_ROHAUSGABE_2026-11-12.txt (477 Fälle, 369 PASS, 108 FAIL)
- Checkout nach allen Phasen sauber (nur .DS_Store untracked, vom Finder)
## Phase 6: Bericht results/FABLE_AUDIT_REPORT_2026-11-12.md
- Bericht geschrieben und Reproduktionen nachgeprüft (14 Einzeiler laufen wie angegeben).

# STEPS-Wissensbenchmark · Ergebnis

Commit `dd1f0baf4b8aef16768792b7e05f05d8b75a81b2` · Arbeitsbaum sauber.

| Bereich | Bestanden | Fehlgeschlagen | Ungeprüft |
|---|---:|---:|---:|
| pilot | 8 | 0 | 0 |
| catalog | 25 | 0 | 0 |
| sample | 48 | 0 | 3 |
| coach | 0 | 0 | 12 |
| publication | 3 | 0 | 0 |
| api | 7 | 0 | 0 |
| backlog | 1 | 0 | 12 |

| Pflichtinhalt | Freigabesperre |
|---|---|
| PAT-031 | KB-M08-METER |
| P02 | KB-M12-PLAYABILITY |
| Harmony Coach | COACH-01, COACH-02, COACH-03, COACH-04, COACH-05, COACH-06, COACH-07, COACH-08, COACH-09, COACH-10, COACH-11, COACH-12 |
| PROG-001-HÖRPRAXIS | KB-M09-LOOP-HEAR |
| SRC-033 | KB-SRC-033-PROVENANCE |
| Wissensgraph | KB-GRAPH-NODES |
| F00412 | KB-HISTORY-F00412 |
| F00571 | KB-HISTORY-F00571 |
| F00704 | KB-HISTORY-F00704 |
| F00768 | KB-HISTORY-F00768 |
| F00937 | KB-HISTORY-F00937 |
| F01002 | KB-HISTORY-F01002 |
| PPR-MIDI-01 | KB-HISTORY-PPR-MIDI-01 |
| PPR-MIDI-02 | KB-HISTORY-PPR-MIDI-02 |
| PPR-MIDI-03 | KB-HISTORY-PPR-MIDI-03 |
| PPR-MIDI-04 | KB-HISTORY-PPR-MIDI-04 |

## Harmony Coach · Domänenabdeckung

| Domäne | Aufgaben | Antworten geprüft | Ausstehend |
|---|---:|---:|---:|
| M01 | 1 | 0 | 1 |
| M02 | 1 | 0 | 1 |
| M03 | 1 | 0 | 1 |
| M04 | 1 | 0 | 1 |
| M05 | 1 | 0 | 1 |
| M06 | 1 | 0 | 1 |
| M07 | 1 | 0 | 1 |
| M08 | 1 | 0 | 1 |
| M09 | 1 | 0 | 1 |
| M10 | 1 | 0 | 1 |
| M11 | 1 | 0 | 1 |
| M12 | 1 | 0 | 1 |

## pilot

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| PILOT-NOTATION-001 | M02 | PILOT | PASS | [[59, 59], [58, 58], [68, 68]] |  |
| PROG-001-HARMONY | M05 | PROG-001 | PASS | {'key': 'C', 'stages': ['I', 'V', 'vi', 'IV'], 'chords': ['C', 'G', 'Am', 'F'], 'written': [[0, 4, 7], [2, 7, 11], [0, 4, 9], [0, 5, 9]], 'resolved': [[0, 4, 7], [2, 7, 11], [0, 4, 9], [0, 5, 9]]} |  |
| PROG-003-HARMONY | M05 | PROG-003 | PASS | {'key': 'C', 'stages': ['ii^7', 'V^7', 'I^maj7'], 'chords': ['Dm7', 'G7', 'Cmaj7'], 'written': [[0, 2, 5, 9], [2, 5, 7, 11], [0, 4, 7, 11]], 'resolved': [[0, 2, 5, 9], [2, 5, 7, 11], [0, 4, 7, 11]]} |  |
| PROG-009-HARMONY | M05 | PROG-009 | PASS | {'key': 'C', 'stages': ['I', 'IV', 'iv', 'I'], 'chords': ['C', 'F', 'Fm', 'C'], 'written': [[0, 4, 7], [0, 5, 9], [0, 5, 8], [0, 4, 7]], 'resolved': [[0, 4, 7], [0, 5, 9], [0, 5, 8], [0, 4, 7]]} |  |
| PROG-001-TONAL-CENTER | M09 | PROG-001 | PASS | {'written': ['C', 'G', 'Am', 'F'], 'relative_minor': ['C', 'G', 'Am', 'F'], 'note': 'Rechnerische Lesart. Höreindruck bleibt kontextabhängig.'} |  |
| PROG-003-VOICE-II-V | M06 | PROG-003 | PASS | {'path': [[0, 'C4'], [1, 'H3']], 'midi': [60, 59], 'delta': [-1]} |  |
| PROG-003-VOICE-V-I | M06 | PROG-003 | PASS | {'path': [[1, 'F4'], [2, 'E4']], 'midi': [65, 64], 'delta': [-1]} |  |
| PROG-009-VOICE-LEADING | M06 | PROG-009 | PASS | {'path': [[1, 'A4'], [2, 'As4'], [3, 'G4']], 'midi': [69, 68, 67], 'delta': [-1, -1]} |  |

## catalog

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| KB-PROG-008-01 | M06 | PROG-008 | PASS | {'stage': 'Idom7', 'resolved': 'C7', 'written': 'C7'} |  |
| KB-PROG-008-02 | M06 | PROG-008 | PASS | {'stage': 'IVdom7', 'resolved': 'F7', 'written': 'F7'} |  |
| KB-PROG-008-03 | M06 | PROG-008 | PASS | {'stage': 'Idom7', 'resolved': 'C7', 'written': 'C7'} |  |
| KB-PROG-008-05 | M06 | PROG-008 | PASS | {'stage': 'IVdom7', 'resolved': 'F7', 'written': 'F7'} |  |
| KB-PROG-008-06 | M06 | PROG-008 | PASS | {'stage': 'Idom7', 'resolved': 'C7', 'written': 'C7'} |  |
| KB-PROG-016-01 | M06 | PROG-016 | PASS | {'stage': 'I^maj7', 'resolved': 'Bmaj7', 'written': 'Bmaj7'} |  |
| KB-PROG-016-03 | M06 | PROG-016 | PASS | {'stage': 'bVI^maj7', 'resolved': 'Gmaj7', 'written': 'Gmaj7'} |  |
| KB-PROG-016-05 | M06 | PROG-016 | PASS | {'stage': 'bIV^maj7', 'resolved': 'Ebmaj7', 'written': 'Ebmaj7'} |  |
| KB-PROG-020-02 | M06 | PROG-020 | PASS | {'stage': 'bII^7(#11)', 'resolved': 'Db7(#11)', 'written': 'Db7(#11)'} |  |
| KB-PROG-027-05 | M06 | PROG-027 | PASS | {'stage': 'V^7(#11)', 'resolved': 'G7(#11)', 'written': 'G7(#11)'} |  |
| KB-P05-NOTEN | M10 | P05 | PASS | {'voicings': [['Dm7', [50], [60, 65]], ['G7', [43], [59, 65]], ['Cmaj7', [48], [59, 64]]], 'motions': [[-1, 0], [0, -1]]} |  |
| KB-P06-NOTEN | M10 | P06 | PASS | {'voicings': [['Csus4', [48], [65, 67]], ['Csus2', [48], [62, 67]], ['Cadd9', [48], [64, 67, 74]], ['Cmadd9', [48], [63, 67, 74]], ['C9', [48], [64, 67, 70, 74]]]} |  |
| KB-P08-NOTEN | M10 | P08 | PASS | {'voicings': [['Eng', [62], [65, 69, 72]], ['Drop-2', [57], [62, 65, 72]], ['Drop-2 verteilt', [57, 62], [65, 72]]], 'octave_drop': 12, 'right_span': 10, 'distributed_hand_spans': [5, 7], 'bass': 57} |  |
| KB-P12 | M10 | P12 | PASS | {'upper': [0, 4, 5, 9], 'total': [0, 2, 4, 5, 9], 'bass': 2, 'row': '\| `P12` \| **Zweihändige Rootless Voicings** \| Den weichen Neo-Soul & Lo-Fi Sound spielen \| LH spielt Grundton D; RH spielt den Vierklang Fmaj7 (F–A–C–E) als grundtonlose Oberstruktur. Zusammen ergibt sich Dm9 mit Grundton \| Phase 4.9/4.10 \|'} |  |
| KB-P16 | M10 | P16 | PASS | {'bass': 0, 'left': [0, 4, 10], 'right': [2, 6, 9], 'upper_intervals': [14, 18, 21], 'omitted_fifth': True} |  |
| KB-P18-VOICINGS | M10 | P18 | PASS | {'symbols': ['Fm7', 'Bb7', 'Cmaj7'], 'bass': [53, 46, 48], 'right': [[56, 63, 67], [56, 60, 62], [55, 59, 64]], 'added_pitch_classes': [[7], [0], []], 'omitted_pitch_classes': [[0], [5], []], 'resolution': [-1, -1, 2]} |  |
| KB-P19 | M10 | P19 | PASS | {'delta': [-1, -1, -2, -2], 'dominant': 'D7/A', 'bass': 9, 'dominant_tones': [0, 2, 6, 9], 'row': '\| `P19` \| **Chromatische Bassführung für Sekundärdominanten** \| Fließende Basslinien in Kadenzen spielen \| $I \\to V^7/V(6/5) \\to ii^6 \\to I^6 \\to V^7_{4/3} \\to I$ ($G \\to C\\sharp \\to C\\natural \\to B \\to A \\to G$); C♯–C–H in Halbtönen, H–A–G in zwei Ganztonschritten \| Phase 4.13/4.14 \|', 'catalog': '\| `PROG-026` \| Secondary Dominant Chromatic Bassline \| `I - V7(6/5)/V - ii6 - I6 - V7(4/3) - I` \| `G - A7/C# - Am/C - G/B - D7/A - G` \| Barock, Klassik, Latin Jazz \| Kostka (2013), Aldwell (1989) \|'} |  |
| KB-PAT-031-RASTER | M08 | PAT-031 | PASS | {'ppq': 480, 'bpm': 120, 'pulse_ticks': 240, 'bell_onsets': [0, 480, 960, 1200, 1680, 2160, 2640], 'beat_onsets': [0, 720, 1440, 2160], 'barlines': {'12': [0, 2880], '6': [0, 1440, 2880]}, 'cycle_seconds': 2.0} |  |
| KB-CONTROL-BLUES | M06 | PROG-008 | PASS | [['C7', [0, 4, 7, 10]], ['F7', [0, 3, 5, 9]]] |  |
| KB-CONTROL-P12 | M10 | P12 | PASS | [[0, 4, 5, 9], [0, 2, 4, 5, 9]] |  |
| KB-CONTROL-P19 | M10 | P19 | PASS | [-1, -1, -2, -2] |  |
| KB-PAT-027-RASTER | M08 | PAT-027 | PASS | {'meter': [4, 4], 'bpm': 128, 'beat_unit': 'Viertel', 'ppq': 480, 'bars': 2, 'ticks_per_bar': 1920, 'onsets': [0, 720, 1440, 2400, 3120], 'bar_seconds': 1.875} |  |
| KB-PAT-028-RASTER | M08 | PAT-028 | PASS | {'meter': [4, 4], 'bpm': 116, 'beat_unit': 'Viertel', 'ppq': 480, 'bars': 1, 'ticks_per_bar': 1920, 'onsets': [1440, 1680], 'bar_seconds': 2.068966} |  |
| KB-PAT-029-RASTER | M08 | PAT-029 | PASS | {'meter': [2, 2], 'bpm': 105, 'beat_unit': 'Halbe', 'ppq': 480, 'bars': 1, 'ticks_per_bar': 1920, 'onsets': [0, 960], 'bar_seconds': 1.142857} |  |
| KB-PAT-026-TICKS | M07 | PAT-026 | PASS | {'ppq': 480, 'onset': 154, 'offset': 34} |  |

## sample

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| KB-M01-A4 | M01 | M01 | PASS | [440.0, 261.6255653005986] |  |
| KB-M02-ENHARMONIC | M02 | M02 | PASS | [61, 61, 'C#4', 'Db4'] |  |
| KB-M03-HARMONIC-MINOR | M03 | M03 | PASS | 3 |  |
| KB-M04-MAJOR-MINOR | M04 | M04 | PASS | [[0, 4, 7, 11], [0, 3, 7, 10]] |  |
| KB-M05-APPLIED | M05 | M05 | PASS | D7 |  |
| KB-M07-CLAVE | M07 | CLAIM-036 | PASS | [0, 720, 1440, 2400, 2880] |  |
| KB-M08-METER | M08 | PAT-031 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Die vorhandenen Hörproben mit einem 12/8-Takt und zwei 6/8-Takten vergleichen. Wahrgenommene Taktanfänge und den musikalischen Verwendungszweck protokollieren. |
| KB-M11-ALTER | M11 | CLAIM-011 | PASS | ['0.5', '-0.5'] |  |
| KB-M12-PLAYABILITY | M12 | P02 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Zwei notierte Voicing-Folgen bei definiertem Tempo mit kleiner Handspanne spielen. Fingersatz, Abstand und mindestens einen Fall mit niedriger L1-Distanz und unbequemer Lage protokollieren. |
| KB-M07-SWING-SOURCE | M07 | CLAIM-034 | PASS | {'journal': 'Music Perception', 'volume_issue': '19(3)', 'pages': '333–349', 'doi': '10.1525/mp.2002.19.3.333'} |  |
| KB-M09-LOOP-HEAR | M09 | PROG-001-HÖRPRAXIS | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Zwei Audiofassungen mit C- bzw. A-zentrierter Melodie erstellen und einer fachkundigen Person in verdeckter Reihenfolge vorspielen. |
| KB-GRAPH-CDR-005 | M03 | CDR-005 | PASS | [1, 2, 1, 2, 2, 2, 2] |  |
| KB-GRAPH-CDR-006 | M03 | CDR-006 | PASS | [2, 2, 2, 1, 2, 1, 2] |  |
| KB-GRAPH-CDR-009 | M04 | CDR-009 | PASS | [55, 60, 64, 71] |  |
| KB-GRAPH-CDR-010-COUNTEREXAMPLE | M04 | CDR-010 | PASS | {'two_triads': [0, 2, 4, 6, 7, 9], 'slash_bass': [0, 2, 6, 9], 'target': [0, 2, 4, 6, 7, 9, 11], 'missing_from_two_triads': [11]} |  |
| KB-GRAPH-CDR-001 | M11 | CDR-001 | PASS | [60, 0] |  |
| KB-GRAPH-CDR-002 | M11 | CDR-002 | PASS | [59, 11] |  |
| KB-GRAPH-CDR-003 | M11 | CDR-003 | PASS | [58, 10] |  |
| KB-GRAPH-CDR-004 | M11 | CDR-004 | PASS | 28 |  |
| KB-GRAPH-CDR-007 | M11 | CDR-007 | PASS | [52, 55, 59, 62] |  |
| KB-GRAPH-CDR-008 | M11 | CDR-008 | PASS | [59, 62, 64, 67] |  |
| KB-GRAPH-CDR-011 | M11 | CDR-011 | PASS | ['D7', 'D7'] |  |
| KB-GRAPH-CDR-013 | M11 | CDR-013 | PASS | ['Cm', 'Fm', 'G7', 'Fm'] |  |
| KB-GRAPH-CDR-015 | M11 | CDR-015 | PASS | 146 |  |
| KB-GRAPH-CDR-016 | M11 | CDR-016 | PASS | 139 |  |
| KB-GRAPH-CDR-018 | M11 | CDR-018 | PASS | [0, 720, 1440, 2400, 2880] |  |
| KB-GRAPH-CDR-010-RESOLUTION | M11 | CDR-010 | PASS | {'target_id': 'C6_9_SHARP11_COLLECTION', 'pitch_classes': [0, 2, 4, 6, 7, 9], 'major_seventh_present': False, 'production_use_allowed': False} |  |
| KB-GRAPH-ONTOLOGY-RECOVERY | M11 | HISTORICAL-ONTOLOGY-RECOVERY | PASS | {'originals': 12, 'historical_definitions': 41, 'fachabnahme': 'AUSSTEHEND'} |  |
| KB-NIGHT-FREQUENCY | M11 | NIGHT-MODEL-FREQUENCY | PASS | [261.625565, 440.0, 523.251131] |  |
| KB-NIGHT-MOD12 | M11 | NIGHT-MODEL-MOD12 | PASS | [0, 0, 0, 1, 7] |  |
| KB-NIGHT-ENHARMONIC | M11 | NIGHT-MODEL-ENHARMONIC | PASS | [['C', 1, 1], ['D', -1, 1]] |  |
| KB-NIGHT-DE_H_B | M11 | NIGHT-MODEL-DE_H_B | PASS | [['B', 0, 11], ['B', -1, 10]] |  |
| KB-NIGHT-DIATONIC | M11 | NIGHT-MODEL-DIATONIC | PASS | ['C', 'Dm', 'Em', 'F', 'G', 'Am', 'Bdim'] |  |
| KB-NIGHT-RELATIVE_COLLECTION | M11 | NIGHT-MODEL-RELATIVE_COLLECTION | PASS | [[0, 2, 4, 5, 7, 9, 11], [0, 2, 4, 5, 7, 9, 11]] |  |
| KB-NIGHT-MINOR_DOMINANT | M11 | NIGHT-MODEL-MINOR_DOMINANT | PASS | ['G7'] |  |
| KB-NIGHT-TRIADS | M11 | NIGHT-MODEL-TRIADS | PASS | [[0, 4, 7], [0, 3, 7], [0, 3, 6], [0, 4, 8]] |  |
| KB-NIGHT-INVERSION | M11 | NIGHT-MODEL-INVERSION | PASS | [[0, 0], [0, 4], [0, 7]] |  |
| KB-NIGHT-SEVENTHS | M11 | NIGHT-MODEL-SEVENTHS | PASS | [[0, 4, 7, 11], [0, 3, 7, 10]] |  |
| KB-NIGHT-CADENCE | M11 | NIGHT-MODEL-CADENCE | PASS | ['G7', 'C'] |  |
| KB-NIGHT-BORROWED | M11 | NIGHT-MODEL-BORROWED | PASS | ['Fm'] |  |
| KB-NIGHT-TRITONE | M11 | NIGHT-MODEL-TRITONE | PASS | [[2, 5, 7, 11], [1, 5, 8, 11]] |  |
| KB-NIGHT-PARALLELS | M11 | NIGHT-MODEL-PARALLELS | PASS | True |  |
| KB-NIGHT-L1 | M11 | NIGHT-MODEL-L1 | PASS | 3 |  |
| KB-NIGHT-METRIC_DUALITY | M11 | NIGHT-MODEL-METRIC_DUALITY | PASS | True |  |
| KB-NIGHT-POLYRHYTHM | M11 | NIGHT-MODEL-POLYRHYTHM | PASS | 12 |  |
| KB-NIGHT-SWING64 | M11 | NIGHT-MODEL-SWING64 | PASS | [154, 34, 32.19697] |  |
| KB-NIGHT-WHITE_KEYS | M11 | NIGHT-MODEL-WHITE_KEYS | PASS | [[0, 2, 4, 5, 7, 9, 11]] |  |
| KB-NIGHT-XML | M11 | NIGHT-MODEL-XML | PASS | {'step': 'D', 'alter': '-1', 'octave': '4'} |  |
| KB-NIGHT-SAME_ROOT_SHIFT | M11 | NIGHT-MODEL-SAME_ROOT_SHIFT | PASS | {'root_preserved': True, 'common': [0, 2, 9], 'removed': [6], 'added': [5]} |  |
| KB-NIGHT-BASS_AMBIGUITY | M11 | NIGHT-MODEL-BASS_AMBIGUITY | PASS | [[0, 4], [4, 4], [9, 4]] |  |
| KB-NIGHT-NEW_PIANO_DRAFT | M11 | NIGHT-MODEL-NEW_PIANO_DRAFT | PASS | {'total_ticks': 7680, 'events': 16, 'onsets': [0, 720, 960, 1680, 1920, 2640, 2880, 3600, 3840, 4560, 4800, 5520, 5760, 6480, 6720, 7440], 'clave_relation': 'SHARED_GRID_ONLY_NOT_HISTORICAL_STYLE_PROOF', 'historical_transcription': False} |  |

## coach

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| COACH-01 | M05 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | Die Frage COACH-01 in einer isolierten Session mit dem historischen Skill stellen. Antwort, Modell, Quellen und Bewertung aller Pflichtbestandteile protokollieren. |
| COACH-02 | M09 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | Die Frage COACH-02 in einer isolierten Session mit dem historischen Skill stellen. Antwort, Modell, Quellen und Bewertung aller Pflichtbestandteile protokollieren. |
| COACH-03 | M04 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | Die Frage COACH-03 in einer isolierten Session mit dem historischen Skill stellen. Antwort, Modell, Quellen und Bewertung aller Pflichtbestandteile protokollieren. |
| COACH-04 | M07 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | Die Frage COACH-04 in einer isolierten Session mit dem historischen Skill stellen. Antwort, Modell, Quellen und Bewertung aller Pflichtbestandteile protokollieren. |
| COACH-05 | M02 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | Die Frage COACH-05 in einer isolierten Session mit dem historischen Skill stellen. Antwort, Modell, Quellen und Bewertung aller Pflichtbestandteile protokollieren. |
| COACH-06 | M01 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-06 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-07 | M03 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-07 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-08 | M06 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-08 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-09 | M08 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-09 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-10 | M10 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-10 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-11 | M11 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-11 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |
| COACH-12 | M12 | Harmony Coach | PENDING | Keine Coach-Antwort mit menschlicher Bewertung erfasst. | COACH-12 mit festgehaltenem Modell und dem historischen Skill ausführen, Rohantwort sichern und anhand der Sollbestandteile fachlich bewerten. |

## publication

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| KB-PUB-VALID | M12 | Pilot-Freigabeprüfung | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.413s  OK |  |
| KB-PUB-UNKNOWN-SOURCE | M12 | Pilot-Freigabeprüfung | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.568s  OK |  |
| KB-PUB-FALSE-LESSON | M12 | Pilot-Freigabeprüfung | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.736s  OK |  |

## api

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| KB-API-SUS-NOTATION | M04 | Theory-API | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.000s  OK |  |
| KB-API-PARENTHESES | M04 | Theory-API | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.000s  OK |  |
| KB-API-OPEN-ROTATION | M04 | Theory-API | PASS | . ---------------------------------------------------------------------- Ran 1 test in 0.000s  OK |  |
| KB-CONTRACT-AUTO | M04 | Theory-API | PASS | {'Cis/DE': 'C#', 'Cis/AUTO': 'C#', 'Es/DE': 'Eb', 'Es/AUTO': 'Eb', 'Es7/DE': 'Eb7', 'Es7/AUTO': 'Eb7'} |  |
| KB-CONTRACT-ANALYSIS | M06 | Theory-API | PASS | {'empty': ['average_l1_step', 'average_l1_step_per_voice', 'circular_pc_distance', 'max_single_voice_jump', 'motion_distribution', 'outer_voice_motions', 'parallel_violations', 'total_circular_distance', 'total_l1_distance', 'transition_count', 'voice_crossings_count'], 'one': ['average_l1_step', 'average_l1_step_per_voice', 'circular_pc_distance', 'max_single_voice_jump', 'motion_distribution', 'outer_voice_motions', 'parallel_violations', 'total_circular_distance', 'total_l1_distance', 'transition_count', 'voice_crossings_count'], 'two': ['average_l1_step', 'average_l1_step_per_voice', 'circular_pc_distance', 'max_single_voice_jump', 'motion_distribution', 'outer_voice_motions', 'parallel_violations', 'total_circular_distance', 'total_l1_distance', 'transition_count', 'voice_crossings_count']} |  |
| KB-CONTRACT-COMPOUND | M04 | Theory-API | PASS | {'Cadd9': [0, 4, 7, 14], 'C7(#11)': [0, 4, 7, 10, 18], 'C9': [0, 4, 7, 10, 14]} |  |
| KB-CONTRACT-DROP2 | M04 | Theory-API | PASS | {'CLOSE': [0, 2, 4, 9, 10], 'DROP2': [0, 4, 9, 10]} |  |

## backlog

| Fall | Domäne | Inhalt | Ergebnis | Beobachtung | Nächster Prüfschritt |
|---|---|---|---|---|---|
| KB-SRC-033-PROVENANCE | M03 | SRC-033 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Die angegebene Publikation bibliografisch suchen und von Oliver Prehns Lehrseite abgrenzen. Originalausgabe oder Katalognachweis mit Fundstelle vorlegen. |
| KB-CLAIM-032-MINOR | M06 | CLAIM-032 | PASS | {'major': [-1, -1], 'minor': [-1, -2]} |  |
| KB-GRAPH-NODES | M12 | Wissensgraph | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Die sechs verbleibenden Definitionen und alle 97 Kanten fachlich prüfen. 41 historische Definitionen wurden im Original wiedergefunden, zwei P10-Begriffe als Projektstrategie eingegrenzt; daraus folgt keine Fachabnahme. |
| KB-HISTORY-F00412 | M12 | F00412 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-F00571 | M12 | F00571 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-F00704 | M12 | F00704 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-F00768 | M12 | F00768 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-F00937 | M12 | F00937 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-F01002 | M12 | F01002 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Archivkette und Live-Bandcamp-CDN liefern identische Registerbytes (14.11.2026). Rechte am vollständigen Bundle und dauerhafte Archivzuordnung dokumentieren; eine Fachfreigabe liegt nicht vor. |
| KB-HISTORY-PPR-MIDI-01 | M12 | PPR-MIDI-01 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Originallieferung, Dateiliste, Prüfsummen und Rechtebeleg für das MIDI-Paket vorlegen. Das Register enthält einen Platzhalter. |
| KB-HISTORY-PPR-MIDI-02 | M12 | PPR-MIDI-02 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Originallieferung, Dateiliste, Prüfsummen und Rechtebeleg für das MIDI-Paket vorlegen. Das Register enthält einen Platzhalter. |
| KB-HISTORY-PPR-MIDI-03 | M12 | PPR-MIDI-03 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Originallieferung, Dateiliste, Prüfsummen und Rechtebeleg für das MIDI-Paket vorlegen. Das Register enthält einen Platzhalter. |
| KB-HISTORY-PPR-MIDI-04 | M12 | PPR-MIDI-04 | PENDING | Hör-, Spiel- oder Fachabnahme ausstehend. | Originallieferung, Dateiliste, Prüfsummen und Rechtebeleg für das MIDI-Paket vorlegen. Das Register enthält einen Platzhalter. |

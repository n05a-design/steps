# Abnahmebogen für die Fachperson (Stand 16.11.2026)

**Zweck:** Am 16.11.2026 hat der Inhaber sechs Graphknoten festgelegt, und mehrere Zusammenfassungen wurden am Original-PDF nachgeprüft. Nichts davon ist fachlich abgenommen. Dieser Bogen bündelt die Punkte, die eine Fachperson bestätigen, korrigieren oder als unbelegt markieren soll.

**Abgrenzung:** Der Bogen ist ein Arbeitsdokument, kein Teil des maschinell geprüften Pilot-Registers ([`PILOT_ABNAHME.md`](../../../knowledge/benchmark/PILOT_ABNAHME.md)). Eine Freigabe hier ändert keinen Status im Graphen automatisch. Sie wird anschließend in einem eigenen PR übernommen.

**Schreibweise:** Tonnamen sind international (B = deutsches H, Bb = deutsches B). Tonhöhen stehen in wissenschaftlicher Notation mit C4 = eingestrichenes c = MIDI 60.

## So ausfüllen

Je Punkt eine Entscheidung ankreuzen und Name sowie Datum eintragen:

- **freigegeben:** Die Aussage stimmt im angegebenen Geltungsbereich.
- **Korrektur:** Die Aussage ist falsch oder zu weit. Bitte die konkrete Stelle und die richtige Fassung nennen.
- **Beleg fehlt:** Die Aussage ist vielleicht richtig, aber nicht ausreichend belegt. Bitte sagen, welcher Beleg fehlt.

Die Entscheidung kann direkt in dieser Datei (per PR) oder als Kommentar am zugehörigen PR eingetragen werden.

---

## Teil A · Graphknoten

### A1 · CDR-012 `MODAL_SHIFT_TO_II7`

- Festlegung · Der Knoten bedeutet II7 → ii7 auf gleichem Grundton. Der Name „TO_II7“ gilt als historische Fehlbenennung. Neue Benennung: `SAME_ROOT_MAJOR_TO_MINOR_SEVENTH`.
- Fundstelle · [Entscheidung zu CDR-012](ENTSCHEIDUNG_CDR012_2026-11-16.md); ERR-033 in [`03_FACHLICHE_FEHLER.md`](../../../knowledge/research/03_FACHLICHE_FEHLER.md); Probe `SAME_ROOT_SHIFT`
- Prüffrage · Ist `Cmaj7 – D7 – Dm7 – G7 – Cmaj7` in C-Dur richtig als `Imaj7 – V7/V – ii7 – V7 – Imaj7` gedeutet, und passt die neue Benennung?
- Erwartung · D7 = D–F♯–A–C (Tonklassen 2, 6, 9, 0) → Dm7 = D–F–A–C (2, 5, 9, 0). Gemeinsam bleiben 0, 2, 9; F♯ sinkt nach F.
- Spielprobe · Optional: Wirkt der Wechsel im Kontext als Eintrübung der Doppeldominante vor V7?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### A2 · CDR-021 `ACCENT_ON_BEAT_2_IN_2_4`

- Festlegung · Akzent auf Zählzeit 2 gilt nur für den Surdo de primeira (marcação) in der Bateria einer Escola de samba, 2/4. Kein Akzentgebot für alle Surdos oder andere Gattungen.
- Fundstelle · [Entscheidung zu CDR-021](ENTSCHEIDUNG_CDR021_2026-11-16.md): Guimarães 2018 S. 30, Pinto 2001 S. 38, Cunha 2013 S. 3/6
- Prüffrage · Ist die Zwei für den Surdo de primeira in der Bateria tatsächlich dynamisch betont, nicht nur der Ort seines Schlags?
- Erwartung · Ja, als charakteristischer Akzent beschrieben. Eine Lautstärkemessung liegt nicht vor.
- Spielprobe · Gewünscht: Einschätzung aus eigener Bateria-Praxis oder Verweis auf eine Aufnahme.
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### A3 · CDR-021 `SURDO_PULSE`

- Festlegung · Rollenabhängiger Surdo-Puls: primeira auf 2 (im Viertelraster auf 2 und 4), segunda auf 1 (auf 1 und 3). Die Rollen werden getrennt geführt.
- Fundstelle · Probe `SURDO_FLORIANOPOLIS_2010_ROLE_GRID`; Marcelino 2010 Fig. 3–4; Bertazzoli 2023 S. 38–39, Fig. 9
- Prüffrage · Ist die Rollenteilung primeira/segunda für die Bateria allgemein zutreffend oder regional verschieden?
- Erwartung · primeira: Ticks 480 und 1440, segunda: 0 und 960 bei 480 PPQ über zwei 2/4-Takte.
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### A4 · CDR-019 `BOSSA_BATIDA`

- Festlegung · Familie variierter Gitarrenbegleitungen mit Bass- und Akkordschicht, keine einzelne feste Figur. Die drei notierten Batidas aus *O Cruzeiro* (13.04.1960) dienen als Beispiele.
- Fundstelle · [Entscheidungen zu CDR-014 und CDR-019](ENTSCHEIDUNG_CDR014_CDR019_2026-11-16.md); [O Cruzeiro 1960](GMD_KORPUS_ABDECKUNG_PRIMARQUELLEN_2026-11-15.md); Inayatullah 2016
- Prüffrage · Ist „Familie von Begleitungen“ eine sachgerechte Beschreibung, und welche Grundformen sollte STEPS als Übungen aufnehmen?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### A5 · CDR-019 `BRAZILIAN_TAMBORIM_SURDO_SYNTHESIS`

- Festlegung · Zugeschriebene Deutung: Die Gitarrenbegleitung überträgt Tamborim und Surdo auf die Gitarre, so Baden Powell laut Reily 1996 (gedruckt S. 5), mit Verweis auf Cabral. Sie ist keine belegte Entstehungsursache.
- Fundstelle · [Reily-Originaltext](GMD_FUNK_REILY_FORTSETZUNG_2026-11-15.md); [Entscheidungen zu CDR-014 und CDR-019](ENTSCHEIDUNG_CDR014_CDR019_2026-11-16.md)
- Prüffrage · Ist die Formulierung als zugeschriebene Deutung angemessen? Kennen Sie eine Primärquelle, etwa Cabral im Songbook Bd. 2, S. 12, oder ein Interview?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### A6 · CDR-014 `PIANO_MONTUNO_GUAJEO`

- Festlegung · Der Knoten wird durch den STEPS-Entwurf `STEPS_SYNCOPATED_PIANO_DRAFT_01` definiert, ausdrücklich als eigene Übung ohne historischen Anspruch.
- Fundstelle · Probe `NEW_PIANO_DRAFT` in [`GRAPH_AUDIT_PLAN.json`](../../../knowledge/relations/GRAPH_AUDIT_PLAN.json)
- Entwurf · 4 Takte 4/4, je eine Sechzehntel (120 Ticks bei 480 PPQ), Akkordfolge Cm – Fm – G7 – Fm. Je Takt vier Ereignisse auf den Zählzeiten 1, 2+, 3 und 4+:

  | Takt | Akkord | 1 | 2+ | 3 | 4+ |
  | --- | --- | --- | --- | --- | --- |
  | 1 | Cm | C4 | Eb4 | G4 | C5 |
  | 2 | Fm | C4 | F4 | Ab4 | C5 |
  | 3 | G7 | B3 | D4 | F4 | G4 |
  | 4 | Fm | C4 | F4 | Ab4 | C5 |

  Das Clave-Raster des Entwurfs liegt bei den Ticks 480, 960, 1920, 2640, 3360, 4320, 4800, 5760, 6480 und 7200.
- Prüffrage · Ist der Entwurf als einfache synkopierte Klavierübung spielbar und sinnvoll? Steht er zur 2:3-Son-Clave in einem stimmigen Verhältnis, oder teilt er nur das Raster?
- Erwartung · Laut Probe nur ein gemeinsames Raster, kein Stilnachweis.
- Spielprobe · Gewünscht: einmal spielen bzw. anhören, mit Urteil zu Spielbarkeit und Clave-Bezug.
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

---

## Teil B · Zusammenfassungen (am Original-PDF nachgeprüft)

### B1 · Hindemith, Stimmumfänge

- Aussage · Sopran C4–G5, Alt G3–D5, Tenor C3–G4, Bass E2–C4. Angehängte schwarze Notenköpfe reichen bis A3–A5, F3–F5, A4 (Tenor nur nach oben) und D2–D4.
- MIDI · Kern 60–79, 55–74, 48–67, 40–60; erweitert 57–81, 53–77, bis 69, 38–62
- Fundstelle · Hindemith, *Traditional Harmony*, Revised Edition, S. 1 (PDF-S. 8), Notenbeispiel unter „Voices“. Aus dem Notenbild abgelesen.
- Prüffrage · Stimmen die abgelesenen Grenzen? Was bedeuten die schwarzen Notenköpfe (Grenzbereich, Ausnahme)?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### B2 · Hindemith, Kap. XIII

- Aussage · Aus V7 entstehen elf alterierte Formen durch enharmonische Umdeutung der Septime oder der Quinte oder durch Ersatz der Quinte durch den Halbton darüber oder darunter. Nr. 6–8 gelten wegen doppelt übermäßiger oder verminderter Intervalle nicht als regulär. Aufgelöst wird ohne chromatische Verbindung, direkt oder trugschlussartig eine Terz tiefer. Nach dem deutschen und dem französischen Sextakkord ist Nr. 9 die häufigste Form. In solchen Folgen gilt das Ohr als unempfindlich für Quintparallelen.
- Fundstelle · S. 88–90 (PDF-S. 95–97); [Zusammenfassung](../../../research/STEPS_Bibliothek/Zusammenfassungen/IMSLP342443-PMLP552428-hindemithTraditionalHarmonyBook.md)
- Prüffrage · Gibt die Zusammenfassung Hindemiths Systematik richtig wieder?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### B3 · Spencer, Akkordsymbole

- Aussage · Alterationen werden als gleichwertige Paare ohne 7 geschrieben: C−9/C♭9, C+11/C♯11, halbvermindert Cm7−5/Cm7♭5. „+“ vor einer Ziffer bedeutet „erhöht“, allein (C+) übermäßig. Der Basston steht als Bruch oder mit Schrägstrich: C7/E (Umkehrung), Cm7/F (Orgelpunkt).
- Fundstelle · Spencer, *The Practice of Harmony*, 3. Aufl., gedruckt S. 334 (PDF-S. 345)
- Prüffrage · Ist die Wiedergabe vollständig und richtig?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### B4 · Schönberg, Kap. XI „Takt und Harmonie“

- Aussage · Schönberg behält zwei Regeln bei: eine zum Orgelpunkt (im nächsten Kapitel) und eine zum Quartsextakkord. Der kadenzierende Quartsextakkord steht auf der betonten Zählzeit, V7 auf der zweiten, der Schlussakkord auf der ersten. Der durchgehende ist frei, soll vom Schüler aber nicht auf die Eins gesetzt werden. Die Übungen werden in Halben notiert, zwei Akkorde pro Takt.
- Fundstelle · *Theory of Harmony* (Übers. Carter), gedruckt S. 202–206 (PDF-S. 214–218)
- Prüffrage · Stimmt die Wiedergabe?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

### B5 · Palmer/Manus/Lethco, Leitfaden zum 4. Finger

- Aussage · Der 4. Finger kommt meist einmal pro Oktave vor. Kreuztonarten bis vier Kreuze: rechts 4 auf der 7. Stufe, links auf der 2. Stufe. B-Tonarten bis vier B: rechts auf Bb, links auf der 4. Stufe. Fünf schwarze Tasten: rechts auf A♯/Bb, links auf F♯/Gb. F-Dur ist geteilt; für einzelne Tonarten und harmonisch Moll gibt es Ausnahmen.
- Fundstelle · *The Complete Book of Scales, Chords, Arpeggios & Cadences*, S. 16–17 (PDF-S. 18–19)
- Prüffrage · Stimmt die Zusammenfassung mit dem Original und der Klavierpraxis überein?
- Entscheidung · ☐ freigegeben · ☐ Korrektur · ☐ Beleg fehlt
- Name, Datum · 
- Anmerkung · 

---

## Nicht Teil dieses Bogens

- Die übrigen 93 Graphkanten, darunter CDR-010 (`FAIL`); siehe [Graphmatrix](../../../knowledge/relations/GRAPH_AUDIT_MATRIX.csv).
- Die Hör- und Spielproben des Fable-Audits; siehe [Abnahmeproben](STEPS_FABLE_5_2_ABNAHMEPROBEN.md).
- Rechtsfragen. Die Entscheidungen dazu stehen im [Rechteinventar](../../../research/gaps/RECHTEINVENTAR_VOLLTEXTE_2026-11-14.md).

# STEPS – Kanonische Akkordprogressions-Bibliothek (PROG-001 bis PROG-028)

> Diese Fassung dokumentiert den Bestandskatalog der allgemeinen Progressions-API. Die einzeln geprüften Einträge der App-Schnittstelle stehen im [kuratierten Lernmaterial](REVIEWED_PROGRESSIONS.md).

**Dokumenttyp:** KONSOLIDIERTER AKKORDPROGRESSIONS-ATLAS  
**Wissensdomänen:** M05 (Harmonielehre), M04 (Akkordtheorie), M06 (Voice Leading), M09 (Genre-Atlas)  
**Notationsstandard:** SPN (C4 = MIDI 60); deutsches H = int. B explizit.  
**Integritätsstatus:** `GATE 1 (IDENTITY_INTEGRITY): RECOVERED` in Phase 4.14.

---

## 1. Übersicht aller 28 kanonischen Progressions-Archetypen

| ID | Name / Typus | Stufen / Analyse | Beispiel (Standardtonart) | Stilistischer Kontext / Anwendung | Quellen & Belege |
|---|---|---|---|---|---|
| `PROG-001` | Pop Four Chords | `I - V - vi - IV` | `C - G - Am - F` | Pop, Rock, Singer-Songwriter | Piston (1987), Kostka (2013) |
| `PROG-002` | Emotional Minor Loop | `vi - IV - I - V` | `Am - F - C - G` | Pop-Balladen, Melodic EDM | Tagg (2014) |
| `PROG-003` | Jazz Two-Five-One | `ii^7 - V^7 - I^maj7` | `Dm7 - G7 - Cmaj7` | Jazz, Bebop, Neo-Soul | Levine (1995), Nettles (1997) |
| `PROG-004` | 50s Doo-Wop Loop | `I - vi - IV - V` | `C - Am - F - G` | Doo-Wop, R&B, 50s Pop | Aldwell/Schachter (1989) |
| `PROG-005` | Andalusische Kadenz | `i - bVII - bVI - V` | `Am - G - F - E` | Flamenco, Rock, Latin | Gauldin (2004) |
| `PROG-006` | Pachelbel-Sequenz | `I - V - vi - iii - IV - I - IV - V` | `D - A - Bm - F#m - G - D - G - A` | Barock, Klassik, Hochzeitsmusik | Fux (1725), Rameau (1722) |
| `PROG-007` | Dorian Groove Vamp | `i^7 - IV^7` | `Dm7 - G7` | Funk, Fusion, Modaler Jazz | Pease (2003) |
| `PROG-008` | 12-Bar Blues | `Idom7 - IVdom7 - Idom7 - V^7 - IVdom7 - Idom7` | `C7 - F7 - C7 - G7 - F7 - C7` | Traditional Blues, Rock'n'Roll | Rawlins/Bahha (2005) |
| `PROG-009` | Minor Plagal Romance | `I - IV - iv - I` | `C - F - Fm - C` | Romantik, Filmkomposition | de la Motte (1976) |
| `PROG-010` | Secondary Dominant Lift | `I - V^7/vi - vi - IV` | `C - E7 - Am - F` | Gospel, Pop, Soul | Kostka/Payne (2013) |
| `PROG-011` | Modal Interchange Aeolian | `I - bVI - bVII - I` | `C - Ab - Bb - C` | Epic Pop, Rock, Filmmusik | Mulholland (2013) |
| `PROG-012` | Descending Circle of Fifths | `vi - ii - V - I` | `Am - Dm - G - C` | Barock, Jazz, Chanson | Rameau (1722), Salzer (1952) |
| `PROG-013` | Tritone Substitution Cadence | `ii^7 - bII^7 - I^maj7` | `Dm7 - Db7 - Cmaj7` | Modern Jazz, Bebop | Levine (1995) |
| `PROG-014` | Backdoor Resolution (IV) | `IV - bVII^7 - I` | `F - Bb7 - C` | R&B, Pop, Soul | Terefenko (2014) |
| `PROG-015` | Royal Road (Ōdō shinkō) | `IV^maj7 - V^7 - iii^7 - vi` | `Fmaj7 - G7 - Em7 - Am` | J-Pop, Anime, Fusion | Jaffe (1996) |
| `PROG-016` | Coltrane Changes (3-Tonic Cycle) | `I^maj7 - V^7/bVI - bVI^maj7 - V^7/bIV - bIV^maj7` | `Bmaj7 - D7 - Gmaj7 - Bb7 - Ebmaj7` | Modern Jazz Matrix (Großterzteilung in Z12) | Cohn (2012), Tymoczko (2011) |
| `PROG-017` | Classical Jazz Backdoor ii–V | `iv^7 - bVII^7 - I^maj7` | `Fm7 - Bb7 - Cmaj7` | Jazz-Standards (*Lady Bird*, *Yardbird*) | Levine (1995), Terefenko (2014) |
| `PROG-018` | Substitute Backdoor ii–V | `ii^7 - bVII^7 - I^maj7` | `Dm7 - Bb7 - Cmaj7` | Cool Jazz, West Coast | Rawlins/Bahha (2005) |
| `PROG-019` | Minor Line Cliché | `i - i^(maj7) - i^7 - i^6` | `Am - Am(maj7) - Am7 - Am6` | Bossa Nova, Spy Film, Ballade | Levine (1995) |
| `PROG-020` | Extended Tritone Sub (Altered) | `ii^9 - bII^7(#11) - I^maj9` | `Dm9 - Db7(#11) - Cmaj9` | Contemporary Jazz | Levine (1995), Pease (2003) |
| `PROG-021` | Neo-Soul Rootless Minor Cycle | `i^9 - iv^9 - bVI^maj9 - V^7(b9)` | `Dm9 - Gm9 - Bbmaj9 - A7(b9)` | Neo-Soul, R&B, Lo-Fi | Mulholland (2013) |
| `PROG-022` | Picardy Third Resolution | `i - iv - bVII - I` | `Dm - Gm - C - D` | Barock, Renaissance, Folk | Aldwell/Schachter (1989) |
| `PROG-023` | Liquid D&B Sub-Pulse Cadence | `i^7 - bVI^maj7 - bVII - i` | `Fm7 - Dbmaj7 - Eb - Fm` | Drum & Bass, UK Bass | Butterfield (2010) |
| `PROG-024` | Bossa Nova Applied Dominant | `I^maj7 - V^7/V - ii^7 - V^7 - I^maj7` | `Cmaj7 - D7 - Dm7 - G7 - Cmaj7` | Bossa Nova (*Girl from Ipanema*) | Mauleón (1993), Jobim (1962) |
| `PROG-025` | Afro-Cuban Minor Ostinato Vamp | `i - iv - V^7 - iv` | `Cm - Fm - G7 - Fm` | Salsa, Afro-Cuban, Mambo (Montuno) | Mauleón (1993), Peñalosa (2009) |
| `PROG-026` | Secondary Dominant Chromatic Bassline | `I - V7(6/5)/V - ii6 - I6 - V7(4/3) - I` | `G - A7/C# - Am/C - G/B - D7/A - G` | Barock, Klassik, Latin Jazz | Kostka (2013), Aldwell (1989) |
| `PROG-027` | Minor Jazz Blues Submediant Turnaround | `i^7 - iv^7 - i^7 - bVI^maj7 - V^7(#11) - i^7` | `Cm7 - Fm7 - Cm7 - Abmaj7 - G7(#11) - Cm7` | Minor Blues (*Birk's Works*, *Footprints*) | Levine (1995), Terefenko (2014) |
| `PROG-028` | Circle of Fifths Soul Cycle | `i^9 - iv^9 - bVII^9 - III^maj9` | `Em9 - Am9 - D9 - Gmaj9` | Neo-Soul, Jazz-Funk, Contemporary R&B | Mulholland (2013), Levine (1995) |

## Präzisierungen zu Blues, Coltrane-Zyklus und Alterationen

- **PROG-008.** `Idom7` und `IVdom7` fordern in dieser Blues-Vorlage
  Dominantseptakkordqualität mit kleiner Septime. In C sind das C7 und
  F7. Die sechs Akkordpositionen fassen die Harmoniewechsel zusammen.
  Für zwölf vollständige Takte müssen Dauern und Wiederholungen
  gesondert angegeben werden. [Open Music Theory, Blues Harmony, Beispiel 1](https://viva.pressbooks.pub/openmusictheory/chapter/blues-harmony/)
- **PROG-016.** Bmaj7, Gmaj7 und Ebmaj7 sind die drei Dursept-Ziele
  des gewählten Ausschnitts. Relativ zur Schreibweise B ist E♭ der
  abgesenkte vierte Stufengrundton, daher `bIV^maj7` und `V^7/bIV`.
  Der Großterz-Zyklus beschreibt die klingende Beziehung. Die frühere
  Vergleichsvariante `C - Eb7 - Ab - B7 - E - G7 - C` bleibt
  als getrennte Dreiklangsskizze erhalten. [McClimon, Fig. 3.8, Giant Steps](https://files.mcclimon.org/projects/dissertation.pdf)
- **PROG-020 und PROG-027.** Die Beispiele verwenden ausdrücklich
  D♭7(♯11) bzw. G7(♯11). Das sind konkrete Dominantseptakkorde
  mit erhöhter Undezime. Die frühere D♭-Variante mit zusätzlich ♯9
  und die offene G7alt-Angabe bleiben historische Varianten.
  `7(alt)` bezeichnet in Jazzkontexten eine alterierte Dominante.
  Die Kurzform legt weder eine einzige Auswahl von Alterationen noch
  ein konkretes Voicing fest. Der STEPS-Parser verlangt explizite
  unterstützte Alterationen und weist die offene Kurzform ab.
  [Open Music Theory, Altered and Extended Chords](https://viva.pressbooks.pub/openmusictheory/chapter/altered-and-extended-dominant-chords/)

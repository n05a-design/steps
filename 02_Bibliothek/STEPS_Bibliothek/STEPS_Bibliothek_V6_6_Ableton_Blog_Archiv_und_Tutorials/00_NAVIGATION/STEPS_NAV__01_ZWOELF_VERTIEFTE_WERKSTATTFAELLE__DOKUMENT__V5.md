# Zwölf vollständig ausgearbeitete analytische Werkstattfälle – STEPS V5

*Alle musikalischen Beispiele sind selbst konstruierte Lehrbeispiele. Das bedeutet: Der analytische Satz ist diskutierbar und fachreviewpflichtig; es sind keine Transkriptionen konkreter Songs. Die zitierte Literatur liefert methodische Modelle, nicht zwingend diese exakte Akkordfolge.*

## Fall 01: Der scheinbar einfache ii–V–I-Schluss

**Material:** C-Dur, 4/4; `Dm7` Takt 1, `G7` Takt 2, `Cmaj7` Takt 3–4. In Tonhöhen: Dm7 D–F–A–C, G7 G–B–D–F, Cmaj7 C–E–G–B. **Funktionale Lesart:** ii7–V7–Imaj7 (PD–D–T). Eine mögliche Stimmführung führt C→B, F bleibt oder geht E, A→G, D kann gehalten oder zu E geführt werden. **Alternative:** Bei Loop ohne eindeutigen Schluss wäre diese Symbolfolge nur ein harmonisches Segment, nicht automatisch eine formale Kadenz. **Kompositionsversuch:** Gib Cmaj7 vier statt zwei Beats und entferne die metrische Ankunft: verändert sich die wahrgenommene Schlussstärke? **Prüfung:** Parser, korrekte Terz/Septimen, Kadenz nicht ausschließlich aus Akkordsymbolen ausgeben. Quelle zur Differenz von Syntax und Form: [V5-001], [V5-007].

## Fall 02: Sekundärdominante ohne Modulation

**Material:** `C | A7 | Dm | G7 | C` in C-Dur. A7 enthält C#, das als Leitton zu Dm führen kann. **Primäranalyse:** I–V7/ii–ii–V7–I. **Gegenanalyse:** Eine zufällige chromatische Farbe ohne klaren D-Ankunftspunkt wäre schwächer begründet. **Kompositionsversuch:** Ersetze Dm durch Fmaj7; die A7-Funktion wird weniger unmittelbar erfüllt. **Algorithmischer Test:** A7 darf ohne Ziel Dm existieren; `tonicization=true` setzt keine lokale Tonartänderung. DCML unterscheidet diese Ebenen [V5-010].

## Fall 03: Minor-mode leading tone

**Material:** `Am | F | Dm | E7 | Am`. E7 besitzt G#; der Akkord ist eine gängige leittönige Dominante in Moll. **Alternative:** `Am | F | G | Em | Am` kann ohne G# dennoch musikalisch plausibel sein, besonders in pop-/modallastigem Kontext. **Kompositionsversuch:** Vergleiche im Schluss E7→Am mit Em→Am bei identischer Melodie A4. **Prüfung:** Der Engine darf „natürliches Moll“ nicht als ausnahmslose Harmonievorschrift verwenden.

## Fall 04: Dorisch oder ii–V?

**Material:** D-Pedal in der Bassstimme, Begleitung `Dm7–G7–Dm7–G7`, Melodieton B4 als charakteristische große Sexte. **Modale Lesart:** D-Dorisch mit IV7-Farbe. **Konkurrenzlesart:** Mit starker C-Ankunft und fehlendem D-Pedal könnte dieselbe Dm7–G7-Bewegung ii–V in C sein. **Kompositionsversuch:** Erzeuge zwei Hörfassungen, eine mit D-Basspedal und Schluss D, eine mit C-Bassauflösung. **Prüfung:** Modusannotation braucht Tonzentrum und Passage, nicht nur Pitch-Class-Mengen [V5-001].

## Fall 05: Mollsubdominante als Chromatik mit Stimme

**Material:** `Cmaj7 | Fmaj7 | Fm6 | C/E`. A→Ab in derselben Stimme ist eine sinnvolle chromatische Linie, Ab→G löst in den Schlussklang. **Funktionale Lesart:** IV→iv über Mischung aus C-Moll, zurück nach I6. **Stimmführungslesart:** gemeinsame Töne und semitonaler Nachbar. **Kompositionsversuch:** Hebe den Bass F→E deutlich hervor und vergleiche mit `Cmaj7–Abmaj7–C`, das andere Common-Tone-Strukturen enthält. **Prüfung:** Nicht „iv macht traurig“ als mathematischen Claim ablegen.

## Fall 06: Tritonussubstitution im lokalen ii–V–I

**Material:** `Dm7 | Db7 | Cmaj7`; zu vergleichen mit `Dm7 | G7 | Cmaj7`. **Schlüsseltonbezug:** G7 besitzt B/F, Db7 in der üblichen Schreibweise Cb/F (enharmonisch B/F). Dies kann melodische Guide-Tone-Leitungen bewahren, während der Bass einen chromatischen Halbtonzug erhält. **Konflikt:** `Db7` ist nicht in allen Voicings/Skalen/Melodien ein klanglich austauschbares G7. **Kompositionsversuch:** Halte B4 als Melodie über beiden Dominanten; analysiere im Db7 B als Cb und die resultierende Textur. **Prüfung:** Erkennung darf auf Tonklassen- und geschriebenen Tonhöhen zugleich arbeiten.

## Fall 07: Poploop mit konkurrierender Tonika

**Material:** `Am | F | C | G`, viermal wiederholt. **Lesart A:** vi–IV–I–V in C. **Lesart B:** i–VI–III–VII in a-Moll. **Warum keine sofortige Entscheidung?** Wiederholung, Bass, Melodie-Endton, Hook-Einstieg und Form können das Zentrum beeinflussen. **Kompositionsversuch:** Melodie beendet Phrase einmal auf C5 mit C-Akzent, einmal auf A4 über Am; Tempo/Harmonic Rhythm gleich halten. **Prüfung:** `alternative_analyses[]` erlauben und `tonal_center_confidence` nicht ohne Messgrundlage als Zahl ausgeben [V5-005].

## Fall 08: Emergent Tonic als großformale Absicht

**Material:** Verse viermal `Am–F–G–G`, Prechorus `Dm–F–G–G`, Chorus beginnt erstmals deutlich `C–G–Am–F`. **Interpretation:** Tonika C kann im Verse impliziert, aber deutlich erst im Chorus als formaler Zielpunkt hörbar werden. **Alternative:** Wenn die Verse-Melodie A stark etabliert, kann A-Moll ebenso plausibel bleiben. **Kompositionsversuch:** Setze das Chorus-C in verschiedene Register, lasse die Textur am Übergang wachsen. **Prüfung:** `emergent_tonic` als interpretative Kategorie und nicht als deterministisches Akkord-Symbolgesetz. Nobile/Spicer [V5-003], [V5-005].

## Fall 09: Blues I7 ist keine automatische Sekundärdominante

**Material:** `C7 | C7 | C7 | C7 | F7 | F7 | C7 | C7 | G7 | F7 | C7 | G7`. **Blues-Lesart:** I7, IV7, V7 als konventionelle Farb-/Formelemente. **Klassische Fehlanalyse:** `C7 = V7/IV`, und das Werk verbringt vier Takte in „nicht eingelöster“ sekundärer Dominante. **Kompositionsversuch:** Spiele die Basslinie mit Wechselnoten und bluesnaher Melodik; der harmonische Ablauf bleibt gleich, Form/Eindruck wechseln. **Prüfung:** `style_scope=blues` aktiviert andere Harmoniepräferenzen als klassische Satzlehre.

## Fall 10: Neo-riemannsche P/L/R-Nachbarschaft

**Material:** `C major (C–E–G) → C minor (C–Eb–G) → Ab major (Ab–C–Eb)`. Erster Schritt P mit E→Eb, zweiter Schritt erhält C/Eb und verlagert G→Ab. **Interpretation:** Chromatische Nähe nach minimaler Stimme und Common Tones. **Alternative:** Einzelne Akkorde könnten in einer Tonart funktional anders kontextualisiert sein. **Kompositionsversuch:** Setze die drei Klänge als lange Streichertöne und danach als kurzes Rockriff: Transformation bleibt, Form/Wirkung verändert sich. **Prüfung:** nicht ungeprüft auf Septakkorde übertragen [V5-015].

## Fall 11: Satz vs. Periode als Formfrage

**Material:** Acht Takte in C, Grundidee M `C5–D5–E5` im 1.+2. Takt, Wiederholung T3+4, Verkürzung/Sequenzierung T5+6, Schlusskadenz T7+8. **Satzlesart:** Presentation (basic idea + repeat) → continuation (fragmentation, acceleration, cadence). **Alternative Periode:** Ein schwächerer Schluss T4 und motivisch rückbezüglicher Nachsatz T5–8 würden eine andere Organisation begünstigen. **Kompositionsversuch:** gleiche Ton-/Akkordvorräte, unterschiedliche Motivwiederkehr und Cadence-Placement; Hörtest. **Prüfung:** `formal_type` nicht aus der Anzahl `8` allein ableiten. Caplin [V5-002].

## Fall 12: Form und Harmonic Rhythm einer Reharmonisierung

**Material:** Vier starke Melodietöne E4–D4–C4–B3 über vier Takte. Harmonisierung A: `Cmaj7 | G7 | Am7 | G7`. Harmonisierung B: `Am7 | Dm7 | Fmaj7 | G7`. Beide unterstützen die starken Melodietöne als Chord Tone (in B: E=Quinte von Am7; D=Grundton von Dm7; C=Quinte von Fmaj7; B=Terz von G7). **Variation:** Ändere B in `Am7(6 Beats)–Dm7(2 Beats) | Fmaj7 | G7`: die eigentliche Dauerstruktur wird wichtiger als die bloße Liste. **Prüfung:** `melody_fit` braucht Onsets, Durations, Voice und zulässige Extensions, nicht nur `[chord-tone=true]`. Theorie-/Form-Schnittstelle [V5-001], [V5-010].

---

## Einheitlicher Reviewbogen pro Fall

1. Sind `pitch spelling`, Akkordtöne und Stufen korrekt?
2. Sind formale und tonale Behauptungen durch Melodie/Bass/Phrase gestützt?
3. Gibt es eine plausible alternative Deutung oder einen offenen Kontext?
4. Was ändert sich bei Metren-/Dauerverschiebung?
5. Kann Codex ein eigenes Beispiel im gleichen Muster erzeugen und es tatsächlich prüfen?
6. Wurden diese Originalbeispiele nicht fälschlich einer externen Publikation zugeschrieben?

**Freigabe:** Alle zwölf Fälle sind `original_pedagogical_synthesis`, **noch kein unabhängiger Expertenreview**.

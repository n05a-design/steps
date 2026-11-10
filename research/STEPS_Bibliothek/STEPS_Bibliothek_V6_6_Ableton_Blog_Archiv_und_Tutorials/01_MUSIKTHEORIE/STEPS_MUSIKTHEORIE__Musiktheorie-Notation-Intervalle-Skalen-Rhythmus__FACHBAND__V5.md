# Band I — MUSIC THEORY: Klang, Notation, Zeit, Struktur und analytische Grundsysteme

*STEPS Research Library V5 · eigenständige didaktisch-musiktheoretische Synthese · nicht als wörtlicher Auszug aus Fachwerken zu verstehen.*

## Leitfrage

Was muss eine Anwendung wissen, damit die Note `F#`, die Pitch Class 6, ein klingender Grundton, der Leitton in G-Dur und die große Terz von D-Dur zwar aufeinander bezogen, aber **nicht dieselbe Dateninformation** sind? Die Antwort reicht von Physik über Schrift und Tonartenkontext bis zur Zeitstruktur. Für Steps ist eine rein chromatische 12er-Zahlenscheibe als Grundlagenrepräsentation unzureichend.

## 1. Tonhöhe, Schall, Stimmungsmodell und Notennamen

Eine musikalische Tonhöhe kann als physikalische Frequenz, als wahrgenommene Tonhöhe, als diskrete MIDI-Note, als Pitch Class oder als notierter Ton erscheinen. Diese Ebenen sind verschieden. In 12-TET gilt für eine MIDI-Notenzahl `n` relativ zu A4=440 Hz die Standardgleichung `f(n)=440·2^((n−69)/12)`. Für A4 gilt n=69 und f=440 Hz; für A5 n=81 und f=880 Hz. Diese Formel beschreibt eine **konkret gewählte Referenzstimmung**, nicht die Summe aller Musiksysteme.

Die Notennamen `F#4` und `Gb4` sind in 12-TET enharmonisch gleichklangend, aber unterschiedlich geschrieben. Die eine Note kann als Terz eines D-Dur-Akkords, die andere als verminderte Quarte oder als tiefalterierte Stufe eines anderen harmonischen Zusammenhangs vorkommen. Steps muss `pitch_class`, `octave`, `diatonic_letter`, `accidental`, `tuning_reference`, `temperament` und `rendered_locale` **getrennt** halten.

**Deutsches und internationales Tonsystem:** Deutsch `H` bezeichnet den international `B` genannten Ton; deutsch `B` bezeichnet international `Bb`. Das Intervall H–C ist eine kleine Sekunde, B–C eine große Sekunde. Ein Lokalisierungsparameter, nicht eine global veränderte Tonhöhendefinition, muss die Schreibweise bestimmen.

**Überprüfung:** Transponiere `F#–A#–C#` diatonisch um einen Halbton abwärts: eine plausible Tonartfassung lautet `F–A–C` und nicht `E#–G##–B#`, es sei denn, der Kontext verlangt diese enharmonische Schreibweise. Die reine Pitch-Class-Addition produziert ohne Schreibkontext keine eindeutige korrekte Lösung.

## 2. Intervalle: Qualität ist mehr als Abstand

Ein Intervall besitzt diatonische Zählung und chromatische Weite. `C–E` ist große Terz (vier Halbtöne); `C–Fb` ist verminderte Quarte (ebenfalls vier Halbtöne). Das Hören in 12-TET kann keinen Unterschied feststellen; der Notations- und Analyseschlüssel sehr wohl. Noch ein Grenzfall: `B–F` (international B4–F5) ist ein Tritonus als verminderte Quinte, `F–B` eine übermäßige Quarte. Ein Parser darf nicht allein aus Restklassen die Qualität ableiten.

**Kompositorischer Nutzen:** Intervallbeziehungen ermöglichen bewusste Motividentität. Ein Motiv `C4–D4–E4` [2,2] Halbtöne hat anderes diatonisches Profil als ein Motiv `C4–D4–Fb4` [2,2], obwohl in 12-TET dieselben MIDI-Noten erklingen. Eine motivische Inversion muss angeben, ob sie diatonisch, chromatisch, tonal, real oder nur im Tonklassenraum gemeint ist.

## 3. Skalen, Modi und Tonzentren

Eine Skala ist zunächst ein Tonmaterial. Ein *Modus als musikalische Praxis* benötigt aber Zentrum, charakteristische Stufen, Melodiegesten, Kadenz-/Verweilmuster und stilistische Konventionen. `D E F G A B C` allein beweist kein D-Dorisch; die Töne gehören ebenso zum C-Dur-Material. D-Dorisch wird plausibler, wenn D als Ruhepunkt fungiert und die große Sexte B charakteristisch verwendet wird. `Dm–G–Dm` mit D-Pedal kann dorisch wirken; `Dm–G–C` mit deutlicher Tonikaankunft kann schlicht ii–V–I in C sein.

**Prüffall:** `C–Bb–F–C` ist in einem rocktypischen Mixolydisch-Kontext als I–bVII–IV–I plausibel. Ein klassischer Dur-Kontext könnte Bb als modale Mischung erklären. Gleichlautende Akkorde, unterschiedliche Analysetraditionen. Der Kontext gehört in den Datensatz.

### Sieben gebräuchliche diatonische Modi (Intervallschritte relativ zur Tonika)

| Modus | Schritte semitonal | Charakteristische Vergleichsstufen |
|---|---|---|
| Ionisch | 0,2,4,5,7,9,11 | Referenz Dur |
| Dorisch | 0,2,3,5,7,9,10 | kleine Terz, große Sexte |
| Phrygisch | 0,1,3,5,7,8,10 | kleine Sekunde |
| Lydisch | 0,2,4,6,7,9,11 | erhöhte Quarte |
| Mixolydisch | 0,2,4,5,7,9,10 | kleine Septime |
| Äolisch | 0,2,3,5,7,8,10 | natürliche Molltonleiter |
| Lokrisch | 0,1,3,5,6,8,10 | verminderte Quinte, instabiles Zentrum in vielen Tonal-Kontexten |

Die Tabelle ist ein **12-TET-Materialinventar**, keine vollständig definierte Stiltheorie. Die normale Diatonik ist zudem nur einer von vielen Systemtypen. Für Raga oder Maqam reicht solch eine Tabelle explizit nicht; siehe Band V.

## 4. Akkordkonstruktion und symbolische Oberflächen

Ein C-Dur-Dreiklang hat die gestapelten Terzen C–E–G. Für `Cmaj7` kommt B hinzu; für `C7` kommt Bb hinzu; für `Cm7` sind es C–Eb–G–Bb. Das Intervallmuster muss **relativ zum Grundton und zur Schreibweise** geprüft werden. `C7(b9)` enthält im Standardverständnis C–E–G–Bb–Db; der Ton Db ist nicht mit C# zu beschriften, wenn die Funktion der kleinen None gemeint ist.

Weitere häufig vermischte Konzepte: `Csus4` besitzt als Grundmodell C–F–G ohne Terz; `Cadd9` besitzt C–E–G–D ohne Septime; `C9` impliziert gewöhnlich C–E–G–Bb–D. Die in tatsächlichem Voicing ausgelassene Quinte ändert nicht zwingend die abstrakte Akkordidentität. Ein *Slash Chord* `C/E` benennt einen Akkord mit Bass E; ein *Upper Structure* kann hingegen einen eigenständigen Oberakkord über einer Bass-/Dominantstruktur bezeichnen. Gleicher Slash-Text ist nicht für alle Genres dasselbe semantische Modell.

**Codevertrag:** `chord_symbol_raw`, `parsed_root`, `quality`, `extensions`, `alterations`, `omissions`, `bass`, `sounding_notes`, `analytical_chord`, `parser_dialect`, `parse_status`, `provenance` als getrennte Felder.

## 5. Zeit, Takt, Rhythmus, Metrum, Hypermetrum

Takte sind Abstraktionen periodischer Betonung, keine zwingend akkordgleichen Zeitscheiben. In 4/4 kann ein Akkord einen halben Schlag, zwei Beats, eineinhalb Takte oder über mehrere Phrasen dauern. Synkopierte Einsatzzeit ist nicht automatisch metrical dissonance; Kontext entscheidet. In einer 16-taktigen Popform können je vier Takte einen größeren hypermetrischen Zyklus bilden. Ein harmonischer Wechsel auf Beat 4& erzeugt einen anderen Erwartungseffekt als derselbe Wechsel auf Taktanfang.

**Originales Gedankenexperiment:** `Cmaj7` dauert 6 Beats, `Fmaj7` dauert 2, `Dm7` dauert 4 und `G7` dauert 4. In 4/4 ist dies eine vierharmonische Struktur mit übergreifenden Einsätzen. Eine Folge `[Cmaj7,Fmaj7,Dm7,G7]` ohne Dauerinformation kann diese Struktur nicht wiederherstellen.

**Composing-Linse:** Rhythmische Transformationen eines Motivs können die Tonfolge bewahren und dennoch die gesamte Phrase neu gewichten: `1,1,2` → Augmentation `2,2,4`; oder Displacement um eine Achtel. Die Unterteilung der Note in BPM und Tick ist eine Implementierungsentscheidung, die metrical hierarchy nicht ersetzt. Quelle zur Relevanz von Metrik in Rock: [V5-008].

## 6. Form aus Phrasen und Funktionen entwickeln

In klassischer Formtheorie ist die Unterscheidung **presentation → continuation** (Satz/Sentence) gegenüber **antecedent → consequent** (Periode/Period) sinnvoll. Ein acht-taktiger Satz kann aus einer zweitaktigen Grundidee, ihrer Wiederholung und einer viertaktigen Fortsetzung/Kadenz bestehen. Eine achttaktige Periode kann durch einen relativ schwachen Schluss im Vordersatz und einen stärkeren Schluss im Nachsatz charakterisiert sein. Eine Phrase wird **nicht nur durch 4+4 Takte** zur Periode: Ohne motivische Rückbeziehung und Schlussverhältnis bliebe der Formbegriff leer. Als Quelle zum Ansatz siehe [V5-002] (hier nur öffentlich verfügbare Metadaten und Kurzansichten eingesehen).

Der Popsong sollte dennoch nicht automatisch in diese Modelle gepresst werden. Nobile zeigt, dass Verse, Prechorus und Chorus über harmonische Prozesse formal verschieden gebaut sein können. Beim sogenannten telos chorus liegt eine zentrale Ankunft häufig **am Anfang** des Chorus; eine klassisch kadenzorientierte Schlusslogik allein erklärt die Energiedramaturgie nicht. Quelle [V5-003].

## 7. Tonraum und Stimmführung

Eine Akkordfolge ist nicht identisch mit einer Akkordstimmführung. `Cmaj7 → Am7` kann mit gemeinsamen Tönen C, E, G von einem vierstimmigen `C E G B` zu `C E G A` realisiert werden: im einfachsten frei vertauschbaren Voicing wechselt nur B zu A. Ein tatsächliches Instrument kann andere Register, Doublings oder Aufteilungen erzwingen. Minimaler Tonklassenabstand ist nur eine Metrik, keine universelle Musikqualitätsfunktion.

Für vierstimmigen Satz in einem engen klassisch geprägten Stil gelten andere Vorgaben als für Jazz-Pianovoicing oder Synth-Pad. Der Begriff „Stimmführung“ ist als eigenständiges Prüf-/Rankingmodul zu implementieren und mit `style_scope` und `voice_identity` zu versehen. Für die Grenze zwischen normativem Part-Writing und wahrnehmungsbezogener Bewegung siehe [V5-014].

## 8. Tonraum, Transformation und Fortgeschrittenentheorie

Bei neo-riemannschen P/L/R-Transformationen werden Dreiklänge anhand bestimmter minimaler Tonbewegungen verknüpft. Beispielsweise verbindet P `C major` (C–E–G) mit `C minor` (C–Eb–G): zwei gemeinsame Töne, eine Halbtonänderung. R verbindet `C major` mit `A minor`: C und E bleiben, G geht zu A als Ganzton. L verbindet `C major` mit `E minor`: E und G bleiben, C geht zu B als Halbton. **Diese Operatoren gelten für spezifizierte Dur-/Moll-Dreiklänge und Tonklassenmodifikationen**, nicht unbesehen für beliebige komplexe Jazzakkorde. Cohns Werk [V5-015] eröffnet hierfür eine andere Betrachtung chromatischer Nähe als klassische Funktionsharmonik.

Posttonale Set-Class-Theorie abstrahiert stärker von Tonart/Funktion; dies kann für planende Klangfelder, symmetrische Sammlungen und algorithmische Transformationen hilfreich sein. Aber eine identische Pitch-Class-Set-Klasse impliziert nicht dieselbe Hörgestalt, Stimmführung oder Phrase. Auch Zwölftontechnik ist ein möglicher Kompositionsansatz und kein zwingendes Folgestadium tonaler Musik.

## 9. Akustik und psychoakustische Grenze

Die physikalischen Komponenten eines Klanges erzeugen keine einfache deterministische Übersetzung „Intervall → Emotion“. Rauigkeit, Spektralzusammensetzung, zeitliche Hüllkurve, Register, Klangfarbe, musikalische Sozialisation und Erwartung können zusammenwirken. Die psychoakustische Grundlage ist für die Parametrisierung von Klang und Spannung wichtig; Begriffe wie „dunkel“, „traurig“ oder „cinematic“ bleiben an Hörkontext und Nutzerwahrnehmung gebundene Beschreibungen. Vermeide fest kodierte Objektivitätsbehauptungen.

## 10. Analyseperspektiven und Validierung

- **Notationslinse:** Stimmen die Buchstaben/Alterationen und die Oktaven?
- **Pitch-Class-Linse:** Stimmen mathematisch die erklingenden Restklassen?
- **Funktionale Linse:** Ist ein Akkord aus dem formalen Kontext heraus sinnvoll als T/PD/D interpretierbar?
- **Modale Linse:** Ist ein modales Zentrum hörbar/strukturell belegbar?
- **Transformationslinse:** Welche Common Tones und kleinsten Veränderungen bestehen?
- **Stil-/Korpuslinse:** Für welche Aufnahmegruppen und Annotationen gilt ein Frequenzwert?
- **Pädagogische Linse:** Wird für Anfänger sinnvoll vereinfacht, ohne fortgeschrittene Alternativen zu leugnen?

### Abnahmetests des Fachbands

1. `F#` und `Gb` haben in 12-TET gleiche Pitch Class, aber verschiedene `diatonic_letter`/`accidental`.
2. `C7(b9)` ergibt die geschriebene None Db, nicht C#.
3. `Dm–G–Dm` ist nicht automatisch ii–V–ii in C; tonaler Kontext und D-Zentrum sind offen.
4. Bei `Cmaj7` mit Rhythmus 6+2 Beats bleibt der Akkordwechsel zeitlich exakt, nicht ein Takt pro Symbol.
5. Die Kennzeichnung „Periode“ verlangt nicht nur 8 Takte, sondern nachprüfbare musikalische Funktionen.
6. Ein tiefer Quintton oder offener Quintenklang darf nicht als eindeutiger Durakkord klassifiziert werden, wenn die Terz fehlt.

## Quellen und Evidenzstatus

Open Music Theory [V5-001] als öffentliches Lehrwerk, music21 Roman Numerals [V5-026] und DCML [V5-010] als **technische Vergleichsstandards**; Caplin [V5-002], Cohn [V5-015], Huron [V5-014] und Nobile [V5-003] als **Forschungsrichtungen/teilweise Abstracts**, nicht als vollständig gelehrte Bände. Alle Notenbeispiele dieses Fachbands sind unabhängig erstellte didaktische Beispiele, keine abgetippten Lehrbuchnoten.

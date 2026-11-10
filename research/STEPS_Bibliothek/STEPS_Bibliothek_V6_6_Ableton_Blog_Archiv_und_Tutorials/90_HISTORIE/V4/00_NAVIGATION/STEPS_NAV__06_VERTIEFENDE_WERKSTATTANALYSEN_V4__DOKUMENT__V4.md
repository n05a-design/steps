# STEPS V4 – Vertiefende Werkstattanalysen

**Zweck:** Eigene, nachspielbare und kritisch kommentierte Lehrfälle für Music Theory, Harmony, Chord Progressions und Composing. Sie ergänzen das historische V3-Paket und die 30 neuen 16-taktigen MIDI-Miniaturen. Alle Noten-/Akkordskizzen sind eigens für STEPS formulierte Unterrichtsbeispiele, keine Übernahme fremder Songs. **Status:** redaktionelle Theorieanalyse; musikalischer Fachreview und Quellen-Locator-Review stehen aus.

## 1. Von Tonklasse zu Notenname: Warum F♯ und G♭ nicht dieselbe Analyse sind

Eine Tonklasse `6` kann in der gleichstufigen Zwölftonrepräsentation sowohl als F♯ als auch als G♭ auftreten. Für reinen MIDI-Playback ist die Unterscheidung häufig unnötig; für Komposition, Satzlehre und Vermittlung ist sie zentral. Die Frage, ob ein Ton zur Stufe 7 oder als chromatisch erniedrigte Stufe wirkt, ist aus dem MIDI-Wert allein nicht rekonstruierbar. Die gleichstufige Äquivalenz ist daher ein Verlust des Symbolraums, nicht dessen vollständige Darstellung.

**Arbeitsfall:** Schreibe F♯-Dur korrekt als `F♯ G♯ A♯ B C♯ D♯ E♯ F♯`. Eine algorithmische Liste `F♯ G♯ A♯ B C♯ D♯ F F♯` mag im 12-TET die gleichen MIDI-Klassen ergeben, ist aber keine korrekt buchstabierte F♯-Dur-Tonleiter. Gleiches gilt für das Tritonusintervall: `C–F♯` ist eine übermäßige Quarte, `C–G♭` eine verminderte Quinte. Ein Kernobjekt braucht daher `(diatonic_letter, accidental, octave, tuning_id, sounding_pitch)`.

**Test:** Alle zwölf Durtonarten mit geeigneten enharmonischen Varianten ausgeben; Buchstabensequenz, Intervalle und Tonklassen getrennt vergleichen. Negative Fälle: Pitch-Class-Zuordnung korrekt, Buchstabenfolge jedoch doppelt. Für exotischere Tonarten darf das System Doppelvorzeichen nicht automatisch unterschlagen.

## 2. Akkordsymbol versus Funktion: C7 ist nicht immer eine Dominante

C7 bezeichnet im verbreiteten Leadsheet-Dialekt einen Dur-Dreiklang C–E–G mit kleiner Septime B♭. In C-Dur-Satzkontext kann er als `V7/IV` in Richtung F auftreten. In einem C-Blues kann derselbe Tonvorrat ein tonikaler `I7`-Klang sein. Beide Analysen können musikalisch sinnvoll sein, aber sie behaupten Verschiedenes: Einmal ist die Septime in einem lokal gerichteten dominantischen Prozess eingebettet; einmal gehört der Klang zur stilistischen Grundkonvention einer Bluesform.

**Kontrastversuch:** (A) `C – C7 – F – G7 – C` mit chromatischer Zwischendominante und danach klassischer Dominante. (B) Eine Blues-Achttaktminiatur mit `C7 – C7 – F7 – C7 – G7 – F7 – C7 – C7`, in der C7 am Anfang und Schluss den Grundbereich markiert. Ein rein intervallbasierter Parser würde beide Male einen identischen ChordObject liefern; der Analyzer muss getrennte `analysis_candidates` mit `style_scope` erzeugen.

**Test:** Akkordtöne von C7 mechanisch prüfen; zwei funktional verschiedene Kontexte mit gleicher Datenstruktur füttern; keine erzwungene Einzellösung. Fachliche Bewertung des Bluesstils separat durchführen.

## 3. Eine Akkordschleife, zwei Zentren: Am–F–C–G

Die Folge `Am–F–C–G` enthält Töne aus C-Dur beziehungsweise A-Äolisch. Der C-Dur-Analyst kann `vi–IV–I–V` schreiben, der äolische Analyst `i–♭VI–♭III–♭VII`. Keiner der beiden Wege ist allein aus vier Symbols eindeutig bewiesen. Die gehörte Mitte kann von melodischen Zieltönen, längeren Akzenten, Basston-Dauern und dem Abschnitt des Songs abhängen. Mark Richards' Analyse zur Axis-Familie ist ein hilfreicher wissenschaftlicher Bezug, allerdings kein Beleg dafür, dass jede Verwendung der Schleife dieselbe Tonikamehrdeutigkeit besitzt (EXT-V4-019).

**Kompositionsversuch A:** Lege eine Melodie an, die auf C beginnt, C auf stärker betonten Abschlüssen wieder aufgreift und die Schleife über C enden lässt. **Versuch B:** Lege A als längeren Zielton und behandle das Schluss-G als Vorbereitung der Rückkehr nach Am. Die Begleitakkorde können gleich bleiben; die formale Schwerpunktsetzung ändert sich. Danach wiederhole beide Versuche bei identischem Tempo und Instrumentenklang.

**Test:** Die Software speichert zwei gültige Kandidaten `C major` und `A aeolian` mit Begründung. Solange die Melodie nicht eingegeben ist, bleibt das Feld `tonal_center: ambiguous` zulässig. Ein automatischer Confidence-Prozentwert ist nicht begründet.

## 4. Funktionsfolge versus Stimmführung: Dm7–G7–Cmaj7

In C-Dur lässt sich `Dm7–G7–Cmaj7` als `ii7–V7–Imaj7` lesen. Das ist zunächst eine funktionale Kurzbeschreibung. Eine zweite Erklärung benutzt die Stimmen: Ein F kann von der Terz des Dm7 zur Septime des G7 gehalten und anschließend nach E im Cmaj7 geführt werden. Ein C kann von der Septime des Dm7 zum B des G7 fallen und auf B als Septime des Cmaj7 liegen bleiben. Die genaue Stimmzuweisung hängt jedoch von Register und Voicing ab: Stimmen darf man nicht im Nachhinein einfach zwischen Registern teleportieren.

| Harmonie | mögliche inneren Stimmen | Bezug |
|---|---|---|
| Dm7 | F4, C5 | Terz und Septime |
| G7 | F4, B4 | Septime und Terz |
| Cmaj7 | E4, B4 | Terz und Septime |

Wähle zusätzlich jeweils einen Bass D2, G2, C2; vergleiche das Bild aus Quintfall im Bass und Sekundbewegung im Oberregister. Prüfe dann die Alternative `Dm7–D♭7–Cmaj7`. D♭7 enthält D♭–F–A♭–C♭, dessen F und C♭ als Tonklassen F und B eine Guide-Tone-Verwandtschaft zu G7 tragen. Die Substitution verändert Bassweg und harmonische Farbe; sie ist nicht `derselbe Akkord`.

**Test:** Symbolbestand, Stimmregister und tatsächliche Notenbewegungen separat ausgeben; alternative Wege nicht ohne Melodieprüfung gleichwertig nennen.

## 5. Modus als Zentrum, nicht als Diatonikliste: D-Dorisch

D-Dorisch enthält `D E F G A B C`. Weil diese Töne auch in C-Dur vorkommen, kann eine reine Pitch-Class-Klassifizierung keinen Modus nachweisen. Eine dorische Gestaltung betont D als Zentrum und lässt die große Sexte B als charakteristische Tonfärbung erfahrbar werden. Eine Folge `Dm–G–Dm` bietet sich als einfache Vergleichsfolie an; der Dur-IV-Akkord enthält B und unterscheidet sich damit vom Gm-Akkord in D-Äolisch.

**Komposition:** Schreibe über acht Takte einen Bass, der überwiegend D bestätigt; betone B einmal melodisch über G und führe anschließend zurück nach A oder D. Wiederhole das gleiche Klangmaterial mit stärkerem C-Dur-Schluss; überprüfe, ob die Wahrnehmung des Zentrums verschoben wird. Dies ist eine Hörübung, keine wissenschaftliche Garantie für einen bestimmten Hörerfolg.

**Test:** Skalenmaterial mechanisch korrekt; Zentrum per getrenntem `modal_final` speichern; Ausprägung des Zentrums mit menschlichem Hörvergleich prüfen.

## 6. Die Moll-Dominante: Em gegenüber E7 in a-Moll

A-Äolisch enthält G, nicht G♯; die natürliche v-Stufe ist `Em`. In vielen tonalen Mollkontexten wird die siebte Stufe für eine stärkere Leittonwirkung erhöht, sodass `E7` mit G♯ vor `Am` verwendet werden kann. Es handelt sich nicht um zwei verschiedene absolute Wahrheiten über a-Moll, sondern um zwei kontextabhängige melodisch-harmonische Verfahren.

**Vergleich:** (A) `Am–G–F–Em–Am`, stärker modale Farbabfolge. (B) `Am–Dm–E7–Am`, tonale Schlusshinführung. Eine plausible Melodie über der letzten Dominante kann G♯–A als halbtönige Auflösung enthalten. Bei der Analyse muss das System neben `scale_id` eine lokale Änderung der Stufe 7 tragen können.

**Test:** `E7 = E G♯ B D`, `Em = E G B`; `G♯–A` ist ein Halbton. Aus dem bloßen E7-Vorkommen darf noch nicht automatisch eine längerfristige Modulation behauptet werden.

## 7. Zwei Phasen derselben Idee: Satzmodell gegenüber Pop-Sektion

Im Kontext klassisch-tonaler Formtheorie kann ein achtaktiger Satz als Präsentation (T. 1–4), Fortsetzung (T. 5–6) und Kadenz (T. 7–8) beschreibbar sein. Eine Wiederholung der Grundidee in der Präsentation und eine fragmentierende Fortsetzung sind dabei nicht bloß numerische Taktetiketten, sondern bestimmte formale Aufgaben. Für einen Pop-Refrain kann dagegen eine kontinuierlich wiederholte Vier-Akkord-Schleife zusammen mit Melodie, Text, timbraler Steigerung und Groove eine schlüssige Form ergeben. William Caplin und Drew Nobile untersuchen dazu unterschiedliche Repertoires und Modelle (EXT-V4-008 und EXT-V4-009).

**Acht-Takt-Kompositionsbrief:** Takte 1–2 Originalmotiv `C4 D4 E4 G4`, 3–4 rhythmisch ähnliche Wiederkehr, 5–6 Fragment `E4 G4` mit schnellerer Setzung, 7–8 längerer Zielton C5 über G7–C. Bewerte als Redaktionsentwurf, nicht als fertig bewiesene Caplin-Satzstruktur; die tatsächliche Melodie braucht Notenwerte und deutliche Kadenzparameter.

**Alternative:** Nutze dasselbe Tonhöhenmaterial im Pop-Refrain viermal, aber steigere die Oberstimme von G4 zu C5 und die Begleitdichte von Solo zu Ensemble. Die reine Chord-String-Analyse erkennt die Formfunktion nicht. Deshalb sind `section_role` und `observed_form_evidence` getrennt.

## 8. Komposition von der Basslinie aus: C–B–A–G

Eine absteigende Linie kann eine identitätsstiftende kompositorische Entscheidung sein. In C-Dur bietet `C – G/B – Am – C/G` den Bass `C–B–A–G` und behält zugleich bekannte harmonische Bezugspunkte. `G/B` ist hier G-Dur mit B im Bass; `C/G` ist C-Dur über G. Die tatsächliche Klangwirkung hängt davon ab, wie stark Bass, Melodie und metrische Positionen hervortreten.

**Praxis:** Fixiere vier Bassnoten je einen Takt. Entwickle zunächst eine selbstständige Oberstimme E–D–C–G, die nicht jeden Bassschritt verdoppelt. Probiere dann eine Variante mit chromatischem Bass C–B–B♭–A. Sie benötigt zusätzliche harmonische Entscheidungen; die gleiche obere Melodie ist nicht automatisch mit jedem Zwischenbass konsonant.

**Test:** Basslinie als `BassLineEvent` mit Pitch, Beat und Dauer sichern; Slash-Akkord und tatsächliche unterste Note im MIDI separat vergleichen.

## 9. Motivtransformation statt unbegrenzter Neumaterial-Erzeugung

Nimm die viertönige Zelle `C4–D4–E4–G4` mit den Dauern `1, 0.5, 0.5, 2` Viertel. Sie besitzt aufwärts gerichtete Kontur und einen längeren Schlusston. In einer formalen Fortschreibung kann man nur die Tonhöhe transponieren (`D4–E4–F♯4–A4`), den Rhythmus vergrößern (`2,1,1,4`), die Intervallkontur wenden (`C4–B♭3–A♭3–F3`) oder die Tonreihenfolge umkehren (`G4–E4–D4–C4`). Jede Operation bewahrt andere Aspekte der ursprünglichen Idee.

**Werkstatt:** Baue vier Phrasen mit jeweils einer dieser Operationen. Dokumentiere, welche Eigenschaft stabil bleibt und welche wegfällt. Am Ende reduziere auf ein Fragment und lasse den ursprünglichen Rhythmus wiederkehren. Eine bloß mathematische Transformation kann einen schlechten Registerverlauf erzeugen; höre jede Version mit dem geplanten Instrument.

**Test:** Verwendete Transformationsfolge mit `origin_motif_id`, `operation`, `parameters`, `result_events` und `voice_range` speichern. Die Implementierung muss bei rhythmischer Augmentation auch Takt- und Formdauer neu prüfen.

## 10. Eine reale Bluesform ist ein Zeitverlauf, kein Tonvorrat

Ein stark vereinfachtes 12-Takt-Schema in C ist:

| Takt | 1 | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|---|
| Akkord | C7 | C7 | C7 | C7 | F7 | F7 | C7 | C7 | G7 | F7 | C7 | G7 |

Der letzte G7 ist ein Turnaround, der zur nächsten Formrunde zurückführen kann. Die Verwendung dominantseptimischer I-/IV-Klänge ist bluesstilistisch plausibel; die konkrete musikalische Realisation braucht Groove, melodische Bluestons, Instrumentierung, Phrasierung und gegebenenfalls Harmonievarianten. Nicht jeder Blues folgt exakt dieser Abfolge.

**Komposition:** Melodie A in Takten 1–4, Antwort über IV in 5–6, Wiederkehr/Variation in 7–8, Schluss-/Turnaround-Geste in 9–12. Schreibe eine Version mit I7 als bewusst stabilem Tonikaklang und eine zweite mit mehr Zielbewegung vor IV7. Der Gegensatz zeigt, warum ein einzelner Dominant-Tag nicht die ganze Bluesharmonik erklären kann.

## 11. Chromatische Transformationsbeziehungen: P, L und R

Ausgehend vom C-Dur-Dreiklang `C–E–G` führt die Paralleltransformation **P** zu `C–E♭–G` (c-Moll), **L** zu `E–G–B` (e-Moll) und **R** zu `A–C–E` (a-Moll). Diese Beziehungen können als graphische Kanten zwischen Dreiklängen dargestellt werden. Sie arbeiten auf einem besonderen mathematischen Objektmodell und sind nicht ohne zusätzliche Definition auf komplexe alterierte Septakkorde oder mikrotonale Tonvorräte übertragbar (EXT-V4-016, EXT-V4-018).

**Komposition:** Wähle `C–Em–Am–C` und verfolge jeweils gemeinsame Töne sowie maximale Einzelstimmenbewegung. Füge einen chromatischen Akkord hinzu und begründe seine Verbindung über konkrete Töne statt über ein pauschales Emotionsetikett. Halte in den Daten fest, ob eine Beziehung (a) reine Pitch-Class-Transformation, (b) ein Voicing-Vorschlag oder (c) eine kontextuelle Funktionsanalyse ist.

**Test:** Dreiklangtonmengen für P/L/R, gemeinsame Töne und theoretisches Register getrennt validieren. Die korrekte Tonmenge beweist noch nicht die gewählte Stimmenzuordnung.

## 12. Komposition für interaktive Medien: Zustand und Übergang

Ein lineares Filmmusik-Cue kann zu einem festen Zeitpunkt einen Klimax planen. Eine interaktive Spielsituation ändert ihre Dauer, Reihenfolge und Intensität in Abhängigkeit vom Geschehen. Deswegen muss eine adaptive Kompositionsidee zwischen stabilem Material, Zustandsgrenzen und Übergangsverfahren unterscheiden. Stephen Baysted diskutiert nach seinem Cambridge-Kapitel die unterschiedlichen kompositorischen Rahmenbedingungen für Film, TV und Videospiele (EXT-V4-027); das bedeutet nicht, dass hier eine vollständige Game-Audio-Engine spezifiziert wäre.

**Originaler Brief:** Zwei Zustände bei 96 BPM, 4/4: *Exploration* `Am–F` als ruhiger, zweitaktiger harmonischer Zyklus mit langem A-Motiv; *Action* `Am–G–F–E7` mit verkürztem rhythmischem Motiv. Übergang an einer gemeinsamen A-Zielstelle am Taktanfang; beide Zustände behalten den Motivkern A–C–E. Das ist eine Kompositionsstruktur, nicht ein fertig produzierte Tonspur.

**Technischer Vertrag:** `state_id`, `loop_length_beats`, `harmonic_key`, `transition_allowed_at`, `shared_motif_id`, `tempo_policy`, `instrumentation_layers`. Validierung des metrischen Übergangspunkts ist automatisch möglich; die musikalische Naht muss gehört werden.

## 13. Klangdichte, Register und formal wahrnehmbarer Höhepunkt

Die Anzahl unterschiedlicher Akkorde ist kein brauchbares Einzelmaß für dramaturgische Spannung. Dieselbe Folge `Am–F–C–G` kann als leiser Begleitloop im unteren Register erklingen und später durch höhere Melodie, dickere Instrumentierung und kürzere Pausen zum Refrain führen. Diese Form ist hörbar, obwohl die Stufenstruktur unverändert bleibt. Andersherum kann maximale Dichte die Verständlichkeit eines wichtigen Motivs verdecken.

**Dreistufiges Originalexperiment:** (I) Takte 1–4 Solo-Piano, Melodie E4–G4; (II) 5–8 zusätzliche Bassoktave und zweistimmige Zwischenlage; (III) 9–12 höheres Motiv bis C5 und geöffnete Akkordlage; (IV) 13–16 bewusstes Ausdünnen und Rückkehr zum Schluss. Vergleiche die Versionen bei angeglichenem Lautheitseindruck, damit Lauterwerden nicht mit besserer Harmonie verwechselt wird.

**Test:** `tension_profile` darf erklärende Parametereinsichten speichern, aber keine unüberprüfte universelle Emotionszahl. Trenne formales Ziel von tatsächlicher Hörerbewertung.

## 14. Interkulturelle Theoriegrenzen und wissenschaftliche Sorgfalt

Die musikalische Vielfalt ist nicht vollständig durch die westliche Akkordfolge als Grundeinheit erfasst. Rāga-basierte nordindische Musik besitzt charakteristische melodische Bewegungen, Ornamentsprache, Aufführungswissen und zeitliche Konzepte. Eine Rāga nur als Pitch-Class-Set oder einen Maqam ausschließlich als Dur-/Mollmodus zu modellieren, zerstört zentrale Information. Die Herausgeber- und Forschungsliteratur muss daher traditionenspezifisch gelesen und bei Bedarf mit Fachleuten geprüft werden; für einen ersten Steps-Bestand ist ein bewusst begrenzter Metadateneintrag ehrlicher als ein falsches Vollmodell (EXT-V4-028).

**Vorgeschlagener Datentyp:** `theory_system: tradition_specific`, `primary_grammar: melodic`, `cultural_scope`, `performance_context`, `melodic_paths`, `intonation_model`, `oral_transmission_notes`, `authority_status`. Die Analyse kann `not_supported_in_current_engine` zurückgeben, statt auf `I–IV–V` zu raten. Diese bewusste Begrenzung ist fachliche Genauigkeit, keine unzulässige Lücke, die durch Halluzination gefüllt werden soll.

## 15. Provenienz-Matrix für reale wissenschaftliche Weiterarbeit

Ein Datenobjekt `PROG-V4-xxxx` oder `ETUDE-V4-xxx` ist zunächst eine **eigene redaktionelle Illustration**. Es belegt nicht automatisch, dass ein wissenschaftliches Werk dieselbe Folge auf genau einer angegebenen Seite verwendet. Anders als in Quellenkompilationen kann man für das eigene Beispiel korrekt `origin: original_STEPS_illustration` schreiben. Die theoretische *Interpretation* des Beispiels braucht dagegen separat eine nachprüfbare fachliche Referenz mit Edition und genauer Fundstelle oder einen ausdrücklich deklarierten Redaktionsstatus.

| Prüfschritt | Belegart | Freigabebedingung |
|---|---|---|
| Akkordtonklasse | Reproduzierbarer Parser-Test | Schema und erwartete MIDI-Klassen stimmen überein |
| Tonartspezifische Benennung | Notations-/Enharmonik-Test | Buchstabenschreibung stimmt; lokale Tonart bekannt |
| Stufenanalyse | Fachliche Kontextlektüre | Tonzentrum, Stil und Alternativen dokumentiert |
| Forminterpretation | Vollständiges melodisches Zeitmaterial | Phrasen-/Kadenzenachweis, ggf. mehrere Linsen |
| Statistische Häufigkeit | Echte Korpusabfrage | Datensatz, Version, Filter, Zähler und Nenner |
| Lehrtext im öffentlichen Repo | Rechte- und Lizenzprüfung | Keine unzulässige Originalübernahme; Attribution geprüft |
| Produktionsreife | Repo- und Regressionstest | Release-Gates bestanden; eigenständige Reviewer-Entscheidung |

**Didaktisches Ergebnis:** Der Anspruch von STEPS ist nicht eine autoritäre Antwortmaschine, sondern die nachvollziehbare Kombination aus musikalisch nutzbaren Beispielen, erklärenden theoretischen Linsen und offen erkennbaren Unsicherheiten.

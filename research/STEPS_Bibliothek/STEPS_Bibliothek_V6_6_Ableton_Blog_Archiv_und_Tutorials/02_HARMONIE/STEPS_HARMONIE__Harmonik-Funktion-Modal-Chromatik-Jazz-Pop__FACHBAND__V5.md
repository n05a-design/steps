# Band II — HARMONY: mehrdimensionale, kontextabhängige Harmonielehre

*STEPS Research Library V5 · Autorensynthese mit originalen didaktischen Akkordfolgen · sämtliche Funktionsdeutungen sind auf den angegebenen Kontext begrenzt.*

## 1. Harmonik ist nicht gleich die Liste erlaubter Akkorde

Ein Akkord ist als simultane/strukturierte Tonzusammenstellung bestimmbar; Harmonie beschreibt den Zusammenhang solcher Klangereignisse in einer Zeit- und Tonraumorganisation. `C–Fm–C` kann als Mischung der Mollsubdominante in C-Dur betrachtet werden, aber auch als planende kontrastierende Farbe innerhalb eines loop-orientierten Popkontexts. Keine dieser Lesarten folgt rein algorithmisch aus drei isolierten Akkordnamen. Nötig sind Tonika-/Modusannahme, Bass, Melodie, Register, rhythmischer Schwerpunkt, Phrasierung und Stil.

**Pflichtfelder für jede Analyse:** `global_key`, `local_key`, `modal_center`, `style_lens`, `chord_spelling`, `bass_line`, `melody_evidence`, `function_claims[]`, `alternative_analyses[]`, `uncertainty_reason`, `source_evidence[]`.

## 2. Funktionale Harmonik und harmonische Syntax

Im allgemeinen Unterrichtsmodell klassisch-tonaler Musik unterscheiden sich tonikaler Bereich, prädominanter Bereich und Dominantbereich. Das ist kein Verbot anderer Übergänge. In C-Dur kann `C–Am–Dm–G7–C` näherungsweise als I–vi–ii–V7–I analysiert werden; vi kann tonikalen Bereich verlängern, ii den Dominantbereich vorbereiten, V7 zur Tonika leiten. In einem vier-taktigen poptypischen Loop ohne Schlusskadenz dürfen dieselben Symbole **nicht automatisch** dieselbe Hierarchie erhalten.

Als differenziertes Beispiel: `F/A–G7/B–C` besitzt Bass A–B–C, während `F–G7–C` Bass F–G–C hat. Beide sind funktional ähnlich, aber haben andere Bassspannung, Inversion und Bewegungsqualität. Das „richtige“ Bassmodell hängt vom kompositorischen Ziel ab.

### Kadenzbegriff und Nicht-Kadenz

`G7 → C` kann Dominantauflösung sein. Eine **authentische Kadenz** im eng gefassten Klassikbegriff ist aber ein formales Schlussereignis mit Lage, Stimmführung, Schlussmoment und Phrasengrenze. In endlos wiederholtem `C–G7–C–G7` ist V–I nicht bei jedem Vorkommen eine selbständige Schlusskadenz. Ebenso bedeutet `F → C` nicht in jedem Stil eine klassisch geprägte Plagalkadenz. Temperleys empirische Arbeit zu Rock-Kadenzen legt gerade die Genre-/Form-Kontext-Frage offen [V5-007].

## 3. Sekundärdominante, Zielharmonie und Tonicization

In C-Dur gehört A7 (A–C#–E–G) nicht zur reinen Durdiatonik. Vor Dm wirkt A7 als `V7/ii` und baut mit C# den Leitton zur Zieltonika D auf: `C–A7–Dm–G7–C`. Ein späteres `A7` ohne Dm-Ankunft kann ebenfalls eine sekundärdominantische Intention tragen, deren Auflösung verzögert, umgelenkt oder verweigert wird. Ein Generator darf die Auflösung weder zum obligatorischen nächsten Schritt noch zu einer statistischen Gewissheit deklarieren.

**Tonicization vs. Modulation:** `C–E7–Am–Dm–G7–C` tonikalisiert A-Moll kurz; eine echte Modulation nach A-Moll braucht längeren kontextuellen Nachweis, z.B. neue Kadenzen, formale Stabilisierung oder stärkere lokale Melodiebestätigung. Der Wert `local_key` muss deshalb unabhängig vom einmaligen V/vi-Ereignis annotierbar bleiben. Die DCML-Spezifikation differenziert `/V`-Tonicization gegenüber lokalen Tonartwechseln [V5-010].

## 4. Moll ist kein bloßer Rechenmodus von Dur

A-Moll kann je nach Satzverlauf die Töne G/G#, F/F# enthalten. `Am–Dm–E7–Am` nutzt E7 mit G# als leittönigem Dominantakkord in A-Moll. `Am–G–F–E7` kombiniert Aeolisch anmutendes Material mit der aus harmonisch-Moll-Praxis bekannten Dominantfunktion. Eine Scala-Klasse `A natural minor` allein deckt nicht alle Tonvorräte einer realen Mollkomposition ab. Im Datenmodell gehören `key`, `local_scale_selection` und `contextual_alterations` zu verschiedenen Ebenen.

**Gegenfall:** `Am–G–F–Em` kann mit natürlichem G im modalen/Popkontext sinnvoll sein; den Em-Akkord pauschal als „falsch“ zu kennzeichnen wäre ein klassischer Analysefehler.

## 5. Modalität und Zentralton

`Dm7–G7` ist für sich genommen mehrdeutig: ii–V in C, aber auch ein dorisch/zentrisches Spiel um D mit G als IV7-Klang. Wird D als Pedal und Ruhepunkt etabliert und die große Sexte B melodisch betont, ist D-Dorisch plausibler. Für einen echten Phrygisch-Kontext kann `Em–F–Em` mit F als bII einen starken Farbkontrast erzeugen; ohne Kontext könnte es auch andere Deutungen zulassen.

Ein modaler Generator benötigt also `modal_center`, `characteristic_pitch_behavior`, `stable_chords`, `cadential_behavior` und `forbidden_claims` („nicht allein aus vorhandenen Tonklassen auf Modus schließen“).

## 6. Mixture, Borrowing und Mollsubdominante

Beispiel: `Cmaj7–Fmaj7–Fm6–C/E` in C-Dur. Der Übergang Fmaj7→Fm6 lässt A zu Ab absinken, während F und C erhalten bleiben können. Die Fm-Farbe kann als parallelmollentlehnter iv-Bereich begründet werden; der C/E-Abschluss ermöglicht im Bass F–E eine Halbtonauflösung. Formal ist dies eine **an bestimmte Dur-/Moll-Begriffe gebundene Analyse**, keine universelle Emotionsmetrik. Ein Algorithmus muss zunächst korrekte Note Spelling, Voicings und Tonika bestimmen.

**Grenzfall:** `C–Ab–Bb–C` ist in Pop/Rock je nach Melodie und metrischer Struktur eine bVI–bVII–I-Turnaroundfarbe. Ein strenger klassischer T–PD–D-Test ist kein sinnvoller alleiniger Evaluator.

## 7. Tritonussubstitution und Chromatik im Jazz

In C können `Dm7–G7–Cmaj7` und `Dm7–Db7–Cmaj7` auf denselben tonikalen Zielklang führen. `G7` enthält die Guide Tones B/F; `Db7` enthält Cb/F, enharmonisch B/F. Die gemeinsamen Guide-Tone-Pitch-Classes tragen die Substitutionsidee, während Bass G→C gegenüber Db→C ein anderer Bewegungsplan ist. Die Gleichsetzung gilt nicht ohne weitergehenden Kontext: Alterationsmöglichkeiten, Klangschreibung und Melodiepassung unterscheiden sich.

Andere Jazzpraktiken: Backdoor `Fm7–Bb7–Cmaj7` kann in C durch bVII7-Ankunft geprägt sein; ein `Cmaj7(#11)` verlangt neben C–E–G–B ein F#, nicht Gb. Jazz-„Funktionsersatz“ ist eine Option, deren Voice Leading und melodische Verträglichkeit **konkret zu testen** sind.

## 8. Chromatische Medianten und neo-riemannsche Nachbarschaft

`C major → E major` (C–E–G → E–G#–B) gehört zu chromatischen Terzbeziehungen; gemeinsame Tonhöhe E, zwei veränderte Stimmen. Ein funktionaler V-I-Reflex erklärt diesen Effekt in der Regel schlechter als eine Studie von Stimmführung, Register und lokalen Tonzentren. Hingegen führt `C major → Ab major` (C–E–G → Ab–C–Eb) eine andere chromatische Bewegungslandschaft vor. Cohns *Audacious Euphony* [V5-015] wird hier als weiter zu vertiefender Forschungsrahmen genannt; das Buch wurde für V5 nicht vollständig gelesen.

Für regelbasierte Tools ist wichtig: Neo-Riemannsche P/L/R-Transformationen modellieren vorzugsweise Dur-/Moll-Dreiklänge. Der Versuch, P auf einen beliebigen `C7alt` anzuwenden, ist ohne zusätzliche Definition formal unbestimmt.

## 9. Vorhalts- und Stimmführungsmodelle

Ein 4–3-Vorhalt über G-Dur kann die Note C zu B führen, während G und D gehalten werden: C (als Vorhalt) → B (Terz). Die zeitliche Vorbereitung und Auflösung sind wesentlich; der bloße Akkord-Snapshot `Gsus4→G` verschweigt Stimme, Register und metrisches Gewicht. Kontrapunktische Regeln sind stilbezogene Handwerkskonventionen, keine Naturgesetze.

Beim Satz in vier Stimmen wird sich die Behandlung paralleler reiner Quinten/Oktaven unter Umständen stark von Guitar Power-Chords unterscheiden. Ein algorithmischer Prüfer muss `strict_common_practice` als expliziten Prüfmodus verwenden, statt jedes Gitarrenriff als Satzfehler zu markieren.

## 10. Pop/Rock: Loop, Tonika und Harmonic-Form

`Am–F–C–G` könnte in A-Moll als i–VI–III–VII wirken; in C-Dur lässt sich vi–IV–I–V lesen. Ohne Melodie, Bassspannung, Phrasierung und Produktionskontext ist die „wahre“ Tonart nicht eindeutig. Spicer zeigt mit fragile, emergent und absent tonics, dass Popmusik sogar gezielt tonikale Stabilität verweigern kann [V5-005]. Nobile zeigt, dass Pop-/Rockabschnitte nicht sinnvoll allein durch gleichförmige 8-Takt-Blöcke beschrieben werden; der harmonische Verlauf und Formfunktion stehen in Wechselwirkung [V5-003].

**Gegenbeispiel:** Wenn ein Chorus auf einer Tonika beginnt und sie lange verlängert, darf eine „Kadenz muss am Chorus-Ende sein“-Engine nicht zu Unrecht einen fehlenden V–I-Abschluss melden. Ein Synthesizer-Pedal kann den harmonischen Zielpunkt bereits am Beginn etablieren.

## 11. Blues: Dominant-Seventh als Grundfarbe

Ein I7-Akkord in einem Blues in C (`C7`) ist häufig **tonikal**, obwohl er nach klassischer Durharmonik eher einen Drang Richtung F als V7/IV nahelegen könnte. Im zwölf-taktigen Blues `C7 | C7 | C7 | C7 | F7 | F7 | C7 | C7 | G7 | F7 | C7 | G7` sind I7 und IV7 genretypisch. Ein klassischer Validator, der die b7 von I als „fremd“ abwertet, würde die Syntax des Blues verkennen. Die Form ist ein **Lehrmuster**, kein universeller Standard für jeden Bluesstil.

## 12. Soul/Gospel/Neo-Soul/R&B als eigenständige Stimmführungswelten

Nicht jeder Gospel- oder Neo-Soul-Klang lässt sich durch eine Akkordlabel-Liste treffend beschreiben. Typisch interessante Aspekte können sein: weiche Binnenstimmbewegung, Upper Structures, Basspedale, chromatische Approaches, Slash-Bass und gesungene melodische Phrasen. Beispiel: `Cmaj9–E7(b9)–Am9–Dm9–G13`; ein möglicher innerer Bewegungsplan nutzt B→Bb→A im oberen Register. Das Beispiel ist eine **selbst konstruierte Lehrstudie**, keine dokumentierte Häufigkeitsbehauptung über eine Stilgemeinschaft.

Für echtes Stilkorpusreview wären notierte/aufgenommene Beispiele mit Kontext notwendig; die Quelle ist nicht automatisch „Genre“.

## 13. Funktion kontra Statistik kontra Wahrnehmung

Ein T–PD–D–T-Modell ist eine **theoretische Analysetradition**, keine Häufigkeitsprognose. Eine Korpusstatistik für `IV→I` ist eine beobachtete relative Häufigkeit unter Korpuswahl, Harmoniesegmentierung und Annotatorenentscheidungen. Eine Tonraumdistanz nach Lerdahl ist ein formales Modell der angenommenen tonalen Organisation [V5-016], nicht direkt ein objektiver Wert für „gute“ Akkorde. In einer Empfehlungslogik müssen diese Signale getrennt ausgewiesen werden.

### Formaler Kandidatenscore (Vorschlag, nicht bereits als Kalibrierung bestätigt)

`score = w_f*functional + w_v*voiceleading + w_m*melody + w_c*corpus + w_r*rhythm + w_u*user_goal`

Dabei muss jedes Teilmodell seinen `scope`, `evidence_level`, `normalization` und seine *Kalibrierungsmethode* offenlegen. Ohne echte Validierung dürfen keine Beispielwerte wie `0.87` als wissenschaftliche Sicherheit verkauft werden.

## 14. Vergleichsmatrix: gleiche Töne, konkurrierende Erklärungen

| Klangfolge | Leseart A | Leseart B | Welche Evidenz entscheidet? |
|---|---|---|---|
| C–Am–Dm–G7 | funktionales I–vi–ii–V7 | harmonisch offener vierteiliger Loop | Phrase, Bass, Tempo, kadenzielle Ankunft |
| Dm7–G7 | ii–V in C | D-Dorisch mit IV7 als Farbakkord | Zentralton, Melodie B, Pedal D |
| C–Bb–F–C | Mixolydisches I–bVII–IV–I | Dur mit bVII-Mischung | Tonzentrum, charakteristischer Melodiegestus |
| G7–C | dominantische Auflösung | wiederholtes Turnaround-Element ohne Abschluss | formaler Schluss, Rhythmus, Wiederholung |
| C–Fm–C | iv aus C-Moll | chromatische Farb-/Stimmführungsbewegung | historische/stilistische Praxis, Stimme A→Ab→G |
| C–E–Am | III chromatisch vor vi | V/vi → vi | Akkordqualität E oder E7, G#→A, Satzfunktion |

## 15. Testideen und wissenschaftliche Grenzen

- Für jede Tonart C, F#, Gb: Spelling, Scale Degree und Akkordzerlegung getrennt prüfen.
- Für `A7→Dm` zwischen *klare angewandte Dominante* und *kein eindeutiger Tonartwechsel* unterscheiden.
- Für Jazz `Dm7→Db7→Cmaj7` die Gleichheit der Guide-Tone-Pitch-Classes sowie die melodische Nichtgleichwertigkeit bestimmter Voicings zeigen.
- Für Blues `C7` innerhalb der Tonika nicht automatisch als sekundäre Dominante ausgeben.
- Für `Am–F–C–G` wenigstens zwei plausible Key-Analysen zulassen.
- Für `C–Ab–C` keine unbedingte Universalregel „bVI hat immer dieselbe Funktion“.

## Forschungsanker

[V5-001] Open Music Theory (Grundlagen und historische Satzmodelle); [V5-003] Nobile (Rockform – Verlagsabstract), [V5-005] Spicer (Poptonalität – Artikel), [V5-007] Temperley (Rockkadenzen – Artikel), [V5-010] DCML (digitale Harmonieannotierung), [V5-014] Huron (Stimmführungspräferenzen – Abstract), [V5-015] Cohn (Chromatik – Verlagsabstract). Der Status der einzelnen Quellen ist im JSON-Register zu unterscheiden.

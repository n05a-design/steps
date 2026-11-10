# STEPS V5 — interdisziplinäre Forschungssynthese und Entwicklungsorientierung

**Status:** research-draft, keine abgeschlossene Peer-Review-Begutachtung. Die Fachbände vertiefen die Forschung, die Tabellen und Studien sind eigene Arbeitsmaterialien. Die 27 neuen Quellenverzeichniseinträge haben in `06_Quellen_und_Rechte` explizite Nachweisstatus.

## A. Von harmonischen Bausteinen zu musikalischen Ereignissen

Eine Akkordprogression ist nur dann fachlich nutzbar, wenn die Tonartbeziehung, Akkordsymbole, lokale Harmoniefunktion, Bass, zeitliche Länge, Melodie und mögliche Wiederholungs-/Formgrenzen gemeinsam beschrieben werden. Ein String wie `C – Am – F – G` kann mehrere harmonische Funktionen erfüllen, abhängig von seinem strukturellen Zentrum, seiner Phrasierung und stilistischen Praxis. Die Benutzeroberfläche muss daher Unterschiede zwischen harmonischem **Bestand**, funktionaler **Deutung**, empirischer **Häufigkeit** und kompositorischer **Option** darstellen.

Die V5-Daten modellieren Lehrfälle mit harmonischen Varianten und eigenen timierten Progressionsobjekten. Musikfachlich komplexe Entscheidungen werden nicht durch einen Algorithmus ersetzt. Transponierte Varianten werden explizit mit `derived_from` verknüpft; diese sind für Parser- und Darstellungstests nützlich, aber keine unabhängigen Forschungsbefunde.

## B. Music Theory als formale und historische Kontextschicht

Für Tonhöhen sind drei verschiedene Repräsentationen wesentlich: Frequenz, Pitch Class und notierte Tonstufe samt Akzidentien. Fis/Ges sind im 12-TET identische Tonklassen, aber nicht beliebige Ersetzungen in Funktionsharmonik, enharmonischer Modulation, Intervallbezeichnung oder Vorzeichenlogik. Die deutsche Schreibung `H` (B natural) / `B` (B flat) muss sichtbar von internationalem `B`/`Bb` getrennt werden. Der Parser muss ausdrücklich entscheiden, welcher Symbolkontext gilt.

Fachtheoretisch müssen Skaleninventare mit tonalem **Zentrum** getrennt bleiben: Die weißen Tasten ergeben nicht automatisch C-Dur, nur weil genau diese Tonklassen vorkommen. Für modale, nichttonale und traditionsspezifische Kontexte ist eine alternative Center- und Melodie-Phrasen-Repräsentation erforderlich.

## C. Harmony als pluralistische und begründete Analyse

Klassisch-funktionale Harmonik, Jazz-Chord-Scale-Modelle, Pop-/Rock-Loops, Blues-Tonikalität und neo-Riemannsche Transformationen sind verschiedene Lenses. Eine Zwischendominante deutet ein temporäres Ziel an, erzwingt aber weder die tatsächlich eintretende Auflösung noch eine dauerhafte Modulation. Der Mixolydisch-/Blues-Kontext kann dominantische Akkordqualitäten auf der Tonika enthalten, ohne ein klassisches V7→I-Modell vorauszusetzen.

Musiktheoretische Methoden zur Form erklären weitere Unterschiede: William Caplin behandelt präzise klassische Formfunktionen und die Möglichkeit mehrerer sinnvoller Zuordnungen; Drew Nobile zeigt in *Form as Harmony in Rock Music*, dass Rock-/Popform nicht lediglich eine Textetikettenfolge aus Vers/Chorus ist, sondern auch in ihrer harmonischen Struktur untersucht werden kann. Diese Ansätze dürfen nicht zu einem universellen Satz-/Periodenalgorithmus verkürzt werden. [V5-002] und [V5-003] sind Forschungsanker; konkrete Kapitelbehauptungen benötigen den jeweiligen Nachweis im Quellenregister.

Ein besonders wichtiger Pop-Befund aus Mark Spicers Forschung sind fragile, emergent und absent tonics. Ein Analysemodell muss daher auch unsichere oder fehlende Tonika zulassen statt eine nicht existente Schlussauflösung zu erfinden. Ein Progessionsgenerator kann wiederum harmonische Mehrdeutigkeit absichtlich als kreatives Mittel wählen. Quelle [V5-005].

## D. Composing ist eine eigenständige fachliche Disziplin

Komposition umfasst die Konzeption, das Herstellen, Ausarbeiten und Revidieren musikalischer Strukturen. Dazu gehören Motiv, Melodiekontur, rhythmische Zellen, Sequenz, Umkehrung, Augmentation, Diminution, Fragmentierung, Phrase, Form, Kontrapunkt, instrumentaler Satz, Register, orchestrale Farbe, Dramaturgie und stilistischer Kontext. Ein Akkordgenerator liefert höchstens einen Teil dieser Entscheidungen.

**Ein überprüfbarer Composing-Workflow** verläuft beispielsweise als `brief → motivic seed → rhythmic profile → melody → harmonic hypotheses → bass motion → form sections → voice leading → register/orchestration → revision → explanation/tests`. Die Reihenfolge ist keine universelle Norm; man kann genauso von einem Bassostinato, einer Melodie, einer Textzeile oder einer Klangfarbe aus beginnen. Steps soll diese alternativen Wege abbilden statt eine einzige Kompositionsmethode vorzuschreiben.

**Beispiel aus einem eigenen Studienentwurf:** Motive `C5(1)–D5(1)–E5(2)` und eine Antwortfigur können durch Verlagerung des Anfangstons, Repetition, metrische Verschiebung und rhythmische Fragmentierung verändert werden. Die Harmonik kann zunächst `Cmaj7 | Am7 | Fmaj7 | G7` tragen; zum Schluss kann eine echte Kadenz entstehen oder bewusst offen bleiben. Entscheidend ist eine nachvollziehbare Entscheidung: Wurde das Motiv verändert, um Tonalität, Dichte, Register oder formale Funktion zu beeinflussen? Ein Urteil allein anhand der Akkordrömer wäre unvollständig.

Die 16 maschinenlesbaren neuen 32-Takt-Studien demonstrieren die Datenpipeline (Noten, Stimmen, Takt, Akkord, Form, Export). Sie sind **nicht** als von erfahrenen Komponisten freigegebene, stilistisch ideale Werke einzuordnen. Mehrere sollen gezielt auf tatsächliche Stimmführungsprobleme, motivische Unschärfen und instrumentale Grenzen geprüft werden.

## E. Empirische Modelle, Korpora und Statistik

Die V5-Quellen [V5-010]–[V5-013] bilden einen starken Ausgangspunkt für strukturierte Harmonieannotation, Standards und Code-Tests. DCML erlaubt reichhaltigere Annotationen als einfache Akkordfolgeketten. ChoCo führt heterogene Corpora zusammen und schafft den Zugang zu großer Datenbreite, aber **Dataset-Lizenzen, Annotationen und zugrundeliegende musikalische Werke sind getrennte Rechteobjekte**. `music21` ist eine potenzielle Referenzimplementierung, kein Nachweis, dass sein gesamter Corpus frei redistribuierbar ist.

Statistische Rankings müssen ihre Bezugsmenge offenlegen: `Quelle, Stil, Epoche, Sample, Labelset, N, Auswertungs-/Glättungsmethode`. Ein mögliches Ranking ist hilfreich, aber die Häufigkeit einer Akkordfolge in einer Stichprobe beweist weder ihre Richtigkeit noch ihre künstlerische Überlegenheit. ML und große Datensatzimporte bleiben nachgelagert.

## F. Kulturen und Forschungsgrenzen

Maqam- und Raga-Praktiken lassen sich nicht durch Überschreiben eines westlichen Akkordschemas mit alternativen Skalentönen fachlich korrekt beschreiben. Melodieführung, charakteristische Bewegungsfiguren, Ornamentation, kultureller Kontext, Form und traditionelle Lehrpraktiken können entscheidend sein. Hier wird die Grenze einer universellen westlichen Harmony-App ausdrücklich dokumentiert. Traditionsspezifische Gegenstände gehören zunächst in eine fachliche Forschungs- und Risikoübersicht und erfordern externe Expertise. V5-020 bis V5-023 sind dafür Einstiegspunkte, keine umfassende Begutachtung jeder Tradition.

## G. Datenmodell und fachliche Abnahme

Ein verifizierbarer Wissenseintrag braucht einen dauerhaften `source_id`, die überprüfte Belegstelle, Claim-Status, theoretischen Geltungsbereich, Beispiele, Gegenbeispiele und eine anwendungsbezogene Frage. **Quellenstatus sind nicht austauschbar:** eine akademische Webseite mit einem Abstract ist kein voller Text; ein gelesener Standardabschnitt ist kein Review sämtlicher Ausgaben und Testimplikationen.

Die ausführbare mechanische Prüfung umfasst Schema-/Datenrelationen, Taktlängen und Ereignislogik, MIDI- und MusicXML-Strukturen. Künstlerische Qualität, stimmführungsspezifische Angemessenheit und Interpretation erfordern darüber hinaus echte menschliche Fachprüfung. V5 hält beide Klassen explizit getrennt.

## H. Übergabe an Codex

Die konkrete Umsetzung ist in `07_Codex/CODEX_MASTER_EXECUTION_V5.md` in 35 Arbeitspaketen festgelegt. Die wissenschaftliche Grundlage ist eine **kuratierte Arbeitsdatenbank**, nicht die Behauptung eines endgültigen Konsenses. Codex muss erst das reale Steps-Repository prüfen, danach Quellen und Regeln validieren, Daten migrieren, Schema und Tests entwickeln und nur überprüfte Inhalte als kanonische Referenz freigeben. Produktcode, Merge, Vertriebslizenzen oder Rohbuchimporte folgen nicht automatisch aus diesem Paket.

## I. Forschungsprioritäten für die nächste Revision

P0: Claim-Locator, Exemplar-Review, Pitch-/Intervall-/Mode-Tests, Repository-Baseline, Lizenz. P1: Composing-Fachreview, echte Notensätze/Gehörprüfung, Stilanalysen und konkurrierende Theorien. P2: eigenständige corpusbasierte Validierung, erweiterte Literatur und Auswahl musikhistorischer Repertoires. P3: experimentelle UI/Skill-Integration, Nutzertests und musikalische Langzeitbewertung. Als deferred bleiben Drum-Engine und riesige, unkontrollierte Corpus-Downloads.

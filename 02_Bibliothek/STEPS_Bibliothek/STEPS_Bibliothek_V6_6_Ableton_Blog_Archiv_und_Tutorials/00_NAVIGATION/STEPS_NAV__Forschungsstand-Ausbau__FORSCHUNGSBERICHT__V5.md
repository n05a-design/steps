# STEPS – Forschungsstand V5: von der Sammelbibliothek zur überprüfbaren musikalischen Wissensinfrastruktur

**Stand:** 2026-11-08 · **Version:** 5.0.0-research-draft · **Gegenstand:** Musiktheorie, Harmonik, Akkordprogressionen, Komposition und die Schnittstellen zu Wahrnehmung, Interaktion, Notation und Datenwissenschaft.

## 1. Warum eine weitere Version nötig ist

Die V4 enthält zahlreiche Begriffe, Progressionsfälle, kurze Studien und MIDI-Etüden. Ihr größtes Defizit ist **nicht bloß die Zahl der Einträge**, sondern die bislang fehlende wissenschaftliche Rückführbarkeit auf konkrete, zugängliche Passagen der Forschung, der Unterschied zwischen algorithmisch erzeugten Varianten und unabhängig überprüften musikalischen Modellen sowie die nicht hinreichend ausgearbeitete Kette von **musikalischer Idee → kompositorische Entscheidung → Analyse → Alternativanalyse → Validierung → Softwarefunktion**.

Die V5 verschiebt die Zielgröße deshalb: Ein Theorieobjekt ist erst fachlich hilfreich, wenn seine Bedingungen, Ausnahmen und ein originales Hör-/Notationsbeispiel erkennbar sind. Eine Akkordfolge ist nicht mit der pauschalen Erklärung „funktional“ hinreichend analysiert. Eine Kompositionsetüde ist nicht durch MIDI-Parsebarkeit kompositorisch gültig. Und eine Quelle ist erst dann Claim-Evidenz, wenn der konkrete Beleg tatsächlich gelesen und lokalisiert ist.

## 2. Vier Säulen und ihre Wechselwirkungen

1. **Music Theory** beschreibt musikalische Repräsentationen und Beziehungen; aus einer Pitch-Class-Menge allein folgt keine korrekte Vorzeichnung, Notation oder analytische Interpretation.
2. **Harmony** erklärt Akkordbeziehungen unter einem expliziten Analysemodell und in einer historischen/stilistischen Praxis. Der Dominantbegriff in Common-Practice, Jazz, Blues und Pop steht nicht für dieselbe Syntax.
3. **Chord Progressions** verbindet Harmonik mit Zeit, Bass, Melodie, Phrasierung, Form und Stil. Akkordfolgen sind Ereignisse in einer kompositorischen Struktur, keine frei schwebenden String-Arrays.
4. **Composing** ist eine gleichwertige eigenständige Arbeitsebene: Ideenfindung, Auswahl, Motivik, Themenbau, Variation, Stimmen-/Registerplanung, Form, Dramaturgie, Arrangement, Umsetzung und Revision.

**Kernthese für Steps:** Ein unterstützendes System muss den *begründeten Möglichkeitsraum* sichtbar machen, ohne Kompositionsentscheidungen zu automatischen „Wahrheiten“ zu erklären. Ein Generator bietet Wege; eine Analyse bietet konkurrierende Lesarten; eine Wissensbasis erklärt, unter welchen Bedingungen eine Lesart plausibel ist.

## 3. Neue externe Forschung: belegte Schwerpunktsetzungen

- **Musikalische Form darf nicht auf Taktzahlen reduziert werden.** Caplin modelliert klassische Phrasenfunktionen, während Drew Nobile für Rock- und Popsongs den Zusammenhang zwischen harmonischem Verlauf und Form herausarbeitet. Ein Satzmodell ist nicht automatisch eine Rock-Song-Schablone. Quellen: [V5-002], [V5-003].
- **Poptonalität kann absichtlich verschleiert sein.** Mark Spicer unterscheidet fragile, emergent und absent tonics. Steps muss deshalb auch „Tonika fehlt“ als analysierbaren Zustand zulassen; es darf keinen I-Akkord nachträglich erfinden. Quelle: [V5-005].
- **Stimmführung ist nicht dasselbe wie minimale mathematische Entfernung.** David Huron diskutiert Wahrnehmung und Präferenzregeln; Cohn stellt für bestimmte chromatische Beziehungen Common Tones und semitonale Bewegung heraus. Beide Systeme beschreiben andere Aspekte des gleichen musikalischen Geschehens. Quellen: [V5-014], [V5-015].
- **Korpora beschreiben Stichproben.** de Clercq/Temperleys Rockkorpus wurde bewusst aus einer historisch und redaktionell verzerrten Grundgesamtheit gezogen. Codex darf keine Quoten daraus zu Naturgesetzen generalisieren. Quelle: [V5-009].
- **Anwendungsschemata brauchen Tonartenkontext und Unsicherheit.** DCML stellt u.a. globale/lokale Tonart und komplexe angewandte Akkorde dar; ChoCo normalisiert heterogene Harmonieannotationen. Beide sind Vergleichsstandards, aber kein automatisch verbindliches internes Steps-Datenmodell. Quellen: [V5-010], [V5-011].
- **Offene Software und offene Musikdaten haben unterschiedliche Rechte.** Die `music21`-Dokumentation unterscheidet die BSD-Lizenz des Codes von teilweise gesondert lizenzierten Corpus-Dateien. Bei ChoCo sind Subsets verschieden lizenziert. Quellen: [V5-011], [V5-013].
- **Musiktheorie ist kulturell situiert.** Ein Maqam wird nicht allein durch eine westliche Skalenliste beschrieben, sondern u.a. durch *sayr*, Phrasen und Ornamentation; Raga umfasst musikalische Praxis und ästhetische Dimensionen. Schemata für europäische Dreiklangsfolgen sind hier kein tragfähiges Universalmodell. Quellen: [V5-020], [V5-021], [V5-022].

## 4. Drei Evidenzklassen und ihre Konsequenz

| Status | Bedeutung | Darf Codex damit tun | Darf Codex nicht tun |
|---|---|---|---|
| `landing_page_checked` | Verlagsseite, Abstract, Inhaltsübersicht oder öffentliche Dokumentationsseite in dieser Recherche gesehen | Bibliografieren; Forschungsrichtung und Geltungsbereich formulieren | Behaupten, das ganze Buch sei gelesen oder genaue nicht eingesehene Seiten seien belegt |
| `content_section_checked` | Konkreter frei zugänglicher Textabschnitt (z.B. technischer Standard oder veröffentlichter Journaltext) eingesehen | Eng am tatsächlich eingesehenen Abschnitt belegte Aussagen machen | Aus einem Abschnitt auf das ganze Buch/Korpus schließen |
| `candidate_unchecked` | Sekundär erwähnt, bibliografische/inhaltliche Einzelprüfung noch offen | Kandidaten-Backlog führen | Quelle als geprüften Beleg für eine Theory Card verwenden |

**Insbesondere:** Die 77 V4-Quellen-/Editionseinträge bleiben im historischen Archiv und sind nicht automatisch alle erneut unabhängig geprüft. V5 führt nur den in dieser Ausbaurunde neu überprüften Evidenzstatus explizit aus.

## 5. Forschungsfragen, die nach dieser Ausbaustufe offen bleiben

- Welche exakten Datenformate, Spelling-Libraries, Schlüsselsysteme und Tests sind im echten Steps-Repository bereits enthalten?
- Wie werden westliche und nichtwestliche Systemtypen im Domainmodell nebeneinander und ohne falsche Gleichsetzung repräsentiert?
- Wo liegen exakte Fundstellen für alle grundlegenden Theorie- und Kompositions-Claims statt allgemeiner Quellennennungen?
- Welche musikalischen Kontrapunkt-/Formlehren dienen welchem Stil, Repertoire und Lernniveau?
- Können musikfachliche Reviewer die automatisch generierten Daten tatsächlich anhand von Partituren und Hörbeispielen freigeben?
- Welches reale Benutzerziel soll die erste funktionierende Version erfüllen? Das darf nicht aus dem Research erraten werden.

## 6. Reviewstandard: Was künftig als »fertig« gelten darf

1. Ein überprüfbares Quellenobjekt mit Scope und Lizenzstatus.
2. Ein fachliches Claim-Objekt mit einsehbarer Belegstelle oder explizitem `pedagogical_synthesis` statt fingiertem Beleg.
3. Eine Abgrenzung zwischen `identity`, `constraint`, `tendency`, `interpretation`, `empirical_frequency`, `compositional_option`.
4. Ein musikalisches Minimalbeispiel plus ein Gegenbeispiel oder Grenzfall.
5. Eine reproduzierbare technische Prüfung, soweit der Claim formal prüfbar ist.
6. Eine unabhängige musikalische/inhaltliche Reviewentscheidung, wenn interpretativ.
7. Eine dokumentierte Schnittstelle zu Produktfunktionen, ohne die Funktionen als bereits implementiert auszugeben.

## 7. Version und Veröffentlichung

Dieses Archiv ist eine **Wissens- und Forschungsgrundlage**, keine Änderung am Steps-Git-Repository. Originalquellen aus den 20 PDF/TXT-Anhängen und öffentlich-rechtlich geschützte vollständige Bücher bleiben außerhalb des veröffentlichten Wissensbestands, solange Rechte und Zugriff nicht geklärt sind. Git-Merge, offene Lizenzwahl und technische Produktentscheidungen sind keine Nebenwirkungen der Forschung.

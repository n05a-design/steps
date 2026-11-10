# Band VII — Produkt-UX, Didaktik, Skill-Orchestrierung und Forschungsbetrieb

## 1. Positionierung: unabhängiges Harmony-&-Composition-Labor

Der fachliche Mehrwert von Steps entsteht nicht dadurch, mehr Akkordkürzel als ein kommerzielles Plugin anzuzeigen, sondern dadurch, dass alternative musikalische Wege **erklärbar, hörbar, veränderbar und überprüfbar** werden. Der Nutzer kann einen Akkord, eine Melodie, ein Motiv, eine Basslinie oder einen formalen Abschnitt als Ausgangspunkt verwenden. Das System zeigt mögliche Beziehungen, deren Gültigkeitsbereich und die damit verbundenen kreativen Entscheidungen.

**Drei Nutzerziele unterscheiden:** (1) Lernen/Verstehen („Weshalb?“), (2) musikalisch Erkunden („Was könnte folgen?“), (3) Komponieren/Überarbeiten („Welche eigene Entscheidung setze ich um?“). Diese Ziele benötigen unterschiedliche Voreinstellungen, aber dieselbe source-aware Knowledge Base.

## 2. Harmonic Explorer – alternatives Verständnis statt erzwungener Lösung

Ausgangsakkord `Cmaj7` in C-Dur mit explizitem Stilfilter: Das System kann nach diatonischen Nachbarn, angewandten Dominanten, Mischung, chromatischen Medianten, Stimmführungsnähe, melodischer Verträglichkeit und empirischen Korpusübergängen gruppieren. Jede Kategorie besitzt getrennte Gründe.

**Karte `Fm6`:** (a) mögliche iv-Mischung, (b) konkrete Notentöne F–Ab–C–D, (c) mögliche Linie A→Ab→G in passendem Kontext, (d) Art des Nachweises: musiktheoretische Erklärung, nicht direkte empirische Häufigkeit, (e) Grenzen: *kein universell dunkler Effekt*, (f) mögliche Ziele C/E, G7 oder neue Farbe, nicht ein verpflichtender Folgeakkord.

## 3. Composer Workbench – separates Produktmodul

Fünf verknüpfte Arbeitsflächen ohne zwingende UI-Implementierung in der jetzigen Forschungsphase:

1. **Motif Board:** Noten/Rhythmus, Transformation, Wiedererkennbarkeit, Herkunft jeder Variante.
2. **Form Lane:** Section, Phrase, motivische Funktion, Ziel-/Kontrastplanung.
3. **Harmony Lane:** Progressionsereignisse, lokale Tonart/Modus, alternative Analysen.
4. **Voicing/Arrangement Lane:** Instrumentenregister, Stimmenidentität, Basslinie, innere Stimmen, Dichte.
5. **Revision Timeline:** Änderungen, A/B-Vergleiche, eigene Entscheidungen und fachliche Hinweise.

Ein Nutzer kann z.B. eine Melodie fixieren und verschiedene Harmoniefassungen entwickeln, dann eine davon als Version A festhalten und nur den Bass umarbeiten. Der Quellcode darf keine Entscheidung über die künstlerische Endfassung erfinden.

## 4. Didaktische Staffelung

**Beginner:** Tonart/Skala, Akkordbau, einfache diatonische Folgen, Grundmotive, Phrase, einfache Hörvergleiche. **Intermediate:** Septakkorde, Inversionen, Sekundärdominanten, Modal Interchange, motivische Variation, Satz-/Songform. **Advanced:** harmonische Mehrdeutigkeit, jazz-/blues-/pop-spezifische Modelle, Stimmführungskonflikte, Tonartenwege, chromatische Medianten, Instrumentierung. **Research:** Quellenstatus, formalisierte Regeln, Korpora, Repertoire-/Stichprobenbias, konkurrierende Theorieansätze, Evidenz- und Lizenzprüfungen.

Die Darstellungen dürfen vereinfacht sein, müssen aber sichtbar vereinfachte Interpretationen bleiben. „V7 muss nach I“ ist keine geeignete Beginner-Regel; besser ist „V7 führt in vielen tonalen Kontexten häufig zu I, aber es gibt andere Wege“.

## 5. Übungsgenerator: Aufgaben mit begründeten Zielkriterien

- **Spelling:** F#-Dur vs Gb-Dur korrekt notieren und enharmonische Differenz erklären.
- **Akkordbau:** `C7(b9)` in notierten Tönen erklären, dann mit `Cmaj9` vergleichen.
- **Modalität:** dieselbe `Dm7–G7`-Tonmenge in C-ii–V und D-Dorisch kontextualisieren.
- **Komposition:** Ein zweitaktiges Motiv rhythmisch augmentieren, als Antwortphrase umformen, anschließend Bass und Harmonik ergänzen.
- **Harmonic Rhythm:** gleiches Progressionsmuster mit anders gewichteten Akkordwechseln vertonen.
- **Blues:** I7 im Bluesschema als tonikal begründen, ohne Klassikfehlerdiagnose.
- **Wissenschaft:** Unterschied zwischen einer `landing_page_checked`-Quellenkarte und fachlich belegtem Claim erklären.

## 6. „Why does this work?“ – Antwortdatenvertrag

```json
{
  "selected_option": "Fm6",
  "context": {"tonic": "C", "style_lens": "major_with_modal_mixture"},
  "possible_explanations": [
    {"type": "modal_mixture", "claim": "iv6 may be read as mixture from parallel minor", "status": "interpretation"},
    {"type": "voice_leading", "claim": "A-Ab-G is a potential semitonal descent in a concrete voicing", "status": "requires_voicing"}
  ],
  "not_claimed": ["the only correct next chord", "objectively sad", "empirically most frequent"],
  "user_controls": ["style", "complexity", "melody", "bass", "harmonic_rhythm"]
}
```

## 7. Quellenprovenienz in der Oberfläche

Ein Zitat nur mit `V5-XXX` ohne konkreten Locator ist eine bibliografische Richtung, nicht eine durchgängig überprüfte Fundstelle. Die UI sollte den Unterschied zwischen „Theoriereferenz identifiziert“, „dieser Abschnitt gelesen“ und „Claims fachlich reviewed“ erklären. Bei unklaren Datenlizenzen werden originale Daten nicht ungefragt im Produkt ausgeliefert.

## 8. Skills: schmale Regeln, tiefe References

Die zukünftige `SKILL.md` sollte Aufgaben klassifizieren (Erklärung, Analyse, Composing, Code, Daten), relevanten Knowledge-Bereich laden, die Stil-/Tonartannahmen markieren, überprüfbare Quellen anführen und bei Mehrdeutigkeit mehrere Deutungen zulassen. Sie soll keine große Enzyklopädie als alleinigen Textcontainer duplizieren. Für Codex ist die Reihenfolge **Library/Review → strukturierte Rule Objects → Test Cases → schlanker Skill → User-UI**. Das ist ein Architekturvorschlag, keine bereits implementierte STEPS-Komponente.

## 9. Evaluation als Produktprinzip

Ein Satz „diese Folge funktioniert“ ist aus technischer, stilistischer, kognitiver und ästhetischer Perspektive unterschiedlich. Ein Lernsystem kann die mathematische Akkordstruktur validieren und eine begründete harmonische Deutung anbieten. Es darf jedoch die subjektive Qualität einer Komposition nicht als garantierten Fakt ausgeben. Ein User-Feedback-System sollte getrennt erfassen: Erklärung verstanden? Hörvergleich hilfreich? musikalisch verwendbar? theoretische Begründung plausibel? UI verständlich? Quellen transparent?

## 10. Wettbewerb: Inspiration ohne Nachbau

Historische Quellen nennen Chord Files, ModeWheel, The Chord Wheel, Hookpad, Scaler, Tonaly und weitere Produkte. V5 überprüft nicht systematisch ihre aktuellen Veröffentlichungsstände oder die jeweiligen Lizenzen; konkrete Features aus den alten V1–V4-Dokumenten bleiben deshalb **historische Analyse**, keine verifizierte Feature-Spezifikation von heute. Das eigene Steps-Design soll Fähigkeiten wie modal zentrierte Navigation, erklärbare Alternative, Motif-/Form-Bearbeitung und A/B-Hörvergleich zu einer transparenten, eigenständigen Workflow-Architektur verbinden.

## 11. Governance: neue Quelle bis geprüfte Funktion

`Source acquisition → Metadata/license → Reading with locator → Atomic claim → Conflict review → Style/Scope mapping → Example/counterexample → Formal unit test or manual review → KB version → Skill reference → Feature/UI validation`.

Nur ein ausdrücklich freigegebener Review darf einen Kontextclaim in den kanonischen Bestand verschieben. Ein automatisierter Validator kann nicht entscheiden, ob ein bestimmter Jazz- oder Popakkord künstlerisch „gut“ ist.

## 12. Produkt-Roadmap

- **R1 Fachmodell:** Quellenregistry, Spelling, Akkord-/Progression-/Motif-/Form-Objekte.
- **R2 Erklärung:** Multi-Lens-Anzeige, Alternativanalyse, didaktische Einführung, Beispielprüfung.
- **R3 Composer Workbench:** Motiv, Melodie, Bass, Form, Voice Leading, Revision.
- **R4 Notation/Playback:** vollständiger Notations- und MIDI-Interchange, Stimmregister und A/B-Vergleich.
- **R5 Corpus/Statistik:** nur mit echten lizenzierten Daten und ausgewiesener Stichprobe.
- **R6 spätere Erweiterungen:** ML-Assistenz und Drum-/Groove-Engine; ausdrücklich nicht Teil des jetzigen Research-Implementierungsauftrags.

**Forschungsanker:** Originale STEPS-Anforderungen V1–V4; Fachstandards [V5-001], [V5-010]–[V5-013], Formwissenschaft [V5-003], Tonika-/Songform [V5-005], MusicXML/MIDI [V5-024], [V5-025].

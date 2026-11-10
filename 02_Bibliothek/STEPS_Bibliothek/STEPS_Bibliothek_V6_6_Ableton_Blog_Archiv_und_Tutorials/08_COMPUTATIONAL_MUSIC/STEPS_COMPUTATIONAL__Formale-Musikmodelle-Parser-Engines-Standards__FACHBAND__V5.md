# Band VI — Computational Music Theory, Datenverträge, Engines, Sicherheit und Evaluierung

## 1. Architektur: Entkoppelung aus fachlichen Gründen

Die musikalische Wissensbasis ist kein GUI-Modul. Eine Tkinter-App und ein Codex-Skill sollen dieselben überprüften Theory Objects verwenden, ohne dass die Theorie aus Button-Callbacks zurückgewonnen werden muss. Das Repository ist in diesem Auftrag **nicht** geprüft; alle folgenden Pfade sind Vorschläge, an den Ist-Zustand anzupassen.

```text
steps/
  theory/       pitch, interval, scale, spelling, chord, key
  harmony/      annotations, rules, interpretations, scopes
  progressions/ events, rhythm, sections, transformation
  composing/    motif, phrase, theme, form, instrument, revision
  knowledge/    source, claim, concept, relationship, conflict
  adapters/     MIDI, MusicXML, Roman/ChordSymbol, JAMS/DCML
  validators/   syntax, musical logic, scope, provenance
  ui/           vorhandene Tkinter-Oberfläche oder später andere Oberfläche
```

## 2. Pitch und Spelling als separates Domänenmodell

Pitch Class `0..11` ist ein mathematisch nützlicher abstrakter Wert. Musikalische Note `F#4` braucht außerdem Buchstabenname F, Alteration +1, Oktave 4 und ggf. Locale/Tuning. Jeder Algorithmus, der aus `pitch_class=6` immer „F#“ macht, kann in Gb-Dur theoretisch falsch sein. Das API darf numerische Tonklassen und korrekt geschriebene Noten *nie* stillschweigend gleichsetzen.

Prüfbeispiel: In Gb-Dur ist der Tonvorrat `Gb Ab Bb Cb Db Eb F`. Das ist gleichklingend zu F#-Dur in 12-TET, aber F#-Dur wäre `F# G# A# B C# D# E#`. Das `Cb` entspricht B, das `E#` entspricht F. Beide Fassungen als getrennte Schreibprovenienz erhalten.

## 3. Akkordsymbole und Roman-Zahlen

Harte-Style-Symbole, Lead-Sheet-Notation, Jazz-Symbole und DCML-Roman-Annotationen unterscheiden sich semantisch. Ein Parser muss seinen Dialekt angeben. `V7/ii` bedeutet eine angewandte Dominante; `C/E` bedeutet ein Akkord mit E im Bass; beide enthalten einen Slash, aber haben unterschiedliche Grammatik. Ein Regex, der `/` ohne Kontext auftrennt, ist fehlerhaft. DCML enthält ausdrückliche Konventionen für lokale Tonart, angewandte Akkorde, Kadenz, Vorhalt und Pedal [V5-010]. `music21.roman.RomanNumeral` [V5-026] ist eine nützliche technische Vergleichsimplentation, nicht das Maß aller kontextuellen Musiktheorie.

## 4. Regeltypen und formale Geltungsbereiche

```yaml
rule_id: ST-V5-RULE-APPLIED-001
kind: tendency
statement: Sekundärdominanten können zu ihrer Zielharmonie leiten
preconditions: [tonal_context, applied_dominant_label]
style_scope: [common_practice, jazz, selected_pop]
exceptions: [deceptive_resolution, elision, dominant_chain, delayed_arrival]
testable_claims:
  - leading_tone_can_resolve_to_target
non_claims:
  - target_must_follow_immediately
source_support: []
review_status: proposed
```

Das Schema zwingt eine Unterscheidung zwischen **harter Definition** (`major triad pc intervals = [0,4,7] in 12TET`), **Bedingung** (`no simultaneous overlap within one nonpolyphonic harmonic lane`), **Tendenz** (`V7→I häufig`), **Interpretation** (`Rock-Loop hat emergente Tonika`) und **Kompositionsvorschlag** (`hier wäre iv möglich`). Strukturelle Testbarkeit ≠ wissenschaftliche Normativität.

## 5. Progression und Rhythmus als Ereignisse

Verwende rationale Ticks oder Fraction-Dauern; Float-Beats allein können bei Triolen numerische Fehler erzeugen. Speichere Meter und event time getrennt. Vermeide „ein Akkord pro Takt“ als stillschweigende Annahme. Wenn ein harmonisches Ereignis über eine Section-Boundary reicht, muss die Schnittstelle eine klare Cross-Section-Darstellung haben. Bei Import aus MIDI darf keine automatische Roman-Analyse als ground truth gesetzt werden.

## 6. Composing-Modell mit Revision/Provenienz

Eine Komposition braucht mehr als ChordEvents. Minimale Objekte: `Piece`, `Section`, `Phrase`, `Motif`, `Transformation`, `NoteEvent`, `HarmonyEvent`, `Voice`, `InstrumentProfile`, `Version`, `Decision`, `Review`. Ein Motif-Transformation-Objekt erhält Quell-Motiv-ID, Operation, Parameter (Pivot/Intervalle/Time Scale), Resultat und Reversibilität. Ein Arrangement-Objekt hält Register, Besetzung, Doublings, Artikulation und Layer. Wenn sich die Melodie ändert, darf sie nicht automatisch die Akkord-Analyse überschreiben.

## 7. Technische Austauschformate

- **MIDI 1.0/2.0:** Playback und Performance-Events; MIDI2 erweitert MIDI1, ersetzt es nicht [V5-025]. Keine komplette Garantie korrekt notierter Enharmonik.
- **MusicXML 4.0:** Austausch digitaler Notenschrift, Akkordbezeichnungen, Stimmen, Takt/Notationsdetails [V5-024]. Rückkonvertierung kann Layout-/Interpretationsebenen verlieren.
- **JAMS/ChoCo:** Corpus-Annotation und zeitbezogene harmonische Label, Provenienz- und Dataset-Bewusstsein [V5-011].
- **DCML:** tonale/harmonische Analysen inkl. lokaler/globaler Keys und Kadenz [V5-010].
- **JSON/YAML:** eigene versionierte KB-Objekte mit expliziten Schemata; ohne kontrollierte Migration keine Versionstabilität.
- **Music21:** Vergleichsbibliothek für Symbol-/Key-/Roman-Berechnungen; Lizenztrennung zwischen Code und Corpus [V5-013].

## 8. Wissensgraph und Quellenketten

`SOURCE → LOCATOR → CLAIM → CONCEPT → RULE / EXAMPLE → TEST / FEATURE` ist eine fachliche Rückverfolgung, nicht bloß eine Ordnerstruktur. Jeder Claim braucht Geltungsbereich, Evidenzart, Verantwortlichkeit und Status. Wird eine Quelle umgelagert oder ein Claim widerlegt, müssen abhängige Objekte auffindbar sein. Externe Web-URLs können brechen; DOI/ISBN, bibliografische Ausgabe, eine geprüfte Kapitelstelle und bibliografisches Archivmetadatum sind robuster als Chat-Zitatmarker.

## 9. Research-Evidence-Level als API-Feld

Ein Bibliografieeintrag mit Verlagsabstract darf zu `source_status: landing_page_checked` werden; daraus darf nicht `claim.status: scientifically_validated` folgen. Bewahre alle Schritte: `identified`, `metadata_checked`, `content_accessible`, `locator_checked`, `claim_checked`, `peer_reviewed`, `adopted`. Automatisierte Datenvalidierung darf `adopted` nicht setzen, wenn ein fachlicher Reviewer verlangt wird.

## 10. Korpusstatistik, Datenqualität und Lizenzen

ChoCo integriert heterogene Annotationen, aber auch dort gelten unterschiedliche Subdatensatz-Lizenzen; JAAH, CASD und Mozart Piano Sonata werden mit zusätzlichen CC BY-NC-SA-Bedingungen angegeben [V5-011]. Der When-in-Rome-Code-/Analysebestand trennt neu erstellte und konvertierte Inhalte mit teilweise anderen Lizenzursprüngen [V5-012]. Codex darf keine Korpora blind ins öffentliche Git laden. Auch das `music21`-Corpus ist nicht automatisch unter der BSD-Code-Lizenz [V5-013].

**Statistikformeln:** Empirische `P(chord_next | context, corpus, annotation_schema)` ist bedingt auf diese Wahl. Datensatz-Ableitung benötigt eindeutige Maße für observation grain: chord event vs bar vs phrase vs song. Genre-Bias und falsche Join-Kardinalität können Scheinresultate erzeugen. Ein 2026er Content-Release ist nicht allein wegen „mehr Songs“ repräsentativer.

## 11. Tests: Ebenen und Erfolgsmeldungen

- **Syntax:** JSON Schema, Typen, IDs, Links, Takt-Event-Konsistenz, MusicXML/MIDI-Parsebarkeit.
- **Numerik:** Intervalle, Pitch Classes, Transposition, Oktaven, MIDI Ranges, Tick-Konversion.
- **Notationslogik:** Spelling F#/Gb, Akkordalterationen, Tonleitern in scharfen/flachen Keys, deutsche H/B-Konvention.
- **Harmonieanalyse:** bekannte Beispiele plus bewusst mehrdeutige Alternativfälle, style-scoped Rules, falsche automatische Funktionen als Negative Tests.
- **Form/Melodie:** Phrasenenden und Kadenz nur bei Kontext, Motiv-Transformation-Korrektheit, Melody-Fit mit Tensions.
- **Review:** Stimmführung, Spielbarkeit, künstlerische Absicht/Qualität; Automatik kann offene Fragen aufdecken, nicht abschließend entscheiden.

Ein erfolgreicher MIDI-Parser-Check zeigt lediglich syntaktische Konsistenz. Er beweist weder Korrektheit einer Roman-Zahl noch musikalische Qualität einer Komposition.

## 12. Sicherheit und Offenheit

Repository-Einträge können urheberrechtlich geschützte PDFs, Noten, Samples oder komplette kommerzielle Buchtexte enthalten. Solche Dateien nicht ungeprüft publishen. Bei einer schwachen Metadatenlage bleibt ein `copyright_review_pending`-Flag in allen abgeleiteten Datensätzen. Eine offene Softwarelizenz deckt nicht automatisch die externe Source Library. Der Code und die Fachinhalte brauchen getrennte Lizenz-/Attributionsentscheidungen.

## 13. Produkt- und UX-Schicht

Chord Files, ModeWheel, Tonnetz, Hookpad und Scaler sind inspirierende Vergleichsfelder, aber konkrete Drittproduktgrafiken oder proprietäre Texte sind keine Implementierungsvorlagen. Für Steps ist die nachvollziehbare Begründung einer Akkord- oder Kompositionsoption wichtig: Nutzer sieht alternative `lenses`, das `why`, anwendbare `constraints`, Spannungs-/Stimmführungs-Signale und **echte** Quellen. Falls eine Quelle nur `landing_page_checked` ist, soll die UI sie nicht als fachlich bestätigten Claim darstellen.

## 14. Roadmap für technische Integration

**P0** Repo read-only inventarisieren und Source/License-Gate einbauen. **P1** Pitch/Scale/Chord/Key- und formale Schema-Tests. **P2** Theory Objects, Progression Events, Claims, Multi-Lens-Analyse und Counterexamples. **P3** Composing Objects, Motif/Transformation/Voice/Arrangement und evaluierbare Originalstudien. **P4** UI-/Skill-Integration, fachliche Reviews, Komponierexperimente. **Später** Corpus-Ranking/ML; Drum-Engine und Drum-Datensätze bleiben außerhalb dieses Auftrags. Aktuelles Rhythmus- und Meterwissen gehört jedoch vollständig zu Composing.

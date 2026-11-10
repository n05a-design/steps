# Architekturziel STEPS

## Komponenten

1. **Domain (`src/steps`)**: reine und deterministische Modelle für Pitch/Intervals/Scales/Chords, Transposition, Enharmonik und Progressionsrelationen; keine UI, Dateisystem- oder Musikplayer-Abhängigkeit.
2. **Application (`app`)**: später GUI, Session-Lifecycle, Interaktionszustand, Darstellung, Accessibility und Adapter.
3. **Knowledge (`knowledge`)**: Quellen-IDs, Begriffskataloge, fachliche Relationen und Demo-Daten mit Provenienz.
4. **Research (`research`)**: Forschung, methodischer Zweifel, Wettbewerber und Ableton-/Produktionsarchive. Keine direkte Runtime-Abhängigkeit.
5. **Schemas (`schemas`)**: stabile Contracts; Änderungen werden versioniert und mit Regressionstests begleitet.
6. **Quality (`tests`, `tools/validation`, CI)**: statische Strukturchecks, später Domain-/UI-/Datenprüfungen und Linkprüfung.
7. **Design (`design`)**: eigene Assets und Design-Tokens getrennt von externen Inspirationsmaterialien.

## Fachliche Gates vor Implementierung

- Begriffsschema/Notationssystem DE vs. international, enharmonisches Spelling, Tonarten und Kontext klar definiert.
- Akkorde und Progressionsbeziehungen typisiert; alternative Analysewege zulässig.
- Quellregistry mit Lizenz-/Evidenzstatus befüllt.
- Definition eines MVP: Chord-Explorer mit Create/Edit, Explanation, Transposition; Playback/Export nur nach technischer Freigabe.

## Abgrenzungen

Die Dokumentenbibliothek V6.6/V6.7 stellt **keine** lauffähige App dar. Code aus `glide-to-do` ist ein potentieller Referenzbestand, nicht bereits in diesem Repo verifiziert. Music-production-Archive sind explizit außerhalb des ersten Harmony-MVP.

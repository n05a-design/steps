# Architektur-Entscheidungsnotiz: Glide 3.53.0 als STEPS-Ausgangsbasis

**ID:** DEC-GLIDE-STEPS-2026-11-10
**Status:** `user_direction_confirmed; implementation_method_proposed`
**Stand:** 10.11.2026
**STEPS-Referenz:** `1fc07e230dc6a2fe92fd6662da43e332d596b376`
**Glide-Referenz:** `9e767bea5e21063466a28ac3a679406484ad5d5f`

## Festgelegte Zielrichtung

Die Projektverantwortlichen haben festgelegt, die erfolgreich geprüfte Glide-App **3.53.0** als technische Referenz und Ausgangsbasis zu verwenden. Die eigentliche STEPS-App entsteht nach einem **kontrollierten, nachvollziehbaren Rückbau der Glide-Aufgabenfachlichkeit auf eine neutrale Desktop-Shell**. Die verbleibenden UI-/Infrastruktur-Fähigkeiten bilden das Grundgerüst für STEPS. Glide bleibt als eigenständiges Ursprungssystem unverändert.

## Nicht vorweggenommene technische Wahl

Das Wort „Rückbau“ legt den technischen Pfad noch nicht abschließend fest. Die Alternativen **A** inkrementeller Fork/Rückbau, **B** selektive Extraktion, **C** vorübergehender Adapter und **D** äquivalente schlanke Shell auf Basis der Glide-UX-Verträge sind anhand derselben tatsächlichen Tests, Risiko- und Wartbarkeitskriterien zu vergleichen. Aufgrund der zentralen `ListApp`-Kopplung darf ein Voll-Fork ohne Nebenwirkungsanalyse nicht als billig oder risikoarm angenommen werden.

## Fachliche Grenzen

STEPS soll keine Aufgabenlisten unter anderem Namen darstellen. Geplante Musikdomänen bleiben unabhängig von Glide: Pitch/Spelling, Chords, Progressions, Harmonic-Context, MusicTime, MIDI, Drums, Knowledge und Pädagogik. Glide-Daten-/Nutzer-/Systempfade bleiben unberührt. Eigene STEPS-Namen, Markenassets, Lockfiles, Settings und Projektdaten sind zwingend.

## Prüf- und Freigabevoraussetzungen

- Vollständiger Freeze/Hash-/Dependency- und Lizenzvergleich von Glide-Origin und `src/glide-v3.53/`.
- Erhaltungsvertrag für Shell, Theme, Settings, Navigation, Fokus, Responsivität, Accessibility, Crash Recovery und Packaging.
- Negativtests gegen jede Glide-Nutzerdatenberührung, versteckte Task-Action, Timer und Hook.
- 30 Shell-QA-Szenarien getrennt nach Plattform, tatsächliches `PASS` nur bei reproduzierbarem Lauf.
- Architektur-ADR über `src/steps/` gegenüber `src/steps-0.00/` und die geplante Importpaketstruktur.
- Explizite Code-/Asset-/Lizenzfreigabe vor öffentlicher Veröffentlichung; keine automatische Drittmaterial-Mitlizenzierung durch MPL-2.0.

## Quellenhinweise

- `docs/engineering/SHELL_EXTRACTION_DEEP_SPEC.md`
- `docs/architecture/GLIDE_TO_STEPS_2_AREA_SHELL.md`
- `docs/architecture/REUSE_AND_MIGRATION_MATRIX.md`
- `prompts/02_GLIDE_FINISH_FREEZE.md`, `03_GLIDE_AUDIT_REUSE.md`, `04_GLIDE_TO_STEPS_SHELL.md`, `26_GLIDE_SHELL_COMPARE_SPIKES.md`
- `src/glide-v3.53/`, `src/steps-0.00/`

**Abgrenzung:** Dies ist eine Dokumentation der Zielrichtung, kein Nachweis einer bereits aufgebauten STEPS-Shell oder einer erfolgten Code-Migration.

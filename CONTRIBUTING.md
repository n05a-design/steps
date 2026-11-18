# Contributing to STEPS

Open or identify an issue before making a change. Describe the problem, scope,
expected outcome, dependencies, and sources. English is the default language
for new public documentation and user-facing strings; German-language
contributions are welcome.

- Keep pure music-domain logic in [`src/steps/`](src/steps/) and desktop/UI
  integrations in [`app/`](app/). New knowledge content needs source
  provenance, rights status, and the required domain review.
- For API changes, update the [generated API reference](docs/theory/API.md)
  and the relevant [implementation status](docs/IMPLEMENTATION.md).
- Do not add third-party PDFs, website snapshots, audio, MIDI, screenshots, or
  source code without an explicit provenance and rights review.
- Each pull request documents its purpose, affected files/data paths, relevant
  tests, compatibility impact, and known limitations. Assess the domains in
  the [continuous repository maintenance contract](docs/governance/CONTINUOUS_MAINTENANCE.md).
- Tests must be deterministic and reproducible offline. Include explicit
  cases for German `H/B`, international `B/Bb`, enharmonic spelling, and
  context-dependent harmonic interpretations when those contracts are
  affected.
- Do not merge historical library editions based only on similar filenames.
  Preserve their identifiers and document substantive differences.
- Respect the repository's MPL-2.0 license and the separate terms of external
  material. Do not copy code from Glide without a documented license and
  architecture review.

## Deutsch

Vor Änderungen ein Issue mit **Problem, Scope, erwarteten Ergebnissen und
Quellen** eröffnen oder ein bestehendes Issue benennen. Englisch ist die
Standardsprache für neue öffentliche Dokumentation und sichtbare Texte;
deutschsprachige Beiträge sind willkommen.

- Reine Musikdomänenlogik gehört nach [`src/steps/`](src/steps/), Desktop- und
  UI-Integrationen nach [`app/`](app/). Neue Wissensinhalte benötigen
  Quellenherkunft, Rechteklasse und die erforderliche Fachprüfung.
- Bei API-Änderungen die [generierte Referenz](docs/theory/API.md) und den
  [Implementierungsstand](docs/IMPLEMENTATION.md) aktualisieren.
- Keine externen PDFs, Webseiten-Snapshots, Audio-, MIDI-, Bild- oder
  Quellcodedateien ohne Provenienz- und Rechteprüfung hinzufügen.
- Jede PR dokumentiert Zweck, betroffene Dateien/Datenpfade, relevante Tests,
  Kompatibilität und bekannte Grenzen. Die
  [kontinuierliche Repository-Pflege](docs/governance/CONTINUOUS_MAINTENANCE.md)
  ist zu berücksichtigen.
- Tests müssen deterministisch und offline reproduzierbar sein. Betroffene
  Verträge zu deutschem `H/B`, internationalem `B/Bb`, Enharmonik und
  harmonischer Mehrdeutigkeit brauchen explizite Fälle.
- Historische Bibliotheksversionen nicht nur wegen ähnlicher Dateinamen
  zusammenführen; Kennungen und fachliche Unterschiede bewahren.
- MPL-2.0 sowie die separaten Bedingungen fremder Inhalte beachten. Glide-Code
  nicht ohne dokumentierte Lizenz- und Architekturprüfung übernehmen.

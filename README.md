<p align="center">
  <img src="app/assets/brand/steps-app-icon-512.png" alt="STEPS app icon" width="96" height="96">
</p>

<h1 align="center">STEPS</h1>

<p align="center">
  <strong>Build chord progressions. Explore harmony. Export MIDI.</strong><br>
  An open-source music-theory toolkit for musicians and producers. A typed Python core and Tkinter desktop prototype support chord progressions, context-aware analysis, and MIDI export.
</p>

<p align="center">
  <img alt="Status: music core and desktop prototype" src="https://img.shields.io/badge/Status-Core%20%2B%20desktop%20prototype-555">
  <img alt="Python 3.11 to 3.14" src="https://img.shields.io/badge/Python-3.11%E2%80%933.14-209F95">
  <a href="LICENSE"><img alt="MPL-2.0 license" src="https://img.shields.io/badge/License-MPL--2.0-209F95"></a>
  <a href="https://github.com/n05a-design/steps/actions/workflows/python-tests.yml"><img alt="STEPS test suite" src="https://github.com/n05a-design/steps/actions/workflows/python-tests.yml/badge.svg?branch=main"></a>
</p>

<p align="center">
  <a href="#see-it-in-action"><strong>See it in action</strong></a> ·
  <a href="#quick-start">Quick start</a> ·
  <a href="#what-works-today">Current capabilities</a> ·
  <a href="#status-and-scope">Project status</a> ·
  <a href="README.de.md">Deutsch</a>
</p>

## What STEPS is

The core keeps the distinctions behind harmony visible: sounding pitch, pitch class, note spelling, chord identity, chord symbol, voicing, inversion, and harmonic function.

The product direction is a local-first workspace for learning while composing; this remains a hypothesis, not a result of completed user research. `v0.1.0` is the latest published release.

## Why STEPS?

- **Context changes meaning.** A chord symbol and its harmonic function are not the same; the example below resolves `V7/vi` in C to `E7`.
- **Notation stays explicit.** German `H/B` and international `B/Bb` remain distinct, with enharmonic spelling preserved where supported.
- **Selected examples are traceable.** Reviewed lessons connect their claims to source evidence; the wider research archive is not automatically product content.

## See it in action

This generated piano-roll view shows voicings computed by the core for three reviewed examples. It illustrates core output, not a screenshot of the desktop prototype.

<img alt="Generated piano-roll visualization of voicings for Pop Four Chords, Jazz Two-Five-One, and Minor Plagal Romance" src="design/assets/project-page-pilot-voicings.svg" width="1200" height="482" loading="lazy">

<p><sub>Reviewed pilot examples · the darker note in each chord is the bass</sub></p>

```python
from app.knowledge import get_reviewed_progression
from src.steps.progression import resolve_roman_degree

example = get_reviewed_progression("PROG-003")
print(example.progression.chords_str)                 # Dm7 - G7 - Cmaj7
print(resolve_roman_degree("V7/vi", "C").symbol)       # E7
```

The [reviewed examples](knowledge/concepts/progressions/REVIEWED_PROGRESSIONS.md) include source-linked lessons and approval evidence.

## What works today

- **Pitch, spelling, intervals, and chords:** typed theory APIs distinguish German `H/B` from international `B/Bb` and preserve enharmonic spelling where supported.
- **Progressions and voicings:** key-aware Roman-numeral analysis, transposition, chord voicings, and configurable voice-leading styles are available in the Python core.
- **Contextual recommendations:** progression services can return candidates and relation types; theoretical interpretations remain context-dependent.
- **Desktop vertical slices:** the prototype explores next-chord candidates, loads reviewed examples as projects, and exposes a persisted voice-leading style. These are implemented workflows, not independent release or human-domain acceptance.
- **Project data:** versioned JSON project storage and session save/load services exist. The controller-level vertical-slice test exercises a save/reopen round trip.
- **MIDI:** SMF format 0/1 writers and export services are available. The CLI and desktop prototype expose export paths; automated tests inspect the resulting files.
- **English and German:** localized catalogs and a persisted UI-language preference are implemented.
- **Reviewed examples:** selected learning examples are published with source references and review evidence. The larger research archive is not automatically approved product content.
- **Desktop:** edit chords, inspect localized continuation suggestions and their provenance, and compare voice-leading styles on aligned piano rolls. The workflow includes reviewed examples, MIDI export and project save/open with unsaved-change prompts.

See the [implementation status](docs/IMPLEMENTATION.md) for precise behavior and limits.

## Status and scope

- `v0.1.0` is the latest public release. Current development version is `0.7.0-dev` (`0.7.0.dev0`), with the desktop application running on the integrated `glide_shell` `0.6.2` (from Glide `v1.0.2`) with responsive 2-area layout, 10 accessible Glide themes, UI accent colors, 10 background tints, adjustable corner radius, font scaling, user settings persistence, and modal appearance customization. A macOS development bundle can be built locally. Distribution approval and the 1.0 scope and date remain open.
- Project open/save exists in the prototype; native file-dialog, recovery, accessibility, and platform acceptance remain open. Automated MIDI tests do not establish DAW interoperability.
- English/German catalogs and persisted language selection exist; independent translation acceptance remains open.
- There is no in-app audio playback or MIDI import, and no user-study evidence for learning outcomes or product-market fit.

[ADR-013](decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md) defines chord progressions and MIDI export as the v0.1 product slice and defers drum editing to app v2. Reconsidering that scope requires an explicit owner decision.

## Quick start

Use Python 3.11–3.14 from the repository root. The test and core commands do not require a separate runtime dependency.

```sh
python3 -m app.main --headless
python3 -B -m unittest discover -s tests
```

Export the prototype's initial progression to an SMF file:

```sh
python3 -m app.main --export-midi /tmp/steps-progression.mid
```

To open the Tkinter prototype, run `python3 -m app.main` in an environment with Tk and a graphical display. A source checkout is not the same as a published desktop installer.

To build and inspect the existing Python wheel artifact without installing it into the repository environment:

```sh
python3 -m pip wheel . --no-deps --wheel-dir ./dist
python3 -B -m unittest tests.test_package_artifacts -v
```

The wheel check uses an isolated install to verify the `steps` entry point, runtime resources, and all three reviewed examples. For the native macOS development bundle and widget tests, see the [Desktop verification guide](tests/native_ui/README.md).

## Product target and documentation

The [STEPS 1.0.0 product target](docs/product/V1.0.0_PRODUCT_CONTRACT.md) compares the proposed 1.0 scope with repository evidence, identifies gaps, and defines release gates. It is a proposal awaiting owner review; it does not claim that those gates have passed.

- [Product strategy](docs/product/PRODUCT_STRATEGY_AND_MVP.md)
- [Architecture and engineering](docs/architecture/README.md)
- [Internationalization assessment](docs/engineering/INTERNATIONALIZATION.md)
- [Music-domain and MIDI contracts](docs/engineering/MUSIC_DOMAIN_AND_MIDI.md)
- [Roadmap](docs/roadmap/ROADMAP_AND_RESOURCE_PLAN.md)
- [Knowledge base and sources](knowledge/README.md)
- [Continuous repository maintenance](docs/governance/CONTINUOUS_MAINTENANCE.md)
- [Security policy](SECURITY.md)

## Contributing and community

Read [CONTRIBUTING.md](CONTRIBUTING.md) before opening a change. English is the default for new public documentation; German contributions are welcome. UI language and musical notation are separate settings and must remain so.

Report bugs and propose features in the [issue tracker](https://github.com/n05a-design/steps/issues/new/choose). For a music-theory issue, include the notation convention, musical context, expected interpretation, and source where available. Do not post private or copyrighted source material in a public issue.

## License and rights

STEPS source code is licensed under [MPL-2.0](LICENSE). Research sources, learning data, and third-party assets may have separate terms; consult the [rights policy](knowledge/sources/RIGHTS_POLICY.md). The repository license does not grant rights to every file or source cited in the project.

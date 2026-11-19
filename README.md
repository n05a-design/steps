<p align="center">
  <img src="app/assets/brand/steps-app-icon-512.png" alt="STEPS icon" width="96">
</p>

<h1 align="center">STEPS</h1>

<p align="center">
  <strong>Build chord progressions. Understand harmony. Learn from sources.</strong><br>
  STEPS is an independent open-source music-theory project. Its Python core, a Tkinter desktop prototype, project-storage services, and Standard MIDI File export are in the repository. A complete installable product has not yet been released.
</p>

<p align="center">
  <img alt="Status: music core and desktop prototype" src="https://img.shields.io/badge/Status-Core%20%2B%20desktop%20prototype-555">
  <img alt="Python 3.11 to 3.14" src="https://img.shields.io/badge/Python-3.11%E2%80%933.14-209F95">
  <a href="LICENSE"><img alt="MPL-2.0 license" src="https://img.shields.io/badge/License-MPL--2.0-2E7D32"></a>
  <a href="https://github.com/n05a-design/steps/actions/workflows/python-tests.yml"><img alt="STEPS test suite" src="https://github.com/n05a-design/steps/actions/workflows/python-tests.yml/badge.svg?branch=main"></a>
</p>

<p align="center">
  <a href="#quick-start"><strong>Quick start</strong></a> ·
  <a href="#what-works-today">Current capabilities</a> ·
  <a href="docs/product/V1.0.0_PRODUCT_CONTRACT.md">1.0 target and gaps</a> ·
  <a href="README.de.md">Deutsch</a>
</p>

## What STEPS is

STEPS helps musicians and producers build chord progressions, inspect how musical context changes their interpretation, and export progression data. The project keeps sounding pitch, pitch class, note spelling, chord identity, chord symbol, voicing, inversion, and harmonic function distinct.

The product direction is a local-first workspace for people who want to learn while composing. That is a product hypothesis, not a result of completed user research. The current published release is `v0.1.0`; development metadata is `0.2.0-dev` / `0.2.0.dev0`. STEPS 1.0.0 has not yet been approved or scheduled.

## What works today

- **Pitch, spelling, intervals, and chords:** typed theory APIs distinguish German `H/B` from international `B/Bb` and preserve enharmonic spelling where supported.
- **Progressions and voicings:** key-aware Roman-numeral analysis, transposition, chord voicings, and configurable voice-leading styles are available in the Python core.
- **Contextual recommendations:** progression services can return candidates and relation types; theoretical interpretations remain context-dependent.
- **Desktop vertical slices:** the prototype explores next-chord candidates, loads reviewed examples as projects, and exposes a persisted voice-leading style. These are implemented workflows, not independent release or human-domain acceptance.
- **Project data:** versioned JSON project storage and session save/load services exist. The controller-level vertical-slice test exercises a save/reopen round trip.
- **MIDI:** SMF format 0/1 writers and export services are available. The CLI and desktop prototype expose export paths; automated tests inspect the resulting files.
- **Reviewed examples:** selected learning examples are published with source references and review evidence. The larger research archive is not automatically approved product content.
- **Desktop prototype:** a Tkinter two-area window supports chord entry, transposition, theory display, MIDI export, and project open/save with unsaved-change prompts and visible errors. It is not yet a complete packaged or platform-accepted application.

See the [implementation status](docs/IMPLEMENTATION.md) for precise behavior and limits.

## What is not ready yet

- No verified desktop installers or complete platform-by-platform release acceptance.
- Project open/save is exposed in the main window; native platform, accessibility, and recovery acceptance remain open.
- English/German catalog coverage and runtime/persisted UI-language switching exist; independent translation and native platform/accessibility review remain open.
- No in-app audio playback or MIDI import.
- No external DAW interoperability sign-off is evidenced by the automated MIDI tests alone.
- No user-study evidence establishes learning outcomes or product-market fit.
- No approved STEPS 1.0.0 scope or release date exists.

The existing [v0.1 decision](decisions/ADR-013-v01-umfang-akkorde-und-midi-export.md) defines chord progression work and MIDI export as the product slice and defers drum editing to app v2. Reconsidering that scope requires an explicit owner decision.

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

The wheel check verifies the `steps` console entry point and the localized catalogs and brand assets packaged in the artifact. It starts the installed package in headless mode. It does not build or verify a signed desktop installer, notarized application, platform-specific package, or fresh-machine installation.

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

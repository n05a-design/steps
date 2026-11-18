# STEPS Internationalization Architecture and Glide Reference

**Status:** STEPS target contract with an initial implementation in the current work branch; translation and native-platform acceptance remain pending.

**Assessment date:** 2026-11-18.
**Glide evidence:** `n05a-design/glide-to-do` main `1e99bf1d1f6d0a6d79315a62f5bd4ecb08ca05eb`; i18n PR #134 merge `5f0db505488b18c18fbce9b9c2c7eafe9a6027c9`.

## Current STEPS status

The initial implementation in this branch adds the Tkinter-free `app/i18n.py` resolver, JSON catalogs under `app/locales/`, a persisted `system`/`en`/`de` UI preference, a runtime language menu, and a CLI `--language` override. The current UI strings, project dialogs, analysis labels, and headless CLI output are routed through the catalogs. This implementation has automated catalog, persistence, runtime-switch, notation-independence, and entrypoint tests; it is not yet merged or accepted through native platform, assistive-technology, or translation review.

System resolution checks `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, then `LANG`, and finally Python's detected locale. For a `LANGUAGE` list, the first supported language is used; unsupported values resolve to English. User preference files are stored in the platform's standard per-user configuration directory and contain only the UI language, never project or notation data.

The accepted music-domain contract already requires separate pitch, pitch-class, spelling, chord identity, symbol, voicing, inversion, and context function. Localization must not collapse these distinctions or mutate stored musical values.

## Glide i18n audit

The Glide reference is useful as an architectural example, not a STEPS code dependency. Its i18n implementation was added in [PR #134](https://github.com/n05a-design/glide-to-do/pull/134), merged on 2026-11-17. The source repository is licensed MPL-2.0. No Glide source or catalog is copied by this assessment.

### Observed design

| Concern | Glide implementation observed in `i18n.py` / PR #134 | STEPS implication |
|---|---|---|
| Core/UI boundary | The translation module uses only Python standard-library modules and has no Tkinter dependency | Keep language resolution and catalog lookup pure and independently testable. |
| Languages | `de` and `en`; the Glide module sets German as its default | STEPS resolves unsupported languages to English and supports a separate `system` preference. Do not copy Glide's default unchanged. |
| System detection | Checks `LANGUAGE`, `LC_ALL`, `LC_MESSAGES`, `LANG`, then `locale.getlocale()`; recognizes English and German | Isolate detection behind a deterministic function and test environment precedence on each supported OS. |
| Catalogs | JSON resources with semantic dotted keys; the two Glide catalogs have 102 keys each | Use stable semantic keys and require catalog/key/placeholder parity in CI. |
| Translation API | Glide exposes `t(key, default=None, **kwargs)` with catalog/default/key fallback | STEPS uses `LocaleManager.translate(message_id, **values)` and raises for missing keys or invalid placeholders; keep incomplete catalogs visible. |
| Interpolation | `safe_format` uses named Python format fields and returns the template when formatting raises selected errors | Define and test exact placeholder semantics. Validate placeholder parity; avoid swallowing unrelated runtime errors. |
| Cache and runtime switching | Catalogs are cached; `set_language` updates the in-process language and loads the selected and default catalogs | Switching must refresh every visible STEPS view, menu, dialog, and status message without changing a project. |
| Preference persistence | Glide's core module stores process state only; the settings UI is a separate integration | STEPS stores only `{"language": ...}` in a per-user preferences file using an atomic replacement; restart behavior is tested, while cross-platform CI and settings-write failure acceptance remain. |
| UI integration | Glide PR #134 reports translation integration for settings, menus, mnemonics, and selected sidebar entries | The STEPS main window localizes its current menus, labels, dialogs, and analysis content; headless behavior is tested, while native accessibility and a complete surface inventory remain open. |
| Tests | Glide's `test_i18n.py` contains 11 tests for resolution, lookup, formatting, parity, and import/module constraints | STEPS `tests/test_i18n.py` covers key/placeholder parity, system resolution, platform paths, persistence, runtime switching, missing keys, and notation independence. Continue cross-OS and human reviews; no Glide code is reused. |
| Follow-up | [PR #137](https://github.com/n05a-design/glide-to-do/pull/137) adjusts dialog/window tests to avoid assuming a particular translated quit label; it reports the i18n suite still passing | UI tests should assert stable action IDs/behavior rather than localized display text except in translation-specific tests. |

### Design limitations to improve rather than copy

- Glide's German default is at odds with STEPS's requested English-first product policy.
- Unknown/unsupported language values fall back to German in the current helper. STEPS should resolve unsupported system languages to English and preserve the original preference (`system`) separately from the resolved language.
- Glide returns empty catalogs after several load/parse errors and falls back at runtime. STEPS should fail catalog validation in CI and surface a clear diagnostic for a broken bundled catalog.
- The helper does not persist settings itself and provides no pluralization contract. Do not infer persistence from the helper module or add pluralization machinery until the product text needs it.
- The reported setting UI and the core translation module are separate concerns. STEPS acceptance must test preference storage, restart, and full-screen refresh directly.

## STEPS target contract

### Language and notation are independent

The UI preference is `system`, `en`, or `de`. On first run, `system` detects a supported system language; any unsupported system language resolves to English. A user-selected `en` or `de` survives restart. English is the product default and fallback.

Musical notation remains a separate setting, at minimum `INT` and `DE`. For example, an English UI may display German note names, and a German UI may display international names. Language changes must not rewrite:

- project schema keys, IDs, enum values, or serialized field names;
- pitch class, MIDI note number, rhythm/time values, or chord identity;
- the selected notation convention or any existing spelling;
- source text, claim status, or a reviewed content revision.

### Core/catalog contract

1. Provide one Tkinter-free resolver and translation API under the existing application/domain boundaries. The i18n core must not import UI modules.
2. Keep stable semantic keys in structured JSON catalogs. English and German keys and named placeholders must be parity-checked.
3. Use explicit `en`, `de`, and `system` preference values. Store the preference in app settings, not in each musical project.
4. Ensure missing keys and malformed catalogs fail CI. Runtime fallback must be deterministic and diagnosable; it must not convert a missing translation into an apparent success.
5. Change language at runtime only if all open views can refresh reliably. Otherwise, state clearly that restart is required and preserve the unsaved work state.
6. Route CLI/help output through the same language contract where it is user-facing. Keep machine-readable output, file formats, API names, and standard identifiers language-neutral.
7. Test Unicode, German diacritics, non-ASCII symbols, multiline content, punctuation, and string expansion. Do not use translation text as a command, file path, or serialized identifier.

### Knowledge content is not a UI string

A localized UI label and a translated music-theory claim are different data. For learning content, preserve the identity and source provenance of the underlying claim, while tracking each language version with an explicit locale and content revision. A translation needs its own linguistic review; any change affecting the musical meaning also needs domain review. An approved English claim does not automatically approve a German translation, and vice versa. Historical source quotations remain in their original language and are not replaced by machine translation.

## Verification gates

| Gate | Required check |
|---|---|
| Catalog integrity | Both catalogs parse; required keys are non-empty; key sets and named placeholders match. |
| Runtime contract | `system` precedence/fallback and explicit `en`/`de` selection are deterministic and tested without Tk. |
| Persistence | Preference survives app restart; legacy/missing settings use the documented `system` default; project files remain unchanged. |
| UI completeness | A maintained inventory or extraction-based gate detects visible hard-coded user text in the release surface; dialogs, errors, menus, accessibility labels, and CLI are included. |
| Runtime switching | Every open screen refreshes, or documented restart behavior is shown; no data loss or chord reinterpretation occurs. |
| Musical independence | With identical project bytes and `INT`/`DE` notation preference, switching UI language changes no project values, spelling, or MIDI output. |
| Knowledge review | Locale/revision/provenance and domain/translation review states are independently validated. |
| Platform behavior | Language detection, resource packaging, persistence, and Unicode tests run on each supported OS; native visual and assistive-technology checks are separately recorded. |

## Implementation sequence

1. Issue #154 specifies the independent UI-language and notation contract; keep the still-open 1.0 product and support-platform decisions separate.
2. The current branch implements and tests a Tkinter-free resolver/catalog API and preference persistence.
3. Initial English/German catalogs and the current desktop/CLI text surface are migrated; human translation review and a maintained surface inventory remain required.
4. Runtime window refresh and automated notation independence are implemented; verify native dialogs, accessibility, and data/MIDI invariance on supported platforms.
5. Add content localization metadata only when a specific reviewed learning-content translation is needed; no knowledge claims change in the current branch.
6. Locale catalogs, application code, design tokens, and brand assets are included in the wheel; validate installed artifacts and supported platforms in CI before declaring package acceptance.

The resolver, settings integration, initial catalog migration, and runtime switching are implemented on this branch. Translation review, native/accessibility acceptance, full supported-platform verification, and release sign-off remain open under [issue #154](https://github.com/n05a-design/steps/issues/154).

## References

- [STEPS product target and readiness](../product/V1.0.0_PRODUCT_CONTRACT.md)
- [Music-domain and MIDI contracts](MUSIC_DOMAIN_AND_MIDI.md)
- [Project storage and portability](DATA_STORAGE_AND_PORTABILITY.md)
- [Glide reuse boundaries](../system_reuse/GLIDE.md)
- [Glide i18n PR #134](https://github.com/n05a-design/glide-to-do/pull/134), [follow-up PR #137](https://github.com/n05a-design/glide-to-do/pull/137)

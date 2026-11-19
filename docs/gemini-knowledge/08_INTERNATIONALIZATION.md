# Internationalization and Notation Independence

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED / TESTED for resolver, catalogs, preference and runtime switching; PARTIAL for human translation and native acceptance.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## UI language

`app/i18n.py` and `app/locales/en.json`, `de.json` implement English and German UI catalogs. The preference contract supports `system`, `en`, and `de`; supported system locale resolution and English fallback are described in `docs/engineering/INTERNATIONALIZATION.md`. Desktop runtime switching and CLI `--language` are implemented.

## Musical notation is a separate setting

UI locale must never set or mutate musical notation. In `DE`, `H` means B natural and `B` means B-flat; in `INT`, `B` means B natural and `Bb` means B-flat. An English interface can use German notation and a German interface can use international notation. Preserve spelling, pitch, project values, source text and MIDI behavior when changing UI language.

## Status and required checks

Automated catalog parity, placeholder, persistence, runtime, CLI and notation-independence checks exist in `tests/test_i18n.py`, `tests/test_cli_i18n_inventory.py`, and `scripts/check_ui_text_inventory.py` / `check_cli_text_inventory.py`. Independent human translation review and native-platform/accessibility acceptance remain PARTIAL or NOT_EVIDENCED. A test passing does not certify translation quality.

## Maintenance

Any new visible UI/CLI text must follow the existing catalog contract; do not add a competing translation layer. Check both locales and keep machine identifiers language-neutral. Reviewed knowledge translations require separate linguistic and domain review. See `docs/governance/CONTINUOUS_MAINTENANCE.md`.

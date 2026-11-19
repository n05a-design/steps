# Design and Branding

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** IMPLEMENTED — STEPS-specific design files and app assets exist; comprehensive visual/accessibility acceptance is PARTIAL.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

## Existing design resources

- `design/brand/Logo_Steps-01.svg`, `Logo_Steps-02.svg`, `Logo_Steps-03.svg`
- `design/tokens/tokens.json`
- `design/assets/project-page-pilot-voicings.svg`
- `app/assets/brand/` application icon/logo exports
- `app/brand.py` asset references

The `design/README.md` identifies brand, assets, tokens, components, wireframes, and external references. The interface itself is a Tkinter prototype in `app/ui/`.

## Brand boundary

[ADR-004](../../decisions/ADR-004-lizenz-und-marke.md) keeps the code under MPL-2.0, plans CC BY 4.0 for project-owned knowledge data, preserves third-party rights by asset, and calls for STEPS-owned brand assets. This is not a trademark clearance: the STEPS name remains subject to a separate brand/name review.

## Do not assume reuse rights

Design inspiration from Glide or other products does not grant permission to copy a logo, font, screenshot, code or asset. Validate source and license for each third-party resource before bundling. Never infer that a folder README proves the asset inventory is complete.

## Open acceptance

Contrast, scaling, high DPI, dark/system themes, keyboard focus, accessible names, visual polish and native rendering require manual review on supported platforms. Automated token/asset checks are useful but do not establish accessibility or user acceptance. See `docs/product/LEARNING_AND_EXPERIENCE.md` and `docs/quality/VERIFICATION_PLAN_V2.md`.

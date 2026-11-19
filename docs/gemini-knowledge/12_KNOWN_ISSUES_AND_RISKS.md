# Known Issues, Gaps, and Risks

**Baseline commit:** `00f4d5b9079575260c9f26d6d0f3305ab15e241a`
**Audit date:** 2026-11-19
**Status:** PARTIAL — material risks are documented; this file is not a complete defect or security audit.
**Status key:** IMPLEMENTED = exists; TESTED = automated evidence; PARTIAL = incomplete; PLANNED = future; BLOCKED = decision or dependency; HISTORICAL = dated state; NOT_EVIDENCED = insufficient evidence.

| Risk / question | Status | Why it matters / next evidence |
|---|---|---|
| 1.0 scope and date | BLOCKED | No accepted 1.0 ADR or schedule; owner decision needed |
| Native platform and accessibility quality | NOT_EVIDENCED | CI smoke is not human OS/screen-reader review |
| Independent DAW interoperability | NOT_EVIDENCED | Automated SMF tests do not prove behavior in external DAWs |
| Translation quality | PARTIAL | Catalog/test coverage exists, but human translation review remains |
| Music theory coverage | PARTIAL | Deterministic code and approved examples cover selected cases, not every school or style |
| Public source/asset rights | BLOCKED / PARTIAL | Repository license does not grant rights to every third-party file; per-file review is required |
| Knowledge completeness | PARTIAL | Reviewed pilot content is not a fully curated corpus or general retrieval system |
| Distribution/installers | NOT_EVIDENCED | Python wheel tests are not signed desktop installer acceptance |
| Learning/product-market outcomes | NOT_EVIDENCED | No user study result is established here |
| Research archive reliability | HISTORICAL / source-bound | V6.6/V6.7 labels are archive revisions, not product version or test coverage |

## Risk handling

Do not delete or rewrite historical material to make a status look clean. Flag uncertainty in `research/gaps/` and preserve source identity. For suspected rights or security issues, follow `SECURITY.md`, `docs/governance/RIGHTS_SECURITY_AND_RELEASE.md`, and project governance; do not make unsupported legal claims.

## Open musical questions

Confirm theory framework and style assumptions for any analysis; preserve alternative readings. Check chord-symbol forms and notation convention explicitly. The current engine's supported grammar and behavior are narrower than all real-world harmony. Do not invent supported APIs or imply that a research concept is implemented.

## References

- `docs/project/CONFLICTS_AND_GAPS.md`
- `research/gaps/OPEN_GAPS.md`
- `docs/quality/RISK_REGISTER.md`
- `SECURITY.md`

# Wiki Publication Manifest

**Status:** OWNER_ACTION_REQUIRED. GitHub Wiki support is enabled, but no initialized
`n05a-design/steps.wiki` repository was observed.

## Required source pages

Only exact approved source commits may populate the wiki:

| Source | Destination | Locale | Publication state |
|---|---|---|---|
| `README.md` | `Home` | EN | DRAFT |
| `docs/product/V1.0.0_PRODUCT_CONTRACT.md` | `Product-Target-and-Readiness` | EN | DRAFT |
| `docs/IMPLEMENTATION.md` | `Implementation-Status` | EN/DE summary | DRAFT |
| `knowledge/README.md` | `Knowledge-Base` | EN | DRAFT |
| `SECURITY.md` | `Security` | EN | DRAFT |

## Initialization and publication gate

1. The repository owner initializes the Wiki.
2. The owner approves source pages and destination names.
3. A trusted post-merge workflow creates a dry-run diff.
4. Manual changes on the Wiki are detected and block overwrite.
5. The publication workflow records source commit and destination result.

No research claim or copyrighted source excerpt may be published without its existing
source, rights, domain-review, and language-review states.

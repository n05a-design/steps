# STEPS Verification Results

**Baseline:** `4eca71a347517cb11adcf8090c6be987597a2fa0`
**Environment:** macOS 27.2.1, Python 3.14.5

## Passed commands

| Command | Exit | Result |
|---|---:|---|
| `python3 -B -m unittest discover -s tests -p 'test_*.py' -q` | 0 | 746 tests passed |
| `python3 -B -m unittest discover -s .agents/skills/steps-knowledge-curation/tests -q` | 0 | 40 tests passed |
| `python3 -B scripts/run_knowledge_benchmark.py --scope pilot` | 0 | 8/8 passed |
| `python3 -B scripts/audit_knowledge_coverage.py --check` | 0 | Coverage inventory/check passed |
| `python3 -B scripts/check_documentation_consistency.py --check` | 0 | Documentation consistency passed at `dd1f0b...` |
| `python3 -B scripts/check_gemini_knowledge_pack.py --check` | 0 | 23 mandatory files found |
| `python3 -B scripts/check_ui_text_inventory.py --check` | 0 | No literal active widget/dialog text found |
| `python3 -B scripts/check_cli_text_inventory.py --check` | 0 | CLI text routes through i18n |

## Blocked command

| Command | Exit | Result |
|---|---:|---|
| `python3 -B scripts/run_knowledge_benchmark.py --scope all` | 1 | `PASS 92 · FAIL 0 · PENDING 27` |

The exit code reflects open mandatory cases, not failed benchmark calculations. It is not evidence that the 27 cases passed.

## CI evidence

PR #187 showed successful CI checks, and `origin/main` live Actions for merge commit `4eca71a...` included:

- Python wheel artifact
- Unit tests for Python 3.11–3.14
- Desktop UI smoke for macOS, Ubuntu/Xvfb, and Windows
- Curation skill
- Pilot publication gate
- Knowledge coverage inventory
- Documentation/repository structure/secret guardrails

## Not run or owner-dependent

- External DAW import/export proof
- Human music-theory acceptance of all 27 pending cases
- Native signed/notarized installers
- Real graphical human accessibility/UX acceptance
- Owner live verification of wiki, Discussions, Projects, and Funding settings

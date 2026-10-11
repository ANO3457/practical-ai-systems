# Changelog

## Unreleased

### Contributor experience
- Per-system `system.json` manifests replace hard-coded registries, so new systems never conflict with each other in a central list.
- `scripts/check_systems.py` enforces the contribution contract (required files, standalone stdlib-only imports, zero-dependency web apps, README sections, no scaffold placeholders) with fix-it messages.
- `scripts/new_system.py` and `templates/system/` scaffold a new system (Python + web app) that passes tests out of the box.
- `Makefile` with `check`, `test`, `eval`, `readme`, `web-test`, `serve`, `new`, `clean` targets; `--only` flag for single-system evaluation.
- CI now tests Python 3.10/3.12/3.13 and builds/tests every changed web app; clearer failure annotations.
- GitHub Pages gallery of all 30 web apps (`scripts/build_site.py`, `.github/workflows/pages.yml`).
- Added CODE_OF_CONDUCT, SECURITY, CODEOWNERS, Dependabot, failing-case issue template, issue config, refreshed PR template, `docs/ADDING_A_SYSTEM.md`, and a "first PR in 10 minutes" CONTRIBUTING section.

### Fixes
- `pii_redactor`: phone numbers with a parenthesized area code left a stray `(` after redaction (Python and web), now covered by regression tests.
- `voice_eval` and `mcp_kb` now load fixtures from `eval/cases.json` like every other system.
- Removed four empty placeholder system folders.

### Systems
- Expanded the runnable system catalog from 10 to 30: 10 Beginner, 10 Intermediate, and 10 Advanced projects, each with its own code, synthetic evaluation fixtures, tests, and README.
- Added ten offline-first runnable prototypes with synthetic regression evaluations, tests, and scoped limitations.
- Added shared lexical retrieval, metric, and optional model-provider interfaces.
- Added contribution templates and CI evaluation reproducibility checks.

## 0.1.0 — planned

Initial public systems release. Tag only after all thirty systems meet the launch checklist in `docs/releases/0.1.0.md`.

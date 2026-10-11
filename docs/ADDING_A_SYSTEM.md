# Adding a new system

This walkthrough takes a new system from idea to merged PR. Budget 1–3 hours. Open a **System request** issue first so scope is agreed before you build.

## 1. Pick a good system

A good system here:

- teaches **one** practical AI-engineering idea (retrieval, extraction, guardrails, evaluation, routing…);
- runs **offline** with the Python standard library — no model download, no API key;
- has an **observable** success/failure you can score on 4–25 synthetic cases;
- has an honest, specific **failure mode** worth writing down.

Check the [existing 30 systems](../README.md#projects-by-experience-level) to avoid duplicates.

## 2. Scaffold

```bash
python3 scripts/new_system.py keyword_extractor \
  --title "Keyword extractor" \
  --level Beginner \
  --hook "Pull the most distinctive words out of a short document with TF-IDF." \
  --prerequisites "Basic Python and word counts."
```

This creates `systems/keyword_extractor/` with a working placeholder: Python app, evaluation, tests, README, `system.json`, and a TypeScript web app. Everything passes except `scripts/check_systems.py`, which flags the placeholders you must replace. That's intentional.

## 3. Implement

| File | What to do |
|---|---|
| `app.py` | Replace `run()` with your logic. Standard library only. Keep a CLI in `main()`. |
| `eval/cases.json` | Write synthetic cases, including at least one the system gets **wrong** or abstains on. |
| `evaluate.py` | Return `{"cases": N, "<metric>": value, ..., "scope": "..."}`. |
| `test_<name>.py` | Unit tests for behavior and edge cases (empty input, ties, malformed data). |
| `README.md` | Quickstart command that actually runs, results pointer, concrete known limitations. |
| `system.json` | Adjust `level`/`order` if needed. `order` controls position within the level. |
| `web/src/app.ts` | Port `app.py` 1:1. Same cases in `EVAL_CASES`. |
| `web/src/app.test.ts` | Mirror the Python tests. |
| `web/index.html` | Inputs for your system, a "Known limitations" section, labelled form controls. |

## 4. Verify

```bash
make test SYSTEM=keyword_extractor
make eval SYSTEM=keyword_extractor      # writes eval/results.json
make readme                              # adds your system to the README index
make web-test SYSTEM=keyword_extractor
make check                               # everything CI runs
```

## 5. Open the PR

Commit `system.json`, the code, `eval/cases.json`, the generated `eval/results.json`, and the README diff. Fill in the PR template. CI tests Python on 3.10–3.13 and builds/tests your web app.

## Checklist the contract enforces

- [ ] snake_case folder name; all required files present
- [ ] no imports from `common/`, other systems, or third-party packages
- [ ] web app has no runtime `dependencies` and only `./` or `node:` imports
- [ ] README has `## Quickstart` and `## Known limitations`
- [ ] no leftover scaffold placeholders (`TODO`, etc.)
- [ ] committed `eval/results.json` matches a fresh run

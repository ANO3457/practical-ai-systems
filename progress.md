# Progress log

## 2026-10-05 — Decision paths
- Added declarative learning paths over the existing catalog, recipes, and lexical baseline.
- Added validation for project IDs, local links, and generated output.

## 2026-10-05 — Product plan
- Defined the repository's product direction: original runnable AI systems with evaluations, failure cases, and trade-offs.
- Set phased priorities for the first ten systems, tutorial depth, learning/contribution flow, and sustainable growth.

## 2026-10-06 — First ten system prototypes
- Added ten offline-first systems with per-project code, small synthetic evaluations, result packets, and focused tests.
- Added shared evaluation/provider helpers and CI checks.
- Model downloads were unavailable in the environment, so no model-backed results are claimed.

## 2026-10-07 — README and CI follow-up
- Diagnosed and fixed duplicate `run:` keys in the GitHub Actions workflow; the subsequent Actions run passed.
- Reworked README onboarding around Beginner / Intermediate / Advanced levels and kept project-level caveats visible.
- Reframed the public product description around this repository's own runnable-system concept.

## 2026-10-11 — Grew to 10 systems per level
- Added 20 new offline-first systems (7 Beginner, 7 Intermediate, 6 Advanced) to reach 10 per level / 30 total, each with its own code, synthetic eval fixtures, focused tests, and README.
- New Beginner: extractive summarizer, near-duplicate question detector, PII redactor, lexicon sentiment classifier, readability scorer, FAQ intent router, CSV schema validator.
- New Intermediate: synonym query rewriter, prompt-injection scanner, cost/latency guardrail tracker, post-OCR table extractor, caption QC, RAG citation checker, schema drift detector.
- New Advanced: multi-agent triage handoff, retrieval evaluation harness (recall@k/MRR/nDCG), canary rollout simulator, adversarial red-team harness against the bounded agent, trace anomaly detector, multi-hop reasoning router.
- Registered every new system in `scripts/evaluate_systems.py` and `scripts/render_systems.py`; regenerated `eval/results.json` for all 30 systems and the README's experience-level index.
- Full suite green: 104 systems-level tests, 33 top-level tests (catalog/paths/systems), 4 example tests, `build_catalog.py`, `render_systems.py`, and `evaluate_systems.py --check` all pass with no stale generated views.

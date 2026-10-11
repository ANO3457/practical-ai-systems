# Security policy

## Scope

The systems in this repository are **teaching examples**. Several (for example `pii_redactor`, `prompt_injection_detector`, `repo_guard`, `redteam_harness`) intentionally demonstrate simple heuristics *and document how they fail*. A heuristic missing an attack is usually a **known limitation**, not a vulnerability. Please open a normal issue or PR that adds the failing case to `eval/cases.json`, which is a great contribution.

Report privately if you find:

- a committed secret, credential, or real personal data;
- a way for repository tooling or CI (scripts, workflows, web servers) to execute untrusted code or leak data;
- a dependency or workflow supply-chain issue.

## How to report

Use GitHub's [private vulnerability reporting](https://github.com/shivamnegi92/practical-ai-systems/security/advisories/new). Please do not open a public issue for these. Expect an acknowledgement within 7 days.

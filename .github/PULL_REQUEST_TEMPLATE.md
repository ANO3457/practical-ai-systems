## What changed and why?

<!-- One or two sentences. Link the issue if there is one; an issue is optional for small changes. -->

**Maintainer review is required before merge.** Passing CI does not guarantee acceptance.


## Type
- [ ] Docs / typo
- [ ] New or changed eval cases
- [ ] Bug fix in an existing system
- [ ] Web app change
- [ ] New system
- [ ] Tooling / CI

## Checks
- [ ] `make check` passes locally (or the equivalent commands in CONTRIBUTING.md)
- [ ] `make web-test SYSTEM=<name>` passes for any web app I touched
- [ ] Python `app.py` and `web/src/app.ts` stay in sync if I changed behavior
- [ ] Synthetic or clearly licensed data only; no secrets, personal, or employer-confidential material
- [ ] `eval/results.json` regenerated (`make eval`) and result claims match the measured scope
- [ ] Known limitations updated if I found or introduced a failure mode
- [ ] No generated `node_modules/` or build output is included
- [ ] Web `package.json` changes include matching lockfile changes

# One-command workflows for contributors. Only needs python3 (and node for web targets).
PY ?= python3
SYSTEM ?=

.PHONY: help check test eval readme web-test new serve clean

help: ## Show available commands
	@grep -E '^[a-z-]+:.*## ' $(MAKEFILE_LIST) | awk 'BEGIN{FS=":.*## "}{printf "  make %-10s %s\n", $$1, $$2}'

check: ## Run everything CI runs (except web tests)
	$(PY) scripts/check_systems.py
	$(PY) scripts/build_catalog.py
	$(PY) -m unittest discover -s common -t .
	$(PY) -m unittest discover -s systems -p 'test_*.py'
	$(PY) -m unittest discover -s tests
	$(PY) -m unittest discover -s examples -p 'test_*.py'
	$(PY) scripts/evaluate_systems.py --check
	$(PY) scripts/render_systems.py
	git diff --check

test: ## Unit tests for one system: make test SYSTEM=doc_qa (or all systems)
ifeq ($(SYSTEM),)
	$(PY) -m unittest discover -s systems -p 'test_*.py'
else
	$(PY) -m unittest discover -s systems/$(SYSTEM) -t . -v
endif

eval: ## Regenerate eval/results.json: make eval SYSTEM=doc_qa (or all)
	$(PY) scripts/evaluate_systems.py --check --write $(if $(SYSTEM),--only $(SYSTEM),)

readme: ## Regenerate the README project index from system.json manifests
	$(PY) scripts/render_systems.py --write

web-test: ## Build + test web apps: make web-test SYSTEM=doc_qa (or all)
	@for d in $(if $(SYSTEM),systems/$(SYSTEM)/web,systems/*/web); do \
		echo "== $$d"; (cd $$d && npm install --silent --no-audit --no-fund && npm test --silent) || exit 1; \
	done

serve: ## Run one web app: make serve SYSTEM=doc_qa
	@test -n "$(SYSTEM)" || (echo "usage: make serve SYSTEM=<name>" && exit 1)
	cd systems/$(SYSTEM)/web && npm install --silent && npm start

new: ## Scaffold a system: make new SYSTEM=my_system (prompts are flags, see scripts/new_system.py)
	@test -n "$(SYSTEM)" || (echo "usage: make new SYSTEM=<snake_case_name>" && exit 1)
	$(PY) scripts/new_system.py $(SYSTEM) --title "$(SYSTEM)" --level Beginner \
		--hook "Describe what learners build." --prerequisites "Basic Python."

clean: ## Remove build artifacts
	find . -name __pycache__ -type d -prune -exec rm -rf {} +
	find systems -path '*/web/dist' -type d -prune -exec rm -rf {} +

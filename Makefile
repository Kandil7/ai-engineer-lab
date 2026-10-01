# Full-Stack AI Engineer Lab — task runner
#
# Works in Git Bash on Windows and on Linux CI. PowerShell-only operations stay in
# infra/scripts/*.ps1; see MAKEFILE.md for the full command reference.
#
# Primary target: `make ci` — the same gates GitHub Actions runs.

DEVMATE   := projects/04-ai-engineering/devmate
COMPOSE   := docker compose -f infra/docker/docker-compose.yml

# Run tools from DevMate's venv (works on Windows Git Bash and Linux CI).
# Poetry has no lockfile here and is not the environment of record.
ifeq ($(OS),Windows_NT)
PY        := cd $(DEVMATE) && .venv/Scripts/python
PSH       := powershell
else
PY        := cd $(DEVMATE) && .venv/bin/python
PSH       := pwsh
endif

.DEFAULT_GOAL := help
.PHONY: help ci lint fmt fmt-check types test test-int eval run cli \
        up up-tools down reset ps logs validate docs-check fresh-check clean

## ---------------------------------------------------------------- help

help:  ## Show available targets
	@grep -hE '^[a-zA-Z_-]+:.*?##' $(MAKEFILE_LIST) \
	  | awk 'BEGIN {FS = ":.*?## "}; {printf "  \033[36m%-14s\033[0m %s\n", $$1, $$2}'

## ---------------------------------------------------------------- quality

ci: lint fmt-check types test docs-check fresh-check  ## Everything CI runs
	@echo "CI passed."

lint:  ## Lint DevMate (ruff)
	$(PY) -m ruff check .

fmt:  ## Format DevMate in place
	$(PY) -m ruff format .

fmt-check:  ## Verify formatting without writing
	$(PY) -m ruff format --check .

types:  ## Type-check DevMate (mypy)
	$(PY) -m mypy src/

test:  ## Unit tests with coverage
	$(PY) -m pytest -q --cov=devmate --cov-report=term-missing

test-int:  ## Integration tests (needs `make up`)
	$(PY) -m pytest -q -m integration

## ---------------------------------------------------------------- devmate

eval:  ## Run the RAG evaluation harness (offline by default)
	@test -f $(DEVMATE)/src/devmate/eval/run_ragas.py || { echo "eval harness missing: expected src/devmate/eval/run_ragas.py"; exit 1; }
	$(PY) -m devmate.eval.run_ragas

run:  ## Serve the DevMate API locally
	$(PY) -m uvicorn devmate.api.main:app --reload

cli:  ## Run the DevMate CLI — make cli ARGS="stats ."
	$(PY) -m devmate.cli.main $(ARGS)

## ---------------------------------------------------------------- infra

up:  ## Start Postgres, Redis, Qdrant
	$(COMPOSE) up -d

up-tools:  ## Start infra plus PgAdmin / Redis Commander
	$(COMPOSE) --profile dev-tools up -d

down:  ## Stop containers, keep volumes
	$(COMPOSE) down

reset:  ## Stop containers AND delete all data
	$(COMPOSE) down -v

ps:  ## Container status
	$(COMPOSE) ps

logs:  ## Follow logs — make logs SVC=qdrant
	$(COMPOSE) logs -f $(SVC)

## ---------------------------------------------------------------- workspace

validate:  ## Run the 5 .ai registry validator suites (PowerShell)
	$(PSH) -NoProfile -ExecutionPolicy Bypass -File tests/prompts/validate.ps1
	$(PSH) -NoProfile -ExecutionPolicy Bypass -File tests/workflows/validate.ps1
	$(PSH) -NoProfile -ExecutionPolicy Bypass -File tests/templates/validate.ps1
	$(PSH) -NoProfile -ExecutionPolicy Bypass -File tests/registries/validate.ps1
	$(PSH) -NoProfile -ExecutionPolicy Bypass -File tests/repo-structure/validate.ps1

docs-check:  ## Find broken relative links in docs/
	@fail=0; \
	for f in $$(find docs -name '*.md' -not -path 'docs/plan/archive/*'); do \
	  d=$$(dirname "$$f"); \
	  for l in $$(grep -oE '\]\([^)#][^)]*\.md[^)]*\)' "$$f" 2>/dev/null \
	      | sed -E 's/^\]\(//; s/\)$$//; s/#.*$$//'); do \
	    case "$$l" in http*) continue ;; esac; \
	    [ -f "$$d/$$l" ] || { echo "BROKEN  $$f -> $$l"; fail=1; }; \
	  done; \
	done; \
	[ $$fail -eq 0 ] && echo "docs links OK" || exit 1

fresh-check:  ## Fail if current-focus.md is older than 8 days
	@f=docs/tracking/current-focus.md; \
	s=$$(grep -oE '[0-9]{4}-[0-9]{2}-[0-9]{2}' "$$f" | head -1); \
	a=$$(( ( $$(date +%s) - $$(date -d "$$s" +%s) ) / 86400 )); \
	echo "current-focus.md: $$a day(s) old (stamped $$s)"; \
	[ $$a -le 8 ] || { echo "STALE — update it (weekly review)"; exit 1; }

clean:  ## Remove caches and build artifacts
	find . -type d -name __pycache__ -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .pytest_cache -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .mypy_cache -prune -exec rm -rf {} + 2>/dev/null || true
	find . -type d -name .ruff_cache -prune -exec rm -rf {} + 2>/dev/null || true
	@echo "cleaned."

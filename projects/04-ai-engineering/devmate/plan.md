# Plan: DevMate — A1 (CI green + `devmate stats` CLI)

- **Owner:** Project Planner mode (retrospective, written 2026-09-26)
- **Date:** 2026-09-26
- **Status:** In Progress
- **Project path:** `projects/04-ai-engineering/devmate`

## Goal

Ship milestone A1: a green CI pipeline and a working `devmate stats` command, as the
foundation for the A2 LLM layer. This plan is written retrospectively — the scaffold
exists — to record what is done, what was repaired, and what remains.

## MVP First

- MVP scope:
  - `devmate stats <path>` prints repository statistics (verified working 2026-09-26)
  - `make ci` equivalent gates pass: ruff, ruff format, mypy, pytest
  - Packaging ships all 13 subpackages; `import devmate.db` works
  - Dockerfile installs the app, not just its dependencies
- Explicitly deferred (Later):
  - LLM layer streaming/traced/costed (A2), RAG eval harness (A3), deployment (A4)
  - `eval/run_ragas.py`, `devmate/eval/` package, integration tests against live services
  - Stats-command unit tests, API/agent/guard/retrieve test coverage

## Task Breakdown

| # | Task | Est. (min) | Depends on | Status |
| - | ---- | ---------- | ---------- | ------ |
| 1 | Add missing `__init__.py` to 10 subpackages; verify wheel contents | 30 | — | done |
| 2 | Fix `db/models.py` reserved `metadata` columns; add regression tests | 60 | — | done |
| 3 | Rewrite Dockerfile builder stage (`pip install .`, drop poetry export) | 45 | 1 | done |
| 4 | Push to `master`, confirm GitHub Actions green (devmate + workspace jobs) | 15 | 1–3 | todo |
| 5 | Write stats-command unit tests (`tests/unit/test_cli_stats.py`) | 60 | — | done |
| 6 | Repair legacy Tier 0 backlog R1–R7 + R9 | 240 | — | todo |

## Proposed File Structure

```text
src/
  devmate/
    agent/ api/ cache/ cli/ db/ guards/ index/ ingest/ llm/ mcp/ obs/ retrieve/
    __init__.py  config.py          # every subpackage now has __init__.py
tests/
  unit/
    test_chunker.py  test_cost.py  test_repo_reader.py  test_db_models.py
    test_cli_stats.py               # to be added (task 5)
docker/
  Dockerfile                        # pip-install builder stage
```

## Risks & Blockers

- Risk: `make` is not installed on this machine, so `make ci` cannot run locally.
- Mitigation: run the underlying commands directly (venv python + `powershell -File tests/*/validate.ps1`); documented in `docs/tracking/current-focus.md`.
- Risk: no lockfile — CI resolves fresh on every run.
- Resolved 2026-10-06: `uv.lock` committed (166 packages); CI installs with
  `uv sync --locked --extra dev` and runs the gate via `uv run --frozen`.
  `uv audit` runs advisory (scoped to main + dev; eval/agents findings and
  the python-jose CVEs tracked in current-focus.md).

## Open Questions

- None for A1 scope. A2 will decide the Claude API key story for local dev.

## Acceptance Criteria

- [x] `devmate stats <path>` prints correct statistics
- [x] ruff, ruff format, mypy, pytest pass locally
- [x] Wheel contains all 13 packages; `import devmate.db` succeeds
- [x] GitHub Actions green on `master` (run 36269637267, 2026-09-26)
- [x] Stats command has unit tests (4 tests in `tests/unit/test_cli_stats.py`, passing 2026-09-26)

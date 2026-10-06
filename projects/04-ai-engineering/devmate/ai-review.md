# Code Review: DevMate scaffold (all modules, pre-A2)

> **Addendum 2026-10-06** — findings closed since the review, without rewriting
> the original: the JWT `secret_key` default now fails startup under
> `APP_ENV=production` (`config.py` model validator, verified raising);
> `debug` defaults to `False`; `class Config` migrated to `ConfigDict`;
> the bottom `pathlib` import moved up with the bogus comment dropped;
> all 11 `datetime.utcnow()` sites use `datetime.now(UTC)`;
> `python-jose` + `passlib` removed as dead deps (imported nowhere), which
> cleared the rsa/ecdsa CVEs and adverse statuses — `uv audit` gates in CI
> with zero findings; qdrant bumped to 1.12.2 (CVE-2024-3829 fixed, `.search()`
> signature verified). mypy stays at 3.12: numpy 2.5.3 stubs are unparsable
> under a 3.11 target (documented in pyproject). Still open: function-length
> splits, API/agent test coverage, Docker image build.

- **Reviewer:** Code Reviewer mode
- **Date:** 2026-09-26
- **Project path:** `projects/04-ai-engineering/devmate`
- **Scope reviewed:** `src/devmate/` (21 files), `tests/unit/`, `pyproject.toml`, `docker/Dockerfile`
- **Overall score:** 6/10

> Reviewer does **not** rewrite code by default — findings only, with exact file references.
> Two High findings below were fixed during this review (packaging, DB import);
> they are recorded as resolved with their regression evidence.

## Findings by Severity

### Critical

- None open. (The `devmate.db` import crash and the wheel-packaging gap were
  Critical/High and are now fixed — see resolved items.)

### High

- [x] **`src/devmate/db/models.py:46` (was)** — Five models declared a column named
  `metadata`, reserved on the SQLAlchemy Declarative API. `import devmate.db` raised
  `InvalidRequestError` at import time. · _Why:_ every consumer of the DB layer (API,
  agent, MCP) was dead on arrival. · _Fix:_ renamed the attribute to `meta` with
  `mapped_column(JSONB, name="metadata")`; column name preserved; 4 constructor call
  sites updated. · _Regression:_ `tests/unit/test_db_models.py` (4 tests, passing).
- [x] **`src/devmate/*/ ` (was)** — 10 of 13 subpackages lacked `__init__.py`, so
  `find_packages` resolved 3 packages and any built wheel omitted the API, CLI, agent,
  and retrieval code. · _Why:_ the Docker image and any non-editable install shipped
  a broken artifact. · _Fix:_ added the missing `__init__.py` files; wheel build
  verified to contain all 13 packages.
- [ ] **`src/devmate/config.py:68`** — JWT `secret_key` defaults to a public string.
  · _Why:_ any deployment that forgets `SECRET_KEY` signs tokens with a known key.
  · _Fix:_ fail startup when `app_env` is production and the default is unchanged.
- [ ] **`docker/Dockerfile` (pre-fix state)** — builder ran `poetry export` against a
  PEP 621 file with no `[tool.poetry]`, installed dependencies only, and the runtime
  stage copied `src/` without installing the package. · _Fix applied:_ builder now
  runs `pip install --prefix=/install .`; runtime resolves `devmate` from
  site-packages. · _Remaining:_ image build itself not yet run (needs Docker daemon).

### Medium

- [ ] **Test coverage 47%, 8 modules untested** — agent (645 lines), API (386 lines),
  guardrails, retriever, vector store, embeddings client, MCP server, CLI have zero
  tests. Only chunker, cost, repo reader, and now db models are covered.
  _Fix:_ task 5 (stats tests) first, then API happy-path tests before A2 grows the LLM layer.
- [ ] **13 functions exceed the 50-line limit** — worst: `src/devmate/cli/main.py:38`
  `stats` (115 lines), `src/devmate/agent/agent.py:518` `run` (85 lines),
  `src/devmate/retrieve/rag.py:134` `query` (74 lines). _Fix:_ split `stats` into
  collect/format/present; extract the agent tool-dispatch table.
- [ ] **`src/devmate/config.py:17`** — `debug` defaults to `True`, and
  `api/main.py:381` passes it as uvicorn `reload`. _Fix:_ default `False`; enable
  explicitly in dev (the `make run` path).
- [ ] **`pyproject.toml:88`** — mypy targets `python_version = "3.12"` while CI and
  `requires-python` start at 3.11. _Fix:_ set mypy to 3.11 so the gate matches the
  oldest supported runtime.

### Low

- [ ] **`src/devmate/api/main.py:386`** — `from pathlib import Path` at file bottom
  with a "circular imports" comment; a stdlib import cannot be circular. Move it up,
  drop the comment.
- [ ] **`src/devmate/config.py:101`** — class-based `Config` is deprecated in
  Pydantic v2 (warning on every test run). Migrate to `ConfigDict`.
- [ ] **`datetime.utcnow()`** in `src/devmate/obs/cost.py:115`,
  `src/devmate/db/models.py:447`, and `tests/unit/test_cost.py` — deprecated.
  Use `datetime.now(datetime.UTC)`.

## What's Good

- Ruff, ruff format, and mypy all pass clean on 21 source files; complexity cap
  (C901 ≤ 15) holds.
- Secrets discipline is right: keys come from env, `.env` is gitignored, the scan
  of tracked files found only fake teaching keys.
- CLI surface is coherent (`stats`, `ask`, `ingest`, `serve`, `cost`) and `stats`
  works end to end with JSON output.
- Qdrant client pin documents exactly why (`<1.9`, `.search()` API removal) —
  the kind of comment that prevents a future breakage.

## Checklist

- [x] No hardcoded secrets
- [x] Errors handled explicitly
- [x] Inputs validated at boundaries
- [ ] Functions < 50 lines, files < 800 lines (13 functions over; files OK)
- [ ] Tests exist for new behavior (8 modules untested)

## Approval

- Decision: **Approve with warnings**
- Blocking items: GitHub Actions must go green (task 4); stats tests (task 5) before A2.

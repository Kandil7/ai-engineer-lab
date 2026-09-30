# DevMate — State Audit

> Point-in-time audit of what exists, what works, and what is stubbed. Update at the
> close of each milestone. Companion to `plan.md` (scope) and `ai-review.md` (review
> state).

**Audited:** 2026-09-30

## 1. Package inventory

`src/devmate/` (14 packages):

| Package | Responsibility | State |
| --- | --- | --- |
| `cli/` | Typer CLI: `stats`, `ask`, `ingest`, `serve`, `cost` | working (`stats` verified) |
| `ingest/` | `repo_reader.py` (AST/file walk), `chunker.py` | working |
| `index/` | `embeddings.py`, `vector_store.py` (Qdrant adapter) | working (live Qdrant needed) |
| `retrieve/` | `retriever.py` (hybrid), `rag.py` (pipeline, context budget) | working |
| `llm/` | `client.py` (Anthropic + Ollama, typed errors, tenacity), `schemas.py`, `prompts/` | working; Langfuse keys pending |
| `obs/` | `tracing.py` (Langfuse), `cost.py` (token + $ tracking) | wired; live traces pending |
| `eval/` | `run_ragas.py`, `metrics.py`, `datasets.py`, `validate_prompt_golden.py` | offline harness working (2026-09-30) |
| `agent/` | `agent.py` (tools + ReAct loop) | scaffolded |
| `mcp/` | `server.py` (MCP server) | scaffolded |
| `api/` | `main.py` (FastAPI: `/health`, `/ask` SSE, `/ingest`) | working |
| `db/` | SQLAlchemy models (conversations, messages, eval runs, cost) | working |
| `cache/` | `semantic_cache.py` (Redis) | working |
| `guards/` | `guardrails.py` (input/output) | working |
| `config.py` | pydantic-settings | working |

## 2. Toolchain

- Install: `pip install -e ".[dev]"` from `pyproject.toml` (pip-from-pyproject is the
  environment of record; Poetry not used).
- Gates: ruff, ruff format, mypy, pytest — all pass locally and in CI.
- CI: `.github/workflows/ci.yml` — `devmate` job (lint/types/tests), `workspace` job
  (the five `.ai` validators), `docs` job (links + freshness), advisory `legacy-lint`.

## 3. Tests

`tests/unit/` (7 files): `test_cli_stats.py`, `test_repo_reader.py`, `test_chunker.py`,
`test_cost.py`, `test_db_models.py`, `test_api_sse.py`, `test_rag_context_budget.py`.
`tests/integration/` and `tests/load/` are README placeholders (not yet written).

## 4. Milestones

| Milestone | State | Notes |
| --- | --- | --- |
| A1 CI green + `devmate stats` | **Done** | CI run 36269637267 |
| A2 LLM layer traced and costed | In progress | Ollama path verified; prompt golden cases + offline schema tests done; remaining: Langfuse keys + a live traced `devmate ask` |
| A3 RAG with measured eval + 2 ADRs | In progress | offline `devmate.eval.run_ragas` implemented; golden sets load; offline Hit@5 path = 1.0; live retrieval needs Qdrant + ingest; chunking and vector-store ADRs still open |
| A4+ | Planned | deployment, agents, hardening, portfolio |

## 5. Known gaps (not yet done)

- **Live end-to-end**: no live Qdrant ingest + retrieval run recorded yet under A3.
- **Observability**: Langfuse keys not configured; no live traces.
- **ADRs**: the A3 pair (chunking strategy, Qdrant vs Chroma) still need measured
  numbers.
- **Deployment**: no public URL; no multi-stage image running in compose for the API.
- **Hardening**: cache, guardrails, and fallback exist in code but no measured
  hit-rate / latency / injection-resistance evidence yet (see `docs/failure-modes.md`).
- **`docs/` in this folder**: `failure-modes.md` and `state-audit.md` now exist; keep
  them current.

## 6. Cleanup notes

- A stale `build/lib/` tree duplicates `src/` (setuptools build output); it should be
  removed from the working tree and is not tracked.
- `README.md` links resolve as of this audit (`docs/failure-modes.md`,
  `docs/state-audit.md`).

---

*Created as a state-of-record snapshot. Update the dates and the milestone table as
work lands.*

# Deployment Plan — DevMate A4 (public URL)

- **Owner:** Project Planner mode
- **Date:** 2026-10-11
- **Status:** Config ready — cloud deploy is a dashboard step (Render + Qdrant Cloud); demo-corpus bake-in open
- **Project path:** `projects/04-ai-engineering/devmate/`
- **Milestone:** A4 (weeks 4 / target application 2026-10-12)

## Goal

Ship DevMate to a public URL a recruiter can click: a running API (`/health`, `/ask` SSE,
`/ingest`) backed by Postgres + Redis + Qdrant, with a Streamlit UI and cost/trace observability.

## Current state (FACT — verified 2026-10-11)

| Piece | State |
| --- | --- |
| Multi-stage Dockerfile | Exists: `docker/Dockerfile` (builder + runtime, non-root, healthcheck) |
| API endpoints | Exist: `/health`, `/ready`, `/ask` (SSE), `/ingest`, `/ai/usage`, `/traces` |
| DB models | Exist: `src/devmate/db/models.py` |
| Alembic migrations | **Missing**: `migrations/` is empty |
| Streamlit UI | **Missing**: `ui/` does not exist, so the compose `devmate-ui` service fails |
| Compose stack | Exists: postgres, redis, qdrant, mongodb, langfuse, devmate-api, devmate-mcp, devmate-ui |
| Eval gate + integration tests | Green (Hit@5 >= 1.0, MRR >= 0.70; 3 integration tests pass live) |

## MVP First

- **MVP scope:** deploy the API and the UI to one platform with managed Postgres + Redis and a
  reachable Qdrant; pre-ingest this repo as the corpus; a recruiter opens the UI, asks a
  question, and gets a grounded answer with sources and a cost figure.
- **Explicitly deferred (Later):** MCP server in production; self-hosted Langfuse in production;
  multi-tenant auth; autoscaling; the "most expensive queries" SQL view (do it in the SQL sprint);
  a custom domain.

## Task Breakdown

| # | Task | Est. (min) | Depends on | Status |
| - | ---- | ---------- | ---------- | ------ |
| 1 | Alembic: `alembic.ini`, `migrations/env.py`, initial revision from `db/models.py` | 60 | db models | done |
| 2 | Streamlit UI `ui/app.py`: ask box, sources, cost, ingest trigger | 90 | API | done |
| 2b | Fix compose build context + copy `ui/` + `.dockerignore` so the image builds | 30 | — | done |
| 3 | Platform config: `render.yaml` Blueprint + runbook | 45 | platform decision | done |
| 4 | Provision managed Postgres + Redis (Render Blueprint) | 30 | platform | manual (dashboard) |
| 5 | Qdrant Cloud free cluster; set host/port/key | 45 | platform | manual (dashboard) |
| 6 | Bake a `sample_corpus/` and ingest it on boot | 60 | 4, 5 | todo (open) |
| 7 | Secrets via platform env (Groq, OpenAI, Qdrant) | 20 | 4 | manual (dashboard) |
| 8 | Keep-warm ping or a documented cold-start note | 20 | deploy | manual |
| 9 | Smoke test the public URL: `/health`, one `/ask` | 15 | deploy | manual |

## Proposed File Structure

```text
projects/04-ai-engineering/devmate/
  alembic.ini                                  # new
  migrations/env.py                            # new (async engine)
  migrations/versions/0001_initial.py          # new
  ui/app.py                                    # new
  ui/requirements.txt                          # new (or reuse [dev])
  docker/Dockerfile                            # exists (verify UI CMD)
  deploy/render.yaml  |  deploy/railway.json   # new
  deploy/README.md                             # new (runbook: how to deploy + roll back)
  .env.example                                 # exists; add prod keys
```

## Risks & Blockers

- **Platform lock-in vs speed.** Railway is fastest to stand up; Render gives a free web service
  with managed Postgres/Redis. Decide once; the config differs.
- **Vector store in prod.** Qdrant Cloud free tier is simplest; a self-hosted container needs a
  second service and persistent volume.
- **Cost of a public LLM demo.** A public `/ask` with a real Anthropic key can be abused; add a
  rate limit (already in config) and a budget cap, or use a cheap/offline fallback for the demo.
- **Cold starts.** Free tiers sleep; the README must say so, or add a keep-warm ping.
- **Secrets.** Never commit keys; use platform env vars only.
- **Async Alembic.** The app uses async SQLAlchemy (`asyncpg`); `env.py` must run migrations with
  a sync driver or `run_sync`.

## Open Questions

- **Decided (2026-10-11):** platform = **Render** (Blueprint); vector store =
  **Qdrant Cloud** free cluster; generation = **Groq** (`llama-3.1-8b-instant`);
  embeddings = **OpenAI** (`text-embedding-3-small`, since Groq has no embeddings).
- **Still open:** the demo corpus (task 6) — the prod image has no repository on
  disk, so a small `sample_corpus/` must be baked in and ingested on first boot.
- **Still open:** is the Streamlit UI required for A4, or is the API + a hosted
  README enough? (Assumed yes; the UI is built and boot-verified.)

## Acceptance Criteria

- [ ] `alembic upgrade head` creates the schema; `migrations/versions/0001_initial.py` exists.
- [ ] `ui/app.py` runs and the compose `devmate-ui` service starts without error.
- [ ] The public `/health` returns `{"status":"healthy"}`.
- [ ] A public `/ask` returns a grounded answer with at least one source.
- [ ] The README states the URL, the cost per query, and the cold-start behaviour.

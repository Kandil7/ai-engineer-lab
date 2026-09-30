# Full-Stack AI Engineer Lab

[![Code Intelligence](https://img.shields.io/badge/Structural%20Graph-60%2C751%20nodes%20%2F%20141%2C083%20edges-blue)](docs/CODEBASE-INTELLIGENCE.md)
[![Review Graph](https://img.shields.io/badge/Review%20Graph-11%2C590%20nodes%20%2F%2087%2C721%20edges-green)](docs/CODEBASE-INTELLIGENCE.md)
[![Multimodal Graph](https://img.shields.io/badge/Multimodal%20Graph-49%2C856%20nodes%20%2F%2054%2C483%20edges-purple)](docs/CODEBASE-INTELLIGENCE.md)
[![DevMate Gate](https://img.shields.io/badge/DevMate-42%20tests%20green-brightgreen)](projects/04-ai-engineering/devmate/)
[![Eval Harness](https://img.shields.io/badge/Eval-Offline%20Hit%405%201.0-orange)](projects/04-ai-engineering/devmate/eval/)

A **Repo-Centric Agentic Workspace** — a learning + execution + review operating system for
becoming a production-level AI / Full-Stack AI Engineer. This is not a notes folder; it is an
engineering environment where prompts, templates, workflows, ADRs, reviews, and **running
systems** are versioned engineering artifacts.

> The "agents" here are **prompted operating modes** (markdown under `.ai/`), not runtime
> processes. Orchestration is human-led and workflow-driven.

---

## Where you are right now (2026-09-30)

| Track | Status |
| ----- | ------ |
| **Plan of record** | [Active Track — 10-Week AI Engineer](docs/roadmap/active-track-10-week.md) ([ADR-0004](docs/decisions/0004-adopt-10-week-ai-engineer-track.md)) |
| **Vehicle** | DevMate — `projects/04-ai-engineering/devmate/` |
| **A1** CI + stats CLI | **Done** (GitHub Actions green) |
| **A2** LLM layer | **In progress** — golden cases + offline eval done; Langfuse UI keys + live traced `ask` remain |
| **A3** RAG eval | **In progress** — offline harness shipped; live retrieval + 2 ADRs remain |
| **A4** Public URL | Planned |
| **Strategic follow-on** | [Production AI Systems Engineer roadmap](docs/roadmap/production-ai-systems-engineer.md) — P1–P8, start after A4/A6 |

**Immediate execution window:** [`docs/tracking/current-focus.md`](docs/tracking/current-focus.md)

---

## Target Stack

| Layer | Technology | Live in DevMate? |
| ----- | ---------- | ---------------- |
| AI services | FastAPI / Python (RAG, embeddings, agents, MCP) | **Yes** |
| LLM providers | Anthropic, OpenAI, Ollama (fallback chain) | **Yes** |
| Observability | Langfuse + cost ledger + span tracing | Code yes; UI keys pending |
| Vector DB | Qdrant 1.8.0 (compose pinned) | Compose ready |
| Relational DB | PostgreSQL 16 | Compose ready |
| Cache | Redis 7 | Compose ready |
| Eval | Offline harness (`devmate.eval.run_ragas`) | **Yes** |
| Backend (core) | Go (auth, users, routing) | Deferred (long track) |
| Mobile / Web | Flutter / Next.js | Deferred |
| Infra | Docker / Docker Compose | Compose file present |

---

## Learning Strategy

**Write code yourself first**, then use AI as assistant — not replacement.

- **70% build** / 20% review / 10% theory
- Use AI for: quick explanations, code review, architecture hints, boilerplate
- Don't use AI for: writing entire systems you can't explain
- Every feature flows: `plan → design → build → review → fix → reflect`
- **Golden rule:** if you can't explain the code an hour later, AI wrote it for you, not with you

See [`docs/product/learning-strategy.md`](docs/product/learning-strategy.md) and
[`docs/product/ai-learning-operating-manual.md`](docs/product/ai-learning-operating-manual.md).

---

## Repository Map

```text
.ai/                         # Prompt + workflow system (the "brain")
  prompts/                  # system, roles, tasks, critics, repair
  workflows/                # feature, debugging, learning, architecture, evaluation
templates/                   # Standardized artifact templates
registries/                  # YAML inventories (source of truth for inventory)
docs/
  CODEBASE-INTELLIGENCE.md  # Multi-layer code intelligence
  roadmap/
    active-track-10-week.md # PLAN OF RECORD (A1–A10)
    production-ai-systems-engineer.md  # Strategic P1–P8 follow-on
    milestones.md           # A / P / M milestone IDs
    progress-dashboard.md   # Status snapshot
    skills-matrix.md        # Skill levels with evidence rules
  decisions/                # ADRs 0001–0006
  curriculum/               # 4 lecture + practice modules (DevMate-anchored)
  reference/                # LLM production architecture, checklists, interview bank
  learning/                 # paths, deep-dives, design notes, source-summaries
  tracking/current-focus.md # What to work on RIGHT NOW
  product/                  # goals, learning strategy, operating manual
  architecture/             # overview, monorepo structure, .ai architecture
  cheat-sheets/             # git, docker, postgres, qdrant, prompt-design
evaluations/
  prompts/golden-cases/     # Prompt golden cases + offline answers
  rag/datasets/             # RAG golden set (devmate-golden.jsonl)
  rag/baselines/            # Recorded retrieval top-k for offline eval
  rag/reports/              # Dated eval harness reports
projects/
  00-core-foundations/      # Python / Go / DSA / web curriculum
    python/                 # 10-phase module + SKILLS_MASTERY_MAP + 11 challenge sets
  04-ai-engineering/
    devmate/                # ACTIVE PROJECT — package, tests, eval, docker
      src/devmate/          # llm, retrieve, obs, eval, agent, api, guards, cache, mcp
      eval/README.md        # How to run the harness
      tests/unit/           # Offline unit tests (no API key)
    model-serving/          # Curriculum (serving labs still to build)
    security/               # 10 security modules
  06-devops/                # llmops guide, docker/ci-cd/deployment notes
  07-capstone/              # ThanaweyaGPT scaffold (deferred)
infra/docker/               # compose: postgres, redis, mongo, qdrant, langfuse
tests/                      # Workspace validators (5 suites)
```

See [`docs/architecture/monorepo-structure.md`](docs/architecture/monorepo-structure.md).

---

## DevMate (active system)

An AI assistant for code repositories: ingest a repo, ask questions, get grounded answers
with sources, with cost tracking and traces.

| Capability | Location | State |
| ---------- | -------- | ----- |
| CLI (`stats`, `ask`, `ingest`, `serve`, `cost`) | `src/devmate/cli/main.py` | Working |
| LLM client (streaming, retries, 3 providers, fallback) | `src/devmate/llm/client.py` | Working |
| Cost ledger | `src/devmate/obs/cost.py` | Working (records; budgets later) |
| Span tracing + Langfuse export | `src/devmate/obs/tracing.py` | Code ready; UI keys pending |
| RAG pipeline + hybrid retrieval | `src/devmate/retrieve/`, `src/devmate/index/` | Working offline path |
| Guardrails + semantic cache | `src/devmate/guards/`, `src/devmate/cache/` | Present; hardening is A6 |
| Agent + MCP | `src/devmate/agent/`, `src/devmate/mcp/` | Present; week 5–6 focus |
| Offline eval harness | `src/devmate/eval/` + `evaluations/` | **Shipped 2026-09-30** |

### Verify like CI does

```powershell
cd projects/04-ai-engineering/devmate
& .venv\Scripts\python.exe -m ruff check .
& .venv\Scripts\python.exe -m ruff format --check .
& .venv\Scripts\python.exe -m mypy src/
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m devmate.eval.run_ragas --mode offline
```

Last verified 2026-09-30: ruff 0, format clean, mypy 0, **pytest 52 passed**, offline
eval Hit@5 1.000 on recorded retrieval path (not a live measurement).

---

## Code Intelligence

Four-layer code intelligence for token-efficient engineering:

| Layer | Tool | What it does | Stats (2026-09-30) |
| ----- | ---- | ------------ | ------------------- |
| **Structural Graph** | codebase-memory-mcp | Tree-sitter + LSP call graph | **60,751 nodes, 141,083 edges** |
| **Review Graph** | code-review-graph | PR blast-radius, communities | 11,590 nodes, 87,721 edges |
| **Multimodal Graph** | graphify | Code + docs + schemas | 49,856 nodes, 54,483 edges |
| **Context Pack** | repomix | One-shot repo packing | 1,244,995 tokens, 1,082 files |

**Quick commands:**

```text
Who calls X?        → codebase-memory trace_path --function_name <qn> --direction both
Find by pattern     → codebase-memory search_graph --name_pattern ".*X.*"
Impact of changes   → codebase-memory detect_changes
Blast radius        → code-review-graph detect_changes_tool
God nodes           → graphify god_nodes
Pack for LLM        → repomix pack_codebase
Reindex             → codebase-memory index_repository (full)
```

**Post-reindex call-graph notes (DevMate):**

- `get_rag_pipeline` — 8 callers (API + CLI)
- `RAGPipeline.query` — 5 callers; callees include hybrid search, tracer, LLM complete
- `Tracer.trace` — 47 callers across API, CLI, RAG, agents, guards, eval
- `score_retrieval` / `run_offline` — eval harness edges resolve
- `LLMClient.complete` — inbound CALLS still weak (lazy client); use source for that edge

Full reference: [`docs/CODEBASE-INTELLIGENCE.md`](docs/CODEBASE-INTELLIGENCE.md)

---

## Workflow Rules

1. **Plan before build.** Start every feature at `.ai/workflows/feature/01-plan.md`.
2. **Architecture before large implementation.** System boundaries → ADR or architecture review.
3. **Review before done.** No feature is complete without `ai-review.md`.
4. **Document every bug** in a debugging-session artifact.
5. **Deterministic paths.** Artifacts land where the workflow says.
6. **Registries are source of truth** for prompt/workflow/template inventory.

---

## Daily Loop (5+ hours)

| Block | Time | Activity |
| ----- | ---- | -------- |
| Build | 3h | The week's deliverable — code first |
| Learn | 1h | One topic, docs-first, **after** building it |
| Review | 1h | AI code review + debugging log |
| Recall | 30m | Explain without notes + daily log + plan |

Full cadence: [`docs/WEEKLY_PROTOCOL.md`](docs/WEEKLY_PROTOCOL.md)

---

## Active Plan

**[Active Track — 10-Week AI Engineer](docs/roadmap/active-track-10-week.md)** — adopted
2026-08-02 by [ADR-0004](docs/decisions/0004-adopt-10-week-ai-engineer-track.md).
Target: a remote AI/LLM engineering role. Vehicle: **DevMate**.

> **Governing rule (amended by [ADR-0006](docs/decisions/0006-adopt-master-ai-engineering-curriculum.md)):**
> curriculum content is allowed again when it traces to a DevMate concept or an interview
> answer — never as a substitute for building.

| Week | Milestone | Deliverable | Status (2026-09-30) |
| ---- | --------- | ----------- | ------------------- |
| 0 | A1 | CI green + `devmate stats` CLI | **Done** |
| 1 | A2 | LLM layer — streaming, traced, costed | **In progress** |
| 2–3 | A3 | RAG with a measured eval harness | **In progress** (offline) |
| 4 | A4 | **Deployed at a public URL** + SQL sprint | Planned |
| 5–6 | A5 | Agent with 4 tools + MCP server | Planned |
| 7 | A6 | Cache, guardrails, hardening | Planned |
| 8 | A7 | Portfolio — blog, README, CV | Planned |
| 9–10 | A8, A9 | 40 applications, first interview | Planned |
| 11+ | A10 | Deferred ML sprint | Planned |

**Right now:** [`docs/tracking/current-focus.md`](docs/tracking/current-focus.md) ·
**Status:** [`docs/roadmap/progress-dashboard.md`](docs/roadmap/progress-dashboard.md)

### Other tracks

| Track | Status |
| ----- | ------ |
| [Production AI Systems Engineer](docs/roadmap/production-ai-systems-engineer.md) (P1–P8) | Strategic follow-on after A4/A6 |
| [Phase 2 — Athar & Baligh](docs/roadmap/phase-2-athar-baligh.md) | After A7 |
| [Long track — 12-month roadmap](docs/roadmap/master-roadmap.md) (Go, Flutter/Next.js, ThanaweyaGPT) | Deferred |

---

## Progress

### Workspace Build (Complete)
- [x] Phase 0 — Foundations (repo skeleton, templates, prompts, registries)
- [x] Phase 1 — Core MVP (end-to-end feature on `auth-service`)
- [x] Phase 2 — Reliability (learning workflows, source templates, tests)
- [x] Phase 3 — Scale (scaffolding, repo validation, deep dives)
- [x] Phase 4 — Advanced (curriculum, operating manual, DevMate scaffold)

### Code Intelligence (Current)
- [x] Structural graph reindexed 2026-09-30 — 60,751 nodes / 141,083 edges
- [x] Review graph built — 11,590 nodes / 87,721 edges / 23 communities
- [x] Multimodal graph built — 49,856 nodes / 54,483 edges
- [x] Context pack ready — 1,244,995 tokens / 1,082 files
- [x] Security exercises — 10 modules (directory-per-exercise)
- [x] DevMate call-graph retrace after reindex (RAG/eval/tracer edges resolved)

### Learning + Systems
- [x] Python foundations — large curriculum under `projects/00-core-foundations/python/`
- [x] **Skills mastery map** — the 6 Athar skills mapped to topics + mastery evidence ([SKILLS_MASTERY_MAP.md](projects/00-core-foundations/python/SKILLS_MASTERY_MAP.md))
- [x] **Production Python track** — Unicode/Arabic text, separation of concerns, code review, test strategy (`02-advanced-python/35-38`)
- [x] **System design phase** (`10-system-design/`) — contracts, queues, consistency, failure modes, ADRs
- [x] **Database ops topics** — migrations/Alembic, backup/restore (`04-databases/`)
- [x] **11 challenge sets** (Bronze/Silver/Gold with measured guards) — 186 tests, starter-fails/solution-passes verified
- [x] AI curriculum — lectures + practice under `docs/curriculum/` and `projects/04-ai-engineering/`
- [x] fast.ai Deep Learning track — 13 modules
- [x] **A1 — CI green + `devmate stats` CLI**
- [x] Prompt golden cases + offline schema tests (A2 partial)
- [x] Offline eval harness + unit tests + first report (A3 partial)
- [ ] **A2 remainder — Langfuse keys + live traced `devmate ask`**
- [ ] **A3 remainder — live retrieval + chunking/vector ADRs**
- [ ] A4–A10 — see table above
- [ ] Deferred: Go, frontend, classical ML, P-track production depth

---

## Getting Started

```powershell
# 1. Optional infra (Postgres / Redis / Qdrant / Langfuse)
#    docker compose requires approval on this workstation.
#    Start only what you need, e.g.:
#    docker compose -f infra/docker/docker-compose.yml up -d postgres redis qdrant

# 2. Work on the active project
cd projects/04-ai-engineering/devmate
& .venv\Scripts\python.exe -m pytest -q
& .venv\Scripts\python.exe -m devmate.eval.run_ragas --mode offline

# 3. Create a new ADR
./infra/scripts/new-adr.ps1 "Adopt keyset pagination"

# 4. Start today's log
./infra/scripts/new-daily-log.ps1

# 5. Query code intelligence
#    See docs/CODEBASE-INTELLIGENCE.md
```

**Langfuse (self-hosted, compose service `langfuse`):** langfuse 2.x has no env-based key
seeding. Open `http://localhost:3000`, sign in as documented in
`infra/docker/docker-compose.yml`, create a project, copy keys into
`projects/04-ai-engineering/devmate/.env` as `LANGFUSE_PUBLIC_KEY` / `LANGFUSE_SECRET_KEY`.

---

## Documentation Index

| Document | Role |
| -------- | ---- |
| [`docs/tracking/current-focus.md`](docs/tracking/current-focus.md) | What to do right now |
| [`docs/roadmap/active-track-10-week.md`](docs/roadmap/active-track-10-week.md) | Plan of record |
| [`docs/roadmap/production-ai-systems-engineer.md`](docs/roadmap/production-ai-systems-engineer.md) | Production AI / platform track + gap analysis |
| [`docs/roadmap/milestones.md`](docs/roadmap/milestones.md) | A / P / M milestone IDs |
| [`docs/roadmap/skills-matrix.md`](docs/roadmap/skills-matrix.md) | Skill levels with evidence rules |
| [`docs/roadmap/progress-dashboard.md`](docs/roadmap/progress-dashboard.md) | Status snapshot |
| [`docs/reference/llm-production-architecture.md`](docs/reference/llm-production-architecture.md) | Production LLM systems reference |
| [`projects/00-core-foundations/python/SKILLS_MASTERY_MAP.md`](projects/00-core-foundations/python/SKILLS_MASTERY_MAP.md) | The 6 Athar skills → topics → mastery evidence |
| [`projects/04-ai-engineering/devmate/eval/README.md`](projects/04-ai-engineering/devmate/eval/README.md) | Eval harness usage |
| [`docs/CODEBASE-INTELLIGENCE.md`](docs/CODEBASE-INTELLIGENCE.md) | Graph tools and reindex |
| [`AGENTS.md`](AGENTS.md) | Agent operating rules for this repo |

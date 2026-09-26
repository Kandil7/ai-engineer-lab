# Full-Stack AI Engineer Lab

[![Code Intelligence](https://img.shields.io/badge/Structural%20Graph-53%2C461%20nodes%20%2F%20126%2C790%20edges-blue)](docs/CODEBASE-INTELLIGENCE.md)
[![Review Graph](https://img.shields.io/badge/Review%20Graph-11%2C590%20nodes%20%2F%2087%2C721%20edges-green)](docs/CODEBASE-INTELLIGENCE.md)
[![Multimodal Graph](https://img.shields.io/badge/Multimodal%20Graph-49%2C856%20nodes%20%2F%2054%2C483%20edges-purple)](docs/CODEBASE-INTELLIGENCE.md)

A **Repo-Centric Agentic Workspace** — a learning + execution + review operating system for
becoming a production-level Full-Stack AI Engineer. This is not a notes folder; it is an
engineering environment where prompts, templates, workflows, ADRs, and reviews are
versioned **engineering artifacts**.

> The "agents" here are **prompted operating modes** (markdown under `.ai/`), not runtime
> processes. Orchestration is human-led and workflow-driven.

---

## Target Stack

| Layer            | Technology                                   |
| ---------------- | -------------------------------------------- |
| Backend (core)   | Go (auth, users, routing, billing)           |
| AI services      | FastAPI / Python (RAG, embeddings, agents)   |
| Mobile           | Flutter                                       |
| Web dashboard    | Next.js + TypeScript                          |
| Relational DB    | PostgreSQL                                    |
| Document DB      | MongoDB                                       |
| Cache / sessions | Redis                                         |
| Vector DB        | Qdrant                                        |
| Infra            | Docker / Docker Compose                       |

---

## Learning Strategy

**Write code yourself first**, then use AI as assistant — not replacement.

- **70% build** / 20% review / 10% theory
- Use AI for: quick explanations, code review, architecture hints, boilerplate
- Don't use AI for: writing entire systems you can't explain
- Every feature flows: `plan → design → build → review → fix → reflect`
- **Golden rule:** if you can't explain the code an hour later, AI wrote it for you, not with you

See [`docs/product/learning-strategy.md`](docs/product/learning-strategy.md) for the complete 5-axis resource system.
See [`docs/product/ai-learning-operating-manual.md`](docs/product/ai-learning-operating-manual.md) for the complete AI agent usage guide.

---

## Repository Map

```text
.ai/               # Prompt + workflow system (the "brain")
  prompts/         # system, roles, tasks, critics, repair
  workflows/       # feature, debugging, learning, architecture, evaluation
templates/         # Standardized artifact templates (ADR, review, plan, ...)
registries/        # YAML inventories: prompts, workflows, templates, decisions, skills
docs/
  CODEBASE-INTELLIGENCE.md  # Multi-layer code intelligence (3 graphs + context pack)
  roadmap/         # active-track-10-week (PLAN OF RECORD), milestones, dashboard
  decisions/       # ADRs
  reference/       # LLM production architecture, clean code, ML map, interviews
  learning/        # paths, deep-dives, daily-logs, source-summaries
  tracking/        # current-focus — what to work on right now
  plan/archive/    # superseded plans, kept for provenance
  product/         # workspace-goals, scope, feature-priorities, learning-strategy
  cheat-sheets/    # git, docker, postgres, qdrant, prompt-design
learning-sources/  # Source-driven learning (books, repos, notebooks, official-docs)
evaluations/       # Golden cases, regressions, RAG datasets, eval reports
projects/          # Phase folders 00→07 (devmate is the active project)
  04-ai-engineering/
    security/exercises/  # 10 security modules (94 files, directory-per-exercise)
infra/             # docker-compose + PowerShell scripts
tests/             # repo-structure, templates, workflows, prompts validation
```

See [`docs/architecture/monorepo-structure.md`](docs/architecture/monorepo-structure.md) for the
full tree and rationale.

---

## Code Intelligence

Four-layer code intelligence for token-efficient, context-aware engineering:

| Layer | Tool | What it does | Stats |
|-------|------|--------------|-------|
| **Structural Graph** | codebase-memory-mcp | Tree-sitter + LSP call graph, 155 languages | 53,461 nodes, 126,790 edges |
| **Review Graph** | code-review-graph | PR blast-radius, community detection, impact analysis | 11,590 nodes, 87,721 edges, 23 communities |
| **Multimodal Graph** | graphify | Code + docs + schemas, god nodes, shortest path | 49,856 nodes, 54,483 edges, 2,833 communities |
| **Context Pack** | repomix | One-shot repo packing for ad-hoc LLM tasks | 1,244,995 tokens, 1,082 files |

**Quick commands:**
```text
Who calls X?        → codebase-memory trace_path --function_name X --direction inbound
Find by pattern     → codebase-memory search_graph --name_pattern ".*X.*"
Impact of changes   → codebase-memory detect_changes
Blast radius        → code-review-graph detect_changes_tool
God nodes           → graphify god_nodes
Pack for LLM        → repomix pack_codebase
```

Full reference: [`docs/CODEBASE-INTELLIGENCE.md`](docs/CODEBASE-INTELLIGENCE.md)

---

## Workflow Rules

1. **Plan before build.** Start every feature at `.ai/workflows/feature/01-plan.md`.
2. **Architecture before large implementation.** Touching system boundaries → ADR or architecture review is mandatory.
3. **Review before done.** No feature is complete without `ai-review.md`.
4. **Document every bug** in a debugging-session artifact.
5. **Deterministic paths.** Artifacts land where the workflow says — no ad-hoc locations.
6. **Registries are source of truth** for prompt/workflow/template inventory and versions.

---

## Daily Loop (5+ hours)

| Block  | Time | Activity                                      |
| ------ | ---- | --------------------------------------------- |
| Build  | 3h   | The week's deliverable — code first            |
| Learn  | 1h   | One topic, docs-first, **after** building it   |
| Review | 1h   | AI code review + debugging log                 |
| Recall | 30m  | Explain without notes + daily log + plan       |

Full cadence: [`docs/WEEKLY_PROTOCOL.md`](docs/WEEKLY_PROTOCOL.md)

---

## Active Plan

**[Active Track — 10-Week AI Engineer](docs/roadmap/active-track-10-week.md)** — adopted
2026-08-02 by [ADR-0004](docs/decisions/0004-adopt-10-week-ai-engineer-track.md).
Target: a remote AI/LLM engineering role. Vehicle: **DevMate**.

> **Governing rule (amended by [ADR-0006](docs/decisions/0006-adopt-master-ai-engineering-curriculum.md)):**
> curriculum content is allowed again, but only when it traces to a DevMate concept or an
> interview answer — never as a substitute for building. The build-first ratio still has
> to hold: running services first, teaching material second.

| Week | Milestone | Deliverable |
| ---- | --------- | ----------- |
| 0 | A1 | CI green + `devmate stats` CLI |
| 1 | A2 | LLM layer — streaming, traced, costed |
| 2–3 | A3 | RAG with a measured eval harness |
| 4 | A4 | **Deployed at a public URL** + SQL sprint |
| 5–6 | A5 | Agent with 4 tools + MCP server |
| 7 | A6 | Cache, guardrails, hardening |
| 8 | A7 | Portfolio — blog, README, CV |
| 9–10 | A8, A9 | 40 applications, first interview |
| 11+ | A10 | Deferred ML sprint (buffer weeks) |

**Right now:** [`docs/tracking/current-focus.md`](docs/tracking/current-focus.md) ·
**Status:** [`docs/roadmap/progress-dashboard.md`](docs/roadmap/progress-dashboard.md)

### Other tracks

| Track | Status |
| ----- | ------ |
| [Phase 2 — Athar & Baligh](docs/roadmap/phase-2-athar-baligh.md) | After A7 |
| [Long track — 12-month roadmap](docs/roadmap/master-roadmap.md) (Go, Flutter/Next.js, ThanaweyaGPT) | Deferred |

---

## Progress

### Workspace Build (Complete ✅)
- [x] Phase 0 — Foundations (repo skeleton, templates, prompts, registries)
- [x] Phase 1 — Core MVP (one end-to-end feature on `auth-service`)
- [x] Phase 2 — Reliability (learning workflows, source templates, tests)
- [x] Phase 3 — Scale (scaffolding scripts, repo validation, deep dives)
- [x] Phase 4 — Advanced (RAG eval harness, capstone structure, operating manual)

### Code Intelligence (Complete ✅)
- [x] Structural graph — codebase-memory-mcp indexed (53,461 nodes, 126,790 edges, 8 languages)
- [x] Review graph — code-review-graph built (11,590 nodes, 87,721 edges, 23 communities)
- [x] Multimodal graph — graphify built (49,856 nodes, 54,483 edges, 2,833 communities)
- [x] Context pack — repomix ready (1,244,995 tokens, 1,082 files)
- [x] Security exercises — 10 modules split into 94 files (directory-per-exercise)

### Learning Journey
- [x] Python foundations — 1,941 files across 9 phases: core (41 topics), advanced (27), libraries (NumPy, Pandas, Matplotlib, SciPy), databases, web frameworks, DSA, ML, MLOps, GenAI
- [x] AI curriculum — 9,554 lines of lectures and practice workbooks under `docs/curriculum`, plus phase-4 tracks (agents, RAG, embeddings, prompt engineering, security, fast.ai) with lectures, exercises, and quizzes
- [x] fast.ai Deep Learning track — 13 modules with lectures, exercises, and quizzes
- [ ] **A1 — CI green + first DevMate command** ← YOU ARE HERE
- [ ] A2–A10 — see the table above
- [ ] Deferred: Go, frontend, classical ML

---

## Getting Started

```powershell
# 1. Bring up local infra (Postgres / Redis / Qdrant / MongoDB / Langfuse)
docker compose -f infra/docker/docker-compose.yml up -d

# 2. Work on the active project
cd projects/04-ai-engineering/devmate

# 3. Create a new ADR
./infra/scripts/new-adr.ps1 "Adopt keyset pagination"

# 4. Start today's log
./infra/scripts/new-daily-log.ps1

# 5. Query code intelligence
# See docs/CODEBASE-INTELLIGENCE.md for full tool reference
```

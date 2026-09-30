# Milestones — Full-Stack AI Engineer Lab

> Trackable milestones with evidence. Update status at weekly reviews.
> Statuses: `Planned` · `In Progress` · `Blocked` · `Review` · `Done` · `Deferred`

**Last updated:** 2026-08-02

---

## Two tracks, two ID prefixes

| Prefix | Track | Status |
| --- | --- | --- |
| **A** | [Active Track — 10-Week AI Engineer](active-track-10-week.md) | **Active** |
| **M** | [Long Track — 12-month master roadmap](master-roadmap.md) | Deferred under [ADR-0004](../decisions/0004-adopt-10-week-ai-engineer-track.md) |

Long-track milestones are retained rather than deleted — several will be revisited after
employment, and M1/M3/M6 are partially satisfied already.

---

# Active Track (A1–A10)

| ID | Milestone | Week | Evidence | Status |
| --- | --- | --- | --- | --- |
| A1 | CI green + `devmate stats` CLI | 0 | `.github/workflows/ci.yml`, `devmate/src/` | In Progress |
| A2 | LLM layer traced and costed | 1 | `devmate/src/devmate/obs/` | Planned |
| A3 | RAG with measured eval + 2 ADRs | 2–3 | `evaluations/rag/reports/` | Planned |
| A4 | **Deployed at a public URL** | 4 | live link in `devmate/README.md` | Planned |
| A5 | Agent with 4 tools + MCP server | 5–6 | `devmate/src/devmate/agent/`, `devmate/mcp/` | Planned |
| A6 | Production hardening | 7 | `devmate/docs/failure-modes.md` | Planned |
| A7 | Portfolio complete | 8 | `docs/writing/`, `docs/career/` | Planned |
| A8 | 40 applications submitted | 9–10 | `docs/tracking/applications.md` | Planned |
| A9 | First technical interview | 9–10 | `docs/tracking/applications.md` | Planned |
| A10 | Deferred ML sprint | 11+ | `python/07-machine-learning/` | Planned |

---

### A1 — CI Green + `devmate stats` CLI

- **Description:** Repo hygiene fixed, CI pipeline running, and the first DevMate command
  shipped: walk a repository, parse Python with `ast`, report functions/classes/LOC/file types.
- **Acceptance:** `make ci` passes locally and on GitHub · `devmate stats .` produces
  hand-verified numbers for this repo · unit tests pass · 5 PRs merged with clean history ·
  one deliberate interactive rebase · pyproject typo fixed and tracked binaries removed.
- **Blocked by:** nothing.

### A2 — LLM Layer Traced and Costed

- **Description:** Claude API integration with streaming, structured outputs, retries with
  backoff, and typed errors — instrumented from the first call.
- **Acceptance:** `devmate ask "<q>"` streams an answer · every call appears as a Langfuse
  trace · token count and dollar cost recorded per request · 10 golden cases committed ·
  three deliberate failures (mid-stream kill, oversized prompt, malformed structured output)
  documented in `mistakes.md`.
- **Blocked by:** A1.
- **Note:** observability is a *precondition* here, not a later addition — the correction
  recorded in ADR-0004.

### A3 — RAG with Measured Evaluation

- **Description:** Full retrieval pipeline, built eval-first: golden set → harness → three
  chunkers → Qdrant → Chroma comparison → hybrid + rerank.
- **Acceptance:** 25-question golden set over this repo · `make eval` prints recall@5,
  recall@10, MRR, faithfulness · three chunking strategies compared in a table · `VectorStore`
  Protocol with two working adapters · hybrid retrieval (dense + BM25) with reranking · **two
  ADRs, each citing measured numbers** (chunking strategy; vector store comparison).
- **Blocked by:** A2.
- **Note:** the eval harness precedes the chunkers. Comparing without measuring produces
  opinion.

### A4 — Deployed at a Public URL

- **Description:** FastAPI service, containerized, deployed, with Postgres persistence and a
  Streamlit UI. Includes the 3-day SQL sprint.
- **Acceptance:** public URL reachable · `/health` and `/ready` respond · `/ask` streams over
  SSE · rate limiting and API-key auth active · Postgres stores conversations, messages, eval
  runs, and per-query cost · migrations with justified indexes · multi-stage Dockerfile ·
  service present in `infra/docker/docker-compose.yml` · cold-start behaviour handled or
  documented.
- **Blocked by:** A3.
- **Note:** **the governing rule lifts here.** First portfolio-ready artifact.

### A5 — Agent with 4 Tools + MCP Server

- **Description:** Tool-using agent, built one tool at a time, plus an MCP server exposing
  DevMate retrieval.
- **Acceptance:** 4 working tools (`search_code`, `read_file`, `run_tests`, `propose_patch`) ·
  ReAct loop with step cap and loop detection, **proven by a test** · LangGraph port with a
  written comparison against the hand-rolled version · MCP server reachable from a real MCP
  client · agent eval reporting task completion and tool-selection accuracy.
- **Blocked by:** A4.
- **Note:** MCP is the differentiator — it appears in current postings and the repo has none.

### A6 — Production Hardening

- **Description:** Cache, guardrails, fallback, and testing appropriate to a non-deterministic
  system.
- **Acceptance:** Redis semantic cache with a measured hit rate · input guardrails blocking
  OWASP LLM top-10 injection attempts, with evidence · output guardrails (PII, schema) ·
  model fallback chain · tests using a mocked LLM, prompt snapshots, and recorded cassettes ·
  p50/p95 latency under load · `failure-modes.md` covering every dependency failure exercised.
- **Blocked by:** A5.

### A7 — Portfolio Complete

- **Description:** Everything built becomes legible. No new features.
- **Acceptance:** technical blog post about decisions and trade-offs (not a tutorial) ·
  portfolio README with architecture diagram, eval numbers, cost per query, demo GIF · CV
  targeted at remote AI roles · LinkedIn and GitHub profile updated · 3 recorded 2-minute
  English explanations · drafted answers to all 27 interview questions.
- **Blocked by:** A6.
- **Acceptance test:** a stranger understands what the project does and why it is built that
  way, from the README alone, in under two minutes.

### A8 — 40 Applications Submitted

- **Description:** 20 per week across weeks 9–10, tracked with a feedback loop.
- **Acceptance:** `docs/tracking/applications.md` with 40 entries · each recording platform,
  stack from the posting, status, **gap identified**, and the task created to close it.
- **Blocked by:** A7.

### A9 — First Technical Interview

- **Description:** Reach and complete a technical round.
- **Acceptance:** interview completed · every question that caused a stumble logged as a gap ·
  each gap converted into a task.
- **Blocked by:** A8.

### A10 — Deferred ML Sprint

- **Description:** Close the classical ML/DL gap deliberately deferred in ADR-0004.
- **Acceptance:** sklearn pipeline end-to-end · data leakage induced, measured, and fixed ·
  a PyTorch training loop written by hand · self-attention implemented from scratch ·
  gradient-boosting vs. neural net comparison written up · able to explain backpropagation,
  data leakage, and self-attention at a whiteboard without notes.
- **Blocked by:** A7 (uses buffer weeks 11–12; runs in parallel with A8/A9).
- **Reference:** [`../reference/ml-fundamentals-map.md`](../reference/ml-fundamentals-map.md)

---

### Active-track dependency chain

```text
A1 → A2 → A3 → A4 → A5 → A6 → A7 → A8 → A9
     (CI)  (LLM) (RAG) (deploy) (agent) (harden) (portfolio) (apply)
                                                  └→ A10 (ML sprint, parallel)
```

Strictly linear through A7 — each week's deliverable is the next week's foundation. Two float
weeks (11–12) absorb slippage.

---

# Production AI Systems track (P0–P8)

> Strategic track defined 2026-09-30 in
> [`../learning/design/production-ai-systems-engineer-roadmap.md`](../learning/design/production-ai-systems-engineer-roadmap.md).
> Not the plan of record. Gate: finish active-track A4 and preferably A6 first.

| ID | Milestone | Phase | Status |
| --- | --- | --- | --- |
| P0 | Gate: A4 + A6 complete | — | Planned |
| P1 | Eval infrastructure + CI gate | P1 | Planned |
| P2 | SLOs + observability operations | P2 | Planned |
| P3 | Cost enforcement + routing | P3 | Planned |
| P4 | Reliability + red-team schedule | P4 | Planned |
| P5 | Self-hosted serving lab | P5 | Planned |
| P6 | Gateway + eval-gated release | P6 | Planned |
| P7 | K8s / orchestration depth | P7 | Planned — demand-gated |
| P8 | Platform capstone | P8 | Planned |

# Long Track (M1–M13) — deferred

> Retained for post-employment depth. Not scheduled. See
> [`master-roadmap.md`](master-roadmap.md) and
> [`phase-2-athar-baligh.md`](phase-2-athar-baligh.md).

## Phase 0 — Foundations

| ID | Milestone | Evidence | Status |
| --- | --- | --- | --- |
| M1 | Go basics + mini exercises | `projects/00-core-foundations/go/` | Deferred — 2 of 10 exercises scaffolded |
| M2 | HTML/CSS/JS portfolio | `projects/00-core-foundations/` | Deferred |
| M3 | Git workflow mastery | this repo | Partially met — folded into A1 |
| M6 | First source-learning workflow | `docs/learning/source-summaries/` | Partially met — 1 summary exists |

## Phase 0 → 1 Bridge

| ID | Milestone | Evidence | Status |
| --- | --- | --- | --- |
| M4 | Auth-service MVP | `projects/01-backend-go/01-auth-service/` | Deferred — scaffolded, incomplete |
| M5 | PostgreSQL schema design | `projects/03-databases/postgres-design/` | Superseded by A4's SQL sprint |

## Phases 1–2 — Backend + Frontend

| ID | Milestone | Evidence | Status |
| --- | --- | --- | --- |
| M7 | Frontend app (Flutter or Next.js) | `projects/02-frontend/` | Deferred |
| M8 | Full-stack integration | complete app | Deferred |
| M9 | Docker deployment | `projects/06-devops/docker/` | Partially met by A4 |

## Phases 3–5 — AI

| ID | Milestone | Evidence | Status |
| --- | --- | --- | --- |
| M10 | AI foundations complete | `projects/04-ai-engineering/` | Superseded by A2 |
| M11 | RAG system working | `projects/04-ai-engineering/rag-system/` | Superseded by A3 |
| M12 | Agent system working | `projects/04-ai-engineering/agents/` | Superseded by A5 |

## Phase 7 — Capstone

| ID | Milestone | Evidence | Status |
| --- | --- | --- | --- |
| M13 | ThanaweyaGPT MVP | `projects/07-capstone/thanaweyagpt/` | Deferred — DevMate is the active vehicle |

---

## Summary

| Track | Total | Done | In Progress | Planned | Deferred / Superseded |
| --- | --- | --- | --- | --- | --- |
| Active (A) | 10 | 1 | 1 | 8 | 0 |
| Production (P) | 9 | 0 | 0 | 9 | 0 |
| Long (M) | 13 | 0 | 0 | 0 | 13 |

**The number that matters: deployed services = 0.** Target A4, week 4. Production AI
Systems evidence requires more than a URL: eval gates, SLOs, cost enforcement, and
measured serving numbers (see P-track).

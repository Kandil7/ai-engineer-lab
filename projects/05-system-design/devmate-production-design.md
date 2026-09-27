# System Design: DevMate Production Architecture

> Interview-grade design of the DevMate system at production scale, grounded in
> the track's measured numbers — not a greenfield fantasy. Every capacity figure
> traces to a milestone deliverable (A2–A6).

## Table of Contents

1. [Overview](#overview)
2. [Requirements](#requirements)
3. [Capacity Estimation](#capacity-estimation)
4. [API Design](#api-design)
5. [Data Model](#data-model)
6. [Component Deep Dives](#component-deep-dives)
7. [Scaling Strategy](#scaling-strategy)
8. [Failure Modes](#failure-modes)
9. [Cost Model](#cost-model)
10. [Deployment](#deployment)
11. [Tradeoffs and ADRs](#tradeoffs-and-adrs)

## Overview

DevMate answers questions over code repositories: ingest a repo, retrieve
relevant chunks, generate grounded answers, propose patches. At production
scale it serves concurrent `/ask` streams with p95 under 3 seconds, retrieval
recall@10 above 0.95, and per-query cost below two cents — each number owned
by a milestone and re-verified by gates, not asserted once.

```
Client -> API (FastAPI, SSE) -> Retrieve (Qdrant + BM25 -> RRF -> rerank)
                                    |
                              Generate (Claude primary, fallback chain)
                                    |
                              Observe (Langfuse traces + Postgres costs)
                                    v
                         Cache (Redis semantic) / Persist (Postgres)
```

## Requirements

Functional: ingest repo or docs folder; streaming answers with citations;
code explanations; patch proposals behind approval; conversation history;
eval harness runnable in CI.

Non-functional: p95 total latency < 3 s (retrieve < 100 ms, rerank < 150 ms,
generate < 2 s — the weeks 2–3 stage budgets); recall@10 >= 0.95 on the
golden set; faithfulness sampled weekly; $/query < $0.02 blended; 99.9%
monthly availability excluding provider outages (degrade, don't crash);
per-tenant data isolation; every LLM call traced with tokens and cost.

## Capacity Estimation

Portfolio scale first (the A4 promise): 100 daily users × 20 queries =
2,000 queries/day. At 2k prompt + 500 completion tokens blended across
haiku/sonnet paths, daily token volume ≈ 5M ≈ $15–30/day before caching.
Redis semantic cache at 30% hit rate cuts roughly a third. Growth scale
(10×): the only components that change are the pool sizes, the Qdrant
replica count, and the cache memory — the architecture does not.

## API Design

- `GET /health` — liveness plus dependency checks (Qdrant, Postgres, Redis, provider reachability); load balancers and keep-warm pings use it.
- `POST /ask` (SSE streaming) — `{question, conversation_id?, model_policy?}`; streams tokens, then a terminal event with trace id, cost, and citations.
- `POST /ingest` — `{repo_url | docs_path}`; returns a job id; chunking and embedding run async (ingest is minutes, never request-scoped).
- Auth: API key per tenant, rate limits per key (week 4 middleware). Every
  response carries the trace id; every request carries the tenant for cost
  attribution and isolation filtering.

## Data Model

Postgres (relational, per the track's SQL requirement): conversations,
messages (with prompt version + model id on each — the reproducibility rule),
eval runs and scores, cost ledger per query per tenant. Qdrant: chunk vectors
with payloads (`language`, `filename`, `chunk_type`, `repo_name`, tenant)
and the HNSW config from the index ADR. Redis: semantic cache entries keyed
by embedding similarity, with hit-rate metrics. MongoDB was evaluated and
rejected — the data is relational and the track requires SQL.

## Component Deep Dives

**Ingest.** Clone or read docs → clean (regex baseline from the Handbook's
`clean_text`, extended per failure logs) → chunk (fixed/recursive/AST-aware
per the chunking ADR) → embed in batches → upsert with md5 content ids
(idempotent re-ingest). Chunk metadata records sizes for reproducibility.

**Retrieve.** Query → metadata filter (tenant + facets, pre-filtered) →
dense Qdrant arm + BM25 arm in parallel → RRF fusion → cross-encoder rerank →
top-k with citations. Per-arm recall is logged so misses attribute to an arm,
never to "the system". The `VectorStore` Protocol keeps Qdrant swappable;
the eval harness keeps it honest.

**Generate.** Versioned Jinja prompts from the registry (never inline
strings) → primary model with structured output schemas → fallback chain
(primary → cheaper → cached → graceful error). Prompt version rides every
trace; a prompt change without an eval run is a policy violation (LLMOps).

**Observe.** Langfuse spans per stage with usage, latency, and cost; Postgres
cost ledger for billing views; p50/p95 dashboards sliced by model and prompt
version (averages hide single-version regressions); hallucination sampling
queue with weekly human review.

## Scaling Strategy

Stateless API replicas behind the balancer (no session state in process);
Qdrant scales by replica for reads, sharding past single-node RAM; Postgres
read replicas when the cost dashboard, not anxiety, says so; Redis sized from
measured hit-rate curves. The load test (week 7) re-runs per scaling change —
capacity claims without fresh numbers are expired.

## Failure Modes

Provider outage → fallback chain serves degraded answers with a visible
banner, never an exception page. Qdrant down → BM25-only degraded mode with
recall impact logged. Redis full → evict (cache is expendable by design).
Prompt-injection payload → input guardrails block with evidence (OWASP-mapped
tests). Key revocation mid-request → typed error, partial stream closed
cleanly. Each mode has a drill entry in `failure-modes.md` — designed,
induced, and recorded, not hypothesized.

## Cost Model

Unit economics per 1k queries: blended model spend (dominated by output
tokens on reasoning paths) minus cache savings (hit rate × full cost) plus
infra (hosting tiers + vector DB). Guardrails: per-query cost ceiling with
alerts, per-tenant budgets with throttles, prompt-change cost diff in CI
(a prompt edit that triples output tokens fails the gate before merge).
The A2 deliverable — stating one ask's cost in dollars — generalizes into
this ledger.

## Deployment

Railway/Render free tier for the portfolio URL (cold starts disclosed, keep-warm
ping documented); Docker multi-stage images from week 4; GitHub Actions
pipeline (lint → types → tests → eval-gated prompt changes → deploy);
SageMaker evaluated and rejected (training-grade spend for an inference-grade
goal). Rollback is config-speed: previous prompt version + previous image tag,
one step each.

## Tradeoffs and ADRs

Qdrant over Chroma (ADR-0005, measured). RAG first, fine-tuning deferred
(documented, week-11 reference: the LLM Handbook SFT/DPO pipeline). Hand-rolled
ReAct before LangGraph (pedagogy with a comparison note). Langfuse over Opik
(one platform, traces from day one). Postgres over MongoDB (relational data +
SQL requirement). Each tradeoff carries revisit conditions — a design without
them is a snapshot, not a system.

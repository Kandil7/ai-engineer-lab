# Reliability — Distributed Systems Patterns

The five-part dependency contract — timeout, retry, circuit breaker, fallback,
metrics — plus idempotency, backpressure, dead-letter queues, graceful
shutdown, rate limiting, and observability. Every claim in this track is
grounded in verified facts from this repository's own services (DevMate), its
Compose stack, and its CI; gaps in the codebase are named as gaps, not papered
over.

---

## Architecture: The Dependency Contract

```
                    request
                       │
                       ▼
              ┌─────────────────┐
   deny ──────┤  rate limiter   │──────► 429 + Retry-After
              └────────┬────────┘
                       │ allow
                       ▼
              ┌─────────────────┐
   open ──────┤ circuit breaker │──────► fallback / degraded response
              └────────┬────────┘
                       │ closed / half-open
                       ▼
              ┌─────────────────┐
  exhausted ──┤ timeout+retry   │──────► DLQ / typed error upstream
              └────────┬────────┘
                       │ success
                       ▼
                    dependency ──► response
                       │
                       ▼
              metrics (RED + saturation) ──► alerts
```

Each box blocks a different failure mode. The lecture teaches why omitting any
one of them moves the failure into a shared resource you did not intend to
share.

---

## Track Contents

| File | What it covers |
|------|----------------|
| `lectures/01-reliability-patterns-lecture.md` | The five defenses end to end: timeouts and deadlines, retries with classification and jitter, idempotency and outboxes, breakers and bulkheads, backpressure and DLQs, shutdown order, rate-limit tiers, cache stampede, consistency, degradation ladders, RED and error budgets |
| `lectures/01-reliability-patterns-glossary.md` | 47-term quick-reference table plus detailed definitions, each with code drawn from this repo or naming the repo's gap explicitly |
| `quizzes/01-reliability-patterns-quiz.md` | 15 questions (5 Easy, 7 Medium, 3 Hard) with inline answers and explanations, score tracking, answer key |
| `exercises/01-reliability-patterns.py` | Offline rule engine: 8 REL rules over a policy pack (BAD trips all 8, GOOD raises zero) plus runnable seeded components — full-jitter retry, breaker state machine, per-caller token bucket, idempotency store, deadline budget |
| `README.md` | This page |

---

## What Is Grounded (FACT)

Verified at the cited paths before this track was written:

- **HTTP timeouts exist on every client DevMate owns:** `llm/client.py:146`
  (60s/10s), `index/embeddings.py:73` (OpenAI) and `:246` (Ollama),
  `retrieve/retriever.py:56` (Cohere reranker, 30s/10s). The Qdrant client at
  `index/vector_store.py:101` passes no `timeout=` — that gap is Exercise 5's
  assignment.
- **Retry is classified and jittered:** tenacity
  `wait_exponential_jitter(initial=1, max=30)` + `stop_after_attempt(3)` +
  retry-on-timeout/network only, `llm/client.py:157-162`; `429` and `401` map
  to typed errors at `llm/client.py:214-219`; validation failures re-raise
  instead of rotating providers at `llm/client.py:773-775`.
- **Bounded queues and ordered shutdown exist at the API edge:**
  `asyncio.Queue(maxsize=...)` at `api/main.py:146`, LLM client closed in the
  lifespan at `api/main.py:65`. There is **no** SIGTERM handler, **no**
  circuit breaker, and **no** DLQ anywhere in `devmate/src/` — verified by
  repo-wide search; the lecture records these as gaps.
- **The infrastructure applies the same discipline:** Compose healthchecks at
  `infra/docker/docker-compose.yml:66-70` gate `depends_on:
  service_healthy` (lines 146-152); rate-limit defaults
  (`RATE_LIMIT_REQUESTS=100`, window 60s) at lines 141-143; CI's readiness
  wait is a bounded retry loop — `socket.create_connection(timeout=1)`, 30
  attempts, 1s sleep — at `.github/workflows/ci.yml:140-154`, and the eval
  gate (Hit@5 ≥ 1.0, MRR ≥ 0.70) at lines 71-77 is a quality error budget.

Sources: `source-index#28` (Chip Huyen, *AI Engineering* — application
reliability framing), `source-index#9` (Docker Compose Specification).

---

## Complements (Not Duplicates)

This track is registered knowledge applied at the **service call boundary**.
Two registry nodes already own adjacent territory, and this content sits next
to them rather than repeating them:

- `data.reliability` (knowledge-registry) — idempotency and checkpointing for
  **data pipelines**: `projects/00-core-foundations/data-engineering/03-idempotency`
  and `04-checkpointing`. Job-level replay; this track covers request-level
  retries, breakers, and queue mechanics.
- `system-design.failure-modes` — failure modes and resilience theory:
  `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`.
  Taxonomy and runbooks; this track teaches the mechanics of each pattern and
  their code in a live service.

---

## Verification

Run from the repository root:

```powershell
python -m py_compile projects\06-devops\reliability\exercises\01-reliability-patterns.py
python projects\06-devops\reliability\exercises\01-reliability-patterns.py
powershell -NoProfile -ExecutionPolicy Bypass -File tests\repo-structure\validate.ps1
powershell -NoProfile -ExecutionPolicy Bypass -File tests\knowledge\validate.ps1
```

Expected: compile exits 0; the demo exits 0 with the BAD pack tripping all
8 REL rules and the GOOD pack raising zero findings; both validators exit 0.
The exercise is stdlib-only, offline, and seeded — reruns are identical.

---

*AI Engineer Lab — DevOps track, reliability lane.*

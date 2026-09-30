# DevMate — Failure Modes and Resilience

> A6 evidence artifact. Every failure mode gets a detection, a blast radius, and a
> recovery, written before the incident. Companion to the design in
> `docs/learning/design/project-plan-devmate-completion.md` and the theory in
> `projects/00-core-foundations/python/10-system-design/04-failure-modes-and-resilience`.

## 1. The pipeline (what can fail)

```text
CLI / API  ->  ingest (repo_reader -> chunker)  ->  index (embeddings -> Qdrant)
           ->  retrieve (retriever -> rag)      ->  llm (Anthropic | Ollama)
           ->  obs (Langfuse + cost)             <- db (Postgres), cache (Redis), guards
```

Each arrow is a dependency that can fail. The sections below classify the
failures and design the response.

## 2. Failure taxonomy

| Class | Example in DevMate | Response |
| --- | --- | --- |
| **Transient** | Ollama 500 / network blip / rate limit | retry with backoff (`tenacity`), capped attempts |
| **Permanent** | malformed repo path, unparseable file, bad payload | no retry; log + skip + surface |
| **Partial** | worker killed mid-ingest | redelivery + idempotent upsert |
| **Silent** | stale index, ungrounded answer, cost overrun | detection metrics + alarm; never silent |

Silent failures are the dangerous class: no exception, no failed request, and the
user discovers the damage as a wrong or ungrounded answer.

## 3. FMEA-lite

| Component | Mode | Detection | Blast radius | Recovery |
| --- | --- | --- | --- | --- |
| ingest / repo_reader | unreadable file or path | per-file log + skipped count | one file missing from the index | re-run with a fixed path; idempotent |
| chunker | wrong boundaries (too small/large) | chunk-size distribution metric | retrieval quality drops silently | re-chunk + re-index; chunking ADR |
| embeddings | provider error / rate limit | `tenacity` retries + failure counter | ingest stalls | backoff, then dead-letter the batch |
| Qdrant | unreachable / write rejected | health check + write error | search serves stale index | rebuild index from source (Postgres) |
| retrieve / rag | context over budget | `rag_context_char_budget` guard + log | provider 500 on long prompts | cap retrieved context (see §5) |
| LLM provider | 500 / timeout / auth | typed errors (`LLMError`, `LLMTimeoutError`, `LLMAuthError`) | single answer fails | provider fallback chain (§6) |
| Postgres | unreachable | health check + 503 | no persistence / no rebuild source | failover; Postgres is the source of truth |
| Redis | cache unavailable | cache-miss rate spike | latency/cost rise, answers still correct | serve uncached; TTL bounds staleness |
| Langfuse | unreachable | trace-export errors | observability gap (not user-visible) | buffer + retry; never block the request |
| guards | over-blocking a category | guardrail-trigger rate by category | legitimate answers refused | fix the class, not the whole guard |

Severity is ranked 1–5 for what to fix first; data loss and silent wrongness rank
highest.

## 4. Timeouts

Every outbound call has an explicit deadline: the LLM client, Qdrant, Postgres, and
Redis. An un-timed call can hang forever, wedging a request and (under load) backing
up the worker pool. A timeout converts an unbounded hang into a bounded failure the
retry policy or the fallback can handle.

## 5. The first real incident (from `mistakes.md`)

**Symptom:** `devmate ask` returned `500` from Ollama for long questions only.

**Root cause:** the retrieved-context prompt exceeded `qwen2.5-coder:7b`'s default
context window. Short questions fit; long ones did not.

**Fix:** a `rag_context_char_budget` (8000 chars) enforced in
`RAGPipeline._build_context`, plus `ollama_num_ctx` (8192) passed to Ollama.
Regression tests: `tests/unit/test_rag_context_budget.py`.

**Rule:** retrieval `top_k` is a candidate count, not a prompt guarantee — always
budget the context you actually paste. This is a *silent-before-fix* failure: it
looked like a provider error but was a budget error.

## 6. Fallback chain

```text
primary model -> cheaper/local model -> cached answer -> graceful error
```

- The LLM client selects a provider (Anthropic or Ollama); a failure falls to the
  next provider when configured.
- The cache serves a validated, non-abstained prior answer (RAG System 06).
- The last rung is an explicit error, never a fabricated answer.

## 7. Graceful degradation ladder

| State | User-visible behavior |
| --- | --- |
| All dependencies healthy | full retrieval + grounded citations |
| Index stale | answer + "results may lag recent edits" |
| Index unavailable | keyword/SQL fallback over the Postgres source |
| LLM provider down | cached answers only + explicit notice |
| Nothing left | 503 with a reason — **never a fabricated citation** |

The final rung is the integrity rule: an honest "cannot answer now" beats a confident
wrong citation.

## 8. Detections to build (A6 checklist)

- [ ] DLQ depth and job age (ingest workers).
- [ ] Drift metric: source version vs index version.
- [ ] Cache hit rate.
- [ ] Guardrail trigger rate by category.
- [ ] p50/p95 latency and provider error rate.
- [ ] Cost per request (token tracking already in `obs/cost.py`).
- [ ] Rolling faithfulness on a sample of answers.

## 9. The mastery answers

**"What happens if a worker fails?"** Partial/transient. At-least-once redelivery
plus idempotent upserts means the chunk is neither lost nor duplicated; a permanent
failure dead-letters with its identity. Detection: DLQ depth and job age.

**"What happens if the index goes stale?"** Silent, so it is measured: drift alerts,
the staleness state machine bounds it, the degradation ladder keeps answers honest,
and the rebuild job re-derives the index from Postgres. Detection: drift alert.
Recovery: rebuild runbook.

---

*Created as A6 evidence. Update the FMEA when a component changes; add every new
incident to `mistakes.md` and, if it is a new class, to the table in §3.*

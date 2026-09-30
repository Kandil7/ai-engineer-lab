# Embeddings 02: Batch Processing

## Topic Overview

Embedding generation is a throughput problem. A pipeline that embeds one text per API call is
hundreds of times slower and more expensive than one that batches, and at corpus scale that
difference decides whether ingestion takes minutes or days. Batching, retry with backoff, and
asynchronous processing turn a naive per-item loop into a pipeline that finishes.

This lecture covers the batch, the rate limit, the retry discipline, async processing during
ingestion, and throughput tracking. The through-line is that embedding is an unreliable,
rate-limited, network-bound operation, so the code must be written for partial failure and
throughput, not for the happy path.

The failure modes are concrete: a per-item loop that is too slow, a 429 that crashes the batch,
a retry that hammers the API, and an ingestion pipeline that blocks on embedding. Each has a
standard fix, and the fixes compose.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Batch texts into API calls.
2. Handle rate limits with retries.
3. Retry with exponential backoff and bounded attempts.
4. Process embeddings asynchronously during ingestion.
5. Track throughput and batch failure rate.
6. Explain why a per-item loop is the wrong default.

## Prerequisites

- Embeddings 01 (model selection) for the model being called.
- Basic concurrency and error-handling familiarity.

---

## 1. The Batch

### One call for many texts

Embedding APIs accept batches, so a batch of 100 texts is one call instead of 100:

```python
def batches(texts: list[str], size: int) -> list[list[str]]:
    """Split texts into batches of the given size."""
    return [texts[i : i + size] for i in range(0, len(texts), size)]
```

The throughput multiplies by the batch size, which is the difference between a pipeline that
completes and one that does not.

### Batch size

The batch size is tuned to the API's limit and to memory. Too small wastes calls; too large
exceeds the request limit or the provider's token cap. Measure the throughput at a few sizes and
pick the one that uses the limit without hitting it.

### The measurement

The exercise shows 250 texts in 3 batches of up to 100, rather than 250 calls. That is the
difference the batch makes, and it is why batching is the first optimization.

## 2. Rate Limits

### What they are

APIs rate-limit by requests per minute and tokens per minute. A batch that exceeds the limit
gets a 429. The limit is a property of the account tier and the provider.

### Handling them

A 429 is not a fatal error; it is a signal to wait and retry. The pipeline must recognize it and
back off rather than crash or, worse, hammer the API. Unmanaged rate limits turn a working
ingestion into a failing one at exactly the wrong moment.

### The production lesson

Rate limits are part of the contract. A pipeline that works in development (low volume) and
fails in production (high volume) usually has no rate-limit handling.

## 3. Retries with Backoff

### Exponential backoff

A transient error or a 429 is retried with exponential backoff: wait, retry, double the wait:

```python
def embed_with_retry(text: str, attempts: int) -> str:
    """A stub: retries with backoff, then fails loudly."""
    for attempt in range(attempts):
        ...
    raise RuntimeError("embedding failed after retries")
```

### Bounded attempts

The retry is bounded: a fixed number of attempts, then the batch fails loudly. Silent infinite
retries hide a real outage, and unbounded retries can amplify a problem (the thundering herd).

### Fail loudly, not silently

A persistent failure raises. The ingestion pipeline records the failed batch and moves on or
stops, but it never silently drops texts, because dropped texts are missing vectors and missing
vectors are retrieval failures discovered much later.

### Jitter

Adding a small random jitter to the backoff avoids synchronized retries from many workers, which
would re-create the rate-limit spike the backoff was meant to avoid.

## 4. Asynchronous Processing

### Embedding in the background

Embedding runs in the background during ingestion. The ingestion pipeline does not block on the
embedding call; it enqueues and continues. Async processing keeps the pipeline moving.

### Why it matters

Embedding a large corpus is slow and rate-limited, so blocking the pipeline on it couples the
whole ingestion to the slowest, most failure-prone step. Decoupling lets the pipeline make
progress and lets embedding retry independently.

### The consequence for consistency

Because embedding is asynchronous, the index may briefly lag the corpus. The pipeline records
the state so a query knows which passages are indexed, which is the provenance discipline
(RAG System 06).

## 5. Throughput Tracking

### What to measure

Track embeddings per second and the batch failure rate. A dropping throughput signals a
rate-limit or a network problem; a rising failure rate signals something worse.

### Why it matters

Throughput is the metric that tells you the pipeline is healthy during a long ingestion. Without
it, a stalled ingestion looks like a slow one until it is discovered hours later.

### The cost link

Throughput and cost are read together: a pipeline that is fast but expensive and one that is
cheap but slow are both tradeoffs, made explicit by the metrics.

## 6. Putting It Together

### The pipeline

```text
texts -> batches -> retry with backoff -> embed -> store vectors
       (background, tracked, bounded, resumable)
```

### Resumability

The pipeline records which batches completed, so an interrupted ingestion resumes rather than
restarting. Resumability plus idempotency (Data Engineering 03) is what makes a large ingestion
safe to re-run.

### The standard fixes

A per-item loop, no retry, retry without backoff, blocking ingestion, and no tracking are the
five mistakes this lecture removes, and each has a one-line fix.

## Real-World Application

- Embedding the Athar corpus in batches of a few hundred passages with backoff, tracked for
  throughput.
- Handling a 429 during a large DevMate ingestion by backing off rather than failing.
- Running embedding in a background worker so the ingest pipeline does not block.
- Recording completed batches so an interrupted ingestion resumes.

## Common Mistakes

1. **A per-item loop.** Hundreds of times slower and more expensive.
2. **No retry on 429.** The batch fails and texts are dropped.
3. **Retrying without backoff.** Hammering the rate limit.
4. **Blocking ingestion on embedding.** The pipeline stalls on the slowest step.
5. **No throughput tracking.** A stalled ingestion looks slow.
6. **No resumability.** An interrupted ingestion restarts from zero.

## Key Takeaways

1. Batching multiplies throughput; tune the batch size to the API's limits.
2. Rate limits are part of the contract and must be handled, not ignored.
3. Retries use exponential backoff with bounded attempts and fail loudly.
4. Embedding runs asynchronously during ingestion so the pipeline does not block.
5. Track throughput and failure rate, and make the pipeline resumable.

## Self-Check Questions

1. Why is a per-item embedding loop the wrong default at corpus scale?
2. What should happen on a 429, and what should not?
3. Why must retries be bounded, and what happens on the final failure?
4. Why does embedding run asynchronously during ingestion?
5. What does a dropping throughput tell you, and why is it worth tracking?

## Further Reading / Connections

- Embeddings 03 (caching) — avoiding the calls entirely.
- Data Engineering 03 (idempotency) — why re-running ingestion safely matters.
- Model Serving 03 (inference serving) — retries and fallback in serving.
- `projects/04-ai-engineering/devmate/src/devmate/index/embeddings.py` — a working embedder.

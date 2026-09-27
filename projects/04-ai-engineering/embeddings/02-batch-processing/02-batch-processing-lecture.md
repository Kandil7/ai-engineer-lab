# Embeddings 02: Batch Processing

## 🎯 Topic Overview

Embedding generation is a throughput problem. Batching, retries, and
async processing turn a slow per-item loop into a fast pipeline. This
lecture covers the batch, the rate limit, and the retry discipline.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Batch texts into API calls
2. Handle rate limits with retries
3. Process asynchronously during ingestion
4. Track the throughput
5. Avoid the per-item loop

---

## 1. The Batch

Embedding APIs accept batches. A batch of 100 texts is one call instead of
100 — the throughput multiplies. The batch size is tuned to the API's
limit. The roadmap's exit test: "texts are embedded in batches."

```python
def embed_batch(texts, batch_size=100):
    for i in range(0, len(texts), batch_size):
        yield embed(texts[i : i + batch_size])
```

## 2. Rate Limits

APIs rate-limit: a limit on requests per minute and tokens per minute. A
batch that exceeds the limit gets a 429. The roadmap's exit test: "rate
limits are handled."

## 3. Retries

A 429 or a transient error is retried with exponential backoff — wait,
retry, double the wait. The retry is bounded: a fixed number of attempts,
then the batch is failed loudly. The roadmap's exit test: "retries use
exponential backoff."

## 4. Async Processing

Embedding runs in the background during ingestion. The ingestion pipeline
does not block on the embedding call. Async processing keeps the pipeline
moving. The roadmap's exit test: "embedding is processed asynchronously."

## 5. Throughput Tracking

The pipeline tracks embeddings per second and the batch failure rate. A
dropping throughput signals a rate-limit or a network problem. The metrics
make the pipeline observable.

## Common Mistakes

- A per-item loop (one call per text).
- No retry on 429 (the batch fails).
- Retrying without backoff (hammering the API).
- Blocking ingestion on embedding.
- No throughput tracking.

## Key Takeaways

1. Batching multiplies throughput.
2. Rate limits are handled, not ignored.
3. Retries use exponential backoff.
4. Embedding runs async during ingestion.
5. Throughput is tracked.
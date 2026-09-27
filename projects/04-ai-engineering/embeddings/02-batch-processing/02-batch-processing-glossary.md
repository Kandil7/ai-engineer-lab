# Embeddings 02: Batch Processing — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Batch | Many texts in one API call | 100 per call |
| Rate limit | The API's requests/tokens per minute | 3000 RPM |
| 429 | The rate-limit response | retry |
| Exponential backoff | Wait, retry, double the wait | bounded retries |
| Async processing | Embedding in the background | non-blocking ingestion |
| Throughput | Embeddings per second | tracked |
| Per-item loop | One call per text | the anti-pattern |

---

## Alphabetical Glossary

### 429

**Definition:** The rate-limit response. The batch exceeded the API's
limit and must be retried.

**Example:**
```python
# HTTP 429 Too Many Requests
```

**Related concepts:** Rate limit, Exponential backoff

---

### Async processing

**Definition:** Embedding runs in the background during ingestion. The
pipeline does not block on the embedding call.

**Example:**
```python
# embed in the background; ingestion continues
```

**Related concepts:** Throughput

---

### Batch

**Definition:** Many texts in one API call. A batch of 100 is one call
instead of 100.

**Example:**
```python
for i in range(0, len(texts), 100):
    embed(texts[i : i + 100])
```

**Related concepts:** Per-item loop

---

### Exponential backoff

**Definition:** The retry discipline: wait, retry, double the wait. Bounded
to a fixed number of attempts, then fail loudly.

**Example:**
```python
# wait 1s, 2s, 4s, then give up
```

**Related concepts:** 429

---

### Per-item loop

**Definition:** One API call per text. The anti-pattern that multiplies
latency and rate-limit hits.

**Example:**
```python
# for t in texts: embed(t)  # slow
```

**Related concepts:** Batch

---

### Rate limit

**Definition:** The API's bound on requests per minute and tokens per
minute. Exceeding it returns a 429.

**Example:**
```python
# 3000 RPM, 2M tokens/min
```

**Related concepts:** 429

---

### Throughput

**Definition:** Embeddings per second. Tracked to make the pipeline
observable; a drop signals a rate-limit or network problem.

**Example:**
```python
# 500 embeddings/sec
```

**Related concepts:** Async processing

---

## Related Concepts

- **Model selection**: the model runs in batches (topic 01)
- **Caching**: cached embeddings skip the batch (topic 03)
- **Quality evaluation**: batches feed the eval (topic 04)

## Key Takeaways

1. Batching multiplies throughput.
2. Rate limits are handled, not ignored.
3. Retries use exponential backoff.
4. Embedding runs async during ingestion.
5. Throughput is tracked.
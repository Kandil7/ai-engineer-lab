# Model Serving 03: Inference Serving — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Serving API | The request/response contract | stable shape |
| Batching | Grouping requests for throughput | server-side |
| Concurrency | Handling multiple users | server-side |
| Latency | Time to first token / total time | p95 |
| Throughput | Tokens per second | tokens/sec |
| Fallback chain | Backup model on primary failure | availability |
| End-to-end test | Request, response, metric check | CI gate |

---

## Alphabetical Glossary

### Batching

**Definition:** Grouping requests for throughput. Handled by the server
(vLLM, TGI), not the application.

**Example:**
```python
# the server batches; the app sends individual requests
```

**Related concepts:** Concurrency

---

### Concurrency

**Definition:** Handling multiple users simultaneously. The server's
responsibility.

**Example:**
```python
# 10 concurrent requests served
```

**Related concepts:** Batching

---

### End-to-end test

**Definition:** Testing the full serving path: request, response, metric
check. Catches API drift and regressions.

**Example:**
```python
# send a request; assert the response and latency
```

**Related concepts:** Serving API

---

### Fallback chain

**Definition:** Routing to a backup model when the primary fails or times
out. Preserves availability at the cost of consistency.

**Example:**
```python
# primary -> fallback -> error
```

**Related concepts:** Latency

---

### Latency

**Definition:** Time to first token and total time. The responsiveness
metric.

**Example:**
```python
# p95 time-to-first-token < 500ms
```

**Related concepts:** Throughput

---

### Serving API

**Definition:** The request/response contract: shape, error codes. Stable
across model changes.

**Example:**
```python
# POST /v1/completions -> {text, usage}
```

**Related concepts:** End-to-end test

---

### Throughput

**Definition:** Tokens per second. The volume metric.

**Example:**
```python
# 500 tokens/sec under load
```

**Related concepts:** Latency

---

## Related Concepts

- **Self-hosted models**: the server (topic 02)
- **Choosing a model**: the model behind the API (topic 01)
- **Production monitoring**: the metrics (ai-evaluation 07)

## Key Takeaways

1. The API is the contract; the model can change.
2. The server handles batching and concurrency.
3. Latency and throughput are the metrics.
4. A fallback chain preserves availability.
5. The serving path is tested end-to-end.
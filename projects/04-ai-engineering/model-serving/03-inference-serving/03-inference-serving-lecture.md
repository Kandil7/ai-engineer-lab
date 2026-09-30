# Model Serving 03: Inference Serving

## Topic Overview

Serving a model is the production boundary. On one side is the application and its
users; on the other is a model that is slow, occasionally unavailable, and does not
batch itself. The serving layer is what makes the model look like a dependable service:
a stable API, batching for throughput, metrics for visibility, and a fallback for when
the model or the provider fails.

This lecture covers the serving API contract, how batching and concurrency actually get
handled (by the server, not the application), the metrics that matter and why percentiles
beat averages, the fallback chain that preserves availability, and the end-to-end test
that catches drift and regressions in the serving path.

The recurring theme is that the application should be thin and the server should do the
hard work. Applications that try to batch requests themselves, or that assume the model
is always up, build the failure modes this lecture exists to prevent.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define a stable serving API contract separate from the model behind it.
2. Explain how batching and concurrency are handled by the server.
3. Monitor latency and throughput with percentiles and the right signals.
4. Design a fallback chain that preserves availability.
5. Write an end-to-end test of the serving path.
6. Describe prefill versus decode and the metrics that follow from them.

## Prerequisites

- Model Serving 02 (self-hosted models) for the server the API sits in front of.
- AI Evaluation 07 (production monitoring) for the alerting context.

---

## 1. The Serving API Contract

### The API is the contract

The serving API defines the request shape, the response shape, and the error codes. It
is stable across model changes: the model behind it can be swapped, quantized, or
replaced while callers see no difference.

### What the contract includes

- **Request:** the prompt or messages, the generation parameters, and any metadata.
- **Response:** the text, the token usage, and the model identifier that produced it.
- **Errors:** a typed shape for rate limits, timeouts, and upstream failures, with
  status codes the caller can act on.

### Why stable matters

If the response shape changes when the model changes, every caller breaks. Pinning the
contract lets the model be an implementation detail, which is what makes the
provider-agnostic choice from Model Serving 02 real.

## 2. Batching and Concurrency

### The server's job

Batching groups independent requests so the GPU processes them together, which raises
throughput substantially. Concurrency handles multiple users at once. Both are handled
inside the serving server (vLLM, TGI, and similar), which uses continuous batching to
keep the GPU busy as requests arrive and finish.

### The application's job

The application sends individual requests and trusts the server. It does not try to
batch requests itself; application-level batching adds latency waiting for a batch to
fill and duplicates logic the server already does better. Keeping the application thin
is the correct division of labor.

### Why it matters for capacity

On a single 16 GB GPU, batching is the difference between serving a handful of users and
serving many. It is also why the same model performs very differently under Ollama (no
continuous batching) and vLLM (batching): the server, not the model, sets the ceiling.

## 3. Monitoring Latency and Throughput

### The two metric families

- **Latency:** time to first token (TTFT) and total time. TTFT is what users feel while
  waiting for the answer to start; total time is how long it takes to finish.
- **Throughput:** tokens per second, and requests per second. Throughput is what
  determines how many users one GPU can serve.

### Percentiles, not averages

Report p50, p95, and p99. Averages hide the tail, and the tail is where users suffer.
The exercise's `p95` makes the point:

```python
def p95(values: Sequence[float]) -> float:
    """The 95th percentile latency."""
    sorted_v = sorted(values)
    idx = int(len(sorted_v) * 0.95)
    return sorted_v[min(idx, len(sorted_v) - 1)]
```

On the sample latencies, p95 lands on the slow request, which is the one the average
would have hidden.

### A degradation is a signal

A rising TTFT or a falling tokens-per-second rate signals overload (queueing), a model
problem, or a resource contention. The metric is how you learn about it before users
report it (AI Evaluation 07).

## 4. The Fallback Chain

### What it is

A fallback chain routes to a backup path when the primary fails or times out: a smaller
model, a cheaper provider, or a cached response, and finally a graceful error. It
preserves availability at the cost of some consistency.

```python
def serve(request, primary, fallback) -> dict:
    """Route to the primary; fall back on failure."""
    try:
        return primary(request)
    except Exception:
        return fallback(request)
```

### The properties to design for

- **Bounded failure.** The primary must fail fast (a timeout), not hang, or the fallback
  never runs.
- **Ordered degradation.** Primary, then a cheaper or cache path, then a clear error.
- **Observability of the fallback.** Every fallback should be recorded; a silent
  fallback hides an underlying outage.

### Consistency is the cost

The fallback answer may differ from the primary's in style or quality. That is the
tradeoff: availability over consistency. Document it so users are not surprised by a
sudden change in tone during an incident.

## 5. Testing the Serving Path

### The end-to-end test

The serving path is tested end to end: a request goes in, a response comes out, and a
metric is checked. The test catches API drift, latency regressions, and fallback
failures that unit tests on isolated functions would miss.

### What to assert

- The response matches the contract shape.
- The fallback serves when the primary raises.
- Latency stays under a bound (or is at least recorded).
- The model identifier in the response matches what is deployed.

### Failure injection

Deliberately break the primary (raise an exception, kill the dependency) and confirm the
fallback serves and the metrics record it. This is the serving-path version of the
"break it on purpose" discipline used elsewhere in the track.

## 6. Prefill and Decode

### The two phases

Generating a response has a prefill phase (the model reads the prompt and builds the KV
cache) and a decode phase (the model emits tokens one at a time). Prefill is
compute-bound and fast per token but scales with prompt length; decode is memory-bound
and produces tokens sequentially.

### The metrics follow

TTFT is dominated by prefill plus queueing; tokens per second is the decode rate.
Understanding the split explains why a long prompt raises TTFT without lowering the
decode rate, and why concurrency raises queueing latency. It is the vocabulary for
reading the serving metrics instead of guessing at them.

## 7. Capacity and Overload

### Queueing under load

When requests arrive faster than the GPU can process them, they queue. Queueing shows up
as rising TTFT before it shows up as errors, which is why TTFT is an early overload
signal. A system that only alerts on errors is blind to the overload that precedes them.

### Overload behavior

Decide what happens at capacity: reject fast (a clear 429) or queue with a bounded wait.
Rejecting fast protects the users who are served; unbounded queueing turns a slow system
into a down one. The choice belongs in the API contract.

## Real-World Application

- Putting a stable `/ask` contract in front of DevMate's model so the model can change
  without changing the API.
- Running a p95 TTFT alert on the serving endpoint.
- Wiring a fallback chain from the primary model to a cheaper one to a cached response.
- Load-testing the serving path and reading p95 versus p50 to see the tail.

## Common Mistakes

1. **No API contract.** Callers guess the shape and break when the model changes.
2. **No monitoring.** Degradation is invisible until users complain.
3. **No fallback.** The model or provider is a single point of failure.
4. **No end-to-end test.** API drift and fallback failures ship unnoticed.
5. **Batching in the application.** It adds latency and duplicates the server's job.
6. **Averaging latency.** The tail is hidden.
7. **Unbounded queueing at capacity.** The system degrades from slow to down.

## Key Takeaways

1. The serving API is a stable contract; the model behind it can change.
2. The server handles batching and concurrency; the application stays thin.
3. Monitor latency (TTFT, total) and throughput (tokens/sec) with percentiles, not
   averages.
4. A fallback chain preserves availability at the cost of consistency, and every
   fallback is recorded.
5. Test the serving path end to end, including a deliberately broken primary.

## Self-Check Questions

1. Why must the serving API be stable even when the model changes?
2. Why is application-level batching the wrong place to batch?
3. What does p95 latency reveal that the average hides?
4. Describe a fallback chain and the property the primary must have for it to work.
5. Why does a long prompt raise TTFT without necessarily lowering the decode rate?

## Further Reading / Connections

- Model Serving 02 (self-hosted models) — the server this layer fronts.
- Model Serving 04 (HF Inference SDK) — a managed alternative with its own limits.
- AI Evaluation 07 (production monitoring) — the alerting that consumes these metrics.
- `docs/reference/llm-production-architecture.md` — the request pipeline and cost
  sections.

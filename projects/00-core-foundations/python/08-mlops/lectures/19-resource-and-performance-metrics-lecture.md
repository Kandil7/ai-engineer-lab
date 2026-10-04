# MLOps — 19: Resource and Performance Metrics

## Topic Overview

Accuracy tells you whether a model is right; resource and performance
metrics
tell you whether it can **run** — at what latency, on what hardware, at
what
cost. A model that scores 0.95 but needs 40 GB of VRAM and 2 seconds per
request
is not deployable on a 16 GB card with a 200 ms SLO. These metrics are
the
deployability half of ML quality, and they are what turn "it trains"
into "it
ships."

There are two families. **Performance indicators** measure the service:
latency
percentiles (p50/p95/p99), throughput, and error rate. **Resource
utilization**
measures the machine: GPU utilization and VRAM, CPU, RAM, disk IO, and
network.
A model is efficient when it delivers good accuracy per unit of the
scarce
resource — per millisecond, per gigabyte, per dollar.

This matters most on a fixed budget. The RTX 5000's 16 GB is not a
suggestion;
it is the hard ceiling the memory model (weights + KV cache +
activations) must
fit under. Measuring before optimizing is the discipline: profile the
latency,
read the utilization, and only then reach for quantization
(`08-mlops/08`),
pruning, or a smaller batch.

## Learning Objectives

By the end of this lecture, you will be able to:
1. Explain why accuracy alone does not prove deployability
2. Compute latency percentiles (p50/p95/p99) and state why the tail matters
3. Measure throughput and relate it to batch size and latency
4. Read GPU/CPU/memory utilization and identify the bottleneck resource
5. Compute efficiency ratios (accuracy per ms, per GB, per dollar)
6. Profile a model's latency and memory with the right tools
7. Wire resource and performance metrics into gates and alerts

## Prerequisites

| Need | Where |
|---|---|
| Experiment metrics | `08-mlops/lectures/02-experiment-tracking-lecture.md` |
| Cost pillars | `08-mlops/lectures/15-cost-optimization-lecture.md` |
| Inference optimization | `08-mlops/lectures/08-inference-optimization-lecture.md` |
| Monitoring and drift | `08-mlops/lectures/11-monitoring-and-drift-lecture.md` |

## 1. The Four Metric Families

A model's quality is four numbers, not one. Train/validation metrics say
it
learned; **performance indicators** say it serves; **resource
utilization** says
it fits; **cost** says it is affordable.

```python
model_quality = {
    "accuracy": 0.91,  # train/val (Lecture 02)
    "latency_p95_ms": 180,  # performance (this lecture)
    "vram_gb": 9.2,  # resource (this lecture)
    "cost_per_1k_requests": 0.04,  # cost (Lecture 15)
}
```

A model is deployable only when **all four** clear their budgets. An
optimizer
that improves accuracy while doubling latency has not improved the model
for
production.

## 2. Performance Indicators

### Latency percentiles

The p50 is the median request; the p95 and p99 are the tail — the worst
5% and
1%. Users experience the tail, so an SLO is always a percentile ("p95
under
200 ms"), never a mean. A model with a fast mean and a slow tail still violates
the SLO.

```python
def percentile(latencies: list, q: float) -> float:
    """p50, p95, p99 from a sorted list of request latencies (ms)."""
    ordered = sorted(latencies)
    k = min(len(ordered) - 1, int(q / 100 * len(ordered)))
    return ordered[k]
```

### Throughput

Throughput is requests per second. It rises with batch size (more
parallelism)
and falls with latency. The batch size that maximizes throughput usually
hurts
per-request latency — which is why "fast" and "high-throughput" are
different
goals, served by different batching choices.

### Error rate

The fraction of requests that fail or time out. A model that is accurate
but
crashes 2% of requests is worse than a slightly weaker model that never
crashes.
Error rate joins latency and accuracy as the three production numbers.

## 3. Resource Utilization

### GPU: utilization and VRAM

GPU **utilization** (percent of SMs active) says whether the card is
working or
waiting on data — low utilization with high latency means a data
pipeline
bottleneck, not a compute bottleneck. **VRAM** is the hard ceiling:
weights +
KV cache + activations must fit, and the margin is what allows a bigger
batch.

### CPU, RAM, IO, network

The GPU does not run alone. CPU preprocessing, RAM for the dataset, disk
IO for
checkpoints and artifacts, and network for the artifact store all
constrain a
run. A training job that is IO-bound wastes an expensive GPU waiting on
a slow
disk — the classic misallocation resource metrics expose.

```python
def utilization(used: float, total: float) -> float:
    return used / total if total else 0.0


def headroom(used: float, total: float) -> float:
    """The fraction still free; a negative value is an OOM."""
    return (total - used) / total if total else 0.0
```

### Reading the bottleneck

The rule: the bottleneck is the resource at 100% while the others idle.
GPU at
100% with CPU idle is a compute bottleneck (optimize the model); GPU idle with
CPU at 100% is a data-pipeline bottleneck (optimize loading); VRAM full
while
utilization is low is a memory inefficiency (quantize, prune, smaller
batch).

## 4. The Efficiency Ratio

Accuracy per unit of the scarce resource is the number that compares
models
fairly. A 0.91 model at 100 ms beats a 0.92 model at 2 seconds for any
latency
SLO — by a factor of twenty.

```python
def efficiency(quality: float, cost: float) -> float:
    """Quality per unit cost — accuracy/ms, accuracy/GB, accuracy/dollar."""
    return quality / cost if cost else float("inf")
```

This ratio is the basis for every "should we ship the bigger model"
decision.
It also connects to cost (Lecture 15): the cost ledger is the efficiency
ratio
with dollars as the denominator.

## 5. Profiling

### The tools

- **Latency**: time the request path (`time.perf_counter` around inference),
  always as a percentile distribution, never a single number.
- **GPU**: `nvidia-smi` (utilization, VRAM), `torch.profiler` (per-op breakdown).
- **Memory**: peak RSS, and the VRAM high-water mark during the largest batch.
- **End-to-end**: measure the deployed service under load, not just the model in
  a script — the serving stack (queueing, batching) dominates at scale.

```python
import time


def time_request(fn, *args):
    start = time.perf_counter()
    out = fn(*args)
    return (time.perf_counter() - start) * 1000, out  # ms
```

### The discipline

Profile before optimizing. A guess about the bottleneck is wrong often
enough
to waste the optimization budget. The profiler's output — which op,
which
resource — is what chooses quantization, pruning, or a pipeline fix.

## 6. The Metrics Dashboard

The minimum dashboard for a production model is six panels: accuracy
(the task
metric), latency p50/p95/p99, throughput, error rate, GPU utilization +
VRAM,
and cost per 1k requests. These six are the full deployability picture,
and a
regression in any one is a candidate for an alert.

The dashboard is also where the four metric families live together, so a
change
is evaluated on all of them — the same "all four budgets" rule as
section 1,
made visible.

## 7. Resource Metrics in the Lifecycle

- **CI gate (Lecture 12)**: a latency-budget gate and a VRAM-budget gate join the
  eval gate — a candidate that regresses p95 or OOMs does not promote.
- **Registry (Lecture 04)**: the recorded artifact includes the latency and
  memory profile, so a rollback decision has the numbers.
- **Production (Lecture 11)**: utilization and performance indicators are
  monitored with SLOs; a drift in p95 or a VRAM climb triggers an alert.
- **Budgets (Lecture 15)**: the cost ledger keys on these metrics, so a resource
  regression shows up as dollars.

```python
def resource_gate(candidate, limits):
    """A candidate must fit the VRAM ceiling and the latency SLO."""
    if candidate["vram_gb"] > limits["vram_gb"]:
        return False, f"FAIL: VRAM {candidate['vram_gb']} > {limits['vram_gb']}"
    if candidate["latency_p95_ms"] > limits["latency_p95_ms"]:
        return False, f"FAIL: p95 {candidate['latency_p95_ms']} > {limits['latency_p95_ms']}"
    return True, "PASS: resource and latency within budget"
```

## 8. Profiling Tools in Practice

### nvidia-smi: the first look

`nvidia-smi` reports GPU utilization and VRAM in one line — the fastest
way to
answer "is the card working, and is memory full." It is a snapshot, not
a
history; for trends, log it on a schedule.

```bash
nvidia-smi --query-gpu=utilization.gpu,memory.used,memory.total --format=csv -l 5
```

### torch.profiler: the per-op breakdown

When utilization is high but the model is slow, `torch.profiler` shows
which
operation costs the time — a specific matmul, a data transfer, a
synchronization
point. The profiler's output is what chooses quantization, kernel
fusion, or a
pipeline fix, because it replaces the guess with a measurement.

### Per-request timing: the service view

Wrap the inference path with a high-resolution timer and record the
distribution,
not one number. The service view (percentiles) and the profiler view
(per-op)
are complementary: the first says *that* it is slow, the second says
*where*.

### The workflow

Hypothesis → profile → fix → re-measure. A profiling session that does
not end
in a specific change (smaller batch, quantized layer, fixed loader) was
exploration, not engineering. The discipline is the same as debugging:
measure,
change one thing, measure again.

## 9. Capacity Planning

### From metrics to machines

Throughput and latency determine replicas: if one instance serves 50 rps
at the
target p95, and the peak load is 500 rps, you need 10 instances plus
headroom.
The arithmetic is simple; the inputs (real throughput, real peak) must
be
measured, not assumed.

### The headroom rule

Target 70% utilization, not 100%. A system at 100% has no margin for a
traffic
spike or a slow dependency — and latency degrades nonlinearly near
saturation.
Headroom is the insurance that keeps p95 stable when load varies.

### Autoscaling

Queue-based scaling (add replicas when the request queue grows) and
CPU/GPU-based
scaling (add replicas at a utilization threshold) automate the headroom.
The
scaling policy is part of the deployment artifact, and its lag (minutes
to spin
up a GPU instance) is part of the capacity math.

### The cost of getting it wrong

Over-provisioning wastes money; under-provisioning violates the SLO. The
efficiency ratio (`4`) is the language for this trade: the cheapest
fleet that
meets the SLO wins.

## 10. Setting a Latency Budget

### From product to number

The latency SLO comes from the product, not the model. A chatbot needs a
first
token in ~500 ms; a batch job has no interactive SLO; a real-time
bidding system
needs single-digit milliseconds. The product's tolerance is the starting
point,
and the model gets a share of it.

### The decomposition

A request's total budget splits across components: retrieval, model
inference,
and post-processing. If the end-to-end SLO is 500 ms and retrieval takes
200 ms,
the model has 300 ms — minus margin. Each component gets its own
sub-SLO, and
the sum must fit.

### The margin

Leave headroom for variance: the tail, not the mean, and a slow
dependency on a
bad day. A budget with no margin is a budget that fails the first time
traffic
spikes. The margin is the difference between a target and a guarantee.

## Every Use Case

- **Every inference endpoint**: p50/p95/p99, throughput, and error rate on the
  dashboard from day one.
- **Every training run**: GPU utilization and VRAM high-water mark logged with
  the run record (Lecture 02).
- **Every candidate promotion**: the resource gate runs alongside the eval gate.
- **Every GPU purchase or cloud bill**: the efficiency ratio justifies the spend.
- **Every optimization (quantize/prune/distill)**: measured in ms, GB, and
  accuracy — not just accuracy.
- **Every incident review**: utilization at the time of failure is the first chart.
- **Every LLM deployment**: TTFT/TPOT plus the VRAM math (weights + KV cache).

## Real-World Use Cases for AI Engineers

- **API engineer**: a 190 ms p95 against a 200 ms SLO, monitored per release; a
  regression that pushes p95 to 230 ms blocks promotion automatically.
- **GPU-constrained engineer (RTX 5000)**: the VRAM high-water mark says 14.8 GB
  on a 16 GB card, so the batch is cut before the OOM happens in production.
- **Training engineer**: GPU utilization at 40% with a 3-hour epoch exposes an
  IO-bound data pipeline; fixing the loader (not the model) recovers the hours.
- **LLM engineer**: TTFT is fine but TPOT degrades, which points at the KV cache
  (memory) rather than compute — quantize the cache first.
- **Platform engineer**: the cost ledger keys serving dollars to per-request ms,
  so a latency regression shows up as a cost anomaly, not just a chart.

## Common Mistakes to Avoid

### Mistake 1: Reporting accuracy only
A 0.92 that OOMs is not better than a 0.91 that fits. Report all four
families.

### Mistake 2: Mean latency instead of p95/p99
The mean hides the tail users feel. SLOs are percentiles.

### Mistake 3: Confusing throughput and latency
Maximizing one usually hurts the other. Choose by the SLO, not by habit.

### Mistake 4: Optimizing before profiling
A guess about the bottleneck wastes the optimization budget. Measure
first.

### Mistake 5: Ignoring the error rate
An accurate model that crashes is a production failure. Error rate is
the third
production number.

### Mistake 6: No resource gate in CI
A candidate that regresses p95 or exceeds VRAM ships silently. Gate it
like the
eval metric.

### Mistake 7: One measurement, assumed eternal
Latency and memory drift with data, batching, and traffic. Monitor, do
not assume.

## Best Practices

1. Report accuracy, latency, resources, and cost together — always
2. SLO on p95/p99, never on the mean
3. Choose throughput versus per-request latency by the product need
4. Read the bottleneck: the saturated resource names the fix
5. Profile before optimizing; optimize the measured bottleneck only
6. Gate promotion on resources and latency alongside accuracy
7. Record the profile in the registry with the model version
8. Monitor all six dashboard panels in production
9. Key cost anomalies to the same resource metrics
10. Size the batch from the VRAM high-water mark, not from hope

## Complexity and Cost

| Operation | Time | Space | Cheaper alternative |
|---|---|---|---|
| Latency profiling | O(requests) | O(samples) | sample a subset of traffic |
| GPU utilization read | `nvidia-smi`, instant | O(1) | — |
| Full profiler run | O(one batch) | O(trace) | profile the hot path only |
| VRAM high-water mark | one max batch | O(1) | estimate from weights + cache |
| Production monitoring | continuous | O(metrics) | downsampled retention |

## AI Engineering Relevance

**Where this shows up:** every deployability decision. Resource and performance
metrics are the language in which "it runs" is stated, measured, and
gated.

| Concept here | Used for |
|---|---|
| Percentile latency | SLOs users actually feel |
| Throughput | Capacity planning and batching |
| GPU/VRAM utilization | Finding the bottleneck resource |
| Efficiency ratio | Comparing models fairly |
| Profiling | Choosing the right optimization |

**Scale note:** at one model the metrics are a dashboard; at fifty they are the
gates that keep bad candidates out of production. The percentile, the
high-water
mark, and the efficiency ratio are the three numbers that scale from one
GPU to
a fleet.

## Practice Exercises

### Exercise 1: Percentiles (Easy)
Implement `percentile(latencies, q)` and compute p50/p95/p99 on a mixed
distribution; show the mean hiding the tail.

### Exercise 2: Throughput (Medium)
Implement `throughput(requests, seconds)` and a batch-size sweep showing
the
latency/throughput trade-off.

### Exercise 3: Bottleneck Reader (Medium)
Implement `find_bottleneck(utilization: dict)` returning the saturated
resource
and the recommended fix (model vs pipeline vs memory).

### Exercise 4: Resource Gate (Hard)
Implement `resource_gate(candidate, limits)` and integrate it with an
accuracy
check so promotion requires all four metric families; write the
pass/fail/OOM
cases as tests.

## Summary

| Concept | Description |
|---|---|
| Deployability | Accuracy + latency + resources + cost, all within budget |
| Percentiles | p50/p95/p99; the tail is the SLO |
| Throughput | Requests per second; trades against per-request latency |
| Utilization | Used/total per resource; the saturated one is the bottleneck |
| Efficiency | Quality per unit of the scarce resource |

A model is not done when it is accurate; it is done when it is accurate,
fast enough, small enough, and cheap enough. Resource and performance
metrics
are how that claim is made, gated, and monitored.

## Quick Reference

| Task | Idiom |
|---|---|
| p95 latency | sorted tail, not the mean |
| Bottleneck | the resource at 100% while others idle |
| VRAM budget | weights + KV cache + activations <= card |
| Efficiency | accuracy / ms, /GB, /dollar |
| Profile first | `nvidia-smi` + per-request timing + `torch.profiler` |
| Promotion | accuracy gate + resource gate + cost within budget |

## Next Steps

Next: **[20 Continuous Training](20-continuous-training-lecture.md)** —
when and
how a model is rebuilt automatically.
Continues in: **[Phase 8 MLOps](../../08-mlops/README.md)**.
Official docs:
https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html




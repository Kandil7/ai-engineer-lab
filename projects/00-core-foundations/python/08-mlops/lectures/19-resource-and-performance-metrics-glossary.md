# Resource and Performance Metrics — Glossary 19

## Quick Reference Table
| Term | Category | One-Line Definition |
|---|---|---|
| Latency | Performance | Time from request to response |
| Percentile | Performance | The value below which a share of requests fall |
| p95 / p99 | Performance | The tail: 95th and 99th percentile request |
| Throughput | Performance | Requests served per second |
| Error rate | Performance | Fraction of requests that fail or time out |
| Utilization | Resource | Used divided by total for a resource |
| VRAM | Resource | GPU memory; the hard ceiling on a card |
| Headroom | Resource | The fraction of a resource still free |
| Bottleneck | Diagnosis | The saturated resource while others idle |
| Efficiency ratio | Comparison | Quality per unit of a scarce resource |
| High-water mark | Resource | The peak memory observed during a run |
| SLO | Policy | A percentile target a service must meet |

## Detailed Definitions
### Latency
**Definition**: The time from request arrival to response return, measured per
request and summarized as a percentile distribution.
**Related**: Percentile, Throughput

### Percentile / p95 / p99
**Definition**: The latency value below which the given share of requests fall;
p95 is the tail users feel, which is why SLOs are percentiles, not means.
```python
ordered[int(0.95 * len(ordered))]
```
**Related**: SLO, Error rate

### Throughput
**Definition**: Requests served per second; rises with batch size and falls with
latency. Maximizing it usually hurts per-request latency.
**Related**: Latency, Bottleneck

### Error rate
**Definition**: The fraction of requests that fail, time out, or return the
wrong shape; the third production number alongside latency and accuracy.
**Related**: SLO

### Utilization / VRAM / headroom
**Definition**: `used / total` for a resource; VRAM is the GPU-memory ceiling
(weights + KV cache + activations); headroom is what remains free.
**Related**: Bottleneck, High-water mark

### Bottleneck
**Definition**: The resource at 100% while the others idle; it names the fix
(model for GPU, pipeline for CPU, memory for VRAM).
**Related**: Utilization, Efficiency ratio

### Efficiency ratio
**Definition**: Quality divided by cost (accuracy per ms, per GB, per dollar) —
the number that compares models fairly across sizes.
**Related**: Bottleneck

### High-water mark
**Definition**: The peak memory observed, usually at the largest batch; the
number that sizes the batch against the card.
**Related**: VRAM

### SLO
**Definition**: A service-level objective — a percentile target (e.g. p95 under
200 ms) the service must meet, with alerts on breach.
**Related**: Percentile, Error rate

## Key Concepts Summary
### Deployability is four budgets
- Accuracy, latency, resources, cost — all must clear.

### The tail and the bottleneck
- SLO on p95/p99; the saturated resource names the fix.

### Measure before optimizing
- Profile first; optimize the measured bottleneck only.

## Practice Terms
Match each term to its definition (answers at the bottom).
1. p95 — ___
2. Throughput — ___
3. Utilization — ___
4. Headroom — ___
5. Efficiency ratio — ___

**Answers:** 1-e, 2-b, 3-c, 4-d, 5-a where a=quality per unit cost,
b=requests per second, c=used divided by total, d=the fraction still free,
e=the tail 95% of requests beat.

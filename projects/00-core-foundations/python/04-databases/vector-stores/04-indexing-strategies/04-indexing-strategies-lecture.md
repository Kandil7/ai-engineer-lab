# Databases — 04: Indexing Strategies (Tuning HNSW, Quantization)

## Topic Overview

Knowing HNSW parameters (topic 02) is not the same as setting them. This
lecture is the operating discipline: grid-sweep M against ef_search, read the
recall-latency knee, choose scalar or binary quantization for the RAM budget,
and record every decision so the next engineer reproduces the index instead
of rediscovering it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Run an M × ef_search grid and plot recall@k against p95 latency
2. Identify the knee and defend it as the operating point
3. Choose scalar vs binary quantization from a RAM budget, with the recall cost stated
4. Explain when to rebuild (ef_construction, M) vs retune live (ef_search)
5. Document an index configuration as a reproducible record, not tribal knowledge

## Prerequisites

| Need | Where |
|---|---|
| HNSW knobs and the tradeoff curve | [02](../02-ann-algorithms/02-ann-algorithms-lecture.md) |
| Exact baseline for recall | [03](../03-exact-knn/03-exact-knn-lecture.md) |
| The runnable exercise | [04-indexing-strategies.py](04-indexing-strategies.py) |

## 1. The Sweep Protocol

Fix the corpus, the query sample (≥200 queries or the curve wobbles), and
the latency budget first. Then grid M ∈ {8, 16, 32} against ef_search ∈
{16, 32, 64, 128}, measuring recall@k and p95 per cell. The plot rises
steeply then flattens — the knee is the point where doubling latency buys
<0.5pp recall. Anything past the knee is vanity compute.

```python
# Per cell, record the full tuple — a recall number without its config is trivia:
# (M, ef_search, recall@10, p95_ms, index_MB, build_s)
record = {"M": 16, "ef_search": 64, "recall@10": 0.971,
          "p95_ms": 38.0, "index_MB": 412.0, "build_s": 190.0}
```

## 2. Quantization From the RAM Budget

Work backwards from RAM: collection bytes must fit with headroom for growth
and the OS page cache. Scalar quantization (float32 → int8, ~4x) costs
~1pp recall on most text workloads; binary (~32x) costs more and suits
first-stage retrieval followed by exact re-rank. The rule: quantize until the
recall delta exceeds the budget, then step back one level.

## 3. Rebuild vs Retune

Live-tunable without a rebuild: ef_search only. Everything else — M,
ef_construction, quantization level, distance metric — requires rebuilding
the index, which means a build pipeline, a shadow collection, and a recall
gate before cutover. If your operating point needs a rebuild-monthly cadence,
say so in the config record; silent index drift is how recall rots.

## 4. The Config Record

One file per collection: parameters, corpus snapshot id, query sample id,
measured recall@k and p95, RAM footprint, date, owner. The DevMate vector
store ADR (weeks 2–3) is this record at decision scale — same fields, plus
the contender it beat and why.

## Common Mistakes

- Tuning on 20 queries and shipping the noise.
- Recording recall without the M/ef_search/RAM tuple that produced it.
- Binary quantization everywhere because "32x smaller" — then precision dies.

## DevMate Connection

The Qdrant-vs-Chroma ADR is won by whoever runs this protocol on both
contenders with the same corpus, queries, and budget. `index_MB` maps to the
infra bill; `p95_ms` maps to the weeks 2–3 performance budget (retrieve
<100 ms); recall@10 maps to the eval harness. One sweep, three milestone
deliverables fed.

## Key Takeaways

1. Sweep the grid, find the knee, stop there.
2. Quantize backwards from the RAM budget.
3. ef_search retunes live; everything else rebuilds.
4. A config without its measurement tuple is trivia.

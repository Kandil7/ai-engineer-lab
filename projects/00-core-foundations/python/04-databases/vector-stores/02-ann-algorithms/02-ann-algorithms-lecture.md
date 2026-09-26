# Databases — 02: ANN Algorithms (HNSW, IVF, Quantization)

## Topic Overview

Brute force costs O(n*d) per query and dies around millions of vectors. This
lecture covers the three ideas that replace it: HNSW graph search (what Qdrant
runs by default), IVF partitioning (what sweeps the corpus down to a few
buckets), and product quantization (what shrinks the vectors themselves). Each
trades a little recall for a lot of speed — and recall@k from topic 01 prices
each trade.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Trace an HNSW search: enter at the top layer, greedy-descend, beam-search the base layer
2. Explain M, ef_construction, and ef_search as build-time vs query-time knobs
3. Explain IVF: coarse quantizer picks buckets, search scans only those
4. Explain product quantization: split vector into subspaces, replace each with a code
5. State the failure mode of each: HNSW hub nodes, IVF missed buckets, PQ distortion
6. Read a recall-vs-latency curve and pick an operating point with a latency budget

## Prerequisites

| Need | Where |
|---|---|
| Similarity metrics, brute force, recall@k | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| The runnable exercise | [02-ann-algorithms.py](02-ann-algorithms.py) |

## 1. HNSW: Navigable Small Worlds

HNSW builds a layered graph. Upper layers are sparse long-range links;
the base layer is a dense neighborhood graph where each node connects to
about M neighbors. Search enters at the top, greedily walks to the nearest
node, drops a layer, and repeats; at the base layer a beam search of width
ef_search refines the candidates. Query cost is roughly logarithmic in n.

```python
# The three knobs, and who pays for each:
# M               — neighbors per node: index size + build time (build-time)
# ef_construction — beam width at build: index quality (build-time)
# ef_search       — beam width at query: recall vs latency (QUERY-time)
#
# Rule of thumb: raise ef_search until recall@k stops moving, then stop.
# It is the only knob you can turn without rebuilding the index.
```

Reference: Malkov & Yashunin, arXiv:1603.09320.

## 2. IVF: Partition First, Search Second

Inverted-file indexing clusters the corpus into buckets (a coarse quantizer,
usually k-means) and at query time searches only the nearest few buckets.
Fewer buckets searched means faster queries and lower recall — the number of
probed buckets is the dial. IVF pairs well with quantization: small codes,
few buckets, huge corpora.

Reference: Jégou et al., arXiv:1104.1453.

## 3. Product Quantization: Shrink the Vectors

Split a d-dimensional vector into m subspaces; replace each sub-vector with
the id of its nearest centroid (learned per subspace). A 768-float vector
becomes m bytes. Distances are approximated from lookup tables, so queries
stay fast and RAM stays small. The price is distortion: fine distinctions
between near-duplicates blur, which is exactly where reranking (weeks 2–3)
earns its keep.

## 4. Reading the Tradeoff Curve

Fix a latency budget (say p95 < 100 ms), sweep ef_search or bucket count,
plot recall@k. The curve rises steeply then flattens — the operating point is
the knee, not the maximum. Topic 04 turns this into a mechanical sweep; this
lecture is the theory that makes the sweep interpretable instead of random.

## Common Mistakes

- Tuning ef_construction at query time (it is baked into the built graph).
- Probing one IVF bucket and wondering where recall went.
- Comparing indexes by latency without fixing recall@k first.

## DevMate Connection

Qdrant's default index is HNSW — ADR-0005's comparison rests on understanding
M/ef_search well enough to configure both contenders fairly. The weeks 2–3
`VectorStore` Protocol hides the index behind an interface, but the eval
harness measures through it: recall@5/10 is the recall@k of this lecture at
DevMate's operating point.

## Key Takeaways

1. HNSW: layered graph, logarithmic search, ef_search is the live knob.
2. IVF: bucket the corpus, probe a few; buckets probed is the dial.
3. PQ: compress vectors to codes; distortion is paid in near-duplicate ranking.
4. Fix latency, sweep, read recall@k — the knee is the operating point.

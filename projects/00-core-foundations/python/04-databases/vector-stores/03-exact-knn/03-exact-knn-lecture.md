# Databases — 03: Exact kNN (Brute Force)

## Topic Overview

Approximate indexes are only meaningful against an exact baseline, and
small corpora never need anything else. This lecture makes brute-force kNN
a precision instrument: distance metrics compared on the same data,
argpartition for top-k without a full sort, and the dimensionality analysis
that tells you when exact search stops being viable.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Implement exact kNN with numpy in O(n*d) time and O(n) extra space
2. Use argpartition to get top-k without paying O(n log n) for a full sort
3. Compare L2 vs cosine rankings on the same corpus and explain divergences
4. State when exact search is the right production choice (small n, eval baselines)
5. Produce the ground-truth rankings every ANN recall measurement needs

## Prerequisites

| Need | Where |
|---|---|
| Metrics and brute-force cost | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| The runnable exercise | [03-exact-knn.py](03-exact-knn.py) |

## 1. Exact kNN, No Shortcuts

```python
import numpy as np

def exact_knn(query, corpus, k, metric="cosine"):
    if metric == "cosine":
        qn = query / np.linalg.norm(query)
        cn = corpus / np.linalg.norm(corpus, axis=1, keepdims=True)
        scores = cn @ qn                    # higher wins
        idx = np.argpartition(-scores, k)[:k]
        order = idx[np.argsort(-scores[idx])]
    else:
        dists = np.linalg.norm(corpus - query, axis=1)   # smaller wins
        idx = np.argpartition(dists, k)[:k]
        order = idx[np.argsort(dists[idx])]
    return order
```

`argpartition` puts the top-k in place in O(n) — the full sort only touches
k elements. On small corpora this whole function *is* the retriever.

## 2. L2 vs Cosine on the Same Data

Run both rankings on one corpus and diff them. Divergences come from
magnitude: vectors with large norms dominate dot/L2 rankings while cosine
ignores them. In text retrieval corpus vectors are usually normalized, so the
rankings agree — when they don't, the first suspect is an unnormalized write
path, not a broken metric.

## 3. When Exact Wins

Exact search is the production choice when n is small (thousands, not
millions), when determinism matters (eval baselines, regression tests), and
whenever anyone claims an index improvement — the claim is priced against
this function. DevMate's eval harness keeps a brute-force path for exactly
this reason: recall@k needs truth, and truth is O(n*d).

## 4. Dimensionality Reality Check

Cost scales with n AND d. Doubling dimensions doubles brute-force time but
barely moves HNSW query time (graph hops, not scans). That asymmetry is the
one-paragraph explanation of why high-dimensional embeddings killed exact
search in production while keeping it alive in evaluation.

## Common Mistakes

- Full `argsort` on millions of rows to get top-10.
- Forgetting L2 sorts ascending while cosine sorts descending.
- Dropping the exact baseline "because ANN is faster" — then recall is undefined.

## DevMate Connection

The weeks 2–3 eval harness computes recall@5/10 and MRR. Every one of those
numbers divides by a brute-force truth set produced by this lecture's
function. Keep an exact path in the `VectorStore` Protocol — it is the
cheapest correctness insurance in the whole retrieval stack.

## Key Takeaways

1. argpartition top-k: O(n), no full sort.
2. L2/cosine divergences mean magnitude is leaking in — usually unnormalized writes.
3. Exact search stays in production for small n and in evals forever.

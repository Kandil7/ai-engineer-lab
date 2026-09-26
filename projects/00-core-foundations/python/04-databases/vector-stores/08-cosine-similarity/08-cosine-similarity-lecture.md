# Databases — 08: Cosine Similarity (The Unit-Vector Identity)

## Topic Overview

Cosine similarity is used everywhere in retrieval and understood shallowly
almost as often. This lecture goes one level deeper than topic 01: the exact
algebra that makes dot product equal cosine on normalized vectors, why
stores normalize on write, what breaks when they don't, and how to verify
normalization in a pipeline you didn't build.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Prove the unit-vector identity: cos(a,b) = a·b when ||a|| = ||b|| = 1
2. Explain why vector stores normalize on write (cheaper dot product at query)
3. Detect unnormalized vectors from ranking anomalies
4. Choose the stored metric (cosine vs dot vs L2) from the write path you control
5. Verify a third-party index's metric claims with probe queries

## Prerequisites

| Need | Where |
|---|---|
| The three metrics | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| Exact rankings | [03](../03-exact-knn/03-exact-knn-lecture.md) |
| The runnable exercise | [08-cosine-similarity.py](08-cosine-similarity.py) |

## 1. The Identity, Proved

```python
import numpy as np

# cosine(a, b) = a.b / (||a|| * ||b||). If ||a|| = ||b|| = 1:
# cosine(a, b) = a.b / 1 = a.b. That is the whole trick.
a = np.array([3.0, 4.0]); b = np.array([1.0, 0.0])
print(np.dot(a, b))                                        # 3.0 (meaningless scale)
an, bn = a / np.linalg.norm(a), b / np.linalg.norm(b)
print(np.dot(an, bn), np.dot(an, bn) / (np.linalg.norm(an) * np.linalg.norm(bn)))  # equal
```

## 2. Normalize on Write

Normalizing at ingest means every query pays one cheap dot product instead
of two norms plus a division per comparison. At millions of comparisons per
second that division matters. The store's "cosine" index is very often a
dot-product index over pre-normalized vectors — same rankings, less arithmetic.

## 3. When It Breaks

Unnormalized writes poison dot-product rankings: long documents (large norms)
float to the top regardless of relevance. Symptoms: rankings correlate with
document length, short precise matches buried. Diagnosis: check norms of
stored vectors (variance near zero means normalized); fix the write path,
then re-ingest — no query-side patch repairs bad stored geometry.

## 4. Verifying a Store's Claims

Probe any index with known vectors: insert orthogonal pairs (cosine 0),
duplicates (cosine 1), and scaled copies (cosine 1 iff magnitude-free). If
scaled copies rank differently, the "cosine" index is really dot product over
unnormalized data. Three probes, total certainty about the metric you pay for.

## Common Mistakes

- Assuming "cosine index" means cosine arithmetic (usually dot over normalized).
- Normalizing queries but not the corpus (or vice versa).
- Tuning relevance when the bug is unnormalized writes.

## DevMate Connection

The Qdrant adapter configures the collection metric explicitly — this lecture
is what makes that one-line choice deliberate rather than copied. Eval deltas
after any re-ingest get checked against norm statistics first, ranking
theories second.

## Key Takeaways

1. cos = dot on unit vectors; the proof is one line.
2. Normalize on write; dot product at query.
3. Length-correlated rankings mean unnormalized data — re-ingest, don't retune.
4. Probe orthogonal/duplicate/scaled triples to verify any store's metric claim.

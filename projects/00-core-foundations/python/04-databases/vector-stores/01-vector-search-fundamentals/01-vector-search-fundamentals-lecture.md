# Databases — 01: Vector Search Fundamentals

## Topic Overview

RAG retrieval quality starts before any database: a query is embedded, the
corpus is embedded, and "most similar" means nearest in vector space. This
lecture builds that foundation with numpy only — embeddings as points, the
three similarity metrics, brute-force kNN, and the recall-vs-latency tradeoff
that motivates every approximate index you will meet in topic 02.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what an embedding is geometrically: a point where distance means dissimilarity
2. Compute cosine similarity, dot product, and L2 distance by hand on small vectors
3. State exactly when dot product equals cosine similarity (unit-normalized vectors)
4. Implement brute-force kNN and state its cost: O(n*d) per query
5. Measure retrieval quality with recall@k against a brute-force baseline
6. Explain why exact search fails at scale, motivating ANN indexes

## Prerequisites

| Need | Where |
|---|---|
| numpy basics (arrays, norms, argsort) | `03-libraries/numpy/` |
| The runnable exercise | [01-vector-search-fundamentals.py](01-vector-search-fundamentals.py) |

## 1. Embeddings Are Points

A text embedding model maps a string to a vector of floats, typically a few
hundred to a few thousand dimensions. The training objective places
semantically similar texts near each other. "Near" needs a metric — that is
section 2 — but the geometric intuition comes first: retrieval is not keyword
matching, it is nearest-neighbor lookup in a learned space.

```python
import numpy as np

# Same idea as embed_text() in the exercise: coordinates carry meaning.
q = np.array([0.9, 0.1, 0.0])  # "vector search retrieval"
c1 = np.array([0.8, 0.2, 0.1])  # near-duplicate wording
c2 = np.array([0.0, 0.1, 0.9])  # unrelated topic
```

## 2. Three Metrics, One Decision

```python
def cosine_sim(a, b):
    return float(np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b)))


def dot_sim(a, b):
    return float(np.dot(a, b))


def l2_dist(a, b):
    return float(np.linalg.norm(a - b))
```

- **Cosine similarity** measures angle, ignoring magnitude. Range −1 to 1.
  The default for text retrieval.
- **Dot product** mixes angle and magnitude. It equals cosine similarity
  **only when both vectors are unit-normalized** — most embedding stores
  normalize on write exactly so the cheaper dot product can be used.
- **L2 distance** measures straight-line distance; smaller is more similar.
  Sensitive to magnitude, so normalize first or know why you didn't.

```python
print(cosine_sim(q, c1), cosine_sim(q, c2))  # 0.99... vs 0.11...
```

## 3. Brute-Force kNN and Its Cost

Score every corpus vector against the query, keep the top k. Cost per query
is O(n*d): n corpus vectors times d dimensions. At n = 10^4 and d = 768 that
is ~8M multiply-adds — fine. At n = 10^7 it is ~8G — not fine, and this is
the entire reason topic 02 exists. Brute force never disappears, though: it
remains the **ground truth** that approximate indexes are measured against.

## 4. Recall@k: Measuring Against Truth

An approximate index returns *candidate* neighbors; recall@k is the fraction
of the true top-k it recovered. If brute force says the answers are {A, B, C}
and the index returns {A, C, D}, recall@3 = 2/3. Every index decision in this
module is a point on the recall-vs-latency curve, and recall@k is the axis
that keeps vendors honest.

## Common Mistakes

- Comparing dot products of unnormalized vectors and calling it cosine similarity.
- Forgetting that L2 is a distance (smaller wins) while cosine is a similarity.
- Benchmarking an ANN index without a brute-force baseline to compute recall.

## DevMate Connection

Weeks 2–3 build exactly this pipeline: embed the repo, store it in Qdrant
(ADR-0005), retrieve dense candidates, and measure recall@5/10 and MRR with
`devmate/eval/run_ragas.py`. The `VectorStore` Protocol exists so the Qdrant
adapter can be swapped and re-measured — the recall@k discipline from this
lecture is what makes that comparison mean something.

## Key Takeaways

1. Retrieval is nearest-neighbor search in embedding space.
2. Cosine is the default metric; dot product matches it on normalized vectors.
3. Brute-force kNN costs O(n*d) and is the ground truth for recall@k.
4. Recall@k against brute force is how every faster index earns its place.

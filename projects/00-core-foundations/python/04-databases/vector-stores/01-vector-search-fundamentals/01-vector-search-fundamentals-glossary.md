# Vector Stores 01: Vector Search Fundamentals — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Embedding | Dense float vector placing a text in semantic space | 768-dim query vector |
| Cosine similarity | Angle-based similarity, −1 to 1, magnitude-free | 0.93 = near-duplicate |
| Dot product | Angle × magnitude similarity; equals cosine on unit vectors | Qdrant dot-product index |
| L2 distance | Straight-line distance; smaller means more similar | Post-filter re-rank |
| kNN | The k nearest vectors to a query under a metric | top-5 chunks for a question |
| Brute force | Exact search scoring all n vectors: O(n*d) | recall@k ground truth |
| Recall@k | Fraction of true top-k an index recovers | 2/3 when one answer missed |

---

## Alphabetical Glossary

### Brute force

**Definition:** Exact nearest-neighbor search that scores every corpus vector
against the query. O(n*d) per query — too slow at scale, but the ground truth
all approximate indexes are measured against.

**Example:**
```python
scores = [cosine_sim(q, c) for c in corpus]  # all n, then top-k
```

**Related concepts:** kNN, Recall@k, ANN

---

### Cosine similarity

**Definition:** Dot product divided by both norms; measures angle between
vectors, ignoring magnitude. The default metric for text embeddings.

**Example:**
```python
cosine_sim(q, related)  # 0.926 — same topic, different words
```

**Related concepts:** Dot product, Normalization, L2 distance

---

### Dot product

**Definition:** Sum of element-wise products. Mixes direction and magnitude,
so it equals cosine similarity only on unit-normalized vectors.

**Example:**
```python
dot_sim(q, c)  # valid stand-in for cosine after normalizing on write
```

**Related concepts:** Cosine similarity, Normalization

---

### Embedding

**Definition:** A dense vector of floats produced by a model, where geometric
nearness tracks semantic similarity. Queries and corpus share the space.

**Example:**
```python
q = embed_text("vector search retrieval", dim=16)
```

**Related concepts:** Vector, kNN, Cosine similarity

---

### kNN

**Definition:** k-nearest neighbors: the k corpus vectors closest to the query
under the chosen metric. The retrieval primitive of every RAG system.

**Example:**
```python
brute_force_knn(q, corpus, k=5)  # indices of the 5 best chunks
```

**Related concepts:** Brute force, Recall@k, ANN

---

### L2 distance

**Definition:** Euclidean (straight-line) distance between vectors. A distance,
not a similarity: smaller wins. Magnitude-sensitive unless normalized.

**Example:**
```python
l2_dist(q, c)  # 0.2 = near, 1.7 = far (on unit vectors)
```

**Related concepts:** Cosine similarity, Normalization

---

### Recall@k

**Definition:** Fraction of the true (brute-force) top-k that a candidate
result set recovers. The honesty metric for approximate indexes.

**Example:**
```python
recall_at_k(exact_topk, approx_topk)  # 0.67 when one of three is missed
```

**Related concepts:** Brute force, kNN, MRR

---

## Related Concepts

- **ANN**: approximate indexes that trade recall for speed (topic 02)
- **Normalization**: unit-length scaling that aligns dot product with cosine (topic 08)
- **MRR**: mean reciprocal rank — rewards the first correct hit, used in DevMate evals

## Key Takeaways

1. Retrieval is geometry: nearness in embedding space.
2. Cosine by default; dot product only on normalized vectors.
3. Brute force is slow and indispensable — it defines recall@k.

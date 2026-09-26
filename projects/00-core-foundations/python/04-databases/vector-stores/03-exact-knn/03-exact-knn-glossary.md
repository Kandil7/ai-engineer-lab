# Vector Stores 03: Exact kNN — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Exact search | Scores all n vectors; recall 1.0 by definition | eval baseline |
| argpartition | O(n) partial selection of top-k without full sort | top-10 of 1M rows |
| Curse of dimensionality | Distance contrasts fade as d grows; exact cost scales with d | 768-dim embeddings |
| Determinism | Same query, same ranking, every run | regression tests |
| Ground truth | Brute-force rankings that define recall | ANN acceptance gate |

---

## Alphabetical Glossary

### argpartition

**Definition:** numpy partial sort placing the k-th element correctly with all
smaller (or larger) unordered before it. Top-k selection in O(n).

**Example:**
```python
idx = np.argpartition(-scores, 10)[:10]  # top-10, unsorted; sort only these
```

**Related concepts:** Exact search, kNN

---

### Curse of dimensionality

**Definition:** As dimensions grow, pairwise distances concentrate and exact
search cost scales linearly with d. The reason high-dim embeddings need ANN
in production while keeping exact search for evaluation.

**Example:**
```python
# d=768: brute force 8M ops per query at n=10^4; HNSW barely notices d
```

**Related concepts:** ANN, Exact search

---

### Determinism

**Definition:** Exact search returns identical rankings every run — no
sampling, no approximation. Required for regression tests and eval truth.

**Example:**
```python
# golden-set evals pin the exact path so metric deltas mean code changes
```

**Related concepts:** Ground truth, Recall@k

---

### Exact search

**Definition:** Nearest-neighbor search with no approximation: every vector
scored, true top-k returned. O(n*d); recall 1.0 by definition.

**Example:**
```python
exact_knn(q, corpus, k=5)  # the truth set for recall@5
```

**Related concepts:** Brute force, ANN, Ground truth

---

### Ground truth

**Definition:** The exact rankings used as the denominator of recall and the
reference of regression tests. Produced by exact search, versioned with the
eval set.

**Example:**
```python
# evaluations/rag/datasets/*-golden.jsonl pairs questions with known sources
```

**Related concepts:** Exact search, Recall@k, Golden set

---

## Related Concepts

- **Golden set**: question-to-source pairs encoding expected retrieval (DevMate weeks 2–3)
- **MRR**: rewards the rank of the first correct hit
- **ANN**: what replaces exact search when n outgrows it (topic 02)

## Key Takeaways

1. Exact search is slow, deterministic, and irreplaceable as truth.
2. argpartition makes top-k O(n).
3. Keep the exact path in every vector interface.

# Vector Stores 05: Hybrid Search — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hybrid search | Dense + keyword arms fused per query | DevMate retrieve/ |
| BM25 | Term-overlap ranking with IDF, saturation, length norm | exact error-code lookup |
| Dense retrieval | Embedding nearest-neighbor arm | paraphrase-tolerant search |
| Sparse vector | Mostly-zero term-weight vector | BM25 over vocab |
| RRF | Rank-based fusion: sum 1/(60+rank), no normalization | two-arm merge |
| Score normalization | Per-query min-max scaling before weighted sums | cosine + BM25 merge |
| Arm attribution | Per-arm recall measured to blame the right side | dense 0.9 / BM25 0.4 |

---

## Alphabetical Glossary

### Arm attribution

**Definition:** Measuring each retrieval arm's recall separately so fixes land
on the failing side. Fusion-level debugging without it is guesswork.

**Example:**
```python
# golden miss: dense recall 1.0, BM25 recall 0.0 -> fix tokenization, not weights
```

**Related concepts:** Hybrid search, Recall@k

---

### BM25

**Definition:** Best Match 25: keyword ranking with inverse document frequency,
term-frequency saturation, and length normalization. Exact-token strength,
synonym blindness.

**Example:**
```python
# query "ef_search": changelog hits rank top; paraphrase queries sink
```

**Related concepts:** Sparse vector, IDF

---

### Dense retrieval

**Definition:** Nearest-neighbor search over embedding vectors. Paraphrase
strength, exact-token blindness. The semantic arm of hybrid search.

**Example:**
```python
# "tuning guide" matches "recall-latency tradeoffs" with zero shared tokens
```

**Related concepts:** Hybrid search, Embedding

---

### Hybrid search

**Definition:** Running dense and keyword retrieval per query and fusing the
rankings. Covers both failure directions at the cost of two arms to maintain.

**Example:**
```python
# devmate retrieve/: dense candidates + BM25 candidates -> RRF -> rerank
```

**Related concepts:** BM25, Dense retrieval, RRF

---

### RRF

**Definition:** Reciprocal Rank Fusion: per-document sum of 1/(k+rank), k=60
conventionally. Fuses rankings without normalizing incompatible scores.

**Example:**
```python
rrf([dense_top10, bm25_top10])  # rank 1 in both arms dominates fairly
```

**Related concepts:** Score normalization, Hybrid search

---

### Score normalization

**Definition:** Rescaling each arm's scores (e.g., per-query min-max to
[0,1]) so weighted fusion compares like with like. Unneeded under RRF.

**Example:**
```python
# cosine [-1,1] and BM25 [0,inf) must never be added raw
```

**Related concepts:** RRF, Hybrid search

---

### Sparse vector

**Definition:** High-dimensional, mostly-zero vector of term weights (one
dimension per vocabulary term). The BM25 representation.

**Example:**
```python
# 50k-dim vector, ~12 nonzero entries for a short query
```

**Related concepts:** BM25, Dense retrieval

---

## Related Concepts

- **Reranking**: cross-encoder rescoring of fused candidates (DevMate weeks 2–3)
- **IDF**: down-weights terms appearing in many documents
- **Golden set**: decides fusion weights empirically

## Key Takeaways

1. Two arms, opposite blind spots, one fusion.
2. RRF dodges normalization; weighted sums need it.
3. Attribute failures per arm before touching anything.

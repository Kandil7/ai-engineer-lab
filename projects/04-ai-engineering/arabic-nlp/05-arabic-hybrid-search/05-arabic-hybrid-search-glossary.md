# Arabic NLP 05: Hybrid Search and Reranking — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Hybrid search | Lexical + dense arms fused per query | BM25 + embeddings |
| RRF | Rank-based fusion: sum 1/(k+rank) | no normalization needed |
| Reranker | Cross-encoder scoring (query, passage) pairs | top-50 → top-5 |
| Cross-encoder | Joint model scoring pairs, accurate but slow | rerank stage |
| Bi-encoder | Separate embeddings, fast but coarse | dense arm |
| Fusion weight | Relative arm influence in the merge | RRF k, arm weights |
| Golden set | Labeled pairs measuring all three rows | hybrid vs single-arm |

---

## Alphabetical Glossary

### Bi-encoder

**Definition:** The embedding model encoding query and passage separately.
Fast and corpus-scalable, but coarser than joint scoring.

**Example:**
```python
q = embed(query)
p = embed(passage)
cos(q, p)
```

**Related concepts:** Cross-encoder, Dense arm

---

### Cross-encoder

**Definition:** A model scoring (query, passage) jointly. Far more accurate
than bi-encoder cosine, too slow for the full corpus — hence the rerank stage.

**Example:**
```python
score = cross_encoder(query, passage)  # joint, accurate
```

**Related concepts:** Bi-encoder, Reranker

---

### Fusion weight

**Definition:** The relative influence of each arm in the merged ranking.
Tuned on the golden set; on Arabic, neither arm should drown the other.

**Example:**
```python
# RRF k, or weighted score sums after normalization
```

**Related concepts:** RRF, Golden set

---

### Golden set

**Definition:** The labeled query-to-passage pairs measuring lexical, dense,
and hybrid recall@k. The arbiter of fusion tuning.

**Example:**
```python
# three rows: lexical 0.81, dense 0.78, hybrid 0.90
```

**Related concepts:** Recall@k, Fusion weight

---

### Hybrid search

**Definition:** Running lexical and dense retrieval per query and fusing the
rankings. Covers both failure directions at the cost of two arms.

**Example:**
```python
# BM25 top-k + dense top-k -> RRF -> rerank
```

**Related concepts:** RRF, Reranker

---

### Reranker

**Definition:** The cross-encoder stage rescoring fused candidates. Fixes
near-duplicate misranking that both arms share.

**Example:**
```python
rerank(fused_top50, query)  # -> top-5
```

**Related concepts:** Cross-encoder, Hybrid search

---

### RRF

**Definition:** Reciprocal Rank Fusion: per-document sum of 1/(k+rank),
k=60 conventionally. Fuses rankings without normalizing incompatible scores.

**Example:**
```python
rrf([lexical_top10, dense_top10])
```

**Related concepts:** Hybrid search, Fusion weight

---

## Related Concepts

- **Lexical arm**: exact-match strength (topic 03)
- **Dense arm**: meaning-match strength (topic 04)
- **Recall@k**: the measurement across all three rows

## Key Takeaways

1. Fuse by rank, rerank the union.
2. RRF needs no score normalization.
3. Hybrid must beat both arms — measure all three.
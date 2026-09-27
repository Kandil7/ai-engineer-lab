# RAG System 03: Reranking — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Bi-encoder | Separate query/chunk embeddings, fast and coarse | candidate finding |
| Cross-encoder | Joint (query, chunk) scoring, accurate and slow | candidate reordering |
| Rerank depth | Number of fused candidates rescored | top-50 → top-5 |
| Reranker | The cross-encoder stage after fusion | last quality lever |
| No-rerank baseline | Recall without the reranker | contribution measure |
| Latency budget | The time ceiling for reranking | < 150 ms |
| Retrieval miss | Relevant chunk never in candidates | reranker can't fix |

---

## Alphabetical Glossary

### Bi-encoder

**Definition:** A model embedding query and chunk separately, compared by
vector similarity. Fast and corpus-scalable, but coarse — it cannot see the
query-chunk interaction.

**Example:**
```python
score = cosine(embed(query), embed(chunk))
```

**Related concepts:** Cross-encoder, Reranker

---

### Cross-encoder

**Definition:** A model scoring (query, chunk) jointly. Accurate because it
sees the interaction, slow because it costs a forward pass per pair.

**Example:**
```python
score = cross_encoder(query, chunk)
```

**Related concepts:** Bi-encoder, Rerank depth

---

### Latency budget

**Definition:** The time ceiling for the rerank stage. Sets the maximum
rerank depth.

**Example:**
```python
# rerank < 150 ms -> depth capped by the cross-encoder's per-call cost
```

**Related concepts:** Rerank depth

---

### No-rerank baseline

**Definition:** Recall@k measured without the reranker. The comparison that
proves the reranker earns its latency.

**Example:**
```python
# no-rerank 0.84 vs rerank 0.90: the reranker earns its place
```

**Related concepts:** Reranker, Recall@k

---

### Rerank depth

**Definition:** The number of fused candidates the cross-encoder rescored.
A latency-quality trade: deeper costs more, catches more.

**Example:**
```python
# rerank top-50 down to top-5
```

**Related concepts:** Cross-encoder, Latency budget

---

### Reranker

**Definition:** The cross-encoder stage that reorders fused candidates. The
last quality lever before generation.

**Example:**
```python
# retrieve -> top-50 -> rerank -> top-5 -> generate
```

**Related concepts:** Cross-encoder, Rerank depth

---

### Retrieval miss

**Definition:** The relevant chunk never reaching the candidates. Reranking
cannot fix it — the fix is upstream.

**Example:**
```python
# chunk not in top-50 -> reranking top-50 changes nothing
```

**Related concepts:** Reranker, Recall@k

---

## Related Concepts

- **Hybrid fusion**: reranking reorders the fused candidates (arabic-nlp 05)
- **Recall@k**: the measurement for the reranker's contribution
- **Stage budgets**: the latency ceilings rerank depth obeys

## Key Takeaways

1. Bi-encoder finds, cross-encoder reorders.
2. Rerank only the fused candidates.
3. Depth is a latency-quality trade.
4. Measure the contribution; reranking can't fix misses.
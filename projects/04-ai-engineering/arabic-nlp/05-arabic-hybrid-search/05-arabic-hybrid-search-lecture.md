# Arabic NLP 05: Hybrid Search and Reranking

## 🎯 Topic Overview

Lexical search matches exact terms; dense search matches meaning. Each fails
where the other succeeds, so production Arabic retrieval runs both and fuses
them. This lecture covers the fusion (reciprocal rank fusion), the reranker
that rescues the fused candidates, and the Arabic-specific tuning that makes
hybrid search actually beat either arm alone.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Run lexical and dense arms on the same query
2. Fuse rankings with reciprocal rank fusion (RRF)
3. Rerank fused candidates with a cross-encoder
4. Measure hybrid vs single-arm recall@k on the golden set
5. Tune fusion weights and diagnose which arm failed

---

## 1. Two Arms, One Answer

```python
# lexical arm: BM25 over the normalized+stemmed index (topic 03)
# dense arm:   cosine over embeddings (topic 04)
# hybrid:      fuse both rankings, then rerank the union
```

The query runs both arms in parallel. Each returns a ranked list. The fusion
step combines them; the reranker reorders the union by a stronger model.

## 2. Reciprocal Rank Fusion

```python
def rrf(rank_lists: list[list[int]], k: int = 60) -> list[int]:
    scores: dict[int, float] = {}
    for ranks in rank_lists:
        for rank, doc in enumerate(ranks, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)
```

RRF sums `1/(k + rank)` per document across arms. The k=60 constant dampens
the top ranks so one arm can't dominate. No score normalization needed —
ranks are ranks. A document ranked 1 by both arms scores highest.

## 3. Reranking

The fused top-k is rescored by a cross-encoder: a model that scores
(query, passage) pairs jointly, far more accurate than the bi-encoder
embeddings but too slow for the full corpus. Rerank only the fused
candidates (e.g., top-50 → top-5). The reranker fixes the fusion's blind
spot: near-duplicate passages that both arms ranked but ranked wrong.

## 4. Measuring Hybrid

Same golden set, same recall@k, three rows: lexical alone, dense alone,
hybrid. Hybrid should meet or beat both — if it doesn't, the fusion weights
or the reranker are wrong. The exercise prints all three so the comparison
is explicit, not assumed.

## 5. Arabic-Specific Tuning

The lexical arm's quality is set by topics 02–03 (normalization, stemming).
The dense arm's by topic 04 (model choice). Hybrid tuning is the last lever:
RRF k, rerank depth, and whether to weight arms. Each is measured on the
golden set. On Arabic, the lexical arm often carries exact-term and
name queries; the dense arm carries paraphrase — the fusion must not let
either drown the other.

## Common Mistakes

- Fusing raw scores instead of ranks (incompatible scales).
- Reranking the whole corpus (too slow) instead of the fused candidates.
- Judging hybrid without the single-arm baselines.
- Tuning fusion weights before measuring each arm.

## Key Takeaways

1. Hybrid = lexical + dense, fused by rank, then reranked.
2. RRF needs no score normalization; k=60 dampens dominance.
3. Rerank only the fused candidates.
4. Measure all three rows; hybrid must beat both arms.
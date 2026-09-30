# Qdrant 03: Hybrid Search

## Topic Overview

Vector search finds semantic matches; keyword search finds exact terms. Hybrid search runs both and
fuses the results, so a query is answered whether the match is semantic or lexical. Qdrant supports this
natively through prefetch and fusion, and the fusion is the point where the two signals meet.

This lecture covers the two retrievers, the fusion (reciprocal rank fusion), the fusion weights, and
when hybrid beats either retriever alone.

The core idea is complementarity: the two retrievers fail in opposite directions, so running both and
fusing recovers each retriever's misses with the other's hits. The fusion is a rank operation, not a
score operation, because the two retrievers' scores are not comparable.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Run vector and keyword search on the same query.
2. Fuse the two ranked lists with reciprocal rank fusion.
3. Explain why the fusion uses ranks, not scores.
4. Tune the fusion weights on the golden set.
5. Explain when hybrid beats either retriever alone.
6. Explain how Qdrant implements the two-stage retrieval.

## Prerequisites

- Qdrant 02 (vector search) and Arabic NLP 03 (lexical retrieval) for the two arms.
- Arabic NLP 05 (hybrid search) for the Arabic-specific treatment of the same pattern.

---

## 1. Two Retrievers

### The vector retriever

Vector search captures meaning: a query with synonyms or paraphrases finds passages that share no
tokens:

```text
query -> embed -> vector search -> top-k by similarity
```

### The keyword retriever

Keyword search captures exact terms: a query with a rare proper noun or an exact phrase finds passages
containing it.

### The complementarity

Each retriever catches what the other misses. A query with a rare term needs keyword; a query with
synonyms needs vector. The two are complementary, which is why hybrid is the default.

### The exit test

The roadmap's exit test is that hybrid search combines semantic and keyword, which is the whole point of
running both.

## 2. The Fusion

### Reciprocal rank fusion

Fusion combines the two ranked lists by reciprocal rank fusion (RRF): each result scores the sum of
`1 / (k + rank)` across the lists:

```python
def rrf_score(ranks: list[int]) -> float:
    """Reciprocal rank fusion: sum of 1/(60 + rank) across the lists."""
    return sum(1 / (60 + r) for r in ranks)
```

A result ranked first in both lists scores highest:

```python
assert fused[0] == "b3:p12:0", "ranked first in both lists -> top"
```

### Why ranks, not scores

Vector scores (cosine) and keyword scores (BM25) are on different scales, so adding them requires
normalization that is itself a tuning problem. Ranks are comparable across retrievers, so RRF fuses
them without normalization.

### The constant

The `k = 60` constant dampens the top ranks so one retriever cannot dominate. A smaller `k` sharpens
the top ranks; a larger `k` flattens them. It is a tuning parameter.

### The exit test

The roadmap's exit test is that the fusion combines the two lists, which is the operation that makes
hybrid.

## 3. The Weights

### What they do

The two signals can be weighted, so a corpus with rare technical terms can weight keyword higher and a
corpus with synonyms can weight vector higher.

### Tuning

The weights are tuned on the golden set, not guessed: try combinations, measure recall@k, keep the best.
The tuning is evidence-based, like every other retrieval decision.

### The exit test

The roadmap's exit test is that the hybrid weights are tuned, which is what makes the fusion fit the
corpus.

## 4. When Hybrid Wins

### The cases

Hybrid wins when the query has both semantic and lexical components, or when either retriever alone
misses. It is the default because it rarely loses and often wins.

### The cost

Hybrid runs two retrievals and a fusion, so it is more expensive than either arm. The cost is justified
only if the golden set shows the recall gain.

### The exit test

The roadmap's exit test is that hybrid is evaluated against the golden set, because the gain must be
measured, not assumed.

## 5. Qdrant's Implementation

### Prefetch and fusion

Qdrant supports hybrid search through prefetch: the query runs against multiple sub-queries (a dense
vector and a sparse/keyword vector), and the results are fused:

```text
prefetch: dense (cosine) + sparse (keyword) -> fuse (RRF) -> top-k
```

The two-stage retrieval is the same shape as retrieve-then-rerank: a recall stage that gathers
candidates and a fusion stage that ranks them.

### The rerank stage

Qdrant can also apply a reranking step after the fusion (RAG System 03), which is the accuracy layer on
top of the recall layers.

### The exit test

The roadmap's exit test is that the hybrid search is implemented, which is Qdrant's prefetch-and-fuse.

## 6. The Exercise

### What it models

The exercise models RRF fusion of a vector list and a keyword list, the highest-scoring result, and
results present in only one list.

### The assertions

```python
fused = fuse(vector, keyword)
assert fused[0] == "b3:p12:0", "ranked first in both lists -> top"
assert "b3:p12:1" in fused
assert rrf_score([1]) > rrf_score([3])
```

The presence of single-list results shows that the fusion does not discard a retriever's hits.

## Real-World Application

- Athar hybrid retrieval: dense (cosine) plus sparse (keyword), fused by RRF, then reranked.
- Weighting keyword higher for a corpus of technical terms and rare names.
- Tuning the fusion on the golden set to confirm the hybrid gain over either arm.
- Using Qdrant's prefetch to run both arms and fuse in one call.

## Common Mistakes

1. **Using only one retriever.** The other's hits are missed.
2. **Fusing raw scores.** Incomparable scales distort the fusion.
3. **Weights guessed, not tuned.** The fusion does not fit the corpus.
4. **No evaluation against the golden set.** The gain is assumed.
5. **Tuning the fusion before the arms are good.** Polishing the wrong layer.
6. **Ignoring the cost.** Hybrid is more expensive than a single arm.

## Key Takeaways

1. Vector captures meaning; keyword captures exact terms; they are complementary.
2. RRF fuses by ranks, so no score normalization is needed; `k = 60` dampens dominance.
3. The fusion weights are tuned on the golden set.
4. Hybrid rarely loses and often wins, but the gain must be measured against the cost.
5. Qdrant implements hybrid via prefetch (multiple sub-queries) and fusion.

## Self-Check Questions

1. Why do vector and keyword retrieval fail in opposite directions?
2. Why does RRF use ranks rather than scores?
3. How are the fusion weights tuned, and where?
4. When is hybrid not worth its cost?
5. How does Qdrant implement hybrid search with prefetch?

## Further Reading / Connections

- Qdrant 02 (vector search) and 04 (metadata filtering).
- Arabic NLP 03 (lexical retrieval) and 05 (hybrid search) — the Arabic treatment.
- RAG System 03 (reranking) — the accuracy layer after the fusion.
- `docs/cheat-sheets/qdrant.md` — the command reference.

# RAG System 03: Reranking

## 🎯 Topic Overview

Retrieval returns candidates; reranking reorders them. The bi-encoder
embeddings that found the candidates are coarse — a cross-encoder scoring
(query, chunk) pairs jointly is far more accurate but too slow for the full
corpus. Reranking applies the accurate model to the fused candidates only.
This lecture covers the bi-encoder/cross-encoder distinction, rerank depth,
and measuring the reranker's contribution.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why bi-encoders are coarse and cross-encoders accurate
2. Rerank only the fused candidates, never the full corpus
3. Choose rerank depth from the latency budget
4. Measure reranking's contribution to recall@k
5. Diagnose when reranking does not help

---

## 1. Bi-Encoder vs Cross-Encoder

A bi-encoder embeds query and chunk separately, then compares vectors —
fast, corpus-scalable, but coarse: it cannot see how the query and chunk
interact. A cross-encoder scores (query, chunk) jointly — it sees the
interaction, so it is far more accurate, but it costs a forward pass per
pair, so it cannot scan the corpus. The division of labor: bi-encoder finds
candidates, cross-encoder reorders them.

```python
# bi-encoder: embed once, compare vectors (fast, coarse)
q_vec = embed(query)
c_vec = embed(chunk)
score = cosine(q_vec, c_vec)

# cross-encoder: score the pair jointly (accurate, slow)
score = cross_encoder(query, chunk)
```

## 2. Rerank Depth

Rerank the top-N fused candidates (e.g., top-50) down to top-k (e.g.,
top-5). The depth N is a latency-quality trade: deeper reranking catches
more true positives but costs more cross-encoder calls. The budget decides
N — the roadmap's stage budgets (rerank < 150 ms) set the ceiling.

## 3. Measuring the Contribution

Compare recall@k with and without reranking on the same golden set. If
reranking does not improve recall, it is not earning its latency. The
measurement is the same protocol as every other retrieval decision — never
assume the reranker helps.

## 4. When Reranking Does Not Help

Reranking cannot fix what retrieval never found. If the candidates lack the
relevant chunk, reordering them changes nothing. A reranker that shows no
gain is a retrieval problem, not a reranker problem — the fix is upstream
(chunking, filters, fusion weights).

## 5. The Pipeline

```text
retrieve (bi-encoder + BM25, fused) -> top-50 candidates
rerank (cross-encoder) -> top-5
generate (grounded on the top-5)
```

Reranking sits between retrieval and generation. It is the last quality
lever before the answer is written.

## Common Mistakes

- Reranking the full corpus (too slow).
- Judging the reranker without a no-rerank baseline.
- Expecting reranking to fix retrieval misses.
- Choosing depth without a latency budget.

## Key Takeaways

1. Bi-encoder finds, cross-encoder reorders.
2. Rerank only the fused candidates.
3. Depth is a latency-quality trade.
4. Measure the reranker's contribution.
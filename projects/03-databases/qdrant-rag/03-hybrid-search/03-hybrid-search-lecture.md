# Qdrant 03: Hybrid Search

## 🎯 Topic Overview

Vector search finds semantic matches; keyword search finds exact terms.
Hybrid search runs both and fuses the results, so a query is answered
whether the match is semantic or lexical. This lecture covers the two
retrievers, the fusion, and the weights.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Run vector and keyword search on the same query
2. Fuse the two result lists
3. Weight the two signals
4. Explain when hybrid beats either alone
5. Tune the fusion

---

## 1. Two Retrievers

Vector search captures meaning; keyword search captures exact terms. For
Arabic, a query with a rare term benefits from keyword search; a query
with synonyms benefits from vector search. The two retrievers are
complementary — each catches what the other misses. The roadmap's exit
test: "hybrid search combines semantic and keyword."

## 2. The Fusion

Fusion combines the two ranked lists into one. Reciprocal rank fusion
scores each result by the reciprocal of its rank in each list — a result
ranked first in both lists wins. The fusion is the point where the two
signals meet.

```python
def rrf_score(ranks):
    return sum(1 / (60 + r) for r in ranks)
```

## 3. The Weights

The two signals can be weighted: a corpus with rare technical terms may
weight keyword higher; a corpus with synonyms may weight vector higher.
The weights are tuned on the golden set, not guessed. The roadmap's exit
test: "the hybrid weights are tuned."

## 4. When Hybrid Wins

Hybrid wins when the query has both semantic and lexical components, or
when either retriever alone misses. A query with a rare proper noun needs
keyword; a query with paraphrased terms needs vector. Hybrid is the
default because it rarely loses and often wins.

## 5. Tuning the Fusion

The fusion is tuned on the golden set: try weight combinations, measure
recall@k, keep the best. The tuning is evidence-based, like every other
retrieval decision. The roadmap's exit test: "hybrid search is evaluated
against the golden set."

## Common Mistakes

- Using only one retriever.
- Fusing without weights (both signals equal by default).
- Weights guessed, not tuned.
- No evaluation against the golden set.
- Ignoring the fusion's rank normalization.

## Key Takeaways

1. Vector captures meaning; keyword captures exact terms.
2. Fusion combines the two ranked lists.
3. Weights are tuned on the golden set.
4. Hybrid rarely loses and often wins.
5. The fusion is evaluated, not guessed.
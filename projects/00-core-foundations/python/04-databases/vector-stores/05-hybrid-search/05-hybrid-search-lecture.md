# Databases — 05: Hybrid Search (Dense + BM25 Fusion)

## Topic Overview

Dense retrieval misses exact tokens (error codes, names, versions); keyword
search misses synonyms and paraphrase. Production retrieval runs both arms
and fuses them. This lecture covers the dense arm, the BM25 arm, score
normalization, and reciprocal rank fusion — the hybrid pipeline DevMate runs
in weeks 2–3.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the complementary failure modes: dense misses tokens, BM25 misses meaning
2. Compute BM25 scores and explain IDF, term saturation, and length normalization
3. Normalize two incompatible score scales before any fusion
4. Implement reciprocal rank fusion (RRF) and explain the k=60 constant's role
5. Diagnose which arm failed on a missed query and fix that arm

## Prerequisites

| Need | Where |
|---|---|
| Dense retrieval and recall@k | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| The runnable exercise | [05-hybrid-search.py](05-hybrid-search.py) |

## 1. Two Arms, Two Blind Spots

```python
# query: "Qdrant ef_search tuning guide"
# dense arm: finds "HNSW recall-latency tradeoffs" (meaning, no shared tokens)
# BM25 arm:  finds "ef_search" changelog entries (tokens, maybe off-topic)
# Either arm alone misses something the user asked for.
```

Dense fails on rare exact strings; BM25 fails on vocabulary mismatch. The
exercise measures each arm's recall@10 separately first — fusion without
per-arm numbers is superstition.

## 2. BM25 in One Screen

BM25 scores term overlap with three corrections: IDF down-weights common
terms, saturation caps the reward for repeating a term, length normalization
stops long documents winning by volume. You do not need to memorize the
formula; you need to know which knob to turn when scores misbehave (usually
length normalization on code corpora with huge files).

## 3. Fusion Without Lying to Yourself

Dense scores (cosine, −1..1) and BM25 scores (unbounded positives) cannot be
added raw. Two honest options: normalize each arm to [0,1] per query (min-max
over the retrieved set) then weight-sum, or skip scores entirely with RRF —
`sum(1/(60 + rank))` per document across arms — which needs no normalization
at all. RRF's constant 60 dampens the top ranks so one arm can't dominate;
tune the arm weights on the golden set, not by taste.

```python
def rrf(rank_lists, k=60):
    fused = {}
    for ranks in rank_lists:
        for rank, doc in enumerate(ranks, start=1):
            fused[doc] = fused.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(fused, key=fused.get, reverse=True)
```

## 4. Diagnose the Arm, Not the Fusion

On a missed golden question, check per-arm recall before touching fusion:
if dense missed it, the fix is embeddings/chunking (module 2 territory, weeks
2–3 chunking ADR); if BM25 missed it, the fix is tokenization/stemming; if
both found it but fusion buried it, the fix is weights. Most "hybrid is
broken" tickets are one broken arm.

## Common Mistakes

- Adding raw cosine and BM25 scores (different planets).
- Tuning fusion weights before measuring per-arm recall.
- Equal weights by default — the golden set decides the weights.

## DevMate Connection

`devmate/src/devmate/retrieve/` runs dense + BM25 fusion followed by
reranking. The weeks 2–3 eval reports per-arm recall precisely so the failure
attribution in section 4 is data, not instinct. The metadata-filtering
fold-in (topic 06) constrains both arms before fusion.

## Key Takeaways

1. Dense and BM25 fail in opposite directions — run both.
2. Normalize scales or use RRF; never add raw scores.
3. Weights come from the golden set.
4. Diagnose per arm; fix the arm, not the fusion.

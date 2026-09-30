# Arabic NLP 05: Hybrid Search and Reranking

## Topic Overview

Lexical search matches exact terms; dense search matches meaning. Each fails where the other
succeeds, so production Arabic retrieval runs both and fuses them. The fusion is reciprocal
rank fusion (RRF), which combines the two ranked lists without needing to reconcile their
incomparable scores. A reranker then rescues the fused candidates, reordering them with a
more accurate but slower model.

This lecture covers the two arms, the fusion, the reranker, and the Arabic-specific tuning
that makes hybrid search actually beat either arm alone. The discipline throughout is
measurement: hybrid must be proven to meet or beat both single arms on the golden set, not
assumed to, because a badly weighted fusion can be worse than one good arm.

Hybrid search is the production Arabic retrieval pattern, and this lecture is where the
lexical arm (Topic 03) and the dense arm (Topic 04) become one system.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Run the lexical and dense arms on the same query.
2. Fuse their rankings with reciprocal rank fusion.
3. Rerank the fused candidates with a cross-encoder.
4. Measure hybrid versus single-arm recall@k on the golden set.
5. Tune the fusion and diagnose which arm failed.
6. Explain why fusing ranks rather than scores avoids an incompatibility.

## Prerequisites

- Arabic NLP 03 (lexical retrieval) and 04 (embeddings) for the two arms.
- AI Evaluation 03 (retrieval evaluation) for recall@k, precision@k, and MRR.

---

## 1. Two Arms, One Answer

### The three-step shape

```python
# lexical arm: BM25 over the normalized+stemmed index (topic 03)
# dense arm:   cosine over embeddings (topic 04)
# hybrid:      fuse both rankings, then rerank the union
```

The query runs both arms in parallel. Each returns a ranked list of document ids. The fusion
combines them into one ranking; the reranker then reorders the top of that ranking.

### Why not pick one arm

The lexical arm wins on exact terms, names, and rare vocabulary; the dense arm wins on
paraphrase and semantic query-document pairs with no shared tokens. A query workload mixes
both, so a single arm leaves a class of queries badly served. Hybrid covers the union.

### The cost

Hybrid runs two retrievals and a reranker, so it is more expensive per query than either arm
alone. The cost is justified only if the golden set shows the recall gain; otherwise the
cheaper single arm is the right choice.

## 2. Reciprocal Rank Fusion

### The mechanism

RRF scores each document by summing `1 / (k + rank)` across the arms in which it appears:

```python
def rrf(rank_lists: list[list[int]], k: int = 60) -> list[int]:
    scores: dict[int, float] = {}
    for ranks in rank_lists:
        for rank, doc in enumerate(ranks, start=1):
            scores[doc] = scores.get(doc, 0.0) + 1.0 / (k + rank)
    return sorted(scores, key=scores.get, reverse=True)
```

### Why ranks, not scores

BM25 scores and cosine similarities live on different scales and are not directly
comparable; adding them requires normalization that is itself a tuning problem. RRF sidesteps
this by using ranks, which are already comparable across arms. A document ranked first by
both arms scores highest; a document ranked first by one arm and absent from the other still
scores well.

### The constant k

The `k = 60` constant dampens the top ranks so that one arm cannot dominate the fusion. A
smaller `k` sharpens the influence of top ranks; a larger `k` flattens it. It is a tuning
parameter, measured on the golden set.

## 3. Reranking

### The cross-encoder

The fused top-k is rescored by a cross-encoder: a model that scores (query, passage) pairs
jointly rather than embedding them separately. Joint scoring is far more accurate because the
model sees the query and the passage together, but it is too slow to run over the whole
corpus.

### Rerank only the candidates

The pipeline retrieves a generous candidate set (for example the fused top 50) and reranks
only those down to the final top 5. The retriever's job is recall; the reranker's job is
precision at the top. This division is why hybrid plus reranking beats either alone.

### What the reranker fixes

The reranker fixes the fusion's blind spot: passages that both arms ranked highly but not
first, and near-duplicate passages where the coarse arms cannot tell which is the better
answer. It is the accuracy layer on top of the recall layers.

## 4. Measuring Hybrid

### Three rows, one set

The golden set is scored three ways: lexical alone, dense alone, and hybrid. Hybrid should
meet or beat both:

```python
assert r_hyb >= r_lex and r_hyb >= r_dense, "hybrid must not underperform either arm"
```

If it does not, the fusion weights, the RRF constant, or the reranker is wrong, and the
numbers say so instead of a hunch.

### Per query type

Break the comparison down by query type (verse, hadith, fiqh, unanswerable). Hybrid may win
overall while losing on one type, which points to a specific arm or a fusion weight that
needs attention.

### The report

Report recall@k and MRR for all three rows, plus precision@k so noise is visible. This is the
retrieval exit test applied to hybrid search.

## 5. Arabic-Specific Tuning

### Where the quality comes from

The lexical arm's quality is set by Topics 02 and 03 (normalization, stemming). The dense
arm's by Topic 04 (model choice). Hybrid tuning is the last lever, not the first: tuning the
fusion before the arms are good is polishing the wrong thing.

### The arms carry different queries

On Arabic, the lexical arm often carries exact-term and name queries, and the dense arm
carries paraphrase and conceptual queries. The fusion must not let either drown the other,
which is what the RRF constant and any arm weighting control.

### Reranking depth

The rerank depth (how many candidates go to the reranker) trades latency for precision.
Deeper reranking catches more reorderings at higher cost. Measure the recall and latency
tradeoff on the golden set.

## 6. Diagnosing Which Arm Failed

### The method

For a query that hybrid gets wrong, check each arm:

- The lexical arm failed if the query and the relevant passage share no normalized tokens
  (paraphrase, synonym).
- The dense arm failed if the query and the passage have low cosine despite shared meaning
  (weak model, normalization mismatch).
- The reranker failed if both arms ranked the passage well but the reranker demoted it.

Each points to a different fix, and the per-arm ranks make the diagnosis mechanical rather
than speculative.

## Real-World Application

- Running Athar retrieval as lexical plus dense, fused by RRF, reranked down to the passages
  that become the answer's context.
- Tuning the RRF constant down when the lexical arm should carry exact verse citations.
- Raising the rerank depth when the fused top-5 keeps missing the best passage at rank 8.
- Reporting lexical, dense, and hybrid recall@5 side by side in the retrieval ADR.

## Common Mistakes

1. **Fusing raw scores instead of ranks.** Incomparable scales distort the fusion.
2. **Reranking the whole corpus.** Too slow; rerank only the fused candidates.
3. **Judging hybrid without the single-arm baselines.** No evidence it helps.
4. **Tuning fusion weights before the arms are good.** Polishing the wrong layer.
5. **Ignoring per query-type results.** An aggregate can hide a class of failures.
6. **Assuming hybrid always wins.** A bad fusion can underperform one good arm.

## Key Takeaways

1. Hybrid runs the lexical and dense arms and fuses them, then reranks the candidates.
2. RRF uses ranks, so no score normalization is needed; `k = 60` dampens dominance.
3. Rerank only the fused candidates; the retriever maximizes recall, the reranker precision.
4. Measure all three rows on the golden set; hybrid must meet or beat both arms.
5. Tune the arms first, the fusion last, and record the configuration in the retrieval ADR.

## Self-Check Questions

1. Why does RRF use ranks rather than scores, and what problem does that avoid?
2. Why is the reranker run only on the fused candidates and not the whole corpus?
3. Hybrid underperforms the lexical arm on the golden set. What are the likely causes?
4. Why must the golden set cover both exact-term and paraphrase queries?
5. A query fails under hybrid. How do you tell which arm or stage is responsible?

## Further Reading / Connections

- Arabic NLP 03 and 04 — the two arms this lecture fuses.
- Arabic NLP 06 (ANN search) — serving the dense arm at scale.
- AI Evaluation 03 (retrieval evaluation) — the metrics reported for all three rows.
- `docs/learning/deep-dives/athar-retrieval-deep-dive.md` — the fusion in the real system.

# Arabic NLP 06: Approximate Nearest Neighbor (ANN) Search

## Topic Overview

Exact nearest-neighbor search computes the distance from the query to every vector in the
corpus. On a small corpus that is fine. On a large one it is the bottleneck: at a million
vectors, every query is a million distance computations, and latency grows linearly with the
collection. ANN search trades a small amount of recall for a large amount of speed by
pruning the search space, and it is what makes dense retrieval practical at corpus scale.

This lecture covers why exact search does not scale, the recall/speed tradeoff the ANN index
introduces, the index structure (HNSW), the parameters that control the tradeoff, and how to
tune them against the golden set so the recall loss is measured rather than silent.

The central discipline is the same as everywhere in retrieval: the index parameters are a
tuning decision made on the golden set, and the recall loss they cause is a number you report,
not an accident you discover in production.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why exact search does not scale to large corpora.
2. Explain the ANN recall/speed tradeoff.
3. Describe the HNSW index structure at a high level.
4. Choose the ANN parameters and measure the recall loss.
5. Tune the index on the golden set and record the choice.
6. Explain how ANN combines with the hybrid and reranking pipeline.

## Prerequisites

- Arabic NLP 04 (embeddings) and 05 (hybrid search) for the dense arm.
- AI Evaluation 03 (recall@k) for measuring the loss.

---

## 1. Why Exact Search Does Not Scale

### The linear scan

Exact search scores every vector against the query and returns the top-k. Its cost is
proportional to the corpus size, so a query over a million vectors is roughly a thousand
times more work than over a thousand vectors.

### The consequence

For a small Athar sample the exact scan is instant. For a full corpus, the per-query latency
makes the system unusable. This is not a constant-factor problem to optimize; it needs a
different search structure.

### The lesson

The transition from exact to ANN is a scale decision, not a quality decision. You move to
ANN when the corpus grows past the point where exact search meets the latency budget, and
you accept a measured recall cost for the speed.

## 2. The ANN Tradeoff

### The mechanism

ANN prunes the search space so only a fraction of vectors are scored. The pruning is guided
by an index structure that places similar vectors near each other, so a query walks toward
the nearest region instead of scanning everything.

### The cost

The true nearest neighbor may be pruned, so recall drops slightly. The tradeoff is controlled
by the index parameters: more search exploration means higher recall and lower speed, less
exploration means the reverse. The exercise models it with a pruning fraction:

```python
def ann_search(points, query, k, prune):
    """ANN: score only a fraction of the vectors (the pruned set)."""
    n = max(1, int(len(points) * prune))
    sampled = list(points)[:n]  # stub: the index prunes to this subset
    ...
```

Light pruning keeps recall; heavy pruning loses the true neighbor. The real index makes this
choice through its parameters rather than a fixed fraction.

### Why it is acceptable

A small recall loss at the ANN layer is absorbed by the layers above it: the fused candidate
set is generous, and the reranker has the accuracy to recover a candidate that ANN ranked a
little low. The retrieval pipeline is designed with that slack.

## 3. The Index Structure

### HNSW at a high level

Hierarchical Navigable Small World (HNSW) builds a multi-layer graph over the vectors. The
upper layers are sparse and act as a highway to the right region; the lower layers are dense
and hold the fine structure. A query enters at the top, descends, and explores neighbors at
each layer until it reaches the local nearest neighbors.

### Built once, searched many

The index is constructed once during ingestion and searched on every query. Construction
cost is paid at write time, which is why re-indexing after an embedding-model change is a
deliberate, scheduled operation rather than a per-query cost.

### The parameters

The index has two families of parameters: those that govern the graph's construction (the
connectivity, which trades memory and build time for a better graph) and those that govern
the search (how much of the graph is explored, which trades speed for recall). Together they
are the recall/speed dial.

## 4. Measuring the Recall Loss

### The protocol

Compare ANN results against exact results on the golden set. Exact search defines the true
neighbors; ANN is scored on how often it recovers them. The recall loss is the gap:

```python
exact = exact_search(points, query, k)  # true neighbors
ann = ann_search(points, query, k, prune)  # approximate
# recall of ANN = overlap with the exact top-k
```

### Reporting the loss

Report the ANN recall relative to exact, alongside the latency. A parameter setting that
loses 2% recall for a 10x speedup may be the right trade; one that loses 20% for 2x is not.
The numbers make the trade explicit.

### The latency side

Measure p50 and p95 latency, not the mean (Model Serving 03). Load and concurrency change
the tail, and the tail is what users feel.

## 5. Tuning on the Golden Set

### The loop

Try parameter combinations, measure recall@k and latency, and keep the setting that meets the
latency budget with the highest recall. This is the same measured-tuning discipline used for
BM25's constants and the embedding model choice.

### The budget first

Decide the latency budget before tuning; otherwise there is no target to optimize against. A
search that returns the perfect answer in two seconds may be worse than a 95%-recall answer
in 200 milliseconds.

### Record the setting

The chosen parameters, the recall loss, and the latency belong in the retrieval ADR, and the
index's parameter setting is part of the deployed configuration so a change is deliberate.

## 6. ANN in the Hybrid Pipeline

### Where it sits

ANN serves the dense arm: the query embedding is searched against the ANN index to produce
the dense ranked list, which is then fused with the lexical arm (Topic 05). The ANN layer is
therefore upstream of fusion and reranking.

### Why the slack matters

Because the fused candidate set is generous and the reranker is accurate, the dense arm can
tolerate a little ANN recall loss. This is why ANN is safe here: it feeds a pipeline designed
to recover from a slightly imperfect arm.

### When it does not

If the dense arm is the only retriever and there is no reranker, the ANN recall loss is the
final recall loss, and the parameters must be tuned conservatively. The pipeline shape
decides how much approximation is acceptable.

## Real-World Application

- Serving the Athar dense arm with an HNSW index in Qdrant, tuned to a latency budget against
  the golden set.
- Measuring ANN recall against exact search before raising the corpus size.
- Recording the index parameters and the recall loss in the retrieval ADR.
- Re-indexing deliberately after an embedding-model change, since the index was built for the
  old vectors.

## Common Mistakes

1. **Exact search on a large corpus.** Latency grows linearly and becomes unusable.
2. **Ignoring the recall loss.** Approximation degrades quality silently.
3. **Parameters guessed, not tuned.** The recall/speed dial is left unset.
4. **No latency measurement.** Speed is assumed, not known.
5. **Tuning on the wrong set.** The parameters are optimized against the wrong queries.
6. **Re-indexing without a scheduled operation.** The embedding change and the index drift
   apart.

## Key Takeaways

1. Exact search does not scale; ANN prunes the search space for speed.
2. ANN trades a little recall for a lot of speed, controlled by the index parameters.
3. HNSW builds a navigable multi-layer graph, built once and searched many times.
4. Measure the recall loss against exact search and the latency with percentiles; tune to the
   latency budget on the golden set.
5. ANN feeds the dense arm of the hybrid pipeline, which is designed to absorb its small
   recall loss.

## Self-Check Questions

1. Why does exact search's cost grow with the corpus, and why is that a structural problem?
2. What does ANN trade away, and what controls how much?
3. Describe HNSW in two sentences and say why the index is built once.
4. How do you measure the ANN recall loss, and what do you report with it?
5. Why is a small ANN recall loss acceptable in a hybrid pipeline but not in a single-arm
   retriever?

## Further Reading / Connections

- Arabic NLP 04 (embeddings) and 05 (hybrid search) — the arm ANN serves and the pipeline it
  feeds.
- AI Evaluation 03 (retrieval evaluation) — the recall metric used to measure the loss.
- Model Serving 03 (inference serving) — percentile latency and the tail.
- `projects/03-databases/qdrant-rag/` — the vector store that provides the HNSW index.

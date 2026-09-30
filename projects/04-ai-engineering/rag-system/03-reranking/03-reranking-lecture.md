# RAG System 03: Reranking

## Topic Overview

Retrieval returns candidates; reranking reorders them. The bi-encoder embeddings that found
the candidates are coarse by design: they embed the query and the passage separately, so they
cannot see how the two interact. A cross-encoder scores the (query, passage) pair jointly and
is far more accurate, but it costs a forward pass per pair, so it cannot scan a corpus.
Reranking is the reconciliation: use the cheap model to find a wide candidate set, and the
expensive model to reorder a narrow one.

This lecture covers the bi-encoder versus cross-encoder distinction, why reranking applies
only to the fused candidates, how rerank depth is a latency-quality trade decided by the
budget, and how to measure the reranker's actual contribution. The measuring part is what
keeps reranking honest: a reranker that does not improve recall on the golden set is not
earning its latency.

The lecture also covers the case where reranking cannot help: when the candidates never
contained the relevant passage, no reordering recovers it. That diagnosis points upstream, to
retrieval, not to the reranker.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why bi-encoders are coarse and cross-encoders are accurate.
2. Rerank only the fused candidates, never the full corpus.
3. Choose rerank depth from a latency budget.
4. Measure the reranker's contribution to recall@k and MRR.
5. Diagnose when reranking does not help and route the fix upstream.
6. Place reranking correctly in the retrieval-to-generation pipeline.

## Prerequisites

- RAG System 02 (filters and retrieval) and Arabic NLP 05 (hybrid search) for the candidate
  set.
- AI Evaluation 03 (retrieval evaluation) for the metrics.

---

## 1. Bi-encoder Versus Cross-encoder

### The bi-encoder

A bi-encoder embeds the query and the passage independently and compares the vectors:

```python
# bi-encoder: embed once, compare vectors (fast, coarse)
q_vec = embed(query)
c_vec = embed(chunk)
score = cosine(q_vec, c_vec)
```

Because the two are encoded separately, the model never sees the interaction between the
query and the passage. That is what makes it fast (passage embeddings are computed once at
ingest) and what makes it coarse.

### The cross-encoder

A cross-encoder scores the pair jointly:

```python
# cross-encoder: score the pair jointly (accurate, slow)
score = cross_encoder(query, chunk)
```

It sees the query and the passage together, so it captures relevance the bi-encoder misses,
but it must run a forward pass per pair and cannot precompute passage embeddings. It cannot
scan a corpus; it can only reorder a candidate set.

### The division of labor

The bi-encoder is the finder: high recall, cheap, corpus-scalable. The cross-encoder is the
ranker: high precision, expensive, applied to a narrow set. Retrieval maximizes recall;
reranking maximizes precision at the top.

## 2. Rerank Only the Candidates

### Why not the corpus

Running the cross-encoder over the corpus is thousands of times more work than the bi-encoder
scan it is meant to refine. The whole point of retrieval is to avoid scoring everything.

### The depth parameter

The pipeline reranks the top-N fused candidates down to the top-k final passages:

```text
retrieve (bi-encoder + BM25, fused) -> top-50 candidates
rerank (cross-encoder) -> top-5
generate (grounded on the top-5)
```

N is the rerank depth. Deeper reranking catches more true positives (the relevant passage
ranked 30th can be promoted) but costs more cross-encoder calls, which raises latency.

### The budget sets N

The rerank depth is a latency-quality trade decided by the budget. If the stage budget allows
150 ms for reranking, N follows from the cross-encoder's per-pair latency. Recording the
budget first turns the choice from a guess into arithmetic.

## 3. Measuring the Contribution

### The no-rerank baseline

Measure recall@k and MRR on the golden set with and without reranking. If reranking does not
improve the metrics, it is not earning its latency. Never assume the reranker helps; measure
it, like every other retrieval decision.

### The exercise

The exercise simulates a cross-encoder that recognizes an exact phrase the coarse bi-encoder
missed, and asserts that reranking does not hurt recall and that the exact-phrase chunk is
promoted to rank 1:

```python
assert with_rerank >= no_rerank, "reranking must not hurt recall"
assert reranked[0]["chunk_id"] == "c5", "exact-phrase chunk promoted to top"
```

### What to report

Report recall@k, precision@k, and MRR for both rows, so the reader sees whether reranking
improved coverage, ranking, or both. A reranker that raises MRR while recall holds is doing
exactly its job.

## 4. When Reranking Does Not Help

### The upstream failure

Reranking cannot fix what retrieval never found. If the relevant passage is not in the
candidate set, reordering the candidates changes nothing. The symptom is a reranker that
shows zero gain, which is really a retrieval recall problem.

### The diagnosis

Check whether the relevant passage is in the candidate set at all:

- **In the set, ranked low:** reranking's job; tune depth or the cross-encoder.
- **Not in the set:** retrieval's job; fix chunking, filters, fusion weights, or the
  embedding model (RAG System 07, "missing material").

### The lesson

A no-gain reranker is information, not a failure. It says the bottleneck is upstream, and
routing the fix to retrieval is the correct response.

## 5. The Pipeline Position

### Between retrieval and generation

Reranking sits between retrieval and generation: it is the last quality lever before the
answer is written from the context (RAG System 04). Its output defines what the model reads,
so its quality directly bounds the answer's quality.

### The interaction with fusion

In hybrid search (Arabic NLP 05), the reranker runs on the fused list, so it corrects the
fusion's blind spot: passages both arms ranked highly but not first, and near-duplicates the
coarse arms cannot separate. Reranking and fusion are complementary, not alternatives.

### The cost accounting

Reranking is a model call with its own cost and latency. Track it like any other inference
cost (Model Serving 01), and include it in the per-query budget.

## Real-World Application

- Reranking the Athar fused top-50 down to the 5 passages that become the answer's context.
- Measuring that reranking lifts MRR on verse queries without changing recall, confirming it
  is ranking, not retrieval, that needed help.
- Discovering a no-gain reranker on fiqh queries and fixing the candidate set instead.
- Setting the rerank depth to 30 because the cross-encoder's per-pair latency fits the stage
  budget.

## Common Mistakes

1. **Reranking the full corpus.** The cross-encoder cannot scan a corpus; it is too slow.
2. **Judging the reranker without a no-rerank baseline.** Its contribution is assumed.
3. **Expecting reranking to fix retrieval misses.** It reorders; it does not retrieve.
4. **Choosing depth without a latency budget.** The trade is made blindly.
5. **Ignoring the reranker's own cost.** It is a model call and belongs in the budget.
6. **Reranking before fusion.** The reranker should see the fused candidates.

## Key Takeaways

1. The bi-encoder finds candidates cheaply and coarsely; the cross-encoder reorders them
   accurately and expensively.
2. Rerank only the fused candidates, down from top-N to top-k.
3. Rerank depth is a latency-quality trade set by the stage budget.
4. Measure reranking against a no-rerank baseline on the golden set; a no-gain reranker points
   upstream to retrieval.
5. Reranking sits between fusion and generation and bounds the context quality.

## Self-Check Questions

1. Why can a cross-encoder not scan the full corpus, and what does that imply for the
   pipeline?
2. What does the rerank depth control, and what sets it?
3. A reranker shows no recall gain. Is the reranker broken? Explain.
4. Why must the baseline be measured without reranking?
5. Why does the reranker run after fusion rather than before it?

## Further Reading / Connections

- Arabic NLP 05 (hybrid search) — the fusion whose output is reranked.
- RAG System 04 (context construction) — the consumer of the reranked top-k.
- RAG System 07 (context failure modes) — "missing material" as the upstream cause.
- AI Evaluation 03 (retrieval evaluation) — recall@k, precision@k, and MRR.

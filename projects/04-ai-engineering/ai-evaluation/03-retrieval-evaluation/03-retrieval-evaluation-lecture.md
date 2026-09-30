# AI Evaluation 03: Retrieval Evaluation

## Topic Overview

Retrieval quality is measured against the golden set with ranked metrics:
recall@k, precision@k, and MRR. These are not three ways to say the same thing; they
answer different questions and diagnose different failures. Reporting one of them
alone hides the failure modes the other two would reveal.

This lecture builds the three metrics from ranked results, shows how each answers a
distinct question ("did we find the material", "how much noise did we show", "how
high did the right answer rank"), and shows how to read them together as a
diagnostic. It ends with the discipline that turns metrics into a gate: a baseline
run, fixed thresholds, and enforcement in CI.

Everything here runs against the golden set from AI Evaluation 01, which is why that
lecture comes first. The retrieval metrics are the densest signal in the whole RAG
pipeline: if the right passage is not retrieved, no amount of generation quality can
recover it.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compute recall@k and precision@k from a ranked result list.
2. Compute MRR for single-answer queries.
3. Choose the metric that matches the retrieval task.
4. Read the three metrics together to diagnose a retrieval failure.
5. Set baseline thresholds and enforce them as a CI gate.
6. Explain why retrieval recall bounds generation quality.

## Prerequisites

- AI Evaluation 01 (the golden set this lecture measures against).
- Applied ML 03 (precision and recall as classification rates) for the intuition.

---

## 1. Recall@k

### The question

Recall@k asks: of the relevant passages, how many appear in the top k?

```python
def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant)
```

For a query with three relevant passages, recall@5 of 2/3 means two of the three were
retrieved within the top five. The denominator is all relevant passages, so recall@k
measures coverage: did we find the material at all?

### Why it is primary for RAG

Missing a relevant passage means the answer cannot be grounded in it. Many RAG
failures are retrieval failures in disguise: the generator answered plausibly because
the grounding passage never reached the context window. Recall is therefore the
primary retrieval metric, and it is an upper bound on how good the answer can be.

### Choosing k

k should match the number of passages that will actually reach the generator. If the
context window holds five passages, recall@5 is the metric that reflects what the
model can use; recall@10 is informative but partly academic.

## 2. Precision@k

### The question

Precision@k asks: of the top k results, how many are relevant?

```python
def precision_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = retrieved[:k]
    return sum(1 for r in top if r in relevant) / k
```

### Why it matters

High recall with low precision means the right passages are found but buried in
noise. The context window is a budget: passages spent on irrelevant material are
passages not available for grounding. Precision also affects the user experience,
because whatever is shown is what they see.

### The precision-recall tension

The two move against each other with k. Increasing k raises recall (more chances to
include a relevant passage) and lowers precision (more slots filled with noise).
A reranker exists precisely to raise precision at the top without sacrificing recall,
by rescoring a wide candidate set down to a tight, relevant one.

## 3. MRR

### The question

MRR (mean reciprocal rank) asks: how high did the first relevant passage rank?

```python
def mrr(retrieved: list[str], relevant: set[str]) -> float:
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1 / i
    return 0.0
```

Reciprocal rank is 1 when the first result is relevant, 1/2 when the second is the
first relevant one, and so on. MRR is the mean over a set of queries. It is the metric
for "find me the one passage" queries: a verse lookup, a specific hadith, a known
citation. MRR is 1.0 when the answer is always first and 0.5 when it is always second.

### When MRR is the wrong metric

MRR only sees the first relevant result, so it is the wrong tool for multi-answer
queries, where several passages matter and the ranking of the rest is invisible to it.
For those, recall@k and nDCG tell the real story.

## 4. Reading Them Together

The three metrics diagnose different failures:

| Pattern | Diagnosis | Fix direction |
| --- | --- | --- |
| Low recall@k | The retriever misses material | Indexing, chunking, or query understanding |
| High recall, low precision@k | Material found but ranked under noise | Ranking, or add a reranker |
| High recall, low MRR | Material found but not first | Reranking, or better query-document matching |
| All low | Missing at every level | Start with the retrieval stage; the pipeline is broken at its base |

### The exercise shows all three

The good retriever in the exercise scores recall@5 = 1.0, precision@5 = 0.6, MRR = 1.0:
it finds everything and puts the best first, while two of five slots are noise. The
"buried" retriever keeps recall@5 = 1.0 but drops MRR to 1/3, because the first
relevant passage is now at rank 3. The "missing" retriever collapses recall@5 to 1/3.
Each pattern is a distinct, actionable signal.

## 5. nDCG and Graded Relevance

### Why graded relevance

Precision@k treats relevance as binary. When passages are "highly relevant",
"somewhat relevant", or "not relevant", binary metrics throw away information. nDCG
(normalized discounted cumulative gain) rewards relevant items near the top with a
discount for position, so a highly relevant passage at rank 1 counts more than the
same passage at rank 5.

### When to use it

Use nDCG when the golden set carries graded relevance labels and when the ranking
within the top-k matters, not just membership. It is the standard metric for
search-style evaluation and a strong complement to recall@k and MRR.

## 6. Thresholds, Baselines, and the CI Gate

### Baseline first

Run the current system against the golden set and record the numbers. Those numbers
are the baseline; the thresholds are derived from them, not invented.

### Set the gate

Choose thresholds that catch regressions without failing on noise. A common pattern:
the gate fails if recall@5 drops below the baseline minus a small tolerance. The
golden set is fixed (AI Evaluation 01), so a drop in the metric is a drop in the
system, not a change in the yardstick.

### Enforce in CI

The gate runs on every change. A retrieval change that drops recall@5 below the
threshold fails the build before it ships. This is the difference between having
metrics and having a regression guard.

### The exit test

The roadmap's exit test: "recall@5 and MRR are measured and reported." Reporting both
means the reader can see whether a change helped coverage or only ordering, which a
single number would hide.

## 7. Connection to the Pipeline

Retrieval metrics are upstream of every generation metric. A faithfulness score
computed over passages that were never retrieved is measuring the wrong thing. This is
why the retrieval evaluation runs first and why its numbers are quoted before the
generation numbers in any report: they bound what the rest of the pipeline can
achieve.

## Real-World Application

- Reporting Athar retrieval as recall@5 and MRR per query type (verse, hadith, fiqh)
  so a weakness in one type is visible.
- Using a reranker to lift precision@5 without dropping recall@5, and proving it with
  the two numbers side by side.
- Setting a CI gate that blocks a chunking change which silently lowers recall@5.
- Explaining to an interviewer why recall is the primary retrieval metric for RAG.

## Common Mistakes

1. **Reporting recall without precision.** Noise becomes invisible; the context budget
   is wasted and no metric shows it.
2. **Using MRR for multi-answer queries.** It only sees the first relevant result.
3. **Tuning one metric while another collapses.** A reranker can lift precision@5
   while quietly dropping recall@5.
4. **No baseline thresholds.** The gate has no teeth and never fails.
5. **Measuring on a moving golden set.** The metric moves with the yardstick, not the
   system.
6. **Choosing k unrelated to the context window.** Recall@10 is academic if only five
   passages reach the model.

## Key Takeaways

1. Recall@k: did we find the material? It bounds generation quality.
2. Precision@k: how much noise did we show? It reflects the context budget.
3. MRR: how high did the first relevant passage rank? It is for single-answer queries.
4. The three metrics diagnose different failures; report and read them together.
5. Baseline, threshold, and enforce in CI against the fixed golden set.

## Self-Check Questions

1. A query has three relevant passages; the retriever returns two of them in the top
   five and nothing else relevant. Compute recall@5 and precision@5.
2. The first relevant passage is at rank 3. What is the reciprocal rank?
3. Which metric would you optimize for a verse-lookup feature, and which for a
   fiqh reasoning feature?
4. A change lifts precision@5 from 0.4 to 0.7 while recall@5 drops from 0.9 to 0.7.
   Is that a win? Defend your answer.
5. Why must thresholds come from a baseline run against a fixed golden set?

## Further Reading / Connections

- AI Evaluation 01 (gold datasets and annotation) — the fixed set these metrics score
  against.
- AI Evaluation 02 (faithfulness and citation precision) — the generation metrics that
  sit downstream of retrieval.
- `projects/04-ai-engineering/rag-system/03-reranking` — the step that lifts precision
  without losing recall.
- `docs/reference/ml-fundamentals-map.md` — ranking-metric background.

# AI Evaluation 03: Retrieval Evaluation

## 🎯 Topic Overview

Retrieval quality is measured against the golden set with ranked metrics:
recall@k, precision@k, and MRR. These metrics answer different questions —
did we find the relevant passages, and did we rank them first? This lecture
covers the three metrics, when each matters, and how to read them together.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Compute recall@k and precision@k from ranked results
2. Compute MRR for single-answer queries
3. Choose the right metric for the retrieval task
4. Read the three metrics together for failure diagnosis
5. Use them as CI gates against the golden set

---

## 1. Recall@k

Recall@k asks "of the relevant passages, how many appear in the top k?"
For a query with 3 relevant passages, recall@5 = 2/3 means two of the three
were retrieved in the top 5. Recall answers "did we find the material?"
For a RAG system, missing a relevant passage means the answer cannot be
grounded — recall is the primary retrieval metric.

```python
def recall_at_k(retrieved, relevant, k):
    top = retrieved[:k]
    return len(set(top) & set(relevant)) / len(relevant)
```

## 2. Precision@k

Precision@k asks "of the top k results, how many are relevant?" It answers
"how much noise did we show?" A high recall with low precision means the
right passages are buried in noise — the context window is wasted on
irrelevant material. Precision matters when the context budget is tight.

## 3. MRR

MRR (mean reciprocal rank) asks "how high did the first relevant passage
rank?" For a query with one known answer, MRR rewards ranking it first.
It is the metric for "find me the one passage" queries — a verse lookup,
a specific hadith. MRR is 1.0 when the answer is always first, 0.5 when
it is always second.

```python
def mrr(rank_of_first_relevant):
    return 1 / rank_of_first_relevant
```

## 4. Reading Them Together

The three metrics diagnose different failures. Low recall@k: the retriever
misses material — fix indexing or query understanding. High recall, low
precision@k: the retriever finds material but ranks noise above it — fix
ranking or add reranking. High recall, low MRR: the material is found but
not ranked first — the answer is grounded but the user sees the wrong
passage first.

## 5. The CI Gate

All three run against the golden set on every change. The thresholds are
set from a baseline run, then enforced: a change that drops recall@5 below
the threshold fails CI. The roadmap's exit test: "recall@5 and MRR are
measured and reported."

## Common Mistakes

- Reporting recall without precision (noise invisible).
- Using MRR for multi-answer queries (it only sees the first).
- Tuning on one metric while another collapses.
- No baseline thresholds (the gate has no teeth).
- Measuring on a moving golden set.

## Key Takeaways

1. Recall@k: did we find the material?
2. Precision@k: how much noise did we show?
3. MRR: how high did the first relevant passage rank?
4. The three metrics diagnose different failures.
5. Thresholds from a baseline, enforced in CI.
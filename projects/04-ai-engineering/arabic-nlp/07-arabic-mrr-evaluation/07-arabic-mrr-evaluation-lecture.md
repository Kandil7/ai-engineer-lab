# Arabic NLP 07: MRR Evaluation

## 🎯 Topic Overview

Retrieval quality is measured, not assumed. MRR (mean reciprocal rank)
rewards ranking the first relevant passage high; recall@k rewards finding
the relevant passages at all. This lecture covers the two metrics and the
Arabic golden set they run against.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Compute MRR from ranked results
2. Compute recall@k
3. Read the two metrics together
4. Build the Arabic golden set
5. Use the metrics as CI gates

---

## 1. MRR

MRR is the mean of the reciprocal ranks of the first relevant passage. A
query whose first relevant passage is ranked first contributes 1.0; ranked
second contributes 0.5. MRR rewards getting the answer to the top. The
roadmap's exit test: "MRR is measured."

```python
def mrr(rank_of_first_relevant):
    return 1 / rank_of_first_relevant
```

## 2. Recall@k

Recall@k asks whether the relevant passages appear in the top k. For a
query with one relevant passage, recall@5 is 1.0 if it is in the top 5.
Recall answers "did we find the material?" The roadmap's exit test:
"recall@k is measured."

## 3. Reading Them Together

MRR and recall@k diagnose different failures. High recall, low MRR: the
material is found but not ranked first — the answer is grounded but the
user sees the wrong passage first. Low recall: the material is missing —
fix the retriever. The roadmap's exit test: "the metrics are read
together."

## 4. The Arabic Golden Set

The golden set is a fixed set of Arabic queries with known relevant
passages. The queries cover the corpus's question types: verse, hadith,
fiqh, and unanswerable. The set is the yardstick every retrieval change is
measured against. The roadmap's exit test: "the golden set is built."

## 5. The CI Gate

MRR and recall@k run against the golden set on every change. A change that
drops recall@5 below the baseline fails CI. The thresholds come from a
baseline run, then are enforced. The roadmap's exit test: "the metrics
gate changes in CI."

## Common Mistakes

- Reporting MRR without recall (finding ignored).
- A golden set that changes under the system.
- No baseline thresholds.
- Metrics never run in CI.
- A golden set without unanswerable queries.

## Key Takeaways

1. MRR rewards ranking the first relevant passage high.
2. Recall@k rewards finding the material.
3. The two metrics diagnose different failures.
4. The Arabic golden set is the yardstick.
5. The metrics gate changes in CI.
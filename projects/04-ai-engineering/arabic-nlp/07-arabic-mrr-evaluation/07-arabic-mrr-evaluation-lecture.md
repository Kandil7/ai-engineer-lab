# Arabic NLP 07: MRR Evaluation

## Topic Overview

Retrieval quality is measured, not assumed. Two metrics carry most of the weight in Arabic
retrieval evaluation: MRR (mean reciprocal rank), which rewards ranking the first relevant
passage high, and recall@k, which rewards finding the relevant passages at all. They answer
different questions, and reading them together is what turns two numbers into a diagnosis.

This lecture covers both metrics, the Arabic golden set they run against, how to read them
together, and how they become a CI gate. It is in the Arabic module because the Arabic golden
set has properties the generic retrieval evaluation lecture does not emphasize: the query
types (verse, hadith, fiqh, unanswerable), the by-book separation, and the fact that exact
verse lookups and open-ended fiqh questions need different metrics to be fair.

The metrics are the same tools introduced in AI Evaluation 03; this lecture applies them to
the Arabic setting and shows the failure patterns that matter for an Islamic-text corpus.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compute MRR from a ranked result list.
2. Compute recall@k from a ranked result list.
3. Read MRR and recall@k together to diagnose a failure.
4. Build an Arabic golden set that covers the corpus's query types.
5. Use the metrics as CI gates with thresholds derived from a baseline.
6. Choose which metric matters most for each Arabic query type.

## Prerequisites

- Arabic NLP 03 to 06 for the retrieval pipeline being measured.
- AI Evaluation 01 (golden set) and 03 (retrieval evaluation) for the full treatment.

---

## 1. MRR

### Definition

MRR (mean reciprocal rank) is the mean over queries of the reciprocal rank of the first
relevant passage. A query whose first relevant passage is ranked first contributes 1.0;
ranked second contributes 0.5; ranked third contributes 1/3; no relevant passage found
contributes 0.0:

```python
def mrr(retrieved: list[str], relevant: set[str]) -> float:
    for i, r in enumerate(retrieved, start=1):
        if r in relevant:
            return 1 / i
    return 0.0
```

### What it rewards

MRR rewards getting the answer to the very top. It is the metric for single-answer queries
where there is one right passage and its position is what matters: a specific verse lookup,
a specific hadith, a known citation.

### Where it is the wrong metric

MRR only sees the first relevant result. For a multi-answer fiqh question with several
supporting passages, MRR ignores everything after the first, so it can look perfect while
most of the needed evidence is buried. Recall@k and nDCG are the metrics for those queries.

## 2. Recall@k

### Definition

Recall@k asks whether the relevant passages appear in the top k:

```python
def recall_at_k(retrieved: list[str], relevant: set[str], k: int) -> float:
    top = set(retrieved[:k])
    return len(top & relevant) / len(relevant)
```

For a query with one relevant passage, recall@5 is 1.0 if it is in the top 5. For a query
with three relevant passages, recall@5 of 2/3 means two of the three made the top 5.

### What it rewards

Recall answers "did we find the material?" It is the primary metric for RAG, because a
relevant passage that was never retrieved cannot ground the answer (AI Evaluation 03).

### The context-window link

k should match how many passages actually reach the generator. If the context window holds
five passages, recall@5 is the metric that reflects what the model can use; recall@20 is
informative but partly academic.

## 3. Reading Them Together

The two metrics diagnose different failures:

| Pattern | Diagnosis | Fix direction |
| --- | --- | --- |
| High recall, high MRR | Retrieval works | Keep it |
| High recall, low MRR | Material found but ranked low | Reranking, better matching |
| Low recall, high MRR | Only the top passage is found | Recall is the problem; indexing, query understanding |
| Low recall, low MRR | Missing at every level | Fix the retrieval stage first |

The exercise shows the patterns directly: the good retriever scores MRR 1.0 and recall@5 1.0;
the buried retriever keeps recall@5 1.0 but drops MRR to 1/3; the missing retriever collapses
recall to 0.0.

### Why both

A single metric hides half the story. MRR alone hides the passages that never ranked; recall
alone hides the ranking quality near the top. Reporting both is what makes the diagnosis
mechanical.

## 4. The Arabic Golden Set

### Coverage

The golden set is a fixed set of Arabic queries with known relevant passages. The queries
cover the corpus's question types:

- **Verse** (a specific ayah lookup): MRR matters most; there is one right answer.
- **Hadith** (a specific narration): MRR matters, sometimes with a few relevant narrations.
- **Fiqh** (legal reasoning across passages): recall@k matters; several passages support the
  answer.
- **Unanswerable** (the corpus does not contain the answer): tests abstention, not ranking.

```python
# Each golden query carries the relevant passage ids and a verified answer.
{
    "query": "ما حكم الصلاة في السفر؟",
    "relevant": ["b3:p12:0", "b3:p12:1"],
    "type": "fiqh",
    "answer": "القصر جائز للمسافر",
}
```

### By-book separation

The golden set's passages must not appear in any tuning data, and for Athar the separation is
by book (Applied ML 02): a golden query's source book must not also supply indexing or
tuning passages, or the retriever can recognize the book instead of retrieving by meaning.

### Frozen

The set is frozen at creation. If a change makes a previously irrelevant passage look
relevant, you accept the label and treat the change as a regression, or version the set and
document why. A set that moves with the system is not a yardstick.

## 5. The CI Gate

### Baseline and thresholds

Run the current system against the golden set, record recall@5 and MRR, and derive thresholds
from that baseline. The thresholds are enforced: a change that drops recall@5 below the floor
fails the build (AI Evaluation 06).

### Per query type

Set and report thresholds per query type where the metric differs (MRR for verse, recall@k
for fiqh). An aggregate threshold can hide one type collapsing, and for an Islamic-text corpus
losing fiqh recall is a serious regression even if verse MRR holds.

### Same set, same metrics

Because the set is fixed and the metrics are fixed, a movement in the number is a movement in
the system. That is the property that makes the gate meaningful.

## 6. Which Metric for Which Query

### The mapping

| Query type | Primary metric | Why |
| --- | --- | --- |
| Verse lookup | MRR | One right passage; position is what matters |
| Hadith lookup | MRR, recall@k | One or a few right narrations |
| Fiqh reasoning | recall@k | Several supporting passages must be found |
| Unanswerable | abstention rate | The correct behavior is to abstain |

### Why the mapping matters

Judging verse lookups by recall@k alone (or fiqh questions by MRR alone) mis-measures the
system. The metric must match the query's structure, exactly as classification metrics must
match the cost of each error (Applied ML 03).

## Real-World Application

- Reporting Athar retrieval as MRR for verse queries and recall@5 for fiqh queries, with
  per-type thresholds.
- Diagnosing a fiqh regression as a recall problem (passages not retrieved) rather than a
  ranking problem.
- Setting a CI gate that fails when verse MRR drops below the baseline.
- Keeping the golden set frozen and by-book separated so the numbers stay comparable.

## Common Mistakes

1. **Reporting MRR without recall.** Passages that never ranked are invisible.
2. **Reporting recall without MRR.** Ranking quality near the top is invisible.
3. **A golden set that changes under the system.** It stops being a yardstick.
4. **No baseline thresholds.** The gate never fires.
5. **Metrics never run in CI.** Regressions ship.
6. **A golden set without unanswerable queries.** Abstention is untestable.
7. **One aggregate metric for all query types.** A type collapse hides in the average.

## Key Takeaways

1. MRR rewards ranking the first relevant passage high; recall@k rewards finding the material.
2. The two metrics diagnose different failures; report and read them together.
3. The Arabic golden set covers verse, hadith, fiqh, and unanswerable queries, is frozen, and
   is separated by book.
4. Thresholds come from a baseline and are enforced in CI; per-type thresholds catch a type
   collapse.
5. Match the metric to the query type: MRR for single-answer lookups, recall@k for multi-passage
   reasoning, abstention rate for unanswerable queries.

## Self-Check Questions

1. A query's first relevant passage is at rank 3, and two of three relevant passages are in the
   top 5. Compute MRR and recall@5.
2. Which metric would you optimize for a specific-verse feature, and which for a fiqh feature?
3. Why must the golden set be separated by book for Athar?
4. High recall with low MRR points to which fix?
5. Why report per query-type thresholds rather than one aggregate threshold?

## Further Reading / Connections

- AI Evaluation 01 (gold datasets) and 03 (retrieval evaluation) — the general treatment this
  lecture specializes.
- Arabic NLP 05 (hybrid search) — the pipeline scored by these metrics.
- AI Evaluation 06 (eval in CI) — turning the metrics into a gate.
- `evaluations/rag/datasets/devmate-golden.jsonl` — a golden set in this format.

# AI Evaluation 01: Gold Datasets and Annotation

## Topic Overview

Evaluation is only as good as the ground truth it measures against. A gold dataset
is a small, hand-verified set of queries with known-good answers and known-relevant
passages. It is the yardstick every retrieval and generation change is measured
against, and it is the single most valuable artifact in an evaluation stack,
because every other metric silently inherits its quality.

This lecture covers what a golden set is and is not, why coverage matters more than
size, how annotation guidelines make labels reproducible, and how to measure whether
two annotators actually agree. A golden set built without guidelines does not
measure the system; it measures the disagreement between the people who labeled it.

The golden set is also the anchor for everything downstream: retrieval metrics,
faithfulness, citation precision, and the judge all run against it, and it is what
turns "the answers look better" into "recall@5 went from 0.62 to 0.78".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Design a golden set that covers the query space rather than sampling it.
2. Write annotation guidelines that produce consistent labels across annotators.
3. Measure inter-annotator agreement with Cohen's kappa and interpret the number.
4. Keep the golden set strictly separate from any training or tuning data.
5. Use the golden set as a fixed regression gate in CI.

## Prerequisites

- Applied ML 02 (train/validation/test and leakage) for the separation discipline.
- Basic familiarity with a JSON-like record and a label.

---

## 1. What a Gold Dataset Is

### Definition

A golden set is a small, curated collection of queries, each paired with the
passages that are genuinely relevant and, where applicable, a verified answer. It is
not training data and it is not a random sample of user traffic. It is a fixed
yardstick: the same set runs against every change so that a regression is visible
immediately.

```python
# One golden query
{
    "query": "ما حكم الصلاة في السفر؟",
    "relevant": ["b3:p12:0", "b3:p12:1"],
    "answer": "القصر جائز للمسافر",
    "notes": "مسألة فقهية مشهورة، لا خلاف جوهري",
}
```

### What it is not

It is not the training set (that would leak the answers into the metric). It is not
a convenience sample of whatever queries came in last week (that reflects traffic,
not the query space). It is not a moving target you edit whenever a result looks
wrong (then it stops being a yardstick and starts being a tuning parameter).

### Why "gold"

The label is human-verified, which is what makes it gold. The relevant passage list
is the truth the retriever is scored against; the answer is the truth the generator
is scored against. Every later metric inherits the quality of these labels.

## 2. Coverage Over Size

### The principle

Fifty well-chosen queries beat five hundred random ones. A random sample over-represents
the common case and under-represents exactly the cases that break systems. The golden
set must cover the query space deliberately: the question types the system will see,
the hard cases, and the edge cases.

### Coverage dimensions

For an Islamic-text system the dimensions include:

- **Verse questions** (a specific ayah lookup).
- **Hadith questions** (a specific narration, often with an isnad).
- **Legal (fiqh) questions** (reasoning across passages).
- **Unanswerable questions** (the corpus does not contain the answer), which test
  abstention, not retrieval.

```python
# Coverage is a set of question types, not a count.
types = {"verse", "hadith", "fiqh", "unanswerable"}
assert "unanswerable" in types, "abstention cases belong in the set"
```

### Why unanswerable cases matter

A system that never abstains will answer anything, including questions outside its
corpus, and it will sound confident while doing it. If the golden set has no
unanswerable queries, no metric can detect that failure, and the system is free to
hallucinate.

### Balance across dimensions

Record how many queries fall in each dimension. A set that is 90% verse lookups
measures verse lookups and tells you nothing about fiqh reasoning. Balance is a
design decision you make on paper before you start labeling.

## 3. Annotation Guidelines

### Why guidelines come first

Two annotators must produce the same labels from the same query. They will not do
this by intuition. The guidelines define, in writing:

1. What counts as a relevant passage (topical match? answers the question? cites it?).
2. How to select the answer text when several passages support it.
3. How to mark a query as unanswerable.
4. How to handle ambiguity, partial relevance, and multi-passage answers.

### The test of good guidelines

A good guideline is operational: another person can apply it to a new example and
get the label you would have given. If two reasonable people read the guideline and
disagree on an example, the guideline is not finished.

### Guidelines are versioned

When the guidelines change, the labels they produced are no longer comparable with
older labels. Version the guidelines alongside the golden set so a metric movement
can be attributed to the system and not to a silent re-reading of the rules.

## 4. Inter-Annotator Agreement

### Measuring, not assuming

Agreement is measured, not assumed. Two annotators agreeing 80% of the time sounds
good until you notice the majority label is 90% of the data, in which case guessing
the majority would also agree 80% of the time. Raw agreement flatters concentrated
labels.

### Cohen's kappa

Kappa corrects raw agreement for the agreement expected by chance:

```python
def cohen_kappa(a: list[str], b: list[str], categories: set[str]) -> float:
    """Agreement corrected for chance. a and b are parallel label lists."""
    n = len(a)
    assert len(b) == n
    observed = sum(1 for x, y in zip(a, b) if x == y) / n
    chance = 0.0
    for c in categories:
        pa = a.count(c) / n
        pb = b.count(c) / n
        chance += pa * pb
    return (observed - chance) / (1 - chance)
```

Kappa is 1 for perfect agreement, 0 for chance-level agreement, and negative for
worse-than-chance. A common reading: below 0.7 signals the guidelines are ambiguous
and the labels are not yet trustworthy.

### The exercise makes it concrete

Two annotators label 50 queries relevant (R) or not (N), with the majority label N
for 40 of them. They agree on 48 of 50, a raw agreement of 0.96. But chance
agreement is high because N dominates, so kappa lands well below 0.96 and the
assertion `0.7 <= kappa < 0.96` holds. High raw agreement can hide ambiguity, and
kappa exposes it.

## 5. Keeping the Golden Set Separate

### No leakage

The golden set must not appear in training or tuning data. If a passage in the
golden set was used to tune the retriever, the retriever is scored on material it has
seen. This is Applied ML 02's leakage rule applied to evaluation: keep the yardstick
out of the model.

### The by-group rule

For Athar, the separation is by book. If a golden query's source book also supplies
training or tuning passages, the retriever can "recognize" the book rather than
retrieve by meaning. Split by group, not by row.

### Frozen relevance

Relevance labels are frozen at creation. If a change makes a previously irrelevant
passage look relevant, you do not silently edit the label; you either accept the
label as the truth and treat the change as a regression, or you version the golden
set and document why it changed.

## 6. The Golden Set as a Regression Gate

### In CI

The golden set runs in CI on every change. A retrieval change that drops recall@5
below the threshold fails the build before it ships. This is what makes the golden
set more than a document: it is an executable contract.

### The anchor for everything else

Faithfulness, citation precision, and the judge all measure against the same golden
set. Because the human answers are known there, it is also where the judge itself is
validated (AI Evaluation 04).

### The exit test

The roadmap's exit test: "build a golden set of 50 queries with verified answers."
That is the deliverable this lecture produces, and every later retrieval, generation,
and judge metric depends on it existing and being trustworthy.

## Real-World Application

- Building the Athar golden set with verse, hadith, fiqh, and unanswerable coverage.
- Establishing `evaluations/rag/datasets/devmate-golden.jsonl` as the fixed set the
  DevMate eval harness runs against.
- Writing the annotation guideline before labeling so two people produce one set of
  labels.
- Reporting kappa in the evaluation report so a reader can judge whether the labels
  are trustworthy.

## Common Mistakes

1. **Using training data as the golden set.** Leakage inflates every metric.
2. **Sampling user traffic instead of curating coverage.** Common cases are
   over-represented; breakers are missing.
3. **No annotation guidelines.** The labels measure the annotators, not the system.
4. **Never measuring agreement.** Untrustworthy labels go unnoticed.
5. **Letting the golden set change under the system.** It stops being a fixed
   yardstick.
6. **Omitting unanswerable queries.** Abstention becomes untestable.
7. **Labeling without versioning the guidelines.** A metric move cannot be attributed.

## Key Takeaways

1. The golden set is a fixed, curated, human-verified yardstick, not training data
   and not a traffic sample.
2. Coverage beats size; design the query space on paper before labeling.
3. Guidelines make labels reproducible; write them before annotating.
4. Measure agreement with kappa; below 0.7 is a warning, and high raw agreement can
   hide ambiguity.
5. The golden set gates every change in CI and anchors every downstream metric,
   including the judge.

## Self-Check Questions

1. Why can a raw agreement of 0.96 correspond to a kappa well below 0.9?
2. Give two query types an Islamic-text golden set must include, and why the second
   one is the abstention case.
3. Why must the golden set be split from training data by group for Athar?
4. What does it mean to "freeze" relevance labels, and why does editing them quietly
   break the metric?
5. How does the golden set allow you to validate an LLM judge?

## Further Reading / Connections

- AI Evaluation 02 (faithfulness and citation precision) — the first metric that runs
  on the golden set.
- AI Evaluation 03 (retrieval evaluation) — recall@k and MRR scored against it.
- AI Evaluation 04 (LLM-as-judge) — validated on the golden set's human labels.
- Applied ML 02 (train/validation/test and leakage) — the by-group separation rule.
- `evaluations/rag/datasets/` — where the golden set lives.

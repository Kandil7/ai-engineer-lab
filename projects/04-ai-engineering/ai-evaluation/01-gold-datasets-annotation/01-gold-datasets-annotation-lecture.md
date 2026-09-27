# AI Evaluation 01: Gold Datasets and Annotation

## 🎯 Topic Overview

Evaluation is only as good as the ground truth it measures against. A gold
dataset is a small, hand-verified set of queries with known-good answers —
the yardstick every retrieval and generation change is measured against.
This lecture covers building the golden set, writing annotation guidelines,
and measuring annotator agreement.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Design a golden set that covers the query space
2. Write annotation guidelines that produce consistent labels
3. Measure inter-annotator agreement
4. Keep the golden set separate from the training data
5. Use the golden set as a regression gate

---

## 1. What a Gold Dataset Is

A golden set is a small, curated set of queries with verified answers and
relevant passages. It is not training data and it is not a sample of user
traffic — it is a fixed yardstick. The same golden set runs against every
change, so a regression is visible immediately. The roadmap's exit test:
"build a golden set of 50 queries with verified answers."

```python
# One golden query
{
    "query": "ما حكم الصلاة في السفر؟",
    "relevant": ["b3:p12:0", "b3:p12:1"],
    "answer": "القصر جائز للمسافر",
    "notes": "مسألة فقهية مشهورة، لا خلاف جوهري",
}
```

## 2. Coverage Over Size

Fifty well-chosen queries beat five hundred random ones. The golden set
must cover the query space: the question types the system will actually
see, the hard cases, and the edge cases. For an Islamic-text system that
means verse questions, hadith questions, legal (fiqh) questions, and
questions with no answer in the corpus — the abstention cases.

## 3. Annotation Guidelines

Two annotators must produce the same labels from the same query. The
guidelines define: what counts as a relevant passage, how to pick the
answer, how to mark a query as unanswerable, and how to handle ambiguity.
Without guidelines, the golden set measures the annotators, not the system.

## 4. Inter-Annotator Agreement

Agreement is measured, not assumed. Cohen's kappa corrects for chance
agreement: two annotators agreeing 80% of the time on a binary label is
less impressive when the majority label is 90%. Kappa below 0.7 means the
guidelines are ambiguous and the labels are not trustworthy.

```python
def cohen_kappa(a, b, categories):
    # observed agreement minus chance agreement, over 1 minus chance
    ...
```

## 5. The Golden Set as a Regression Gate

The golden set runs in CI on every change. A retrieval change that drops
recall@5 on the golden set is caught before it ships. The golden set is
the anchor of the whole evaluation story: faithfulness, citation
precision, and the judge all measure against it.

## Common Mistakes

- Using training data as the golden set (leakage).
- Sampling user traffic instead of curating coverage.
- No annotation guidelines (labels measure the annotators).
- Never measuring agreement (labels are not trustworthy).
- Golden set changing under the system (no longer a fixed yardstick).

## Key Takeaways

1. The golden set is a fixed, curated yardstick.
2. Coverage beats size.
3. Guidelines make labels reproducible.
4. Measure agreement; kappa below 0.7 is a warning.
5. The golden set gates every change in CI.
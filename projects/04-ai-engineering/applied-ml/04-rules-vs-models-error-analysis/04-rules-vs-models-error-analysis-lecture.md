# Applied ML 04: Rules vs Models and Error Analysis

## 🎯 Topic Overview

Not every problem needs a model. A hand-written rule can beat a model on
small, well-understood problems — and knowing when is a core skill. When a
model does win, error analysis turns its failures into the next
improvement. This lecture covers the rules-vs-model decision and the error
analysis loop.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Decide when a rule beats a model (small, deterministic, explainable)
2. Compare a rule baseline against a model on the same test set
3. Run error analysis: cluster failures, find the pattern, fix the cause
4. Diagnose whether a failure is data, features, or model
5. State the roadmap exit test: "know when the rule is better than the model"

---

## 1. When Rules Win

A rule wins when the problem is small, deterministic, and explainable:
keyword routing, exact-match classification, threshold decisions. A model
wins when the pattern is complex, fuzzy, or learned from data. The rule is
also the baseline every model must beat — if a model cannot beat a simple
rule, the model is not earning its complexity.

```python
# A rule baseline: keyword-based question-type classification
def rule_classify(q: str) -> str:
    if any(w in q for w in ["كيف", "ما هو", "لماذا"]):
        return "how/what"
    if any(w in q for w in ["من", "أين"]):
        return "who/where"
    return "other"
```

## 2. The Comparison

The rule and the model are compared on the same test set with the same
metrics — precision, recall, F1. The roadmap's exit test is exactly this:
"know when the rule is better than the model." If the rule wins on the
metrics that matter, ship the rule; the model adds cost and opacity for no
gain.

## 3. The Error Analysis Loop

```python
# 1. Collect the test failures
# 2. Cluster them by pattern (which class, which input shape)
# 3. Find the cause (data, features, or model)
# 4. Fix the cause, re-test, re-measure
```

Error analysis is a loop, not a step: failures → pattern → cause → fix →
re-measure. Each pass should reduce a specific failure cluster. Without the
clustering, fixes are guesses.

## 4. Diagnosing the Failure Layer

- **Data failure**: wrong labels, missing values, duplicates — the data is
  wrong.
- **Feature failure**: the features don't capture the signal — the
  representation is wrong.
- **Model failure**: the model can't fit the pattern — the capacity or
  algorithm is wrong.

The diagnosis determines the fix. Re-training a model on bad data fixes
nothing; adding features to a model that can't fit fixes nothing.

## 5. The Exit Test

The roadmap's stage-6 exit: "you know when the rule is better than the
model and can interpret the confusion matrix." Both come together here: the
confusion matrix shows where the model fails, and the rules-vs-model
comparison decides whether a model is even warranted.

## Common Mistakes

- Reaching for a model when a rule suffices.
- Judging a model without a rule baseline.
- Fixing failures without clustering them first.
- Re-training on bad data instead of fixing the data.

## Key Takeaways

1. Rules win on small, deterministic, explainable problems.
2. The rule is the baseline every model must beat.
3. Error analysis is a loop: failures → pattern → cause → fix → re-measure.
4. Diagnose the failure layer before fixing.
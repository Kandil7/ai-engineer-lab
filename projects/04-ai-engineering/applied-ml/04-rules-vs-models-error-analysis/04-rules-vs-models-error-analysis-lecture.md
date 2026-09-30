# Applied ML 04: Rules vs Models and Error Analysis

## Topic Overview

Not every problem needs a model. A hand-written rule can beat a learned model on
small, deterministic, explainable problems, and knowing when to stop and write the
rule is a core engineering skill rather than a shortcut. A model that cannot beat a
simple baseline is adding cost, latency, and opacity for nothing. Reaching for a
transformer when three keyword checks would do is one of the most common ways
junior work looks junior.

When a model does earn its place, the work has only started. Error analysis is the
loop that turns its failures into the next improvement: collect the failures,
cluster them, name the cause, fix it, and re-measure. A model that is never error
analyzed plateaus on the first score it happens to reach, because nothing tells you
where to look next.

This lecture covers the rules-versus-model decision, the discipline of the baseline,
and the error analysis loop, anchored to the Arabic question-type classifier in the
exercise and to the roadmap exit test that asks you to know when the rule is better
than the model.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Decide when a rule beats a model using size, determinism, and explainability.
2. Treat a rule baseline as the bar every model must clear.
3. Compare a rule and a model on the same test set with the same metrics and
   threshold.
4. Run the error analysis loop: failures, pattern, cause, fix, re-measure.
5. Diagnose whether a failure is data, features, or model.
6. State the exit test and record the rules-versus-model decision as an ADR when it
   is non-trivial.

## Prerequisites

- Applied ML 02 (a clean split) and Applied ML 03 (precision, recall, and reading a
  confusion matrix).
- The ability to read a small Python function and its assertions.

---

## 1. When a Rule Wins

### The three conditions

A rule wins when the problem is **small** (few cases to handle), **deterministic**
(the mapping is knowable by a human), and **explainable** (a person can state the
rule and defend it). Keyword routing, exact-match classification, and threshold
decisions fit. A model wins when the pattern is large, fuzzy, or only learnable from
data.

### The rule as a product decision

A rule is shippable today, testable line by line, and debuggable when it fails. A
model needs data collection, labeling, training, evaluation, and monitoring. When
the rule's accuracy is sufficient for the cost of its errors, the model's extra
machinery buys nothing the user can see, and it adds a new failure mode: silent,
hard-to-explain wrong answers.

### The Arabic keyword baseline

```python
HOW_WORDS = {"كيف", "ما هو", "لماذا", "كيفية"}
WHO_WORDS = {"من", "أين", "متى"}


def rule_classify(q: str) -> str:
    """Keyword rule baseline for question-type classification."""
    if any(w in q for w in HOW_WORDS):
        return "how"
    if any(w in q for w in WHO_WORDS):
        return "who"
    return "other"
```

This is not a toy. Real routers, filters, and pre-classifiers look like this, and on
a bounded vocabulary a rule like this is often the right production choice.

## 2. The Rule Is the Baseline

### Why every model needs one

Without a baseline you cannot tell whether the model learned anything. The baseline
answers: what does the dumbest reasonable approach score? If a model does not beat
it, the model is not earning its complexity. Reporting "the model got 0.86 F1"
without "the rule got 0.81" tells the reader nothing about whether the model should
exist.

### The deliberate loser

The exercise's `model_classify` is intentionally worse than the rule: it only
recognizes "كيف" and misses the other "how" words. On this data the rule has higher
recall, and the assertions prove it. The lesson is not that models are bad. It is
that on this data size the rule is sufficient, and you should be able to show that
with numbers rather than assume it either way.

## 3. The Comparison Protocol

### The steps

1. Fix one held-out test set (Applied ML 02).
2. Run the rule and the model over the *same* inputs.
3. Score both with the *same* metrics: precision, recall, and F1 per class.
4. Compare on the metric that matches the cost of the errors (Applied ML 03).
5. Decide, and record the decision.

### Why every variable must match

Comparing the rule and the model at different thresholds, or on different data,
produces a difference that is partly the setup rather than the approach. Keep data,
metrics, threshold, and preprocessing identical; vary only the approach. This is the
same discipline as comparing two retrieval strategies on one gold set.

### What a win looks like

A model earns its place when it beats the baseline on the metric that matters, by a
margin large enough to justify its cost. "Slightly better on a small sample" is not
a win, because the difference may be noise and the maintenance cost is real.

## 4. The Error Analysis Loop

```text
failures -> pattern -> cause -> fix -> re-measure
```

### Collect the failures

List every test case the model gets wrong, with its input, prediction, and truth. A
model that is 80% correct has 20% of cases that are the entire improvement surface.
The aggregate hides them; the list exposes them, which is why the exercise computes
and prints the specific failing questions.

### Cluster the failures

Group the failures by shared shape. In the exercise, every how-class failure begins
with "ما هو" or "لماذا": the failures are not random, they are one missing pattern.
Clustering converts a list into a testable hypothesis.

### Name the cause, fix it, re-measure

The cause determines the fix. A missing keyword is a feature gap; a mislabeled
example is a data bug; a pattern the model cannot represent is a model limitation.
Fix the named cause and re-run the same test set so the improvement is measurable.

### The loop, not the step

Error analysis repeats. Each pass should shrink one cluster. A pass that shrinks
nothing means the cause was misdiagnosed; go back to the clustering step. This is
why it is called a loop.

## 5. Diagnosing the Failure Layer

| Layer | Symptom | Fix |
| --- | --- | --- |
| **Data** | Wrong labels, duplicates, missing values, train/test leakage | Fix the data; re-training on bad data changes nothing |
| **Features** | The signal exists in the world but the input does not carry it | Add or repair the feature |
| **Model** | The features carry the signal but the model cannot fit it | Increase capacity, change the algorithm, or add regularization |

The diagnosis order matters: check data before features, features before model. Most
"the model is bad" conclusions are actually data or feature failures, and re-training
a model on mislabeled data reproduces the same mistakes.

## 6. Reading the Confusion Matrix for Clusters

The matrix (Applied ML 03) is the map of failures. Read it per class: the how-class
errors concentrate in one row or column, so the fix is targeted; the who-class
errors form a different cluster, if they exist at all. Error analysis starts where
the matrix shows the densest off-diagonal cell, not with the lowest overall score.
The aggregate tells you how bad it is; the matrix tells you what to do.

## 7. The Exit Test and the ADR

### The exit test

The roadmap's stage-6 exit test: you know when the rule is better than the model, and
you can interpret the confusion matrix. Both skills are exercised here. The matrix
shows where the model fails, and the comparison decides whether a model is warranted
at all.

### Record the decision

When the decision is non-trivial or hard to reverse, record it as an ADR. "We will
not build an ML model for intent classification; the rule is sufficient" is exactly
the kind of long-lived choice that deserves one, with the measured numbers, the cost
of each error, and the condition that would reopen the decision (for example, a new
vocabulary that the rule does not cover).

## Real-World Application

- Routing Arabic questions to handlers by keyword before considering a learned
  classifier.
- Deciding whether Athar needs a learned relevance model or a tuned BM25 rule first.
- Using the confusion matrix to find that a DevMate guardrail over-blocks one category,
  then fixing that class rather than the whole model.
- Answering "why did you not use a transformer for this" with measured numbers from
  the baseline comparison.

## Common Mistakes

1. **Reaching for a model when a rule suffices.** Complexity must be earned with a
   measured win.
2. **Judging a model without a baseline.** You cannot know if it learned anything.
3. **Fixing failures without clustering.** Un-clustered fixes are guesses.
4. **Re-training on bad data.** Diagnose the layer first; data beats model for most
   failures.
5. **Comparing rule and model at different thresholds or on different data.** The
   comparison becomes meaningless.
6. **Stopping after one pass of the loop.** Error analysis is a loop.
7. **Skipping the ADR.** The rules-versus-model choice is long-lived and should be
   recorded.

## Key Takeaways

1. Rules win on small, deterministic, explainable problems; a model must beat the rule
   baseline to earn its complexity.
2. Compare on the same held-out data, the same metrics, and the same threshold.
3. Error analysis is a loop: failures, pattern, cause, fix, re-measure.
4. Diagnose the failure layer (data, features, model) before fixing.
5. The exit test combines the rules-versus-model decision with reading the confusion
   matrix, and the decision belongs in an ADR when it is non-trivial.

## Self-Check Questions

1. Give two conditions under which you would ship a rule instead of a model.
2. Why is a rule baseline mandatory before training a model?
3. The model's how-class failures all begin with "ما هو" or "لماذا". What layer is the
   cause, and what is the fix?
4. A classifier is wrong on 20% of cases. Why is the list of failures more useful than
   the 80% figure?
5. When should the rules-versus-model decision become an ADR?
6. How would you decide that a model's edge over the rule is real rather than noise?

## Further Reading / Connections

- Applied ML 02 (train/validation/test and leakage) and Applied ML 03
  (precision/recall/confusion) — the two prerequisites.
- `projects/04-ai-engineering/ai-evaluation/` — the full evaluation harness this loop
  feeds.
- `docs/reference/ml-fundamentals-map.md` — the baselines and error-analysis sections.
- `docs/decisions/` — where the rules-versus-model ADR belongs.

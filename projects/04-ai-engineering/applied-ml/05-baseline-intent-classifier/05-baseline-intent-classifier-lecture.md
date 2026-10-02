# Applied ML 05: Baseline Intent Classifier

## Topic Overview

This is the exit artifact for the ML-foundations axis: an Arabic intent classifier built
with a non-LLM baseline, a leakage-aware split, and an error report. It combines the
four earlier lectures into one small, runnable deliverable. The point is not a
state-of-the-art classifier; it is the discipline of building a trustworthy measurement
around a simple one.

The task is question-type classification: given an Arabic question, label it `how`,
`who`, or `other`. A keyword rule is the baseline; a tiny multinomial Naive Bayes model
is the learned comparison. The dataset is grouped by source, so the split must respect
the group or the model will memorize the source instead of the label.

The artifact demonstrates the whole loop: split without leakage, compare a rule against
a model against a majority baseline, report per-class precision/recall/F1, and list the
misclassifications for error analysis. It is the shape every later evaluation reuses.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build a non-LLM baseline (a keyword rule) for a classification task.
2. Split data by group so no source straddles train and test.
3. Train a small model (multinomial Naive Bayes) from scratch.
4. Score a rule, a model, and a majority baseline with per-class P/R/F1.
5. Read the misclassifications as an error report.
6. Explain why a model must beat the majority baseline to be worth its complexity.

## Prerequisites

- Applied ML 02 (train/validation/test and leakage), 03 (precision/recall/confusion),
  and 04 (rules versus models and error analysis).
- Basic Python; the script is standard-library only.

---

## 1. The Task and the Data

### The label set

Three labels: `how` (procedural or explanatory questions), `who` (entity and factoid
questions), and `other` (instructions, summaries, translations). Three is enough to make
the problem non-trivial while keeping the metrics readable.

### The grouping key

Every example carries a `source` (a book). Examples from one source share vocabulary,
so they are not independent. That is the group the split must respect (Applied ML 02).

### The baseline

The keyword rule is the baseline: a small set of markers per label, with `other` as the
default. It is cheap, explainable, and the bar the model must clear.

## 2. The Leakage-Aware Split

### Split by source, not by row

```python
def split_by_source(rows, train_frac=0.6):
    sources = sorted({src for _, _, src in rows})
    cut = max(1, int(train_frac * len(sources)))
    train_sources = set(sources[:cut])
    train = [r for r in rows if r[2] in train_sources]
    test = [r for r in rows if r[2] not in train_sources]
    return train, test
```

Rows from one source go entirely to train or entirely to test. No source appears on both
sides, which is the leakage check the script asserts.

### Why the split failed the first time

A first attempt grouped sources so that all `how` and `who` examples were in train and
only `other` examples in test. The split was leakage-free but single-class in test, so the
model's recall for `how` and `who` was structurally zero. A leakage-free split can still
be a bad split; the test set must represent the label distribution.

### The assertion

```python
assert not (train_sources & test_sources), "a source straddles the split"
```

That assertion is the group-leakage guard. It is the same check Applied ML 02 describes,
applied to real rows.

## 3. The Rule Baseline

### The rules

```python
RULES = {
    "how": ("كيف", "كيفية", "ما هو", "ما هي", "لماذا"),
    "who": ("من هو", "من هي", "أين", "متى", "من "),
}


def rule_classify(text):
    for label, words in RULES.items():
        if any(w in text for w in words):
            return label
    return "other"
```

### Strengths and limits

The rule is exact and explainable, and it is strong on the obvious cases. It fails on
questions whose type is implied rather than marked, and it cannot generalize. It is the
baseline, not the goal.

## 4. The Learned Model

### Multinomial Naive Bayes

The model counts tokens per label and predicts by the highest log-posterior:

```python
class NaiveBayes:
    def fit(self, rows): ...
    def predict(self, text):
        scores = {label: self.log_prior[label] for label in LABELS}
        for tok in text.split():
            for label in LABELS:
                scores[label] += self.log_likelihood[label].get(
                    tok, self._default[label]
                )
        return max(scores, key=lambda label: scores[label])
```

### Why Naive Bayes

It is small, fast, deterministic, and understandable, and it works with a handful of
examples. It is the right complexity for a baseline comparison: if a model this simple
cannot beat the rule, a larger one probably will not either, and the rule is the better
ship.

### Laplace smoothing

Unseen tokens would otherwise zero a label's probability. The `+1` smoothing and the
`_default` log-probability keep unseen tokens from erasing a label.

## 5. Metrics

### Per-class P/R/F1

Precision, recall, and F1 are computed per class (Applied ML 03):

```python
def prf(golds, preds, label):
    tp = sum(1 for g, p in zip(golds, preds) if g == label and p == label)
    fp = sum(1 for g, p in zip(golds, preds) if g != label and p == label)
    fn = sum(1 for g, p in zip(golds, preds) if g == label and p != label)
    ...
```

### Macro-F1 and the majority baseline

Macro-F1 averages the per-class F1, so a rare class counts as much as a common one. The
majority baseline (always predict the most common label) is the floor: a model that does
not beat it has learned nothing. The script asserts the model beats the majority.

### What to report

Report all three rows (rule, majority, model) and the per-class numbers, so a reader sees
where the model wins and where it does not.

## 6. Error Analysis

### The list

The error report lists every misclassification with its text, gold label, predicted
label, and source:

```python
def error_analysis(rows, preds):
    return [
        (text, gold, pred, src)
        for (text, gold, src), pred in zip(rows, preds)
        if pred != gold
    ]
```

### What it reveals

The failures cluster by pattern. If every `other` example that starts with a question
marker is misclassified as `how`, the fix is a rule or a feature, not more epochs
(Applied ML 04). The list is the improvement surface.

### The exit test

The roadmap's ML exit test is met here: an Arabic intent classifier with a non-LLM
baseline, a correct (leakage-free) split, and an error report. It is the artifact the
later evaluation work reuses.

## Real-World Application

- Choosing between a rule and a model for a routing or filtering task before paying for
  a model.
- Establishing a non-LLM baseline that any later model must beat on the same split.
- Detecting group leakage when passages, users, or documents are not independent.
- Producing an error report that points at a feature or a rule, not at "the model".

## Common Mistakes

1. **Splitting by row when rows share a source.** Group leakage inflates the score.
2. **A leakage-free split that is also unbalanced.** A single-class test set hides a
   structural recall failure.
3. **Judging a model without the majority baseline.** It may have learned nothing.
4. **Reporting only accuracy.** It hides the per-class failures.
5. **Fixing failures without clustering them.** The error report is the input to the fix.
6. **Reaching for a large model before the simple one is beaten.** Complexity must earn
   its place.

## Key Takeaways

1. The non-LLM baseline (a rule) is the bar every model must clear.
2. Split by group so no source straddles train and test; assert it.
3. A small model (Naive Bayes) is the right complexity for a baseline comparison.
4. Per-class P/R/F1 plus the majority baseline reveal what an aggregate hides.
5. The error report is the improvement surface; cluster failures before fixing.

## Self-Check Questions

1. Why must the split be by source rather than by row for this dataset?
2. Why was the first split leakage-free but still wrong?
3. Why is the majority baseline the right floor for the model?
4. What does macro-F1 add over accuracy?
5. How does the error report tell you whether the fix is data, features, or model?

## Further Reading / Connections

- Applied ML 02 (train/validation/test and leakage) and 03 (precision/recall/confusion)
  and 04 (rules versus models) — the four lectures this artifact combines.
- `projects/00-core-foundations/python/07-machine-learning/` — the wider ML curriculum.
- `projects/04-ai-engineering/ai-evaluation/` — where the same protocol scales to RAG.

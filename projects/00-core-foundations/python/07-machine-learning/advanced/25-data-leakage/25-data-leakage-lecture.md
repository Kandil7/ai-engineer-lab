# Data Leakage — The 0.99 → 0.71 Story

> **Topic 25 — ML rigor series.** Target leakage, train/test contamination,
> temporal and group leakage, duplicate rows — and the worked example where a
> "0.99 accuracy" model collapses to its honest 0.71 once the leak is fixed.

Companion exercise: `25-data-leakage.py`

---

## Topic Overview

Data leakage is the most expensive bug in applied machine learning because it
makes the system look *better* than it is. Nothing crashes. The offline metric
climbs. The team ships, and production quietly delivers a fraction of the
promised performance — if it works at all. Leakage is information reaching the
model during training that will not be available at prediction time.

The concept is simple; the practice is not, because leakage hides in ordinary
code. A feature computed after the outcome, a scaler fitted before splitting, a
random split on time-ordered rows, the same patient in train and test, a join
that duplicates rows. Each is a one-line mistake with a large, invisible cost.

This lecture names the five classes, walks the worked example where a leaky
model reports 0.99 and an honest one reports 0.71, and gives an audit checklist
that turns "suspiciously good" into a routine inspection.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Define leakage and explain why it inflates offline metrics.
2. Identify the five leakage classes in real code.
3. Reproduce the 0.99 → 0.71 collapse with the synthetic churn example.
4. Apply the six-point leakage audit checklist to a dataset.
5. Use pipelines and correct splitters to make leaks structurally impossible.
6. Treat a suspiciously high score as a trigger for audit, not celebration.

## Prerequisites

- Train/test splitting (Topic 10).
- Cross-validation basics (Topic 22).
- Why preprocessing must fit on train only (Topic 24).

## 1. What Leakage Is

**Leakage** = information from outside the training set (the future, the test
set, or the target itself) reaches the model during training. The model appears
brilliant offline and fails in production, because the leaked signal does not
exist at prediction time.

The tell is usually a number that is too good: accuracy above the plausible
ceiling of the problem, AUC near 1.0, or a validation score far above what a
domain expert expects. That is not a win; it is a symptom.

## 2. The Five Leakage Classes

### a) Target leakage — features that encode the answer

A column like `days_since_last_order = 0` exactly when the customer churned is
a perfect predictor that **does not exist before the event**. Any feature
derived after the outcome is target leakage. The test: could this value be known
at the moment a prediction must be made?

### b) Train/test contamination — preprocessing on all data

Fitting a scaler, imputer, or encoder on the **entire** dataset before
splitting bakes test statistics into the training transform. Target encoding of
categoricals is the worst case: the encoding of a category literally contains
the test labels.

### c) Temporal leakage — the future in the past

Random splitting on time-ordered data (financial, clickstream, sensors) puts
future rows in the training window. Splits must respect time; use
`TimeSeriesSplit`, never `shuffle=True` on time.

### d) Group leakage — the same entity in both splits

Medical data has multiple rows per patient; a random split puts the same
patient in train **and** test, so the model memorizes patients instead of
learning the disease. Use `GroupKFold` with the entity id.

### e) Duplicate rows across splits

Duplicated rows (dedup bugs, join fan-out) can appear in both splits and are
trivially "predicted". Deduplicate before splitting.

## 3. The Worked Example

Synthetic churn data with honest AUC ≈ 0.75:

| Intervention | Reported AUC |
|---|---|
| Clean data | 0.75 |
| Add target-leaky column | 0.99+ |
| Scaler fit on all data | 0.81 |
| Duplicate rows in both splits | 0.88 |

Fix the leaks and the number returns to ~0.71 — which is the number that
reproduces in production. The exercise implements each intervention and prints
the table, so you can watch the number move and then come back.

The order of investigations matters: check obvious target leakage first (it is
the largest inflation), then preprocessing contamination, then duplicates, then
splitter correctness.

## 4. The Leakage Audit Checklist

1. Does any feature encode the target (post-event info)?
2. Is every scaler/encoder/imputer fit on **train only**?
3. Are there duplicated rows spanning train and test?
4. Is the split time-aware for temporal data?
5. Are groups (patient/company/session) kept together?
6. Is hyperparameter tuning inside cross-validation?

Run this before believing any score. It costs minutes and prevents the most
expensive class of production failure.

## Common Mistakes to Avoid

1. **Fitting the scaler once, globally.** Put it in a pipeline.
2. **Random split on time-series.** Use `TimeSeriesSplit`.
3. **Target encoding computed on all rows.** Compute inside CV folds with
   smoothing.
4. **Not deduplicating before the split.** Duplicate leakage is trivial and
   common.
5. **Tuning on the test set.** The test set becomes a validation set and stops
   being honest.
6. **Trusting a perfect score.** Near-perfect is a red flag, not a result.

## Key Takeaways

1. Leakage inflates offline metrics and sinks production models.
2. Five classes: target, contamination, temporal, group, duplicates.
3. A suspiciously high score is a red flag — audit before celebrating.
4. Pipelines + proper splitters make leaks structurally impossible.
5. The honest number is the one that reproduces in production.

## Self-Check Questions

1. Give an example of target leakage in a churn model.
2. Why does fitting a scaler on all data leak, even without touching labels?
3. Which splitter fixes group leakage, and what does it preserve?
4. Why is target encoding especially dangerous?
5. What is the first thing to check when validation AUC is 0.99?

## Further Reading / Connections

- **Previous:** Topic 24, Pipelines — the structural fix.
- **Next:** Topic 26, Validation Strategies — correct splitters.
- **Exercise:** `25-data-leakage.py` reproduces the 0.99 → 0.71 table.

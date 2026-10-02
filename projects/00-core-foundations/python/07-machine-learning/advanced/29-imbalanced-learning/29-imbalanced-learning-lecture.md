# Imbalanced Learning — When 99% Accuracy Is Failure

> **Topic 29 — ML rigor series.** Class weights, resampling (undersample,
> oversample, SMOTE), threshold moving, and honest evaluation when the
> positive class is 1%.

Companion exercise: `29-imbalanced-learning.py`

---

## Topic Overview

The most valuable problems in production are imbalanced: fraud, churn, disease
screening, failure prediction, anomaly detection. In each, the event you care
about is rare, and the default training objective quietly learns to ignore it.
A model that predicts "no" for everything is 99% accurate and catches nothing,
which is the operational definition of useless.

Imbalance is not one problem but three decisions: how the loss weights the
classes, whether the data distribution is changed, and where the decision
threshold sits. Each has a different cost and a different failure mode. The
common thread is that accuracy is the wrong scorecard; the report must be built
from positive-class metrics and the confusion matrix.

This lecture covers class weights, resampling including SMOTE, threshold moving,
and — critically — how to resample inside cross-validation so the fix does not
become a new leak.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why accuracy is meaningless under severe imbalance.
2. Apply `class_weight="balanced"` and state the sklearn formula.
3. Compare undersampling, oversampling, and SMOTE.
4. Implement the SMOTE interpolation formula.
5. Move the decision threshold to match a business cost.
6. Resample inside CV folds to avoid synthetic leakage.
7. Report PR-AUC, F-beta, and the confusion matrix together.

## Prerequisites

- Confusion matrix and metrics (Topics 12, 27).
- Cross-validation and leakage (Topics 22, 25, 26).

## 1. The Imbalance Reality

Fraud, churn, disease screening, anomaly detection — the highest-value
problems are imbalanced. A model that always predicts the majority class is
99% accurate and 100% useless. The question is never "accuracy" but "how many
positives did we catch, at what cost?"

## 2. Strategy 1 — Class Weights

The one-line fix: `class_weight="balanced"` scales each class's loss inversely
to its frequency, so the rare class matters as much as the common one.

```python
from sklearn.linear_model import LogisticRegression

LogisticRegression(class_weight="balanced")
```

Trees support `class_weight` too; sklearn's balanced formula is
`n_samples / (n_classes * class_count)`.

**When it fails.** Weights change the effective prior, so the output
probabilities are no longer calibrated to the original prevalence — recalibrate
if you need true probabilities.

## 3. Strategy 2 — Resampling

- **Undersample** the majority class (fast, discards data).
- **Oversample** the minority class by duplication (risk: overfitting).
- **SMOTE**: synthesize new minority samples by interpolating between a
  sample and its k nearest neighbors — the standard, most robust approach.

```python
# SMOTE core idea (implemented from scratch in the exercise):
new = X_minor[i] + lambda_ * (X_minor[neighbor] - X_minor[i])  # lambda_ ~ U(0,1)
```

Resample **inside cross-validation** — resampling before CV leaks synthetic
samples across folds.

**When it fails.** SMOTE on categorical features (interpolating categories is
meaningless without SMOTE-NC) and SMOTE with very few minority points (neighbours
are all near-duplicates, so it overfits).

## 4. Strategy 3 — Threshold Moving

Keep the model; change the decision boundary. Default `0.5` is arbitrary on
imbalance — lower it to catch more positives (recall up, precision down) or
raise it to reduce alert noise:

```python
pred = proba >= 0.2  # business-tuned threshold
```

Threshold moving is the cheapest strategy and the most honest about the
tradeoff: it changes the operating point, not the model. Combine it with class
weights when you need the model itself to attend to the minority.

## 5. Honest Evaluation Under Imbalance

- **PR-AUC** is the primary metric (positive-class only).
- **F-beta** (e.g. F2) matches recall-first business goals.
- **Stratified CV** keeps the rare class in every fold.
- Report the **confusion matrix** — not just one number.

**When it fails.** Reporting a single F1 and hiding the alert rate. Pair every
metric with the fraction of items flagged, so the reviewer sees the operational
load.

## 6. Real-World Use Case — Fraud Detection

```python
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import recall_score

model = RandomForestClassifier(class_weight="balanced")
model.fit(X_train, y_train)
proba = model.predict_proba(X_test)[:, 1]
# Business review cost caps alerts: pick threshold where FP cost is acceptable
pred = proba >= 0.15
print(f"caught {recall_score(y_test, pred):.0%} of fraud with {pred.mean():.0%} alert rate")
```

The threshold is chosen so the alert rate fits the review team's capacity, and
the recall is the resulting catch rate — the number the business actually feels.

## Common Mistakes to Avoid

1. **Optimising accuracy.** Majority-class trivia.
2. **Resampling before splitting/CV.** Leaks synthetic samples.
3. **Oversampling by duplication without regularisation.** Overfits.
4. **Leaving the threshold at 0.5.** Wrong operating point under imbalance.
5. **Using SMOTE on categoricals.** Interpolation is invalid there.
6. **Reporting one metric.** Show PR-AUC, F-beta, and the confusion matrix.
7. **Ignoring calibration after weighting/resampling.** Probabilities shift.

## Key Takeaways

1. Accuracy is meaningless when positives are rare.
2. `class_weight="balanced"` is the 1-line first fix.
3. SMOTE synthesizes minority samples — resample inside CV.
4. Threshold moving trades precision ↔ recall at the business level.
5. PR-AUC + F-beta + stratified CV = the honest report card.

## Self-Check Questions

1. Why does accuracy fail for a 1%-positive dataset?
2. State the SMOTE interpolation formula.
3. Why must resampling happen inside CV folds?
4. When does `class_weight` change calibration, and what do you do?
5. What two numbers should accompany any imbalanced metric report?

## Further Reading / Connections

- **Previous:** Topic 27, Metrics Deep; Topic 25, Data Leakage.
- **Next:** Topic 30, Gradient Boosting.
- **Exercise:** `29-imbalanced-learning.py`.

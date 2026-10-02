# Probability Calibration — Trustworthy Numbers

> **Topic 28 — ML rigor series.** Why raw model scores are often not
> probabilities, Platt scaling, isotonic regression, reliability diagrams,
> and why uncalibrated probabilities break downstream decisions.

Companion exercise: `28-calibration.py`

---

## Topic Overview

A classifier's `predict_proba` output looks like a probability, but for many
models it is only a score on a monotone scale. An SVC or a boosted tree can
output 0.80 while only 55% of those predictions are actually positive. As long
as you only rank — sort by score, pick the top k — that is fine. The moment a
downstream system multiplies the number by a cost, thresholds on it, or averages
it into an expected value, the number must be a real probability.

Calibration is the property: among predictions of 0.80, exactly 80% are true.
It is distinct from discrimination (ranking quality). A model can rank
perfectly and still be badly calibrated, or be well calibrated and rank poorly.

This lecture explains why miscalibration breaks automated decisions, how to
diagnose it with reliability diagrams, how to fix it with Platt scaling or
isotonic regression, and the one rule that makes calibration work: fit the
calibrator on held-out data.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish calibration from discrimination.
2. Explain why SVC, boosting, and neural nets are often miscalibrated.
3. Read a reliability diagram and name the bias.
4. Apply Platt scaling or isotonic regression via `CalibratedClassifierCV`.
5. Measure calibration with the Brier score and log loss.
6. State the held-out-data rule for fitting a calibrator.

## Prerequisites

- Precision/recall and threshold selection (Topic 27).
- Cross-validation (Topic 22).

## 1. The Problem: Scores ≠ Probabilities

Many models — SVC, boosting, neural nets — output numbers that *look* like
probabilities but aren't. An SVC's raw score might say 0.80 while only 55% of
those predictions are true.

**Calibration** is the property: *among predictions of 0.80, exactly 80% are
true.*

Logistic regression is usually well calibrated because it is trained on log
loss, which is a proper scoring rule. Margin-based and ensemble models are not.

## 2. Why It Matters Downstream

When probabilities feed automated decisions (auto-approve, queue, price,
route), miscalibration means systematically wrong choices:

- A system that auto-refunds when `P(return) < 0.2` is relying on those
  numbers being real probabilities.
- Uncalibrated 0.8s that are actually 0.55 → too many refunds, lost money.

The cost is systematic, not random, because the bias is in one direction across
the whole score range.

## 3. Reliability Diagrams

Bin predictions by score and plot predicted vs actual positive rate:

```
predicted 0.20 -> actual 0.42   [BIAS]
predicted 0.60 -> actual 0.58   [OK ]
predicted 0.90 -> actual 0.74   [BIAS]
```

A model perfectly on the diagonal is perfectly calibrated. Points above the
diagonal are under-confident; below, over-confident. Boosted trees commonly sit
below the diagonal at high scores (over-confident), which is why they need
calibration before their probabilities are trusted.

## 4. Fixing Calibration

### Platt scaling (sigmoid)
Fit a logistic function to map raw scores → calibrated probabilities. Smooth,
parametric, good when the miscalibration is a monotone transform.

```python
from sklearn.calibration import CalibratedClassifierCV

CalibratedClassifierCV(model, method="sigmoid", cv=5)
```

### Isotonic regression
Non-parametric, monotone fit — more flexible, needs more data, best when the
distortion is irregular.

### The critical rule
Calibrate on a **held-out set**, never on the training data — or you'll fit
the calibration to the same noise the model memorized. `CalibratedClassifierCV`
does this by cross-validating.

**When it fails.** Isotonic regression on a small calibration set overfits the
step function; prefer sigmoid when data is scarce. Calibrating on training data
produces a calibrator that is confident about the model's memorised noise.

## 5. Measuring Calibration

- **Brier score**: mean squared error of probabilities — lower is better.
- **Log loss**: also rewards calibrated probabilities.
- **Reliability diagram**: visual, per-bin honesty check.

```python
from sklearn.metrics import brier_score_loss

brier = brier_score_loss(y_true, proba)  # lower is better
```

Brier decomposes into calibration and refinement, so a lower Brier after
calibration is direct evidence it helped.

## 6. Real-World Use Case — Loan Auto-Approval

```python
# 1. Train the model
model.fit(X_train, y_train)
# 2. Calibrate on validation data (never train)
calibrated = CalibratedClassifierCV(model, method="isotonic", cv=5)
calibrated.fit(X_val, y_val)
# 3. Auto-approve only when P(default) < 0.05 — now the number is trustworthy
p = calibrated.predict_proba(X_loan)[:, 1]
```

The policy threshold now has a defensible meaning: at most 5% of auto-approved
loans are expected to default, by construction.

## Common Mistakes to Avoid

1. **Treating `predict_proba` as truth for margin models.** Check calibration.
2. **Calibrating on training data.** Fit on held-out folds.
3. **Using isotonic with little data.** It overfits; use sigmoid.
4. **Confusing calibration with accuracy.** A calibrated model can still be weak.
5. **Calibrating once and assuming it holds forever.** Re-check after retraining
   or drift.
6. **Forgetting to recalibrate the *policy* threshold after calibration.** The
   optimal threshold may move.

## Key Takeaways

1. Raw scores from SVC/boosting/NN are usually not probabilities.
2. Reliability diagrams reveal systematic bias by bin.
3. Platt = smooth sigmoid fit; isotonic = flexible monotone fit.
4. Calibrate on held-out data only.
5. Uncalibrated probabilities break every downstream cost decision.

## Self-Check Questions

1. Give a model that ranks well but is badly calibrated, and why.
2. What does a reliability point below the diagonal mean?
3. Why is calibrating on training data wrong?
4. When is sigmoid preferred to isotonic?
5. Why does a calibrated probability matter for an expected-cost decision?

## Further Reading / Connections

- **Previous:** Topic 27, Metrics Deep — why log loss rewards calibration.
- **Next:** Topic 29, Imbalanced Learning.
- **Exercise:** `28-calibration.py`.

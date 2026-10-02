# Metrics Deep Dive — Thresholds as Business Decisions

> **Topic 27 — ML rigor series.** Precision/recall tradeoffs, ROC-AUC vs PR-AUC
> (and when ROC misleads on imbalance), F-beta, log loss, threshold selection
> as a cost decision, regression metrics, multi-class averaging.

Companion exercise: `27-metrics-deep.py`

---

## Topic Overview

Choosing a metric is choosing what the model is optimised to do, and that is a
business decision disguised as a technical one. Accuracy answers "how often are
we right overall", which is almost never the question a product owner is asking.
On a fraud stream at 2% positives, a model that flags nothing is 98% accurate
and worthless; the questions that matter are "how many frauds did we catch" and
"how many of our alerts were real".

The deeper point is that a classifier is not a decision. It produces a score;
a threshold turns the score into a decision. Where you place that threshold
encodes the relative cost of a false positive and a false negative. Two teams
with the same model and different cost structures should ship different
thresholds, and neither number is "the accuracy".

This lecture builds the vocabulary — precision, recall, ROC, PR, F-beta, log
loss — and ends with the procedure for picking a threshold from measured costs
rather than the arbitrary default of 0.5.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why accuracy fails under class imbalance.
2. Define precision, recall, and the tradeoff between them.
3. Choose ROC-AUC or PR-AUC based on the positive-class prevalence.
4. Use F-beta to weight precision or recall to match the business.
5. Select a decision threshold by minimising expected cost.
6. Report regression performance with R², RMSE, and MAE appropriately.
7. Choose the right multi-class averaging (macro, micro, weighted).

## Prerequisites

- Confusion matrix, precision, recall, F1 (Topic 12).
- Imbalanced evaluation (Topic 29).

## 1. Accuracy Is Usually a Lie

A fraud dataset with 2% positives: a model that always predicts "no fraud" is
98% accurate and 100% useless. Accuracy hides what matters on imbalance —
**how many positives did we catch, and how many of our alerts were right?**

Any single number summarising a two-class decision throws away the confusion
matrix: true positives, false positives, true negatives, false negatives. Start
from the matrix; derive the scalar metric the context needs.

## 2. The Precision / Recall Tradeoff

- **Recall** = caught positives / all positives — "did we find them?"
- **Precision** = true alerts / all alerts — "when we say fraud, are we right?"

Raising the threshold raises precision but drops recall, and vice versa. The
right balance is a **business** question: a false positive costs money
(review time, refunds), a false negative costs money (lost fraud).

A useful frame: recall is the fraction of the problem you solve; precision is
the fraction of your effort that was worth it. Both matter, and the exchange
rate is set outside the model.

## 3. ROC-AUC vs PR-AUC — When ROC Misleads

- **ROC-AUC**: plots TPR vs FPR. FPR is over the (huge) negative class, so on
  extreme imbalance the curve can look great while the model is useless.
- **PR-AUC**: plots precision vs recall, both over the **positive** class.
  PR-AUC is brutally honest at 1% positives and is the primary metric for
  imbalanced problems.

The mechanism: with a million negatives, a small rise in FPR still moves the
true-negative count negligibly, so ROC stays high. Precision, however, collapses
the moment false positives accumulate against few true positives.

**When it fails.** Reporting only ROC-AUC for a rare-event problem and
concluding the model is deployable. Always pair it with PR-AUC and the
confusion matrix at the chosen threshold.

## 4. F-beta & Log Loss

- **F1** = harmonic mean of precision and recall (equal weight).
- **F-beta** weights one side: `beta=2` favors recall, `beta=0.5` favors
  precision — match it to the cost structure.
- **Log loss** scores probabilities, not labels — heavily penalizes confident
  wrong predictions. The metric for calibrated probability models.

```python
from sklearn.metrics import fbeta_score

f2 = fbeta_score(y_true, y_pred, beta=2)  # recall-weighted
```

F-beta is still threshold-dependent (it uses hard labels); ROC-AUC and PR-AUC
are threshold-free. Report one threshold-free metric plus the operating point.

## 5. Threshold Selection as a Cost Decision

With costs per false positive and false negative, scan thresholds on the
validation set and pick the one minimizing expected cost:

```python
cost = fp_rate * cost_fp + (1 - recall) * cost_fn
best_threshold = thresholds[argmin(cost)]
```

This is how "99% accurate" models become "0.3% fraud caught with 5% alert
rate" models — and why threshold choice belongs to product, not just ML.

**When it fails.** Tuning the threshold on the test set. Scan on validation;
apply the chosen threshold once to test. Also account for downstream capacity:
if the review team can process 5% of traffic, the alert rate is a hard ceiling.

## 6. Regression Metrics

- **R²**: variance explained — good for reporting.
- **RMSE**: same units as y, penalizes big errors.
- **MAE**: robust to outliers.

Report all three when the error distribution matters: a low MAE with a high RMSE
means a few large errors dominate, which may or may not be acceptable depending
on the application.

## 7. Multi-Class Averaging

- **macro**: average per class, class-size independent — fair for rare classes.
- **micro**: global instance average — favors big classes.
- **weighted**: macro weighted by class frequency — a common default.

Pick to match the claim: macro when every class matters equally, weighted when
you care about overall user experience, micro when reporting aggregate accuracy.

## Common Mistakes to Avoid

1. **Reporting accuracy on imbalanced data.** Meaningless.
2. **ROC-AUC alone at 1% positives.** Use PR-AUC.
3. **Leaving the threshold at 0.5.** It is arbitrary; set it from costs.
4. **Tuning the threshold on the test set.** Scan on validation.
5. **Ignoring capacity constraints.** The alert rate has a ceiling.
6. **Using F1 when the costs are asymmetric.** Use F-beta.
7. **Reporting one regression metric.** RMSE and MAE tell different stories.

## Key Takeaways

1. Accuracy is meaningless on imbalance; use PR-AUC + F-beta.
2. Threshold = business decision (cost of FP vs FN).
3. ROC-AUC can look great while the model is useless at 1% positive.
4. Regression: R² to report, RMSE for units, MAE for robustness.
5. Multi-class: macro for fairness, micro for overall accuracy.

## Self-Check Questions

1. Why does ROC-AUC stay high under extreme imbalance while PR-AUC collapses?
2. What does beta > 1 in F-beta emphasise, and when is that right?
3. How do you pick a threshold from measured FP/FN costs?
4. When would you report macro instead of weighted averaging?
5. Why does log loss reward calibration?

## Further Reading / Connections

- **Previous:** Topic 12, Confusion Matrix; Topic 26, Validation Strategies.
- **Next:** Topic 28, Calibration — making the scores real probabilities.
- **Exercise:** `27-metrics-deep.py`.

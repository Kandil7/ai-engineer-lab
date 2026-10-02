# Gradient Boosting — The Tabular Champion

> **Topic 30 — Modeling depth.** Boosting intuition, sklearn's
> `GradientBoosting` vs `HistGradientBoosting`, early stopping, key
> hyperparameters, native categorical handling, and why GBDTs beat neural
> nets on tabular data.

Companion exercise: `30-gradient-boosting.py`

---

## Topic Overview

Gradient boosting is the workhorse of tabular machine learning. On the kind of
mixed, messy, medium-sized datasets that dominate real business problems, it is
usually the strongest single model and often needs the least feature engineering.
Its opposite, the random forest, builds trees in parallel and averages them to
reduce variance; boosting builds them in sequence, each one correcting the
errors the previous ones made.

The mechanism is elegant: boosting is gradient descent in function space. Each
new shallow tree fits the negative gradient of the loss with respect to the
current ensemble's predictions. For squared error that is literally the
residual; for log loss it is the error scaled by the derivative of the sigmoid.
The final model is a weighted sum of many weak learners.

This lecture explains the sequence, the two sklearn implementations, the
hyperparameters that matter, early stopping as a replacement for guessing the
tree count, and the reasons trees win on tabular data while neural networks win
on text, images, and audio.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain boosting as sequential correction of previous errors.
2. Differentiate `GradientBoosting*` from `HistGradientBoosting*`.
3. Tune `learning_rate`, tree count, and depth together.
4. Use early stopping to find the best iteration count.
5. Handle missing values and categoricals natively with the histogram flavor.
6. Justify GBDTs for tabular data over neural networks.

## Prerequisites

- Decision trees (Topic 11) and random forests (Topic 20).
- Bias/variance (Topic 06) and hyperparameter tuning (Topic 33).

## 1. Boosting Intuition — Learn From Your Mistakes

Boosting builds a **sequence** of shallow trees, each trained to correct the
errors of the ensemble so far:

1. Train tree 1 on the data.
2. Tree 2 predicts the *residuals* (errors) of tree 1.
3. Tree 3 predicts the residuals of trees 1+2. And so on.

The final prediction is the weighted sum of all trees. This is *gradient*
boosting because each tree fits the gradient of the loss.

**Analogy.** A student takes an exam, sees which questions were wrong, and
studies exactly those; the next attempt focuses on the remaining mistakes. The
class improves additively.

**When it fails.** Too many trees at a high learning rate overfit and produce
over-confident probabilities; without early stopping the tree count is a guess.

## 2. sklearn's Two Flavors

```python
# Classic — small/medium data
GradientBoostingClassifier(n_estimators=100, learning_rate=0.1, max_depth=3)

# Fast — large data (LightGBM-style histogram binning, native NaN + categoricals)
HistGradientBoostingClassifier(max_iter=200, learning_rate=0.1)
```

`HistGradientBoosting*` bins continuous features into histograms → drastically
faster training and built-in handling of missing values and categoricals.

**When it fails.** The classic flavor on large data is slow and memory-heavy; the
histogram flavor on tiny data may be overkill but is rarely wrong.

## 3. The Key Hyperparameters

| Param | Effect |
|---|---|
| `n_estimators` / `max_iter` | Number of trees (capacity) |
| `learning_rate` | Step size per tree; lower → more trees needed |
| `max_depth` | Interaction order (usually 3–6) |
| `subsample` | Row sampling → variance reduction |
| `min_samples_leaf` | Regularization → smoother predictions |
| `n_iter_no_change` | Early-stopping patience |

**The golden rule**: `learning_rate` and tree count trade off. Lower the LR,
raise the tree budget, and let **early stopping** find the sweet spot.

## 4. Early Stopping

```python
HistGradientBoostingClassifier(
    max_iter=1000, early_stopping=True, validation_fraction=0.2, n_iter_no_change=10
)
```

Watch validation loss during training; stop when it stops improving. This
replaces blind `n_estimators` guessing.

**When it fails.** Ignoring `random_state` makes the internal validation split
non-reproducible; set it for stable early-stopping behavior. If the validation
fraction is drawn from already-small data, evaluate with an explicit outer
validation set instead.

## 5. Why GBDTs Beat Neural Nets on Tabular

- **Trees handle mixed, messy, scaled-irrelevant features** natively.
- **No feature scaling** needed.
- **Native missing value handling** (histogram flavor).
- **Native categoricals** (LightGBM / sklearn HistGB `categorical_features`).
- Small-to-medium tabular datasets don't have the volume NNs need.
- Neural nets win on **text, images, audio** — high-dimensional, structured
  data. Use the right tool.

**When it fails.** On very high-cardinality categoricals or huge datasets, a
carefully built neural net or a specialised library (LightGBM, XGBoost,
CatBoost) can win; benchmark rather than assume.

## 6. Real-World Use Case — Churn Prediction

```python
model = HistGradientBoostingClassifier(
    max_iter=500,
    learning_rate=0.05,
    max_depth=5,
    early_stopping=True,
    n_iter_no_change=20,
    random_state=0,
)
model.fit(X_train, y_train)  # X may contain NaN and categoricals directly
```

The output probabilities are over-confident by default; if they feed a cost
decision, calibrate them (Topic 28).

## Common Mistakes to Avoid

1. **Tuning tree count by hand.** Use early stopping.
2. **High learning rate with many trees.** Overfits.
3. **Scaling features out of habit.** Trees do not need it.
4. **Imputing before feeding the histogram flavor.** It handles NaN natively.
5. **Trusting raw probabilities.** Boosted models need calibration.
6. **Deep trees.** Interactions beyond depth 6 rarely help and overfit.

## Key Takeaways

1. Boosting = additive sequence of shallow trees fixing prior errors.
2. `learning_rate` ↔ `n_estimators` tradeoff; use early stopping.
3. HistGradientBoosting scales and handles categoricals/NaN natively.
4. GBDTs are the default for tabular; NNs win on text/image/sound.
5. Calibrate before using boosted probabilities in decisions.

## Self-Check Questions

1. How does boosting differ from bagging in tree construction?
2. What does each new tree fit when the loss is squared error?
3. Why does lowering the learning rate require more trees?
4. What two data-handling advantages does the histogram flavor add?
5. Why are boosted probabilities often over-confident?

## Further Reading / Connections

- **Previous:** Topic 20, Random Forest; Topic 11, Decision Trees.
- **Next:** Topic 31, Feature Engineering.
- **Exercise:** `30-gradient-boosting.py`.

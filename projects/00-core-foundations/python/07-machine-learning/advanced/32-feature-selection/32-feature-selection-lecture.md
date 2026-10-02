# Feature Selection — Fewer, Better Features

> **Topic 32 — Modeling depth.** Filter, wrapper, and embedded methods; RFE,
> `SelectFromModel`, L1, multicollinearity and VIF, permutation importance,
> and selection stability.

Companion exercise: `32-feature-selection.py`

---

## Topic Overview

More features are not more signal. Each extra column adds training cost,
inference latency, monitoring surface, and a chance for the model to fit noise.
Feature selection is the discipline of keeping the columns that carry
independent signal and dropping the rest — before training, during training, or
iteratively with the model in the loop.

The methods fall into three families by how much the model participates.
Filters score each feature independently, fast and model-agnostic. Wrappers
search subsets using the model's own performance, powerful but expensive.
Embedded methods select as a side effect of training, notably L1 regularisation
and tree importance.

The trap is that selection itself can leak and can be unstable. Selecting
features using the full dataset, or choosing a set that flips with the random
seed, produces a model that does not reproduce. This lecture covers the three
families, the collinearity diagnostic VIF, permutation importance as the honest
measure, and stability as the shipping gate.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Apply filter methods: variance threshold, ANOVA F, mutual information.
2. Run recursive feature elimination and explain its cost.
3. Use embedded selection via L1 and tree importance.
4. Diagnose multicollinearity with VIF and act on it.
5. Measure feature effect with permutation importance.
6. Verify selection stability across resamples before shipping.

## Prerequisites

- Feature engineering (Topic 31).
- Cross-validation (Topic 22) and leakage (Topic 25).

## 1. Why Select Features

Fewer features = cheaper pipelines, faster training, less overfitting, easier
deployment and monitoring. Selection also removes noise that silently
degrades models.

Operationally, a smaller feature set is also easier to monitor for drift: fewer
columns to track, fewer upstream dependencies to break.

## 2. Filter Methods — Fast, Model-Agnostic

Score each feature independently and keep the top k:

- **VarianceThreshold**: drop near-constant columns.
- **f_classif / ANOVA F**: univariate association with the target.
- **mutual_info_classif**: non-linear association, robust but slower.

```python
from sklearn.feature_selection import SelectKBest, mutual_info_classif

X_sel = SelectKBest(mutual_info_classif, k=20).fit_transform(X_train, y_train)
```

Cheap enough to run on every pipeline; ignores feature interactions.

**When it fails.** A feature weak alone but strong in combination with another
is dropped; filters cannot see interactions.

## 3. Wrapper Methods — Model-Aware

**RFE** (Recursive Feature Elimination) trains the model, drops the least
important feature, repeats. Model-aware and powerful, but expensive — each
iteration refits.

```python
from sklearn.feature_selection import RFECV

selector = RFECV(RandomForestClassifier(), cv=5)
selector.fit(X_train, y_train)
```

**When it fails.** On large feature counts the number of refits makes RFE
impractical; prefer embedded methods first.

## 4. Embedded Methods — Selection During Training

- **L1 regularization** zeroes out coefficients — the remaining non-zero
  features are selected.
- **Tree importance** — `SelectFromModel(RandomForest, threshold="median")`
  keeps features above the median importance.

```python
from sklearn.feature_selection import SelectFromModel
from sklearn.linear_model import LassoCV

selector = SelectFromModel(LassoCV())
```

Fast, model-aware, built into training.

**When it fails.** Impurity-based tree importance is biased toward
high-cardinality features; use permutation importance to double-check.

## 5. Multicollinearity & VIF

**VIF** (Variance Inflation Factor) measures how well a column is predicted
from the others. VIF > 10 indicates harmful collinearity — the column is
redundant and destabilizes linear models:

```python
vif = 1 / (1 - R2_of_column_vs_rest)
```

**When it fails.** Trees tolerate collinearity, so VIF-driven dropping matters
mostly for linear models and for interpretation; do not drop blindly for a
gradient-boosted model.

## 6. Permutation Importance

Shuffle a feature's values and measure the score drop — the honest measure of
"how much does this feature matter". Model-agnostic, but collinear features
share credit, so interpret with care.

```python
from sklearn.inspection import permutation_importance

r = permutation_importance(model, X_val, y_val, n_repeats=10, random_state=0)
```

**When it fails.** With two collinear features, shuffling either alone shows
little drop because the other compensates; permutation importance can appear to
say "neither matters".

## 7. Stability — Selection Must Not Flip

Resample the data a few times; if selection keeps picking the same features,
it's stable. If the chosen set churns wildly, the signal is weak — don't ship
a selection that depends on the seed.

## Common Mistakes to Avoid

1. **Selecting features using all data.** Leakage; select inside CV.
2. **Trusting impurity importance with high-cardinality features.** Biased.
3. **Dropping collinear columns from tree models.** Usually unnecessary.
4. **RFE on hundreds of features.** Too slow; start with embedded.
5. **Shipping an unstable selection.** It will not reproduce.
6. **Selecting and then reporting the training score.** Optimistic.

## Key Takeaways

1. Filter: fast, model-agnostic — variance, F, mutual info.
2. Wrapper (RFE): model-aware but expensive.
3. Embedded: L1 zeros weights; trees rank by importance.
4. VIF > 10 → drop collinear columns (for linear models).
5. Verify selection stability across resamples before shipping.

## Self-Check Questions

1. When does a filter method fail that an embedded method would catch?
2. Why is RFE expensive, and what is the cheaper alternative?
3. What does VIF > 10 mean, and for which models does it matter?
4. Why can permutation importance understate a collinear feature?
5. What does an unstable selection tell you about the signal?

## Further Reading / Connections

- **Previous:** Topic 31, Feature Engineering.
- **Next:** Topic 33, Hyperparameter Tuning.
- **Exercise:** `32-feature-selection.py`.

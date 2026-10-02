# sklearn Pipelines — Fit on Train Only

> **Topic 24 — ML rigor series.** `Pipeline`, `ColumnTransformer`, `FeatureUnion`,
> custom transformers — and why a pipeline is the #1 leakage-prevention tool in
> production ML.

Companion exercise: `24-sklearn-pipelines.py`

---

## Topic Overview

Real machine-learning systems are not "a model". They are a chain: impute the
missing values, scale the numerics, one-hot the categoricals, engineer a few
features, then hand the result to an estimator. Every one of those steps learns
something from the data. The moment a step learns from data it should not see —
the test set, the future — the project is compromised. A scikit-learn
`Pipeline` is the mechanism that makes "learn only from training data"
structural rather than a matter of discipline.

The hard part is not the API; it is the discipline it encodes. A pipeline
guarantees that during cross-validation every preprocessing step is refit on
each training fold and merely applied to the held-out fold. Do the same work by
hand, across dozens of experiments, and you will eventually fit a scaler or
target encoder on the full dataset. The bug is silent: scores go up, the demo is
great, production disappoints.

This lecture builds the pipeline from the inside out: a linear chain, then
per-column recipes, then custom transformers, then parallel feature extraction,
then tuning the whole thing as one object.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Compose a `Pipeline` of preprocessing plus estimator with one `fit`/`predict`.
2. Route column groups to different recipes with `ColumnTransformer`.
3. Write a custom transformer using `BaseEstimator` and `TransformerMixin`.
4. Combine parallel extractors with `FeatureUnion`.
5. Tune a pipeline with `GridSearchCV` using `step__param` keys.
6. Explain why a pipeline prevents preprocessing leakage across CV folds.
7. Deploy a fitted pipeline so training and serving preprocessing match exactly.

## Prerequisites

- `fit`/`predict`/`transform` estimator API (Topic 01).
- Train/test splitting and leakage (Topics 10, 25).
- Basic pandas column handling.

## 1. The Core Idea

A `Pipeline` bundles every preprocessing step and the final estimator into one
object with a single `fit` / `predict` interface:

```python
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LogisticRegression

pipe = Pipeline([("scale", StandardScaler()), ("clf", LogisticRegression())])
pipe.fit(X_train, y_train)  # fit EVERY step on train only
pipe.predict(X_test)  # reuse the fitted steps on test
```

During `fit`, each step's `fit_transform` runs on the training data and the
output is passed to the next step's `fit`. During `predict`, each step's
`transform` (never `fit`) is applied, then the estimator predicts. This is the
whole trick: the transform step has learned its statistics in training and only
applies them afterward.

**Analogy.** A pipeline is an assembly line that was calibrated on the training
parts; when test parts arrive, the line runs the same calibrated tools rather
than re-calibrating on the parts it is about to inspect.

**When it fails.** If you import a step and call `fit_transform` yourself before
handing data to the pipeline, you have skipped the guarantee. Mixing manual
preprocessing with a pipeline is the common way the protection is lost.

**Exit test.** The exercise asserts that a scaler inside a pipeline sees only
training statistics during CV — the honest score is unchanged by refitting.

## 2. ColumnTransformer — Different Recipes per Column Group

Real data mixes numerics and categoricals, each needing its own treatment:

```python
from sklearn.compose import ColumnTransformer
from sklearn.impute import SimpleImputer
from sklearn.preprocessing import OneHotEncoder

preprocessor = ColumnTransformer(
    [
        (
            "num",
            Pipeline([("impute", SimpleImputer(strategy="median")), ("scale", StandardScaler())]),
            ["age", "income"],
        ),
        (
            "cat",
            Pipeline(
                [
                    ("impute", SimpleImputer(strategy="most_frequent")),
                    ("onehot", OneHotEncoder(handle_unknown="ignore")),
                ]
            ),
            ["plan", "region"],
        ),
    ]
)
```

- Numeric columns: impute → scale.
- Categorical columns: impute → one-hot.
- Unseen categories in test are handled by `handle_unknown="ignore"`, which emits
  an all-zero row for an unknown category instead of raising.

**When it fails.** If a column is listed in no transformer, `ColumnTransformer`
drops it by default. Set `remainder="passthrough"` to keep untouched columns, or
list them explicitly, or you will silently lose features.

## 3. Custom Transformers — `BaseEstimator, TransformerMixin`

Production transforms (outlier clipping, custom text features) belong in
`fit`/`transform` classes so the pipeline can manage their lifecycle:

```python
import numpy as np
from sklearn.base import BaseEstimator, TransformerMixin


class ClipOutliers(BaseEstimator, TransformerMixin):
    def fit(self, X, y=None):
        self.low_ = np.quantile(X, 0.01, axis=0)  # learned on TRAIN only
        self.high_ = np.quantile(X, 0.99, axis=0)
        return self

    def transform(self, X):
        return np.clip(X, self.low_, self.high_)
```

Two conventions matter. Learned attributes get a trailing underscore (`low_`,
`high_`) and are created in `fit`; constructor arguments are stored unchanged as
plain attributes. `fit` must return `self` so the pipeline can chain.

**When it fails.** A transformer that refits inside `transform`, or computes
statistics from the `X` it is given at transform time, reintroduces exactly the
leakage the pipeline exists to prevent.

## 4. FeatureUnion — Parallel Feature Extraction

`FeatureUnion` runs several extractors in parallel and concatenates results —
for example, raw features **plus** engineered polynomials:

```python
from sklearn.pipeline import FeatureUnion
from sklearn.preprocessing import FunctionTransformer


def add_age_squared(X):
    return np.hstack([X, (X[:, :1] ** 2)])


union = FeatureUnion(
    [
        ("raw", FunctionTransformer()),
        ("poly", FunctionTransformer(add_age_squared, validate=False)),
    ]
)
```

**When it fails.** Parallel branches that both learn from data are fine, but the
union is fit inside the pipeline, so it must not be pre-fit. Feature counts grow;
watch memory and downstream training time.

## 5. Tuning the Whole Pipeline

Grid-search the pipeline, not the model: parameter names use double-underscore
paths (`clf__n_estimators`, `prep__num__impute__strategy`). Because the CV
happens on the pipeline, transforms are refit inside every fold — no leakage,
honest scores.

```python
from sklearn.model_selection import GridSearchCV

grid = GridSearchCV(
    full,
    {"clf__max_depth": [5, 10], "prep__num__impute__strategy": ["median", "mean"]},
    cv=5,
)
```

**When it fails.** Tuning a bare estimator and then wrapping it in a pipeline
retrains the preprocessing outside CV; tune the whole pipeline instead.

## 6. Real-World Use Case — Loan Default Risk

```python
full = Pipeline(
    [
        ("prep", ColumnTransformer([...])),
        ("clf", RandomForestClassifier(n_estimators=200, random_state=0)),
    ]
)
grid = GridSearchCV(full, {"clf__max_depth": [5, 10], "clf__n_estimators": [100, 200]}, cv=5)
grid.fit(X_train, y_train)  # one object, no leakage
prob = grid.predict_proba(X_loan)  # deploy the whole pipeline
```

The deployed artifact is the fitted pipeline, not the forest. Whoever serves it
gets the identical imputation, scaling, and encoding that were used in training.

## Common Mistakes to Avoid

1. **Fitting preprocessing before splitting.** The pipeline cannot protect you
   from a leak that already happened.
2. **Forgetting `remainder`.** Unlisted columns are dropped silently.
3. **Not returning `self` from `fit`.** The chain breaks.
4. **Using `fit_transform` on test data.** Only `transform` at inference.
5. **Tuning the bare estimator, then wrapping it.** Tune the pipeline.
6. **`handle_unknown="error"` in production.** A new category crashes the service.
7. **Persisting only the model.** Persist the fitted pipeline as one unit.

## Key Takeaways

1. Pipeline = one `fit`/`predict` unit for preprocess + model.
2. ColumnTransformer routes column groups to different recipes.
3. Custom transformers get train-only fitting for free inside a pipeline.
4. `FeatureUnion` composes parallel extractors.
5. Tune pipelines, never bare models.
6. Deploy the whole pipeline so training and serving transforms match.

## Self-Check Questions

1. Why does a pipeline make preprocessing leakage structurally impossible?
2. What does `remainder="passthrough"` change, and when do you need it?
3. What two conventions make a custom transformer pipeline-compatible?
4. Why is tuning a bare model then wrapping it in a pipeline still leaky?
5. What must be persisted to guarantee identical inference preprocessing?

## Further Reading / Connections

- **Next:** Topic 25, Data Leakage — the failure mode pipelines prevent.
- **Related:** Topic 31, Feature Engineering; Topic 33, Hyperparameter Tuning.
- **Exercise:** `24-sklearn-pipelines.py`.

# Feature Engineering — The Highest-Leverage Work

> **Topic 31 — Modeling depth.** Numeric transforms, encodings (one-hot,
> ordinal, target, hashing), interactions, binning, date and text features —
> and the rule that every encoder fits on train only.

Companion exercise: `31-feature-engineering.py`

---

## Topic Overview

In tabular machine learning the model is the easy part. The difference between
a mediocre and a strong system is usually the quality of the input columns, not
the choice of estimator. Feature engineering is the craft of turning raw data —
timestamps, categories, text, counts — into numbers that expose the signal the
model needs and hide the noise it would otherwise latch onto.

The work divides by data type. Numeric columns need their shape handled (skew,
outliers). Categorical columns need encoding, and the right encoding depends on
cardinality and whether the category is ordered. Text needs vectorisation.
Dates hide cycles and deltas that raw timestamps do not reveal.

Running through all of it is one rule: every encoder learns something from the
data, so it must be fit on the training set only. That rule is the difference
between a feature that helps and a feature that leaks.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose numeric transforms (log, clip, scale) by distribution and model.
2. Select an encoding by cardinality and ordering: one-hot, ordinal, target,
   hashing.
3. Compute target encoding safely with smoothing on train only.
4. Add interaction and polynomial features to capture joint effects.
5. Extract date and text features.
6. Apply the golden rule: fit every encoder on train only, inside a pipeline.

## Prerequisites

- Pipelines and ColumnTransformer (Topic 24).
- Data leakage (Topic 25).
- Regression and tree models for context.

## 1. Why It Wins

The model is the easy part. Feature engineering — turning raw logs into
informative columns — is where tabular ML is won. A strong feature can beat a
better model; the reverse rarely happens.

A useful heuristic: spend ten times as long on features as on hyperparameters.
The returns are asymmetric.

## 2. Numeric Transforms

- **Log transform** fixes right-skewed distributions (income, latency,
  revenue): `np.log1p(x)`.
- **Clip / winsorize** caps outliers learned from train quantiles.
- **Standardization** (z-score) for linear models; trees don't need it.

```python
import numpy as np

X["income_log"] = np.log1p(X["income"])
```

**When it fails.** `log1p` requires non-negative values; log-transform of a
column with negatives or zeros silently produces NaN or -inf. Shift first.

## 3. Encoding Strategies

| Strategy | Use for | Notes |
|---|---|---|
| **One-hot** | Nominal low-cardinality (city, channel) | `handle_unknown="ignore"` |
| **Ordinal** | Ranked categories (free < pro < enterprise) | explicit `categories=` |
| **Target encoding** | High-cardinality categories | mean target per group, **smoothed**, fit on train only |
| **Hashing** | Very high cardinality | fixed-size, collision-tolerant |

**Target encoding** — replace a category with the mean target of its rows —
is the single most powerful encoding for high-cardinality features, and the
easiest to leak: it must be computed from train data only, with smoothing.

```python
# smoothed target encoding: blend group mean with the global prior
enc = (group_sum + prior * k) / (group_count + k)
```

**When it fails.** One-hot on a 50,000-cardinality column explodes the feature
space; target encoding without smoothing overfits rare categories; target
encoding on all rows leaks labels.

## 4. Interactions & Polynomials

`age * salary` captures joint effects:

```python
PolynomialFeatures(degree=2, include_bias=False)
# [age, salary] -> [age, salary, age^2, age*salary, salary^2]
```

**When it fails.** Degree-2 over 100 features creates 5,000+ columns; pair with
feature selection (Topic 32) and beware the memory and training-time blowup.

## 5. Binning

`KBinsDiscretizer` turns continuous values into ordinal buckets (quantile or
uniform) — adds robustness to skewed data and helps linear models.

**When it fails.** Binning throws away resolution; for tree models it is usually
unnecessary because trees already learn thresholds.

## 6. Date Features

Extract the signal hidden in timestamps: hour, day-of-week, month, season,
weekend flag, lags and diffs for time series.

```python
X["hour"] = X["ts"].dt.hour
X["dow"] = X["ts"].dt.dayofweek
X["is_weekend"] = X["dow"] >= 5
```

**When it fails.** Feeding a raw epoch integer to a linear model implies a false
linear trend; cyclical features are better encoded with sine/cosine, though
trees can often use the raw split.

## 7. Text Features

`CountVectorizer` / `TfidfVectorizer` turn short text (bios, notes) into
numeric features. Fit on train only — the vocabulary is learned data.

**When it fails.** Refitting the vectorizer on test produces a different
vocabulary and misaligned columns; keep it in the pipeline.

## 8. The Golden Rule — Fit Encoders on Train Only

Every encoder (one-hot, ordinal, target, tf-idf, binner) has a `fit` step that
learns from data. Fit it on the **training set** and transform the rest —
putting encoders inside a `Pipeline`/`ColumnTransformer` makes this automatic.

## 9. Real-World Use Case — E-commerce Conversion

```python
features = [
    np.log1p(order_count),  # skew fix
    target_encoded(product_category),  # high-cardinality
    price / median_price_per_category,  # relative pricing
    hour_of_day,
    is_weekend,  # temporal signals
    tfidf(customer_bio)[:20],  # text signal
]
```

Relative features (price versus the category median) often carry more signal
than the raw value, because they normalise out the category's scale.

## Common Mistakes to Avoid

1. **Fitting encoders on all data.** Leakage.
2. **One-hot on high cardinality.** Feature explosion.
3. **Target encoding without smoothing.** Overfits rare categories.
4. **Logging negative values.** NaN.
5. **Dropping the original feature without comparing.** Sometimes both help.
6. **Ignoring feature interactions.** Linear models miss them.
7. **Refitting the vectorizer at inference.** Column misalignment.

## Key Takeaways

1. Log for skew, clip for outliers, scale for linear models.
2. One-hot nominal, ordinal ranked, target-encoded high-cardinality.
3. Interactions capture joint effects; binning adds robustness.
4. Dates → hour/dow/month; text → TF-IDF.
5. Every encoder fits on train only — or it leaks.

## Self-Check Questions

1. Which encoding for a 30,000-category product id, and how do you avoid leakage?
2. Why is smoothing needed in target encoding?
3. When does binning help, and for which models?
4. What relative feature would you add for price data, and why?
5. Why must the TF-IDF vocabulary be fit on train only?

## Further Reading / Connections

- **Previous:** Topic 24, Pipelines; Topic 25, Data Leakage.
- **Next:** Topic 32, Feature Selection.
- **Exercise:** `31-feature-engineering.py`.

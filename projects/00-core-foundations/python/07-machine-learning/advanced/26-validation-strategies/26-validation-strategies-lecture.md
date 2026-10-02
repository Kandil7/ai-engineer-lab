# Validation Strategies — When CV Lies

> **Topic 26 — ML rigor series.** K-fold, stratified, group, and time-series
> splitting; nested CV for tuning; train/val/test discipline — and when
> cross-validation gives a lying estimate.

Companion exercise: `26-validation-strategies.py`

---

## Topic Overview

Every performance number you report is a claim about how the model will behave
on data it has not seen. Cross-validation is how you make that claim, and the
splitter you choose decides whether the claim is true. The same model, evaluated
with the wrong splitter, can look excellent and fail in production.

The subtlety is that each dataset carries hidden structure: classes are
imbalanced, rows belong to patients or sessions, time orders the observations.
A splitter that ignores that structure silently tests on information the model
has already seen. This is not a tuning detail; it is the difference between an
honest estimate and a fiction.

This lecture covers the four splitters you will use, nested cross-validation for
tuning, the train/validation/test discipline, and the specific conditions under
which cross-validation lies.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Choose `KFold`, `StratifiedKFold`, `GroupKFold`, or `TimeSeriesSplit` from the
   data's structure.
2. Explain why nested CV is required when hyperparameters are tuned.
3. Apply the train/validation/test division of labour correctly.
4. List the conditions under which CV produces a biased estimate.
5. Diagnose a large CV-vs-test gap.

## Prerequisites

- Train/test splitting (Topic 10).
- Cross-validation basics (Topic 22).
- Leakage classes (Topic 25).

## 1. Why the Splitter Matters

The number your model reports is a **claim about production**. The splitter
decides whether that claim is true. Use the wrong splitter and you get
confident, wrong numbers. The splitter encodes your assumptions about what
"unseen" means: unseen rows, unseen entities, or unseen future.

## 2. The Splitters

### KFold
Shuffles and divides into K folds. Fine for IID data with balanced classes.

### StratifiedKFold
Preserves class proportions in every fold — essential when the positive class
is rare. Without it, a fold can randomly lack the minority class entirely, and
the score becomes noise.

```python
from sklearn.model_selection import StratifiedKFold

cv = StratifiedKFold(n_splits=5, shuffle=True, random_state=0)
```

### GroupKFold
Keeps groups (patients, companies, sessions) entirely inside one fold —
prevents group leakage.

```python
from sklearn.model_selection import GroupKFold

cv = GroupKFold(n_splits=5)
scores = cross_val_score(model, X, y, cv=cv, groups=patient_ids)
```

### TimeSeriesSplit
Expanding-window splits for temporal data: each training fold is a strict
prefix of its test fold's past. Never `shuffle` time.

```python
from sklearn.model_selection import TimeSeriesSplit

cv = TimeSeriesSplit(n_splits=5)
```

**When a splitter fails.** `KFold` on imbalanced data can produce folds with no
positives; `GroupKFold` without `groups` raises; `TimeSeriesSplit` with shuffled
input is meaningless because the order was destroyed before it arrived.

## 3. Nested CV — Tuning Inside CV

Tuning outside CV (pick best params on the whole train set, then report a CV
score) is itself a form of leakage: the data used to choose hyperparameters
was also used to score them.

**Nested CV**: an inner loop picks hyperparameters per outer fold; the outer
loop scores the resulting pipeline on data the inner loop never saw. The
result is the number to trust.

```python
from sklearn.model_selection import GridSearchCV, cross_val_score

inner = GridSearchCV(pipeline, param_grid, cv=3)
outer_scores = cross_val_score(inner, X, y, cv=5)  # unbiased estimate
```

**When it fails.** Nested CV costs `outer × inner × params` fits. Use it when an
unbiased estimate matters more than compute (model selection, reporting), and a
single tuned CV when you only need a working model.

## 4. Train / Validation / Test Discipline

The three-way split:

- **Train** (60%): fit models.
- **Validation** (20%): tune hyperparameters, pick the model.
- **Test** (20%): score exactly once, at the very end.

Touching the test set repeatedly is testing on the test set — the fastest way
to make it lie. Each peek biases the estimate because you start selecting
against it.

**When it fails.** With small data, a single validation split is noisy;
cross-validation on the training portion is the better instrument, and the test
set stays untouched.

## 5. When CV Lies

- Random `KFold` on **time-ordered** data (future leaks into train).
- No stratification on rare classes.
- Groups split across folds.
- Tuning outside CV.
- Leaky preprocessing fit on all data before CV.
- Duplicated rows spanning folds.

Each of these makes the reported score higher than the truth. The gap usually
appears first as a large difference between CV and the held-out test set.

## Common Mistakes to Avoid

1. **`shuffle=True` on time-series.** Destroys temporal order.
2. **Forgetting `groups` with `GroupKFold`.** Raises, or leaks if you use plain
   `KFold` instead.
3. **Reporting the inner CV score of a tuned model as generalisation.** Use
   nested CV.
4. **Repeatedly evaluating on test.** It becomes a validation set.
5. **Ignoring class imbalance in the splitter.** Use stratification.
6. **Assuming CV equals production when the data drifts.** CV cannot see a
   future distribution shift.

## Key Takeaways

1. Splitter choice = the honesty of your reported number.
2. Stratify for imbalance, group for entities, time for sequences.
3. Tune inside CV (nested) or accept optimistic scores.
4. Test set is scored once, at the end, or it stops being a test set.
5. A large CV-vs-test gap means leakage or drift — investigate.

## Self-Check Questions

1. Which splitter for repeated measurements of the same patient, and why?
2. Why is tuning outside CV a form of leakage?
3. When is a single validation split better than CV?
4. What does a big gap between CV and test indicate?
5. Why can `StratifiedKFold` change your score dramatically on rare classes?

## Further Reading / Connections

- **Previous:** Topic 25, Data Leakage; Topic 22, Cross-Validation.
- **Next:** Topic 27, Metrics Deep — choosing what to measure.
- **Exercise:** `26-validation-strategies.py`.

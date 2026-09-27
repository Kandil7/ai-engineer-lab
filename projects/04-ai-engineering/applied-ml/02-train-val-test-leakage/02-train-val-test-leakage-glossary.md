# Applied ML 02: Train/Validation/Test and Leakage — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Train set | Data the model fits on | 70% |
| Validation set | Data for tuning and selection | 15% |
| Test set | Data for final measurement, once | 15% |
| Target leakage | Label/future info leaking into features | feature from answer |
| Temporal leakage | Future data in training | time split by time |
| Group leakage | Same source in train and test | same book both sides |
| Group split | Splitting by source, not by row | by book_id |

---

## Alphabetical Glossary

### Group leakage

**Definition:** Rows from the same source appearing in both train and test,
letting the model recognize the source instead of generalizing.

**Example:**
```python
# passages from book b1 in both train and test -> memorizes b1
```

**Related concepts:** Group split, Leakage

---

### Group split

**Definition:** Splitting by source identity (book_id) rather than by row,
so no source appears on both sides of the split.

**Example:**
```python
train = [p for p in passages if p["book_id"] in train_books]
```

**Related concepts:** Group leakage, Test set

---

### Leakage

**Definition:** Information from outside the training signal entering the
model, inflating scores. Target, temporal, and group are the main patterns.

**Example:**
```python
# a feature computed from the answer: target leakage
```

**Related concepts:** Target leakage, Temporal leakage, Group leakage

---

### Target leakage

**Definition:** The label or future information leaking into the features,
so the model "cheats" by reading the answer.

**Example:**
```python
# feature = did the user click? when predicting the click
```

**Related concepts:** Leakage

---

### Temporal leakage

**Definition:** Training on data from after the test period. Time-series data
must be split by time, not randomly.

**Example:**
```python
# train on 2026-09, test on 2026-08: the future leaked
```

**Related concepts:** Leakage

---

### Test set

**Definition:** The final, untouched measurement set. Evaluated once; any
influence on decisions corrupts it.

**Example:**
```python
# measured once at the end, never tuned against
```

**Related concepts:** Validation set, Train set

---

### Train set

**Definition:** The data the model fits on. The largest split; the model
learns its parameters here.

**Example:**
```python
train = data[:0.7]
```

**Related concepts:** Validation set, Test set

---

### Validation set

**Definition:** The tuning set: hyperparameters and candidate selection
happen here so test stays untouched.

**Example:**
```python
val = data[0.7:0.85]
```

**Related concepts:** Train set, Test set

---

## Related Concepts

- **Precision/recall**: the metrics measured on test (topic 03)
- **Error analysis**: what the test failures reveal (topic 04)
- **Golden sets**: the eval analog of a clean test set

## Key Takeaways

1. Train fits, validation tunes, test measures once.
2. Test must never influence decisions.
3. Split by group when rows share a source.
4. High scores are a leakage symptom.
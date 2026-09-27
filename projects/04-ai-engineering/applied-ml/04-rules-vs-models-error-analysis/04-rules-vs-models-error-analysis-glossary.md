# Applied ML 04: Rules vs Models and Error Analysis — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Rule baseline | Hand-written heuristic every model must beat | keyword classifier |
| Rules-vs-model | Deciding when a rule suffices | small/deterministic problems |
| Error analysis | Clustering failures to find the cause | loop, not a step |
| Failure cluster | A group of failures sharing a pattern | same class, same shape |
| Data failure | Wrong labels, missing values, duplicates | fix the data |
| Feature failure | Features miss the signal | fix the representation |
| Model failure | Model can't fit the pattern | fix capacity/algorithm |

---

## Alphabetical Glossary

### Data failure

**Definition:** A failure layer where the data is wrong: bad labels, missing
values, duplicates. Re-training fixes nothing; fixing the data does.

**Example:**
```python
# mislabeled training rows -> model learns the wrong boundary
```

**Related concepts:** Error analysis, Feature failure

---

### Error analysis

**Definition:** The loop of collecting failures, clustering them by pattern,
finding the cause, fixing it, and re-measuring. The engine of model
improvement.

**Example:**
```python
# failures -> cluster -> cause -> fix -> re-measure
```

**Related concepts:** Failure cluster, Data failure

---

### Failure cluster

**Definition:** A group of failures sharing a pattern — the same class, the
same input shape. Clustering is what turns failures into a fixable cause.

**Example:**
```python
# all "who" questions misclassified as "other"
```

**Related concepts:** Error analysis

---

### Feature failure

**Definition:** A failure layer where the features miss the signal. The
representation is wrong; adding more of the same features fixes nothing.

**Example:**
```python
# no feature captures the distinguishing word
```

**Related concepts:** Error analysis, Model failure

---

### Model failure

**Definition:** A failure layer where the model cannot fit the pattern —
insufficient capacity or the wrong algorithm. More data won't fix it.

**Example:**
```python
# a linear model on a nonlinear boundary
```

**Related concepts:** Error analysis, Feature failure

---

### Rule baseline

**Definition:** A hand-written heuristic that every model must beat. If the
model cannot beat the rule, the model is not earning its complexity.

**Example:**
```python
# keyword classifier as the baseline for a question-type model
```

**Related concepts:** Rules-vs-model

---

### Rules-vs-model

**Definition:** The decision of whether a problem needs a model at all.
Rules win on small, deterministic, explainable problems.

**Example:**
```python
# exact-match routing: a rule, not a model
```

**Related concepts:** Rule baseline

---

## Related Concepts

- **Confusion matrix**: the raw material for error analysis (topic 03)
- **Precision/recall**: the metrics the comparison uses (topic 03)
- **Leakage**: a failure cause to rule out first (topic 02)

## Key Takeaways

1. Rules win on small, deterministic problems.
2. The rule is the baseline every model must beat.
3. Error analysis is a loop, not a step.
4. Diagnose the failure layer before fixing.
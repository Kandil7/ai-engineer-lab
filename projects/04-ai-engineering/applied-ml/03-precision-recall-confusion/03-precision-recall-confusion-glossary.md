# Applied ML 03: Precision/Recall and Confusion Matrix — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Confusion matrix | TP/FP/FN/TN table of predictions vs actuals | 2x2 grid |
| True positive (TP) | Predicted yes, actually yes | correct catch |
| False positive (FP) | Predicted yes, actually no | false alarm |
| False negative (FN) | Predicted no, actually yes | miss |
| True negative (TN) | Predicted no, actually no | correct reject |
| Precision | TP / (TP + FP) | when we say yes, are we right? |
| Recall | TP / (TP + FN) | did we catch the yeses? |
| F1 | Harmonic mean of precision and recall | imbalance-penalizing |

---

## Alphabetical Glossary

### Confusion matrix

**Definition:** The table of predicted-vs-actual outcomes: TP, FP, FN, TN.
The raw material from which precision and recall are derived.

**Example:**
```python
# [[TP, FN], [FP, TN]]
```

**Related concepts:** Precision, Recall

---

### False negative (FN)

**Definition:** Predicted no, actually yes — a miss. The error recall
penalizes.

**Example:**
```python
# a relevant passage the retriever did not return
```

**Related concepts:** Recall, Confusion matrix

---

### False positive (FP)

**Definition:** Predicted yes, actually no — a false alarm. The error
precision penalizes.

**Example:**
```python
# a spam flag on a real email
```

**Related concepts:** Precision, Confusion matrix

---

### F1

**Definition:** The harmonic mean of precision and recall, penalizing
imbalance between them. A single summary number for classifier quality.

**Example:**
```python
f1 = 2 * p * r / (p + r)
```

**Related concepts:** Precision, Recall

---

### Precision

**Definition:** TP / (TP + FP): of what the model predicted yes, how much
was right. The "false alarm" metric.

**Example:**
```python
precision(tp, fp)  # 0.9 = 90% of yes-predictions were correct
```

**Related concepts:** Recall, False positive

---

### Recall

**Definition:** TP / (TP + FN): of what was actually yes, how much the model
caught. The "miss" metric.

**Example:**
```python
recall(tp, fn)  # 0.8 = caught 80% of the real yeses
```

**Related concepts:** Precision, False negative

---

### True negative (TN)

**Definition:** Predicted no, actually no — a correct rejection. The quiet
cell that accuracy overweights.

**Example:**
```python
# correctly not flagged as spam
```

**Related concepts:** Confusion matrix

---

### True positive (TP)

**Definition:** Predicted yes, actually yes — a correct catch. The cell both
precision and recall reward.

**Example:**
```python
# a relevant passage correctly retrieved
```

**Related concepts:** Precision, Recall

---

## Related Concepts

- **Error analysis**: reading the matrix for failure patterns (topic 04)
- **Threshold**: the dial trading precision against recall
- **Imbalanced data**: why accuracy lies

## Key Takeaways

1. The matrix is raw material; metrics are derived.
2. Precision for false alarms, recall for misses.
3. Metric choice is a cost decision.
4. Accuracy lies on imbalanced data.
# Applied ML 03: Precision/Recall and the Confusion Matrix

## 🎯 Topic Overview

Accuracy lies when classes are imbalanced. Precision and recall tell the
truth about what a classifier actually does, and the confusion matrix shows
where it fails. This lecture covers the four cells, the two rates, the
precision-recall tradeoff, and how to read a confusion matrix for error
analysis.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Read a confusion matrix: TP, FP, FN, TN
2. Compute precision, recall, and F1 from the matrix
3. Explain the precision-recall tradeoff and when each matters
4. Choose the right metric for the cost of each error type
5. Use the confusion matrix to drive error analysis

---

## 1. The Four Cells

```python
# Predicted vs actual
#              predicted yes   predicted no
# actual yes   TP              FN
# actual no    FP              TN
```

True positive: predicted yes, actually yes. False positive: predicted yes,
actually no (a false alarm). False negative: predicted no, actually yes (a
miss). True negative: predicted no, actually no. The matrix is the raw
material; precision and recall are derived from it.

## 2. Precision and Recall

```python
def precision(tp, fp):
    return tp / (tp + fp)  # of what we predicted yes, how much was right


def recall(tp, fn):
    return tp / (tp + fn)  # of what was actually yes, how much we caught
```

**Precision** answers "when the model says yes, is it right?" **Recall**
answers "of the real yeses, how many did the model catch?" They trade off:
raising the threshold raises precision and lowers recall; lowering it does
the reverse.

## 3. The Tradeoff and the Cost

Which matters more depends on the cost of each error. For retrieval, recall
matters (missing a relevant passage is worse than a false alarm). For
spam filtering, precision matters (a false positive deletes a real email).
The metric choice is a cost decision, not a preference.

## 4. F1 and the Imbalance Trap

F1 is the harmonic mean of precision and recall — a single number that
penalizes imbalance. Accuracy is useless on imbalanced data: a classifier
that always predicts the majority class scores high accuracy and zero
recall on the minority. Always report precision and recall, not accuracy
alone.

## 5. Reading the Matrix for Errors

The confusion matrix shows failure patterns: a column with high FP means
the model over-predicts that class; a row with high FN means it misses it.
For a question-type classifier, the matrix reveals which types get confused
with which — the raw material for error analysis and the roadmap's exit
test ("interpret the confusion matrix").

## Common Mistakes

- Reporting accuracy on imbalanced data.
- Choosing precision or recall without considering error cost.
- Forgetting the matrix is the raw material, metrics are derived.
- Tuning the threshold without re-reading the matrix.

## Key Takeaways

1. The matrix is raw material; precision and recall are derived.
2. Precision: when we say yes, are we right? Recall: did we catch the yeses?
3. Metric choice is a cost decision.
4. Accuracy lies on imbalanced data.
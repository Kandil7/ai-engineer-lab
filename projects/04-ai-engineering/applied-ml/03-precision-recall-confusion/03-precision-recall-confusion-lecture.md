# Applied ML 03: Precision/Recall and the Confusion Matrix

## Topic Overview

Accuracy is the most reported metric and the most misleading one on real data.
When one class is rare, a classifier that never predicts it can score 99% accuracy
and be worthless. Precision and recall are the two rates that survive imbalance,
and the confusion matrix is the raw material both are derived from. If you report
one number for a classifier and that number is accuracy on imbalanced data, you
have almost certainly hidden the failures that matter.

This lecture builds the four cells of the matrix, the two rates, the tradeoff
between them, and the harmonic mean that balances them. It then teaches the part
that is usually skipped: choosing the metric from the cost of each error, because
"is precision or recall better" has no answer until you say what a false positive
and a false negative actually cost.

The same reasoning carries into retrieval, where recall@k and MRR are the
list-shaped versions of these ideas, and into error analysis, which starts from
the pattern of the matrix rather than from a single score.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Read a confusion matrix and name all four cells correctly.
2. Compute precision, recall, F1, and accuracy from the four counts.
3. Explain the precision-recall tradeoff and how a decision threshold moves it.
4. Choose the metric from the cost of each error type rather than by habit.
5. Use the confusion matrix to find error clusters instead of one aggregate score.
6. Map these ideas onto retrieval metrics such as recall@k, MRR, and nDCG.

## Prerequisites

- Applied ML 02 (a clean train/validation/test split), because a leaked split
  makes every metric in this lecture meaningless.
- Basic arithmetic and the idea of a ratio.

---

## 1. The Four Cells

### The matrix

```python
# Predicted vs actual
#              predicted yes   predicted no
# actual yes   TP              FN
# actual no    FP              TN
```

- **True positive (TP):** predicted yes, actually yes.
- **False positive (FP):** predicted yes, actually no. A false alarm.
- **False negative (FN):** predicted no, actually yes. A miss.
- **True negative (TN):** predicted no, actually no.

### The matrix is the raw material

Every rate is derived from these four counts. That is why you should always look
at the matrix and never only at a single summary number: the summary throws away
which failures happened, and the pattern of failures is the actionable part.

### Multi-class matrices

With more than two classes the matrix becomes square, with one row per actual
class and one column per predicted class. The diagonal is correct predictions and
the off-diagonal cells show which classes get confused with which, which is the
starting point for error analysis.

## 2. Precision and Recall

### The two rates

```python
def precision(tp: int, fp: int) -> float:
    return tp / (tp + fp)  # of what we said yes, how much was right


def recall(tp: int, fn: int) -> float:
    return tp / (tp + fn)  # of what was really yes, how much we caught
```

**Precision** answers: when the model says yes, how often is it right? Its
denominator is everything the model flagged, right or wrong, so it drops when the
model raises false alarms.

**Recall** answers: of all the real positives, how many did the model catch? Its
denominator is everything that was actually positive, so it drops when the model
misses things.

### They answer different questions

Neither is "better". Precision is about the quality of the positives you returned.
Recall is about the coverage of the positives that exist. A model tuned for one
usually pays on the other, and which you want depends entirely on what an error
costs.

### A baseline sanity check

The prevalence of the positive class is `(TP + FN) / total`. A model whose recall
is near that number may be doing little better than guessing the base rate, which
is a useful smell test on imbalanced data.

## 3. The Tradeoff and the Cost of Each Error

### The threshold

Most classifiers produce a score between 0 and 1, and a threshold turns the score
into a decision. Raising the threshold makes the model more conservative: fewer
false alarms (precision up) but more misses (recall down). Lowering it does the
reverse.

### Cost decides, not preference

- **Retrieval.** Missing a relevant passage (FN) is usually worse than surfacing an
  extra one (FP), because a later reranker can demote the extra but cannot recover
  the missing one. Recall matters first.
- **Spam filtering.** A false positive deletes a real email; a false negative
  leaves one spam message. Precision matters more.
- **Content safety.** A false negative ships harmful content; a false positive
  annoys a user. Usually recall on the harmful class matters more, paired with a
  human review queue for the positives.

The metric is a cost decision that you document and defend.

### The threshold must be fixed before comparing

If you compare model A at threshold 0.5 and model B at threshold 0.3, the
difference you measure is partly the thresholds, not the models. Choose the
threshold on the validation set, then compare on test.

## 4. F1 and the Accuracy Trap

### F1

F1 is the harmonic mean of precision and recall:

```python
def f1(p: float, r: float) -> float:
    return 2 * p * r / (p + r)
```

It is high only when both are high, so it penalizes lopsided models. Use it when
you genuinely need one number and the two errors cost a similar amount. It still
hides the split between precision and recall, so report all three when the cost is
asymmetric.

### Accuracy and the imbalance trap

```python
def accuracy(tp: int, tn: int, fp: int, fn: int) -> float:
    return (tp + tn) / (tp + tn + fp + fn)
```

Consider 100 positives among 10,000 items. A classifier that predicts "no" for
everything scores 99% accuracy and catches nothing:

```python
assert accuracy(0, 9900, 0, 100) == 0.99  # 0 positives caught
```

The exercise makes the point concrete on a rare-class classifier: accuracy above
0.98 while 20 positives are missed and 100 false alarms are raised. Report
precision and recall, always, and never report accuracy alone on imbalanced data.

## 5. Reading the Matrix for Error Patterns

### Columns and rows

A column with many false positives means the model over-predicts that class. A row
with many false negatives means it misses that class. Off-diagonal cells in a
multi-class matrix show which classes are confused.

### From numbers to clusters

The value of the matrix is the pattern, not the total. If every false negative in
the "how" class is a question beginning with "لماذا" or "ما هو", the failure is not
random, it is a coverage gap in the features or rules. That observation is the whole
point of error analysis (Applied ML 04).

### Calibration versus ranking

The matrix uses hard decisions. If you care about ranking quality, look at the
score distribution and calibration instead of the thresholded labels. A model can
rank perfectly and still score poorly at a badly chosen threshold, and a model can
score well at a threshold while ranking badly.

## 6. A Metric Decision Procedure

1. State the cost of a false positive and of a false negative.
2. If they differ a lot, optimize the costlier error, and report both rates.
3. If they are comparable and classes are balanced, accuracy or F1 may be fine.
4. If classes are imbalanced, never report accuracy alone.
5. Fix the threshold on validation, then measure once on test.
6. Record the metric, the threshold, and the cost argument in the evaluation
   report or ADR.

## 7. Retrieval Versions of These Metrics

Retrieval is classification turned into a ranked list, and the metrics are the
same ideas with a cutoff:

- **Recall@k:** of the passages that should be returned, how many are in the top
  k? This is recall with a rank cutoff.
- **Precision@k:** of the top k, how many are relevant?
- **MRR:** how high is the first relevant result ranked, averaged over queries.
- **nDCG:** a graded ranking quality that rewards relevant items near the top,
  useful when relevance is not binary.

The retrieval exit test reports recall@k and MRR side by side so that a change
which improves ranking near the top is visible separately from a change in how much
is found at all. That separation is the retrieval form of the precision-recall
tradeoff.

## Real-World Application

- Choosing the threshold for a DevMate input guardrail: block fewer harmful inputs
  at the cost of more false alarms, or the reverse, decided by measured cost.
- Reporting Athar retrieval with recall@5 and MRR rather than a single accuracy
  number.
- Explaining in an interview why a 99% accuracy figure on a rare-class task is a red
  flag, and producing the confusion matrix instead.
- Setting alert thresholds where a missed detection costs far more than a false
  page.

## Common Mistakes

1. **Reporting accuracy on imbalanced data.** The majority-class classifier wins on
   paper and fails in production.
2. **Choosing precision or recall without a cost argument.** The choice must be
   justified, not habitual.
3. **Ignoring the matrix.** The pattern of errors is the actionable part; the
   aggregate hides it.
4. **Tuning the threshold without re-reading the matrix.** Each threshold move
   changes which cells fill.
5. **Treating precision and recall as interchangeable.** They answer different
   questions.
6. **Comparing models at different thresholds.** Fix the threshold on validation
   before comparing.
7. **Optimizing F1 when the costs are asymmetric.** A high F1 can still hide an
   unacceptable false-negative rate.

## Key Takeaways

1. The matrix is raw material; precision and recall are derived from it.
2. Precision: of what we flagged, how much was right. Recall: of the real
   positives, how much we caught.
3. The metric is a cost decision; state the cost of each error and record the
   threshold.
4. Accuracy lies on imbalanced data; F1 balances precision and recall but still
   hides asymmetry.
5. Retrieval's recall@k, MRR, and nDCG are the list-shaped versions of the same
   reasoning.

## Self-Check Questions

1. A classifier catches 80 of 100 positives and raises 100 false alarms. Compute
   precision, recall, and accuracy.
2. Why is a majority-class classifier dangerous on imbalanced data?
3. For Athar retrieval, would you optimize precision or recall first, and why?
4. What does a column of the confusion matrix with many false positives tell you?
5. How is recall@5 related to recall, and why report it together with MRR?
6. You move the threshold from 0.5 to 0.7. Which cells of the matrix change, and in
   which direction?

## Further Reading / Connections

- Applied ML 02 (train/validation/test and leakage) — the split that makes these
  numbers honest.
- Applied ML 04 (rules versus models) — the loop that turns matrix patterns into
  fixes.
- `projects/04-ai-engineering/ai-evaluation/03-retrieval-evaluation` — recall@k and
  MRR inside a full harness.
- `docs/reference/ml-fundamentals-map.md` — the metrics and evaluation sections this
  lecture operationalizes.

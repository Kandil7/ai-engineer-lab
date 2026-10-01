# Applied ML 05: Baseline Intent Classifier — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Intent classification | Mapping a question to a type/category | "كيف أتعلم" → `how` |
| Baseline | The cheapest reasonable approach others must beat | keyword rules |
| Majority baseline | Always predicting the most common label | the floor to clear |
| Group split | Split by source so no source straddles train/test | split by `book`/`source` |
| Group leakage | Same source in train and test | model memorizes the source |
| Naive Bayes | Probabilistic classifier from token counts | multinomial NB |
| Laplace smoothing | Adding 1 to counts so unseen tokens don't zero a class | avoiding zero probability |
| Log-prior | log P(label) from the training distribution | class imbalance handling |
| Precision | Of predicted positives, how many are right | Applied ML 03 |
| Recall | Of real positives, how many were caught | Applied ML 03 |
| F1 | Harmonic mean of precision and recall | per-class score |
| Macro-F1 | Mean of per-class F1; weights classes equally | rare class counts |
| Error report | The list of misclassifications with context | the fix's input |
| Exit artifact | The shipped deliverable that proves a skill | this script |

---

## Alphabetical Glossary

### Baseline

**Definition:** The smallest, cheapest reasonable approach to a task, used as the bar a
learned model must beat. Here it is the keyword rule.

**Example:**
```python
rule_classify("من هو الخوارزمي")  # "who"
```

**Related concepts:** Majority baseline, Rules versus models

### Error report

**Definition:** A list of misclassifications (text, gold, predicted, source) used to find
the failure pattern and route the fix to the right layer.

**Example:**
```python
[("لخص هذا النص", "other", "who", "s4")]
```

**Related concepts:** Error analysis, Failure layer

### Group leakage

**Definition:** When rows sharing a source appear in both train and test, so the model
learns to recognize the source rather than the label. Prevented by a group split.

**Example:**
```python
assert not (train_sources & test_sources)  # no group straddles
```

**Related concepts:** Group split, Split

### Group split

**Definition:** Splitting data by a group key (here, `source`) so every group goes
entirely to train or entirely to test.

**Example:**
```python
train, test = split_by_source(rows, train_frac=0.6)
```

**Related concepts:** Group leakage, Train/validation/test

### Laplace smoothing

**Definition:** Adding 1 to every token count (and the vocabulary size to the
denominator) so a token unseen in a class does not assign that class zero probability.

**Example:**
```python
self.log_likelihood[label][tok] = math.log((counts[tok] + 1) / (total + v))
```

**Related concepts:** Naive Bayes

### Macro-F1

**Definition:** The unweighted mean of per-class F1 scores, so each class contributes
equally regardless of frequency.

**Example:**
```python
sum(prf(golds, preds, label)[2] for label in LABELS) / len(LABELS)
```

**Related concepts:** F1, Per-class metrics

### Majority baseline

**Definition:** A classifier that always predicts the most common training label. It is
the floor: a model that does not beat it has learned nothing.

**Example:**
```python
maj = Counter(golds).most_common(1)[0][0]
```

**Related concepts:** Baseline

### Naive Bayes

**Definition:** A probabilistic classifier that assumes token independence and combines
per-token log-probabilities with the class log-prior. Small, fast, and deterministic.

**Example:**
```python
model = NaiveBayes().fit(train)
model.predict("كيف أتعلم")
```

**Related concepts:** Laplace smoothing, Log-prior

### Per-class precision/recall/F1

**Definition:** Precision, recall, and F1 computed for one class at a time, revealing
which classes the model handles and which it misses.

**Example:**
```python
p, r, f1 = prf(golds, preds, "how")
```

**Related concepts:** Macro-F1, Confusion matrix

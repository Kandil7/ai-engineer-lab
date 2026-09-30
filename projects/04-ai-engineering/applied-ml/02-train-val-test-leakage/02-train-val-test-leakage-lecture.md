# Applied ML 02: Train/Validation/Test and Leakage

## Topic Overview

A model's job is to generalize, not to memorize. Every metric you report is a
claim about how the model will behave on data it has never seen, and the
train/validation/test split is the only thing standing between that claim and a
comfortable fiction. Get the split wrong and the number you trust is measuring
the wrong thing.

Leakage is the name for every way that fiction gets built. The model looks
excellent on paper because information it should not have seen reached it during
training or during evaluation. Leakage is rarely a dramatic crash; it is a quiet
inflation of a score that survives until production, where the missing
information does not exist and the model fails.

This lecture covers the three-way split, why the test set is different in kind
from the other two, and the three leakage patterns that account for most
"surprisingly good" results: target leakage, temporal leakage, and group
leakage. For Athar, group leakage is the one that matters most, because passages
from the same book are not independent rows.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Split data into train, validation, and test with a stated rationale for the
   sizes and the boundary.
2. Explain why the test set must never influence any training or design decision.
3. Identify the three leakage patterns (target, temporal, group) in a dataset.
4. Split by group when rows share a source, and prove a random split leaks.
5. Treat a suspiciously high score as a leakage symptom and run a diagnosis
   checklist instead of celebrating it.
6. Connect the split discipline to the roadmap exit test: comparing methods on
   the same held-out set.

## Prerequisites

- Applied ML 01 (vectors and similarity) for the idea of a feature space.
- Basic comfort with Python lists and dictionaries; the exercises are stdlib only.
- The Athar contracts idea (a passage carries a mandatory `book_id` and `page`).

---

## 1. Why Generalization Is the Only Thing That Matters

### What a model actually learns

A model does not learn "the truth". It learns a function that maps the features
it was shown to the labels it was shown, by minimizing error on those specific
examples. The risk is that the function memorizes the examples instead of
capturing the pattern. A model that memorizes every training row and nothing
else will score perfectly on that data and fail on everything else.

### Memorization versus generalization

Generalization is performance on data drawn from the same distribution but not
seen during training. It is the only property that transfers to production. A
model that generalizes a little is more valuable than a model that memorizes
perfectly, because production is made entirely of unseen data.

### The measurement problem

You cannot measure generalization on the data you trained on, because the model
has already seen it and any score there is contaminated by memorization. You
need a set the model has never seen. That set is the test set, and the whole
discipline of this lecture is about protecting its honesty.

## 2. The Three-Way Split

### The three roles

Each split has a distinct job:

| Split | Job | How often used |
| --- | --- | --- |
| **Train** | Fit the parameters | Many times, during training |
| **Validation** | Choose hyperparameters, compare candidate models, decide when to stop | Many times, during development |
| **Test** | Estimate final performance, once | Ideally exactly once, at the end |

### Why three and not two

If you tune on train, the model overfits your tuning. If you tune on test, the
test set stops being a test set: you have started optimizing against it, and its
score no longer estimates unseen performance. Validation absorbs every decision
so that test stays clean.

### Kinds of results and why the split must be stable

Every time you compare two approaches ("recall@5 with reranking versus without")
you must compare them on the *same* held-out set. If you change the gold set
between runs, the difference you measure is partly the set, not the method. This
is the roadmap's exit test for retrieval: the gold set is fixed, and only the
method changes.

### Sizes and the 70/15/15 starting point

```python
# 70/15/15 is a starting point, not a law.
# With little data: 60/20/20. With a lot: 98/1/1 (still keep a real test).
train, val, test = (
    data[: int(0.70 * n)],
    data[int(0.70 * n) : int(0.85 * n)],
    data[int(0.85 * n) :],
)
```

The exact fractions matter less than the discipline: test is decided once, and
the boundary is defined by the *group* (see section 6), not by the row.

### Stratification

If classes are imbalanced, a random split can put almost none of a rare class in
validation. Stratified splitting preserves the class proportions in each split.
For a first pass on a small dataset, stratification is usually worth it.

## 3. Why the Test Set Must Stay Untouched

### The referee analogy

The test set is a referee. A referee who is also your coach has stopped being a
referee. The moment you look at the test score and change the model, the test set
has influenced the model, and the next test score is no longer an unbiased
estimate.

### The adaptive overfitting loop

It is subtle because it is gradual. Look at test, tweak a feature, look at test,
tweak a threshold, look at test. Each step is small, but over twenty steps you
have fit the model to the test set through the human in the loop. The final score
is optimistic and you have no way to know by how much.

### The discipline rule

Evaluate test once, at the end, with the model already frozen. Report that
number. If you need to keep iterating after seeing it, the test set is spent.

### When you break the rule

If the test set has been used, create a fresh one from data it never touched, or
send the old test set back into development and carve a new test set from a
reserve. Do not pretend the contaminated number is still honest.

## 4. Target Leakage

### Definition

Target leakage is when a feature contains information about the label that would
not be available at prediction time. The model learns to read the answer off the
feature.

### The classic example

Predicting whether a patient will be readmitted, using a feature "discharge
disposition" that is only recorded *because* the patient was readmitted. The
feature encodes the label, so the model scores near-perfectly and is useless.

### The Athar example

Predicting whether a passage is "about prayer" using a feature computed from the
section it was filed under, when the section was chosen by a human who read the
passage. The feature is downstream of the label.

### Detection and fix

Ask of every feature: "at the moment of prediction, would this value already be
known?" If the answer requires information from the future, the label, or a
human who saw the label, remove the feature. The fix is almost always to drop or
recompute the feature, not to tune the model.

## 5. Temporal Leakage

### Definition

Temporal leakage is training on data from after the moment you are predicting.
The model sees the future, so it scores well on a past it already knows.

### The random-shuffle error

The default `train_test_split` shuffles rows. On time-ordered data this places
future rows in train and past rows in test, which is the opposite of how the
model will be used. A stock price "predictor" that shuffles will look
clairvoyant.

### Time-series splits

Split by time, not randomly: train on everything before a cutoff, test on
everything after. For repeated evaluation, use a walk-forward (rolling origin)
scheme: move the cutoff forward and re-measure.

```python
cutoff = "2026-06-01"
train = [r for r in rows if r["date"] < cutoff]
test = [r for r in rows if r["date"] >= cutoff]
```

### Detection and fix

If the data has a timestamp that matters (logs, events, conversations, corpus
acquisition order), sort by it and split on a boundary. Never shuffle time.

## 6. Group Leakage

### Definition

Group leakage is when multiple rows that belong to one source or entity are
split across train and test. The model does not learn the pattern; it learns to
recognize the group, and it is tested on the same groups it trained on.

### Why random splits fail on grouped data

Random row splits assume rows are independent. When they are not, some rows from
each group land in train and the rest in test. The model memorizes the group's
signature and the test score measures recognition, not generalization.

### The Athar case

Athar passages are not independent. Ten passages from the same book share
vocabulary, formatting, and subject. If book `b2` has passages in both train and
test, the model can recognize the book rather than learn the task. The split
must be by `book_id`, so that every book lives entirely in one split.

### Splitting by group

```python
def group_split(passages: list[dict], train_frac: float = 0.7) -> tuple[list, list]:
    """Split by book_id so no book appears in both train and test."""
    books = sorted({p["book_id"] for p in passages})
    train_books = set(books[: int(train_frac * len(books))])
    train = [p for p in passages if p["book_id"] in train_books]
    test = [p for p in passages if p["book_id"] not in train_books]
    return train, test
```

`sklearn.model_selection.GroupShuffleSplit` does the same thing when you have
scikit-learn available; the stdlib version above makes the mechanism visible.

### Proving the leak

Run the exercise `/02-train-val-test-leakage.py --verify`. It asserts two things:
the group split keeps every book on one side, and a naive random split of the
same passages leaves book `b2` straddling the boundary. That straddle *is* the
leak, made visible in one assert.

## 7. Diagnosing Leakage

### The first symptom

A suspiciously high score is the symptom, not the win. If validation accuracy is
0.99 on a task you expected to be hard, assume leakage until you have ruled it
out.

### The checklist

1. Does any feature use the label, directly or indirectly?
2. Does any feature require information from the future?
3. Was the split random on data with a meaningful time order?
4. Do rows share a source, and did the split respect it?
5. Did preprocessing (scaling, encoding, deduplication) fit on train only, or on
   all data before the split? Fitting a scaler on the full dataset leaks test
   statistics into training.
6. Was test used more than once?

### The fix

The fix is usually a re-split, not a model change: split by group, split by time,
fit preprocessing on train only, and drop label-derived features. Re-run and
expect the honest score to be lower. The lower score is the useful one.

### Connection to the exit test

The roadmap's retrieval exit test compares lexical, dense, hybrid, and
hybrid+rerank on the *same* held-out questions and reports Recall@k and MRR side
by side. None of those numbers mean anything if the gold set leaked into tuning
or if passages from a test question's source also appeared in development. Clean
split first, then measure.

## Real-World Application

- **Athar retrieval evaluation.** The golden set of questions must be split so
  that no source book's passages appear on both sides. Otherwise reranking will
  look better than it is.
- **DevMate eval harness.** The `devmate-golden.jsonl` questions are held out
  from any chunking or rerank tuning; the harness re-runs the frozen set.
- **Any time-series feature.** Cost, latency, and traffic models must be split by
  time, or the model learns the future.
- **Fine-tuning datasets (Baligh).** If a book contributes examples to both the
  SFT set and the eval set, the eval measures memorization of that book.

## Common Mistakes

1. **Tuning on test.** The referee becomes a coach; every later score is
   optimistic. Use validation for all decisions.
2. **Random splits on grouped data.** Passages, users, or documents from one
   source straddle the boundary and the model recognizes the source.
3. **Features computed from the label.** Target leakage inflates scores until
   production, where the feature's inputs do not exist.
4. **Shuffling time-ordered data.** Temporal leakage makes the model look
   clairvoyant on the past.
5. **Fitting preprocessing on all data.** Scaling, encoding, or deduplication
   computed before the split leaks test statistics into train.
6. **Reporting the best of several test runs.** That is test-set tuning by
   another name.
7. **Treating a high score as good news.** It is a hypothesis that leakage
   exists, and it is usually right.

## Key Takeaways

1. Train fits, validation tunes, test measures once; test must not influence any
   decision.
2. Leakage is silent inflation, not a crash; the symptom is a suspiciously high
   score.
3. The three patterns: target (uses the label), temporal (uses the future), group
   (same source on both sides).
4. When rows share a source, split by the source; for Athar, split by `book_id`.
5. Compare methods on one fixed held-out set; changing the set changes the
   measurement.

## Self-Check Questions

1. Why does the validation split exist if you already have a test split?
2. You get 0.98 accuracy on a task you expected to be hard. Name three leakage
   patterns you would check before trusting it.
3. Athar has 200 books and 40,000 passages. Describe the split you would use and
   why a random row split is wrong.
4. Your scaler is fit on the full dataset and then the data is split. Which kind
   of leakage is this, and what is the fix?
5. You have already looked at the test score twice and adjusted the model each
   time. What should you do to restore an honest estimate?

## Further Reading / Connections

- Applied ML 03 (precision/recall/confusion) — what to measure once the split is
  clean; a leaked split makes every metric wrong.
- Applied ML 04 (rules versus models, error analysis) — how to read the honest
  score and find where the model fails.
- `projects/04-ai-engineering/ai-evaluation/01-gold-datasets-annotation` — how
  the held-out set is built and annotated.
- `docs/reference/ml-fundamentals-map.md` — the leakage and validation-strategy
  sections this lecture operationalizes.
- `docs/learning/deep-dives/athar-retrieval-deep-dive.md` — where the by-book
  split matters in the real system.

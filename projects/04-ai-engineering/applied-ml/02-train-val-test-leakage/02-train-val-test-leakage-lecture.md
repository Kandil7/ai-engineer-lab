# Applied ML 02: Train/Validation/Test and Leakage

## 🎯 Topic Overview

A model's job is to generalize, not memorize. The train/validation/test
split exists to measure generalization honestly, and leakage is how that
measurement gets corrupted. This lecture covers the three-way split, why
test must stay untouched, and the leakage patterns that silently inflate
scores.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Split data into train, validation, and test with a stated rationale
2. Explain why test must never influence training decisions
3. Detect the common leakage patterns (target, temporal, group)
4. Split by group when rows share a source
5. Diagnose suspiciously high scores as possible leakage

---

## 1. The Three-Way Split

Train fits the model. Validation tunes hyperparameters and selects between
candidates. Test measures final performance — once, at the end. The test
set is the honest referee: if it influences any decision, it stops being
honest. The roadmap's exit test ("compare on the same test set") depends on
this discipline.

```python
# 70/15/15 is a starting point, not a law
train, val, test = data[:0.7], data[0.7:0.85], data[0.85:]
```

## 2. Why Test Must Stay Untouched

Every time you look at test performance and change something, the test set
leaks into the model. The fix is discipline: test is evaluated once, at the
end, and any change after that means a fresh test set. Validation exists
precisely so tuning happens without touching test.

## 3. Leakage Patterns

- **Target leakage**: information from the future or the label leaks into
  the features (e.g., a feature computed from the answer).
- **Temporal leakage**: training on data from after the test period (time
  series split by time, not randomly).
- **Group leakage**: rows from the same source split across train and test,
  so the model "recognizes" the source instead of generalizing.

For Athar, group leakage is the critical one: passages from the same book
must not appear in both train and test, or the model memorizes the book.

## 4. Splitting by Group

```python
# Split by book, not by passage: no book appears in both train and test
books = sorted(set(p["book_id"] for p in passages))
train_books = set(books[: int(0.7 * len(books))])
train = [p for p in passages if p["book_id"] in train_books]
```

When rows share a source, split by the source. Random row splits leak the
group identity into the model.

## 5. Diagnosing Leakage

A suspiciously high score is the first symptom. Ask: does any feature use
the label or the future? Are train and test from the same time window? Do
rows from one source straddle the split? The diagnosis is a checklist, and
the fix is usually a re-split.

## Common Mistakes

- Tuning on test (the referee becomes a coach).
- Random splits on grouped data (group leakage).
- Features computed from the label (target leakage).
- Time-series data split randomly (temporal leakage).

## Key Takeaways

1. Train fits, validation tunes, test measures once.
2. Test must never influence decisions.
3. Split by group when rows share a source.
4. Suspiciously high scores are a leakage symptom.
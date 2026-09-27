# Embeddings 04: Quality Evaluation

## 🎯 Topic Overview

Embedding quality is measured, not assumed. The golden pairs test whether
similar texts embed close and dissimilar texts embed far. This lecture
covers the pair design, the similarity check, and the consistency test.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Build golden pairs of similar and dissimilar texts
2. Measure cosine similarity of related pairs
3. Test retrieval accuracy on the golden set
4. Test consistency (same text, same vector)
5. Use the metrics as a regression gate

---

## 1. The Golden Pairs

Golden pairs are hand-verified text pairs with an expected similarity.
Positive pairs: same concept, different wording. Negative pairs: different
concepts, similar wording. The pairs cover the corpus's edge cases —
Arabic, code, formulas. The roadmap's exit test: "the golden pairs are
built."

```python
pairs = [
    ("ما هو العدد الأولي؟", "What is a prime number?", 0.9),
    ("النسبة المئوية", "Percentage", 0.85),
    ("النسبة المئوية", "Physics", 0.3),
]
```

## 2. The Similarity Check

The model embeds both texts; the cosine similarity is compared to the
expected value. A positive pair scoring below its target signals a weak
model. The roadmap's exit test: "similarity is measured."

## 3. Retrieval Accuracy

Retrieval accuracy asks whether the correct documents appear in the top-k
for the golden queries. It is the end-to-end test — the embeddings plus
the search. The roadmap's exit test: "retrieval accuracy is measured."

## 4. Consistency

The same text must produce the same embedding every time. A nondeterministic
model breaks the cache and the retrieval. The consistency test embeds the
same text twice and compares. The roadmap's exit test: "consistency is
100%."

## 5. The Regression Gate

The metrics run on every embedding change — a model swap, a normalization
change. A change that drops retrieval accuracy is a regression. The
metrics gate the pipeline like any other eval.

## Common Mistakes

- No golden pairs (quality assumed).
- Positive pairs only (no negative control).
- No consistency test.
- Metrics never run on change.
- Similarity checked without a threshold.

## Key Takeaways

1. Golden pairs cover similar and dissimilar texts.
2. Cosine similarity is compared to the expected value.
3. Retrieval accuracy is the end-to-end test.
4. Consistency is 100% — same text, same vector.
5. The metrics gate every embedding change.
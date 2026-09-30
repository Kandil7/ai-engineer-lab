# Embeddings 04: Quality Evaluation

## Topic Overview

Embedding quality is measured, not assumed. A model that looks good on a leaderboard can rank
Arabic paraphrases poorly, or fail to separate a positive pair from a negative one, and the only
way to know is to test it on pairs and queries drawn from your own data. Embedding evaluation is
the gate that keeps the whole retrieval stack honest.

This lecture covers golden pairs (hand-verified similar and dissimilar texts with expected
similarities), the similarity check, retrieval accuracy as the end-to-end test, consistency (the
same text must always embed the same way), and using the metrics as a regression gate on every
embedding change.

The two-level structure matters: the pair test isolates the model's representation quality, while
the retrieval-accuracy test measures the model in the full search pipeline. A model can pass one
and fail the other, and the difference points to the layer at fault.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build golden pairs of similar and dissimilar texts.
2. Measure cosine similarity of related pairs against an expected value.
3. Measure retrieval accuracy on the golden query set.
4. Test consistency (same text, same vector).
5. Use the metrics as a regression gate.
6. Distinguish a model problem from a pipeline problem.

## Prerequisites

- Embeddings 01 (model selection) for the model being evaluated.
- AI Evaluation 01 (golden set) and 03 (retrieval evaluation) for the end-to-end protocol.

---

## 1. The Golden Pairs

### What they are

Golden pairs are hand-verified text pairs with an expected similarity. Positive pairs are the
same concept in different words; negative pairs are different concepts with superficially
similar wording:

```python
pairs = [
    ("ما هو العدد الأولي", "What is a prime number?", 0.9),   # positive
    ("النسبة المئوية", "Percentage", 0.85),                    # positive
    ("النسبة المئوية", "Physics", 0.3),                        # negative
]
```

### Why both signs

Positive pairs alone cannot detect a model that maps everything close together. Negative pairs
are the control: they catch a model whose similarities are uniformly high, which would make
retrieval return arbitrary results. Both signs are required for the test to mean anything.

### Coverage

The pairs cover the corpus's edge cases: Arabic, code, formulas, and the domain vocabulary. A
pair set that only covers easy English pairs does not test the model on the data that matters.

## 2. The Similarity Check

### The measurement

The model embeds both texts; the cosine similarity is compared to the expected value:

```python
def passes(pair, vectors, threshold):
    """A positive pair passes when its similarity meets the target."""
    a, b, target = pair
    return cosine(vectors[a], vectors[b]) >= target * threshold
```

### What a failure means

A positive pair scoring below its target signals a weak model or a normalization mismatch. A
negative pair scoring above its target signals a model that fails to separate concepts. Each
points to a different fix.

### The threshold

The threshold is set from the model's measured behavior, not invented. The pair targets encode
the expected similarity; the threshold encodes how much slack to allow.

## 3. Retrieval Accuracy

### The end-to-end test

Retrieval accuracy asks whether the correct documents appear in the top-k for the golden queries.
It is the end-to-end test: the embeddings plus the search, plus the normalization and the index:

```text
query -> embed -> search -> top-k documents -> compare to golden relevant set
```

### Why both levels

The pair test isolates the model's representation. The retrieval test measures the model in the
full pipeline. A model that passes the pairs but fails retrieval has a pipeline problem (an index
issue, a normalization mismatch, a metric choice), not a model problem. The two levels localize
the fault.

### The metrics

Report recall@k and MRR (AI Evaluation 03) on the golden set, exactly as for the retrieval arms.
The embedding evaluation is the same protocol applied to the embedding component.

## 4. Consistency

### The rule

The same text must produce the same embedding every time. A nondeterministic model breaks the
cache (Embeddings 03) and makes retrieval irreproducible:

```python
assert cosine(vectors[text], vectors[text]) == 1.0
```

### Why it matters

If the same text embeds differently across calls, the cache serves vectors that do not match a
fresh embed, and a re-run of ingestion produces a different index. Consistency is a precondition
for the cache and for reproducibility.

### Detecting inconsistency

Embed the same text twice (or across processes) and compare. A model that fails this is unusable
in the pipeline regardless of its quality, because the pipeline assumes determinism.

## 5. The Regression Gate

### On every embedding change

The metrics run on every embedding change: a model swap, a normalization change, an index
parameter change. A change that drops retrieval accuracy is a regression and fails the gate
(AI Evaluation 06).

### Why a gate

Embedding changes are easy to make and easy to get wrong silently. A model swap can improve one
query type and degrade another; without the gate, the degradation ships.

### The baseline and thresholds

The gate uses the same baseline-and-threshold discipline as everything else: capture the current
metrics, derive the floors, and enforce them.

## 6. Model Problem Versus Pipeline Problem

### The diagnosis

| Pair test | Retrieval test | Diagnosis |
| --- | --- | --- |
| Fail | Fail | Model problem: the representation is weak |
| Pass | Fail | Pipeline problem: normalization, index, or metric |
| Pass | Pass | Healthy |
| Fail | Pass | Rare: the pairs are unrepresentative; revisit them |

### The value of the split

The two-level structure turns "retrieval quality dropped" into a specific location: the model or
the pipeline. That is the same localization discipline used throughout the retrieval module
(Arabic NLP 03-05).

## Real-World Application

- Testing an Arabic embedding model on positive and negative pairs drawn from the Athar corpus
  before committing to it.
- Measuring retrieval accuracy on the golden set after a model swap to confirm the gain is real.
- Detecting a nondeterministic model before it corrupts the cache and the index.
- Gating a normalization change on the pair and retrieval metrics.

## Common Mistakes

1. **No golden pairs.** Quality is assumed.
2. **Positive pairs only.** No control for a model that maps everything close.
3. **No consistency test.** A nondeterministic model breaks the cache silently.
4. **Metrics never run on change.** Embedding regressions ship.
5. **Checking similarity without a threshold.** The result is uninterpretable.
6. **Not separating model from pipeline failures.** The fix is aimed at the wrong layer.

## Key Takeaways

1. Golden pairs cover similar and dissimilar texts with expected similarities; both signs are
   required.
2. The similarity check compares measured cosine to the expected value against a threshold.
3. Retrieval accuracy is the end-to-end test, using the same golden set and metrics as the
   retrieval arms.
4. Consistency is 100%: the same text must embed identically, or the cache and reproducibility
   break.
5. The metrics gate every embedding change, and the pair-versus-retrieval split localizes the
   fault to the model or the pipeline.

## Self-Check Questions

1. Why are negative pairs necessary, not just positive ones?
2. What does a pair-test pass with a retrieval-test fail indicate?
3. Why is consistency a precondition for caching?
4. How is the embedding evaluation's protocol related to the retrieval arms' protocol?
5. What should happen when an embedding change drops the retrieval accuracy?

## Further Reading / Connections

- Embeddings 01 (model selection) and 03 (caching) — the choice and the cache this evaluates.
- Arabic NLP 04 (Arabic embeddings) — the Arabic-specific evaluation.
- AI Evaluation 03 (retrieval evaluation) — recall@k and MRR in depth.
- AI Evaluation 06 (eval in CI) — the gate discipline.

# Applied ML 01: Vectors and Similarity

## Topic Overview

Every AI system that compares things rests on vectors. An embedding model turns a
passage into a list of numbers, a query becomes another list in the same space,
and "find the most relevant passage" becomes "find the nearest vector". Features
in classical ML are vectors too. Before you can build retrieval, classification,
or clustering, you need to be fluent in the small set of operations that define
distance and similarity.

This lecture covers the three metrics that matter in practice: the dot product,
cosine similarity, and Euclidean distance. It builds them from scratch, proves the
identity that lets a vector database normalize on write and serve queries with a
single multiply-add, and shows with runnable counter-examples that the metric you
choose changes the ranking of results. A system that ranks by raw dot product and
a system that ranks by cosine can return different documents for the same query.

The material is the geometric foundation under retrieval, classification, and
clustering. It is the first lecture in Applied ML because every later topic, from
leakage to evaluation, assumes you can reason about what "similar" means and why
the choice of metric is a design decision, not an implementation detail.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Represent data (documents, features, embeddings) as vectors and say what each
   dimension means.
2. Compute the dot product, cosine similarity, and Euclidean distance by hand.
3. State and prove the unit-vector identity: on normalized vectors, cosine equals
   the dot product.
4. Choose the right metric for a problem by asking whether magnitude is signal or
   noise.
5. Explain why normalization changes rankings, and demonstrate it with code.
6. Connect the metric choice to how a vector database stores and searches data.

## Prerequisites

- Basic Python: lists, `zip`, comprehensions, floating-point comparison.
- Comfort with the idea of a vector as an ordered list of numbers.
- No linear-algebra library is required; the exercises use the standard library.

---

## 1. Data as Vectors

### What a vector is here

A vector is an ordered list of numbers. The position in the list is the dimension
and the value is the magnitude along that dimension. Two things become vectors in
the same space: a document can become a sparse vector by counting terms, and an
embedding model turns a passage into a dense vector where every dimension is a
learned feature with no human-readable name.

```python
# Two feature vectors, for example term counts for two short documents.
a = [3.0, 4.0, 0.0]
b = [1.0, 2.0, 1.0]
```

### Why the geometric framing helps

If similar items land near each other in the space, then "similarity" becomes
"distance", and distance is something a machine can compute quickly over millions
of rows. The metric is the definition of near. Change the metric and you change
what the system considers relevant, which is why the metric is part of the
retrieval contract and belongs in a decision record.

### Dimensions are not interchangeable

In an embedding, dimension 7 has no independent meaning on its own; meaning lives
in the pattern across dimensions. In a feature vector, dimension 7 might be "word
count" and is interpretable. Both are vectors, but the interpretation of the
dimensions changes how you reason about the metric: dense embeddings usually
favor direction (cosine), while hand-built features often carry their signal in
magnitude (dot or Euclidean).

## 2. The Three Metrics

### Definitions and code

```python
import math


def dot(a: list[float], b: list[float]) -> float:
    return sum(x * y for x, y in zip(a, b))


def norm(v: list[float]) -> float:
    return math.sqrt(sum(x * x for x in v))


def cosine(a: list[float], b: list[float]) -> float:
    return dot(a, b) / (norm(a) * norm(b))


def euclidean(a: list[float], b: list[float]) -> float:
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
```

### Dot product: direction mixed with magnitude

The dot product multiplies matching dimensions and sums. It is cheap and it
rewards both alignment and length: a long vector pointing roughly the same way as
the query scores higher than a short one. It is a similarity (larger is better).

### Cosine similarity: pure direction

Cosine divides the dot product by the product of the two lengths, removing
magnitude and leaving the angle. Two vectors pointing the same way score 1
regardless of length; orthogonal vectors score 0; opposite vectors score -1. It
is the default for text and embeddings because it ignores the spurious effect of
text length.

### Euclidean distance: straight-line separation

Euclidean distance is the length of the difference vector. It is a distance, so
smaller is better. It is sensitive to magnitude, which is sometimes exactly what
you want (a value far from the target is a bad match) and sometimes not.

### Similarity versus distance

This is a frequent and silent bug. Cosine and dot are similarities: you sort
descending and take the top results. Euclidean is a distance: you sort ascending.
A ranker that sorts a Euclidean distance descending returns the worst matches
first and still looks like it works because it returns *some* results.

## 3. The Unit-Vector Identity

### The identity

When both vectors have length 1, `norm(a) = norm(b) = 1`, so the cosine
denominator is 1 and cosine equals the dot product exactly:

```python
def normalize(v: list[float]) -> list[float]:
    n = norm(v)
    return [x / n for x in v]


an, bn = normalize(a), normalize(b)
assert abs(cosine(a, b) - dot(an, bn)) < 1e-9  # the identity holds
```

### Why this matters for cost

If every stored vector is already normalized, a query only needs one dot product
per candidate instead of two norms, a multiply, and a divide. Across millions of
candidates that difference is the difference between a fast index and a slow one.
This is why vector stores normalize vectors on write and why cosine configuration
in Qdrant is effectively a dot-product scan under the hood.

### Cosine is magnitude-free

Scaling a vector does not change its cosine with another vector:

```python
assert abs(cosine(a, b) - cosine([x * 10 for x in a], b)) < 1e-9
```

That is the mathematical statement of "cosine ignores length", and it is why
cosine is robust to a long document that repeats a term many times.

### Euclidean is not magnitude-free

```python
assert euclidean(a, b) != euclidean([x * 10 for x in a], b)
```

Scaling one vector changes the Euclidean distance but not the cosine. The two
metrics answer genuinely different questions.

## 4. Choosing the Metric

### The question to ask

Does a bigger vector mean a better match, or a bigger item? If a longer document
or a higher count genuinely is more relevant, magnitude carries signal and you may
want dot product or a magnitude-aware score. If a longer vector just means there
was more text, magnitude is noise and you want cosine.

### Worked guidance

- **Sparse term counts.** Magnitude often means "mentions the term more", which
  can be legitimate relevance. But it also lets a single long document dominate,
  so many systems normalize or apply sublinear scaling (BM25 is essentially a
  magnitude-dampened term-frequency score).
- **Dense embeddings.** Magnitude mostly reflects text length. Use cosine.
- **Hand-built numeric features.** Euclidean distance is natural when dimensions
  are comparable quantities and "far" means "different".

### Record the decision

The metric is part of the retrieval or model contract. Put the choice and the
reason in the relevant ADR so a future change is deliberate rather than accidental.

## 5. Normalization Changes Rankings

The counter-example below is the heart of the lecture. Two candidate documents
have the identical direction as the query but different lengths:

```python
short = [1.0, 0.0, 0.0]
long_ = [5.0, 0.0, 0.0]
q = [1.0, 0.0, 0.0]

# Dot product: magnitude wins, so the long vector ranks first.
assert dot(long_, q) > dot(short, q)

# Cosine: the directions are identical, so the vectors tie.
assert cosine(long_, q) == cosine(short, q)
```

Under dot product the long vector outranks the short one. Under cosine they are
equal. The same data produces two different answer lists depending on one line of
configuration. This is why "the metric does not matter" is false, and it is what
the exercise's `--verify` mode asserts.

## 6. The Metric in Retrieval and This Repo

### In a retrieval pipeline

1. The embedder maps the query and each passage into one shared vector space.
2. The store ranks passages by the chosen metric.
3. The top-k passages become the context passed to the generator.

If step 2 uses raw dot product on unnormalized vectors, long passages dominate. If
it uses cosine, direction decides. The retrieval evaluation therefore treats the
metric as a variable: the exit test compares lexical, dense, hybrid, and
hybrid-plus-rerank on one fixed held-out set, and the dense arm's score depends on
this choice.

### Where it lives here

- **Athar.** Passages are embedded and searched by cosine; the by-book split in
  Applied ML 02 keeps that evaluation honest because passages from one book are not
  independent.
- **DevMate.** `src/devmate/index/embeddings.py` produces the vectors and
  `src/devmate/index/vector_store.py` stores normalized ones for a dot-product
  query.
- **Qdrant.** A collection is configured with a distance metric; changing it after
  ingestion means re-indexing everything.
- **Reranking.** A reranker rescores the top-k with a second model but depends on
  the first-stage metric to bring the right candidates into the top-k at all.

## Real-World Application

- Choosing the Qdrant distance metric for the Athar collection and documenting the
  reason in the retrieval ADR.
- Debugging "why did this clearly relevant passage not rank" by checking whether
  normalization was applied consistently to the query and the stored vectors.
- Explaining to an interviewer why cosine, not raw dot product, is the default for
  embeddings, using the ranking counter-example above.
- Deciding a magnitude-aware score for a metadata filter where recency or counts
  genuinely should influence ranking.

## Common Mistakes

1. **Calling dot product "cosine".** They agree only on unit vectors; on raw
   vectors they disagree and can reorder results.
2. **Mixing similarity and distance.** Cosine and dot are larger-is-better;
   Euclidean is smaller-is-better. A sort bug hides here.
3. **Normalizing some vectors but not others.** Mixed normalization makes scores
   incomparable across candidates and silently favors whichever side is smaller.
4. **Assuming metrics are interchangeable.** The exercise proves they are not.
5. **Letting document length drive dense rankings.** Use cosine when magnitude is
   noise.
6. **Changing the distance metric after ingestion.** The stored vectors and the
   index were built for the old metric; rebuild before trusting results.

## Key Takeaways

1. Similarity is geometry; the metric defines what "near" means and is a design
   decision.
2. Cosine measures direction; dot and Euclidean are magnitude-sensitive. Match the
   metric to whether length is signal or noise.
3. On unit vectors cosine equals the dot product, so stores normalize on write and
   queries pay a single dot product.
4. Normalization changes rankings; the choice belongs in the retrieval ADR.
5. The dense arm of any retrieval comparison is only meaningful once the metric is
   fixed.

## Self-Check Questions

1. When does `dot(a, b)` equal `cosine(a, b)`, and why does a vector store care?
2. A passage that repeats the query term ten times outranks a more relevant, shorter
   passage. Which metric produced this, and what is the fix?
3. For dense embeddings, is a longer vector more relevant? Justify your answer.
4. Why is normalizing only the query, and not the stored vectors, a bug?
5. Qdrant is configured with Euclidean distance for a collection and you want
   cosine. What must happen before queries are correct?

## Further Reading / Connections

- Applied ML 02 (train/validation/test and leakage) — why the by-book split makes
  these metrics trustworthy for Athar.
- Applied ML 03 (precision/recall/confusion) — how to score the classifier built on
  these vectors.
- `projects/04-ai-engineering/embeddings/01-model-selection` — where the vectors
  come from.
- `projects/03-databases/qdrant-rag/` — the store that applies the metric.
- `docs/reference/ml-fundamentals-map.md` — the linear-algebra and similarity
  sections this lecture operationalizes.

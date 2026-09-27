# Applied ML 01: Vectors and Similarity

## 🎯 Topic Overview

Every AI system rests on vectors: embeddings, features, and queries are all
vectors, and "how similar" is a geometric question. This lecture covers the
vector operations that matter — dot product, cosine similarity, and
distance — and when each is the right tool. It is the math behind retrieval,
classification, and clustering.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Represent data as vectors and explain what each dimension means
2. Compute dot product, cosine similarity, and Euclidean distance by hand
3. State when cosine equals dot product (unit-normalized vectors)
4. Choose the right similarity for the data (magnitude matters or not)
5. Explain why normalization changes rankings

---

## 1. Data as Vectors

A vector is an ordered list of numbers. A document becomes a vector by
counting term frequencies; an embedding model produces a dense vector where
each dimension is a learned feature. The key idea: **similarity is
geometry**. Two similar items are near each other in vector space; the
metric you choose defines "near."

```python
import math

# Two feature vectors (e.g., term counts for two documents)
a = [3.0, 4.0, 0.0]
b = [1.0, 2.0, 1.0]
```

## 2. The Three Metrics

```python
def dot(a, b):
    return sum(x * y for x, y in zip(a, b))


def norm(v):
    return math.sqrt(sum(x * x for x in v))


def cosine(a, b):
    return dot(a, b) / (norm(a) * norm(b))


def euclidean(a, b):
    return math.sqrt(sum((x - y) ** 2 for x, y in zip(a, b)))
```

- **Dot product** mixes direction and magnitude. Cheap; equals cosine only
  on unit vectors.
- **Cosine similarity** measures angle, ignoring magnitude. The default for
  text and embeddings.
- **Euclidean distance** measures straight-line distance. Magnitude-sensitive.

## 3. The Unit-Vector Identity

When both vectors are normalized (length 1), cosine equals dot product:

```python
an = [x / norm(a) for x in a]  # unit vector
bn = [x / norm(b) for x in b]
assert abs(cosine(a, b) - dot(an, bn)) < 1e-9
```

This is why vector stores normalize on write: the query then pays one cheap
dot product instead of two norms plus a division.

## 4. Choosing the Metric

If magnitude carries meaning (a document with more term occurrences is more
relevant), dot or Euclidean. If only direction matters (semantic similarity
of embeddings), cosine. The choice changes rankings — never assume one
metric is interchangeable with another.

## 5. Normalization Changes Rankings

Normalizing changes which items rank highest. A long document with many term
occurrences ranks high by dot product but not by cosine. Decide whether
magnitude is signal or noise before choosing the metric, and record the
decision.

## Common Mistakes

- Using dot product on unnormalized vectors and calling it cosine.
- Forgetting Euclidean is a distance (smaller wins) while cosine is a
  similarity (larger wins).
- Assuming metrics are interchangeable without checking rankings.
- Normalizing some vectors and not others.

## Key Takeaways

1. Similarity is geometry; the metric defines "near."
2. Cosine for direction, dot/Euclidean when magnitude matters.
3. Normalize on write so queries pay one dot product.
4. Metric choice changes rankings — decide deliberately.
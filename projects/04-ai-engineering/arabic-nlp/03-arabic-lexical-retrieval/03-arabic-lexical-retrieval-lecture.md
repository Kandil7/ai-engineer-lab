# Arabic NLP 03: Lexical Retrieval (BM25 and Inverted Index)

## 🎯 Topic Overview

Before embeddings, Arabic retrieval ran on lexical search: an inverted index
mapping terms to documents, scored by BM25. Lexical search is still the
correct first arm of hybrid retrieval — it matches exact terms, error codes,
and names that embeddings blur. This lecture builds the inverted index and
BM25 from scratch, applies the normalization and tokenization from topic 02,
and measures recall against a labeled set.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Build an inverted index: term → postings list
2. Explain BM25: IDF, term frequency saturation, length normalization
3. Apply Arabic normalization and tokenization inside the index
4. Score and rank passages for a query
5. Measure recall@k and diagnose misses

---

## 1. The Inverted Index

```python
from collections import defaultdict


def build_index(passages: list[str]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for doc_id, text in enumerate(passages):
        for term in set(tokenize_light_stem(normalize_arabic(text))):
            index[term].append(doc_id)
    return index
```

The index maps each term to the documents containing it. Using a set per
document means each term appears once per document (term frequency is
computed separately). The normalization and tokenization from topic 02 run
at index time — the index is only as good as its text pipeline.

## 2. BM25 Scoring

BM25 scores a document for a query as a sum over query terms:

- **IDF** down-weights terms appearing in many documents (common words).
- **Term frequency saturation** caps the reward for a term appearing many
  times in one document.
- **Length normalization** stops long documents winning by volume.

```python
import math


def bm25(query_terms, doc_terms, doc_len, avg_len, N, df, k1=1.5, b=0.75):
    score = 0.0
    for term in query_terms:
        tf = doc_terms.count(term)
        if tf == 0:
            continue
        idf = math.log(1 + (N - df[term] + 0.5) / (df[term] + 0.5))
        tf_norm = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_len / avg_len))
        score += idf * tf_norm
    return score
```

The constants k1 and b are the standard defaults; k1 controls saturation,
b controls length normalization. On code or mixed corpora, b often needs
tuning — measured, not assumed.

## 3. Arabic in the Index

The index terms are the normalized, stemmed tokens from topic 02. A query
for "كتب" matches "الكتاب" because both normalize and stem to the same
token. This is where the earlier topics pay off: without normalization, the
inverted index is a fragile exact-match table.

## 4. Measuring and Diagnosing

Run the labeled query set, compute recall@k, and for each miss ask which
stage failed: normalization (the query and passage don't share a normalized
form), tokenization (the stemmer split differently), or scoring (the right
passage ranked below k). The exercise implements this diagnosis loop.

## Common Mistakes

- Building the index on raw text (no normalization, no stemming).
- Forgetting length normalization (long passages dominate).
- Tuning k1/b without measuring recall.
- Using the display text instead of the searchable text.

## Key Takeaways

1. The inverted index is the lexical arm's foundation.
2. BM25 = IDF + saturation + length normalization.
3. The index inherits the text pipeline's quality.
4. Diagnose misses by stage: normalization, tokenization, scoring.
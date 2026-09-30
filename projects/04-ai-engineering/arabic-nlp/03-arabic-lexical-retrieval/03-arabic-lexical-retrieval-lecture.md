# Arabic NLP 03: Lexical Retrieval (BM25 and Inverted Index)

## Topic Overview

Before embeddings, Arabic retrieval ran on lexical search: an inverted index mapping terms
to documents, scored by BM25. Lexical search is still the correct first arm of hybrid
retrieval, because it matches exact terms, error codes, names, and rare vocabulary that
embeddings blur into each other. On Arabic, this arm is especially important: exact-term and
name queries are common, and a well-normalized lexical index handles them cheaply and
precisely.

This lecture builds the inverted index and BM25 from scratch, applies the normalization and
tokenization from Topic 02 inside the index, and measures recall against a labeled set. The
key insight is that the index is only as good as the text pipeline that feeds it: a
mismatched normalization between indexing and query time is the single most common cause of
"the passage is clearly there but does not rank".

The lecture also establishes the diagnosis discipline the later topics reuse: when a query
misses, find which stage failed (normalization, tokenization, or scoring) rather than
tweaking the whole system.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Build an inverted index mapping terms to a postings list of document ids.
2. Explain BM25: IDF, term-frequency saturation, and length normalization.
3. Apply Arabic normalization and light stemming inside the index.
4. Score and rank passages for a query.
5. Measure recall@k and diagnose a miss by stage.
6. Tune the BM25 constants against measured recall, not intuition.

## Prerequisites

- Arabic NLP 02 (normalization and tokenization), applied here at index time.
- AI Evaluation 03 (recall@k) for the metric the index is scored by.

---

## 1. The Inverted Index

### The structure

An inverted index maps each term to the documents that contain it. Building it means
tokenizing every passage and recording, per term, which documents it appeared in:

```python
from collections import defaultdict


def build_index(passages: list[str]) -> dict[str, list[int]]:
    index: dict[str, list[int]] = defaultdict(list)
    for doc_id, text in enumerate(passages):
        for term in set(tokenize(normalize_arabic(text))):
            index[term].append(doc_id)
    return index
```

### The set per document

Using `set` per document means each term appears once in that document's postings entry.
Term frequency is computed separately at scoring time; the index only records membership,
which keeps it small.

### The index inherits the pipeline

The terms stored are the normalized, stemmed tokens from Topic 02. A query for "كتاب"
matches "الكتاب" because both normalize and stem to the same token. Without normalization
and stemming, the inverted index is a fragile exact-match table and Arabic recall collapses.

## 2. BM25 Scoring

### The three ideas

BM25 scores a document for a query as a sum over the query terms, and each term's
contribution combines three ideas:

- **IDF (inverse document frequency):** a term appearing in many documents is less
  informative, so it contributes less.
- **Term-frequency saturation:** the reward for a term appearing many times in one document
  grows sublinearly, so a document cannot win by repeating a word.
- **Length normalization:** long documents are penalized so they do not win by sheer volume.

### The formula

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

### The constants

`k1` controls saturation (how quickly extra occurrences stop helping) and `b` controls length
normalization (`b = 0` disables it, `b = 1` fully applies it). The defaults work well for
prose; code, short passages, and mixed corpora often need a measured adjustment.

## 3. Arabic in the Index

### Normalization at both ends

The query and the passages must go through the same normalization and tokenization. If the
index is built on normalized text but the query is not, or vice versa, they will not share
tokens. This is the most common Arabic lexical miss.

### Light stemming

Light stemming strips a small set of prefixes (ال, وال, بال, فال, لل) without a full
morphological analyzer. It raises recall on inflected queries without the complexity of root
extraction:

```python
PREFIXES = ("ال", "وال", "بال", "فال", "لل")


def light_stem(word: str) -> str:
    for p in PREFIXES:
        if word.startswith(p) and len(word) > len(p) + 1:
            return word[len(p) :]
    return word
```

### The tradeoff

More aggressive stemming raises recall but can raise false matches. Light stemming is a
deliberate middle ground, and it is a decision to measure on the golden set, not to assume.

## 4. Measuring and Diagnosing

### Recall@k as the metric

The labeled set pairs queries with their relevant passages. Recall@k asks whether the
relevant passages appear in the top k. The exercise computes it against the normalized,
stemmed index:

```python
def recall_at_k(query, passages, relevant, k):
    ranked = bm25(query, passages, *build_index(passages))
    top = {doc_id for doc_id, _ in ranked[:k]}
    return len(top & relevant) / max(1, len(relevant))
```

### Diagnosing a miss by stage

When a query misses, ask which stage failed:

- **Normalization:** the query and the passage do not share a normalized form (a diacritic
  or hamza difference survived).
- **Tokenization:** the tokenizer split a word differently in the query than in the index.
- **Scoring:** the right passage ranked below k (IDF or length normalization pushed it
  down).

Each stage has a different fix. Tweaking the score when the failure was normalization wastes
effort and can break working queries.

## 5. Tuning BM25

### Measure, do not guess

Tune `k1` and `b` by trying combinations and measuring recall@k (and precision) on the
golden set. A tiny grid search over `k1` in {1.2, 1.5, 2.0} and `b` in {0.3, 0.5, 0.75} is
usually enough to see whether tuning matters for your corpus.

### When tuning matters

Length normalization matters a lot when passages vary widely in length (short verse
chunks versus long commentary). On uniformly sized chunks it changes little. The corpus
decides; measure it.

### Record the choice

The final constants, the stemming choice, and the normalization pipeline belong in the
retrieval ADR, so a later change is deliberate.

## Real-World Application

- Building the Athar lexical arm over normalized, lightly stemmed passages so a query for a
  bare form matches its definite form.
- Diagnosing a hafiz's verse query that missed because the query carried a diacritic the
  index did not.
- Tuning `b` down when passages are short and of similar length, so length normalization
  stops penalizing the concise verses that are the best answers.
- Recording the pipeline and constants in the retrieval ADR for the Athar system.

## Common Mistakes

1. **Building the index on raw text.** No normalization, no stemming, poor recall.
2. **Different pipelines for query and index.** The most common lease-lexical miss.
3. **Forgetting length normalization.** Long passages dominate on volume, not relevance.
4. **Tuning `k1`/`b` without measuring.** The constants drift on intuition.
5. **Using display text instead of searchable text.** Diacritics split the index.
6. **Over-stemming.** Recall rises, precision falls, and false matches appear.

## Key Takeaways

1. The inverted index maps terms to the documents containing them, with one membership entry
   per document.
2. BM25 combines IDF, term-frequency saturation, and length normalization.
3. The index inherits the quality of the normalization and tokenization pipeline; query and
   index must share it.
4. Diagnose a miss by stage (normalization, tokenization, scoring) before changing anything.
5. Tune the constants and record the pipeline in the retrieval ADR.

## Self-Check Questions

1. Why does the index store one entry per term per document rather than a count?
2. What does IDF down-weight, and why does that help on Arabic?
3. Give the three possible causes of an Arabic lexical miss and one fix for each.
4. When does length normalization matter most, and how do you decide `b`?
5. Why must the query use the same normalization as the index?

## Further Reading / Connections

- Arabic NLP 02 (normalization and tokenization) — the pipeline this index consumes.
- Arabic NLP 04 (embeddings) and 05 (hybrid search) — the dense arm and the fusion.
- AI Evaluation 03 (retrieval evaluation) — recall@k, precision@k, and MRR in depth.
- `projects/03-databases/qdrant-rag/` — a vector store that can also hold lexical metadata.

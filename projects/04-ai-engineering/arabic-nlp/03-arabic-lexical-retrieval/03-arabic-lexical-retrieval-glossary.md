# Arabic NLP 03: Lexical Retrieval — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Inverted index | Term → postings list mapping | كتب → [0, 3, 7] |
| Postings list | Documents containing a term | doc ids |
| BM25 | Lexical scoring: IDF + saturation + length norm | ranker |
| IDF | Inverse document frequency, down-weights common terms | rare terms win |
| Term frequency | Occurrences of a term in a document | saturation input |
| Length normalization | Correcting for document length (b) | long-doc penalty |
| Recall@k | Fraction of relevant in top-k | tokenizer comparison |

---

## Alphabetical Glossary

### BM25

**Definition:** The standard lexical ranking function: per query term, IDF
times a saturated, length-normalized term frequency, summed. The default
lexical arm of hybrid search.

**Example:**
```python
score = sum(idf[t] * tf_norm(t, doc) for t in query)
```

**Related concepts:** IDF, Term frequency, Length normalization

---

### IDF

**Definition:** Inverse Document Frequency: a term appearing in many
documents carries less weight. The "rare terms win" principle.

**Example:**
```python
idf = math.log(1 + (N - df + 0.5) / (df + 0.5))
```

**Related concepts:** BM25

---

### Inverted index

**Definition:** A mapping from each term to the documents containing it.
The data structure that makes lexical search fast.

**Example:**
```python
# "كتب" -> [0, 3, 7]  (documents 0, 3, 7 contain the term)
```

**Related concepts:** Postings list, Tokenization

---

### Length normalization

**Definition:** BM25's correction (via b) so long documents don't win by
volume. Tuned per corpus; often raised on code.

**Example:**
```python
tf_norm = tf * (k1 + 1) / (tf + k1 * (1 - b + b * doc_len / avg_len))
```

**Related concepts:** BM25

---

### Postings list

**Definition:** The list of documents (and optionally positions) containing
a term. The value side of the inverted index.

**Example:**
```python
index["كتب"]  # [0, 3, 7]
```

**Related concepts:** Inverted index

---

### Recall@k

**Definition:** Fraction of relevant passages retrieved in the top-k. The
measurement that validates the whole lexical stack.

**Example:**
```python
# 4 of 5 relevant in top-10 -> 0.80
```

**Related concepts:** BM25, Evaluation

---

### Term frequency

**Definition:** How often a term appears in a document. BM25 saturates it so
repetition stops rewarding beyond a point.

**Example:**
```python
doc_terms.count("كتب")  # 3
```

**Related concepts:** BM25

---

## Related Concepts

- **Normalization/tokenization**: the text pipeline feeding the index (topic 02)
- **Hybrid search**: lexical + dense arms fused (topic 05)
- **RRF**: rank fusion across arms (topic 05)

## Key Takeaways

1. The index is the lexical arm's foundation.
2. BM25 balances rarity, saturation, and length.
3. Measure recall; diagnose misses by stage.
# Arabic NLP 02: Normalization and Tokenization — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Normalization | Canonicalizing text for matching (diacritics, hamza, tatweel) | أ → ا |
| Hamza | Glottal stop, written on carriers (أ إ آ ؤ ئ) | unification target |
| Tatweel | Kashida (ـ), a length-extension mark, removed for search | text.replace |
| Tokenization | Splitting text into indexable units | whitespace vs stemming |
| Light stemming | Stripping common affixes (ال، و، ب) | pragmatic middle |
| Morphological analysis | Root-and-pattern decomposition | highest recall, costly |
| Recall@k | Fraction of relevant passages retrieved in top-k | tokenizer comparison |

---

## Alphabetical Glossary

### Hamza

**Definition:** The glottal stop, written alone (ء) or on carriers (أ إ آ ؤ
ئ). Unifying carrier forms to bare alif is the standard recall trade.

**Example:**
```python
text.replace("أ", "ا").replace("إ", "ا").replace("آ", "ا")
```

**Related concepts:** Normalization

---

### Light stemming

**Definition:** Stripping common Arabic affixes (ال، و، ب، ك) without full
root analysis. The pragmatic middle between whitespace and analyzers.

**Example:**
```python
# "الكتاب" -> "كتاب" — matches "كتاب" and "مكتبة" partially
```

**Related concepts:** Tokenization, Morphological analysis

---

### Morphological analysis

**Definition:** Full root-and-pattern decomposition of Arabic words. Highest
recall, highest cost, language-specific tooling required.

**Example:**
```python
# كتب -> root ك ت ب + pattern; matches every derived form
```

**Related concepts:** Light stemming, Tokenization

---

### Normalization

**Definition:** The ordered pipeline canonicalizing text for matching:
decompose, strip diacritics, recompose, unify hamza, remove tatweel.
Applied to the search text only.

**Example:**
```python
normalize_arabic("أَلْكِتَابُ")  # "الكتاب"
```

**Related concepts:** Hamza, Tatweel

---

### Recall@k

**Definition:** Fraction of relevant passages found in the top-k results.
The metric that decides tokenization and normalization choices.

**Example:**
```python
# whitespace 0.62 vs light-stem 0.81: the stemmer earns its complexity
```

**Related concepts:** Tokenization, Evaluation

---

### Tatweel

**Definition:** The kashida (ـ), a mark extending letter shapes for
calligraphy. Removed in normalization; it carries no meaning.

**Example:**
```python
text.replace("\u0640", "")
```

**Related concepts:** Normalization

---

### Tokenization

**Definition:** Splitting text into indexable units. Arabic's morphology
makes whitespace splitting the weakest option.

**Example:**
```python
# "الكتاب" as one token vs "ال" + "كتاب" vs root "كتب"
```

**Related concepts:** Light stemming, Morphological analysis

---

## Related Concepts

- **Two-text discipline**: normalization touches search text only (topic 01)
- **BM25**: the lexical ranker tokenization feeds (topic 03)
- **Embeddings**: the dense arm with its own tokenization (topic 04)

## Key Takeaways

1. Normalize in a documented, ordered pipeline.
2. Hamza unification is a per-corpus trade.
3. Measure tokenizers with recall@k.
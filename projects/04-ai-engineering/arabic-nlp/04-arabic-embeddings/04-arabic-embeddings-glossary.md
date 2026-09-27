# Arabic NLP 04: Arabic Embeddings — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Embedding | Dense vector where distance means similarity | 768-dim vector |
| Multilingual model | Trained on many languages, often English-skewed | Arabic tokenization risk |
| Arabic-specialized | Model trained/tuned for Arabic semantics | better recall |
| Cosine similarity | Angle-based similarity, magnitude-free | ranking metric |
| Dense arm | Embedding-based retrieval | meaning matching |
| Golden set | Labeled query-to-passage pairs for evaluation | recall@k basis |
| Normalized embedding | Embedding the searchable text, not raw | consistency |

---

## Alphabetical Glossary

### Arabic-specialized

**Definition:** An embedding model trained or tuned specifically for Arabic
semantics, or a multilingual model with verified strong Arabic benchmarks.
The candidate set for the dense arm.

**Example:**
```python
# candidates: Arabic Sentence Transformers, verified multilingual models
```

**Related concepts:** Multilingual model, Golden set

---

### Cosine similarity

**Definition:** The angle-based similarity between vectors, ignoring
magnitude. The standard ranking metric for dense retrieval.

**Example:**
```python
cos = np.dot(a, b) / (np.linalg.norm(a) * np.linalg.norm(b))
```

**Related concepts:** Dense arm

---

### Dense arm

**Definition:** The embedding-based retrieval path: passage and query
embeddings, cosine ranking. Matches meaning where lexical search fails.

**Example:**
```python
# query "كيف أتعلم البرمجة" matches a passage with no shared tokens
```

**Related concepts:** Lexical arm, Hybrid search

---

### Embedding

**Definition:** A dense vector produced by a model, placing text in a space
where semantic nearness is geometric distance.

**Example:**
```python
model.encode("السلام عليكم")  # -> vector
```

**Related concepts:** Dense arm, Cosine similarity

---

### Golden set

**Definition:** The labeled query-to-passage pairs used to evaluate both
retrieval arms with the same recall@k. The arbiter of model choice.

**Example:**
```python
# same set measured BM25 in topic 03; now measures the dense arm
```

**Related concepts:** Recall@k, Arabic-specialized

---

### Multilingual model

**Definition:** A model trained across languages, typically English-heavy.
Convenient, but Arabic tokenization and semantics are often weaker.

**Example:**
```python
# works, but measure before trusting on Arabic
```

**Related concepts:** Arabic-specialized

---

### Normalized embedding

**Definition:** Embedding the normalized searchable text rather than the raw
display text, matching the lexical index's normalization. Consistency beats
perfection.

**Example:**
```python
model.encode(normalize_arabic(passage))
```

**Related concepts:** Normalization, Two-text discipline

---

## Related Concepts

- **Lexical arm**: the exact-match counterpart (topic 03)
- **Hybrid search**: fusing both arms (topic 05)
- **Vector store**: where embeddings live (Qdrant)

## Key Takeaways

1. Arabic embedding quality is measured, never assumed.
2. Same golden set, both arms, comparable recall@k.
3. Embed the normalized text.
4. Dense and lexical fail in opposite directions.
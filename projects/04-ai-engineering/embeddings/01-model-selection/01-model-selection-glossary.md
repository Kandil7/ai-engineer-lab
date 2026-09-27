# Embeddings 01: Model Selection — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Embedding model | Maps text to a vector | all-MiniLM-L6-v2 |
| Dimensions | The vector's length | 384 to 3072 |
| Language coverage | The model handles the corpus language | multilingual |
| Deployment context | Prototype vs production | local vs API |
| Consistency | One model across the pipeline | re-embed on change |
| Golden-set re-eval | The choice measured, not guessed | recall@k |
| Monolingual trap | An English-only model on Arabic | poor embeddings |

---

## Alphabetical Glossary

### Consistency

**Definition:** The same model embeds the corpus and the queries. A model
change requires re-embedding the whole corpus — old and new vectors are
incomparable.

**Example:**
```python
# embed corpus and queries with the same model
```

**Related concepts:** Embedding model

---

### Deployment context

**Definition:** Prototype vs production. Prototyping uses a free local
model; production balances cost and quality.

**Example:**
```python
# prototype: all-MiniLM; production: nomic or API
```

**Related concepts:** Embedding model

---

### Dimensions

**Definition:** The vector's length. Higher captures more but costs more to
store and search.

**Example:**
```python
# 384 (MiniLM) to 3072 (text-embedding-3-large)
```

**Related concepts:** Embedding model

---

### Embedding model

**Definition:** Maps text to a vector. The choice decides retrieval
quality.

**Example:**
```python
# model.encode("النص") -> [0.1, 0.2, ...]
```

**Related concepts:** Dimensions, Language coverage

---

### Golden-set re-eval

**Definition:** Re-evaluating the model choice by measuring recall@k on the
golden set. Evidence-based, not guessed.

**Example:**
```python
# compare models on the golden set, keep the best recall@k
```

**Related concepts:** Embedding model

---

### Language coverage

**Definition:** The model handles the corpus language. A monolingual
English model embeds Arabic poorly.

**Example:**
```python
# multilingual model for an Arabic corpus
```

**Related concepts:** Monolingual trap

---

### Monolingual trap

**Definition:** Using an English-only model on an Arabic corpus. Produces
poor embeddings and poor retrieval.

**Example:**
```python
# an English model on Arabic text -> weak similarity
```

**Related concepts:** Language coverage

---

## Related Concepts

- **Vector search**: the model's vectors are searched (qdrant-rag 02)
- **Arabic NLP**: Arabic-specific embedding choices (arabic-nlp 04)
- **Batch processing**: the model runs in batches (topic 02)

## Key Takeaways

1. The choice is a tradeoff across axes.
2. The model must cover the corpus language.
3. The deployment context decides the tier.
4. One model across the whole pipeline.
5. Re-evaluate when the corpus changes.
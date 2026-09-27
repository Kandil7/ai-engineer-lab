# RAG System 01: Chunking by Source Structure — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Chunk | One embeddable, retrievable unit | a paragraph |
| Structure-aware | Chunking by source boundaries | page, section, paragraph |
| Two-text discipline | Original for citation, searchable for matching | per-chunk |
| Provenance | book_id, page, source_version on every chunk | traceability |
| chunk_id | Unique chunk identifier | b1:p7:2 |
| AST-aware | Chunking code by syntax boundaries | functions, classes |
| Recall@k | Fraction of relevant chunks retrieved in top-k | chunker comparison |

---

## Alphabetical Glossary

### AST-aware

**Definition:** Chunking code by syntax-tree boundaries (functions, classes)
with line ranges. Complete citable units for code corpora.

**Example:**
```python
# one function per chunk + file:lines metadata
```

**Related concepts:** Structure-aware, Chunk

---

### Chunk

**Definition:** One embeddable, retrievable unit of a document. Sized to
preserve a complete thought.

**Example:**
```python
# one paragraph, capped by a token limit
```

**Related concepts:** Structure-aware, Provenance

---

### chunk_id

**Definition:** The unique identifier of a chunk, encoding its provenance:
book_id, page, and index.

**Example:**
```python
# "b1:p7:2" = book b1, page 7, chunk 2
```

**Related concepts:** Provenance

---

### Provenance

**Definition:** The recorded origin of a chunk: book_id, page,
source_version. A chunk without provenance cannot be cited honestly.

**Example:**
```python
{"book_id": "b1", "page": 7, "source_version": "v1"}
```

**Related concepts:** chunk_id, Two-text discipline

---

### Recall@k

**Definition:** Fraction of relevant chunks retrieved in the top-k. The
measurement that decides chunking strategy.

**Example:**
```python
# structure-aware 0.88 vs fixed-size 0.81
```

**Related concepts:** Chunk, Structure-aware

---

### Structure-aware

**Definition:** Chunking by the source's natural boundaries — page, section,
paragraph — instead of blind fixed sizes.

**Example:**
```python
# split on "\n\n" paragraph boundaries, cap by tokens
```

**Related concepts:** Chunk, AST-aware

---

### Two-text discipline

**Definition:** Every chunk carries original (verbatim, for citation) and
searchable (normalized, for matching). Normalization never alters the quote.

**Example:**
```python
# original: "قالَ اللهُ"  searchable: "قال الله"
```

**Related concepts:** Provenance, Chunk

---

## Related Concepts

- **Retrieval**: chunks are what retrieval finds (topic 02)
- **Context construction**: chunks become the answer's evidence (topic 04)
- **Citations**: chunks carry the source for citation (topic 05)

## Key Takeaways

1. Chunk by the source's boundaries.
2. Two texts per chunk.
3. Provenance on every chunk.
4. Measure chunking by recall.
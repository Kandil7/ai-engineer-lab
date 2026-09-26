# Vector Stores 07: Chunking and Retrieval Quality — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Chunk | One embeddable unit of a document | 500-token window |
| Overlap | Shared prefix between consecutive chunks | 50 tokens |
| Sentence-boundary chunking | Splits on linguistic units, variable sizes | prose corpora |
| AST-aware chunking | Splits code on syntax boundaries with line ranges | whole functions |
| Retrieval quality | recall@k/MRR of a chunking strategy on fixed queries | ADR results table |
| Signal dilution | Oversized chunks averaging meaning into mush | 4000-token chunks |
| Boundary loss | Answers spanning a cut becoming unretrievable | zero-overlap splits |

---

## Alphabetical Glossary

### AST-aware chunking

**Definition:** Code chunking on syntax-tree boundaries (functions, classes)
with recorded line ranges and syntax-error fallback. Complete citable units.

**Example:**
```python
# one function per chunk + file:lines metadata for citations
```

**Related concepts:** Chunk, Retrieval quality

---

### Boundary loss

**Definition:** Retrieval failure where the answer spans a chunk cut and
neither side ranks. Prevented by overlap or boundary-aware splitting.

**Example:**
```python
# zero overlap: the answer's two halves each score too low to surface
```

**Related concepts:** Overlap, Chunk

---

### Chunk

**Definition:** The unit of embedding and retrieval. Sized to preserve one
idea; the highest-leverage retrieval parameter.

**Example:**
```python
# 500 tokens: enough context, tight enough signal
```

**Related concepts:** Overlap, Retrieval quality

---

### Overlap

**Definition:** Tokens shared between consecutive chunks to preserve boundary
context. Costs roughly overlap/size extra index.

**Example:**
```python
# 50/500: 10% more index for boundary safety
```

**Related concepts:** Chunk, Boundary loss

---

### Retrieval quality

**Definition:** Measured recall@k/MRR of a strategy on fixed queries. The
only valid basis for chunking decisions.

**Example:**
```python
# AST-aware recall@10 0.91 vs fixed 0.84 -> ADR cites this row
```

**Related concepts:** Recall@k, Chunk

---

### Sentence-boundary chunking

**Definition:** Splitting on sentence ends instead of fixed counts. Variable
sizes, preserved linguistic units; usually beats fixed-size on prose.

**Example:**
```python
# NLTK/sentence-splitter boundaries, capped with max-token merge
```

**Related concepts:** Chunk, AST-aware chunking

---

### Signal dilution

**Definition:** Quality loss when chunks are so large the query-relevant part
is averaged out. The failure mode of "fit more context" thinking.

**Example:**
```python
# whole-file chunks: every query retrieves, nothing ranks
```

**Related concepts:** Chunk, Retrieval quality

---

## Related Concepts

- **Context precision**: whether retrieved chunks are relevant (RAG evals)
- **Reranking**: rescores fused candidates, can't fix unretrieved ones
- **Golden set**: the fixed queries strategies are compared on

## Key Takeaways

1. Chunks carry ideas; size them deliberately.
2. Overlap and boundaries are measured insurance.
3. Numbers decide; intuition proposes.

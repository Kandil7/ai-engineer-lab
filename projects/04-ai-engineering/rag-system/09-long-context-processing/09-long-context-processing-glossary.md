# RAG System 09: Long Context Processing — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Context budget | The window minus prompt and output | finite |
| Truncation | Dropping the lowest-ranked material | fast, lossy |
| Summarization | Compressing long material | gist, not detail |
| Chunking | Splitting before retrieval | retrieval-side |
| Compaction | Summarizing older conversation turns | long conversations |
| Budget utilization | How much of the budget is used | measured |
| Ranked window | The ordered, budget-capped context | topic 04 |

---

## Alphabetical Glossary

### Budget utilization

**Definition:** How much of the context budget is used. Measured to ensure
the budget is respected.

**Example:**
```python
# 80% of the budget used -> near the limit
```

**Related concepts:** Context budget

---

### Chunking

**Definition:** Splitting long documents before retrieval so each chunk
fits the budget. The retrieval-side strategy.

**Example:**
```python
# split a 10K-token document into 500-token chunks
```

**Related concepts:** Truncation

---

### Compaction

**Definition:** Summarizing older conversation turns and keeping recent
ones. The strategy for long conversations.

**Example:**
```python
# summarize turns 1-20; keep turns 21-25
```

**Related concepts:** Summarization

---

### Context budget

**Definition:** The model's context window minus the prompt and output
space. Every piece of context is measured against it.

**Example:**
```python
# 8K window - 2K prompt - 1K output = 5K budget
```

**Related concepts:** Truncation

---

### Summarization

**Definition:** Compressing long material into a shorter form. Preserves
the gist but loses detail. Costs a model call.

**Example:**
```python
# summarize a 3K-token passage into 300 tokens
```

**Related concepts:** Compaction

---

### Truncation

**Definition:** Dropping the lowest-ranked material to fit the budget. Fast
and lossy.

**Example:**
```python
# drop the lowest-scored chunks until the budget fits
```

**Related concepts:** Context budget

---

## Related Concepts

- **Context construction**: the budget-aware builder (topic 04)
- **Caching**: cached contexts avoid recomputation (topic 06)
- **Chunking by structure**: the chunking strategy (topic 01)

## Key Takeaways

1. The budget is the window minus prompt and output.
2. Truncation drops the lowest-ranked material.
3. Summarization compresses but loses detail.
4. Chunking is the retrieval-side strategy.
5. Long conversations are compacted.
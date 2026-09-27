# RAG System 04: Context Construction — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Context | The material the model reads to answer | reranked chunks |
| Evidence id | Chunk identifier cited in the answer | b1:p7:2 |
| Token budget | The context size ceiling | stage budget |
| Grounding | Answering only from the context | no memory answers |
| Thin context | Too little material to answer | abstain signal |
| Ranked window | Context ordered by relevance, budget-capped | top chunks first |
| Original text | Verbatim quote in the context | citation source |

---

## Alphabetical Glossary

### Context

**Definition:** The assembled material the model reads to answer. Its
quality decides the answer's quality more than the model does.

**Example:**
```python
context = [{"evidence_id": "b1:p7:2", "text": "..."}]
```

**Related concepts:** Evidence id, Token budget

---

### Evidence id

**Definition:** The chunk identifier the answer cites. Every claim traces to
an evidence id in the context.

**Example:**
```python
# answer cites "b1:p7:2" -> the exact chunk
```

**Related concepts:** Context, Grounding

---

### Grounding

**Definition:** Answering only from the context, never from memory. The
roadmap's exit test: summarize retrieved text, not recall.

**Example:**
```python
# the prompt forbids answering outside the context
```

**Related concepts:** Context, Thin context

---

### Original text

**Definition:** The verbatim quote carried in the context for display and
citation. The normalized form was for retrieval, not for the reader.

**Example:**
```python
# context holds "قالَ اللهُ" verbatim, not the normalized form
```

**Related concepts:** Context, Evidence id

---

### Ranked window

**Definition:** The context ordered by rerank score and capped by the token
budget. Drop the lowest-ranked chunks when over budget, never the highest.

**Example:**
```python
# top-5 chunks by rerank score, within the budget
```

**Related concepts:** Context, Token budget

---

### Thin context

**Definition:** Too little material to answer — few chunks, low scores, no
chunk touching the question's key terms. The abstain signal.

**Example:**
```python
# no chunk mentions the question's topic -> abstain
```

**Related concepts:** Grounding, Abstention

---

### Token budget

**Definition:** The context size ceiling set by the stage budgets. Exceeding
it truncates and can drop the answer.

**Example:**
```python
# context must fit the generation budget
```

**Related concepts:** Context, Ranked window

---

## Related Concepts

- **Abstention**: the correct behavior on thin context (topic 05)
- **Citations**: evidence ids become the answer's citations (topic 05)
- **Reranking**: produces the order the context follows (topic 03)

## Key Takeaways

1. The context is the model's only allowed source.
2. Order by relevance, respect the budget.
3. Original text in the context.
4. Every claim traces to an evidence id.
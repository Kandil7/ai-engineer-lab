# RAG System 04: Context Construction

## 🎯 Topic Overview

The context is what the model actually reads. It is assembled from the
reranked chunks, and its quality decides the answer's quality more than the
model does. This lecture covers what belongs in the context, how to order
it, the token budget, and the discipline that keeps the model grounded in
the evidence.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Assemble a context from reranked chunks with provenance
2. Order chunks by relevance and keep the budget
3. Keep the original text in the context, not the normalized form
4. Make the model cite evidence ids from the context
5. Detect when the context is too thin to answer

---

## 1. What Belongs in the Context

The context holds the reranked chunks — their original text, their
provenance, and their evidence ids. The model answers from this material,
not from memory. The roadmap's exit test — "summarize retrieved text, not
answer from memory" — is enforced by the context being the only source the
model is allowed to use.

```python
context = [
    {"evidence_id": "b1:p7:2", "text": "قال الله تعالى...", "book_id": "b1", "page": 7},
    {"evidence_id": "b1:p8:0", "text": "...", "book_id": "b1", "page": 8},
]
```

## 2. Ordering and Budget

Chunks are ordered by rerank score, most relevant first. The total context
must fit the token budget — the roadmap's stage budgets set the ceiling.
When the budget is exceeded, drop the lowest-ranked chunks, never the
highest. The context is a ranked window, not a dump.

## 3. Original Text, Not Normalized

The context carries the original text — the verbatim quote — so the answer
can cite it exactly. The normalized searchable form was for retrieval; the
context is for the reader and the citation. Mixing them up breaks the quote.

## 4. Grounding and Evidence Ids

The model is instructed to answer only from the context and to cite
evidence ids. The prompt makes the contract explicit: every claim traces to
an evidence id in the context. This is the foundation of the citation
discipline in the next topic.

## 5. Thin Context Detection

When the context lacks the material to answer, the model must abstain
rather than guess. The signal is thin context: few chunks, low rerank
scores, no chunk touching the question's key terms. Abstention is the
correct behavior — the next topic covers it in depth.

## Common Mistakes

- Putting normalized text in the context (breaks the quote).
- Exceeding the token budget (truncation drops the answer).
- Ordering chunks arbitrarily (the model reads the wrong material first).
- Letting the model answer from memory instead of the context.

## Key Takeaways

1. The context is the model's only allowed source.
2. Order by relevance, respect the budget.
3. Original text in the context, not normalized.
4. Every claim traces to an evidence id.
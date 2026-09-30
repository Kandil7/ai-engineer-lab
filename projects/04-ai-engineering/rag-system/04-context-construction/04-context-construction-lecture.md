# RAG System 04: Context Construction

## Topic Overview

The context is what the model actually reads. It is assembled from the reranked passages, and
its quality decides the answer's quality more than the model does. A perfect model given the
wrong passages produces a wrong answer; an adequate model given the right passages produces a
grounded one. Context construction is where retrieval becomes generation.

This lecture covers what belongs in the context (the reranked passages with their original
text, provenance, and evidence ids), how to order it, the token budget, why the original text
must be used rather than the normalized search text, and how to detect a context too thin to
answer. It is the last step before generation and the foundation of abstention and citation
(RAG System 05).

The recurring theme is that the context is a contract: the model may answer only from it, every
claim must trace to an evidence id in it, and thin context must lead to abstention rather than
a guess.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Assemble a context from reranked passages with provenance and evidence ids.
2. Order passages by relevance and respect the token budget.
3. Keep the original text in the context, not the normalized form.
4. Instruct the model to answer only from the context and cite evidence ids.
5. Detect a thin context and route it to abstention.
6. Measure context quality for diagnosis.

## Prerequisites

- RAG System 03 (reranking) for the ordered candidates.
- Arabic NLP 01 (the two-text discipline) for why the context holds the original text.

---

## 1. What Belongs in the Context

### The reranked passages

The context holds the reranked passages: their original text, their provenance (book, page,
source version), and their evidence ids. The model answers from this material and nothing
else:

```python
context = [
    {
        "evidence_id": "b1:p7:2",
        "text": "ما الصلاة على المؤمن...",
        "book_id": "b1",
        "page": 7,
    },
    {"evidence_id": "b1:p8:0", "text": "...", "book_id": "b1", "page": 8},
]
```

### The evidence id

The evidence id is the handle the answer's citations resolve to (RAG System 05). It must be
stable and unique, which the chunking step (RAG System 01) guarantees by carrying the
provenance path on every chunk.

### The model's only source

The roadmap's exit test is that the model summarizes the retrieved text rather than answering
from memory. That is enforced here: the context is the only material the model is allowed to
use, and the prompt states it.

## 2. Ordering and Budget

### Order by relevance

Passages are ordered by rerank score, most relevant first. Order matters because models attend
more to the beginning of the context, and because the first passages are the ones most likely
to ground the answer.

### Respect the token budget

The total context must fit the token budget: the model's window minus the prompt and the
reserved output space. When the budget is exceeded, drop the lowest-ranked passages, never the
highest:

```python
def build_context(chunks, budget_tokens):
    """Assemble a ranked, budget-capped context from reranked chunks."""
    ranked = sorted(chunks, key=lambda c: c["score"], reverse=True)
    ...
```

### A ranked window, not a dump

The context is a ranked window into the retrieved material, not everything that was retrieved.
Including low-relevance passages dilutes the signal and spends budget that the best passages
need.

## 3. Original Text, Not Normalized

### The rule

The context carries the original text, the verbatim quote, so the answer can cite it exactly.
The normalized searchable form was for retrieval (Arabic NLP 01); the context is for the
reader and the citation.

### Why mixing them is a bug

If the context holds normalized text, the answer quotes a diacritic-stripped, hamza-unified
version that no longer matches the book. The user sees a quote that looks nearly right and is
not what the source says. This is the most common Arabic RAG bug, and it is prevented by
keeping the two texts separate from ingest onward.

### The citation resolves to the original

The citation's link resolves to the original passage and its source, so the reader can verify
the quote against the book. That is only possible if the context carried the original.

## 4. Grounding and Evidence Ids

### The instruction

The model is instructed to answer only from the context and to cite evidence ids:

```text
Answer only from the context below. Cite the evidence id of every passage you use.
If the context does not contain the answer, say you cannot answer.
```

### Every claim traces to an id

The structured output makes the contract mechanical: the answer is a list of claims, each with
an evidence id from the context. A claim without an id is a hallucination by construction and
is rejected by backend validation (RAG System 05).

### The context is the grounding source

Grounding is not a property of the model; it is a property of the pipeline. The model is
grounded because it is given evidence and required to cite it, not because it chose to be.

## 5. Thin Context Detection

### The signal

A thin context is one that lacks the material to answer: few passages, low rerank scores, or
no passage touching the question's key terms:

```python
def is_thin(context, query_terms):
    """Thin if no chunk touches the query's key terms."""
    return not any(any(t in c["text"] for t in query_terms) for c in context)
```

### The response

Thin context routes to abstention (RAG System 05), not to a guess. The model must refuse
rather than answer from its parameters, because answering from memory is exactly the
hallucination the RAG pipeline exists to prevent.

### The link to failure modes

Thin context is the observable symptom of the "missing material" failure mode (RAG System 07).
Detecting it in the context is cheaper than detecting the wrong answer later.

## 6. Measuring Context Quality

### What to log

Log the query, the context ids, the rerank scores, and the answer (RAG System 07). Context
quality is then measurable after the fact: what fraction of queries had a thin context, what
fraction had noisy context, and how did the answer fare.

### The link to evaluation

Context quality is upstream of every generation metric (faithfulness, citation precision).
Measuring it directly isolates whether a bad answer was a retrieval failure or a generation
failure, which is the diagnosis the eval harness needs.

### The budget utilization

Track how much of the token budget the context uses. A context that consistently uses half the
budget suggests the rerank depth or the budget is mistuned; one that always overflows suggests
the passages are too large and chunking needs attention.

## Real-World Application

- Building the Athar context from the reranked top-5, carrying original text and evidence ids
  for citation.
- Instructing the generator to cite and to abstain, then validating the citations in the
  backend.
- Detecting thin context on an out-of-corpus question and abstaining instead of hallucinating.
- Logging context ids and scores so a faithfulness regression can be traced to retrieval.

## Common Mistakes

1. **Putting normalized text in the context.** The quote breaks against the source.
2. **Exceeding the token budget.** Truncation drops the passage that held the answer.
3. **Ordering arbitrarily.** The model reads the wrong material first.
4. **Letting the model answer from memory.** Grounding is lost; hallucination follows.
5. **No thin-context detection.** The model guesses instead of abstaining.
6. **No logging.** Context failures become undiagnosable.

## Key Takeaways

1. The context is the model's only allowed source; it holds the reranked passages, their
   original text, provenance, and evidence ids.
2. Order by relevance and respect the token budget; drop the lowest-ranked material.
3. Keep the original text in the context, not the normalized search text, so citations are
   exact.
4. Every claim must trace to an evidence id, enforced by structured output and backend
   validation.
5. Detect thin context and route it to abstention; log context quality for diagnosis.

## Self-Check Questions

1. Why does the context carry the original text rather than the normalized search text?
2. What happens when the token budget is exceeded, and which passages are dropped?
3. How is grounding enforced mechanically rather than hoped for?
4. What are the signals of a thin context, and what is the correct response?
5. Why is measuring context quality necessary for diagnosing a bad answer?

## Further Reading / Connections

- RAG System 05 (abstention and citations) — the contract the context feeds.
- RAG System 07 (context failure modes) — the failures the context can exhibit.
- Arabic NLP 01 (Arabic text fundamentals) — the two-text discipline.
- AI Evaluation 02 (faithfulness and citation precision) — measuring the grounded answer.

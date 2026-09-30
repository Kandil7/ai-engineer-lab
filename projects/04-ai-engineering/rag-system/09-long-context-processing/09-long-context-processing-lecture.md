# RAG System 09: Long Context Processing

## Topic Overview

Long documents and long conversations push against the context budget, the finite window a
model can read. Retrieval tries to fill that window with the most relevant material, but the
material can be too large, or the conversation can grow past the window, and the system must
decide what to keep and what to drop. Handling that decision well is the difference between a
system that degrades gracefully and one that silently loses the answer.

This lecture covers the context budget, the three strategies for staying within it
(truncation, summarization, and chunking), how to handle long conversations with compaction,
and the discipline of measuring budget utilization.

The unifying rule is that the budget is a hard constraint, and when it binds, the lowest-ranked
material is what goes. Truncation that drops the highest-ranked passage is worse than no
truncation at all, because it discards the answer while spending the budget.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the context budget and how it is computed.
2. Choose between truncation, summarization, and chunking.
3. Build a budget-aware context that drops the lowest-ranked material.
4. Handle long conversations with compaction.
5. Measure budget utilization and detect a mistuned budget.
6. Explain why chunking is a retrieval-side strategy and truncation a context-side one.

## Prerequisites

- RAG System 04 (context construction) for the ranked context and the budget.
- RAG System 01 (chunking) for the retrieval-side strategy.

---

## 1. The Context Budget

### What it is

The context budget is the model's context window minus the prompt overhead and the space
reserved for the output. It is the number of tokens available for retrieved material and
conversation history.

### Why it is hard

The budget is finite and shared between the instructions, the retrieved passages, the
conversation history, and the output. Every piece competes for it, and the system must
allocate. The budget is a design constraint the whole pipeline is built around.

### The roadmap's rule

The roadmap's exit test is that the budget is respected: the system never overflows the window,
and when it is pressed, it drops the right material. Overflowing produces truncation by the
model's tokenizer, which drops the end of the prompt, which is where the answer often is.

## 2. Truncation

### What it is

Truncation drops the lowest-ranked material to fit the budget:

```python
def fit_budget(chunks, budget_tokens):
    """Truncation: drop the lowest-ranked material to fit the budget."""
    ranked = sorted(chunks, key=lambda c: c["score"], reverse=True)
    ...
```

It is fast and lossy: the dropped material is gone. It is the default context-side strategy
when the material does not fit.

### The rule that matters

Drop the lowest-ranked material, never the highest. A truncation that discards the top passage
to keep a marginal one defeats the purpose. Because the context is ranked (RAG System 04), the
correct drop set is well defined.

### When truncation is right

Truncation is right when the relevant material is a small part of a larger set and the ranking
is trustworthy. It is the simplest strategy and often the correct one for retrieval.

## 3. Summarization

### What it is

Summarization compresses long material into a shorter form, preserving the gist and losing
detail. It is a model call, so it costs latency and tokens, and it can introduce its own errors
(including hallucination in the summary).

### When it is right

Summarization is right when the material is long and its gist is what is needed, for example a
long conversation history or a long document where the detail is not the answer. It is wrong
when precision matters, because the summary may drop the exact passage the answer needs.

### The tradeoff

Summarization trades compute for budget: you spend a model call to free context space. It is
the right tool when the freed space is worth more than the call, which depends on the budget
pressure.

## 4. Chunking

### The retrieval-side strategy

Chunking splits long documents before retrieval, so each chunk already fits the budget (RAG
System 01). It is a retrieval-side strategy, applied at ingest, while truncation and
summarization are context-side strategies applied at query time.

### Why it is the primary fix

If documents are chunked well, the context assembler rarely needs to truncate a huge passage,
because no passage is huge. Chunking is the structural fix; truncation and summarization patch
the remaining cases.

### The link to structure

Structure-aware chunking (RAG System 01) produces passages aligned to natural boundaries, so a
chunk is a coherent unit that fits the budget, which is the desirable state.

## 5. Long Conversations

### The problem

A long conversation grows the history until it consumes the budget meant for retrieved
material, crowding out the evidence and degrading the answer.

### Compaction

The strategy is compaction: summarize the older turns and keep the recent ones:

```python
def compact(turns, keep_recent):
    """Compaction: summarize older turns, keep recent ones."""
    ...
```

The summary preserves the conversation's context; the recent turns preserve its detail. The
split point is a tuning decision bounded by the budget.

### What to keep

Keep the recent turns verbatim and summarize the rest. The recent turns carry the immediate
context; the older ones usually matter only for their gist. Pinning important facts (from
semantic memory, RAG System 10) can outlive compaction.

## 6. Measuring Budget Utilization

### What to measure

Track how much of the budget the context uses. A context that consistently uses half the budget
means the budget or the rerank depth is mistuned (the system is leaving space unused); one that
always overflows means passages are too large and chunking needs attention.

### Why it matters

Budget utilization is a leading indicator: a rising utilization means the corpus or the
conversations are growing, and the system is heading toward truncation. Catching the trend
early lets chunking or compaction be adjusted before quality drops.

### The link to the log

Budget utilization is part of the context log (RAG System 07), so the trend is visible over
time and a regression is attributable.

## Real-World Application

- Truncating a large Athar retrieval set to the budget, dropping the lowest-scored passages
  first.
- Compacting a long DevMate session so recent turns stay verbatim and older ones become a
  summary.
- Detecting that documents are too large for the budget and moving to finer chunking.
- Tracking budget utilization to catch a corpus growth trend early.

## Common Mistakes

1. **Ignoring the budget.** The model truncates at the end, dropping the answer.
2. **Truncating the highest-ranked material.** The budget is spent on the wrong passages.
3. **Summarizing when chunking suffices.** Compute is spent to fix a structural problem.
4. **No compaction for long conversations.** History crowds out evidence.
5. **No budget measurement.** The trend toward overflow is invisible.
6. **Letting detail-sensitive material be summarized.** The exact passage is lost.

## Key Takeaways

1. The context budget is the window minus prompt and output; the system must allocate it.
2. Truncation drops the lowest-ranked material and is the default context-side strategy.
3. Summarization compresses gist at the cost of a model call and lost detail; use it when the
   gist is what is needed.
4. Chunking is the retrieval-side structural fix; truncation and summarization patch the rest.
5. Long conversations are compacted, and budget utilization is measured to catch the trend
   early.

## Self-Check Questions

1. How is the context budget computed, and why is it a shared resource?
2. Which material does truncation drop, and why does that rule matter?
3. When is summarization the right strategy, and what does it cost?
4. Why is chunking the primary fix for long documents rather than truncation?
5. What does a consistently half-used budget tell you?

## Further Reading / Connections

- RAG System 01 (chunking) — the retrieval-side structural fix.
- RAG System 04 (context construction) — the ranked context and the budget.
- RAG System 10 (memory systems) — compaction and the facts that outlive it.
- Model Serving 03 (inference serving) — why prompt length affects time to first token.

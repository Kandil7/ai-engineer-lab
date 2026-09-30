# RAG System 09: Long Context Processing

## 🎯 Topic Overview

Long documents and long conversations push against the context budget.
This lecture covers the three strategies — truncation, summarization, and
chunking — and the discipline of staying within the budget.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain the context budget
2. Choose between truncation, summarization, and chunking
3. Design a budget-aware context builder
4. Handle long conversations
5. Measure the budget utilization

---

## 1. The Context Budget

The model's context window is finite. The budget is the window minus the
prompt and the output space. Every piece of context is measured against
the budget. The roadmap's exit test: "the context budget is respected."

## 2. Truncation

Truncation drops the lowest-ranked material to fit the budget. It is fast
and lossy — the dropped material is gone. The roadmap's exit test:
"truncation drops the lowest-ranked material."

## 3. Summarization

Summarization compresses long material into a shorter form. It preserves
the gist but loses detail. Summarization is a model call, so it costs
latency and tokens. The roadmap's exit test: "summarization compresses
long material."

## 4. Chunking

Chunking splits long documents before retrieval, so each chunk fits the
budget. Chunking is the retrieval-side strategy; truncation and
summarization are the context-side strategies. The roadmap's exit test:
"long documents are chunked before retrieval."

## 5. Long Conversations

A long conversation grows the context. The strategy is compaction:
summarize the older turns and keep the recent ones. The roadmap's exit
test: "long conversations are compacted."

## Common Mistakes

- Ignoring the budget (truncation at random).
- Summarizing when chunking suffices.
- No compaction for long conversations.
- No budget measurement.
- Truncating the highest-ranked material.

## Key Takeaways

1. The budget is the window minus prompt and output.
2. Truncation drops the lowest-ranked material.
3. Summarization compresses but loses detail.
4. Chunking is the retrieval-side strategy.
5. Long conversations are compacted.
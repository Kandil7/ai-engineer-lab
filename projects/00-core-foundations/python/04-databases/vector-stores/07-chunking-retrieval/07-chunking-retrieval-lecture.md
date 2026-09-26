# Databases — 07: Chunking and Retrieval Quality

## Topic Overview

Embeddings work on chunks, not documents: too large and the signal drowns,
too small and the meaning fragments. This lecture covers why chunking is the
highest-leverage retrieval decision, fixed-size with overlap, sentence
boundaries, and how to measure a chunking strategy by retrieval quality
instead of intuition — the weeks 2–3 chunking ADR in miniature.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why chunk size bounds retrieval quality in both directions
2. Implement fixed-size chunking with overlap and state what overlap costs
3. Implement sentence-boundary chunking and state when it beats fixed-size
4. Measure two strategies against each other with recall@k on fixed queries
5. Argue a chunking choice from numbers for a code corpus specifically

## Prerequisites

| Need | Where |
|---|---|
| Recall@k measurement | [01](../01-vector-search-fundamentals/01-vector-search-fundamentals-lecture.md) |
| The runnable exercise | [07-chunking-retrieval.py](07-chunking-retrieval.py) |

## 1. Why Chunk

One embedding per document averages the whole thing into mush — a query
about one paragraph retrieves the document but ranks it by its average
meaning, and the generator receives far more context than the answer needs.
One embedding per sentence fragments meaning across boundaries and explodes
the index. Chunks are the compromise, and their size is the single most
consequential retrieval parameter most teams set by default and never revisit.

```python
def fixed_chunks(text, size=500, overlap=50):
    # Overlap preserves boundary context; cost is ~overlap/size extra index.
    return [text[i:i + size] for i in range(0, len(text), size - overlap)]
```

## 2. Fixed-Size vs Sentence Boundaries

Fixed-size is predictable: uniform token counts, uniform costs, splits that
cut sentences (and code blocks) mid-thought. Sentence-boundary chunking
respects linguistic units at the price of variable sizes. On prose the
boundary version usually wins recall; on code neither wins automatically —
which is why DevMate tests AST-aware chunking as the third contender.

## 3. Measuring, Not Preferring

Fix the queries, fix k, vary only the chunker, read recall@k. The exercise
runs this comparison on a small corpus so the protocol is muscle memory
before the weeks 2–3 ADR runs it on the whole repo. A strategy change that
moves recall@10 by 5pp matters more than most model swaps — measure it like
one.

## 4. Code Is Special

Code has hard structure (functions, classes) that sentences approximate
poorly. AST-aware chunking splits on syntax boundaries with line ranges, so a
retrieved chunk is a complete unit the generator can cite and the developer
can read. Syntax-error fallback keeps the pipeline alive on broken files.
This is the argument the chunking ADR makes with numbers.

## Common Mistakes

- 4000-token chunks "to fit more context" — signal drowns, recall drops.
- Zero overlap on fixed-size — answers spanning boundaries become unretrievable.
- Comparing chunkers while also changing the model — vary one thing.

## DevMate Connection

The weeks 2–3 build order puts the golden set and eval harness before the
three chunkers precisely so this lecture's protocol runs at repo scale:
fixed-size vs recursive vs AST-aware, recall@5/10 and MRR per strategy, ADR
with a results table. Chunking is the ADR DevMate interviews are built on.

## Key Takeaways

1. Chunk size bounds quality from both sides; overlap has a measured cost.
2. Sentence boundaries beat fixed-size on prose; code needs syntax boundaries.
3. Compare chunkers by recall@k, varying nothing else.

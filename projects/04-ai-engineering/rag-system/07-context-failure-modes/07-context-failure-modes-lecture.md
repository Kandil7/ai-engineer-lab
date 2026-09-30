# RAG System 07: Context Failure Modes

## 🎯 Topic Overview

The context is the model's only allowed source, so context failures are
answer failures. This lecture covers the four failure modes — missing
material, noisy material, stale material, and contradictory material —
and how each shows up in the answer.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Identify the four context failure modes
2. Trace each failure to its retrieval cause
3. Detect failures in the answer
4. Design guards against each mode
5. Log context quality for diagnosis

---

## 1. Missing Material

The relevant passage is not in the context. The answer is either wrong or
an abstention. The cause is a retrieval failure — low recall, wrong
filters, or a bad query embedding. The roadmap's exit test: "missing
material is detected."

```python
# the golden set knows the relevant passage; the context does not contain it
if not set(golden["relevant"]) & set(context_ids):
    log("missing material", query)
```

## 2. Noisy Material

Irrelevant passages crowd the context. The answer may pick up the noise
or lose the signal. The cause is low precision — the retriever returns
mixed relevance. The guard is a score threshold and a reranker.

## 3. Stale Material

The context holds an outdated version of the source. The answer is wrong
from the model's perspective — it is faithful to stale evidence. The cause
is a cache serving old content or an un-reindexed corpus. The guard is the
provenance version in the context.

## 4. Contradictory Material

Two passages in the context disagree. The answer picks one or
hallucinates a synthesis. The cause is a corpus with conflicting sources.
The guard is the abstention rule on contradiction detection.

## 5. Logging for Diagnosis

Each query logs: the query, the context ids, the scores, and the answer.
A failure is diagnosed by reading the log — was the material missing,
noisy, stale, or contradictory? The log is the diagnosis tool. The
roadmap's exit test: "context quality is logged."

## Common Mistakes

- Ignoring missing material (the answer just goes wrong).
- No score threshold (noise floods the context).
- No provenance version (stale material undetectable).
- No contradiction detection (the answer synthesizes a lie).
- No logging (failures are undiagnosable).

## Key Takeaways

1. Four failure modes: missing, noisy, stale, contradictory.
2. Each has a retrieval cause and a guard.
3. The answer's quality is the context's quality.
4. Provenance version catches staleness.
5. Log context quality for diagnosis.
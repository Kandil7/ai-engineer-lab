# RAG System 07: Context Failure Modes

## Topic Overview

The context is the model's only allowed source, so context failures are answer failures. When
an answer is wrong, the instinct is to blame the model, but in a RAG system the more common
cause is the context: the right material was missing, the context was full of noise, the
material was stale, or two passages contradicted each other. Naming these four failure modes
turns a vague "the answer is bad" into a specific, testable diagnosis.

This lecture covers missing material, noisy material, stale material, and contradictory
material, tracing each to its retrieval cause and its guard, and covering the logging that
makes the diagnosis possible.

The value of the taxonomy is that each mode has a different fix. Missing material is a recall
problem; noisy material is a precision problem; stale material is a versioning problem;
contradictory material is a corpus-curation problem. Treating them all as "retrieval is bad"
leads to changes that fix one and break another.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Identify the four context failure modes.
2. Trace each failure to its retrieval or data cause.
3. Detect each failure with a concrete signal.
4. Design the guard for each mode.
5. Log context quality so failures are diagnosable after the fact.
6. Route each failure to its correct fix rather than the wrong layer.

## Prerequisites

- RAG System 04 (context construction) for the context and its signals.
- RAG System 05 (abstention and citations) for the correct response to bad context.

---

## 1. Missing Material

### What it is

The relevant passage is not in the context. The answer is either wrong or an abstention. The
cause is a retrieval failure: low recall, an over-restrictive filter, a bad query embedding, or
a chunking boundary that split the answer.

### Detection

The golden set knows the relevant passage; the context does not contain it:

```python
if not set(golden["relevant"]) & set(context_ids):
    log("missing material", query)
```

### The guard

The guard is better recall: fix the retriever (Arabic NLP 03-05), loosen an over-restrictive
filter (RAG System 02), or reconsider the chunk boundaries (RAG System 01). Thin-context
detection (RAG System 04) routes it to abstention in the meantime.

## 2. Noisy Material

### What it is

Irrelevant passages crowd the context. The answer may pick up the noise or lose the signal
among distractions. The cause is low precision: the retriever returned mixed relevance.

### Detection

A low-score passage is present:

```python
def detect_noisy(context, min_score):
    return any(c["score"] < min_score for c in context)
```

### The guard

The guard is a score threshold plus a reranker (RAG System 03). The reranker promotes the
relevant passages and demotes the noise; a threshold drops anything below the relevance floor,
even if the budget allows it.

## 3. Stale Material

### What it is

The context holds an outdated version of the source. The answer is wrong from the world's
perspective, but the model is faithful to stale evidence, which makes the failure harder to
notice: the answer is grounded, just in a superseded source.

### Detection

The expected source version is absent, or a superseded version is present:

```python
def detect_stale(context_versions, expected):
    return expected not in context_versions
```

### The guard

The guard is the provenance version in the context (RAG System 01, 02) and a cache keyed on the
corpus version (RAG System 06). A re-ingest bumps the version, and the stale passages are
filtered out.

## 4. Contradictory Material

### What it is

Two passages in the context disagree. The answer picks one arbitrarily or hallucinates a
synthesis of both. The cause is a corpus with conflicting sources, which is common in domains
with schools of thought.

### Detection

Two passages make different claims:

```python
def detect_contradictory(context):
    claims = [c.get("claim") for c in context if c.get("claim")]
    return len(set(claims)) > 1 and len(claims) > 1
```

### The guard

The guard is the abstention rule on detected contradiction: present both views or refuse to
pick, rather than silently synthesize. For a domain like Islamic jurisprudence, presenting the
difference between sources is often the correct answer.

## 5. Logging for Diagnosis

### What to log

Each query logs the query, the context ids, the scores, the versions, and the answer. A failure
is then diagnosable by reading the log: was the material missing, noisy, stale, or
contradictory?

### Why the log is the tool

Without the log, a bad answer is a mystery and every hypothesis is a guess. With it, the
failure mode is read off the record, and the fix is routed to the right layer. The log is the
diagnosis tool the roadmap's exit test calls for.

### The link to evaluation

The logged signals aggregate into context-quality metrics: thin-context rate, average context
score, stale rate. These are leading indicators that a traditional error rate would miss, and
they connect the production monitoring (AI Evaluation 07) back to the retrieval layer.

## 6. Routing the Fix

### The mapping

| Failure mode | Cause | Fix layer |
| --- | --- | --- |
| Missing | Low recall | Retrieval: indexing, fusion, filters |
| Noisy | Low precision | Ranking: reranker, threshold |
| Stale | Versioning | Ingest and cache: provenance versions |
| Contradictory | Corpus conflict | Curation and abstention |

### Why the mapping matters

Each mode lives in a different layer, so a fix aimed at the wrong layer wastes effort and can
break a working mode. The taxonomy is what keeps the fix pointed at the cause.

## Real-World Application

- Diagnosing a wrong Athar answer as missing material and fixing the chunker rather than the
  prompt.
- Adding a score threshold to stop noisy passages crowding the context.
- Catching stale passages after a re-ingest by filtering on `source_version`.
- Presenting two scholarly opinions as a deliberate answer rather than synthesizing a third.

## Common Mistakes

1. **Blaming the model for a context failure.** The context is the more common cause.
2. **No score threshold.** Noise floods the context.
3. **No provenance version.** Stale material is undetectable.
4. **No contradiction handling.** The answer synthesizes a lie.
5. **No logging.** Failures are undiagnosable and the fix is a guess.
6. **Fixing the wrong layer.** A recall fix applied to a precision problem.

## Key Takeaways

1. Four failure modes: missing, noisy, stale, contradictory; each has a cause and a guard.
2. Missing is a recall problem, noisy a precision problem, stale a versioning problem,
   contradictory a curation problem.
3. Detect each with a concrete signal, and guard each at its own layer.
4. Log the query, context ids, scores, versions, and answer so diagnosis is mechanical.
5. Read context quality as a leading indicator that error rates miss.

## Self-Check Questions

1. Why is a stale answer harder to notice than a missing one?
2. What signal detects noisy context, and what is the guard?
3. Why is presenting two opinions often correct for a contradictory context?
4. What does each log entry need so a failure can be diagnosed after the fact?
5. Map each failure mode to the layer that should fix it.

## Further Reading / Connections

- RAG System 03 (reranking) — the precision fix for noisy material.
- RAG System 04 (context construction) — thin-context detection.
- RAG System 06 (caching) — the staleness the version key prevents.
- AI Evaluation 07 (production monitoring) — the signals these failures surface.

# RAG System 10: Memory Systems

## Topic Overview

Memory is what the system remembers between interactions. A stateless RAG system answers each
query from the corpus alone; a system with memory also carries the conversation, the facts
learned about the user or the task, and the history of past interactions. Memory is what turns a
question-answering tool into an assistant that improves across a session and across sessions.

This lecture covers the three memory types (conversation, semantic, and episodic), the write
and read paths, how to bound growth, and how to test coherence. The discipline is that memory is
a first-class store with the same engineering concerns as the corpus: a schema, a write path, a
read path, a bounds, and consistency.

The hardest part is coherence: a system with memory can contradict its own past, which erodes
trust faster than a wrong answer. Memory without coherence testing is a liability.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish conversation, semantic, and episodic memory.
2. Design the write path so memory is written after each interaction without blocking the
   response.
3. Design the read path so memory is assembled into the context at query time.
4. Bound memory growth with TTLs, caps, and retention windows.
5. Test memory coherence across sessions.
6. Explain how memory interacts with the context budget.

## Prerequisites

- RAG System 04 (context construction) for how memory enters the context.
- RAG System 09 (long context processing) for compaction and the budget.

---

## 1. The Three Types

### Conversation memory

Conversation memory holds the current session's turns. It is the immediate context: what the
user just said, what the system just answered. It is bounded by the session and compacted when
it grows (RAG System 09).

### Semantic memory

Semantic memory holds facts extracted from interactions: the user's preferences, the task's
constraints, the decisions made. It is the durable knowledge about the user or task, and it
outlives the session.

### Episodic memory

Episodic memory holds past interactions as retrievable events: this query produced this answer
under these conditions. It is the history, retrieved by similarity to the current query.

### Why the distinction matters

Each type has a different lifetime, a different retrieval pattern, and a different failure mode.
Collapsing them into one store (usually raw conversation history) loses the structure that makes
memory useful.

## 2. The Write Path

### What happens after an interaction

After each interaction, memory is written:

- Conversation memory appends the turn.
- Semantic memory extracts and stores facts.
- Episodic memory stores the interaction as a retrievable event.

### Asynchronous by default

The write path should not block the user's response. The answer is returned, and the memory
writes happen in the background (a worker queue, RAG System 09's compaction completes over
time). Blocking on the write couples the user's latency to the memory subsystem.

### Extraction is the hard part

Semantic extraction is a model step: deciding which facts to store. It can be wrong, so it is
validated and versioned like any other model output, and a bad extraction is reversible.

## 3. The Read Path

### Assembling the context

At query time, memory is read:

- Conversation memory provides the recent turns.
- Semantic memory provides the facts relevant to the task.
- Episodic memory provides similar past interactions.

The read path assembles these into the context, alongside the retrieved corpus passages, within
the budget (RAG System 04, 09).

### The relevance filter

Not all memory is relevant to every query. Unlike conversation memory, semantic and episodic
memory are filtered by relevance before entering the context, or they would flood it. The filter
is the same retrieval idea applied to memory.

### The budget competition

Memory competes with corpus passages for the context budget. A system that always injects all
memory starves the retrieval; one that injects none forgets the conversation. The allocation is
a design decision.

## 4. Bounding Growth

### Why bounded

Memory grows without bound if unmanaged: every turn appends, every interaction adds an episode.
Unbounded memory is a cost problem and a relevance problem, because old irrelevant memory
crowds the reads.

### The bounds

- **TTL on conversation memory:** turns expire after the session or a time window.
- **Size cap on semantic memory:** keep the most relevant or most recent facts up to a limit.
- **Retention window on episodic memory:** keep a bounded number of recent episodes, decayed by
  age.

### The eviction rule

Eviction must be principled, not arbitrary. The usual rules are recency (newer first), relevance
(highest-value first), or a combination. The rule is recorded, because silent eviction of
important memory is a source of surprising failures.

## 5. Testing Coherence

### What coherence means

Memory coherence means the system does not contradict its own memory. If semantic memory says the
capital of France is Paris, a later answer that says otherwise is a coherence failure.

```python
def is_coherent(memory, claim):
    """Coherence: the system does not contradict its own memory."""
    return all(v != f"not-{claim}" for v in memory.semantic.values())
```

### Why it is tested across sessions

Coherence failures surface across sessions, when today's answer meets yesterday's memory. The test
asks the same question in different sessions and checks for contradiction.

### The response to a contradiction

When memory contradicts itself, the system must resolve it (prefer the newer fact) or abstain,
never silently pick one. Contradictory memory is the same failure mode as contradictory context
(RAG System 07), and it gets the same treatment.

## 6. Memory and the Rest of the Pipeline

### The context link

Memory enters the context through the same budget and the same grounding rules. Memory-provided
claims are cited like corpus passages, so the answer stays verifiable.

### The security link

Memory is per-user and must be tenant-scoped like any other data (RAG System 08). A memory store
that leaks across users is the same incident as a retrieval leak.

### The evaluation link

Memory adds a class of evaluation questions: does the system remember correctly, and does it
forget when it should? These are added to the golden set as multi-turn cases.

## Real-World Application

- Athar remembering a session's discussion context while keeping facts about the user's
  preferences in semantic memory.
- DevMate recalling prior interactions with a repository as episodic memory, retrieved by
  similarity to the current question.
- Bounding conversation memory by compaction so a long session does not starve retrieval.
- Testing that a fact learned in one session is neither forgotten nor contradicted in the next.

## Common Mistakes

1. **No memory types.** Everything is raw conversation history.
2. **Blocking the response on memory writes.** Latency is coupled to the memory subsystem.
3. **Unbounded memory growth.** Cost and relevance both degrade.
4. **Injecting all memory every query.** It floods the context and starves retrieval.
5. **No coherence testing.** The system contradicts its own past.
6. **Memory not tenant-scoped.** It leaks across users.

## Key Takeaways

1. Three memory types: conversation, semantic, and episodic, each with a different lifetime and
   retrieval pattern.
2. The write path is asynchronous; semantic extraction is a model step and is validated.
3. The read path assembles memory into the context within the budget, filtered by relevance.
4. Growth is bounded by TTLs, caps, and retention windows with a principled eviction rule.
5. Coherence is tested across sessions, and contradictory memory is resolved explicitly, not
   silently.

## Self-Check Questions

1. What does each of the three memory types store, and how do their lifetimes differ?
2. Why should the write path not block the user's response?
3. Why must semantic and episodic memory be filtered by relevance before entering the context?
4. Give one bound for each memory type and the eviction rule.
5. Why is memory coherence tested across sessions rather than within one?

## Further Reading / Connections

- RAG System 04 (context construction) and 09 (long context processing) — how memory enters the
  context under the budget.
- RAG System 07 (context failure modes) and 08 (context security) — contradiction and isolation.
- AI Evaluation 07 (production monitoring) — memory coherence as a monitored signal.
- `.ai/workflows/` — where multi-turn behavior is specified.

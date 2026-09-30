# RAG System 07: Context Failure Modes — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Missing material | Relevant passage not in the context | low recall |
| Noisy material | Irrelevant passages crowd the context | low precision |
| Stale material | Outdated source version in the context | cache or reindex |
| Contradictory material | Two passages disagree | conflicting sources |
| Context quality log | The query + context ids + scores | diagnosis tool |
| Provenance version | The source version in the context | staleness guard |
| Score threshold | The similarity floor | noise guard |

---

## Alphabetical Glossary

### Contradictory material

**Definition:** Two passages in the context disagree. The answer picks one
or hallucinates a synthesis. The cause is a corpus with conflicting
sources.

**Example:**
```python
# passage A says X, passage B says not-X -> contradiction
```

**Related concepts:** Abstention

---

### Context quality log

**Definition:** The record of each query: the query, context ids, scores,
and answer. The diagnosis tool for context failures.

**Example:**
```python
log(query, context_ids, scores, answer)
```

**Related concepts:** Missing material

---

### Missing material

**Definition:** The relevant passage is not in the context. The answer is
wrong or an abstention. The cause is a retrieval failure.

**Example:**
```python
# golden["relevant"] not in context_ids
```

**Related concepts:** Noisy material

---

### Noisy material

**Definition:** Irrelevant passages crowd the context. The answer may pick
up the noise or lose the signal. The cause is low precision.

**Example:**
```python
# 5 passages in the context, only 1 is relevant
```

**Related concepts:** Score threshold

---

### Provenance version

**Definition:** The source version carried in the context. The staleness
guard — a mismatch means the material is outdated.

**Example:**
```python
# context carries source_version "v2"; cache holds "v1" -> stale
```

**Related concepts:** Stale material

---

### Score threshold

**Definition:** The similarity floor that drops weak matches. The noise
guard.

**Example:**
```python
# score < 0.7 -> dropped from the context
```

**Related concepts:** Noisy material

---

### Stale material

**Definition:** An outdated version of the source in the context. The
answer is faithful to stale evidence. The cause is a cache or an
un-reindexed corpus.

**Example:**
```python
# cache serving a corrected passage's old version
```

**Related concepts:** Provenance version

---

## Related Concepts

- **Context construction**: where failures enter the context (topic 04)
- **Caching**: stale material comes from caches (topic 06)
- **Abstention**: the guard on contradiction (topic 05)

## Key Takeaways

1. Four failure modes: missing, noisy, stale, contradictory.
2. Each has a retrieval cause and a guard.
3. The answer's quality is the context's quality.
4. Provenance version catches staleness.
5. Log context quality for diagnosis.
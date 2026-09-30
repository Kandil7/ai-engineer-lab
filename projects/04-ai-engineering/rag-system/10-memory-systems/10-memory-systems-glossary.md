# RAG System 10: Memory Systems — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Conversation memory | The current session's turns | recent turns |
| Semantic memory | Facts extracted from past interactions | stored facts |
| Episodic memory | Past interactions as retrievable events | similar sessions |
| Write path | Memory written after each interaction | async |
| Read path | Memory read at query time | assembles context |
| Memory bound | TTL, size cap, retention window | growth limit |
| Coherence | No self-contradiction across sessions | tested |

---

## Alphabetical Glossary

### Coherence

**Definition:** The system does not contradict its own memory. Tested by
asking the same question across sessions.

**Example:**
```python
# session 1: "my name is X"; session 2: "my name is X" -> coherent
```

**Related concepts:** Semantic memory

---

### Conversation memory

**Definition:** The current session's turns. Provides recent context.

**Example:**
```python
# the last 5 turns in the context
```

**Related concepts:** Episodic memory

---

### Episodic memory

**Definition:** Past interactions stored as retrievable events. Provides
similar past interactions.

**Example:**
```python
# "last week you asked about X" -> retrieved
```

**Related concepts:** Conversation memory

---

### Memory bound

**Definition:** The growth limit: TTL on conversation, size cap on
semantic, retention window on episodic.

**Example:**
```python
# conversation TTL 24h; semantic cap 10K facts; episodic window 90d
```

**Related concepts:** Write path

---

### Read path

**Definition:** Memory read at query time. Assembles the context from the
three memory types.

**Example:**
```python
# recent turns + relevant facts + similar episodes -> context
```

**Related concepts:** Write path

---

### Semantic memory

**Definition:** Facts extracted from past interactions and stored
separately. Provides relevant facts at query time.

**Example:**
```python
# "user prefers Arabic" -> stored as a fact
```

**Related concepts:** Coherence

---

### Write path

**Definition:** Memory written after each interaction. Asynchronous — the
user's response is not blocked.

**Example:**
```python
# after each turn: append conversation, extract facts, store episode
```

**Related concepts:** Read path

---

## Related Concepts

- **Context construction**: memory feeds the context (topic 04)
- **Caching**: conversation memory is a cache (topic 06)
- **Long context**: compaction manages conversation memory (topic 09)

## Key Takeaways

1. Three types: conversation, semantic, episodic.
2. The write path is asynchronous.
3. The read path assembles the context.
4. Growth is bounded by TTL and caps.
5. Coherence is tested across sessions.
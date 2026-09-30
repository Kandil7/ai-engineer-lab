# RAG System 10: Memory Systems

## 🎯 Topic Overview

Memory is what the system remembers between interactions. This lecture
covers the three memory types — conversation, semantic, and episodic —
and the architecture that keeps them coherent.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Distinguish conversation, semantic, and episodic memory
2. Design the memory write path
3. Design the memory read path
4. Bound memory growth
5. Test memory coherence

---

## 1. The Three Types

Conversation memory holds the current session's turns. Semantic memory
holds facts extracted from past interactions. Episodic memory holds
past interactions as retrievable events. Each serves a different
purpose. The roadmap's exit test: "the three memory types are
distinguished."

## 2. The Write Path

Memory is written after each interaction. Conversation memory appends
the turn. Semantic memory extracts and stores facts. Episodic memory
stores the interaction as a retrievable event. The write path is
asynchronous — the user's response is not blocked. The roadmap's exit
test: "memory is written after each interaction."

## 3. The Read Path

Memory is read at query time. Conversation memory provides the recent
turns. Semantic memory provides relevant facts. Episodic memory provides
similar past interactions. The read path assembles the context from
memory. The roadmap's exit test: "memory is read at query time."

## 4. Bounding Growth

Memory grows without bound if unmanaged. The bounds: TTL on conversation
memory, a size cap on semantic memory, and a retention window on episodic
memory. The roadmap's exit test: "memory growth is bounded."

## 5. Testing Coherence

Memory coherence means the system does not contradict its own memory.
The test: ask the same question across sessions and check for
contradiction. The roadmap's exit test: "memory coherence is tested."

## Common Mistakes

- No memory types (everything is conversation).
- Blocking the response on memory writes.
- Unbounded memory growth.
- No coherence testing.
- Memory without a read path.

## Key Takeaways

1. Three types: conversation, semantic, episodic.
2. The write path is asynchronous.
3. The read path assembles the context.
4. Growth is bounded by TTL and caps.
5. Coherence is tested across sessions.
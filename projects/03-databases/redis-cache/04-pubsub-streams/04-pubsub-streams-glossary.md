# Redis 04: Pub/Sub and Streams — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Channel | A named topic for routing | chat:abc123 |
| Publish | Sending a message to a channel | PUBLISH |
| Subscribe | Registering interest in a channel | SUBSCRIBE |
| Fire-and-forget | Messages are not stored | offline = missed |
| Stream | A persistent, replayable log | guaranteed delivery |
| Consumer | A reader of a stream | reads at its own pace |
| Delivery guarantee | Pub/Sub none, Streams yes | the choice |

---

## Alphabetical Glossary

### Channel

**Definition:** A named topic that routes messages. A publisher sends to a
channel; every subscriber of that channel receives it.

**Example:**
```python
# chat:abc123 routes to the session's subscribers
```

**Related concepts:** Publish, Subscribe

---

### Consumer

**Definition:** A reader of a stream. Reads messages at its own pace, with
the full history available.

**Example:**
```python
# a worker reading the job stream
```

**Related concepts:** Stream

---

### Delivery guarantee

**Definition:** Whether a message is guaranteed to reach its consumer.
Pub/Sub offers none; Streams offer persistence and replay.

**Example:**
```python
# jobs need Streams; live chat tolerates Pub/Sub
```

**Related concepts:** Fire-and-forget, Stream

---

### Fire-and-forget

**Definition:** Pub/Sub does not store messages. A subscriber offline
misses what was published while it was away.

**Example:**
```python
# a message published with no subscriber is lost
```

**Related concepts:** Delivery guarantee

---

### Publish

**Definition:** Sending a message to a channel. Every subscriber receives
it.

**Example:**
```python
# PUBLISH chat:abc123 {message}
```

**Related concepts:** Channel, Subscribe

---

### Stream

**Definition:** A persistent, replayable log. Messages are stored;
consumers read them at their own pace; history is available.

**Example:**
```python
# XADD job:queue ...; XREAD ...
```

**Related concepts:** Consumer, Delivery guarantee

---

### Subscribe

**Definition:** Registering interest in a channel. The subscriber receives
every message published to it.

**Example:**
```python
# SUBSCRIBE chat:abc123
```

**Related concepts:** Channel, Publish

---

## Related Concepts

- **Key patterns**: channels are named like keys (topic 02)
- **Rate limiting**: counters are separate from channels (topic 03)
- **Background tasks**: streams feed workers (background-tasks skill)

## Key Takeaways

1. A channel routes messages to subscribers.
2. Publish sends; subscribe registers interest.
3. Pub/Sub is fire-and-forget.
4. Streams add persistence and replay.
5. The choice is a delivery guarantee decision.
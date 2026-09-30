# Redis 04: Pub/Sub and Streams

## Topic Overview

Redis Pub/Sub delivers messages to subscribers in real time; Redis Streams adds persistence and replay.
The two look similar and solve different problems, and choosing the wrong one produces either lost
messages or unnecessary complexity. The decision is a delivery-guarantee decision: does the message
need to survive if the subscriber is not listening?

This lecture covers the channel, the publish/subscribe model and its fire-and-forget nature, what
Streams add, and how to choose between them.

The core discipline is to state the delivery guarantee you need before picking the mechanism. Pub/Sub
guarantees nothing beyond "delivered if a subscriber is connected"; Streams guarantee persistence and
replay. Everything else follows from that.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Publish to a channel and subscribe to it.
2. Explain the fire-and-forget nature of Pub/Sub.
3. Explain what Streams add over Pub/Sub.
4. Choose Pub/Sub or Streams for a use case.
5. Name channels consistently.
6. Explain why the choice is a delivery-guarantee decision.

## Prerequisites

- Redis 02 (key patterns) for the naming discipline.
- Data Engineering 04 (checkpointing) for the persistence idea.

---

## 1. The Channel

### What it is

A channel is a named topic. A publisher sends a message to a channel; every subscriber of that channel
receives it:

```text
PUBLISH chat:abc123 {message}
SUBSCRIBE chat:abc123
```

### The routing key

The channel is the routing key, and its name follows the same namespacing discipline as keys:
`chat:{session_id}` routes a message to the session's subscribers. A consistent naming scheme keeps the
channels understandable.

### The exit test

The roadmap's exit test is that real-time delivery uses channels, which is the mechanism for one-to-many
delivery.

## 2. Publish and Subscribe

### The model

Publish sends a message to a channel; subscribe registers interest in a channel:

```python
ps.subscribe("chat:abc123", "client-1")
assert ps.publish("chat:abc123", "hello") == ["client-1"]
```

Every current subscriber receives the message, which is the one-to-many broadcast.

### The exit test

The roadmap's exit test is that messages are published and subscribed, which is the basic pub/sub
operation.

## 3. Fire-and-Forget

### The nature

Pub/Sub does not store messages. A message published when no subscriber is listening is lost:

```python
assert ps.publish("chat:empty", "lost") == [], "no subscriber -> lost"
```

### When it is fine

Fire-and-forget is fine for ephemeral events: a live chat message, a notification, a cache-invalidation
signal. If a subscriber misses it, the state is still consistent because the event was about a moment,
not about durable data.

### When it is wrong

Fire-and-forget is wrong for anything that must be delivered: a job, a payment event, an audit record.
Lost delivery here is lost work, and Pub/Sub provides no recovery.

### The exit test

The roadmap's exit test is that the fire-and-forget limitation is understood, which is what prevents
using Pub/Sub for durable work.

## 4. Streams

### What they add

Streams add persistence and replay. Messages are stored, consumers read them at their own pace, and
history is available:

```python
stream.add("job-1")
stream.add("job-2")
assert stream.read() == ["job-1", "job-2"], "history is available"
```

### Why persistence matters

A stream is a log, not a broadcast. A consumer that was offline can read the messages it missed, and a
new consumer can replay history. This is what durable work needs.

### The link to the queue

Streams are the Redis-side of the queue pattern (System Design 02): jobs that survive process death,
consumers that ack, and redelivery. The stream is the transport; the idempotency and the DLQ live in
the consumer.

### The exit test

The roadmap's exit test is that guaranteed delivery uses streams, which is the durable mechanism.

## 5. Choosing

### The decision

| Need | Mechanism |
| --- | --- |
| Ephemeral broadcast, real time | Pub/Sub |
| Guaranteed delivery, replay | Streams |

Pub/Sub for a live chat, a notification, or a cache-invalidation signal. Streams for jobs, events that
must not be lost, and replayable history.

### The exit test

The roadmap's exit test is that the choice is deliberate, which is what prevents lost messages or
needless complexity.

## 6. The Exercise

### What it models

The exercise models Pub/Sub delivery, the loss when no subscriber is present, and a stream that
persists its history.

### The assertions

```python
assert ps.publish("chat:abc123", "hello") == ["client-1"]
assert ps.publish("chat:empty", "lost") == [], "no subscriber -> lost"
assert stream.read() == ["job-1", "job-2"], "history is available"
```

The loss assertion is the lesson: Pub/Sub drops a message with no listener.

## Real-World Application

- A live chat session using Pub/Sub on `chat:{session_id}` for real-time delivery.
- Cache invalidation signaled over Pub/Sub, where a missed signal is corrected by the TTL.
- Background jobs on a Stream so a worker that was offline reads the jobs it missed.
- An audit event on a Stream so the history is replayable.

## Common Mistakes

1. **Pub/Sub for guaranteed delivery.** Messages are lost.
2. **No channel naming convention.** Channels become unpredictable.
3. **Subscribers that cannot reconnect.** Messages during the gap are lost.
4. **Streams for ephemeral broadcast.** Unnecessary persistence and complexity.
5. **Ignoring the fire-and-forget limitation.** Durable work loses data.
6. **No consumer acknowledgment in streams.** The queue discipline is incomplete.

## Key Takeaways

1. A channel routes messages to subscribers; the channel name follows the key discipline.
2. Publish sends and subscribe registers interest; every current subscriber receives the message.
3. Pub/Sub is fire-and-forget, fine for ephemeral events and wrong for durable work.
4. Streams add persistence and replay, the Redis-side of the queue pattern.
5. The choice is a delivery-guarantee decision, made before choosing the mechanism.

## Self-Check Questions

1. Why is Pub/Sub fine for a live chat but wrong for a background job?
2. What do Streams add over Pub/Sub?
3. How does the channel naming discipline resemble key naming?
4. How do Streams relate to the queue pattern?
5. Why should the delivery guarantee be decided before the mechanism?

## Further Reading / Connections

- Redis 01 to 03 — the other Redis patterns.
- System Design 02 (queues and workflows) — the queue pattern streams implement.
- Data Engineering 04 (checkpointing) — the persistence-and-replay idea.
- `docs/cheat-sheets/qdrant.md` — related infrastructure reference.

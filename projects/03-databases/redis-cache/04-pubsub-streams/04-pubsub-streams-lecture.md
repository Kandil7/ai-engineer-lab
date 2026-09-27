# Redis 04: Pub/Sub and Streams

## 🎯 Topic Overview

Redis Pub/Sub delivers messages to subscribers in real time; Redis Streams
adds persistence and replay. This lecture covers the channel, the
publish/subscribe model, and when streams replace pub/sub.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Publish to a channel and subscribe to it
2. Explain the fire-and-forget nature of Pub/Sub
3. Explain what Streams add
4. Choose Pub/Sub vs Streams
5. Use channels for real-time delivery

---

## 1. The Channel

A channel is a named topic. A publisher sends a message to a channel; every
subscriber of that channel receives it. The channel is the routing key —
`chat:{session_id}` routes a message to the session's subscribers. The
roadmap's exit test: "real-time delivery uses channels."

```
PUBLISH chat:abc123 {message}
SUBSCRIBE chat:abc123
```

## 2. Publish and Subscribe

Publish sends a message to a channel; subscribe registers interest in a
channel. A message published when no subscriber is listening is lost —
Pub/Sub is fire-and-forget. The roadmap's exit test: "messages are
published and subscribed."

## 3. Fire-and-Forget

Pub/Sub does not store messages. A subscriber that is offline misses the
messages published while it was away. This is fine for ephemeral events —
a live chat — and wrong for anything that must be delivered. The roadmap's
exit test: "the fire-and-forget limitation is understood."

## 4. Streams

Streams add persistence and replay: messages are stored, consumers read
them at their own pace, and history is available. A stream is a log, not a
broadcast. The roadmap's exit test: "guaranteed delivery uses streams."

## 5. Choosing

Pub/Sub for ephemeral broadcast: live chat, notifications, cache
invalidation. Streams for guaranteed delivery: jobs, events that must not
be lost, replayable history. The choice is a delivery guarantee decision.

## Common Mistakes

- Pub/Sub for guaranteed delivery (messages lost).
- No channel naming convention.
- Subscribers that cannot reconnect.
- Streams for ephemeral broadcast (overkill).
- Ignoring the fire-and-forget limitation.

## Key Takeaways

1. A channel routes messages to subscribers.
2. Publish sends; subscribe registers interest.
3. Pub/Sub is fire-and-forget.
4. Streams add persistence and replay.
5. The choice is a delivery guarantee decision.
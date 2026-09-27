# Redis 04: Pub/Sub and Streams — Quiz

> **Topic Overview**: The channel, fire-and-forget, and streams.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 10 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**A channel is:**

- A) A cache
- B) A named topic for routing
- C) A key
- D) A stream

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: chat:abc123 routes to the session's subscribers.

</details>

---

### Question 2 — Easy

**Publish:**

- A) Registers interest
- B) Sends a message to a channel
- C) Stores messages
- D) Deletes messages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Every subscriber receives it.

</details>

---

### Question 3 — Easy

**Subscribe:**

- A) Sends a message
- B) Registers interest in a channel
- C) Stores messages
- D) Deletes messages

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The subscriber receives every published message.

</details>

---

### Question 4 — Medium

**Pub/Sub is:**

- A) Persistent
- B) Fire-and-forget
- C) Replayable
- D) Guaranteed

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Messages are not stored.

</details>

---

### Question 5 — Medium

**A subscriber offline during a publish:**

- A) Receives it later
- B) Misses it
- C) Caches it
- D) Replays it

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Fire-and-forget loses it.

</details>

---

### Question 6 — Medium

**Streams add:**

- A) Speed
- B) Persistence and replay
- C) Channels
- D) Subscribers

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Messages are stored and readable later.

</details>

---

### Question 7 — Medium

**A stream is:**

- A) A broadcast
- B) A log
- C) A cache
- D) A channel

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Consumers read at their own pace.

</details>

---

### Question 8 — Hard

**Pub/Sub is right for:**

- A) Jobs that must not be lost
- B) Ephemeral broadcast
- C) Replayable history
- D) Guaranteed delivery

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Live chat, notifications.

</details>

---

### Question 9 — Hard

**Streams are right for:**

- A) Ephemeral broadcast
- B) Guaranteed delivery
- C) Live chat
- D) Cache invalidation

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Jobs and events that must not be lost.

</details>

---

### Question 10 — Hard**

**The choice between Pub/Sub and Streams is a:**

- A) Speed decision
- B) Delivery guarantee decision
- C) Cache decision
- D) Key decision

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Whether messages must be delivered.

</details>

---

## Answer Key

| Q# | Answer | Difficulty |
|----|--------|------------|
| 1 | B | Easy |
| 2 | B | Easy |
| 3 | B | Easy |
| 4 | B | Medium |
| 5 | B | Medium |
| 6 | B | Medium |
| 7 | B | Medium |
| 8 | B | Hard |
| 9 | B | Hard |
| 10 | B | Hard |

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 9-10 | Expert | Redis section complete |
| 7-8 | Proficient | Review streams |
| 5-6 | Developing | Re-study fire-and-forget |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [03 - Rate Limiting](03-rate-limiting-quiz.md)
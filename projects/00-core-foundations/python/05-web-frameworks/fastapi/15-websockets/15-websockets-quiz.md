# FastAPI 15: WebSockets — Quiz

> **Topic Overview**: Bidirectional connections and their costs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is a WebSocket?**
- A) One-way push
- B) A persistent, bidirectional connection over one TCP connection
- C) A cache
- D) A REST verb

<details><summary>Reveal Answer</summary>**B.** Full-duplex.</details>

### Question 2 — Easy
**How does FastAPI declare a socket route?**
- A) `@app.websocket("/ws")`
- B) `@app.get("/ws")`
- C) `@app.ws("/ws")`
- D) `@socket("/ws")`

<details><summary>Reveal Answer</summary>**A.** WebSocket decorator.</details>

### Question 3 — Medium
**What is the main operational cost of WebSockets?**
- A) CPU
- B) Holding many persistent connections consumes memory and file descriptors
- C) Disk
- D) None

<details><summary>Reveal Answer</summary>**B.** Connection state per client.</details>

### Question 4 — Medium
**Why is scaling WebSockets harder than REST?**
- A) It is not
- B) Connections are pinned to a worker; broadcasts need a shared channel (e.g. Redis)
- C) Encryption
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Cross-worker fan-out.</details>

### Question 5 — Medium
**When is SSE a better fit than WebSockets?**
- A) Always
- B) When only the server pushes (token streams), as it is simpler over HTTP
- C) Never
- D) For bidirectional chat

<details><summary>Reveal Answer</summary>**B.** One-way push.</details>

### Question 6 — Hard
**What must you handle for a robust socket?**
- A) Nothing
- B) Disconnects, idle timeouts, heartbeats, and auth on connect
- C) Caching
- D) Sorting

<details><summary>Reveal Answer</summary>**B.** Connection lifecycle.</details>

### Question 7 — Hard
**Why authenticate a WebSocket at connect time?**
- A) Style
- B) The handshake authorizes the channel; tokens can travel in query/subprotocol
- C) For speed
- D) It is not needed

<details><summary>Reveal Answer</summary>**B.** Auth at handshake.</details>

### Question 8 — Hard
**Why can a load balancer break WebSockets?**
- A) It cannot
- B) Without sticky sessions or upgrade support, the connection is dropped or misrouted
- C) It caches
- D) It sorts

<details><summary>Reveal Answer</summary>**B.** Upgrade + affinity.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand WebSockets. |
| 5-6 | Review scaling and auth. |
| < 5 | Re-read the lecture. |

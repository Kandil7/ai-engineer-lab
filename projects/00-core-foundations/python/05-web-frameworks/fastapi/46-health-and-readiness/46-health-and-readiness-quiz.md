# FastAPI 46: Health and Readiness — Quiz

> **Topic Overview**: Liveness, readiness, and dependency-checked probes.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does liveness answer?**
- A) Can I take traffic?
- B) Is the process alive and not deadlocked?
- C) Is the DB up?
- D) Is config valid?

<details><summary>Reveal Answer</summary>**B.** Restart-or-not signal.</details>

### Question 2 — Easy
**What does readiness answer?**
- A) Is the process alive?
- B) Can this instance serve traffic right now?
- C) Is the version correct?
- D) Is the port open?

<details><summary>Reveal Answer</summary>**B.** Traffic-or-not signal.</details>

### Question 3 — Medium
**Why separate the two?**
- A) Style
- B) A starting instance is alive but not ready; restarting it instead of waiting loops forever
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Different reactions.</details>

### Question 4 — Medium
**What must a readiness check verify?**
- A) Nothing
- B) The dependencies it needs: DB, cache, model loaded
- C) The git hash
- D) The logs

<details><summary>Reveal Answer</summary>**B.** Dependency-gated traffic.</details>

### Question 5 — Medium
**What does a failing readiness probe do in Kubernetes?**
- A) Restarts the pod
- B) Removes it from the service endpoints until it recovers
- C) Deletes it
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Shed traffic, not the pod.</details>

### Question 6 — Hard
**Why must health checks be cheap and fast?**
- A) Style
- B) They run constantly; a heavy check becomes the load and can flap under it
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Lightweight pings.</details>

### Question 7 — Hard
**How does graceful shutdown interact with readiness?**
- A) It does not
- B) The pod stops being ready, drains in-flight requests, then exits
- C) It restarts
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Drain before death.</details>

### Question 8 — Hard
**Why version the health response?**
- A) Style
- B) Deploy tooling and clients can confirm the running build during a rollout
- C) Speed
- D) Caching

<details><summary>Reveal Answer</summary>**B.** Observable rollouts.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You probe correctly. |
| 5-6 | Review liveness vs readiness. |
| < 5 | Re-read the lecture. |

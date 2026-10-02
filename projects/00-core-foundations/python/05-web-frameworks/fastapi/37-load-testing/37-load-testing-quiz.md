# FastAPI 37: Load Testing — Quiz

> **Topic Overview**: Percentiles, load models, saturation, and SLO capacity.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why do averages lie about latency?**
- A) They do not
- B) A few slow requests hide inside the mean while users feel the tail
- C) They are slow to compute
- D) They need more samples

<details><summary>Reveal Answer</summary>**B.** The tail is the experience.</details>

### Question 2 — Easy
**What do p50/p95/p99 say?**
- A) Averages
- B) The latency that half, 95%, and 99% of requests beat
- C) Error rates
- D) Throughputs

<details><summary>Reveal Answer</summary>**B.** Distribution cutoffs.</details>

### Question 3 — Medium
**What is an open load model?**
- A) Unlimited users
- B) Requests arrive at a fixed rate regardless of how slow the server gets
- C) A cached test
- D) A unit test

<details><summary>Reveal Answer</summary>**B.** Arrivals independent of completions.</details>

### Question 4 — Medium
**What is a closed load model?**
- A) Same as open
- B) A fixed number of clients each wait for their own response before sending again
- C) A firewall
- D) A cache

<details><summary>Reveal Answer</summary>**B.** Feedback-loop traffic.</details>

### Question 5 — Medium
**What happens at saturation?**
- A) Nothing
- B) Queues grow and latency explodes while throughput flattens
- C) Errors drop
- D) Caching helps

<details><summary>Reveal Answer</summary>**B.** The knee in the curve.</details>

### Question 6 — Hard
**Why test against an SLO, not "as fast as possible"?**
- A) Style
- B) The SLO decides which capacity number ships and which regression blocks
- C) It is faster
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Capacity vs objective.</details>

### Question 7 — Hard
**How do you find the real bottleneck?**
- A) Guess
- B) Hold one resource fixed at a time and watch which relieves the knee
- C) Add workers
- D) Cache everything

<details><summary>Reveal Answer</summary>**B.** Isolate the constraint.</details>

### Question 8 — Hard
**Why can a passing load test still mislead?**
- A) It cannot
- B) Test traffic often differs from production mix, payload size, and data distribution
- C) It is slow
- D) It caches

<details><summary>Reveal Answer</summary>**B.** Representative load matters.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You load-test for decisions. |
| 5-6 | Review percentiles and saturation. |
| < 5 | Re-read the lecture. |

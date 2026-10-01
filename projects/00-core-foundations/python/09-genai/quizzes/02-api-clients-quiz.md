# GenAI 02: API Clients — Quiz

> **Topic Overview**: Calling LLM APIs reliably — retries, timeouts, streaming, and typed errors.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why wrap an LLM provider behind an interface?**
- A) For speed
- B) So the provider is a swappable detail and the app is testable
- C) For security
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Provider-agnostic code stays flexible.</details>

### Question 2 — Easy
**Why set a timeout on every call?**
- A) For accuracy
- B) An un-timed call can hang and wedge the request
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** A timeout bounds the failure.</details>

### Question 3 — Medium
**Which errors are transient and worth retrying?**
- A) Auth errors
- B) Rate limits, timeouts, and 5xx
- C) Validation errors
- D) None

<details><summary>Reveal Answer</summary>**B.** Transient errors deserve backoff retries.</details>

### Question 4 — Medium
**Which errors must not be retried?**
- A) 429
- B) 400 validation and auth errors
- C) Timeouts
- D) 503

<details><summary>Reveal Answer</summary>**B.** They fail the same way every time.</details>

### Question 5 — Medium
**Why use exponential backoff with jitter?**
- A) For speed
- B) To avoid synchronized retry storms when a dependency recovers
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Jitter spreads the retries.</details>

### Question 6 — Hard
**Why stream responses?**
- A) For accuracy
- B) It lowers perceived latency by showing output as it is produced
- C) For cost
- D) It changes the model

<details><summary>Reveal Answer</summary>**B.** TTFT is what the user feels.</details>

### Question 7 — Hard
**Why keep an API key out of source and in the environment?**
- A) For speed
- B) A committed secret is exposed in history forever
- C) For accuracy
- D) It changes behavior

<details><summary>Reveal Answer</summary>**B.** Secrets belong in env/secret stores.</details>

### Question 8 — Hard
**A call succeeds sometimes and hangs other times. First fix?**
- A) Bigger model
- B) A timeout plus a bounded retry, then inspect the timeout rate
- C) Lower temperature
- D) More tokens

<details><summary>Reveal Answer</summary>**B.** Bound the call, then measure.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can call APIs robustly. |
| 5-6 | Review error classes and backoff. |
| < 5 | Re-read the lecture. |

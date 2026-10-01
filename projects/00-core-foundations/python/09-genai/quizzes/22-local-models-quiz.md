# GenAI 22: Local Models — Quiz

> **Topic Overview**: Running models locally with Ollama or vLLM within a VRAM budget.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**Why run a model locally?**
- A) Always faster
- B) Privacy, no per-token cost, and offline operation
- C) Smaller models
- D) No GPU needed

<details><summary>Reveal Answer</summary>**B.** Local has real benefits for the right workload.</details>

### Question 2 — Easy
**What must you budget before loading a local model?**
- A) Disk only
- B) VRAM: weights plus KV cache plus activations plus overhead
- C) Bandwidth
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** Fit is a budget, not a guess.</details>

### Question 3 — Medium
**When does self-hosting beat an API?**
- A) Always
- B) At high steady volume where amortized cost beats per-token billing
- C) At low volume
- D) Never

<details><summary>Reveal Answer</summary>**B.** Break-even depends on utilization.</details>

### Question 4 — Medium
**What is quantization's tradeoff?**
- A) None
- B) Less memory and faster compute for some quality loss
- C) More memory
- D) More accuracy

<details><summary>Reveal Answer</summary>**B.** Measure quality after quantizing.</details>

### Question 5 — Medium
**Why does a model that "fits" at rest still OOM under load?**
- A) It does not
- B) The KV cache and activations grow with context length and concurrency
- C) The GPU is broken
- D) For cost

<details><summary>Reveal Answer</summary>**B.** Budget the peak, not the idle case.</details>

### Question 6 — Hard
**Why measure local latency instead of assuming it is fast?**
- A) Local is always fast
- B) A small local model may be slower than a hosted frontier model at TTFT
- C) For cost
- D) It is fast

<details><summary>Reveal Answer</summary>**B.** Measure, do not assume.</details>

### Question 7 — Hard
**Why expose an OpenAI-compatible API locally?**
- A) For security
- B) The app stays provider-agnostic; only the base URL changes
- C) For speed
- D) It is required

<details><summary>Reveal Answer</summary>**B.** Reversibility via a stable interface.</details>

### Question 8 — Hard
**When is a hosted API the better choice?**
- A) Never
- B) Low or bursty volume, frontier capability, or no GPU-ops capacity
- C) Always
- D) At high volume

<details><summary>Reveal Answer</summary>**B.** Managed scaling can win.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can run local models. |
| 5-6 | Review the VRAM budget and break-even. |
| < 5 | Re-read the lecture. |

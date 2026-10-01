# MLops 15: Cost Optimization — Quiz

> **Topic Overview**: Controlling ML cost across training, storage, and inference.

---

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

---

## Questions

### Question 1 — Easy

**What are the main ML cost drivers?**

- A) Keyboard time
- B) GPU compute, storage, and inference (tokens/requests)
- C) Electricity only
- D) Licenses only

<details><summary>Reveal Answer</summary>

**B.** Compute, storage, and serving.

</details>

### Question 2 — Easy

**Why is cost per request better than cost per token?**

- A) It is smaller
- B) It folds in retries and wasted tokens from wrong answers
- C) It is required
- D) It is the same

<details><summary>Reveal Answer</summary>

**B.** The useful unit is a useful answer.

</details>

### Question 3 — Medium

**How does caching reduce inference cost?**

- A) It changes the model
- B) A cache hit avoids the model call entirely
- C) It compresses the model
- D) It does not

<details><summary>Reveal Answer</summary>

**B.** Hits serve without inference.

</details>

### Question 4 — Medium

**How does batching reduce inference cost?**

- A) It changes the model
- B) It processes several requests per forward pass, raising utilization
- C) It compresses data
- D) It does not

<details><summary>Reveal Answer</summary>

**B.** Better hardware utilization lowers cost per request.

</details>

### Question 5 — Medium

**Why set per-request token/compute limits?**

- A) For accuracy
- B) To bound the cost of a single request and prevent runaway spend
- C) For speed
- D) For security

<details><summary>Reveal Answer</summary>

**B.** Limits cap the tail of spend.

</details>

### Question 6 — Hard

**When does self-hosting beat a per-token API?**

- A) Always
- B) At high steady utilization where the amortized GPU cost is below the API bill
- C) At low utilization
- D) Never

<details><summary>Reveal Answer</summary>

**B.** The break-even depends on volume and utilization.

</details>

### Question 7 — Hard

**Why track cost per useful answer over time?**

- A) For reporting only
- B) It catches regressions (retries, prompt bloat, cache rot) that quietly raise spend
- C) For accuracy
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** The trend reveals cost drift.

</details>

### Question 8 — Hard

**A cheaper model is 10% less accurate. How do you decide?**

- A) Always take cheaper
- B) Weigh the quality loss (measured on the golden set) against the cost saving for the task
- C) Always take accurate
- D) Ignore quality

<details><summary>Reveal Answer</summary>

**B.** The trade is measured on both axes.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can optimize ML cost. |
| 5-6 | Review cost per request and caching. |
| < 5 | Re-read the lecture. |

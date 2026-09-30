# AI Evaluation 07: Production Monitoring — Quiz

> **Topic Overview**: Metrics, alerts, feedback loop, quality drift.

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

**The three production metric groups are:**

- A) Cost, speed, size
- B) Latency, error rate, quality
- C) Input, output, cache
- D) Read, write, delete

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The health of the serving path.

</details>

---

### Question 2 — Easy

**The dashboard displays:**

- A) The cache
- B) Metrics over time
- C) The model
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Latency percentiles, error rate, quality.

</details>

---

### Question 3 — Easy

**Alerts fire when:**

- A) The cache expires
- B) A metric crosses a threshold
- C) The model is loaded
- D) The query is sent

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The signal that something is wrong.

</details>

---

### Question 4 — Medium

**Quality drift is:**

- A) A cache miss
- B) Slow degradation of answer quality over time
- C) A latency spike
- D) A model load

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Detected against the baseline.

</details>

---

### Question 5 — Medium

**The feedback loop turns failures into:**

- A) Cache entries
- B) Test cases in the eval set
- C) Model updates
- D) Alerts

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: User feedback feeds the eval set.

</details>

---

### Question 6 — Medium

**Drift is measured against:**

- A) The cache
- B) The baseline
- C) The model
- D) The query

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The reference quality level.

</details>

---

### Question 7 — Medium

**Without a dashboard, metrics are:**

- A) Tracked
- B) Invisible
- C) Cached
- D) Alerted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: No one sees them.

</details>

---

### Question 8 — Hard

**Monitoring latency but not quality misses:**

- A) Slow responses
- B) Answer degradation
- C) Cache misses
- D) Error rates

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The answer can be fast and wrong.

</details>

---

### Question 9 — Hard

**Without a feedback loop, failures:**

- A) Disappear
- B) Repeat
- C) Are cached
- D) Are alerted

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: The same failure happens again.

</details>

---

### Question 10 — Hard**

**The roadmap's exit test for monitoring is:**

- A) It is ignored
- B) Metrics are tracked and alerts are set
- C) It is cached
- D) It is optional

<details>
<summary>Reveal Answer</summary>

**Correct Answer: B**

**Explanation**: Dashboard, alerts, feedback loop.

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
| 9-10 | Expert | AI-evaluation section complete |
| 7-8 | Proficient | Review drift detection |
| 5-6 | Developing | Re-study the metrics |
| 0-4 | Novice | Restart the lecture |

---

**Previous**: [06 - Eval in CI](06-eval-in-ci-quiz.md)
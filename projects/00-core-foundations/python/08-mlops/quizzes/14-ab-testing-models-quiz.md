# MLops 14: A/B Testing Models — Quiz

> **Topic Overview**: Comparing two model versions online with controlled traffic and a decision rule.

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

**What is an A/B test?**

- A) Two models trained at once
- B) Comparing two variants by splitting live traffic and measuring a metric
- C) A code review
- D) A dataset split

<details><summary>Reveal Answer</summary>

**B.** Controlled online comparison.

</details>

### Question 2 — Easy

**Why randomize traffic?**

- A) For speed
- B) So the groups differ only by the variant, not by traffic composition
- C) For cost
- D) For security

<details><summary>Reveal Answer</summary>

**B.** Randomization isolates the treatment effect.

</details>

### Question 3 — Medium

**What is the primary metric?**

- A) Latency only
- B) The single success metric the test is powered to decide on
- C) Any metric
- D) The model size

<details><summary>Reveal Answer</summary>

**B.** A test decides on one primary metric; others are guardrails.

</details>

### Question 4 — Medium

**Why predefine the sample size?**

- A) For cost
- B) Otherwise peeking biases the result; the test needs enough data to be conclusive
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** Predefining prevents invalid early stopping.

</details>

### Question 5 — Medium

**What is a guardrail metric?**

- A) The primary metric
- B) A metric that must not regress (latency, error rate) while the primary improves
- C) A model metric
- D) A GPU metric

<details><summary>Reveal Answer</summary>

**B.** Guardrails catch a win that costs something unacceptable.

</details>

### Question 6 — Hard

**The variant wins on the primary metric but latency doubles. Ship?**

- A) Yes
- B) Not automatically; the guardrail regression must be weighed as an explicit tradeoff
- C) Ignore latency
- D) Re-run

<details><summary>Reveal Answer</summary>

**B.** Guardrails make the tradeoff explicit.

</details>

### Question 7 — Hard

**What is the novelty effect?**

- A) A permanent gain
- B) A temporary lift from newness that fades; it can make an early result misleading
- C) A latency spike
- D) A data bug

<details><summary>Reveal Answer</summary>

**B.** Run long enough to see past the novelty.

</details>

### Question 8 — Hard

**Why is an offline win not a guarantee of an online win?**

- A) They are identical
- B) The live distribution, feedback loops, and user behavior differ from the offline set
- C) Offline is more accurate
- D) They cannot differ

<details><summary>Reveal Answer</summary>

**B.** Offline is a proxy; online is the ground truth.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run an A/B test. |
| 5-6 | Review guardrails and sample size. |
| < 5 | Re-read the lecture. |

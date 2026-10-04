# MLops 21: Deployment Strategies — Quiz

> **Topic Overview**: Shadow, canary, blue-green, A/B, rollback, and choosing by risk.

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

**What does a shadow deployment do?**

- A) Serves the candidate to 50%
- B) Scores live traffic without serving the candidate
- C) Deploys twice
- D) Tests offline only

<details><summary>Reveal Answer</summary>

**B.** Real inputs, zero user impact.

</details>

### Question 2 — Easy

**What makes blue-green different from canary?**

- A) It is slower
- B) One router switch moves all traffic, and rollback is instant and total
- C) It uses no environments
- D) It never rolls back

<details><summary>Reveal Answer</summary>

**B.** Instant, total reversibility at the price of two environments.

</details>

### Question 3 — Medium

**Why is a canary a loop, not a step?**

- A) It runs forever
- B) The slice expands through gates: 5% → 25% → 50% → 100% with a check each time
- C) It has no gate
- D) It serves everyone

<details><summary>Reveal Answer</summary>

**B.** Each expansion is gated on the comparison.

</details>

### Question 4 — Medium

**What can shadow validate that offline eval cannot?**

- A) Nothing
- B) The real input distribution, train/serve skew, and latency under live load
- C) User satisfaction
- D) Business lift

<details><summary>Reveal Answer</summary>

**B.** But it cannot measure user impact — only serving can.

</details>

### Question 5 — Medium

**When is A/B the right deployment strategy?**

- A) When you need to prove business lift with statistics
- B) When you want the fastest deploy
- C) When risk is zero
- D) Never

<details><summary>Reveal Answer</summary>

**B.** The statistical comparison decides promotion.

</details>

### Question 6 — Hard

**A canary lifts the target metric but breaks a guardrail. Ship it?**

- A) Yes, lift wins
- B) No — a violated guardrail is a failure, not a win
- C) Ship half
- D) Ignore guardrails

<details><summary>Reveal Answer</summary>

**B.** Guardrails exist for exactly this case.

</details>

### Question 7 — Hard

**What is the correct order for a high-risk release?**

- A) Direct deploy
- B) Shadow, then canary, then full
- C) A/B only
- D) Blue-green only

<details><summary>Reveal Answer</summary>

**B.** Validate, bound, then serve.

</details>

### Question 8 — Hard

**How do you choose among the strategies?**

- A) By habit
- B) Risk first, then reversibility, then cost — and test the rollback
- C) Always blue-green
- D) Always direct

<details><summary>Reveal Answer</summary>

**B.** The strategy you pick is the one you live with at 2 a.m.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can ship a model safely. |
| 5-6 | Review shadow vs canary vs blue-green. |
| < 5 | Re-read the lecture. |

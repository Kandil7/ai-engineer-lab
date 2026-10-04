# MLops 20: Continuous Training — Quiz

> **Topic Overview**: Why models degrade, retraining triggers, champion/challenger, and avoiding thrash.

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

**Why do models degrade without any code change?**

- A) GPUs get slower
- B) The data distribution moves (concept, data, or label drift)
- C) The code rots
- D) Seeds expire

<details><summary>Reveal Answer</summary>

**B.** A model is a snapshot of a moment; time changes the distribution.

</details>

### Question 2 — Easy

**What is a retraining trigger?**

- A) A bug
- B) A named condition (schedule, drift, performance, data) that starts a retrain
- C) A GPU alarm
- D) A random timer

<details><summary>Reveal Answer</summary>

**B.** Triggers are recorded for the audit trail.

</details>

### Question 3 — Medium

**What is the difference between champion and challenger?**

- A) The champion is newer
- B) The champion is the live model; the challenger must beat it to promote
- C) They are identical
- D) The challenger is always promoted

<details><summary>Reveal Answer</summary>

**B.** A retrained model is a candidate, not an upgrade.

</details>

### Question 4 — Medium

**What is retrain thrash?**

- A) Fast training
- B) Retraining so often the system promotes noise and burns compute
- C) A data error
- D) A serving outage

<details><summary>Reveal Answer</summary>

**B.** Minimum intervals and cooldowns prevent it.

</details>

### Question 5 — Medium

**Why must a CT retrain be idempotent?**

- A) For speed
- B) A failed retrain must be safely re-runnable without duplicating a registry entry
- C) For cost
- D) It must not

<details><summary>Reveal Answer</summary>

**B.** The same pinned pipeline can run twice safely.

</details>

### Question 6 — Hard

**Why record the trigger reasons for every retrain?**

- A) For the dashboard color
- B) A retrain with no named reason is indistinguishable from thrash in an audit
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>

**B.** Reasons are the audit trail's first line.

</details>

### Question 7 — Hard

**A challenger beats the champion by epsilon on noisy data. Promote?**

- A) Yes, always
- B) No — require significance beyond the eval set's noise, or hold
- C) Flip a coin
- D) Retrain again immediately

<details><summary>Reveal Answer</summary>

**B.** Significance, not epsilon, plus cooldown.

</details>

### Question 8 — Hard

**What must be re-measured on every retrain before promotion?**

- A) Only accuracy
- B) Accuracy, fairness, and resources — the retrained model can regress any of them
- C) Only the loss
- D) Nothing

<details><summary>Reveal Answer</summary>

**B.** A retrain is a new model; gate it like one.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can run continuous training safely. |
| 5-6 | Review triggers and champion/challenger. |
| < 5 | Re-read the lecture. |

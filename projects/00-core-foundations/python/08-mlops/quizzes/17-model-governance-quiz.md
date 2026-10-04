# MLops 17: Model Governance — Quiz

> **Topic Overview**: Fairness, bias detection, explainability, model cards, and wiring governance into the lifecycle.

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

**What is model governance?**

- A) Model training speed
- B) The policies and artifacts that make a model auditable, explainable, and fair
- C) A GPU setting
- D) A serving framework

<details><summary>Reveal Answer</summary>

**B.** Governance is about accountability, not performance.

</details>

### Question 2 — Easy

**Which is NOT a source of bias?**

- A) Historical data
- B) Sampling
- C) Label choice
- D) A fast GPU

<details><summary>Reveal Answer</summary>

**D.** Bias enters via data, sampling, labels, proxies, and measurement.

</details>

### Question 3 — Medium

**Why does dropping the protected attribute not remove bias?**

- A) It does
- B) Neutral features (zip code) act as proxies for the protected attribute
- C) The model memorizes
- D) It slows training

<details><summary>Reveal Answer</summary>

**B.** Proxy features reintroduce the bias you removed.

</details>

### Question 4 — Medium

**What does demographic parity require?**

- A) Equal accuracy for all
- B) Equal positive-decision rate across groups
- C) Equal training time
- D) Equal feature counts

<details><summary>Reveal Answer</summary>

**B.** It measures decision rates, not error rates.

</details>

### Question 5 — Medium

**What is the difference between global and local explainability?**

- A) Global is faster
- B) Global explains the model overall; local explains one decision
- C) Local is for developers only
- D) They are the same

<details><summary>Reveal Answer</summary>

**B.** Local reason codes serve the affected person and regulators.

</details>

### Question 6 — Hard

**Why can you not satisfy all fairness definitions at once?**

- A) They are the same
- B) The impossibility results: when base rates differ, the definitions conflict
- C) The code is hard
- D) Models are random

<details><summary>Reveal Answer</summary>

**B.** There is an explicit trade-off, not a technical solution.

</details>

### Question 7 — Hard

**What makes a model card a governance artifact rather than marketing?**

- A) Its length
- B) A real out-of-scope section that names where the model must not be used
- C) Its color scheme
- D) Its author

<details><summary>Reveal Answer</summary>

**B.** Naming misuse is how governance prevents it.

</details>

### Question 8 — Hard

**What does a fairness gate do in CI?**

- A) Speeds the build
- B) Blocks promotion when a candidate exceeds the fairness threshold or regresses
- C) Trains the model
- D) Serves predictions

<details><summary>Reveal Answer</summary>

**B.** It makes governance automatic, like the eval gate.

</details>

---

## Scoring Guide

| Score | Reading |
|-------|---------|
| 7-8 | You can govern a model end to end. |
| 5-6 | Review the fairness metrics and the trade-off. |
| < 5 | Re-read the lecture. |

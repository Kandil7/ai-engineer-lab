# GenAI 10: Retrieval Quality — Quiz

> **Topic Overview**: Measuring retrieval with recall@k, precision@k, and MRR.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does recall@k measure?**
- A) Ranking quality only
- B) The fraction of relevant passages found in the top k
- C) Noise
- D) Cost

<details><summary>Reveal Answer</summary>**B.** Did we find the material?</details>

### Question 2 — Easy
**What does precision@k measure?**
- A) Coverage
- B) The fraction of the top k that is relevant
- C) Speed
- D) Cost

<details><summary>Reveal Answer</summary>**B.** How much noise did we show?</details>

### Question 3 — Medium
**What does MRR measure?**
- A) Coverage
- B) How high the first relevant passage ranks
- C) Cost
- D) Latency

<details><summary>Reveal Answer</summary>**B.** Reciprocal rank of the first relevant result.</details>

### Question 4 — Medium
**High recall, low MRR diagnoses what?**
- A) Missing material
- B) Found but ranked low — a ranking problem
- C) High cost
- D) No problem

<details><summary>Reveal Answer</summary>**B.** Ranking, not retrieval.</details>

### Question 5 — Medium
**Low recall diagnoses what?**
- A) Ranking
- B) Missing material — the retriever must improve
- C) Noise
- D) Cost

<details><summary>Reveal Answer</summary>**B.** Coverage failed.</details>

### Question 6 — Hard
**Why report recall and precision together?**
- A) They are the same
- B) Each hides what the other shows
- C) For speed
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Together they localize the failure.</details>

### Question 7 — Hard
**Why set thresholds from a baseline?**
- A) For speed
- B) The CI gate needs a floor derived from measured behavior
- C) For cost
- D) It is optional

<details><summary>Reveal Answer</summary>**B.** Without a baseline the gate has no teeth.</details>

### Question 8 — Hard
**Which metric for a single-answer verse lookup?**
- A) Precision@k only
- B) MRR
- C) Recall@100
- D) Accuracy

<details><summary>Reveal Answer</summary>**B.** Position of the one right answer matters.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can measure retrieval. |
| 5-6 | Review the three metrics. |
| < 5 | Re-read the lecture. |

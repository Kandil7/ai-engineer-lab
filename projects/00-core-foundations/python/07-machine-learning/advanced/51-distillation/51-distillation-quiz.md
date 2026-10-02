# ML 51: Knowledge Distillation — Quiz

> **Topic Overview**: Soft labels, temperature, dark knowledge, KL loss, and
> the compression toolbox.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does distillation transfer from teacher to student?**
- A) The teacher's weights
- B) The teacher's soft prediction distributions
- C) The teacher's architecture
- D) The training data

<details><summary>Reveal Answer</summary>**B.** The student imitates softened outputs, not just labels.</details>

### Question 2 — Easy
**What is a soft label?**
- A) A one-hot vector
- B) A full per-class probability distribution
- C) A binary label
- D) A text description

<details><summary>Reveal Answer</summary>**B.** The teacher's confidence structure.</details>

### Question 3 — Medium
**What does a temperature T > 1 do?**
- A) Sharpens the distribution
- B) Softens the distribution, exposing secondary structure
- C) Changes the number of classes
- D) Adds noise

<details><summary>Reveal Answer</summary>**B.** It exposes the dark knowledge.</details>

### Question 4 — Medium
**What is dark knowledge?**
- A) Knowledge from dark mode
- B) The information in the non-argmax probabilities
- C) Hidden weights
- D) The bias term

<details><summary>Reveal Answer</summary>**B.** The confusability structure a hard label hides.</details>

### Question 5 — Medium
**Why scale the KL loss by T²?**
- A) To match the gradient magnitude of the temperature-scaled loss
- B) It is a typo
- C) To increase the temperature
- D) To reduce overfitting

<details><summary>Reveal Answer</summary>**A.** T² rescales the gradient correctly.</details>

### Question 6 — Hard
**Why serve the student at T = 1 after training at T > 1?**
- A) T > 1 flattens confidence and hurts calibration at serving time
- B) T = 1 is faster
- C) T > 1 uses more memory
- D) They are equivalent

<details><summary>Reveal Answer</summary>**A.** Train softened, serve sharp.</details>

### Question 7 — Hard
**When is distillation not worth it?**
- A) When the teacher is barely better than the student
- B) When the teacher is huge
- C) When the student is small
- D) Always worth it

<details><summary>Reveal Answer</summary>**A.** No teacher advantage, nothing to transfer.</details>

### Question 8 — Hard
**How do distillation, pruning, and quantization compose?**
- A) They are mutually exclusive
- B) Distill to a small model, then prune and quantize it
- C) Quantize first, always
- D) Prune only

<details><summary>Reveal Answer</summary>**B.** Knowledge, redundancy, and representation — three orthogonal levers.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You distill efficiently. |
| 5-6 | Review temperature and dark knowledge. |
| < 5 | Re-read the lecture. |

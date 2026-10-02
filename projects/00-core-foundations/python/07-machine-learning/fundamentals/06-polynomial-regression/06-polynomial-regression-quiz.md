# ML 06: Polynomial Regression — Quiz

> **Topic Overview**: Curved fits, complexity, and the bias-variance tradeoff.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does polynomial regression add to linear?**
- A) Clusters
- B) Powers of the feature (x², x³, …)
- C) Classes
- D) Weights only

<details><summary>Reveal Answer</summary>**B.** Curvature via features.</details>

### Question 2 — Easy
**Is polynomial regression still "linear" in the model sense?**
- A) No
- B) Yes; it is linear in the coefficients it learns
- C) It is nonlinear in coefficients
- D) It is a tree

<details><summary>Reveal Answer</summary>**B.** Linear in parameters.</details>

### Question 3 — Medium
**What happens as the degree increases without limit?**
- A) Always better
- B) The model overfits, wiggling through noise
- C) It clusters
- D) It clips

<details><summary>Reveal Answer</summary>**B.** High variance.</details>

### Question 4 — Medium
**What is underfitting?**
- A) Too much flexibility
- B) Too little flexibility; the model misses real structure
- C) Perfect fit
- D) No data

<details><summary>Reveal Answer</summary>**B.** High bias.</details>

### Question 5 — Medium
**How do you choose the degree?**
- A) Always highest
- B) Cross-validation or a held-out set, balancing train and validation error
- C) Randomly
- D) By speed

<details><summary>Reveal Answer</summary>**B.** Tune complexity by validation.</details>

### Question 6 — Hard
**What does regularisation do to a high-degree fit?**
- A) Removes it
- B) Adds a penalty on large coefficients, shrinking the wiggles
- C) Sorts
- D) Encodes

<details><summary>Reveal Answer</summary>**B.** Ridge/Lasso control variance.</details>

### Question 7 — Hard
**What is the bias-variance tradeoff?**
- A) Both low is bad
- B) More flexibility lowers bias but raises variance; balance via validation
- C) They are independent
- D) Only bias matters

<details><summary>Reveal Answer</summary>**B.** The central tension.</details>

### Question 8 — Hard
**Why can extrapolation with a high-degree polynomial be wild?**
- A) It cannot
- B) High powers amplify far outside the training range
- C) It clips
- D) It clusters

<details><summary>Reveal Answer</summary>**B.** Unstable outside support.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand polynomial fits. |
| 5-6 | Review overfitting and the tradeoff. |
| < 5 | Re-read the lecture. |

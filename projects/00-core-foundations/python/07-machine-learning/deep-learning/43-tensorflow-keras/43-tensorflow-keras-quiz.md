# ML 43: TensorFlow and Keras — Quiz

> **Topic Overview**: Declarative vs explicit, Sequential vs Functional API,
> compile/fit, SavedModel, and framework choice.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What style does Keras use?**
- A) Explicit loop
- B) Declarative (describe the model, framework runs the loop)
- C) Symbolic only
- D) Imperative only

<details><summary>Reveal Answer</summary>**B.** Keras abstracts the training loop behind `fit`.</details>

### Question 2 — Easy
**What does `compile` do?**
- A) Runs training
- B) Binds optimizer, loss, and metrics
- C) Saves the model
- D) Loads data

<details><summary>Reveal Answer</summary>**B.** Configures, does not run.</details>

### Question 3 — Medium
**When is the Functional API required over Sequential?**
- A) For any model
- B) For branched, merged, or shared-layer graphs
- C) For linear stacks
- D) For regression only

<details><summary>Reveal Answer</summary>**B.** Sequential only expresses straight-line stacks.</details>

### Question 4 — Medium
**What is a callback?**
- A) A loss function
- B) A hook into the training loop (EarlyStopping, checkpoint)
- C) An optimizer
- D) A layer

<details><summary>Reveal Answer</summary>**B.** Loop control without writing the loop.</details>

### Question 5 — Medium
**What is a SavedModel?**
- A) A checkpoint of weights only
- B) A self-describing graph-plus-weights bundle for serving
- C) A CSV export
- D) A TensorBoard log

<details><summary>Reveal Answer</summary>**B.** A portable serving artifact.</details>

### Question 6 — Hard
**Which framework is the default for research and LLM tooling?**
- A) Keras
- B) PyTorch
- C) TensorFlow Lite
- D) Neither

<details><summary>Reveal Answer</summary>**B.** Novel loops and LLM code are overwhelmingly PyTorch.</details>

### Question 7 — Hard
**Why would a team pick TensorFlow/Keras over PyTorch?**
- A) Keras models are always faster
- B) TF serving ecosystem and low-ceremony standard tasks
- C) PyTorch cannot do regression
- D) Keras is the only option for CNNs

<details><summary>Reveal Answer</summary>**B.** The choice is ecosystem and ergonomics, not capability.</details>

### Question 8 — Hard
**What is the single most important mapping between the frameworks?**
- A) Dense vs Linear names
- B) `fit` versus the hand-written training loop
- C) The import statement
- D) The seed function

<details><summary>Reveal Answer</summary>**B.** That one abstraction is the whole ergonomics difference.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can read both frameworks. |
| 5-6 | Review Sequential vs Functional and compile/fit. |
| < 5 | Re-read the lecture. |

# ML 44: JAX and Flax — Quiz

> **Topic Overview**: Functional view, jit/grad/vmap, Flax init/apply, and
> PyTorch-vs-JAX tradeoffs.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**In JAX, what is the model's parameters?**
- A) Hidden object state
- B) A plain value passed into a pure function
- C) A global variable
- D) A database record

<details><summary>Reveal Answer</summary>**B.** Parameters are an external value; the model is a pure function.</details>

### Question 2 — Easy
**What does `jax.jit` do?**
- A) Trains the model
- B) Compiles a function to fast device code
- C) Loads data
- D) Saves the model

<details><summary>Reveal Answer</summary>**B.** Trace once, compile, reuse the kernel.</details>

### Question 3 — Medium
**What does `jax.grad` differentiate with respect to by default?**
- A) The second argument
- B) The first argument
- C) All arguments
- D) Nothing

<details><summary>Reveal Answer</summary>**B.** The first argument, unless `argnums` says otherwise.</details>

### Question 4 — Medium
**What does `jax.vmap` replace?**
- A) A Python loop with a vectorized kernel
- B) A loss function
- C) A compiler
- D) A device

<details><summary>Reveal Answer</summary>**A.** It lifts a function over a batch axis.</details>

### Question 5 — Medium
**What is Flax's init/apply split for?**
- A) Separating data from labels
- B) Keeping the module pure: init makes params, apply runs the forward pass
- C) Splitting training from testing
- D) Separating CPU from GPU

<details><summary>Reveal Answer</summary>**B.** Purity lets the same function be transformed freely.</details>

### Question 6 — Hard
**Why do JAX's transforms compose so cleanly?**
- A) Because the model is a pure function of its parameters
- B) Because JAX is faster
- C) Because it uses GPUs
- D) Because it is object-oriented

<details><summary>Reveal Answer</summary>**A.** Purity makes jit(vmap(grad(...))) a valid expression.</details>

### Question 7 — Hard
**When is JAX's advantage most decisive?**
- A) For TPU-scale, XLA-compiled, massively parallel workloads
- B) For a single small CPU model
- C) For dynamic control flow
- D) For legacy Keras serving

<details><summary>Reveal Answer</summary>**A.** pmap across TPUs and composed transforms.</details>

### Question 8 — Hard
**What is the honest default for a full-stack AI engineer?**
- A) JAX for everything
- B) PyTorch as the workhorse; JAX when transforms/TPU scale are the bottleneck
- C) Never use JAX
- D) Only Flax

<details><summary>Reveal Answer</summary>**B.** Learn the ideas; adopt JAX where it pays.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You grasp the functional-transform model. |
| 5-6 | Review jit/grad/vmap and init/apply. |
| < 5 | Re-read the lecture. |

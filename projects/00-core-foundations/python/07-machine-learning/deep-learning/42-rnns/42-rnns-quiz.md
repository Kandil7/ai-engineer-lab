# ML 42: Recurrent Neural Networks — Quiz

> **Topic Overview**: Recurrence, sequence shaping, vanishing gradients,
> LSTM/GRU gating, and RNN-vs-transformer.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What does an RNN carry forward between steps?**
- A) The loss
- B) A hidden state
- C) The batch
- D) The learning rate

<details><summary>Reveal Answer</summary>**B.** The running summary of the sequence so far.</details>

### Question 2 — Easy
**What tensor layout does batch_first=True use?**
- A) (seq, batch, features)
- B) (batch, seq_len, features)
- C) (features, batch, seq)
- D) (batch, features, seq)

<details><summary>Reveal Answer</summary>**B.** (batch, seq_len, features).</details>

### Question 3 — Medium
**What is the vanishing gradient problem?**
- A) Gradients grow to infinity
- B) Gradients shrink geometrically across long sequences
- C) The loss becomes zero
- D) The model overfits

<details><summary>Reveal Answer</summary>**B.** Multiplied across steps, the gradient approaches zero.</details>

### Question 4 — Medium
**How does the LSTM fix the vanishing gradient?**
- A) By using larger batches
- B) The cell state is updated by addition, giving the gradient a highway
- C) By removing tanh
- D) By using more layers

<details><summary>Reveal Answer</summary>**B.** Additive updates let the gradient flow without vanishing.</details>

### Question 5 — Medium
**Which is the lighter alternative to LSTM?**
- A) RNN
- B) GRU
- C) Transformer
- D) CNN

<details><summary>Reveal Answer</summary>**B.** GRU has two gates and no separate cell state.</details>

### Question 6 — Hard
**What is the RNN's cost in the sequence length?**
- A) O(seq²)
- B) O(seq) time with O(1) state
- C) O(seq³)
- D) O(log seq)

<details><summary>Reveal Answer</summary>**B.** Linear time, constant state — the streaming advantage.</details>

### Question 7 — Hard
**When would you choose an RNN over a transformer?**
- A) For a compact, low-latency streaming model
- B) For the longest possible context
- C) Always
- D) Never

<details><summary>Reveal Answer</summary>**A.** Constant memory fits streaming and on-device constraints.</details>

### Question 8 — Hard
**Which hidden representation is the classic choice for sequence classification?**
- A) The mean of all outputs
- B) The final hidden state
- C) The first output
- D) A random step

<details><summary>Reveal Answer</summary>**B.** The final hidden state summarizes the whole sequence.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand recurrence and gating. |
| 5-6 | Review vanishing gradients and LSTM/GRU. |
| < 5 | Re-read the lecture. |

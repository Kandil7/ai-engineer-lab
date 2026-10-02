# ML 41: Convolutional Neural Networks — Quiz

> **Topic Overview**: Convolution, stride/padding, pooling, channels, receptive
> field, and the conv classifier stack.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What are the two inductive biases of a CNN?**
- A) Depth and width
- B) Translation invariance and locality
- C) Attention and masking
- D) Batch and epoch

<details><summary>Reveal Answer</summary>**B.** Shared weights (invariance) and small kernels (locality).</details>

### Question 2 — Easy
**What is a filter/kernel?**
- A) A data row
- B) A small learned weight matrix slid across the input
- C) A pooling window
- D) A loss function

<details><summary>Reveal Answer</summary>**B.** The learned pattern detector.</details>

### Question 3 — Medium
**A 28×28 input through a 3×3 kernel with no padding produces what output size?**
- A) 28
- B) 26
- C) 30
- D) 24

<details><summary>Reveal Answer</summary>**B.** `out = 28 - 3 + 1 = 26`.</details>

### Question 4 — Medium
**Why does a CNN have far fewer parameters than a dense layer on the same input?**
- A) It drops features
- B) Filter weights are shared across all positions
- C) It is quantized
- D) It uses pooling only

<details><summary>Reveal Answer</summary>**B.** One filter's weights serve the whole image.</details>

### Question 5 — Medium
**What does max pooling primarily provide?**
- A) More channels
- B) Downsampling and small-shift invariance
- C) Gradient clipping
- D) Label smoothing

<details><summary>Reveal Answer</summary>**B.** Keeps strong activations, discards exact location.</details>

### Question 6 — Hard
**What is the receptive field?**
- A) The number of filters
- B) The input region that influences one output neuron
- C) The batch size
- D) The learning rate range

<details><summary>Reveal Answer</summary>**B.** Grows with depth and kernel size.</details>

### Question 7 — Hard
**Why are two stacked 3×3 convs often preferred over one 5×5 conv?**
- A) Same receptive field with fewer parameters and more non-linearity
- B) They are faster to write
- C) They remove the need for pooling
- D) They use less memory in all cases

<details><summary>Reveal Answer</summary>**A.** Two 3×3 = one 5×5 field, cheaper and deeper.</details>

### Question 8 — Hard
**Where do parameters concentrate in a typical CNN classifier?**
- A) The conv layers
- B) The dense head after flattening
- C) The pooling layers
- D) The activation functions

<details><summary>Reveal Answer</summary>**B.** Flattening into a Linear layer spikes the count.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You understand the convolution stack. |
| 5-6 | Review stride/padding and receptive field. |
| < 5 | Re-read the lecture. |

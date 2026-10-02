# ML 49: Quantization — Quiz

> **Topic Overview**: Affine quantization, round-trip error, PTQ vs QAT,
> symmetric/asymmetric, INT8/INT4.

## Score Tracker

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 8 |
| Correct Answers | 0 |
| Score | 0% |

## Questions

### Question 1 — Easy
**What is the affine mapping for quantization?**
- A) x -> float
- B) q = round(x/s + z), back via x_hat = (q - z)*s
- C) x -> one-hot
- D) x -> log scale

<details><summary>Reveal Answer</summary>**B.** Scale and zero-point map float to integer.</details>

### Question 2 — Easy
**What does PTQ stand for?**
- A) Post-training quantization
- B) Pre-training quantization
- C) Parallel training quantization
- D) Partial training quantization

<details><summary>Reveal Answer</summary>**A.** Quantize after training, no retrain.</details>

### Question 3 — Medium
**Why is QAT needed when PTQ hurts accuracy?**
- A) QAT is cheaper
- B) Training with fake quantization makes the model robust to rounding
- C) QAT is faster
- D) QAT removes weights

<details><summary>Reveal Answer</summary>**B.** The model learns weights that survive quantization.</details>

### Question 4 — Medium
**Why does INT4 have more error than INT8?**
- A) Fewer buckets means a coarser step size
- B) INT4 is slower
- C) INT8 uses a different algorithm
- D) INT4 has no zero-point

<details><summary>Reveal Answer</summary>**A.** 15 buckets vs 255 buckets.</details>

### Question 5 — Medium
**What is the memory win of INT8 over FP32?**
- A) 1/2
- B) 1/4
- C) 1/8
- D) No change

<details><summary>Reveal Answer</summary>**B.** 8 bits vs 32 bits = 1/4 the size.</details>

### Question 6 — Hard
**When is asymmetric quantization preferred over symmetric?**
- A) For one-sided activation ranges (e.g. ReLU outputs)
- B) Always
- C) Never
- D) For tiny models

<details><summary>Reveal Answer</summary>**A.** A real zero-point fits skewed ranges without wasting buckets.</details>

### Question 7 — Hard
**Why measure end-to-end accuracy, not weight round-trip error?**
- A) Round-trip error is the wrong metric; accuracy on real data is what matters
- B) Accuracy is faster to compute
- C) Round-trip error is always zero
- D) They are identical

<details><summary>Reveal Answer</summary>**A.** Weight error ignores activation outliers and the real task.</details>

### Question 8 — Hard
**Which part of the quantization win is unconditional?**
- A) Speed
- B) Memory size
- C) Accuracy
- D) None

<details><summary>Reveal Answer</summary>**B.** Smaller always; speed needs hardware support.</details>

## Scoring Guide
| Score | Reading |
|-------|---------|
| 7-8 | You can quantize safely. |
| 5-6 | Review PTQ vs QAT and INT8/INT4. |
| < 5 | Re-read the lecture. |

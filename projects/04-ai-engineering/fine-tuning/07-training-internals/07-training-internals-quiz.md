# Fine-Tuning 07: LLM Training Internals — Quiz

> **Topic Overview**: The six-stage training step, the memory budgets under
> it, and the discipline that keeps every reported number honest.

---

## Questions

### Question 1
**Difficulty:** Easy

**Which is the correct order of the six stages of one training step?**

- A) Forward, loss, backward, optimizer step, scheduler step, zero-grad
- B) Forward, backward, loss, scheduler step, optimizer step, zero-grad
- C) Loss, forward, backward, scheduler step, optimizer step, zero-grad
- D) Forward, backward, optimizer step, loss, scheduler step, zero-grad

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** One optimizer step runs forward, loss, backward, optimizer,
scheduler, zero-grad, and every hyperparameter maps to exactly one of those
stages. Gradient clipping sits between backward and the optimizer step, so
the optimizer only ever sees capped gradients.

</details>

---

### Question 2
**Difficulty:** Easy

**Why must a fine-tune use the base model's exact tokenizer and chat template?**

- A) Tokenizers are faster than raw strings
- B) Token IDs index the embedding table, and role markers must become the same tokens at train and inference
- C) Chat templates reduce memory usage
- D) Special tokens are only needed for padding

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Token IDs are indices into the base model's embedding
table, so a foreign vocabulary looks up wrong embeddings and trains garbage.
The chat template must match too, so role markers become the same tokens at
train and inference.

</details>

---

### Question 3
**Difficulty:** Easy

**In SFT label construction, what does setting prompt-token labels to `-100` do?**

- A) Marks the tokens as padding for the optimizer
- B) Retrains the embedding rows for those tokens
- C) Excludes those positions from the cross-entropy loss
- D) Truncates the sequence at the prompt boundary

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** `-100` is cross-entropy's `ignore_index`, so only answer
tokens contribute gradients. Without masking, the model spends capacity
learning to predict the user's question, the one text you never want it to
generate on its own.

</details>

---

### Question 4
**Difficulty:** Easy

**A run uses micro-batch 2, gradient accumulation 8, and one GPU. What is the effective batch size?**

- A) 2
- B) 8
- C) 16
- D) 32

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** Effective batch is micro-batch times accumulation times
devices: 2 x 8 x 1 = 16, while peak memory only ever sees 2 sequences. The
scheduler also steps once per optimizer step, so accumulation 8 means 8x
fewer schedule steps for the same data.

</details>

---

### Question 5
**Difficulty:** Medium

**AdamW keeps how many bytes of optimizer state per trainable parameter?**

- A) 4 bytes
- B) 8 bytes
- C) 16 bytes
- D) 32 bytes

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Two fp32 moments, the mean of gradients and the mean of
squared gradients, cost 8 bytes per trainable parameter on top of the
weights. At 7B that is 56 GB of moments alone, which is why full
fine-tuning exceeds 100 GB while QLoRA's adapter state is a few hundred MB.

</details>

---

### Question 6
**Difficulty:** Medium

**Which learning-rate configuration is correct for a full fine-tune of a 7B model?**

- A) Peak 2e-5, warmup ratio 0.05, learning rate held at peak until the end
- B) Peak 5e-4, no warmup, constant learning rate
- C) Peak 2e-4, warmup ratio 0.05, cosine decay to near zero
- D) Peak 2e-5, warmup ratio 0.05, cosine decay to near zero

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation:** Full fine-tuning sits in the 5e-6 to 1e-4 band, so 2e-5 is
right, while 2e-4 belongs to the LoRA/QLoRA band of 5e-5 to 1e-3. Warmup
ramps linearly because Adam's moments are uncalibrated at step 1, and cosine
decay lets the model settle instead of oscillating at peak.

</details>

---

### Question 7
**Difficulty:** Medium

**Which statement about 16-bit training on the RTX 5000 (compute capability sm_75) is correct?**

- A) bf16 uses native tensor cores on Turing and needs no scaler
- B) fp16 has fp32's exponent range, so no loss scaler is needed
- C) bf16 has no native tensor cores on sm_75, and fp16 needs a loss scaler to prevent underflow
- D) Both formats run identically on every GPU from sm_70 onward

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** bf16 tensor cores start at Ampere sm_80, so on Turing a
bf16 request errors out or falls back to slower fp32 paths. fp16 gradients
below about 6e-8 underflow to zero, so GradScaler scales the loss before
backward and unscales before clipping and the optimizer step.

</details>

---

### Question 8
**Difficulty:** Medium

**Training loss keeps falling while eval loss starts rising. What is the diagnosis and the first response?**

- A) Overfitting: stop at the eval-loss minimum and consider weight decay or more clean data
- B) Underfitting: raise the learning rate immediately
- C) Healthy: the gap shows the model is specializing
- D) Data leakage: delete the eval set and retrain

<details>
<summary>View Answer</summary>

**Correct Answer:** A

**Explanation:** Rising eval loss against falling train loss is the
overfitting signature, so stop at the eval-loss minimum before the gap
widens. Underfitting looks different, both losses stuck high, and is treated
with a higher LR within the band, higher rank, or more steps.

</details>

---

### Question 9
**Difficulty:** Medium

**What is the correct split and decontamination discipline before training?**

- A) Train first, then carve an eval set from the leftovers
- B) Split train, validation, and test from the raw set before any augmentation, then deduplicate across the splits
- C) Shuffle the raw set and reuse the same file for train and eval
- D) Decontaminate only against external benchmarks you plan to ignore

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Split before you train, because validation selects
checkpoints and detects overfitting while test is touched once at the end.
Exact dedup plus fingerprint near-dedup then catches the paraphrase clusters
that leak eval items into train.

</details>

---

### Question 10
**Difficulty:** Medium

**Which checkpoint should be shipped?**

- A) The last checkpoint of the run
- B) The checkpoint with the lowest training loss
- C) The checkpoint saved at the highest learning rate
- D) The checkpoint with the best held-out metric, keeping the last one for rollback

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation:** Eval loss bottoms out before the final step, so the last
checkpoint is usually past the minimum and the lowest train-loss save is the
most overfit one. Select on a held-out metric and keep the best plus the
last so an interruption does not lose the run.

</details>

---

### Question 11
**Difficulty:** Hard

**For 7B full fine-tuning in mixed precision, which term dominates the training-state memory?**

- A) fp16 weights at 14 GB
- B) fp16 gradients at 14 GB
- C) AdamW moments at 56 GB
- D) Activations at batch 2 and sequence length 2048

<details>
<summary>View Answer</summary>

**Correct Answer:** C

**Explanation:** AdamW's two fp32 moments cost 8 bytes per trainable
parameter, which is 56 GB at 7B and dwarfs the 14 GB weights and 14 GB
gradients, with 28 GB of master weights on top. The sum exceeds 100 GB,
while QLoRA's adapter-only state lands near 5-6 GB on the same card.

</details>

---

### Question 12
**Difficulty:** Hard

**How is catastrophic forgetting detected, and what is the cheapest mitigation?**

- A) From the fine-tune's own eval loss; mitigate by raising the LoRA rank
- B) From a regression suite run on the base model and the candidate; mitigate first with a lower learning rate and fewer epochs
- C) From training-loss spikes; mitigate by adding a loss scaler
- D) From the checkpoint count; mitigate by saving fewer checkpoints

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** The fine-tune's own eval loss stays happy while
unreinforced capabilities drift away, so only a fixed regression suite
reveals the damage. The cheapest forgetting tax is a smaller update: lower
LR and fewer epochs first, then LoRA, then mixing in general data.

</details>

---

### Question 13
**Difficulty:** Hard

**How do DPO and RLHF differ on the preference-tuning ladder?**

- A) DPO trains a separate reward model; RLHF does not
- B) DPO needs no reward model and optimizes chosen-versus-rejected pairs against a frozen reference, while RLHF trains a reward model and runs PPO with a KL penalty
- C) RLHF is cheaper because it skips the reference model
- D) SFT is the last rung, and DPO replaces it entirely

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** SFT is rung one at 1x cost; DPO adds no reward model and
pushes chosen answers up against rejected ones relative to a frozen
reference; RLHF trains a reward model and runs PPO with a KL penalty at
5-10x the cost. Climb only after SFT and data quality have plateaued.

</details>

---

### Question 14
**Difficulty:** Hard

**What must you do after merging two LoRA adapters?**

- A) Nothing: merging is exact arithmetic, so the result is at least as good as either adapter
- B) Retrain the base model to absorb the merge
- C) Increase the LoRA rank of both adapters before merging
- D) Evaluate on the golden set, because merging is arithmetic, not evaluation, and interfering adapters merge silently into a worse model

<details>
<summary>View Answer</summary>

**Correct Answer:** D

**Explanation:** Linear interpolation, task arithmetic, and DARE are all
arithmetic on weight deltas and raise no error when adapters interfere
through overlapping regions of weight space. The merged model can be
confidently broken, so re-evaluate on the golden set before shipping.

</details>

---

### Question 15
**Difficulty:** Hard

**Before choosing rank, learning rate, or batch size, which two questions must be answerable?**

- A) Which dataset is largest, and which GPU is cheapest
- B) What specific failure in the baseline am I fixing, and which held-out metric proves the fix
- C) Which LoRA config won the last benchmark, and how many epochs is typical
- D) How low can the training loss go, and how fast can the run finish

<details>
<summary>View Answer</summary>

**Correct Answer:** B

**Explanation:** Every knob is justified only relative to a named baseline
failure and a proving metric on a held-out golden set; without them, "which
LoRA config is best" is unanswerable in the abstract. If you cannot state
both, the right move is another hour of failure analysis, not a training
run.

</details>

---

## Scoring Guide

| Score | Rating | Recommendation |
|-------|--------|----------------|
| 13-15 | Expert | Ready for training data |
| 10-12 | Proficient | Review the memory arithmetic |
| 7-9 | Developing | Re-study the training step |
| 0-6 | Novice | Restart the lecture |

---

## Score Tracking

| Metric | Value |
|--------|-------|
| Questions Answered | 0 / 15 |
| Correct Answers | 0 |
| Score | 0% |

---

## Answer Key

| Question | Answer | Difficulty |
|----------|--------|------------|
| 1 | A | Easy |
| 2 | B | Easy |
| 3 | C | Easy |
| 4 | C | Easy |
| 5 | B | Medium |
| 6 | D | Medium |
| 7 | C | Medium |
| 8 | A | Medium |
| 9 | B | Medium |
| 10 | D | Medium |
| 11 | C | Hard |
| 12 | B | Hard |
| 13 | B | Hard |
| 14 | D | Hard |
| 15 | B | Hard |

---

**Previous**: [06 - RAG vs Fine-Tuning](../06-rag-vs-fine-tuning/06-rag-vs-fine-tuning-quiz.md)

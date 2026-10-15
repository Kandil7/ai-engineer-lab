# Fine-Tuning 07: LLM Training Internals — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| AdamW | Adam with decoupled weight decay; two fp32 moments per parameter | 8 bytes/param of optimizer state |
| Autocast | Scoped automatic mixed precision in PyTorch | forward in fp16 under `autocast` |
| Effective batch size | micro-batch × accumulation × devices | 2 × 8 × 1 = 16 |
| Catastrophic forgetting | Fine-tuning erodes capabilities the task data never reinforced | regression suite catches it |
| Checkpoint selection | Picking the best save by a held-out metric, not train loss | min eval loss, keep best and last |
| Cross-entropy loss | Negative log-likelihood of the next token | the SFT objective |
| Decontamination | Removing eval leakage from train | exact + near-dedup across splits |
| DPO | Preference optimization without a separate reward model | (prompt, chosen, rejected) pairs |
| Gradient accumulation | Several micro-batches before one optimizer step | simulate batch 16 on 16 GB |
| Gradient clipping | Cap gradient norm before the optimizer step | `max_norm=1.0` |
| Gradient checkpointing | Recompute activations in backward; trade compute for memory | required for 7B on 16 GB |
| Learning rate schedule | LR as a function of step: warmup then decay | cosine to ~0 over total steps |
| Loss scaling | Multiply loss so fp16 gradients avoid underflow | `GradScaler`, fp16 only |
| Mixed precision | fp16/bf16 compute with fp32 master weights | halves activation memory |
| Optimizer state | Adam's running moments stored per parameter | the hidden VRAM term |
| Overfitting | Train loss falls while held-out loss rises | early stop at the minimum |
| Prompt masking | Loss ignored on prompt tokens (`-100`) | train only on answer tokens |
| Regression suite | Fixed general-capability checks run pre/post | catches catastrophic forgetting |
| RLHF | Reward model + PPO with KL penalty to a reference | the expensive top rung |
| Tokenizer mismatch | IDs from the wrong vocabulary | never swap a base model's tokenizer |
| Underfitting | Both train and held-out loss stuck high | raise LR/rank, train longer |
| Warmup | Linear LR ramp at the start of training | 3-5% of total steps as a ratio |
| Weight decay | Decoupled L2-style shrinkage in AdamW | 0.0 to 0.1, default 0.01 |
| Task vector / merging | θ_tuned − θ_base added or interpolated | DARE, linear adapter merge |

---

## Detailed Definitions

### AdamW

**Definition:** The default optimizer for fine-tuning. Adam tracks a first moment `m`
(mean of gradients) and a second moment `v` (mean of squared gradients) per parameter;
AdamW adds **decoupled weight decay** so the decay step `(1 - lr * wd)` is applied
directly to the weights rather than mixed into the gradient. Both moments are stored in
fp32: **8 bytes of optimizer state per trainable parameter**, the hidden cost that
dominates full fine-tuning memory.

**Example:**
```python
# 7B trainable parameters => 56 GB of AdamW moments alone
# QLoRA adapters ~20M params => ~0.16 GB
optimizer = AdamW(trainable_params, lr=2e-4, weight_decay=0.01)
```

**Related concepts:** Optimizer state, Weight decay, Memory budget

---

### Autocast

**Definition:** PyTorch's scoped automatic mixed precision. Inside the context manager,
eligible ops run in fp16 (or bf16) and the framework keeps fp32 master weights for the
optimizer. It replaces manual casting of every layer.

**Example:**
```python
with torch.cuda.amp.autocast(dtype=torch.float16):
    loss = model(**batch).loss  # matmuls in fp16
```

**Related concepts:** Mixed precision, Loss scaling

---

### Catastrophic forgetting

**Definition:** The erosion of capabilities during fine-tuning when updates move weights
away from regions that supported behaviors the new task never reinforced. The fine-tune's
own eval loss stays happy; only a general-capability regression suite reveals the loss.

**Example:**
```python
# task metric up, general suite down => a tradeoff, not a win
candidate_score, regressions = evaluate_with_suite(candidate, base_suite)
```

**Related concepts:** Regression suite, LoRA (frozen base reduces the risk)

---

### Checkpoint selection

**Definition:** Choosing which saved weights to keep or ship by ranking checkpoints on a
**held-out** metric (eval loss or task metric), never on training loss. The last
checkpoint is usually past the minimum. Keep the best (to ship) and the last (to resume).

**Example:**
```python
best = min(checkpoints, key=lambda c: c.eval_loss)  # not c.train_loss
```

**Related concepts:** Overfitting, Evaluation discipline

---

### Cross-entropy loss

**Definition:** The SFT objective. At each answer position, the loss is the negative
log-probability the model assigned to the actual next token: `L = -log P(token | context)`.
Lower loss means the model assigns higher probability to the training targets — which
is not the same as better task behavior.

**Example:**
```python
loss = F.cross_entropy(logits.view(-1, vocab), labels.view(-1), ignore_index=-100)
```

**Related concepts:** Prompt masking, Overfitting

---

### Decontamination

**Definition:** Removing any train example that overlaps — exactly or nearly — with an
evaluation item, before training. Leakage turns eval scores into a measure of memorized
test answers. Combine exact dedup with near-dedup (MinHash, embedding similarity), and
split before augmenting.

**Example:**
```python
if fingerprint(train_row) ~near(fingerprint(eval_row)):
    drop_or_reassign(train_row)   # paraphrases count as leakage too
```

**Related concepts:** Evaluation discipline, Splits (train/val/test)

---

### DPO (Direct Preference Optimization)

**Definition:** Preference tuning that skips the separate reward-model stage. Trains on
(prompt, chosen, rejected) triples with a loss that pushes chosen answers up and rejected
answers down relative to a **frozen reference model**. One forward-backward per step;
cheaper and stabler than RLHF, but it needs trustworthy preference pairs.

**Example:**
```json
{"prompt": "...", "chosen": "answer A with citations", "rejected": "answer B without"}
```

**Related concepts:** RLHF, SFT (always rung one)

---

### Effective batch size

**Definition:** The number of sequences whose gradients contribute to one optimizer
step: `micro_batch × gradient_accumulation × device_count`. Peak memory sees only the
micro-batch; the optimizer sees the effective batch. Record it in the run config;
changing it invalidates an unexamined learning rate.

**Example:**
```python
effective = micro_batch * grad_accum * devices  # 2 * 8 * 1 = 16
```

**Related concepts:** Gradient accumulation, Learning rate schedule

---

### Gradient accumulation

**Definition:** Running several forward-backward passes while accumulating gradients,
then applying one optimizer step. The standard way to reach a useful effective batch on
a small GPU. The scheduler still steps once per optimizer step, so total steps must be
planned in optimizer steps, not micro-batches.

**Example:**
```python
for i, batch in enumerate(loader):
    loss = model(**batch).loss / accum
    loss.backward()  # gradients accumulate
    if (i + 1) % accum == 0:
        optimizer.step()
        scheduler.step()
        optimizer.zero_grad(set_to_none=True)
```

**Related concepts:** Effective batch size, Memory budget

---

### Gradient clipping

**Definition:** Rescaling the gradient vector so its global norm does not exceed a cap
(typically `max_norm=1.0`), applied **after** backward and **before** the optimizer
step. It exists because one poisoned batch or an fp16 anomaly can produce a spike that
destroys the weights in a single update. With a loss scaler, unscale before clipping.

**Example:**
```python
torch.nn.utils.clip_grad_norm_(model.parameters(), max_norm=1.0)
```

**Related concepts:** Loss scaling, Training step pipeline

---

### Gradient checkpointing

**Definition:** Discarding most intermediate activations after the forward pass and
recomputing them during backward. Costs roughly 30% more compute and cuts activation
memory by a large factor. Usually mandatory for 7B-class training on 16 GB.

**Example:**
```python
model.gradient_checkpointing_enable()  # Hugging Face trainers
```

**Related concepts:** Memory budget, Gradient accumulation

---

### Learning rate schedule

**Definition:** The LR as a function of optimizer step — almost always a linear warmup
to a peak, then cosine or linear decay toward zero or a small floor. Warmup protects the
early steps when Adam's moments are uncalibrated; decay lets the model settle. The
schedule is defined in optimizer steps, so accumulation changes its wall-clock meaning.

**Example:**
```python
lr(step) = peak * step / warmup                      # during warmup
lr(step) = peak * 0.5 * (1 + cos(pi * progress))     # cosine decay after
```

**Related concepts:** Warmup, Effective batch size

---

### Loss scaling

**Definition:** Multiplying the loss by a large factor (e.g., 2^12) before the backward
pass so small gradients land in fp16's representable range instead of underflowing to
zero. `GradScaler` adjusts the factor dynamically and skips steps on inf/NaN. Needed for
**fp16 only**; bf16's exponent range makes it unnecessary.

**Example:**
```python
scaler = GradScaler()
scaler.scale(loss).backward()
scaler.step(optimizer)
scaler.update()
```

**Related concepts:** Mixed precision, Autocast

---

### Memory budget

**Definition:** The full pre-run accounting: `weights + gradients + optimizer state +
activations + overhead`. For 7B full FT over 100 GB (impossible on 16 GB); for 7B QLoRA
about 5-6 GB. Budget before launching; an OOM at step 40 means the arithmetic was wrong,
not that luck ran out.

**Example:**
```python
total = weights_gb + grads_gb + optim_gb + acts_gb + OVERHEAD_GB  # compare to 16.0
```

**Related concepts:** Optimizer state, Gradient checkpointing, QLoRA

---

### Mixed precision

**Definition:** Computing forward/backward in fp16 or bf16 while keeping fp32 master
weights for the optimizer update. Halves activation and gradient memory and engages
tensor cores. On Turing (sm_75) the correct choice is fp16 plus a loss scaler; bf16
tensor cores exist only from Ampere sm_80.

**Example:**
```python
# RTX 5000 (sm_75): fp16 + GradScaler, not bf16
```

**Related concepts:** Autocast, Loss scaling

---

### Optimizer state

**Definition:** The per-parameter memory an optimizer keeps beyond the weights — for
AdamW, two fp32 moments (`m` and `v`), 8 bytes per trainable parameter. It is the hidden
VRAM cost of fine-tuning: negligible under QLoRA (adapters only), prohibitive for full
fine-tuning (56 GB of moments for 7B). Paged optimizers can offload it to CPU RAM.

**Example:**
```python
optim_gb = trainable_params_b * 8  # AdamW moments, bytes/param -> GB
```

**Related concepts:** AdamW, Memory budget

---

### Overfitting

**Definition:** Memorizing the training strings instead of generalizing. Detected by
**eval loss rising while train loss falls** (or by task metrics plateauing) on a
held-out split. Remedies: early stopping at the eval minimum, lower rank, weight decay,
more clean data, fewer epochs. On small instruction sets it is the default failure mode.

**Example:**
```python
overfit = train_loss < 0.05 and eval_loss > train_loss * 3
```

**Related concepts:** Checkpoint selection, Data quality

---

### Prompt masking

**Definition:** Setting the loss to be ignored on prompt positions (labels `-100`,
PyTorch cross-entropy's `ignore_index`) so gradients come only from answer tokens.
Without it the model trains to predict the user's question — capacity spent on the
wrong target. Non-negotiable in SFT.

**Example:**
```python
labels = [-100] * len(prompt_ids) + answer_ids
```

**Related concepts:** Cross-entropy loss, Chat template

---

### Regression suite

**Definition:** A small fixed set of general-capability checks — out-of-domain
formatting, known-answer questions, safety probes — run on the base model and every
fine-tuned candidate. The only reliable detector of catastrophic forgetting, because the
fine-tune's own eval loss cannot see it.

**Example:**
```python
base = run_suite(base_model)
cand = run_suite(candidate)
flag = [k for k in base if cand[k] < base[k] - TOLERANCE]
```

**Related concepts:** Catastrophic forgetting, Evaluation discipline

---

### RLHF

**Definition:** Reinforcement learning from human feedback: train a reward model on
preference pairs, then optimize the policy with PPO against that reward plus a
KL-penalty to a frozen reference. The top rung of the cost ladder (often 5-10× SFT) and
the hardest to stabilize. Worth it when preference quality is the product; almost never
the first tool.

**Example:**
```python
# reward = reward_model(x, y) - beta * kl(policy || reference)
```

**Related concepts:** DPO, SFT

---

### Splits (train / validation / test)

**Definition:** Partitioning raw data **before** any augmentation. Train feeds gradients;
validation selects checkpoints and tunes hyperparameters; test is touched once at the
end. A re-split without a new data version silently invalidates every prior comparison.

**Example:**
```python
train, val, test = split(raw, [0.9, 0.05, 0.05], seed=42, stratify=None)
```

**Related concepts:** Decontamination, Checkpoint selection

---

### Tokenizer mismatch

**Definition:** Feeding token IDs that do not belong to the base model's vocabulary, or
training with a chat template different from the one used at inference. IDs are indices
into the embedding table; the wrong vocabulary indexes the wrong embeddings. The
tokenizer travels with the model and is part of the training-inference contract.

**Example:**
```python
# always: tokenizer = AutoTokenizer.from_pretrained(BASE); apply its chat template
enc = tokenizer.apply_chat_template(messages, return_tensors="pt")
```

**Related concepts:** Chat template, Vocabulary coverage

---

### Underfitting

**Definition:** Both train and held-out loss stuck high; the model has not learned the
task. Causes: LR too low, LoRA rank too low, too few steps, or insufficient capacity.
Remedy: raise LR within the method's band, raise rank, train longer. Less common than
overfitting on small instruction sets.

**Example:**
```python
underfit = train_loss > 3.0 and abs(eval_loss - train_loss) < 0.1
```

**Related concepts:** Learning rate schedule, Rank (LoRA)

---

### Warmup

**Definition:** The initial phase of the schedule where LR ramps linearly from 0 (or a
small value) to the peak. It protects early steps when gradients are noisy and Adam's
moments are uncalibrated — a large step 1 can diverge permanently. Express it as a ratio
of total steps (3-5% typical for fine-tuning), not an absolute count.

**Example:**
```python
warmup_steps = int(total_steps * warmup_ratio)  # 0.03 * 1000 = 30 steps
```

**Related concepts:** Learning rate schedule, Effective batch size

---

### Weight decay

**Definition:** Regularization that multiplies weights by `(1 - lr * wd)` each step,
pulling them toward zero. In AdamW the decay is decoupled from the gradient (unlike
L2-in-gradient "Adam with L2"). Typical fine-tuning range 0.0-0.1; too much decay on
small adapters shrinks them into noise.

**Example:**
```python
optimizer = AdamW(params, lr=2e-4, weight_decay=0.01)
```

**Related concepts:** AdamW, Overfitting

---

### Task vector / model merging

**Definition:** Representing a fine-tune as `θ_tuned − θ_base` (a task vector) and
combining vectors or LoRA adapters by linear interpolation, scaled addition, or DARE
(drop-and-rescale of delta parameters). Merging is arithmetic, not evaluation: it can
silently produce a model worse than either part. Always re-eval on the golden set after
any merge.

**Example:**
```python
merged_lora = alpha * adapter_A + beta * adapter_B  # then evaluate
```

**Related concepts:** LoRA, Evaluation discipline

---

### Vocabulary coverage

**Definition:** How efficiently the base tokenizer represents your domain text. Poor
coverage splits domain terms into many rare subwords, inflating sequence length, context
budget, and training time. Measure before training: tokenize a corpus sample and inspect
tokens-per-word against general text.

**Example:**
```python
ratio = len(tokenizer.encode(sample)) / len(sample.split())
# 1.3 is typical English; 2.5+ on domain text is a warning
```

**Related concepts:** Tokenizer mismatch, Memory budget (activations scale with length)

---

## Related Concepts

- **SFT (topic 01)**: the behavior-shaping method whose internals this topic opens up
- **LoRA/QLoRA (topic 02)**: the parameter-efficient methods that make the memory
  arithmetic of Section 8 work on 16 GB
- **Training data (topic 03)**: where decontamination and the quality-over-quantity rule
  are executed
- **Training runs (topic 04)**: where these settings become a recorded config
- **Model registry (topic 05)**: where checkpoint selection results are versioned
- **Transformers from scratch** (`projects/00-core-foundations/python/07-machine-learning/deep-learning/40-transformers-from-scratch/`):
  attention internals, linked forward, not re-taught here
- **Neural-net foundations** (`projects/04-ai-engineering/fastai-deep-learning/lectures/03-neural-net-foundations-lecture.md`):
  SGD and backprop from first principles

## Key Takeaways

1. The training step is forward, loss, backward, optimizer, scheduler, zero-grad — and
   every hyperparameter maps to one stage.
2. AdamW's 8 bytes of state per trainable parameter is the hidden VRAM cost; it is why
   QLoRA fits 16 GB and full 7B fine-tuning does not.
3. Warmup-then-decay with a method-appropriate peak LR is the default schedule;
   effective batch is micro × accum × devices.
4. On Turing sm_75, use fp16 with a loss scaler; bf16 needs Ampere sm_80.
5. Mask the prompt, split and decontaminate before training, select checkpoints on a
   held-out metric, and evaluate after every merge.
6. The failure-first rule: name the baseline failure and the proving metric before
   choosing any LoRA config.

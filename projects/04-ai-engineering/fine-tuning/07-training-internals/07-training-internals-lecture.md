# Fine-Tuning 07: LLM Training Internals

## Topic Overview

Fine-Tuning 01 through 06 taught what to train, on what data, and how to version the
result. This lecture opens the training loop itself. A training step is a fixed
pipeline: forward pass, loss, backward pass, optimizer step, scheduler step, zero-grad.
Every hyperparameter you have ever set — learning rate, batch size, warmup, precision —
is a knob on one stage of that pipeline, and misconfiguring any of them wastes GPU-hours
or produces numbers nobody can trust.

Underneath the loop sit four budgets that decide whether a run is even possible: the
memory for weights, gradients, optimizer states, and activations. On a 16 GB card those
budgets are tight enough that the arithmetic matters before the run, not after the
out-of-memory crash. Mixed precision, gradient accumulation, gradient checkpointing, and
QLoRA are all answers to the same question: how do you fit a 7B model's training state
into 16 GB.

This lecture covers the step pipeline end to end, tokenization at the training level,
cross-entropy loss and prompt masking, AdamW's hidden memory cost, learning-rate warmup
and decay, gradient accumulation math, fp16 versus bf16 on Turing hardware, full memory
accounting, overfitting and catastrophic forgetting, the SFT-to-DPO-to-RLHF ladder,
decontamination, checkpoint selection, evaluation discipline, and model merging. The
running theme is the engineering rule from the end of the lecture: never fine-tune
without a named baseline failure and a metric that proves the fix.

**Duration:** 4-5 hours
**Difficulty:** Intermediate
**Prerequisites:** Fine-Tuning 01 (SFT) and 02 (LoRA/QLoRA); neural-net foundations
(SGD, backprop); basic Python

---

## Learning Objectives

By the end of this lecture, you will be able to:

1. **Trace** a single training step through forward, loss, backward, optimizer,
   scheduler, and zero-grad.
2. **Verify** that a tokenizer, chat template, and special tokens match the base model
   before training starts.
3. **Compute** cross-entropy loss on answer tokens only and explain prompt masking.
4. **Account** for AdamW optimizer state as the hidden VRAM cost of fine-tuning.
5. **Design** a warmup-then-decay learning-rate schedule and pick a peak LR for full
   fine-tuning versus LoRA.
6. **Calculate** the effective batch size from micro-batch, accumulation, and devices.
7. **Choose** fp16 versus bf16 given the GPU's compute capability, and explain why
   Turing needs a loss scaler.
8. **Budget** total training memory — weights, gradients, optimizer, activations — before
   launching a run on a 16 GB card.
9. **Diagnose** overfitting, underfitting, and catastrophic forgetting from train/eval
   curves and regression suites.
10. **Decide** when SFT is enough and when preference tuning (DPO/RLHF) is worth the
    cost, and select checkpoints on held-out metrics.

---

## Key Concepts

### 1. The Training Step Pipeline

One optimizer step is six ordered stages. Frameworks hide them behind `trainer.train()`,
but every one of them is present, and every hyperparameter maps to exactly one stage:

```
batch of tokenized examples
        │
        ▼
┌───────────────────┐
│ 1. FORWARD        │  logits = model(input_ids, attention_mask)
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 2. LOSS           │  L = cross_entropy(logits, labels)   # prompt masked (-100)
└─────────┬─────────┘
          ▼
┌───────────────────┐
│ 3. BACKWARD       │  grads = ∂L/∂θ   (autograd; clip grads if max_norm set)
└─────────┬─────────┘
          ▼
┌───────────────────────┐
│ 4. OPTIMIZER STEP     │  θ ← AdamW(θ, grads, state)   # consumes optimizer state
└─────────┬─────────────┘
          ▼
┌───────────────────────┐
│ 5. SCHEDULER STEP     │  lr ← schedule(global_step)   # warmup, then decay
└─────────┬─────────────┘
          ▼
┌───────────────────┐
│ 6. ZERO GRAD      │  grads ← 0   (or set_to_none=True)
└───────────────────┘
```

Two details people get wrong:

- **Gradient clipping happens between stage 3 and stage 4**, before the optimizer sees
  the gradients. `clip_grad_norm_(params, max_norm=1.0)` rescales the whole gradient
  vector when its norm exceeds the cap. It exists because a single bad batch —
  especially in fp16 — can produce a gradient spike large enough to destroy weeks of
  learned weights in one update.
- **The scheduler steps once per optimizer step, not per micro-batch.** With gradient
  accumulation of 8, you run eight forward-backward passes and one optimizer-scheduler
  step. The schedule's total is counted in optimizer steps, which is why accumulation
  changes how long warmup lasts in wall-clock terms.

The exercise `07-training-internals.py` validates the configuration around this
pipeline — accumulation, precision, LR bands, warmup, masking, memory, splits, and
checkpoint metric — before you spend a GPU-hour.

### 2. Tokenization and Vocabulary

The tokenizer is part of the model, not a preprocessing detail. Four rules decide
whether your training run means anything:

1. **The tokenizer must be the base model's exact tokenizer.** Token IDs are indices
   into the embedding table. Feeding IDs from a different vocabulary looks up the wrong
   embeddings and trains garbage. Never swap tokenizers without reinitializing the
   embedding layer, which is effectively pretraining again.
2. **The chat template must match at training and inference.** Fine-Tuning 01 covered
   the contract; at the training level it means the dataset is rendered through
   `tokenizer.apply_chat_template(...)` before tokenization, so role markers
   (`<|user|>`, `<|assistant|>`) become real tokens in the sequence.
3. **Special tokens change the embedding table.** Adding new special tokens requires
   `model.resize_token_embeddings(len(tokenizer))`. Fresh rows are randomly initialized;
   if you train without enough steps to learn them, the new tokens are noise. Prefer the
   base model's existing special tokens unless you have a real reason.
4. **Padding and truncation have side effects.** Decoder-only models are trained with
   right padding typically, and loss on padding positions must be masked (labels =
   -100). Truncation defaults matter: truncating from the right chops off the end of the
   answer — the exact tokens you need the loss on. For SFT, check that no example loses
   its answer to `max_length`, or truncate the prompt side instead.

Vocabulary coverage is the quiet failure: domain text that the base tokenizer splits
into many rare subwords inflates sequence length, burns context budget, and slows
training. Before a run, tokenize a sample of your corpus and look at the token-to-word
ratio. A jump from ~1.3 to ~2.5 tokens per word on domain text is a signal the model's
vocabulary is a poor fit and sequences will be longer than you budgeted.

### 3. Loss: Cross-Entropy and Prompt Masking

SFT is next-token prediction with cross-entropy loss. For each position, the model
emits a distribution over the vocabulary; the loss is the negative log-likelihood of the
actual next token:

```
L = -(1/N) Σ log P(token_t | tokens_<t)
```

The critical training-level detail is **which positions carry loss**. The sequence is
`[prompt tokens] + [answer tokens]`. If loss is computed on the whole sequence, the
model spends capacity learning to predict the user's question — text you never want it
to generate. Prompt masking sets prompt positions to `-100` (PyTorch cross-entropy's
`ignore_index`) so only answer tokens contribute gradients:

```python
# prompt = [101, 102, 103]  answer = [201, 202, 203]
labels = [-100, -100, -100, 201, 202, 203]
# loss is computed on 3 answer tokens, not 6 sequence positions
```

**A falling loss curve is not a quality curve.** Training loss measures how well the
model fits the training strings, including their quirks and errors. It can fall toward
zero on 200 memorized examples while the model gets worse at the task. The honest
signals are eval loss on a held-out set and task metrics on a golden set. Treat training
loss as a smoke detector — NaN or explosion means stop — not as a leaderboard.

### 4. Optimizer States: The Hidden VRAM Cost

SGD without momentum has no memory: it needs only the gradients. Adam and AdamW keep
two running moments per parameter — the first moment `m` (mean of gradients) and the
second moment `v` (mean of squared gradients) — both typically stored in fp32. That is
**8 bytes of optimizer state per trainable parameter**, on top of the parameters
themselves:

| Item | Bytes per param | 7B params |
|---|---|---|
| Weights (fp16) | 2 | 14 GB |
| Gradients (fp16) | 2 | 14 GB |
| AdamW moments `m` + `v` (fp32) | 8 | 56 GB |
| fp32 master weights (mixed precision) | 4 | 28 GB |

The optimizer state is the cost people forget, and it is why full fine-tuning a 7B model
needs more than 100 GB of training state and is impossible on a 16 GB card. Under QLoRA
the trainable parameters are the adapters only (~0.1% of the model), so the 8
bytes/param applies to a few tens of millions of parameters — a few hundred MB, not 56
GB. Paged optimizers (bitsandbytes) can move optimizer state to CPU RAM and page it
back on demand, trading speed for the last few gigabytes of headroom.

Two related knobs:

- **Weight decay** (AdamW, not classic Adam) decays weights toward zero by a factor
  `(1 - lr * wd)` each step, decoupled from the gradient magnitude. It is a
  regularizer; typical values are 0.0 to 0.1 for fine-tuning, and 0.01 is a common
  default. Too much decay on a small fine-tune shrinks the adapters into uselessness.
- **Gradient clipping** (`max_norm=1.0` typically) caps the gradient norm before the
  optimizer step. It is the seatbelt against loss spikes; without it, one poisoned
  batch or an fp16 underflow can derail the whole run.

### 5. Learning Rate Schedules

The learning rate is the single most consequential hyperparameter after the data
itself. The standard schedule is **warmup then decay**:

```
lr
peak ┤        ╭──────────╮
     │       ╱            ╲
     │      ╱              ╲
     │     ╱                ╲
   0 ┤────╱                  ╲───
     0    warmup           cosine/linear decay
          steps            to ~0 or 10% of peak
```

**Why warmup matters.** At step 1, Adam's moments are zero and the gradient estimates
are noisy. A large step this early can throw the weights into a region of the loss
surface the model never recovers from — the classic "loss spike at step 30" that forces
a restart. Warmup ramps the LR linearly from 0 (or a small fraction) to the peak over
the first 1-10% of total steps. A warmup ratio of 0.03-0.05 is a safe default for
fine-tuning; 0.10 is common for pretraining-scale runs.

**Decay shapes the end of the run.** Cosine decay drops the LR following a half-cosine
curve to near zero; linear decay drops it linearly. Both let the model settle into a
minimum instead of oscillating around it at full peak LR forever.

**Typical peak LR bands:**

| Method | Peak LR band | Common default |
|---|---|---|
| Full fine-tuning (7B) | 5e-6 to 1e-4 | 2e-5 |
| LoRA / QLoRA | 5e-5 to 1e-3 | 1e-4 to 2e-4 |

Full fine-tuning moves every weight, so the safe LR is small; LoRA moves a tiny
low-rank subspace and tolerates (and usually needs) a higher LR. The schedule interacts
with total steps: warmup of "30 steps" means something different at 500 total steps
than at 50,000. Express warmup as a ratio and let the trainer convert it.

### 6. Gradient Accumulation

You cannot always fit the batch size you want. Gradient accumulation simulates a large
batch from small ones: run several forward-backward passes, keep accumulating gradients,
then apply one optimizer step.

```
effective_batch = micro_batch × grad_accum × device_count
```

Example: micro-batch 2, accumulation 8, one GPU → effective batch 16, while peak memory
only ever sees 2 sequences at a time. On a 16 GB card this is the standard way to reach
batch 16 or 32 for a 7B QLoRA run.

Two consequences people miss:

- **Fewer optimizer steps per epoch.** With the same epochs and data, accumulation 8
  means 8× fewer scheduler steps. Either raise total steps accordingly or accept a
  shorter schedule; otherwise warmup and decay compress into a handful of updates.
- **LR scaling.** The classical linear scaling rule (Goyal et al.: multiply LR by k when
  batch grows by k) is calibrated for SGD on images and is only weak guidance for
  AdamW fine-tuning. What is true: the LR you picked for effective batch 32 does not
  silently transfer to effective batch 4. If you change the effective batch, re-check
  the LR band from Section 5 and record the effective batch in the run config
  (Fine-Tuning 04).

Gradient accumulation reduces peak activation memory; it does not reduce the memory of
weights, gradients, or optimizer state, which are batch-size independent.

### 7. Mixed Precision on Turing

Mixed precision runs the forward and backward passes in 16-bit while keeping an fp32
master copy of the weights for the optimizer update. It roughly halves activation and
gradient memory and, on GPUs with tensor cores, substantially speeds up matmuls. The
two 16-bit formats differ in one engineering-critical way:

| | fp16 | bf16 |
|---|---|---|
| Mantissa bits | 10 | 7 |
| Exponent bits | 5 (same as fp32) | 8 (same as fp32) |
| Dynamic range | narrow — small gradients underflow to zero | wide — same range as fp32 |
| Loss scaling needed? | **Yes** | No |
| Tensor cores | sm_70+ (Volta and later) | **sm_80+ (Ampere and later)** |

**fp16 needs a loss scaler.** Gradients smaller than ~6e-8 underflow to zero in fp16.
`GradScaler` multiplies the loss by a scale factor (e.g., 2^12) before backward so
gradients land in fp16's representable range, then unscales them before the optimizer
step. If infs/NaNs appear, the scaler halves the scale and skips the step. This machinery
is why bf16 is preferred where it exists — bf16's fp32-width exponent makes underflow a
non-issue, and no scaler is required.

**The hardware fact for this workstation:** the NVIDIA Quadro RTX 5000 is a Turing GPU
(compute capability sm_75). It has fp16 tensor cores but **no native bf16 tensor
cores** — bf16 support starts at Ampere (sm_80). Requesting bf16 on sm_75 does not get
you native tensor-core speed; PyTorch either errors or silently falls back to fp32
paths, which are slower and defeat the purpose. On this machine the correct choice is
**fp16 + autocast + GradScaler**. The exercise flags `bf16` on an sm_75 device with no
fallback as TRN002.

PyTorch usage in one snippet:

```python
from torch.cuda.amp import autocast, GradScaler

scaler = GradScaler()
for batch in loader:
    optimizer.zero_grad(set_to_none=True)
    with autocast(dtype=torch.float16):  # forward in fp16
        loss = model(**batch).loss
    scaler.scale(loss).backward()  # scaled backward
    scaler.unscale_(optimizer)  # unscale before clipping
    torch.nn.utils.clip_grad_norm_(model.parameters(), 1.0)
    scaler.step(optimizer)  # skip step on inf/NaN
    scaler.update()
    scheduler.step()
```

### 8. Memory Accounting

Before any run, sum the training-state terms. All figures below are for a 7B model on
this workstation's 16 GB budget:

```
total = weights + gradients + optimizer + activations + overhead
```

| Term | Full FT (fp16 mixed) | QLoRA (4-bit base) |
|---|---|---|
| Weights | 14 GB (fp16) | ~3.5 GB (4-bit frozen base) |
| Gradients | 14 GB (all params) | ~0.05 GB (adapters only) |
| Optimizer (AdamW moments) | 56 GB | ~0.2 GB (adapters only) |
| fp32 master weights | 28 GB | ~0.1 GB (adapters only) |
| Activations (batch 2, seq 2048) | several GB | ~0.4 GB with checkpointing |
| **Total (ballpark)** | **>100 GB** | **~5-6 GB** |

The arithmetic is why full fine-tuning of a 7B model does not fit 16 GB, and why QLoRA
is the default on this machine. The two memory levers that trade time for space:

- **Gradient checkpointing** discards most intermediate activations and recomputes
  them during the backward pass. It costs roughly 30% more compute and cuts activation
  memory by a large factor — usually required for 7B on 16 GB.
- **Gradient accumulation** caps how many sequences' activations are live at once
  (Section 6). It does not shrink weights, gradients, or optimizer state.

Budget before the run. An out-of-memory at step 40 means the budget was wrong, and the
fix is arithmetic — fewer sequences per micro-batch, shorter `max_seq_len`, checkpointing
on — not luck. The exercise computes this estimate and raises TRN006 when the total
exceeds the budget. Cloud-hybrid workflow applies here: unit-test the config locally,
then run the real GPU training on Colab T4 or Vast.ai where a longer schedule is
affordable.

### 9. Overfitting, Underfitting, and the Data-Quality Trap

Diagnosis is two curves and one table:

| Signal | Underfitting | Healthy | Overfitting |
|---|---|---|---|
| Train loss | stuck high | falling | near zero |
| Eval loss | stuck high, tracks train | falling, tracks train | **rising while train falls** |
| Train vs eval gap | small, both bad | small, both good | large and growing |
| Task metrics | weak | improving | plateau or regress |

- **Underfitting:** LR too low, rank too low, too few steps, or the model simply lacks
  capacity for the task. Raise LR within the band, raise LoRA rank, train longer.
- **Overfitting:** too many epochs on too few examples, rank too high, LR schedule that
  never decays. Stop at the eval-loss minimum (early stopping), lower the rank, add
  weight decay, or get more clean data.

**The data-quality trap.** A clean small set beats a noisy large one, and the margin
widens as noise grows: SFT imitates the data, so wrong answers are learned as right
ones, mixed formats become a mixed-format model, and duplicates over-weight one
pattern. 200 audited examples routinely beat 2,000 scraped ones. Before tuning any
hyperparameter, audit the data (Fine-Tuning 03): dedup, filter, and fix answers. Most
"the loss curve looks wrong" incidents are data incidents wearing a hyperparameter
costume.

### 10. Catastrophic Forgetting

Instruction tuning shifts weights toward the narrow distribution of your task data, and
capabilities that were never reinforced drift away. A model that fine-tunes beautifully
on 500 citation-formatting examples can get worse at arithmetic, multilingual chat, or
refusals — because those behaviors lived in regions of weight space the update moved
through.

**How you notice:** not from the fine-tune's eval loss, which looks great. You notice
from a **regression suite** — a small fixed set of general-capability checks (formatting
on out-of-domain prompts, a few known-answer questions, safety probes) run on the base
model and the fine-tuned candidate. A candidate that wins on the task metric and loses
on the regression suite is a tradeoff, not a win.

**Mitigations, cheapest first:**

1. **Lower LR and fewer epochs.** The cheapest forgetting tax is a smaller update.
2. **LoRA instead of full FT.** Frozen base weights preserve the general behavior by
   construction; a lower rank regularizes the adapter further.
3. **Mix general data into the SFT set.** Even 10-30% general instruction data
   (chat, reasoning, code — whatever the base was good at) acts as a replay buffer.
4. **Explicit replay:** re-include examples from capabilities you must not lose.
5. **Lower LoRA rank / fewer target modules** if regression persists.

Full fine-tuning is the highest-forgetting-risk method; QLoRA with a low rank is the
lowest. This is a primary reason this workstation defaults to QLoRA beyond just memory.

### 11. SFT vs DPO vs RLHF

Three rungs on one ladder. Each rung optimizes a different objective and costs more:

| | SFT | DPO | RLHF (PPO) |
|---|---|---|---|
| Optimizes | likelihood of target answers | preference between chosen/rejected answers | reward model + KL-to-reference |
| Data format | (prompt, gold answer) | (prompt, chosen, rejected) | prompts; preferences go to the reward model |
| Extra models | none | frozen reference model | reward model + reference model |
| Training complexity | one forward-backward | one forward-backward, richer loss | RL loop: sample, score, update — unstable, many knobs |
| Relative cost | 1× | ~1-2× | ~5-10×+ |
| Failure mode | mimicry of data style | over-preference for chosen style | reward hacking, KL collapse |

**What each is for:**

- **SFT** teaches format, tone, domain phrasing — behavior that can be demonstrated with
  gold answers. It is always rung one.
- **DPO** (Direct Preference Optimization) skips the separate reward-model training and
  optimizes a classification-style loss that pushes chosen answers up and rejected
  answers down relative to a frozen reference. You need real preference pairs: human or
  synthetic rankings of two answers to the same prompt.
- **RLHF** trains a reward model on preferences, then optimizes the policy with PPO
  against that reward plus a KL penalty to the reference. It is the right tool when
  preference quality is the product and you can afford the infra.

**When preference tuning is worth it:** when SFT has plateaued on a held-out preference
metric — style calibration, refusal quality, helpfulness-vs-brevity tradeoffs — and you
have a trustworthy preference dataset. **When SFT + better data already wins:** almost
always first. The majority of "we need RLHF" complaints are actually data-quality or
format problems that another pass on the SFT set fixes at a fraction of the cost. Ask
which baseline failure you are fixing (Section 16) before climbing the ladder.

### 12. Decontamination and Splits

A leaked eval set turns your metrics into fiction. If evaluation questions — or near
duplicates — appear in training, the model has memorized the test, and the score
measures memory, not capability. The discipline:

1. **Split before you train.** Carve train / validation / test from the raw set before
   any augmentation. Train feeds gradients; validation selects checkpoints and detects
   overfitting; test is touched once, at the end.
2. **Deduplicate across splits.** Exact dedup by normalized string, then near-dedup by
   fingerprint (MinHash or embedding similarity). Instruction data is full of paraphrase
   clusters; without near-dedup, "different" train rows test the same eval row.
3. **Decontaminate against external benchmarks** if you report numbers on them. A model
   tuned on data that contains MMLU items cannot honestly report MMLU.
4. **Record the split as a data version** (Fine-Tuning 03, 04). A silent re-split is a
   silent invalidation of every comparison made against the old numbers.

The exercise raises TRN007 when the config has no eval path distinct from train.

### 13. Checkpoint Selection

The last checkpoint is not the best checkpoint. Eval loss typically bottoms out before
the final step; training past that point overfits. Selection discipline:

- **Save checkpoints periodically** (every N optimizer steps and/or each epoch) with
  step number and config hash attached.
- **Select on a held-out metric** — eval loss during training, task metric at the end.
  The exercise raises TRN008 when the config selects on train loss.
- **Keep a rollback.** Retain the best checkpoint and the last one. The best is what you
  ship; the last is where you resume after an interruption. Keeping every checkpoint of
  a long run wastes disk; keeping none loses the run to a power cut.
- **Never ship the winner of a single eval number** without the regression suite from
  Section 10.

### 14. Evaluation Before and After

The order of operations that separates an experiment from a hope:

1. **Baseline first.** Run the base model on your golden eval set before any training.
   No baseline, no measurement — you cannot claim improvement against nothing.
2. **Name the failure.** Write down the specific baseline failure you are fixing:
   "answers lack hadith citations," "ignores the Arabic-when-asked constraint," "wrong
   JSON schema 40% of the time." A run without a named failure cannot prove it helped.
3. **Train, then re-run the same eval set** with the same metric and split.
4. **Failure analysis before celebrating.** Read the diffs on the failure cases. A metric
   that moved for the wrong reason — style change mistaken for correctness — will not
   survive contact with users.
5. **Regression-check general capabilities** (Section 10).

This is the same measured-experiment discipline as RAG evaluation, applied to training.
It is also the bridge to Fine-Tuning 04 (run configs) and 05 (registry gates): the
baseline, the named failure, and the after-metrics are what the registry entry records.

### 15. Model Merging

Merging combines two or more sets of weights — often two LoRA adapters — into one model.
The common forms:

- **Linear interpolation:** `W' = W + α·B1A1 + β·B2A2`, or averaging two full models
  with a coefficient.
- **Task arithmetic:** treat the difference `θ_tuned − θ_base` as a task vector and add
  a scaled version to another model.
- **DARE:** drop a fraction of delta parameters at random and rescale the survivors so
  the expected delta is preserved — a sparsification that lets many deltas coexist with
  less interference.

**When merging helps:** combining orthogonal skills (Arabic citation format + JSON
schema compliance) trained as separate adapters; building a multi-task model without one
long joint run; ensembling checkpoints.

**When it silently hurts:** the adapters were trained through overlapping regions of
weight space and interfere — the sum is worse than either alone, with no error raised.
Merging is arithmetic, not evaluation: the merged model can be confidently broken.

**The rule:** always eval after merging, on the same golden set, before shipping. If
either adapter had a regression, the merge inherits it.

### 16. The Failure-First Engineering Rule

The most expensive habit in fine-tuning is treating hyperparameters as a search space
before defining the objective. "Which LoRA config is best?" is unanswerable in the
abstract. The two questions that are always answerable:

1. **What specific failure in the baseline am I fixing?**
2. **Which metric on a held-out golden set proves the fix?**

Every knob in this lecture — rank, LR, warmup, batch, precision, epochs — is justified
only relative to those two answers. If you cannot state them, the right move is not a
training run; it is another hour of failure analysis on the baseline. The exercise
encodes the same discipline as a validator: the good config is not the one with the
biggest batch, it is the one with no misconfiguration and a held-out metric to select
on.

---

## Common Mistakes to Avoid

### 1. Training Without Prompt Masking

```python
# ❌ BAD: loss on prompt tokens teaches the model to predict the user's question
labels = input_ids.copy()

# ✅ GOOD: prompt positions carry -100; only answer tokens contribute gradients
labels = [-100] * len(prompt_ids) + answer_ids
```

### 2. Requesting bf16 on Turing

```python
# ❌ BAD: sm_75 has no native bf16 tensor cores; you get errors or an fp32 fallback
torch_dtype = torch.bfloat16  # RTX 5000 / sm_75

# ✅ GOOD: fp16 + autocast + GradScaler on Turing; bf16 needs Ampere sm_80+
with torch.cuda.amp.autocast(dtype=torch.float16):
    loss = model(**batch).loss
```

### 3. Forgetting the Optimizer State in the Memory Budget

```python
# ❌ BAD: budgeting weights only, then OOM at step 40
mem = params_b * 2  # 14 GB for 7B fp16 — incomplete

# ✅ GOOD: weights + gradients + AdamW moments (+ master weights in mixed precision)
mem = params_b * (2 + 2 + 8 + 4)  # 112 GB for 7B full FT — correctly impossible
```

### 4. Peak LR Chosen Without the Method's Band

```python
# ❌ BAD: pretraining-scale LR on a full fine-tune destroys the weights
peak_lr = 5e-4  # full FT of a 7B model

# ✅ GOOD: small band for full FT, higher band for LoRA/QLoRA
peak_lr = 2e-5  # full FT
peak_lr = 2e-4  # LoRA / QLoRA
```

### 5. Selecting the Checkpoint on Train Loss

```python
# ❌ BAD: the lowest train-loss checkpoint is usually the most overfit one
best = min(checkpoints, key=lambda c: c.train_loss)

# ✅ GOOD: select on a held-out metric; keep best and last for rollback
best = min(checkpoints, key=lambda c: c.eval_loss)
```

### 6. Entering Fine-Tuning With No Baseline

```python
# ❌ BAD: train, look at the loss, declare victory
run_sft(data)
print("loss went down!")

# ✅ GOOD: baseline on golden set, named failure, train, same eval, regression suite
baseline = evaluate(base_model, golden_set)  # record numbers
failure = "answers lack source citations"  # the named failure
candidate = train(data)
after = evaluate(candidate, golden_set)  # compare against baseline
```

---

## Best Practices

1. **Budget memory arithmetically before every run** — weights, gradients, optimizer
   state, activations, overhead — and refuse to launch over budget.
2. **Use fp16 + GradScaler on Turing (sm_75)**; treat bf16 as an Ampere-and-later option
   only.
3. **Warmup 3-5% of steps** as a ratio, not an absolute step count.
4. **Keep peak LR inside the method's band**: ~2e-5 full FT, ~1e-4 to 2e-4 LoRA/QLoRA.
5. **Mask prompt tokens with -100** in every SFT run, without exception.
6. **Compute effective batch explicitly** (`micro × accum × devices`) and record it in
   the run config.
7. **Enable gradient checkpointing** for any 7B-class run on 16 GB.
8. **Split and decontaminate before training**; version the split.
9. **Select checkpoints on a held-out metric**; keep best and last.
10. **Run a baseline and a regression suite** around every fine-tune.
11. **Prefer clean data over more data**; audit before tuning hyperparameters.
12. **Ask the failure-first questions** — which baseline failure, which metric — before
    asking which LoRA config is best.

---

## Practice Exercises

### Exercise 1: Run the Validator
Run `python 07-training-internals.py`. For every finding the bad config raises, write
one sentence naming the real-world consequence of that misconfiguration during a live
training run. Then confirm the good config reports zero findings.

### Exercise 2: Full Memory Arithmetic by Hand
For a 13B model, compute the QLoRA memory total by hand (4-bit weights, adapters
0.5% of params in fp16, AdamW on adapters, activations with checkpointing at batch 2,
seq 2048). Does it fit 16 GB? Identify which single term dominates and which lever
(checkpointing, accumulation, shorter seq, smaller micro-batch) you would pull first.

### Exercise 3: Schedule Table
For a run with 1,000 total steps, peak LR 2e-4, warmup ratio 0.05, cosine decay: compute
the LR at steps 1, 25, 50, 250, 500, and 1,000. Explain why step 25 is the riskiest
step in the run and why step 1,000 is nearly zero.

### Exercise 4: Failure Analysis First
Take any model you use and write a one-paragraph baseline failure analysis: three
concrete failures, each with a metric you could compute on 50 held-out examples. Decide
whether the right tool is SFT, RAG (Fine-Tuning 06), or better data — and say why.

### Exercise 5: The Regression Suite
Design a 10-item general-capability regression suite for a domain fine-tune (for
example, an Arabic Islamic-text assistant): items that check out-of-domain formatting,
a multilingual check, and one safety probe. Specify how you would run it on the base
model and the candidate so the comparison is fair.

---

## Summary

1. **A training step is six ordered stages** — forward, loss, backward, optimizer,
   scheduler, zero-grad — and every hyperparameter belongs to exactly one of them.
2. **The tokenizer, chat template, and special tokens are part of the model**;
   mismatched tokenization silently invalidates the run.
3. **SFT loss is cross-entropy on answer tokens only**; prompt masking with -100 is
   non-negotiable, and training loss is a smoke detector, not a quality metric.
4. **AdamW costs 8 bytes per trainable parameter in optimizer state** — the hidden term
   that makes full 7B fine-tuning exceed 100 GB and QLoRA fit in ~6 GB.
5. **Warmup-then-decay schedules protect early steps**; peak LR has method-specific
   bands, and the schedule is counted in optimizer steps.
6. **Effective batch is micro × accum × devices**; accumulation simulates large batches
   within a small activation budget.
7. **On Turing sm_75 use fp16 with a loss scaler**; bf16 needs Ampere sm_80 and is a
   misconfiguration here without a fallback.
8. **Budget weights + gradients + optimizer + activations + overhead before the run**;
   checkpointing and accumulation trade time for memory.
9. **Overfitting shows as rising eval loss against falling train loss**; a clean small
   dataset beats a noisy large one.
10. **Catastrophic forgetting is detected by a regression suite**, not by the fine-tune's
    own eval loss, and mitigated by lower LR, LoRA, and mixed-in general data.
11. **SFT is the first rung**; DPO and RLHF earn their cost only after SFT and data
    quality have plateaued.
12. **Split, decontaminate, select on held-out metrics, and evaluate after every
    merge** — and never fine-tune without a named baseline failure and the metric that
    proves the fix.

**Next lecture:** Fine-Tuning 04 (training runs), where these settings become a
recorded, reproducible run config — and where the cloud-hybrid path (local prep, Colab
T4 / Vast.ai for the GPU hours) puts them into practice.

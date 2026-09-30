# Fine-Tuning 02: LoRA and QLoRA

## Topic Overview

Full fine-tuning updates every weight in the model. For a 7B model that means storing a
copy of the weights, gradients, and optimizer state for billions of parameters, which
does not fit on a consumer GPU and is often unnecessary anyway. LoRA (Low-Rank
Adaptation) freezes the base model and trains small adapter matrices that approximate
the weight update; QLoRA adds 4-bit quantization so the frozen base fits in consumer
VRAM. Together they are what make fine-tuning a 7B model practical on a 16 GB card.

The core idea is that the change needed to adapt a model is low-rank: a huge weight
matrix does not need a full-size update to learn a task. LoRA represents the update as
the product of two much smaller matrices, and trains only those. This is not an
approximation you pay for at inference; for inference the adapter is merged back into
the base exactly.

This lecture covers what LoRA trains and what it freezes, the role of the rank, how
QLoRA shrinks the memory footprint, how to budget VRAM before the run, and how to merge
the adapter for deployment.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what LoRA trains and what it freezes.
2. Explain the role of the rank and how it trades capacity against cost.
3. Explain how QLoRA fits a large base model into small VRAM.
4. Budget VRAM for a QLoRA run before launching it.
5. Merge the adapter into the base for inference.
6. State why the adapter is the portable artifact.

## Prerequisites

- Fine-Tuning 01 (SFT) for what fine-tuning changes.
- A basic model of GPU memory (weights, gradients, optimizer state, activations).

---

## 1. What LoRA Trains

### The low-rank update

LoRA freezes the base weights and trains two small matrices whose product approximates
the update. Instead of updating a 4096x4096 weight matrix directly, it trains a matrix
`B` of shape (out, r) and a matrix `A` of shape (r, in), where r is much smaller than
either dimension:

```python
# W' = W + BA  where B is (out, r) and A is (r, in)
# only B and A are trained; W is frozen
```

The adapter is typically 0.1% to 1% of the base parameters, which is why it is cheap to
train and small to store.

### The exercise

```python
def lora_update(base, b, a):
    """W' = W + BA. Only B and A are trained; W is frozen."""
    ...
```

The exercise builds the update by hand on a tiny matrix so the mechanism is visible:
the result is the frozen base plus the product of the two small matrices. The same
operation is what a training framework does across every adapted layer.

### Why freezing the base matters

The base model's knowledge and general capability are preserved because those weights
never change. LoRA only learns the task-specific adjustment, which is why it generalizes
well from small datasets and resists the catastrophic forgetting that full fine-tuning
can cause.

## 2. The Rank

### What the rank controls

The rank `r` is the inner dimension of the two adapter matrices: it controls the
adapter's capacity. A higher rank captures more complex adaptations but trains more
parameters and risks overfitting; a lower rank is cheaper and regularizes more.

### The common range and the decision

Rank 8 to 64 covers most tasks. Rank is a hyperparameter, tuned like any other: start
low, raise it only if the eval set says the adapter underfits. Because it is a
hyperparameter, it belongs in the run config (Fine-Tuning 04) and in the comparison
against the baseline.

### Rank as regularization

A low rank is a genuine regularizer, not just a cost saving. It limits how much the
model can change, which on a few hundred examples is often exactly what you want.

## 3. QLoRA: The 4-Bit Base

### The idea

QLoRA quantizes the frozen base model to 4-bit, cutting its weight memory roughly by a
factor of four, and trains the adapters in higher precision on top. A 7B model's weights
drop from about 14 GB in fp16 to about 3.5 GB at 4-bit.

### Why it fits

The memory freed by quantizing the base is what makes fine-tuning a 7B model possible on
a 16 GB GPU. The base is read-only and quantized; the trainable adapters and the
optimizer state are small. The exercise computes the combined footprint:

```python
def qlora_memory_gb(base_params_b, quant_bits, adapter_frac):
    """Weights at quant_bits plus the adapter, in GB."""
    weights = base_params_b * quant_bits / 8
    adapter = base_params_b * adapter_frac * 2  # adapters stay in fp16
    return weights + adapter
```

### Quality

QLoRA is not a free lunch in quality terms; 4-bit quantization loses a little precision.
By design the loss is small, which is why QLoRA reports near-LoRA quality at a fraction
of the memory. The right check is the eval set, not an assumption.

## 4. The Memory Budget

### The components

A QLoRA run needs:

1. The 4-bit base weights (about 3.5 GB for 7B).
2. The adapters in higher precision (small).
3. The optimizer state for the trainable parameters (small).
4. The activations, which dominate the peak and scale with batch size and sequence
   length.

```python
mem = qlora_memory_gb(7.0, 4, 0.01)  # < 5 GB: weights + adapter
assert mem < 5.0
full = qlora_memory_gb(7.0, 16, 0.0)  # > 13 GB: fp16 weights alone
assert full > 13.0
```

### Gradient checkpointing

Activations are the usual cause of an out-of-memory error, and gradient checkpointing is
the standard remedy: recompute activations during the backward pass instead of storing
them, trading compute for memory. On a 16 GB GPU it is usually required for a 7B run.

### Budget before the run

Check the budget before launching, not after an OOM at step 40. A 7B model under QLoRA
with a modest batch and gradient checkpointing fits in 16 GB; a 13B model needs careful
budgeting, a smaller batch, or a shorter sequence length.

## 5. Merging the Adapter

### The merge

For inference, the adapter is merged into the base: `W' = W + BA`. The merged model runs
with no adapter machinery and no inference overhead, and it behaves exactly as the
training produced.

### The adapter is the artifact

The adapter file is a few megabytes versus gigabytes for a full model, so it is the
portable artifact you version and ship. Publishing an adapter without its base model
version is meaningless, because the adapter only makes sense against the exact base it
was trained on (Fine-Tuning 05).

### Merge timing

You can also serve the base plus adapter separately at inference, which keeps adapters
hot-swappable. The tradeoff is a little inference overhead versus the flexibility to
swap adapters without rebuilding the base.

## Real-World Application

- Fine-tuning a 7B Arabic model with QLoRA on the RTX 5000's 16 GB using rank 16, a
  small batch, and gradient checkpointing.
- Storing the Athar SFT adapter (a few MB) as the versioned artifact while the base model
  stays as a shared download.
- Raising the rank from 8 to 32 only after the eval set shows the adapter underfits.
- Merging the adapter for a deployment where adapter-swapping is not needed.

## Common Mistakes

1. **Full fine-tuning when LoRA suffices.** The cost is far higher for a small gain.
2. **Rank chosen without tuning.** Too low underfits, too high overfits.
3. **Running QLoRA without a memory budget.** The run OOMs mid-training.
4. **Forgetting gradient checkpointing.** Activations blow the budget.
5. **Shipping the adapter without the base model version.** It cannot be reconstructed.
6. **Assuming 4-bit is lossless.** Validate quality on the eval set.

## Key Takeaways

1. LoRA trains small low-rank adapters and freezes the base; it preserves the base's
   knowledge and resists catastrophic forgetting.
2. The rank trades capacity against cost and is a tuned hyperparameter.
3. QLoRA's 4-bit base is what fits a 7B model on a 16 GB GPU; budget memory and use
   gradient checkpointing.
4. The merged model runs without adapter overhead; the unmerged adapter is small and
   hot-swappable.
5. The adapter is the portable artifact, but only alongside its exact base version.

## Self-Check Questions

1. What does LoRA freeze, and why does that preserve the base model's knowledge?
2. What does the rank control, and what happens if it is too low or too high?
3. Why does QLoRA make a 7B fine-tune possible on a 16 GB GPU?
4. Which memory component most often causes the OOM, and how is it reduced?
5. Why is the adapter the portable artifact, and what must ship with it?

## Further Reading / Connections

- Fine-Tuning 01 (SFT) — the training method LoRA makes affordable.
- Fine-Tuning 03 (training data) and 04 (training runs) — the data and config for the
  run.
- Fine-Tuning 05 (model registry) — where the adapter version is recorded.
- `docs/reference/books-and-sources.md` — PEFT and QLoRA references.

# Fine-Tuning 02: LoRA and QLoRA

## 🎯 Topic Overview

Full fine-tuning updates every weight — expensive and often unnecessary.
LoRA freezes the base model and trains small low-rank adapters; QLoRA adds
4-bit quantization so the base model fits in consumer VRAM. This lecture
covers the rank, the adapter, and the memory math that makes fine-tuning
possible on a 16 GB GPU.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain what LoRA trains and what it freezes
2. Explain the role of the rank
3. Explain how QLoRA fits a large base in small VRAM
4. Budget VRAM for a QLoRA run
5. Merge the adapter back into the base for inference

---

## 1. What LoRA Trains

LoRA freezes the base model and trains small low-rank matrices that
approximate the weight update. Instead of updating a 4096x4096 weight
matrix, it trains two small matrices whose product approximates the change.
The adapter is a fraction of the base size — typically 0.1% to 1% of the
parameters. The roadmap's exit test: "the model is fine-tuned with LoRA."

```python
# W' = W + BA  where B is (out, r) and A is (r, in)
# only B and A are trained; W is frozen
```

## 2. The Rank

The rank r controls the adapter's capacity. A higher rank captures more
complex adaptations but trains more parameters and risks overfitting. A
lower rank is cheaper and more regularizing. Rank 8 to 64 is the common
range. The rank is a hyperparameter, tuned like any other.

## 3. QLoRA: 4-Bit Base

QLoRA quantizes the frozen base model to 4-bit, so a 7B model's weights
drop from ~14 GB to ~4 GB. The adapters stay in higher precision. The
memory freed by quantization is what makes fine-tuning a 7B model possible
on a 16 GB GPU. The roadmap's exit test: "QLoRA fits the model in the
GPU's memory."

## 4. The Memory Budget

A QLoRA run needs: 4-bit weights, the adapters, the optimizer state, and
the activations. Gradient checkpointing trades compute for memory. The
budget is checked before the run, not after an OOM. A 7B model in QLoRA
with a modest batch fits in 16 GB; a 13B model needs careful budgeting.

## 5. Merging the Adapter

For inference, the adapter is merged into the base: W' = W + BA. The
merged model runs without the adapter machinery. The merge is exact and
reversible — the adapter file alone is the portable artifact, a few
megabytes versus gigabytes for the full model.

## Common Mistakes

- Full fine-tuning when LoRA suffices.
- Rank chosen without tuning.
- Running QLoRA without a memory budget (OOM mid-run).
- Forgetting gradient checkpointing.
- Shipping the adapter without the base model version.

## Key Takeaways

1. LoRA trains small adapters; the base is frozen.
2. The rank trades capacity against cost.
3. QLoRA's 4-bit base is what fits in 16 GB.
4. Budget memory before the run.
5. The adapter merges into the base and is the portable artifact.
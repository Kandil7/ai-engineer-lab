# 07-machine-learning — 49: Quantization — Smaller Numbers, Same Model

Companion exercise: `49-quantization.py`

---

## Topic Overview

Quantization shrinks a model by storing its weights and activations in
fewer
bits — FP32 down to INT8 or INT4 — trading a little precision for a lot
of
memory, bandwidth, and speed. The core idea is affine mapping: represent
a float
value as an integer via a scale and zero-point, so the model fits in a
fraction
of the VRAM and runs on hardware that likes small integers.

The two ways to get there are post-training quantization (PTQ) and
quantization-aware training (QAT). PTQ quantizes a trained model without
retraining — cheap, but accuracy drops when the model is sensitive. QAT
injects
fake quantization into training so the model learns to be robust to it —
more
accurate, but costs a retraining pass. INT8 is the safe default; INT4 is
the
aggressive end, often combined with other tricks.

For a 16 GB GPU this is the difference between "the model fits" and "it
doesn't."
The exercise implements affine quantization from scratch so the
mechanism — scale,
zero-point, round-trip error — is visible, then points at
`torch.quantization`
for the production path.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain affine quantization: scale, zero-point, and the round-trip.
2. Compute the quantization error of INT8 versus INT4.
3. Distinguish PTQ from QAT and when each is required.
4. Explain symmetric versus asymmetric quantization.
5. State why INT8 is the default and INT4 the aggressive option.
6. Reason about the VRAM and speed win on a fixed GPU budget.
7. Use `torch.quantization` dynamic quantization.
8. Explain weight-only versus activation quantization and per-channel schemes.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and dtypes | `36-pytorch-tensors.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Model serving | `model-serving` (in this curriculum) |

## 1. Affine Quantization

### The mapping

Affine quantization maps a float `x` to an integer `q` with a scale `s`
and a
zero-point `z`:

```text
q = round(x / s + z),  clamped to [0, 2^bits - 1]
x_hat = (q - z) * s      # the dequantized approximation
```

The scale sets the step size; the zero-point maps float zero to an
integer. The
dequantized value is an approximation — that error is the price of fewer
bits.

### The code

```python
def quantize(x, bits):
    s = (x.max() - x.min()) / (2**bits - 1)
    z = round(-x.min() / s)
    q = torch.clamp(torch.round(x / s + z), 0, 2**bits - 1).to(torch.int8)
    return q, s, z
```

### The real-world analogy

Quantization is rounding a price to the nearest dollar. The scale is
"one dollar
is the smallest unit," the zero-point is "zero dollars," and the
round-trip error
is the cents you lose. Fewer bits is a coarser dollar — INT4 is rounding
to the
nearest ten dollars, which is fine for a rough estimate and bad for
exact change.

## 2. The Round-Trip Error

### Why fewer bits means more error

The step size is the range divided by the number of buckets. INT8 gives
255
buckets; INT4 gives 15. The finer the buckets, the smaller the
round-trip error —
and the larger the storage. This is the fundamental quantization
tradeoff.

### The measure

Error is the mean squared difference between `x` and `x_hat`. It rises
sharply
as bits drop, which is why INT4 is riskier than INT8, especially for
activations
with outliers. The error is not uniform: an outlier stretches the scale
and
coarsens the step for everyone, which is why per-channel scales help.

## 3. PTQ — Post-Training Quantization

### Quantize after training

PTQ takes a trained FP32 model and quantizes its weights (and optionally
activations) in one pass — no retraining. It is cheap and usually the
first
thing to try. Dynamic PTQ quantizes weights ahead of time and
activations on the
fly; static PTQ uses a calibration dataset to choose activation scales.

### When it fails

PTQ fails when the model is *sensitive* — outliers in activations, or a
large
model where small per-layer errors compound. Then the accuracy drop is
unacceptable and you move to QAT.

## 4. QAT — Quantization-Aware Training

### Learn to be robust

QAT inserts "fake quantization" — quantize then dequantize — into the
forward
pass during training, so the model learns weights that are robust to the
rounding it will face at inference. The result quantizes with far less
accuracy
loss.

### The cost

QAT costs a retraining pass and more engineering. It is the choice when
PTQ's
accuracy drop is too large — the same cost-accuracy ladder as zero-shot
to
fine-tuning, applied to quantization.

## 5. Symmetric vs Asymmetric

### The two schemes

Symmetric quantization centers the range at zero (zero-point is fixed at
0),
which is simpler and faster. Asymmetric uses a real zero-point,
capturing a
skewed range more precisely. Symmetric is the common default; asymmetric
wins
for activations like ReLU outputs that are one-sided.

### Why it matters

The scheme is a precision-versus-simplicity choice. A one-sided
activation range
wastes half the buckets under symmetric quantization, so asymmetric
recovers
that precision at the cost of the extra zero-point.

## 6. Weight-Only and Per-Channel

### What else varies

Weight-only quantization quantizes just the weights (leaving activations
in
higher precision), which is the cheapest and most robust first step —
used by
many LLM INT4 schemes. Per-channel quantization gives each output
channel its
own scale, avoiding the outlier problem that a single global scale
creates.

### Why the options matter

The dials — weight-only vs full, per-tensor vs per-channel, symmetric vs
asymmetric — are how you trade accuracy for size. The robust default is
weight-only + per-channel, which preserves most accuracy at the largest
size win.

## 7. The VRAM and Speed Win

### The arithmetic

INT8 weights are 1/4 the size of FP32; INT4 is 1/8. A 7B model in FP16
needs
~14 GB (weights alone); INT8 halves that, INT4 quarters it. On a 16 GB
card that
is the difference between fitting and not. Smaller weights also move
faster to
the compute units, so quantized inference is both smaller and faster.

### The honest caveat

The speed win requires hardware/software support for the quantized
dtype. The
size win is unconditional; the speed win is not. Quantize for size
first, and
verify the speed on your target.

## Real-World Application

- **Running a 7B model on a 16 GB GPU** — INT8/INT4 turns "OOM" into "fits."
- **Edge and mobile inference** — INT8 models on phones and embedded devices.
- **Serving cost** — smaller weights cut memory bandwidth and hosting cost.
- **The DevMate case** — quantizing the local embedding or LLM model so it fits
  the RTX 5000 alongside the rest of the serving stack.

## Common Mistakes to Avoid

### Mistake 1: INT4 on a sensitive model without QAT
```
# WRONG — PTQ INT4 on a model with activation outliers, large accuracy drop
# CORRECT — start INT8 PTQ; use QAT before going to INT4
```

### Mistake 2: Forgetting the calibration set for static PTQ
```
# WRONG — static quantization with no calibration, poor activation scales
# CORRECT — calibrate scales on a representative sample of real data
```

### Mistake 3: Quantizing only for speed, ignoring the size win
```
# WRONG — dropping quantization because the target lacks int8 kernels
# CORRECT — the memory win is unconditional; measure speed separately
```

### Mistake 4: Measuring error on the wrong tensor
```
# WRONG — reporting weight round-trip error only, ignoring activation outliers
# CORRECT — measure end-to-end accuracy on real data, the metric that matters
```

### Mistake 5: Quantizing before you need to
```
# WRONG — INT4 quantizing a model that already fits and runs fast enough
# CORRECT — quantize when the size/speed is the actual bottleneck
```

### Mistake 6: A single global scale with heavy outliers
```
# WRONG — one scale for a tensor with an outlier, coarsening every bucket
# CORRECT — per-channel scales to contain the outlier's damage
```

## Best Practices

1. Start with INT8 PTQ; it is cheap and usually sufficient.
2. Use a representative calibration set for static PTQ.
3. Escalate to QAT only when PTQ's accuracy drop is unacceptable.
4. Prefer symmetric for simplicity; asymmetric for one-sided ranges.
5. Measure end-to-end accuracy on real data, not weight round-trip error.
6. Verify the speed win on your actual hardware before claiming it.
7. Treat quantization as part of the serving path (`model-serving`).
8. Keep the FP32 original for comparison and rollback.
9. Try weight-only + per-channel first for LLM-scale quantization.

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| PTQ (dynamic) | seconds | 1/4 (INT8) | No retraining |
| PTQ (static) | seconds + calibration | 1/4 | Needs a cal set |
| QAT | one retraining pass | 1/4 at inference | Most accurate |
| INT4 | — | 1/8 | Aggressive; often + QAT |

## AI Engineering Relevance

**Where this shows up:** fitting and serving models on constrained hardware. On
the RTX 5000's 16 GB, quantization is how you run a model that would
otherwise
OOM, and how you cut serving latency on the CPU for edge cases.

| Concept here | Used for |
|---|---|
| Affine mapping | The mechanism every quantizer uses |
| PTQ vs QAT | The cost-accuracy ladder |
| INT8 vs INT4 | The size-accuracy dial |
| Round-trip error | Predicting whether quantization will hurt |

**Scale note:** the memory budget rule from this curriculum — weights + KV cache
+ activations — is where quantization enters. INT8/INT4 change the "weights" term
directly, which is why it is the first lever to pull before offloading
or
upgrading hardware.

## Key Takeaways

1. Affine quantization maps floats to integers via a scale and zero-point.
2. The round-trip error is the price of fewer bits; it rises sharply below INT8.
3. PTQ is cheap (no retrain); QAT is accurate (retrains with fake quantization).
4. INT8 is the safe default; INT4 is the aggressive, often-QAT-requiring option.
5. The size win is unconditional; the speed win needs hardware support.
6. Weight-only + per-channel is the robust LLM-scale default.

## Self-Check Questions

1. What do the scale and zero-point do in affine quantization?
2. Why does INT4 have much more round-trip error than INT8?
3. When does PTQ fail and QAT become necessary?
4. Why would you choose asymmetric over symmetric quantization?
5. Why is the size win of quantization unconditional but the speed win not?
6. What is weight-only quantization, and why is it the robust first step?

## Summary

| Concept | Description |
|---|---|
| Affine quantization | float -> int via scale and zero-point |
| Round-trip error | The price of fewer bits |
| PTQ | Quantize after training, no retrain |
| QAT | Train with fake quantization for robustness |
| INT8 vs INT4 | 1/4 vs 1/8 the size, more vs less error |

## Quick Reference

| Task | Idiom |
|---|---|
| Scale | `s = (max - min) / (2^bits - 1)` |
| Quantize | `q = clamp(round(x/s + z), 0, 2^bits-1)` |
| Dequantize | `x_hat = (q - z) * s` |
| Dynamic PTQ | `torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)` |

## Further Reading / Connections

- `50-pruning-lecture.md` — the redundancy lever this pairs with.
- `51-distillation-lecture.md` — the knowledge lever of the compression toolbox.
- `model-serving` (in `04-ai-engineering`) — quantized models in production.
- Official docs: <https://pytorch.org/docs/stable/quantization.html>

## Next Steps

Next: **[50 — Pruning](../advanced/50-pruning-lecture.md)** — remove the
weights you don't need.


# Fine-Tuning 02: LoRA and QLoRA — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| LoRA | Low-rank adapters; base frozen, small matrices trained | W' = W + BA |
| Rank | The adapter's capacity hyperparameter | 8 to 64 |
| QLoRA | LoRA with a 4-bit quantized base | 7B fits in 16 GB |
| Adapter | The small trained matrices, the portable artifact | a few MB |
| Merge | W' = W + BA for inference | exact, reversible |
| Gradient checkpointing | Trade compute for memory | activations recomputed |
| Memory budget | Weights + adapters + optimizer + activations | checked before the run |

---

## Alphabetical Glossary

### Adapter

**Definition:** The small trained matrices that approximate the weight
update. The portable artifact — a few megabytes versus gigabytes for the
full model.

**Example:**
```python
# B (out, r) and A (r, in), trained while W is frozen
```

**Related concepts:** LoRA, Merge

---

### Gradient checkpointing

**Definition:** Trading compute for memory by recomputing activations
during the backward pass. Often the difference between fitting and OOM.

**Example:**
```python
# activations recomputed instead of stored
```

**Related concepts:** Memory budget

---

### LoRA

**Definition:** Low-rank adaptation: freezing the base model and training
small matrices whose product approximates the weight update. Typically
0.1% to 1% of the parameters.

**Example:**
```python
# W' = W + BA; only B and A are trained
```

**Related concepts:** Adapter, Rank

---

### Memory budget

**Definition:** The full VRAM accounting: 4-bit weights, adapters,
optimizer state, and activations. Checked before the run, not after an OOM.

**Example:**
```python
# 7B QLoRA: ~4 GB weights + adapters + optimizer + activations
```

**Related concepts:** QLoRA, Gradient checkpointing

---

### Merge

**Definition:** Combining the adapter into the base for inference: W' = W +
BA. Exact and reversible.

**Example:**
```python
# merged model runs without the adapter machinery
```

**Related concepts:** Adapter, LoRA

---

### QLoRA

**Definition:** LoRA with a 4-bit quantized base. A 7B model's weights drop
from ~14 GB to ~4 GB, making fine-tuning possible on a 16 GB GPU.

**Example:**
```python
# 4-bit base, adapters in higher precision
```

**Related concepts:** Memory budget, LoRA

---

### Rank

**Definition:** The adapter's capacity hyperparameter. Higher rank captures
more but risks overfitting; lower rank is cheaper and regularizing.

**Example:**
```python
# r = 8 to 64 is the common range
```

**Related concepts:** LoRA

---

## Related Concepts

- **SFT**: LoRA is the parameter-efficient way to run SFT (topic 01)
- **Training runs**: the hyperparameters around the adapter (topic 04)
- **Model registry**: the adapter and base version are registered (topic 05)

## Key Takeaways

1. LoRA trains small adapters; the base is frozen.
2. The rank trades capacity against cost.
3. QLoRA's 4-bit base is what fits in 16 GB.
4. Budget memory before the run.
5. The adapter merges into the base and is the portable artifact.
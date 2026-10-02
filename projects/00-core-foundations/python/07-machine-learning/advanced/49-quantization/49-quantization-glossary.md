# Quantization — Glossary 49

Companion lecture: `49-quantization-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Quantization | Technique | Storing weights/activations in fewer bits |
| Scale | Affine | The step size mapping float to integer |
| Zero-point | Affine | The integer that maps float zero |
| Round-trip error | Metric | Difference between original and dequantized value |
| PTQ | Method | Quantize after training, no retrain |
| QAT | Method | Train with fake quantization for robustness |
| Symmetric | Scheme | Zero-point fixed at zero |
| Asymmetric | Scheme | Real zero-point for skewed ranges |
| INT8 | Precision | 8-bit integers, the safe default |
| INT4 | Precision | 4-bit integers, aggressive |

## Detailed Definitions

### Quantization
**Definition**: Reducing a model's memory and compute by representing its weights
and activations in fewer bits (INT8/INT4) instead of FP32/FP16.
**Example**:
```python
torch.quantization.quantize_dynamic(model, {nn.Linear}, dtype=torch.qint8)
```
**Related**: Scale, Zero-point

### Scale
**Definition**: The step size in affine quantization — the float range divided by
the number of integer buckets — that maps a float to an integer.
**Example**:
```python
s = (x.max() - x.min()) / (2**bits - 1)
```
**Related**: Zero-point, Round-trip error

### Zero-point
**Definition**: The integer that corresponds to float zero in affine
quantization, so zero stays representable.
**Related**: Scale, Symmetric

### Round-trip error
**Definition**: The error between a value and its quantize-then-dequantize
approximation, which grows as bits drop.
**Related**: Quantization, Scale

### PTQ
**Definition**: Post-training quantization — quantizing a trained model in one
pass, no retraining. Cheap; can hurt sensitive models.
**Related**: QAT, Quantization

### QAT
**Definition**: Quantization-aware training — inserting fake quantization into
training so the model learns weights robust to rounding. Costs a retrain, gains
accuracy.
**Related**: PTQ, Quantization

### Symmetric / asymmetric
**Definition**: Symmetric quantization fixes the zero-point at zero; asymmetric
uses a real zero-point to better fit one-sided ranges.
**Related**: Zero-point, Scale

### INT8 / INT4
**Definition**: 8-bit (1/4 of FP32) and 4-bit (1/8) integer precisions — the size
accuracy dial of quantization.
**Related**: Quantization, Round-trip error

## Key Concepts Summary

### The cost-accuracy ladder
- INT8 PTQ (cheap, default) -> QAT -> INT4 (aggressive).

### The mechanism
- `q = clamp(round(x/s + z), 0, 2^bits-1)`, `x_hat = (q - z) * s`.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. Storing weights in fewer bits — ___
2. The step size in affine mapping — ___
3. The integer mapping float zero — ___
4. Error from quantize-dequantize — ___
5. Quantize after training, no retrain — ___
6. Train with fake quantization — ___
7. Zero-point fixed at zero — ___
8. 4-bit precision — ___

**Answers:** 1-quantization, 2-scale, 3-zero-point, 4-round-trip error,
5-PTQ, 6-QAT, 7-symmetric, 8-INT4

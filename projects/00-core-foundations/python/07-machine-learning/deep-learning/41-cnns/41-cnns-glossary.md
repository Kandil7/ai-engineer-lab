# Convolutional Neural Networks — Glossary 41

Companion lecture: `41-cnns-lecture.md`

## Quick Reference Table

| Term | Category | One-Line Definition |
|---|---|---|
| Channel | Tensor | The depth dimension of a feature map (C in B,C,H,W) |
| Convolution | Operation | Sliding a learned filter over the input to produce a feature map |
| Feature map | Representation | The output of one filter, lighting up where its pattern appears |
| Filter / kernel | Parameter | The small learned weight matrix slid across the input |
| Flatten | Operation | Reshaping spatial feature maps into a 1D vector for the dense head |
| Locality | Inductive bias | Nearby pixels are related; distant ones are not |
| Max pooling | Operation | Downsampling by taking the max over a window |
| Padding | Hyperparameter | Zero border added to preserve spatial size |
| Receptive field | Property | The input region that influences one output neuron |
| Stride | Hyperparameter | The step size of the sliding window |
| Translation invariance | Inductive bias | A pattern is recognized regardless of its position |
| BatchNorm | Layer | Normalizes activations per batch to stabilize training |

## Detailed Definitions

### Channel
**Definition**: The depth axis of an image or feature map. Grayscale has 1
channel, RGB has 3, and intermediate conv layers expand to dozens or hundreds.
**Example**:
```python
x = torch.randn(2, 3, 224, 224)  # batch 2, 3 channels, 224x224
```
**Related**: Feature map, Convolution

### Convolution
**Definition**: The operation of sliding a learned filter over the input and
computing a weighted sum at each position, producing a feature map.
**Example**:
```python
nn.Conv2d(1, 8, kernel_size=3)(x)  # 1 -> 8 channels, 3x3 kernel
```
**Complexity**: O(C_in · C_out · K² · H · W) per layer.
**Related**: Filter, Feature map

### Feature map
**Definition**: The output activation of a single filter — a spatial map whose
values are high where the filter's pattern matches the input.
**Related**: Channel, Convolution

### Filter / kernel
**Definition**: The small weight matrix (e.g. 3×3) a conv layer learns. Shared
across all positions, which is the source of translation invariance and low
parameter count.
**Related**: Convolution, Translation invariance

### Flatten
**Definition**: Reshaping the (C, H, W) feature maps into a 1D vector before the
dense classifier head.
**Example**:
```python
x = features(x).flatten(1)  # (B, C, H, W) -> (B, C*H*W)
```
**Related**: Channel, Feature map

### Locality
**Definition**: The inductive bias that nearby pixels are related and distant
ones are not, encoded by the small kernel that only mixes local neighborhoods.
**Related**: Translation invariance, Convolution

### Max pooling
**Definition**: Downsampling a feature map by taking the maximum over a sliding
window, keeping the strongest activation and discarding exact location.
**Example**:
```python
nn.MaxPool2d(kernel_size=2, stride=2)  # halves spatial size
```
**Related**: Stride, Translation invariance

### Padding
**Definition**: Adding a zero border around the input so the output keeps its
spatial size when a kernel would otherwise shrink it.
**Example**:
```python
nn.Conv2d(1, 8, 3, padding=1)  # 28 -> 28 (same size)
```
**Related**: Stride, Convolution

### Receptive field
**Definition**: The region of the original input that influences one output
neuron. Grows with depth and kernel size; must cover the relevant object.
**Related**: Convolution, Filter

### Stride
**Definition**: The step size the filter takes as it slides. Stride 1 preserves
resolution; stride 2 downsamples.
**Example**:
```python
nn.Conv2d(1, 8, 3, stride=2)  # 28 -> 13
```
**Related**: Padding, Max pooling

### Translation invariance
**Definition**: The property that a pattern is recognized regardless of where it
appears, achieved by sharing filter weights across all positions.
**Related**: Locality, Convolution

## Key Concepts Summary

### Output-size arithmetic
- `out = floor((in + 2p - k) / s) + 1`
- Padding preserves size; stride downsamples.

### The two inductive biases
- Locality: small kernels mix only neighbors.
- Translation invariance: shared weights apply everywhere.

### The classic stack
- conv → ReLU → pool, repeated; then flatten → dense head.

## Practice Terms

Match each term to its definition (answers at the bottom).

1. The depth axis of a feature map — ___
2. Sliding a learned filter over the input — ___
3. Downsampling by taking the max over a window — ___
4. The input region one neuron sees — ___
5. Shared weights applied everywhere — ___
6. Reshaping feature maps into a 1D vector — ___
7. Zero border to preserve spatial size — ___
8. The step size of the sliding window — ___

**Answers:** 1-channel, 2-convolution, 3-max pooling, 4-receptive field,
5-translation invariance, 6-flatten, 7-padding, 8-stride

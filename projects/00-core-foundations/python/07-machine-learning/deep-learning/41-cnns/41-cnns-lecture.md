# 07-machine-learning — 41: Convolutional Neural Networks — The Image Learner

Companion exercise: `41-cnns.py`

---

## Topic Overview

A fully-connected network sees an image as a bag of pixels with no notion of
*where* things are. A convolutional neural network (CNN) imposes the two priors
that make images tractable: **translation invariance** (a cat is a cat anywhere
in the frame) and **locality** (nearby pixels are related, distant ones are
not). A CNN learns filters that slide across the image, detecting edges, then
textures, then parts, then objects, layer by layer.

This topic covers the mechanics: the convolution operation, stride and padding,
pooling, channels, and how a stack of conv + pool + dense layers becomes an
image classifier. Because `torchvision` ships without GPU pretrained weights in
this environment, the exercise builds a CNN from `torch.nn` primitives and
verifies the shapes, parameter counts, and the receptive-field arithmetic that
govern why CNNs are cheap and fast.

CNNs are not just for photos. Any grid-structured signal — spectrograms for
audio, time-frequency maps, document-layout tiles — is a candidate. Understanding
the convolution is the bridge from "ML on tables" to "ML on structured signals".

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain translation invariance and locality as the two inductive biases of a CNN.
2. Compute output dimensions from kernel size, stride, and padding.
3. Distinguish depthwise channels from spatial dimensions.
4. Build a conv + ReLU + pool + dense classifier in `torch.nn`.
5. Explain what pooling does and why it aids translation invariance.
6. Compute the parameter count and receptive field of a conv stack.
7. Describe when a CNN helps and when it does not.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Training loop | `37-pytorch-training-loop.py` |

## 1. The Convolution Operation

### What a filter does

A convolution slides a small learned filter (a weight matrix, e.g. 3×3) across
the input, computing a weighted sum at each position. One filter produces one
feature map that lights up wherever the pattern it learned appears:

```python
import torch
import torch.nn as nn

# 1 input channel -> 8 output channels, 3x3 kernel
conv = nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3)
x = torch.randn(2, 1, 28, 28)  # (batch, channels, height, width)
y = conv(x)
print(y.shape)  # torch.Size([2, 8, 26, 26])
```

The 28×28 input becomes 26×26 because a 3×3 kernel has no room at the borders:
`out = in - kernel + 1 = 28 - 3 + 1 = 26`.

### Why shared weights

The same filter is applied at every position — that is the translation
invariance prior. One filter's 9 weights (plus a bias) serve the entire image,
which is why a CNN has orders of magnitude fewer parameters than a dense layer
on the same input, and why it generalizes from few examples.

## 2. Stride and Padding

### The arithmetic

Output size is governed by kernel size `k`, padding `p`, and stride `s`:

```text
out = floor((in + 2p - k) / s) + 1
```

```python
same = nn.Conv2d(1, 8, kernel_size=3, padding=1)  # keeps 28 -> 28
down = nn.Conv2d(1, 8, kernel_size=3, stride=2)  # downsamples 28 -> 13
```

- **Padding** preserves spatial size (useful to keep edges).
- **Stride 2** downsamples, replacing a separate pooling step in some designs.

### Why you control these

Padding without care shrinks the map and throws away border information; a large
stride collapses resolution. Both are design dials: pad to preserve, stride to
summarize.

## 3. Pooling

### Max pooling

Pooling downsamples a feature map by taking the max (or average) over a window.
Max pooling keeps the *strongest* activation and discards its precise location:

```python
pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 26x26 -> 13x13
```

### Why it aids invariance

By discarding exact positions, pooling makes the representation robust to small
shifts — a strong edge a pixel to the left still wins the max. It also cuts the
activation size in half each application, reducing compute and, via the
subsequent flatten, the parameter count of the dense head.

## 4. Channels and Depth

### The channel dimension

Early layers have few channels (e.g. 1 for grayscale, 3 for RGB). Each conv
layer expands channels while shrinking space, so the representation goes from
"raw intensities" to "many abstract feature maps":

```text
(1, 28, 28) -> conv -> (8, 26, 26) -> pool -> (8, 13, 13) -> conv -> (16, 11, 11) ...
```

### The depth trade

Deeper channels = richer features but more parameters. A standard small CNN
doubles channels while halving spatial size each block, keeping total
activation roughly constant — a rule of thumb, not a law.

## 5. Receptive Field

### What a neuron sees

The receptive field is the region of the input that influences one output
neuron. A 3×3 filter sees 9 pixels; stacking two 3×3 convs gives the second
layer a 5×5 receptive field over the original input.

### Why it matters

The receptive field must be large enough to cover the relevant object part
before the classifier can recognize it. Two 3×3 convs match one 5×5 conv's
field with fewer parameters and more non-linearity — a classic reason modern
nets favor stacks of small kernels.

## 6. The Classic Classifier Stack

### The shape

A CNN classifier is conv blocks (conv → ReLU → pool) followed by a flatten and a
dense head:

```python
class TinyCNN(nn.Module):
    def __init__(self):
        super().__init__()
        self.features = nn.Sequential(
            nn.Conv2d(1, 8, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
            nn.Conv2d(8, 16, 3, padding=1),
            nn.ReLU(),
            nn.MaxPool2d(2),
        )
        self.classifier = nn.Linear(16 * 7 * 7, 10)  # 28 -> 14 -> 7

    def forward(self, x):
        return self.classifier(self.features(x).flatten(1))
```

### The cost story

The conv layers are cheap (shared weights); the dense head is where parameters
concentrate. Flattening `16×7×7 = 784` features into a linear layer is why
parameter counts spike at the head.

## 7. When CNNs Help

### The right-shaped data

CNNs shine on grid data with local structure: images, spectrograms, and layout
tiles. They are the wrong tool for tabular data or permutation-invariant sets,
where a dense or attention model is more natural.

### The pretrained shortcut

In practice you rarely train a CNN from scratch — you fine-tune a pretrained
one (ResNet, EfficientNet), the pattern of `39-transfer-learning`. The from-scratch
exercise here teaches the mechanism so the pretrained shortcut is not a black box.

## 8. Common Mistakes to Avoid

### Mistake 1: Wrong output-shape arithmetic
```
# WRONG — Linear(16*8*8) after two pool layers on a 28 input; actual is 7x7
# CORRECT — print(features(x).shape) and size the dense layer from it
```

### Mistake 2: Flattening without checking batch order
```
# WRONG — x.view(x.size(0), -1) after a channels-first vs channels-last mixup
# CORRECT — keep (B, C, H, W) convention throughout
```

### Mistake 3: Forgetting channels in the input tensor
```
# WRONG — passing (28, 28) to Conv2d which expects (C, H, W)
# CORRECT — x.unsqueeze(0).unsqueeze(0) or use a 4D (B, C, H, W) batch
```

### Mistake 4: A receptive field smaller than the object
```
# WRONG — a 3x3-only stack asked to classify a 64x64 object's identity
# CORRECT — deepen or add strides until the field covers the object
```

### Mistake 5: Training from scratch when a pretrained model exists
```
# WRONG — random-init CNN on a 5k-image dataset
# CORRECT — fine-tune a pretrained backbone (39-transfer-learning)
```

## 9. Best Practices

1. Use channels-first (B, C, H, W) tensors and keep the convention explicit.
2. Prefer small 3×3 kernels stacked deep over one large kernel.
3. Pair every conv with normalization (BatchNorm) and a non-linearity.
4. Size the dense head from the actual feature map shape, not from memory.
5. Double channels while halving spatial size per block.
6. Use global average pooling to replace a large flatten when possible.
7. Verify parameter counts; the conv layers should be cheap relative to the head.
8. Fine-tune pretrained backbones instead of training from scratch.
9. Seed everything and record the input normalization.
10. Print the shape after each block when debugging a new architecture.

## 10. Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Conv 3×3 forward | O(C_in·C_out·K²·H·W) | feature maps | Shared weights keep params low |
| Max pooling | O(H·W) | downsampled map | Nearly free; enables invariance |
| Flatten + dense head | O(features·classes) | head weights | Parameter concentration |
| Full training | minutes-hours GPU | activations | Small nets train on the local RTX 5000 |
| Inference | one forward pass | model artifact | Cheap; CNNs are edge-friendly |

## 11. AI Engineering Relevance

**Where this shows up:** document layout analysis for corpus ingestion, image
classification behind visual search, audio tagging via spectrograms, and OCR
preprocessing. On this workstation the relevant numbers are the RTX 5000's
16 GB — a small CNN trains in minutes, while a ResNet-50 fine-tune fits in
VRAM only with a reduced batch or mixed precision.

| Concept here | Used for |
|---|---|
| Conv + pool stack | Feature extraction over images and spectrograms |
| Receptive field | Deciding how deep a model must be for its task |
| Shared weights | Small models that run on edge devices |
| Pretrained CNN + fine-tune | The production default, not from-scratch |

**Scale note:** CNNs are the cheapest deep model to serve — a quantized CNN
(`49-quantization`) can run on a phone. The receptive-field and parameter
reasoning here is the same math you use when sizing a model for a 16 GB budget.

## 12. Summary

| Concept | Description |
|---|---|
| Convolution | Learned filter slid across the input |
| Translation invariance | Shared weights applied everywhere |
| Locality | Nearby pixels matter, distant ones don't |
| Stride / padding | Control output size and downsampling |
| Pooling | Downsample, keep strong activations |
| Receptive field | The input region one neuron sees |
| Channels | Depth of feature maps, grows with depth |

## Quick Reference

| Task | Idiom |
|---|---|
| Conv layer | `nn.Conv2d(in, out, kernel_size, stride, padding)` |
| Pool | `nn.MaxPool2d(kernel_size, stride)` |
| Flatten | `x.flatten(1)` |
| Shape check | `print(model.features(x).shape)` |
| Output size | `out = floor((in + 2p - k) / s) + 1` |

## Next Steps

Next: **[42 — Recurrent Neural Networks](42-rnns-lecture.md)** — sequences and the models that read them.

Continues in: **[09-genai — 21 Fine-Tuning](../../09-genai/lectures/21-fine-tuning-lecture.md)** — fine-tune a pretrained backbone.

Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html>

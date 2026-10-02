# 07-machine-learning — 41: Convolutional Neural Networks — The Image Learner

Companion exercise: `41-cnns.py`

---

## Topic Overview

A fully-connected network sees an image as a bag of pixels with no
notion of
*where* things are. A convolutional neural network (CNN) imposes the two priors
that make images tractable: **translation invariance** (a cat is a cat
anywhere
in the frame) and **locality** (nearby pixels are related, distant ones
are
not). A CNN learns filters that slide across the image, detecting edges,
then
textures, then parts, then objects, layer by layer.

This topic covers the mechanics: the convolution operation, stride and
padding,
pooling, channels, and how a stack of conv + pool + dense layers becomes
an
image classifier. Because `torchvision` ships without GPU pretrained
weights in
this environment, the exercise builds a CNN from `torch.nn` primitives
and
verifies the shapes, parameter counts, and the receptive-field
arithmetic that
govern why CNNs are cheap and fast.

CNNs are not just for photos. Any grid-structured signal — spectrograms
for
audio, time-frequency maps, document-layout tiles, even 1D sensor
streams — is a
candidate. Understanding the convolution is the bridge from "ML on
tables" to
"ML on structured signals," and the same filter/slide/receptive-field
reasoning
carries over to every modern vision and audio model.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain translation invariance and locality as the two inductive biases of a CNN.
2. Compute output dimensions from kernel size, stride, and padding.
3. Distinguish depthwise channels from spatial dimensions.
4. Build a conv + ReLU + pool + dense classifier in `torch.nn`.
5. Explain what pooling does and why it aids translation invariance.
6. Compute the parameter count and receptive field of a conv stack.
7. Describe when a CNN helps and when it does not.
8. Design a small CNN that fits a 16 GB GPU budget by reasoning about parameters.

## Prerequisites

| Need | Where |
|---|---|
| Tensors and autograd | `36-pytorch-tensors.py` |
| Neural network basics | `38-neural-network-basics.py` |
| Training loop | `37-pytorch-training-loop.py` |

## 1. The Convolution Operation

### What a filter does

A convolution slides a small learned filter (a weight matrix, e.g. 3×3)
across
the input, computing a weighted sum at each position. One filter
produces one
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

The 28×28 input becomes 26×26 because a 3×3 kernel has no room at the
borders:
`out = in - kernel + 1 = 28 - 3 + 1 = 26`.

### The real-world analogy

Imagine a magnifying glass scanning a page left-to-right, top-to-bottom.
The
glass is the kernel; each time it stops, it reports one number — how
much the
text under it matches a specific shape. Slide the glass over the whole
page and
you get a map of "where this shape appears." The CNN learns which shapes
to look
for, not where — the where is handled by sliding.

### Why shared weights

The same filter is applied at every position — that is the translation
invariance prior. One filter's 9 weights (plus a bias) serve the entire
image,
which is why a CNN has orders of magnitude fewer parameters than a dense
layer
on the same input, and why it generalizes from few examples.

### When it works, when it fails

A convolution works when the signal has *local, translation-invariant*
structure
— an object is the same object shifted by a few pixels. It fails when
the signal
is permutation-invariant or long-range (where attention or a dense model
wins),
or when the relevant pattern is genuinely position-specific.

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

### Why you control these

Padding without care shrinks the map and throws away border information;
a large
stride collapses resolution. Both are design dials: pad to preserve,
stride to
summarize. Getting this arithmetic right is the difference between a
model that
runs and a shape-mismatch crash at the dense head.

### The analogy

Padding is a picture mat — it adds a neutral border so the frame
(kernel) can
reach the edges without cropping them. Stride is how far you move the
frame
each step; a stride of 2 skips every other position, so you see a
coarser view
and produce a smaller map.

## 3. Pooling

### Max pooling

Pooling downsamples a feature map by taking the max (or average) over a
window.
Max pooling keeps the *strongest* activation and discards its precise
location:

```python
pool = nn.MaxPool2d(kernel_size=2, stride=2)  # 26x26 -> 13x13
```

### Why it aids invariance

By discarding exact positions, pooling makes the representation robust
to small
shifts — a strong edge a pixel to the left still wins the max. It also
cuts the
activation size in half each application, reducing compute and, via the
subsequent flatten, the parameter count of the dense head.

### The analogy

Pooling is summarizing a photo into a thumbnail — you keep the
strongest, most
salient content and lose the exact coordinates. The thumbnail still
tells you
"there is a face here," which is enough for classification.

## 4. Channels and Depth

### The channel dimension

Early layers have few channels (1 for grayscale, 3 for RGB). Each conv
layer
expands channels while shrinking space, so the representation goes from
"raw
intensities" to "many abstract feature maps":

```text
(1, 28, 28) -> conv -> (8, 26, 26) -> pool -> (8, 13, 13) -> conv -> (16, 11, 11) ...
```

### The depth trade

Deeper channels = richer features but more parameters. A standard small
CNN
doubles channels while halving spatial size each block, keeping total
activation roughly constant — a rule of thumb, not a law. The channels
are where
"what kind of feature" lives, while the spatial axes are "where."

## 5. Receptive Field

### What a neuron sees

The receptive field is the region of the input that influences one
output
neuron. A 3×3 filter sees 9 pixels; stacking two 3×3 convs gives the
second
layer a 5×5 receptive field over the original input.

### Why it matters

The receptive field must be large enough to cover the relevant object
part
before the classifier can recognize it. Two 3×3 convs match one 5×5
conv's
field with fewer parameters and more non-linearity — a classic reason
modern
nets favor stacks of small kernels over one big one.

### When it fails

If the receptive field is smaller than the object, the network literally
cannot
see enough of it to classify it — no amount of training fixes that. The
fix is
more depth or larger strides, and the receptive-field math tells you how
much.

## 6. The Classic Classifier Stack

### The shape

A CNN classifier is conv blocks (conv → ReLU → pool) followed by a
flatten and a
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

The conv layers are cheap (shared weights); the dense head is where
parameters
concentrate. Flattening `16×7×7 = 784` features into a linear layer is
why
parameter counts spike at the head. Global average pooling can replace
that
large flatten and cut the head's parameters dramatically.

## 7. When CNNs Help

### The right-shaped data

CNNs shine on grid data with local structure: images, spectrograms, and
layout
tiles. They are the wrong tool for tabular data or permutation-invariant
sets,
where a dense or attention model is more natural. The filter assumption
— local,
translation-invariant structure — is either present or not, and that is
the test.

### The pretrained shortcut

In practice you rarely train a CNN from scratch — you fine-tune a
pretrained one
(ResNet, EfficientNet), the pattern of `39-transfer-learning`. The
from-scratch
exercise here teaches the mechanism so the pretrained shortcut is not a
black box,
and so you can reason about *why* the pretrained backbone is shaped as
it is.

## 8. Feature Hierarchy — From Edges to Objects

### The layered abstraction

A CNN builds meaning in layers. The first layer detects edges and simple
gradients; the second combines edges into corners and textures; the third
combines textures into parts (a wheel, an eye); the last combines parts into
objects. This hierarchy is *emergent*, not programmed — the training data and
the architecture's inductive bias produce it, and it is the same hierarchy
regardless of whether the input is a photo, a spectrogram, or a document tile.

### The analogy

Think of an assembly line: the first station cuts raw shapes, the next assembles
them into components, the next into subassemblies, the last into the finished
product. Each station only sees the previous station's output, and no one
station understands the whole — but the line as a whole produces the object.

### Why it matters for transfer

Because the hierarchy is layered, the early layers are generic (edges, textures)
and the later layers are task-specific (faces, cars). That is exactly why
transfer learning (`39`) freezes early layers and retrains only the head: the
generic layers transfer, the specific layers do not. Understanding the hierarchy
is what makes "freeze the backbone" intuitive rather than arbitrary.

## 9. BatchNorm and Normalization

### What normalization does

Normalization keeps activations on a stable scale so training does not fight
exploding or vanishing values. BatchNorm normalizes each channel's activations
across the batch, then re-scales with learned parameters. It speeds convergence
and, by injecting mild noise through the batch statistics, acts as a regularizer.

```python
conv_block = nn.Sequential(
    nn.Conv2d(1, 8, 3, padding=1),
    nn.BatchNorm2d(8),
    nn.ReLU(),
    nn.MaxPool2d(2),
)
```

### The standard order

The canonical order in a modern block is conv → BatchNorm → ReLU → pool. Putting
the normalization *before* the non-linearity keeps the ReLU from receiving
unstable pre-activations. This order is a convention, but a nearly universal one,
and deviating from it without reason is a smell.

### The normalization discipline

Whatever normalization you apply in training, the *identical* transform must be
applied at inference — BatchNorm needs its running statistics frozen, not the
batch's, at eval time. This is the same "train and eval pipelines must agree"
discipline that `45-data-augmentation` applies to transforms.

## 10. 1D, 2D, and Depthwise Convolutions

### The dimensionality

The convolution generalizes across dimensions. A **1D** convolution slides over a
single axis — time-series, audio waveforms, text token sequences. A **2D**
convolution slides over two axes — images, spectrograms. A **3D** convolution
slides over three — video (time plus two space), medical volumes. The kernel and
the sliding rule are identical; only the number of axes changes.

```python
nn.Conv1d(in_channels=1, out_channels=8, kernel_size=3)   # sequence data
nn.Conv2d(in_channels=1, out_channels=8, kernel_size=3)   # image data
```

### Depthwise separable convolutions

A standard conv mixes *spatial* and *channel* information in one operation. A
depthwise separable conv splits it: a depthwise conv filters each channel
independently (spatial only), then a pointwise 1×1 conv mixes channels. This is
the building block of MobileNet and other efficient architectures, and it cuts
the parameter count by roughly a factor of the kernel size squared.

### Why this matters on constrained hardware

On a 16 GB GPU — or a phone — the difference between a standard conv and a
depthwise separable one is the difference between a model that fits (and runs)
and one that does not. The efficient-conv family is the CNN analogue of the
quantization and pruning levers (`49`, `50`): a footprint reduction achieved by
changing the architecture, not just the numbers.

### The truncation note

Depthwise separable convs trade a little accuracy for a large efficiency win, the
same tradeoff as every other compression technique. MobileNet's success showed
the trade is usually favorable: modern mobile vision is depthwise almost by
default.

## Real-World Application

- **Document layout analysis** — treating scanned-page tiles as images for OCR
  preprocessing and region classification in corpus ingestion.
- **Audio tagging** — classifying spectrograms, where time-frequency maps are
  the grid the CNN reads.
- **Visual search** — embedding images for retrieval via a pretrained CNN.
- **On-device classification** — a small quantized CNN (`49`) running on a phone.
- **The Athar/DevMate case** — any image or spectrogram input in the corpus
  pipeline; the same filter reasoning sizes the model for the RTX 5000.

## Common Mistakes to Avoid

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

### Mistake 6: A huge flatten inflating the head
```
# WRONG — a 1024-channel feature map flattened into a billion-parameter dense head
# CORRECT — global average pooling to shrink the head before the classifier
```

## Best Practices

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

## Complexity and Cost

| Operation | Time | Space | Notes |
|---|---|---|---|
| Conv 3×3 forward | O(C_in·C_out·K²·H·W) | feature maps | Shared weights keep params low |
| Max pooling | O(H·W) | downsampled map | Nearly free; enables invariance |
| Flatten + dense head | O(features·classes) | head weights | Parameter concentration |
| Full training | minutes-hours GPU | activations | Small nets train on the local RTX 5000 |
| Inference | one forward pass | model artifact | Cheap; CNNs are edge-friendly |

## AI Engineering Relevance

**Where this shows up:** document layout analysis for corpus ingestion, image
classification behind visual search, audio tagging via spectrograms, and
OCR
preprocessing. On this workstation the relevant numbers are the RTX
5000's
16 GB — a small CNN trains in minutes, while a ResNet-50 fine-tune fits in
VRAM only with a reduced batch or mixed precision.

| Concept here | Used for |
|---|---|
| Conv + pool stack | Feature extraction over images and spectrograms |
| Receptive field | Deciding how deep a model must be for its task |
| Shared weights | Small models that run on edge devices |
| Pretrained CNN + fine-tune | The production default, not from-scratch |

**Scale note:** CNNs are the cheapest deep model to serve — a quantized CNN
(`49-quantization`) can run on a phone. The receptive-field and
parameter
reasoning here is the same math you use when sizing a model for a 16 GB
budget.

## Key Takeaways

1. The convolution is a learned filter slid across a grid; shared weights give translation invariance.
2. `out = floor((in + 2p - k) / s) + 1` governs every shape decision.
3. Pooling downsamples and adds small-shift invariance, nearly for free.
4. Channels grow with depth; the dense head concentrates parameters.
5. The receptive field must cover the object, or no training can fix the model.
6. CNNs are for local, translation-invariant grid data — and are the cheapest deep model to serve.

## Self-Check Questions

1. Why do shared filter weights produce translation invariance, and why does that reduce parameters?
2. A 32×32 input passes through a 5×5 kernel with padding 2 and stride 2. What is the output size?
3. Why does max pooling aid translation invariance, and what else does it do for the model?
4. Why are two 3×3 convs preferred over one 5×5 conv?
5. What happens if the receptive field is smaller than the object, and how do you fix it?
6. Why do parameter counts concentrate in the dense head, and how do you reduce them?

## Summary

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

## Further Reading / Connections

- `38-neural-network-basics-lecture.md` — the layers a CNN is built from.
- `39-transfer-learning-lecture.md` — fine-tuning a pretrained CNN.
- `45-data-augmentation-lecture.md` — the data-side regularizer for CNNs.
- `49-quantization-lecture.md` — shrinking the CNN for edge deployment.
- Official docs: <https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html>

## Next Steps

Next: **[42 — Recurrent Neural Networks](42-rnns-lecture.md)** —
sequences and the models that read them.

Continues in: **[09-genai — 21
Fine-Tuning](../../09-genai/lectures/21-fine-tuning-lecture.md)** —
fine-tune a pretrained backbone.


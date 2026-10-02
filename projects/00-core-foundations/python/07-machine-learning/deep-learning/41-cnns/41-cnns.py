"""
07-machine-learning — 41: Convolutional Neural Networks — The Image Learner
============================================================================
Topics: convolution, stride/padding, pooling, channels, receptive field,
        the conv + ReLU + pool + dense classifier stack

Why this matters for AI/backend engineering:
    CNNs are the workhorse for any grid-structured signal — images,
    spectrograms, document tiles. Understanding the convolution (and its
    output-size arithmetic) is what lets you size a vision model for a
    16 GB GPU budget instead of guessing.

Note: no GPU pretrained weights are required; we build the CNN from torch.nn
primitives and verify shapes, parameter counts, and receptive-field math.

Run:      python 41-cnns.py
Verify:   python 41-cnns.py --verify
Reference: https://pytorch.org/docs/stable/generated/torch.nn.Conv2d.html
"""

from __future__ import annotations

import torch
import torch.nn as nn

torch.manual_seed(0)


# ============================================================
# 1. The convolution operation and output-size arithmetic
# ============================================================
def conv_out(in_size: int, kernel: int, stride: int, padding: int) -> int:
    """out = floor((in + 2p - k) / s) + 1"""
    return (in_size + 2 * padding - kernel) // stride + 1


conv = nn.Conv2d(1, 8, kernel_size=3)
x = torch.randn(2, 1, 28, 28)
y = conv(x)
print("Example 1: convolution")
print(f"  input {tuple(x.shape)} -> output {tuple(y.shape)}")
print(f"  28x28 with 3x3 kernel, no padding -> {conv_out(28, 3, 1, 0)}x{conv_out(28, 3, 1, 0)}")

# ============================================================
# 2. Stride and padding
# ============================================================
same = nn.Conv2d(1, 8, 3, padding=1)  # preserves 28 -> 28
down = nn.Conv2d(1, 8, 3, stride=2)  # downsamples 28 -> 13
print("\nExample 2: stride and padding")
print(f"  padding=1: {tuple(same(x).shape)} (preserves size)")
print(f"  stride=2 : {tuple(down(x).shape)} (downsamples)")

# ============================================================
# 3. Max pooling
# ============================================================
pool = nn.MaxPool2d(kernel_size=2, stride=2)
print("\nExample 3: max pooling")
print(f"  {tuple(y.shape)} -> {tuple(pool(y).shape)} (halves spatial size)")


# ============================================================
# 4. The classic classifier stack
# ============================================================
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


model = TinyCNN()
print("\nExample 4: classifier stack")
print(f"  input {tuple(x.shape)} -> logits {tuple(model(x).shape)}")

# ============================================================
# 5. Parameter counts — conv is cheap, head is heavy
# ============================================================
conv_params = sum(p.numel() for p in model.features.parameters())
head_params = sum(p.numel() for p in model.classifier.parameters())
total = conv_params + head_params
print("\nExample 5: parameter distribution")
print(f"  conv features: {conv_params:,} params")
print(f"  dense head   : {head_params:,} params")
print(f"  total        : {total:,} params")

# ============================================================
# 6. Receptive field — two 3x3 convs cover a 5x5 field
# ============================================================
print("\nExample 6: receptive field")
print("  one 3x3 conv  -> 3x3 field")
print("  two 3x3 convs -> 5x5 field (fewer params than one 5x5)")
print("  -> stacks of small kernels win on params + non-linearity")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Convolution = learned filter slid across the input")
print("- Translation invariance (shared weights) + locality (small kernel)")
print("- out = floor((in + 2p - k)/s) + 1")
print("- Pooling downsamples and adds small-shift invariance")
print("- Conv layers are cheap; the dense head concentrates parameters")
print("=" * 60)


def _verify() -> None:
    assert conv_out(28, 3, 1, 0) == 26
    assert conv_out(28, 3, 1, 1) == 28  # padding preserves
    assert conv_out(28, 3, 2, 0) == 13  # stride downsamples
    assert y.shape == (2, 8, 26, 26)
    assert same(x).shape == (2, 8, 28, 28)
    assert down(x).shape == (2, 8, 13, 13)
    assert pool(y).shape == (2, 8, 13, 13)
    assert model(x).shape == (2, 10)
    assert conv_params < head_params, "dense head should dominate params"
    assert conv_params + head_params == total
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

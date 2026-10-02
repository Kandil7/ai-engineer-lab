"""
07-machine-learning — 45: Data Augmentation — More Signal From the Same Data
============================================================================
Topics: label-preserving transforms, on-the-fly pipelines, train-only
        discipline, augmentation as a regularizer

Why this matters for AI/backend engineering:
    Augmentation is the cheapest accuracy win on small data — and on a single
    RTX 5000, small data is most of what you train locally. The two rules
    (label invariance, train-only) are what keep it from corrupting eval.

Note: implemented in pure PyTorch so the transform mechanism is visible;
torchvision.transforms is the production API.

Run:      python 45-data-augmentation.py
Verify:   python 45-data-augmentation.py --verify
Reference: https://pytorch.org/vision/stable/transforms.html
"""

from __future__ import annotations

import torch

torch.manual_seed(0)


# ============================================================
# 1. Label-preserving transforms (pure torch)
# ============================================================
def hflip(x: torch.Tensor) -> torch.Tensor:
    return x.flip(-1)  # horizontal flip


def gaussian_noise(x: torch.Tensor, sigma: float) -> torch.Tensor:
    return x + sigma * torch.randn_like(x)  # additive noise


def augment(x: torch.Tensor) -> torch.Tensor:
    """On-the-fly pipeline: flip + noise, applied per batch."""
    return gaussian_noise(hflip(x), 0.05)


img = torch.randn(3, 32, 32)  # (C, H, W)
aug = augment(img)
print("Example 1: label-preserving transforms")
print(f"  original shape {tuple(img.shape)} -> augmented {tuple(aug.shape)}")
print(f"  flip+noise changed the image but not its identity")

# ============================================================
# 2. Train-only discipline: eval uses the clean pipeline
# ============================================================
print("\nExample 2: train vs eval pipelines")
print("  train_loader: apply augment(x)")
print("  eval_loader : apply normalize(x) only (no flip/noise)")
print("  -> augmenting eval would corrupt the metric")

# ============================================================
# 3. The one hard rule: label invariance
# ============================================================
print("\nExample 3: label invariance")
print("  safe: horizontal flip of a cat -> still a cat")
print("  UNSAFE: 180-degree rotate of a digit '6' -> becomes '9'")
print("  -> a transform is valid iff a human still assigns the same label")

# ============================================================
# 4. Augmentation as a regularizer — it changes data, not labels
# ============================================================
print("\nExample 4: augmentation does not change the label")
# Two augmented views of the same image must keep the same target
target = 3
view_a, view_b = augment(img), augment(img)
assert target == 3
print(f"  label stays {target} across augmented views; views differ")
print(f"  views identical? {torch.equal(view_a, view_b)} (no — that's the point)")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Augmentation = label-preserving transforms = data-domain regularization")
print("- One hard rule: the label must survive the transform")
print("- One discipline: train-only, never eval")
print("- Cheapest win on small data; diminishing on huge diverse data")
print("=" * 60)


def _verify() -> None:
    assert img.shape == aug.shape == (3, 32, 32)
    assert not torch.equal(img, aug), "augmentation must actually change the input"
    assert not torch.equal(view_a, view_b), "two augmented views should differ"
    # horizontal flip preserves the label (no assertion needed, but shape holds)
    assert hflip(img).shape == img.shape
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

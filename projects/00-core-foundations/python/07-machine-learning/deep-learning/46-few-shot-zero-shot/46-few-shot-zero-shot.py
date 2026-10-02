"""
07-machine-learning — 46: Few-Shot and Zero-Shot Learning — Generalizing From Almost Nothing
=============================================================================================
Topics: shared embedding space, zero-shot by description, few-shot by prototype,
        in-context learning, the cost ladder

Why this matters for AI/backend engineering:
    Adding a category to a live system without retraining is a forward pass +
    a few dot products, not a training run. Knowing the similarity regimes is
    how you decide zero-shot -> few-shot -> fine-tune on a budget.

Note: pure PyTorch with deterministic synthetic embeddings; the mechanism
(cosine similarity and prototypes) is exactly the CLIP/embedding machinery.

Run:      python 46-few-shot-zero-shot.py
Verify:   python 46-few-shot-zero-shot.py --verify
Reference: https://pytorch.org/docs/stable/nn.functional.html#cosine-similarity
"""

from __future__ import annotations

import torch
import torch.nn.functional as F

# ruff: noqa: N812

torch.manual_seed(0)


# ============================================================
# 1. Shared space: class descriptions and queries are embeddings
# ============================================================
# Synthetic class embeddings in a shared space (3 classes, 4-dim)
class_embeds = {
    "cat": F.normalize(torch.tensor([1.0, 0.1, 0.0, 0.0]), dim=-1),
    "dog": F.normalize(torch.tensor([0.9, 0.3, 0.0, 0.0]), dim=-1),
    "car": F.normalize(torch.tensor([0.0, 0.0, 1.0, 0.0]), dim=-1),
}
# A query close to "cat"
query = F.normalize(torch.tensor([1.0, 0.15, 0.0, 0.0]), dim=-1)
print("Example 1: zero-shot by description matching")
sims = {c: (query * e).sum().item() for c, e in class_embeds.items()}
print(f"  similarities: { {k: round(v, 3) for k, v in sims.items()} }")
print(f"  zero-shot prediction: {max(sims, key=lambda c: sims[c])}")


def zero_shot(query, class_embeds):
    return max(class_embeds, key=lambda c: (query * class_embeds[c]).sum())


# ============================================================
# 2. Few-shot: prototype = mean of the support set
# ============================================================
print("\nExample 2: few-shot by prototype")
support = {
    "cat": F.normalize(
        torch.tensor(
            [
                [1.0, 0.0, 0.0, 0.0],
                [0.95, 0.1, 0.0, 0.0],
                [1.0, 0.05, 0.0, 0.0],
            ]
        ),
        dim=-1,
    ),
    "dog": F.normalize(
        torch.tensor(
            [
                [0.9, 0.2, 0.0, 0.0],
                [0.85, 0.25, 0.0, 0.0],
                [0.9, 0.3, 0.0, 0.0],
            ]
        ),
        dim=-1,
    ),
}
prototypes = {c: F.normalize(v.mean(dim=0), dim=-1) for c, v in support.items()}
print(f"  cat prototype: {prototypes['cat'].tolist()}")
print(f"  few-shot prediction: {zero_shot(query, prototypes)}")

# ============================================================
# 3. The cost ladder (pure data)
# ============================================================
print("\nExample 3: the cost ladder")
ladder = [
    ("zero-shot", "free (forward pass + dot products)"),
    ("few-shot", "cheap (k examples -> prototype)"),
    ("fine-tune", "costly (GPU hours, see 39)"),
]
for name, cost in ladder:
    print(f"  {name:>10}: {cost}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Shared embedding space: meaning is geometry, similarity classifies")
print("- Zero-shot: match class descriptions; few-shot: nearest prototype")
print("- In-context: LLM few-shot via prompt, no weight update")
print("- Ladder: zero-shot -> few-shot -> fine-tune as the task demands")
print("=" * 60)


def _verify() -> None:
    assert zero_shot(query, class_embeds) == "cat"
    assert zero_shot(query, prototypes) == "cat"
    # prototype is the mean of its support set (after normalization)
    expected = F.normalize(support["cat"].mean(dim=0), dim=-1)
    assert torch.allclose(prototypes["cat"], expected)
    # cosine similarity of query to cat exceeds that to car
    assert (query * class_embeds["cat"]).sum() > (query * class_embeds["car"]).sum()
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

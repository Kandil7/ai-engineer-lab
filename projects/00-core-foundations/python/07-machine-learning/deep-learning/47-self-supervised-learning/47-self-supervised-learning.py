"""
07-machine-learning — 47: Self-Supervised Learning — Labels From the Data Itself
================================================================================
Topics: pretext tasks, contrastive (InfoNCE) vs masked modeling,
        pretrain-then-fine-tune

Why this matters for AI/backend engineering:
    Every foundation model you serve — GPT, BERT, CLIP — is an SSL product.
    Understanding the pretext task is what tells you why a pretrained encoder
    generalizes, and when to continue pretraining on in-domain data.

Note: pure PyTorch; contrastive (InfoNCE) on a small batch and a masked-token
prediction demo, both deterministic under a fixed seed.

Run:      python 47-self-supervised-learning.py
Verify:   python 47-self-supervised-learning.py --verify
Reference: https://arxiv.org/abs/2002.05709
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


# ============================================================
# 1. Contrastive learning — InfoNCE
# ============================================================
def info_nce(z_i: torch.Tensor, z_j: torch.Tensor, tau: float) -> torch.Tensor:
    """z_i, z_j: two augmented views of the same batch (batch x dim).
    Positives are on the diagonal; negatives are off-diagonal."""
    z_i = F.normalize(z_i, dim=-1)
    z_j = F.normalize(z_j, dim=-1)
    sim = (z_i @ z_j.T) / tau  # (batch, batch)
    labels = torch.arange(z_i.size(0))  # positives on the diagonal
    return F.cross_entropy(sim, labels)


batch, dim = 8, 16
z_i = torch.randn(batch, dim)
z_j = z_i + 0.1 * torch.randn(batch, dim)  # a positive "view" of each sample
loss = info_nce(z_i, z_j, tau=0.5)
print("Example 1: contrastive (InfoNCE)")
print(f"  loss = {loss.item():.4f} (pulls diagonal positives up, negatives down)")

# A positive pair is more similar than a random negative pair
pos = F.cosine_similarity(z_i, z_j).mean().item()
neg = F.cosine_similarity(z_i, z_j[torch.randperm(batch)]).mean().item()
print(f"  mean positive similarity {pos:.3f} > negative {neg:.3f}")

# ============================================================
# 2. Masked modeling — hide a token, predict from context
# ============================================================
print("\nExample 2: masked modeling")
vocab = F.normalize(torch.randn(16, 8), dim=-1)  # 16 token embeddings
seq = torch.tensor([3, 1, 4, 1, 5, 9, 2, 6])  # a sequence of token ids
mask_pos = 3
masked = seq.clone()
masked[mask_pos] = 0  # 0 = [MASK]
# Predict the masked token by nearest vocabulary embedding to the context mean
context = vocab[masked[masked != 0]].mean(dim=0)
pred = (vocab @ context).argmax().item()
print(f"  masked seq: {masked.tolist()}  (true token {seq[mask_pos].item()})")
print(f"  nearest-embedding prediction: {pred}")

# ============================================================
# 3. Pretrain-then-fine-tune (the production default)
# ============================================================
print("\nExample 3: pretrain-then-fine-tune")
print("  SSL pretrain (unlabeled, free) -> fine-tune (small labeled set)")
print("  -> you inherit the pretraining; your budget is the fine-tune")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Pretext task: labels invented from the data itself")
print("- Contrastive (InfoNCE): positives close, negatives far")
print("- Masked modeling: reconstruct the hidden token from context")
print("- Pretrain-then-fine-tune is how foundation models reach production")
print("=" * 60)


def _verify() -> None:
    assert loss.item() > 0, "InfoNCE loss must be positive"
    assert pos > neg, "positive pairs must be more similar than negatives"
    # The masked token's embedding is the nearest to the context mean
    assert pred == seq[mask_pos].item(), "masked token should be recoverable from context"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

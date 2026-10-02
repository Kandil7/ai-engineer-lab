"""
07-machine-learning — 50: Pruning — Remove the Weights You Don't Need
=====================================================================
Topics: structured vs unstructured, magnitude/global pruning, lottery ticket,
        prune-then-fine-tune

Why this matters for AI/backend engineering:
    Pruning shrinks a model for a tight VRAM or latency budget. The
    structured/unstructured distinction decides whether the shrink actually
    speeds the model up — a real, not academic, difference on a 16 GB GPU.

Note: uses torch.nn.utils.prune (built in). Verified: unstructured sparsity,
global pruning, and structured row-removal all behave as specified.

Run:      python 50-pruning.py
Verify:   python 50-pruning.py --verify
Reference: https://pytorch.org/docs/stable/generated/torch.nn.utils.prune.l1_unstructured.html
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.utils.prune as prune

torch.manual_seed(0)


def main() -> None:
    # ============================================================
    # 1. Unstructured magnitude pruning
    # ============================================================
    lin = nn.Linear(8, 8)
    prune.l1_unstructured(lin, name="weight", amount=0.5)
    sparsity = (lin.weight == 0).float().mean().item()
    print("Example 1: unstructured magnitude pruning")
    print(f"  sparsity: {sparsity:.2f} (bottom 50% of weights zeroed)")
    print(
        f"  weight == weight_orig * mask: "
        f"{torch.equal(lin.weight, lin.weight_orig * lin.weight_mask)}"
    )

    # ============================================================
    # 2. Global unstructured pruning
    # ============================================================
    l1, l2 = nn.Linear(8, 8), nn.Linear(8, 8)
    prune.global_unstructured(
        [(l1, "weight"), (l2, "weight")],
        pruning_method=prune.L1Unstructured,
        amount=0.5,
    )
    g_sparsity = ((l1.weight == 0).float().mean() + (l2.weight == 0).float().mean()).item() / 2
    print("\nExample 2: global unstructured pruning")
    print(f"  mean sparsity across layers: {g_sparsity:.2f}")

    # ============================================================
    # 3. Structured pruning — remove whole rows
    # ============================================================
    lin3 = nn.Linear(8, 8)
    prune.ln_structured(lin3, name="weight", amount=0.5, n=1, dim=0)
    zero_rows = (lin3.weight.sum(dim=1) == 0).sum().item()
    print("\nExample 3: structured pruning (remove rows)")
    print(f"  all-zero rows: {zero_rows} of 8 (a smaller *dense* model)")

    # ============================================================
    # Summary
    # ============================================================
    print("\n" + "=" * 60)
    print("Summary:")
    print("- Unstructured: zero individual weights -> sparse matrix")
    print("- Structured: remove whole rows/channels -> smaller dense (real speedup)")
    print("- Prune, then fine-tune, to recover accuracy")
    print("=" * 60)

    assert abs(sparsity - 0.5) < 1e-6, "unstructured amount=0.5 should zero ~50%"
    assert abs(g_sparsity - 0.5) < 1e-6, "global amount=0.5 should zero ~50% overall"
    assert zero_rows == 4, "structured amount=0.5 removes 4 of 8 rows"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        main()

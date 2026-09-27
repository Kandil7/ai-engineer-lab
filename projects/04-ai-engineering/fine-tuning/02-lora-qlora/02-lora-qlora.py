"""
Fine-Tuning — 02: LoRA and QLoRA
================================
Topics: the low-rank update, the rank, and the QLoRA memory budget.

Why this matters:
    Full fine-tuning is expensive and often unnecessary. This exercise
    builds the LoRA update and budgets VRAM for a QLoRA run.

Run:      python 02-lora-qlora.py
Verify:   python 02-lora-qlora.py --verify
"""

from __future__ import annotations

import sys


def lora_update(
    base: list[list[float]], b: list[list[float]], a: list[list[float]]
) -> list[list[float]]:
    """W' = W + BA. Only B and A are trained; W is frozen."""
    out, r = len(b), len(b[0])
    assert len(a) == r
    assert len(a[0]) == len(base[0])
    result = [row[:] for row in base]
    for i in range(out):
        for j in range(len(base[0])):
            result[i][j] += sum(b[i][k] * a[k][j] for k in range(r))
    return result


def qlora_memory_gb(
    base_params_b: float, quant_bits: int, adapter_frac: float
) -> float:
    """Weights at quant_bits plus the adapter, in GB."""
    weights = base_params_b * quant_bits / 8
    adapter = base_params_b * adapter_frac * 2  # adapters stay in fp16
    return weights + adapter


def main() -> None:
    # A tiny frozen weight matrix and a rank-1 adapter.
    base = [[1.0, 0.0], [0.0, 1.0]]
    b = [[2.0], [3.0]]  # (2, r=1)
    a = [[0.5, 0.5]]  # (r=1, 2)
    updated = lora_update(base, b, a)
    assert updated[0][0] == 1.0 + 2.0 * 0.5, "W' = W + BA"
    assert updated[1][1] == 1.0 + 3.0 * 0.5

    # QLoRA memory: a 7B base at 4-bit plus a small adapter.
    mem = qlora_memory_gb(7.0, 4, 0.01)
    assert mem < 5.0, "7B QLoRA weights + adapter fit well under 16 GB"
    assert mem > 3.5, "weights alone are ~3.5 GB at 4-bit"

    # Full fp16 would be ~14 GB for the weights alone.
    full = qlora_memory_gb(7.0, 16, 0.0)
    assert full > 13.0, "fp16 weights alone exceed a comfortable budget"

    print(f"LoRA update: W' = W + BA, only B and A trained")
    print(f"7B QLoRA memory: {mem:.2f} GB (4-bit weights + fp16 adapter)")
    print(f"7B fp16 weights alone: {full:.1f} GB — why QLoRA fits 16 GB")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

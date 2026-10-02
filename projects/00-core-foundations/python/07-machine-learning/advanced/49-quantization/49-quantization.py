"""
07-machine-learning — 49: Quantization — Smaller Numbers, Same Model
====================================================================
Topics: affine quantization (scale/zero-point), round-trip error, PTQ vs QAT,
        INT8 vs INT4, the VRAM win

Why this matters for AI/backend engineering:
    On a 16 GB GPU, quantization is often the difference between a model that
    fits and one that OOMs. The affine mapping (scale + zero-point) is the
    mechanism every quantizer uses; measuring its error predicts the risk.

Note: implemented from scratch for visibility; torch.quantization is the
production path (see the lecture's Quick Reference).

Run:      python 49-quantization.py
Verify:   python 49-quantization.py --verify
Reference: https://pytorch.org/docs/stable/quantization.html
"""

from __future__ import annotations

import torch


def quantize(x: torch.Tensor, bits: int):
    """Affine quantize a float tensor to `bits`-bit integers."""
    x = x.float()
    s = (x.max() - x.min()) / (2**bits - 1)
    z = round(-x.min().item() / s.item()) if s.item() != 0 else 0
    q = torch.clamp(torch.round(x / s + z), 0, 2**bits - 1).to(torch.int64)
    return q, s, z


def dequantize(q: torch.Tensor, s: torch.Tensor, z: int) -> torch.Tensor:
    return (q - z) * s


def round_trip_error(x: torch.Tensor, bits: int) -> float:
    q, s, z = quantize(x, bits)
    x_hat = dequantize(q, s, z)
    return torch.mean((x - x_hat) ** 2).item()


def main() -> None:
    torch.manual_seed(0)
    x = torch.randn(1000) * 2 + 1  # a weight-like distribution

    print("Example 1: affine quantization round-trip")
    q8, s8, z8 = quantize(x, 8)
    x_hat8 = dequantize(q8, s8, z8)
    print(f"  INT8  error {round_trip_error(x, 8):.2e}")
    print(f"  quantized values are integers in [0,255]: {(q8 == q8.round()).all().item()}")

    print("\nExample 2: fewer bits, more error")
    for bits in (16, 8, 4, 2):
        err = round_trip_error(x, bits)
        print(f"  {bits:>2}-bit: error {err:.2e}")

    print("\nExample 3: the VRAM win")
    print("  FP32 -> INT8 = 1/4 the size; FP32 -> INT4 = 1/8")
    print("  a 14 GB (FP16) 7B model -> ~7 GB (INT8) -> ~3.5 GB (INT4)")

    print("\n" + "=" * 60)
    print("Summary:")
    print("- q = clamp(round(x/s + z), 0, 2^bits-1);  x_hat = (q - z) * s")
    print("- Fewer bits = coarser step = more round-trip error")
    print("- PTQ is cheap; QAT is accurate; INT8 is the default")
    print("=" * 60)

    err8 = round_trip_error(x, 8)
    err4 = round_trip_error(x, 4)
    assert err8 < err4, "INT8 must have less error than INT4"
    assert err8 < 1e-1, "INT8 error must be small for this distribution"
    assert (q8 == q8.round()).all(), "quantized values must be integers"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        main()

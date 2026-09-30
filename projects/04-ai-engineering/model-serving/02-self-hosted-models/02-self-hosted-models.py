"""
Model Serving — 02: Self-Hosted Models
=======================================
Topics: the tradeoff, VRAM budget, and the OpenAI-compatible API.

Why this matters:
    Self-hosting trades cost for infrastructure. This exercise budgets
    VRAM and checks the API compatibility.

Run:      python 02-self-hosted-models.py
Verify:   python 02-self-hosted-models.py --verify
"""

from __future__ import annotations

import sys


def vram_budget(params_b: float, quant_bits: int) -> float:
    """Weights at the given precision, in GB."""
    return params_b * quant_bits / 8


def fits(vram_gb: float, total_budget_gb: float) -> bool:
    return vram_gb <= total_budget_gb


def openai_compatible(base_url: str) -> bool:
    """Both Ollama and vLLM expose an OpenAI-compatible API."""
    return "/v1" in base_url


def main() -> None:
    # VRAM budget: a 7B model at 4-bit fits in 16 GB.
    mem_4bit = vram_budget(7.0, 4)
    assert mem_4bit == 3.5, "7B at 4-bit is ~3.5 GB"
    assert fits(mem_4bit, 16.0), "fits in 16 GB"

    # At 16-bit, the same model is ~14 GB.
    mem_16bit = vram_budget(7.0, 16)
    assert mem_16bit == 14.0
    assert fits(mem_16bit, 16.0), "barely fits"

    # A 13B model at 4-bit is ~6.5 GB.
    mem_13b = vram_budget(13.0, 4)
    assert fits(mem_13b, 16.0)

    # Both Ollama and vLLM expose an OpenAI-compatible API.
    assert openai_compatible("http://localhost:11434/v1"), "Ollama"
    assert openai_compatible("http://localhost:8000/v1"), "vLLM"

    print("7B at 4-bit: 3.5 GB; at 16-bit: 14 GB")
    print("the VRAM budget is checked before the run")
    print("Ollama and vLLM are OpenAI-compatible")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

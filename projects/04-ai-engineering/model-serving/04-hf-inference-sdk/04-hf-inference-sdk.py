"""
Model Serving — 04: HF Inference SDK
=====================================
Topics: the SDK, model selection, and free-tier limits.

Why this matters:
    The HF Inference SDK calls hosted models. This exercise models the
    free-tier limits and the production path.

Run:      python 04-hf-inference-sdk.py
Verify:   python 04-hf-inference-sdk.py --verify
"""

from __future__ import annotations

import sys


def free_tier_allows(requests: int, limit: int) -> bool:
    """The free tier has a rate limit; exceeding it returns 429."""
    return requests <= limit


def pick_model(candidates: list[dict], task: str, language: str) -> str:
    """Select from the Hub by task and language."""
    matching = [
        c for c in candidates if c["task"] == task and language in c["languages"]
    ]
    assert matching, "no model matches the task and language"
    return min(matching, key=lambda c: c["size"])["name"]


def main() -> None:
    # Free-tier limit: 10 requests/min; the 11th is rejected.
    assert free_tier_allows(10, 10)
    assert not free_tier_allows(11, 10), "rate limit exceeded"

    # Hub selection: match task and language, pick the smallest.
    candidates = [
        {
            "name": "big-model",
            "task": "text-generation",
            "languages": ["en"],
            "size": 7,
        },
        {
            "name": "arabic-small",
            "task": "text-generation",
            "languages": ["ar", "en"],
            "size": 3,
        },
        {
            "name": "embed-model",
            "task": "feature-extraction",
            "languages": ["en"],
            "size": 1,
        },
    ]
    assert pick_model(candidates, "text-generation", "ar") == "arabic-small"

    # Production uses Inference Endpoints, not the free tier.
    assert free_tier_allows(1000, 1000), "dedicated endpoint has no free-tier limit"

    print("free-tier rate limit: 10 requests; the 11th is rejected")
    print("Hub selection: match task and language, pick the smallest")
    print("production uses Inference Endpoints, not the free tier")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

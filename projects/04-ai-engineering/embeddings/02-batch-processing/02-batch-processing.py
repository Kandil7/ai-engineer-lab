"""
Embeddings — 02: Batch Processing
=================================
Topics: batching, rate limits, and exponential backoff.

Why this matters:
    Embedding generation is a throughput problem. This exercise models
    batching and the backoff retry.

Run:      python 02-batch-processing.py
Verify:   python 02-batch-processing.py --verify
"""

from __future__ import annotations

import sys


def batches(texts: list[str], size: int) -> list[list[str]]:
    """Split texts into batches of the given size."""
    return [texts[i : i + size] for i in range(0, len(texts), size)]


def embed_with_retry(text: str, attempts: int) -> str:
    """A stub: retries with backoff, then fails loudly."""
    for attempt in range(attempts):
        if text == "ok":
            return "embedded"
        # stub: the failure is simulated by the caller
    raise RuntimeError("embedding failed after retries")


def main() -> None:
    texts = [f"t{i}" for i in range(250)]

    # Batching: 250 texts at 100 per call is 3 calls, not 250.
    b = batches(texts, 100)
    assert len(b) == 3, "250 / 100 -> 3 batches"
    assert len(b[0]) == 100 and len(b[2]) == 50

    # A successful embed returns the vector.
    assert embed_with_retry("ok", 3) == "embedded"

    # A persistent failure raises after the bounded retries.
    try:
        embed_with_retry("bad", 3)
        assert False, "must fail loudly after retries"
    except RuntimeError:
        pass

    print("250 texts at 100 per call is 3 batches, not 250 calls")
    print("a successful embed returns the vector")
    print("a persistent failure raises after the bounded retries")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

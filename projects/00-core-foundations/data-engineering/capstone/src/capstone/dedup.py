"""Two-pass dedup: exact by key, then approximate by MinHash LSH (stdlib only).

YOUR TURN: implement all three functions. Topic 17 is the reference
implementation of the same algorithm at teaching scale; you may reuse its ideas
but this module must be self-contained (no cross-topic imports).
"""

from __future__ import annotations


def dedup_exact(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep the FIRST row per ``passage_id``, drop later repeats. Order kept."""
    raise NotImplementedError("YOUR TURN: implement dedup_exact (keep-first by key)")


def _shingles(text: str, k: int) -> set[str]:
    """Character k-shingles of ``text`` (empty text -> empty set)."""
    raise NotImplementedError("YOUR TURN: implement _shingles")


def minhash_dedup(
    rows: list[dict[str, str]],
    *,
    k: int = 5,
    num_perm: int = 128,
    bands: int = 16,
    band_rows: int = 8,
    threshold: float = 0.8,
    seed: int = 42,
) -> tuple[list[dict[str, str]], list[str], float]:
    """Approximate dedup; return ``(kept, removed_ids, ratio_removed)``.

    Contract (implementation-agnostic, this is what the tests pin):
    - ``kept`` is a subsequence of ``rows`` (subset, input order kept).
    - Any two rows with identical shingle sets always collapse to one survivor
      (identical signatures share every LSH band, estimated Jaccard 1.0).
    - Rows with empty text are SKIPPED (left for the quality gates), never merged.
    - Every removed row must share exact Jaccard >= ``threshold - 0.25`` with a
      surviving-or-earlier row (tolerance band honors estimation variance).
    - ``ratio_removed == len(removed_ids) / len(rows)`` exactly.
    - Deterministic for fixed ``(k, num_perm, bands, band_rows, threshold, seed)``:
      seed every hash permutation from ``seed`` (no bare ``hash()`` — its seed
      is randomized per process; use ``hashlib``).
    """
    raise NotImplementedError(
        "YOUR TURN: implement minhash_dedup (signatures + LSH + filter)"
    )

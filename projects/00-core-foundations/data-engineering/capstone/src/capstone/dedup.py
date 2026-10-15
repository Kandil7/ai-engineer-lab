"""Two-pass dedup: exact by key, then approximate by MinHash LSH (stdlib only).

Reference implementation. Topic 17 is the same algorithm at teaching scale;
this module is self-contained (no cross-topic imports).
"""

from __future__ import annotations

import hashlib


def dedup_exact(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    """Keep the FIRST row per ``passage_id``, drop later repeats. Order kept."""
    seen: set[str] = set()
    kept: list[dict[str, str]] = []
    for row in rows:
        if row["passage_id"] not in seen:
            seen.add(row["passage_id"])
            kept.append(row)
    return kept


def _shingles(text: str, k: int) -> set[str]:
    """Character k-shingles of whitespace-normalized ``text``."""
    norm = " ".join(text.split())
    if not norm:
        return set()
    if len(norm) < k:
        return {norm}
    return {norm[i : i + k] for i in range(len(norm) - k + 1)}


def _perm_value(seed: int, perm: int, shingle: str) -> int:
    """One MinHash permutation value: sha256 over (seed, perm, shingle)."""
    digest = hashlib.sha256(f"{seed}:{perm}:{shingle}".encode()).hexdigest()
    return int(digest, 16)


def _signature(shingles: set[str], num_perm: int, seed: int) -> list[int] | None:
    """MinHash signature (minima per permutation); None for empty sets."""
    if not shingles:
        return None
    return [
        min(_perm_value(seed, perm, s) for s in shingles) for perm in range(num_perm)
    ]


def _lsh_candidates(
    signatures: list[list[int] | None], bands: int, band_rows: int
) -> set[tuple[int, int]]:
    """Index signatures into LSH buckets; return candidate index pairs."""
    buckets: dict[tuple[int, ...], list[int]] = {}
    for idx, sig in enumerate(signatures):
        if sig is None:
            continue
        usable = sig[: bands * band_rows]
        for band in range(bands):
            key = tuple(usable[band * band_rows : (band + 1) * band_rows])
            buckets.setdefault(key, []).append(idx)
    pairs: set[tuple[int, int]] = set()
    for members in buckets.values():
        for a_pos in range(len(members)):
            for b_pos in range(a_pos + 1, len(members)):
                pairs.add((members[a_pos], members[b_pos]))
    return pairs


def _estimated_jaccard(a: list[int], b: list[int]) -> float:
    """Fraction of equal signature positions (MinHash Jaccard estimate)."""
    return sum(1 for x, y in zip(a, b) if x == y) / len(a)


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
    if not rows:
        return [], [], 0.0
    shingle_sets = [_shingles(r["text"], k) for r in rows]
    signatures = [_signature(s, num_perm, seed) for s in shingle_sets]
    pairs = _lsh_candidates(signatures, bands, band_rows)

    # Union-find over merges: estimated Jaccard >= threshold joins components.
    parent = list(range(len(rows)))

    def find(x: int) -> int:
        while parent[x] != x:
            parent[x] = parent[parent[x]]
            x = parent[x]
        return x

    def union(a: int, b: int) -> None:
        ra, rb = find(a), find(b)
        if ra != rb:
            parent[max(ra, rb)] = min(ra, rb)

    for a, b in pairs:
        sig_a, sig_b = signatures[a], signatures[b]
        assert sig_a is not None and sig_b is not None  # candidates are non-empty
        if _estimated_jaccard(sig_a, sig_b) >= threshold:
            union(a, b)

    # Keep the lowest-index member of each component (input order kept).
    survivor: dict[int, int] = {}
    for i in range(len(rows)):
        root = find(i)
        if root not in survivor or i < survivor[root]:
            survivor[root] = i
    keep_idx = sorted(survivor.values())
    keep_set = set(keep_idx)
    kept = [rows[i] for i in keep_idx]
    removed_ids = [rows[i]["passage_id"] for i in range(len(rows)) if i not in keep_set]
    return kept, removed_ids, len(removed_ids) / len(rows)

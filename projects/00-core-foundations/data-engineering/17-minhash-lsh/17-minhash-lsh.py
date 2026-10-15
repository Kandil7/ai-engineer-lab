"""
Data Engineering — 17: MinHash LSH for near-duplicate dedup
============================================================
Topics: shingling, MinHash signatures, LSH banding, two-pass dedup order.

Why this matters: exact hashing misses near-duplicates, so this exercise
finds them with stdlib-only MinHash plus LSH banding on a labelled corpus.
Production path: datasketch (MinHash, MinHashLSH threshold/num_perm); this
teaching implementation per ADR-0012 is STDLIB ONLY, never production code.

Run:      python 17-minhash-lsh.py
Verify:   python 17-minhash-lsh.py --verify
"""

import hashlib
import sys

SEED = 42
NUM_PERM = 128
BANDS = 32
ROWS = 4
SHINGLE_K = 5

D1 = "العلم نور يهدي صاحبه الى الخير والعمل الصالح وطلب المعرفة فضيلة عظيمة"
D2 = "العلم نور يهدي صاحبه الى الخير والعمل الصالح وطلب المعرفة فضيلة كبيرة"
D4 = "القطار السريع يعبر الصحراء ليلا حاملا البضائع الى الميناء البعيد"
D5 = "يحتاج النبات الى الماء وضوء الشمس لينمو ويزهر في فصل الربيع"
CORPUS: list[dict] = [
    {"doc_id": "d1", "text": D1},
    {"doc_id": "d2", "text": D2},
    {"doc_id": "d3", "text": D1},
    {"doc_id": "d4", "text": D4},
    {"doc_id": "d5", "text": D5},
]


def shingles(text: str, k: int = SHINGLE_K) -> set[str]:
    """Character k-shingles of text; a short text yields one shingle."""
    text = text.strip()
    grams = {text[i : i + k] for i in range(max(len(text) - k + 1, 0))}
    return grams or {text}


def jaccard(a: set[str], b: set[str]) -> float:
    """Exact Jaccard similarity of two shingle sets."""
    union = a | b
    return 1.0 if not union else len(a & b) / len(union)


def minhash_signature(
    shingle_set: set[str], num_perm: int = NUM_PERM, seed: int = SEED
) -> list[int]:
    """MinHash signature: per-permutation minima, seeded and deterministic."""
    signature = []
    for perm in range(num_perm):
        best = min((_perm_hash(s, perm, seed) for s in shingle_set), default=0)
        signature.append(best)
    return signature


def _perm_hash(shingle: str, perm: int, seed: int) -> int:
    """Deterministic hash of one shingle under one seeded permutation."""
    digest = hashlib.sha256(f"{seed}:{perm}:{shingle}".encode("utf-8")).digest()
    return int.from_bytes(digest, "big")


def lsh_candidates(
    signatures: dict[str, list[int]], bands: int = BANDS, rows: int = ROWS
) -> set[tuple[str, str]]:
    """LSH banding: pairs sharing one full band bucket become candidates."""
    buckets: dict[tuple[int, str], list[str]] = {}
    for doc_id, sig in signatures.items():
        for band in range(bands):
            window = tuple(sig[band * rows : (band + 1) * rows])
            key = (band, hashlib.sha256(repr(window).encode("utf-8")).hexdigest())
            buckets.setdefault(key, []).append(doc_id)
    candidates: set[tuple[str, str]] = set()
    for doc_ids in buckets.values():
        for i in range(len(doc_ids)):
            for j in range(i + 1, len(doc_ids)):
                first, second = sorted((doc_ids[i], doc_ids[j]))
                candidates.add((first, second))
    return candidates


def content_hash(text: str) -> str:
    """Topic-05-style exact hash: the first pass hands exact dupes to hashing."""
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def main() -> None:
    by_id = {d["doc_id"]: d["text"] for d in CORPUS}
    sets = {i: shingles(t) for i, t in by_id.items()}
    sigs = {i: minhash_signature(s) for i, s in sets.items()}

    assert sigs["d1"] == minhash_signature(sets["d1"]), "signature deterministic"
    exact = jaccard(sets["d1"], sets["d2"])
    est = sum(1 for x, y in zip(sigs["d1"], sigs["d2"]) if x == y) / NUM_PERM
    assert abs(est - exact) <= 0.15, f"estimate {est:.2f} off exact {exact:.2f}"

    cands = lsh_candidates(sigs)
    assert ("d1", "d2") in cands, "LSH finds the planted near-dupe pair"
    assert ("d4", "d5") not in cands, "LSH must not pair unrelated passages"
    assert content_hash(by_id["d1"]) == content_hash(by_id["d3"]), "exact dupe hash"

    before = len(CORPUS)
    exact_kept: list[str] = []
    seen_hashes: set[str] = set()
    for i, t in by_id.items():
        h = content_hash(t)
        if h not in seen_hashes:
            seen_hashes.add(h)
            exact_kept.append(i)
    assert "d3" not in exact_kept, "exact pass removes the duplicate"
    merged = set(exact_kept)
    for a, b in sorted(cands):
        if a in merged and b in merged:
            merged.discard(b)
    after = len(merged)
    assert after < before, "dedup must remove rows"
    assert "d4" in merged and "d5" in merged, "distinct passages kept"

    print(f"rows before: {before}, rows after: {after}")
    print(f"dedup ratio: {(before - after) / before:.2f} removed")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

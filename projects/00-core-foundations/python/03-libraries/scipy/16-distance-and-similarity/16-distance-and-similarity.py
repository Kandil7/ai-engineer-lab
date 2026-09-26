"""Topic 16: Distance and Similarity (scipy.spatial.distance).

cdist / pdist, euclidean / manhattan / cosine metrics, why cosine
for embeddings, normalization, KD-trees and the curse of
dimensionality, brute force vs ANN.
Why this matters for AI/backend engineering: retrieval (RAG),
deduplication, clustering, and ANN serving all reduce to "rank by
distance" — and the metric + representation choice decides whether
that ranking means anything.

Run:  python 03-libraries/scipy/16-distance-and-similarity.py
"""

import os

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
from scipy.spatial import cKDTree
from scipy.spatial.distance import cdist, pdist, squareform

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy")
os.makedirs(OUT, exist_ok=True)

rng = np.random.default_rng(42)

# ---------------------------------------------------------------------------
# Example 1: pdist + squareform -- all pairwise distances
# ---------------------------------------------------------------------------
X = rng.normal(size=(6, 3))
D_cond = pdist(X, metric="euclidean")
D = squareform(D_cond)
print("# Example 1: pdist / squareform")
print(f"   pdist -> {D_cond.shape} (n(n-1)/2), squareform -> {D.shape}")
print(f"   symmetric? {np.allclose(D, D.T)}   zero diagonal? {np.allclose(np.diag(D), 0)}")

# ---------------------------------------------------------------------------
# Example 2: cdist -- query x reference
# ---------------------------------------------------------------------------
Y = rng.normal(size=(4, 3))
De = cdist(X, Y, metric="euclidean")
Dm = cdist(X, Y, metric="cityblock")  # manhattan
Dc = cdist(X, Y, metric="cosine")  # 1 - cosine similarity
print("# Example 2: cdist metrics")
print(f"   euclidean {De.shape}, cityblock {Dm.shape}, cosine {Dc.shape}")
print(f"   nearest ref for query 0 (euclidean): {int(np.argmin(De[0]))}")

# ---------------------------------------------------------------------------
# Example 3: cosine vs euclidean on unit vectors
# ---------------------------------------------------------------------------
Xu = X / np.linalg.norm(X, axis=1, keepdims=True)
cos = squareform(pdist(Xu, metric="cosine"))
eu2 = squareform(pdist(Xu, metric="euclidean")) ** 2
print("# Example 3: cosine and euclidean on unit vectors")
print(f"   cosine == euclidean^2 / 2? {np.allclose(cos, eu2 / 2, atol=1e-12)}")
print("   identical ranking; euclidean on raw vectors is NOT comparable to cosine")

# ---------------------------------------------------------------------------
# Example 4: why cosine for embeddings -- scale invariance
# ---------------------------------------------------------------------------
a = np.array([1.0, 0.0])
b = np.array([0.9, 0.1])
print("# Example 4: scale invariance")
print(f"   cos(a, 2a) = {cdist([a], [2 * a], 'cosine')[0, 0]:.4f} (identical direction)")
print(f"   euclid(a, 2a) = {cdist([a], [2 * a], 'euclidean')[0, 0]:.4f} (magnitude dominates)")
print("   document length is magnitude: cosine ignores it, euclidean does not")

# ---------------------------------------------------------------------------
# Example 5: normalize then rank with euclidean
# ---------------------------------------------------------------------------
q = rng.normal(size=(1, 3))
D_qcos = cdist(q, X, metric="cosine")
D_qeuc = cdist(q / np.linalg.norm(q), Xu, metric="euclidean")
print("# Example 5: normalize-then-euclidean == cosine ranking")
print(f"   rankings identical? {np.array_equal(np.argsort(D_qcos[0]), np.argsort(D_qeuc[0]))}")

# ---------------------------------------------------------------------------
# Example 6: cKDTree -- exact neighbors in low dimensions
# ---------------------------------------------------------------------------
pts = rng.uniform(size=(500, 2))
queries = rng.uniform(size=(3, 2))
tree = cKDTree(pts)
dist, idx = tree.query(queries, k=3)
brute = np.sort(cdist(queries, pts), axis=1)[:, :3]
print("# Example 6: cKDTree vs brute force")
print(f"   kd distances == sorted brute-force distances? {np.allclose(dist, brute, atol=1e-12)}")

# ---------------------------------------------------------------------------
# Example 7: the curse of dimensionality -- contrast collapse
# ---------------------------------------------------------------------------
dims = [2, 4, 8, 16, 32, 64, 128]
spreads = []
for d in dims:
    V = rng.normal(size=(2000, d))
    V /= np.linalg.norm(V, axis=1, keepdims=True)
    Dd = squareform(pdist(V, metric="cosine"))
    spreads.append(Dd.std())
    if d in (2, 128):
        print(
            f"   d={d}: mean dist={Dd.mean():.3f}  "
            f"spread={Dd.std():.3f} (1/sqrt(d)={1 / np.sqrt(d):.3f})"
        )
print("# Example 7: curse of dimensionality")
print("   random unit vectors are ~orthogonal; the distance SPREAD shrinks as 1/sqrt(d)")
print("   -> nearest and farthest neighbors become indistinguishable")

fig, ax = plt.subplots(figsize=(6, 4))
ax.semilogx(dims, spreads, "o-")
ax.set_xlabel("dimension d")
ax.set_ylabel("std of pairwise cosine distance")
ax.set_title("Curse of dimensionality: contrast collapse")
fig.tight_layout()
fig.savefig(os.path.join(OUT, "scipy_16_curse.png"), dpi=100)
print("Plot saved: outputs/scipy/scipy_16_curse.png")

# ---------------------------------------------------------------------------
# Example 8: brute force vs kd-tree -- low vs high dimensions
# ---------------------------------------------------------------------------
n = 20000
queries_n = 800
for d in (2, 64):
    P = rng.normal(size=(n, d))
    Q = rng.normal(size=(queries_n, d))
    t0 = __import__("time").perf_counter()
    cdist(Q, P)
    t_brute = __import__("time").perf_counter() - t0
    t0 = __import__("time").perf_counter()
    cKDTree(P).query(Q, k=3)
    t_kd = __import__("time").perf_counter() - t0
    print(
        f"   d={d}: brute {t_brute:.2f}s, kd-tree {t_kd:.2f}s "
        f"-> kd {'faster' if t_kd < t_brute else 'slower (~brute force)'}"
    )
print("# Example 8: kd-trees help in low dims only")
print(
    "   in 64+ dims the kd-tree degenerates and is slower than brute force (hence ANN: HNSW, IVF)"
)


# ---------------------------------------------------------------------------
def _verify():
    """Assert the facts the examples demonstrate."""
    Df = squareform(pdist(X))
    assert np.allclose(Df, Df.T) and np.allclose(np.diag(Df), 0)
    assert De.shape == (6, 4) and Dm.shape == (6, 4) and Dc.shape == (6, 4)
    assert np.allclose(cos, eu2 / 2, atol=1e-12)
    assert np.isclose(cdist([a], [2 * a], "cosine")[0, 0], 0.0, atol=1e-12)
    assert not np.isclose(cdist([a], [2 * a], "euclidean")[0, 0], 0.0)
    assert np.array_equal(np.argsort(D_qcos[0]), np.argsort(D_qeuc[0]))
    assert np.allclose(dist, brute, atol=1e-12)
    std2, std128 = spreads[0], spreads[-1]
    assert std2 > 0.5 and std128 < 0.2, "contrast must collapse"
    assert std128 < 0.35 * std2, "1/sqrt(d) scaling must hold"
    print("\n[OK] all 8 checks passed")


if __name__ == "__main__":
    _verify()

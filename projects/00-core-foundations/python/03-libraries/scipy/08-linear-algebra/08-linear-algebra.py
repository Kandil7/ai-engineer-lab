"""
08 - SciPy Linear Algebra
==========================
SciPy's linalg module provides advanced linear algebra operations
beyond what NumPy offers, including matrix decompositions, solvers,
and matrix functions.

Topics:
- Solving linear systems (Ax = b)
- Matrix decompositions (LU, QR, Cholesky, SVD)
- Eigenvalue problems
- Matrix functions (expm, logm, sqrtm)
"""

import numpy as np

# Ensure output directory exists (Tier 0 fix: Windows + CI)
import os

OUT_DIR = os.path.join(
    os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "outputs", "scipy"
)
os.makedirs(OUT_DIR, exist_ok=True)

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy import linalg

# ============================================================
# Example 1: Solving Linear Systems
# ============================================================
print("=" * 60)
print("Example 1: Solving Linear Systems Ax = b")
print("=" * 60)

# 3x3 system
A = np.array(
    [
        [3, 1, -1],
        [1, 4, 2],
        [-1, 2, 5],
    ]
)
b = np.array([1, 2, 3])

# Direct solve
x = linalg.solve(A, b)
print("System:")
print(f"  3x + y - z = 1")
print(f"  x + 4y + 2z = 2")
print(f"  -x + 2y + 5z = 3")
print(f"\nSolution: x={x[0]:.4f}, y={x[1]:.4f}, z={x[2]:.4f}")
print(f"Verification AÂ·x = {A @ x} (should equal b = {b})")

# Check if system is well-conditioned
cond = np.linalg.cond(A)
print(f"Condition number: {cond:.2f}")
print(f"System is {'well-conditioned' if cond < 100 else 'ill-conditioned'}")

# Larger random system
np.random.seed(42)
n = 100
A_large = np.random.randn(n, n) + n * np.eye(n)  # Well-conditioned
b_large = np.random.randn(n)
x_large = linalg.solve(A_large, b_large)
residual = np.linalg.norm(A_large @ x_large - b_large)
print(f"\n100x100 system: residual = {residual:.2e}")

# ============================================================
# Example 2: LU Decomposition
# ============================================================
print("\n" + "=" * 60)
print("Example 2: LU Decomposition (A = PLU)")
print("=" * 60)

A_lu = np.array(
    [
        [2, 1, 1],
        [4, 3, 3],
        [8, 7, 9],
    ]
)

# LU decomposition with partial pivoting
P, L, U = linalg.lu(A_lu)
print("A = PLU decomposition:")
print(f"  P (permutation) =\n{P}")
print(f"  L (lower triangular) =\n{L}")
print(f"  U (upper triangular) =\n{U}")

# Verify: P @ L @ U should equal A
reconstructed = P @ L @ U
print(f"\nReconstruction error: {np.max(np.abs(reconstructed - A_lu)):.2e}")

# Solve using LU factors (useful for multiple right-hand sides)
b_lu = np.array([1, 2, 3])
from scipy.linalg import solve_triangular

y = solve_triangular(L, P.T @ b_lu, lower=True)
x_lu = solve_triangular(U, y, lower=False)
print(f"Solution via LU: {x_lu}")
print(f"Verify: {A_lu @ x_lu}")

# ============================================================
# Example 3: Eigenvalue Problems
# ============================================================
print("\n" + "=" * 60)
print("Example 3: Eigenvalue and Eigenvector Computation")
print("=" * 60)

# Symmetric matrix (real eigenvalues)
A_sym = np.array(
    [
        [4, 1, 0],
        [1, 3, 1],
        [0, 1, 2],
    ]
)

eigenvalues, eigenvectors = linalg.eigh(A_sym)
print("Symmetric matrix eigenvalues:")
for i, (val, vec) in enumerate(zip(eigenvalues, eigenvectors.T)):
    print(f"  lambda_{i + 1} = {val:.6f}")
    print(f"    eigenvector = {vec}")

# Verify: A @ v = Î» * v
print(f"\nVerification:")
for i in range(len(eigenvalues)):
    lhs = A_sym @ eigenvectors[:, i]
    rhs = eigenvalues[i] * eigenvectors[:, i]
    print(f"  |A*v_{i + 1} - lambda*v_{i + 1}| = {np.linalg.norm(lhs - rhs):.2e}")

# General (non-symmetric) eigenvalues
A_gen = np.array(
    [
        [1, 2],
        [3, 1],
    ]
)
eigvals, eigvecs = linalg.eig(A_gen)
print(f"\nGeneral matrix eigenvalues: {eigvals}")

# Visualize eigenvalues in complex plane
fig, ax = plt.subplots(figsize=(6, 6))
ax.plot(eigvals.real, eigvals.imag, "ro", markersize=10)
ax.axhline(y=0, color="k", linewidth=0.5)
ax.axvline(x=0, color="k", linewidth=0.5)
ax.set_xlabel("Real part")
ax.set_ylabel("Imaginary part")
ax.set_title("Eigenvalues in Complex Plane")
ax.grid(True, alpha=0.3)
ax.set_aspect("equal")
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_08_eigenvalues.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_08_eigenvalues.png')}")

# ============================================================
# Example 4: Singular Value Decomposition (SVD)
# ============================================================
print("\n" + "=" * 60)
print("Example 4: Singular Value Decomposition (SVD)")
print("=" * 60)

# Create a rank-3 matrix with some structure
np.random.seed(42)
m, n = 100, 80
A_svd = np.random.randn(m, 3) @ np.random.randn(3, n) + 0.1 * np.random.randn(m, n)

# Full SVD
U, s, Vh = linalg.svd(A_svd, full_matrices=False)
print(f"Matrix shape: {A_svd.shape}")
print(f"Number of singular values: {len(s)}")
print(f"Top 5 singular values: {s[:5]}")
print(f"Total energy captured by top 3: {s[:3].sum() / s.sum() * 100:.2f}%")

# Rank-k approximation
fig, axes = plt.subplots(1, 4, figsize=(16, 3))
ranks = [1, 3, 10, 50]
for ax, k in zip(axes, ranks):
    A_k = U[:, :k] @ np.diag(s[:k]) @ Vh[:k, :]
    ax.imshow(A_k, cmap="coolwarm", aspect="auto")
    error = np.linalg.norm(A_svd - A_k) / np.linalg.norm(A_svd)
    ax.set_title(f"Rank-{k}\nRel. error: {error:.3f}")
    ax.set_xticks([])
    ax.set_yticks([])
plt.suptitle("Low-Rank Approximation via SVD", fontsize=14)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_08_svd.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_08_svd.png')}")

# Scree plot (singular value spectrum)
fig, ax = plt.subplots(figsize=(8, 4))
ax.semilogy(range(1, len(s) + 1), s, "bo-", linewidth=2, markersize=5)
ax.axvline(x=3, color="r", linestyle="--", alpha=0.7, label="Rank-3 cutoff")
ax.set_title("Singular Value Spectrum (Scree Plot)")
ax.set_xlabel("Index")
ax.set_ylabel("Singular Value (log)")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_08_scree.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_08_scree.png')}")

# ============================================================
# Example 5: Matrix Decompositions
# ============================================================
print("\n" + "=" * 60)
print("Example 5: Cholesky, QR, and Matrix Functions")
print("=" * 60)

# --- Cholesky Decomposition (for positive definite matrices) ---
A_pd = np.array(
    [
        [4, 2, -2],
        [2, 10, 4],
        [-2, 4, 10],
    ]
)

L_chol = linalg.cholesky(A_pd, lower=True)
print("Cholesky Decomposition (A = LÂ·L^T):")
print(f"  L =\n{L_chol}")
print(f"  Reconstruction error: {np.max(np.abs(L_chol @ L_chol.T - A_pd)):.2e}")

# --- QR Decomposition ---
A_qr = np.random.randn(5, 3)
Q, R = linalg.qr(A_qr)
print(f"\nQR Decomposition:")
print(f"  A shape: {A_qr.shape}, Q shape: {Q.shape}, R shape: {R.shape}")
print(f"  Q orthogonal check: |Q^T*Q - I| = {np.max(np.abs(Q.T @ Q - np.eye(Q.shape[1]))):.2e}")
print(f"  Reconstruction: |Q*R - A| = {np.max(np.abs(Q @ R - A_qr)):.2e}")

# --- Matrix Exponential ---
A_exp = np.array(
    [
        [0, 1],
        [-1, 0],
    ]
)
exp_A = linalg.expm(A_exp)
print(f"\nMatrix exponential exp(A) for A = [[0,1],[-1,0]]:")
print(f"  exp(A) =\n{exp_A}")
print(f"  This is a rotation matrix (cos theta, sin theta; -sin theta, cos theta)")

# Visualize matrix exponential effect
fig, ax = plt.subplots(figsize=(6, 6))
circle = np.array([[np.cos(t), np.sin(t)] for t in np.linspace(0, 2 * np.pi, 100)])
transformed = circle @ exp_A.T
ax.plot(circle[:, 0], circle[:, 1], "b-", linewidth=2, label="Original circle")
ax.plot(transformed[:, 0], transformed[:, 1], "r--", linewidth=2, label="exp(A)Â·circle")
ax.set_xlim(-2, 2)
ax.set_ylim(-2, 2)
ax.set_aspect("equal")
ax.set_title("Effect of Matrix Exponential")
ax.legend()
ax.grid(True, alpha=0.3)
plt.tight_layout()
plt.savefig(
    os.path.join(OUT_DIR, "scipy_08_expm.png"),
    dpi=100,
)
print("Plot saved: {os.path.join(OUT_DIR, 'scipy_08_expm.png')}")

# --- Matrix square root ---
M = np.array([[4, 2], [2, 5]])
sqrt_M = linalg.sqrtm(M)
print(f"\nMatrix square root of [[4,2],[2,5]]:")
print(f"  sqrt(M) =\n{sqrt_M.real}")
print(f"  sqrt(M) @ sqrt(M) =\n{(sqrt_M @ sqrt_M).real}")

print("\n[OK] SciPy linear algebra covered!")
print("   Next: 09-fft.py for Fourier transforms.")

"""
07-machine-learning — 44: JAX and Flax — Functional Transforms and Composability
================================================================================
Topics: the functional view, jit/grad/vmap transforms, Flax init/apply,
        PyTorch-vs-JAX tradeoffs

Why this matters for AI/backend engineering:
    JAX's model-as-pure-function + composable transforms is the mental model
    behind TPU-scale research. Learning the ideas (grad, vmap, jit) sharpens
    how you reason about any framework.

Note: JAX is not installed in this environment, so we run the transform
*philosophy* on PyTorch's analogues (autograd.grad, torch.vmap, torch.compile)
and map each back to its JAX counterpart.

Run:      python 44-jax-flax.py
Verify:   python 44-jax-flax.py --verify
Reference: https://jax.readthedocs.io/
"""

from __future__ import annotations

import torch
import torch.nn as nn

torch.manual_seed(0)


# ============================================================
# 1. The functional view: parameters as a value, model as a pure function
# ============================================================
def predict(params, x):
    """Pure: same (params, x) -> same output, no hidden state."""
    return torch.tanh(params["W"] @ x + params["b"])


params = {"W": torch.randn(3, 4), "b": torch.randn(3)}
x = torch.randn(4)
print("Example 1: the functional view")
print(f"  predict(params, x) -> {tuple(predict(params, x).shape)}")
print("  params is a plain value; predict is a pure function")


# ============================================================
# 2. grad — differentiate a function (JAX: jax.grad)
# ============================================================
def loss(params, x, y):
    return ((predict(params, x) - y) ** 2).sum()


y = torch.randn(3)
x.requires_grad_(True)
grads = torch.autograd.grad(loss(params, x, y), x)[0]  # JAX: jax.grad(loss)(params, x, y)
print("\nExample 2: grad")
print(f"  autograd.grad -> d loss / d x shape {tuple(grads.shape)}")
print("  JAX equivalent: jax.grad(loss)(params, x, y)")

# ============================================================
# 3. vmap — vectorize over a batch (JAX: jax.vmap)
# ============================================================
X_batch = torch.randn(5, 4)  # 5 inputs
# vmap over the data (dim 0), params held fixed (None)
batched = torch.vmap(lambda xb: predict(params, xb), in_dims=(0,))(X_batch)
print("\nExample 3: vmap")
print(f"  torch.vmap over batch -> {tuple(batched.shape)}")
print("  JAX equivalent: jax.vmap(predict, in_axes=(None, 0))(params, X_batch)")

# ============================================================
# 4. jit — compile (JAX: jax.jit)
# ============================================================
print("\nExample 4: jit")
print("  JAX: jax.jit(predict) traces once and compiles to XLA")
print("  PyTorch analogue: torch.compile(predict) (needs a C++ toolchain)")
print("  first call compiles; later calls reuse the compiled kernel")


# ============================================================
# 5. Flax init/apply — params made, then applied
# ============================================================
class MLP(nn.Module):  # Flax: flax.linen.nn.Module
    def __init__(self):
        super().__init__()
        self.d1 = nn.Linear(4, 8)
        self.d2 = nn.Linear(8, 1)

    def forward(self, x):
        return self.d2(torch.relu(self.d1(x)))


mlp = MLP()
# Flax separates init (make params) from apply (run forward on params):
params_dict = mlp.state_dict()  # Flax: params = MLP().init(rng, x)
print("\nExample 5: Flax init/apply")
print(f"  init -> state_dict keys: {list(params_dict.keys())}")
print(f"  apply -> MLP().apply(params, x) -> {tuple(mlp(x).shape)}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Model = pure function of (params, x); params are a value")
print("- jit compiles, grad differentiates, vmap vectorizes — and they compose")
print("- Flax adds init/apply modules while staying functional")
print("- JAX wins at TPU scale; PyTorch remains the ergonomic default")
print("=" * 60)


def _verify() -> None:
    assert predict(params, x).shape == (3,)
    assert grads.shape == (4,)
    assert batched.shape == (5, 3)
    assert set(params_dict.keys()) == {"d1.weight", "d1.bias", "d2.weight", "d2.bias"}
    assert mlp(x).shape == (1,)
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

"""
07-machine-learning — 43: TensorFlow and Keras — The Declarative Framework
==========================================================================
Topics: declarative vs explicit, Sequential/Functional API, compile/fit,
        SavedModel, framework choice

Why this matters for AI/backend engineering:
    Production ML systems mix frameworks — Keras SavedModels and TF Lite on
    edge, PyTorch in research. Reading both is the skill. The Keras mental
    model (compile + fit hides the loop) is the contrast that makes the
    PyTorch loop's explicit control meaningful.

Note: TensorFlow is not installed in this environment, so we run the Keras
*mental model* in PyTorch — the identical model expressed both ways — and
verify they compute the same shapes and the same abstraction mapping.

Run:      python 43-tensorflow-keras.py
Verify:   python 43-tensorflow-keras.py --verify
Reference: https://keras.io/guides/
"""

from __future__ import annotations

import torch
import torch.nn as nn

torch.manual_seed(0)


# ============================================================
# 1. The Keras mental model, expressed in PyTorch
# ============================================================
# Keras:
#   model = keras.Sequential([Dense(64, activation="relu"), Dense(1)])
#   model.compile(optimizer="adam", loss="mse")
#   model.fit(X, y, epochs=10)
#
# PyTorch (the same thing, loop exposed):
class Model(nn.Module):
    def __init__(self):
        super().__init__()
        self.layers = nn.Sequential(nn.Linear(8, 64), nn.ReLU(), nn.Linear(64, 1))

    def forward(self, x):
        return self.layers(x)


model = Model()
opt = torch.optim.Adam(model.parameters())  # <- compile(optimizer="adam")
loss_fn = nn.functional.mse_loss  # <- compile(loss="mse")

X = torch.randn(32, 8)
y = torch.randn(32, 1)
print("Example 1: compile + fit, mapped to PyTorch")
print("  Keras compile(optimizer='adam', loss='mse')  ==  Adam + mse_loss")
print(f"  input {tuple(X.shape)} -> output {tuple(model(X).shape)}")

# ============================================================
# 2. The training loop Keras's fit hides
# ============================================================
loss = torch.tensor(float("inf"))
for epoch in range(5):
    opt.zero_grad()
    loss = loss_fn(model(X), y)
    loss.backward()
    opt.step()
print("\nExample 2: the loop fit() hides")
print(f"  after 5 epochs, loss = {loss.item():.4f}")

# ============================================================
# 3. Sequential vs Functional — the shape they must agree on
# ============================================================
print("\nExample 3: Sequential vs Functional produce the same shapes")


# A "functional-style" equivalent: explicit calls, no Sequential wrapper
class FunctionalStyle(nn.Module):
    def __init__(self):
        super().__init__()
        self.d1 = nn.Linear(8, 64)
        self.d2 = nn.Linear(64, 1)

    def forward(self, x):
        x = torch.relu(self.d1(x))  # layers as callables
        return self.d2(x)


fs = FunctionalStyle()  # same architecture, expressed with explicit named layers
print(f"  sequential out {tuple(model(X).shape)} == functional out {tuple(fs(X).shape)}")

# ============================================================
# 4. Framework decision table (pure data, no runtime)
# ============================================================
print("\nExample 4: framework choice")
decision = {
    "research / novel loop": "PyTorch",
    "standard supervised task": "Keras",
    "TF Serving / TF Lite edge": "TensorFlow/Keras",
    "LLM tooling": "PyTorch",
}
for k, v in decision.items():
    print(f"  {k:>28} -> {v}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Keras is declarative: describe the model, fit runs the loop")
print("- PyTorch is explicit: you own zero_grad/backward/step")
print("- Sequential = linear stacks; Functional = branched graphs")
print("- The choice is ecosystem + ergonomics, never raw capability")
print("=" * 60)


def _verify() -> None:
    assert model(X).shape == (32, 1)
    assert fs(X).shape == (32, 1)
    # Sequential and Functional express the same architecture: same output shape
    assert model(X).shape == fs(X).shape, "equivalent architectures must match in shape"
    assert loss.item() < 1e6, "training must not diverge"
    assert decision["research / novel loop"] == "PyTorch"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

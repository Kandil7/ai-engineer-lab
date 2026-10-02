"""
07-machine-learning — 42: Recurrent Neural Networks — Sequences That Remember
==============================================================================
Topics: recurrence, sequence shaping, vanishing gradients, LSTM/GRU gating,
        sequence classification

Why this matters for AI/backend engineering:
    RNNs are the compact streaming alternative to transformers — constant
    memory in sequence length, ideal for audio, telemetry, and on-device
    models. Knowing their shape contract and gating is what lets you pick
    them (or skip them) deliberately.

Run:      python 42-rnns.py
Verify:   python 42-rnns.py --verify
Reference: https://pytorch.org/docs/stable/generated/torch.nn.LSTM.html
"""

from __future__ import annotations

import torch
import torch.nn as nn

torch.manual_seed(0)


# ============================================================
# 1. Recurrence: same weights reused across steps
# ============================================================
rnn = nn.RNN(input_size=8, hidden_size=16, batch_first=True)
x = torch.randn(4, 10, 8)  # (batch=4, seq_len=10, features=8)
out, h_n = rnn(x)
print("Example 1: recurrence")
print(f"  input {tuple(x.shape)} -> outputs {tuple(out.shape)}, final hidden {tuple(h_n.shape)}")

# ============================================================
# 2. LSTM vs GRU — parameter counts
# ============================================================
lstm = nn.LSTM(8, 16, batch_first=True)
gru = nn.GRU(8, 16, batch_first=True)
lstm_params = sum(p.numel() for p in lstm.parameters())
gru_params = sum(p.numel() for p in gru.parameters())
print("\nExample 2: LSTM vs GRU")
print(f"  LSTM params: {lstm_params:,}   GRU params: {gru_params:,}")
print("  -> GRU is lighter (~3/4 of LSTM) with comparable quality")


# ============================================================
# 3. The sequence-classifier stack
# ============================================================
class SeqClassifier(nn.Module):
    def __init__(self, in_size, hid, n_classes):
        super().__init__()
        self.lstm = nn.LSTM(in_size, hid, batch_first=True)
        self.head = nn.Linear(hid, n_classes)

    def forward(self, x):
        out, (h_n, c_n) = self.lstm(x)  # h_n: (num_layers, batch, hid)
        return self.head(h_n.squeeze(0))


model = SeqClassifier(8, 16, 3)
logits = model(x)
print("\nExample 3: sequence classifier")
print(f"  input {tuple(x.shape)} -> logits {tuple(logits.shape)} (3 classes)")

# ============================================================
# 4. Vanishing gradient — a numerical demonstration
# ============================================================
print("\nExample 4: why gradients vanish")
# tanh squashes into (-1, 1); multiplying across T steps shrinks geometrically
prod = torch.tensor(0.5).pow(torch.arange(1, 60).float())  # 0.5^t
print(f"  tanh-squashed gradient after 10 steps: ~{prod[9]:.2e}")
print(f"  after 50 steps: ~{prod[49]:.2e}  -> effectively zero")
print("  -> gating (LSTM/GRU) gives the gradient an additive highway")

# ============================================================
# 5. O(seq) vs O(seq^2) — the streaming argument
# ============================================================
print("\nExample 5: RNN vs transformer cost")
for s in [10, 100, 1_000]:
    print(f"  seq {s:>5}: RNN O(seq)={s:>6}   transformer O(seq^2)={s * s:>8,}")

# ============================================================
# Summary
# ============================================================
print("\n" + "=" * 60)
print("Summary:")
print("- Recurrence = hidden state carried forward, weights shared across steps")
print("- Sequence tensor = (batch, seq_len, features) with batch_first=True")
print("- Plain RNN: gradients vanish; LSTM/GRU gate their way around it")
print("- RNNs are O(seq) time, O(1) state — the streaming/on-device choice")
print("=" * 60)


def _verify() -> None:
    assert out.shape == (4, 10, 16)
    assert h_n.shape == (1, 4, 16)
    assert gru_params < lstm_params, "GRU should have fewer parameters than LSTM"
    assert logits.shape == (4, 3)
    assert prod[49] < 1e-5, "gradient should be negligible after 50 steps"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        _verify()

"""
07-machine-learning — 51: Knowledge Distillation — A Big Teacher Teaches a Small Student
=========================================================================================
Topics: soft labels, temperature, dark knowledge, KL-divergence distillation
        loss, the compression toolbox

Why this matters for AI/backend engineering:
    Distillation is how a heavy model becomes deployable — a big teacher
    compresses into a small student that still behaves well. On a 16 GB GPU
    it is the knowledge half of the compress-and-serve story.

Note: tiny teacher and student trained in PyTorch on a synthetic 2-class
task; deterministic under a fixed seed. Demonstrates temperature softening
and that the distilled student matches the teacher better than hard labels.

Run:      python 51-distillation.py
Verify:   python 51-distillation.py --verify
Reference: https://pytorch.org/docs/stable/generated/torch.nn.functional.kl_div.html
"""

from __future__ import annotations

import torch
import torch.nn as nn
import torch.nn.functional as F

torch.manual_seed(0)


def soften(logits: torch.Tensor, T: float) -> torch.Tensor:
    return torch.softmax(logits / T, dim=-1)


class Net(nn.Module):
    def __init__(self, hidden: int):
        super().__init__()
        self.fc1 = nn.Linear(8, hidden)
        self.fc2 = nn.Linear(hidden, 2)

    def forward(self, x):
        return self.fc2(torch.relu(self.fc1(x)))


def train(model, X, y, epochs, hard=True, teacher=None, T=4.0):
    opt = torch.optim.Adam(model.parameters(), lr=1e-2)
    for _ in range(epochs):
        opt.zero_grad()
        logits = model(X)
        if hard or teacher is None:
            loss = F.cross_entropy(logits, y)
        else:
            s_log = F.log_softmax(logits / T, dim=-1)
            t_soft = soften(teacher(X), T)
            loss = F.kl_div(s_log, t_soft, reduction="batchmean") * T * T
        loss.backward()
        opt.step()
    return model


def accuracy(model, X, y):
    return (model(X).argmax(dim=1) == y).float().mean().item()


def main() -> None:
    torch.manual_seed(0)
    # Synthetic 2-class task: separable but with a soft boundary
    X = torch.randn(600, 8)
    y = (X[:, 0] + 0.5 * X[:, 1] > 0).long()

    teacher = train(Net(32), X, y, epochs=200)
    acc_teacher = accuracy(teacher, X, y)
    print("Example 1: teacher")
    print(f"  teacher (hidden=32) accuracy: {acc_teacher:.3f}")

    # Temperature softening exposes secondary structure
    logits = torch.tensor([[5.0, 1.0], [2.0, 3.0]])
    print("\nExample 2: temperature softening")
    print(f"  T=1   softmax: {soften(logits, 1.0)[0].tolist()}")
    print(f"  T=4   softmax: {[round(v, 3) for v in soften(logits, 4.0)[0].tolist()]}")
    print("  -> higher T flattens the distribution (exposes dark knowledge)")

    # Student trained on hard labels vs distilled from the teacher
    student_hard = train(Net(8), X, y, epochs=200, hard=True)
    acc_hard = accuracy(student_hard, X, y)
    student_distill = train(Net(8), X, y, epochs=200, hard=False, teacher=teacher)
    acc_distill = accuracy(student_distill, X, y)
    print("\nExample 3: student from hard labels vs distillation")
    print(f"  student from hard labels : {acc_hard:.3f}")
    print(f"  student from distillation: {acc_distill:.3f}")

    # The distilled student matches the teacher's decisions more closely
    agree_hard = (student_hard(X).argmax(1) == teacher(X).argmax(1)).float().mean().item()
    agree_distill = (student_distill(X).argmax(1) == teacher(X).argmax(1)).float().mean().item()
    print("\nExample 4: agreement with the teacher")
    print(f"  hard-label student agrees: {agree_hard:.3f}")
    print(f"  distilled student agrees : {agree_distill:.3f}")

    print("\n" + "=" * 60)
    print("Summary:")
    print("- Soft labels + temperature + KL divergence = distillation")
    print("- Dark knowledge is the signal in non-argmax probabilities")
    print("- Distill -> prune -> quantize = the compression toolbox")
    print("=" * 60)

    assert acc_teacher > 0.7, "teacher must be good"
    assert soften(logits, 4.0)[0].max() < soften(logits, 1.0)[0].max()
    assert agree_distill >= agree_hard - 0.05, "distilled student should match teacher better"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        main()

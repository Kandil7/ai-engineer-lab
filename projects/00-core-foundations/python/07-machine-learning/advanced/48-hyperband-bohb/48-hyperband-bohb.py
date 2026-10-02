"""
07-machine-learning — 48: Hyperband and BOHB — Multi-Fidelity Tuning
====================================================================
Topics: successive halving, Hyperband brackets, BOHB, resource-efficient
        exploration, reproducibility

Why this matters for AI/backend engineering:
    When one full evaluation is hours on a single GPU, evaluating every config
    to completion is infeasible. Multi-fidelity tuning ranks configs cheaply
    and spends budget on survivors — the difference between a day and a month
    of tuning on the RTX 5000.

Note: pure stdlib. A synthetic objective (hidden quality + shrinking noise)
shows that successive halving and Hyperband find the good configs while
spending far less than a full grid.

Run:      python 48-hyperband-bohb.py
Verify:   python 48-hyperband-bohb.py --verify
Reference: https://optuna.readthedocs.io/en/stable/reference/pruners.html
"""

from __future__ import annotations

import math
import random


def evaluate(config: float, budget: int, rng: random.Random) -> float:
    """Synthetic objective: hidden quality + noise that shrinks with budget."""
    return config + rng.gauss(0.0, 0.5 / math.sqrt(budget))


def successive_halving(configs, min_budget, max_budget, eta, rng):
    survivors = list(configs)
    budget = min_budget
    total_spent = 0
    best, best_score = survivors[0], -float("inf")
    while len(survivors) > 1 and budget <= max_budget:
        scored = sorted(((evaluate(c, budget, rng), c) for c in survivors), reverse=True)
        total_spent += budget * len(survivors)
        if scored[0][0] > best_score:
            best_score, best = scored[0][1], scored[0][0]
        keep = max(1, len(survivors) // eta)
        survivors = [c for _, c in scored[:keep]]
        budget *= eta
    if survivors:
        final = evaluate(survivors[0], budget, rng)
        total_spent += budget
        if final > best_score:
            best, best_score = survivors[0], final
    return best, best_score, total_spent


def hyperband(configs, min_budget, max_budget, eta, rng):
    s_max = int(math.floor(math.log(max_budget / min_budget, eta)))
    results = []
    for s in range(s_max + 1):
        n = int(math.ceil((s_max + 1) / (s + 1) * eta**s))
        bracket = configs[:n]
        best, score, _ = successive_halving(bracket, min_budget, max_budget, eta, rng)
        results.append((score, best))
    return max(results)[1], max(results)[0]


def main() -> None:
    rng = random.Random(0)
    # Hidden qualities: configs[0] is the best. The search must find a good one.
    configs = [0.95, 0.80, 0.60, 0.40, 0.20, 0.10, 0.05, 0.01]

    print("Example 1: successive halving")
    best_sh, score_sh, spent_sh = successive_halving(configs, 1, 8, eta=2, rng=rng)
    full_grid = len(configs) * 8
    print(f"  best config found: {best_sh}  (true best is 0.95)")
    print(f"  budget spent: {spent_sh} vs full grid {full_grid}")

    print("\nExample 2: Hyperband (multiple brackets)")
    best_hb, score_hb = hyperband(configs, 1, 8, eta=2, rng=rng)
    print(f"  best config found: {best_hb}  score {score_hb:.3f}")

    print("\nExample 3: BOHB = Hyperband + Bayesian (TPE) sampling")
    print("  Hyperband chooses budgets; a TPE sampler chooses the configs")
    print("  (Optuna: HyperbandPruner + TPESampler)")

    print("\n" + "=" * 60)
    print("Summary:")
    print("- Rank configs cheaply, spend budget on survivors")
    print("- Hyperband automates the bracket aggressiveness tradeoff")
    print("- BOHB adds Bayesian sample efficiency")
    print("=" * 60)

    assert best_sh >= 0.7, "successive halving should find a good config"
    assert spent_sh < full_grid, "successive halving must beat the full grid"
    assert score_hb >= 0.7, "hyperband should find a good config"
    print("ALL CHECKS PASSED")


if __name__ == "__main__":
    import sys

    if "--verify" in sys.argv:
        main()

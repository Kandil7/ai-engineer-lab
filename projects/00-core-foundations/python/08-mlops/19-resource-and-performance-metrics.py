"""
MLOps - 19: Resource and Performance Metrics
============================================
Topics: latency percentiles, throughput, resource utilization, the bottleneck
rule, efficiency ratios, and the resource gate.

Why this matters for AI/backend engineering:
    Accuracy does not prove deployability. A model ships only when its latency,
    memory, and cost fit the budget — on a 16 GB card, the VRAM high-water mark
    and the p95 are the numbers that decide.

Run:      python 19-resource-and-performance-metrics.py
Verify:   python 19-resource-and-performance-metrics.py --verify
Reference: https://pytorch.org/tutorials/recipes/recipes/profiler_recipe.html
"""

from __future__ import annotations

import sys


# ============================================================
# 1. Latency Percentiles
# ============================================================
def percentile(latencies: list, q: float) -> float:
    """The p50/p95/p99 from request latencies (ms)."""
    ordered = sorted(latencies)
    k = min(len(ordered) - 1, int(q / 100 * len(ordered)))
    return ordered[k]


# ============================================================
# 2. Throughput
# ============================================================
def throughput(requests: int, seconds: float) -> float:
    """Requests per second."""
    return requests / seconds if seconds else 0.0


# ============================================================
# 3. Utilization and Headroom
# ============================================================
def utilization(used: float, total: float) -> float:
    return used / total if total else 0.0


def headroom(used: float, total: float) -> float:
    """Fraction still free; negative means the budget is exceeded."""
    return (total - used) / total if total else 0.0


# ============================================================
# 4. Efficiency and the Bottleneck
# ============================================================
def efficiency(quality: float, cost: float) -> float:
    """Quality per unit cost — accuracy/ms, /GB, /dollar."""
    return quality / cost if cost else float("inf")


FIXES = {
    "gpu_util": "optimize the model (quantize/prune/distill)",
    "cpu_util": "optimize the data pipeline (loading/preprocessing)",
    "vram": "reduce memory (quantize, smaller batch, prune)",
}


def find_bottleneck(util: dict) -> tuple:
    """The saturated resource names the fix; below 0.9 the system is balanced."""
    top = max(util, key=lambda k: util[k])
    if util[top] >= 0.9:
        return top, FIXES.get(top, "investigate")
    return None, "no saturation; system is balanced"


# ============================================================
# 5. The Resource Gate
# ============================================================
def resource_gate(candidate: dict, limits: dict) -> tuple[bool, str]:
    """Promotion needs accuracy AND resources within budget."""
    if candidate["vram_gb"] > limits["vram_gb"]:
        return False, f"FAIL: VRAM {candidate['vram_gb']} > {limits['vram_gb']}"
    if candidate["latency_p95_ms"] > limits["latency_p95_ms"]:
        return False, f"FAIL: p95 {candidate['latency_p95_ms']} > {limits['latency_p95_ms']}"
    return True, "PASS: resource and latency within budget"


def main() -> None:
    lat = [40, 45, 50, 55, 60, 65, 70, 75, 80, 200]
    print("Example 1: latency percentiles")
    print(f"  p50={percentile(lat, 50)}  p95={percentile(lat, 95)}  p99={percentile(lat, 99)}")
    print(f"  mean={sum(lat) / len(lat):.0f}  (hides the 200 ms tail)")
    assert percentile(lat, 50) == 65
    assert percentile(lat, 95) == 200

    print("\nExample 2: throughput")
    print(f"  1000 requests in 20 s -> {throughput(1000, 20):.0f} rps")
    assert throughput(1000, 20) == 50.0

    print("\nExample 3: utilization and the bottleneck")
    util = {"gpu_util": 0.35, "cpu_util": 0.97, "vram": 0.55}
    name, fix = find_bottleneck(util)
    print(f"  bottleneck: {name} -> {fix}")
    assert name == "cpu_util"

    util2 = {"gpu_util": 0.5, "cpu_util": 0.6, "vram": 0.55}
    assert find_bottleneck(util2)[0] is None

    print("\nExample 4: the VRAM budget (16 GB card)")
    print("  weights 9.2 + cache 2.1 + activations 3.0 = 14.3 GB")
    print(f"  utilization={utilization(14.3, 16.0):.2f}  headroom={headroom(14.3, 16.0):.2f}")
    assert headroom(14.3, 16.0) > 0

    print("\nExample 5: efficiency and the resource gate")
    print(
        f"  0.91 acc at 180 ms vs 0.92 acc at 2000 ms: "
        f"{efficiency(0.91, 180):.1e} vs {efficiency(0.92, 2000):.1e}"
    )
    ok, msg = resource_gate(
        {"vram_gb": 9.2, "latency_p95_ms": 180}, {"vram_gb": 16.0, "latency_p95_ms": 200}
    )
    print(f"  {msg}")
    assert ok
    assert not resource_gate(
        {"vram_gb": 17.0, "latency_p95_ms": 180}, {"vram_gb": 16.0, "latency_p95_ms": 200}
    )[0]

    print("\n--- Summary ---")
    print("1. SLO on the tail (p95/p99), never the mean.")
    print("2. The saturated resource names the fix.")
    print("3. Gate promotion on all four budgets.")


def _verify() -> None:
    lat = [40, 45, 50, 55, 60, 65, 70, 75, 80, 200]
    assert percentile(lat, 50) == 65
    assert percentile(lat, 95) == 200
    assert percentile(lat, 99) == 200

    assert throughput(1000, 20) == 50.0
    assert abs(utilization(14.3, 16.0) - 0.89375) < 1e-9
    assert headroom(17.0, 16.0) < 0  # over budget

    assert find_bottleneck({"gpu_util": 0.35, "cpu_util": 0.97, "vram": 0.55})[0] == "cpu_util"
    assert find_bottleneck({"gpu_util": 0.99, "cpu_util": 0.5})[0] == "gpu_util"
    assert find_bottleneck({"gpu_util": 0.5})[0] is None

    assert efficiency(0.91, 180) > efficiency(0.92, 2000)
    assert resource_gate(
        {"vram_gb": 9.2, "latency_p95_ms": 180}, {"vram_gb": 16.0, "latency_p95_ms": 200}
    )[0]
    assert not resource_gate(
        {"vram_gb": 17.0, "latency_p95_ms": 180}, {"vram_gb": 16.0, "latency_p95_ms": 200}
    )[0]
    print("[OK] 19-resource-and-performance-metrics: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()
        _verify()

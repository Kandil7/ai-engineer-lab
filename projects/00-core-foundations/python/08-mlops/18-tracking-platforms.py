"""
MLOps - 18: Tracking Platforms
==============================
Topics: the run-record contract, a tracker-agnostic adapter, platform
selection, and the managed-vs-self-hosted cost model.

Why this matters for AI/backend engineering:
    The tracker is how runs become comparable and auditable. Programming
    against a contract (not a vendor SDK) keeps the platform swappable, so
    data residency or cost can change the backend without rewriting training.

Run:      python 18-tracking-platforms.py
Verify:   python 18-tracking-platforms.py --verify
Reference: https://mlflow.org/
"""

from __future__ import annotations

import sys
from dataclasses import asdict, dataclass, field


# ============================================================
# 1. The Run-Record Contract
# ============================================================
@dataclass
class RunRecord:
    run_id: str
    config: dict
    metrics: dict
    artifacts: list
    provenance: dict

    def to_dict(self) -> dict:
        return asdict(self)

    @classmethod
    def from_dict(cls, d: dict) -> RunRecord:
        return cls(**d)


# ============================================================
# 2. A Tracker-Adapter (Memory + Null backends)
# ============================================================
@dataclass
class Tracker:
    name: str

    def start(self, run_id: str, config: dict) -> None:
        raise NotImplementedError

    def log_metric(self, name: str, value: float, step: int) -> None:
        raise NotImplementedError

    def log_artifact(self, path: str) -> None:
        raise NotImplementedError

    def end(self) -> None:
        raise NotImplementedError


@dataclass
class MemoryTracker(Tracker):
    runs: dict = field(default_factory=dict)
    _current: str | None = None

    def start(self, run_id: str, config: dict) -> None:
        self.runs[run_id] = RunRecord(run_id, config, {}, [], {})
        self._current = run_id

    def log_metric(self, name: str, value: float, step: int) -> None:
        assert self._current is not None
        self.runs[self._current].metrics.setdefault(name, []).append((step, value))

    def log_artifact(self, path: str) -> None:
        assert self._current is not None
        self.runs[self._current].artifacts.append(path)

    def end(self) -> None:
        self._current = None


@dataclass
class NullTracker(Tracker):
    def start(self, run_id: str, config: dict) -> None:
        pass

    def log_metric(self, name: str, value: float, step: int) -> None:
        pass

    def log_artifact(self, path: str) -> None:
        pass

    def end(self) -> None:
        pass


def log_run(
    tracker: Tracker,
    run_id: str,
    config: dict,
    metrics: dict[str, list[tuple[int, float]]],
    artifacts: tuple[str, ...] = (),
) -> None:
    """One logging interface; the backend is swappable (adapter pattern).

    Artifacts are logged inside the run window: start() opens the run and
    end() closes it, so anything logged after end() has no current run.
    """
    tracker.start(run_id, config)
    for name, series in metrics.items():
        for step, value in series:
            tracker.log_metric(name, value, step)
    for path in artifacts:
        tracker.log_artifact(path)
    tracker.end()


# ============================================================
# 3. Platform Selection
# ============================================================
def choose_tracker(can_leave_infra: bool, needs_collab: bool, many_long_runs: bool) -> str:
    if not can_leave_infra:
        return "neptune (self-hosted)" if many_long_runs else "mlflow (self-hosted)"
    if needs_collab:
        return "wandb"
    if many_long_runs:
        return "neptune"
    return "mlflow (local) or sacred"


# ============================================================
# 4. The Cost Model
# ============================================================
def monthly_cost(
    runs_per_day: int,
    points_per_run: int,
    artifact_gb_per_run: float,
    price_per_seat: float,
    seats: int,
    price_per_gb: float,
) -> float:
    """A managed bill = seats + storage for 30 days of runs."""
    runs = runs_per_day * 30
    storage_gb = runs * artifact_gb_per_run
    return seats * price_per_seat + storage_gb * price_per_gb


def main() -> None:
    # A run is logged once, through the adapter, to any backend.
    cfg = {"lr": 3e-4, "batch": 64}
    series = {"val_acc": [(0, 0.80), (1, 0.86), (2, 0.91)]}

    mem = MemoryTracker("memory")
    log_run(mem, "run_a1b2", cfg, series, artifacts=("s3://artifacts/best.pt",))
    print("Example 1: tracker adapter")
    print(f"  recorded runs: {list(mem.runs)}")
    print(f"  val_acc series: {mem.runs['run_a1b2'].metrics['val_acc']}")
    assert mem.runs["run_a1b2"].to_dict()["config"] == cfg

    # The same call works against a null backend (tests, dry runs).
    log_run(NullTracker("null"), "dry", cfg, series)
    print("  null backend: the identical call, silently accepted")

    print("\nExample 2: platform selection")
    for args in [
        (False, False, False),
        (True, True, False),
        (True, False, True),
        (True, False, False),
    ]:
        print(f"  leave={args[0]}, collab={args[1]}, long={args[2]} -> {choose_tracker(*args)}")

    print("\nExample 3: the cost model")
    cheap = monthly_cost(5, 100, 0.1, 20.0, 3, 0.02)
    heavy = monthly_cost(300, 10000, 10.0, 20.0, 30, 0.02)
    print(f"  5 runs/day  : ${cheap:,.0f}/mo   (managed free tier is fine)")
    print(f"  300 runs/day: ${heavy:,.0f}/mo   (self-hosted starts to win)")
    assert heavy > cheap

    # Round-trip: the record you own survives any platform.
    rec = RunRecord("r1", cfg, series, ["s3://a"], {"git_sha": "a1b2", "seed": 0})
    assert RunRecord.from_dict(rec.to_dict()).run_id == "r1"

    print("\n--- Summary ---")
    print("1. Own the five-field run record; the platform is a backend.")
    print("2. Select by hosting, scope, collaboration, cost — in that order.")
    print("3. Model the bill before you commit.")


def _verify() -> None:
    cfg = {"lr": 1e-3}
    series = {"loss": [(0, 0.5), (1, 0.4)]}
    mem = MemoryTracker("m")
    log_run(mem, "r", cfg, series)
    assert mem.runs["r"].metrics["loss"] == [(0, 0.5), (1, 0.4)]
    log_run(NullTracker("n"), "r2", cfg, series)

    assert choose_tracker(False, False, False) == "mlflow (self-hosted)"
    assert choose_tracker(True, True, False) == "wandb"
    assert choose_tracker(True, False, True) == "neptune"

    c1 = monthly_cost(5, 100, 0.1, 20.0, 3, 0.02)
    c2 = monthly_cost(300, 10000, 10.0, 20.0, 30, 0.02)
    assert c2 > c1 and c1 > 0

    rec = RunRecord("x", cfg, series, [], {})
    assert RunRecord.from_dict(rec.to_dict()) == rec
    print("[OK] 18-tracking-platforms: all checks passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        _verify()
    else:
        main()
        _verify()

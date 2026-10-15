"""Stage dispatcher: the only module allowed to touch-argv and call stages in order.

Implemented (this is harness, not the exercise): parses ``--stage`` and
``--params``, loads params.yaml, and calls the matching stage function with the
conventional paths below. Stage functions themselves raise NotImplementedError
until you implement them.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

STAGES = ("clean", "profile", "dedup", "gate", "export")


def load_params(path: str) -> dict[str, object]:
    """Load params.yaml with safe_load."""
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise TypeError(f"params file {path} must hold a mapping")
    return data


def run_stage(stage: str, params: dict[str, object]) -> int:
    """Dispatch one stage. Returns process exit code (0 ok)."""
    if stage == "clean":
        raise NotImplementedError(
            "YOUR TURN: wire clean (read raw jsonl -> write clean.parquet)"
        )
    if stage == "profile":
        raise NotImplementedError(
            "YOUR TURN: wire profile (clean.parquet -> profile.json)"
        )
    if stage == "dedup":
        raise NotImplementedError(
            "YOUR TURN: wire dedup (clean.parquet -> deduped.parquet)"
        )
    if stage == "gate":
        raise NotImplementedError(
            "YOUR TURN: wire gate (deduped.parquet -> gold.parquet)"
        )
    if stage == "export":
        raise NotImplementedError(
            "YOUR TURN: wire export (gold.parquet -> gold.jsonl + manifest)"
        )
    raise ValueError(f"unknown stage: {stage}. Available: {', '.join(STAGES)}")


def main(argv: list[str] | None = None) -> int:
    """CLI entry: ``python src/capstone/run.py <stage> --params params.yaml``."""
    parser = argparse.ArgumentParser(description="Capstone stage dispatcher")
    parser.add_argument("stage", choices=list(STAGES) + ["bogus-for-test"])
    parser.add_argument("--params", default="params.yaml")
    args = parser.parse_args(argv)
    if args.stage not in STAGES:
        raise ValueError(f"unknown stage: {args.stage}. Available: {', '.join(STAGES)}")
    params = load_params(args.params)
    return run_stage(args.stage, params)


if __name__ == "__main__":
    raise SystemExit(main())

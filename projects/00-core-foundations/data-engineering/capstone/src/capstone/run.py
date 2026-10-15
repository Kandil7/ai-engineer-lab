"""Stage dispatcher: reads inputs, calls pure stage functions, writes outputs.

Implemented alongside the stage functions: each branch below is the honest
wiring (params in, files out) matching ``dvc.yaml``. Pure logic stays in the
stage modules; only this module touches the filesystem besides export/version.
"""

from __future__ import annotations

import argparse
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

import polars as pl
import yaml

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

STAGES = ("clean", "profile", "dedup", "gate", "export")

RAW_CORPUS = "raw/corpus.jsonl"
CLEAN_PARQUET = "data/clean.parquet"
PROFILE_JSON = "data/profile.json"
DEDUPED_PARQUET = "data/deduped.parquet"
DEDUP_REPORT = "data/dedup_report.json"
GOLD_PARQUET = "data/gold.parquet"
REJECTED_JSONL = "data/rejected.jsonl"
GOLD_JSONL = "data/gold.jsonl"
MANIFEST_JSON = "data/manifest.json"


def load_params(path: str) -> dict[str, object]:
    """Load params.yaml with safe_load."""
    with open(path, encoding="utf-8") as fh:
        data = yaml.safe_load(fh)
    if not isinstance(data, dict):
        raise TypeError(f"params file {path} must hold a mapping")
    return data


def _section(params: dict[str, object], name: str) -> dict[str, Any]:
    section = params.get(name, {})
    if not isinstance(section, dict):
        raise TypeError(f"params section {name!r} must hold a mapping")
    return section


def _read_jsonl(path: str) -> list[dict[str, str]]:
    try:
        lines = Path(path).read_text(encoding="utf-8").splitlines()
    except FileNotFoundError:
        raise FileNotFoundError(
            f"missing input {path}: place the raw corpus there "
            "(one {passage_id, text, source} object per line)"
        ) from None
    return [json.loads(line) for line in lines if line.strip()]


def _frame_rows(path: str) -> list[dict[str, str]]:
    frame = pl.read_parquet(path).select(["passage_id", "text", "source"])
    return [
        {"passage_id": r["passage_id"], "text": r["text"], "source": r["source"]}
        for r in frame.to_dicts()
    ]


def _write_json(path: str, payload: object) -> None:
    target = Path(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(payload, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )


def _git_sha() -> str:
    try:
        proc = subprocess.run(
            ["git", "rev-parse", "--short", "HEAD"],
            capture_output=True,
            text=True,
            timeout=15,
            check=False,
        )
    except (OSError, subprocess.SubprocessError):
        return "unknown"
    sha = proc.stdout.strip()
    return sha if proc.returncode == 0 and sha else "unknown"


def run_stage(stage: str, params: dict[str, object]) -> int:
    """Dispatch one stage. Returns process exit code (0 ok)."""
    if stage == "clean":
        from capstone.clean import frame_from_records

        records = _read_jsonl(RAW_CORPUS)
        frame_from_records(records).write_parquet(CLEAN_PARQUET)
        return 0
    if stage == "profile":
        from capstone.profile import profile_parquet

        _write_json(PROFILE_JSON, profile_parquet(CLEAN_PARQUET))
        return 0
    if stage == "dedup":
        from capstone.dedup import dedup_exact, minhash_dedup
        from capstone.export import export_parquet

        cfg = _section(params, "dedup")
        rows = _frame_rows(CLEAN_PARQUET)
        before = len(rows)
        exact_kept = dedup_exact(rows)
        kept, removed_ids, ratio = minhash_dedup(
            exact_kept,
            k=int(cfg.get("shingle_k", 5)),
            num_perm=int(cfg.get("num_perm", 128)),
            bands=int(cfg.get("bands", 16)),
            band_rows=int(cfg.get("band_rows", 8)),
            threshold=float(cfg.get("threshold", 0.8)),
            seed=int(cfg.get("seed", 42)),
        )
        export_parquet(kept, DEDUPED_PARQUET)
        _write_json(
            DEDUP_REPORT,
            {
                "rows_before": before,
                "rows_after": len(kept),
                "removed_ids": removed_ids,
                "dedup_ratio": ratio,
            },
        )
        return 0
    if stage == "gate":
        from typing import cast

        from capstone.export import export_parquet
        from capstone.gates import quality_gates

        cfg = _section(params, "gates")
        rows = _frame_rows(DEDUPED_PARQUET)
        result = quality_gates(
            rows,
            min_chars=int(cfg.get("min_chars", 20)),
            max_chars=int(cfg.get("max_chars", 20000)),
        )
        # Passed rows are the input row dicts unchanged; the cast records that.
        passed = cast("list[dict[str, str]]", result["passed"])
        export_parquet(passed, GOLD_PARQUET)
        rejected_path = Path(REJECTED_JSONL)
        rejected_path.parent.mkdir(parents=True, exist_ok=True)
        rejected_path.write_text(
            "\n".join(json.dumps(r, ensure_ascii=False) for r in result["rejected"])
            + ("\n" if result["rejected"] else ""),
            encoding="utf-8",
        )
        return 0
    if stage == "export":
        from capstone.export import export_jsonl
        from capstone.version import file_checksum, write_manifest

        rows = _frame_rows(GOLD_PARQUET)
        export_jsonl(rows, GOLD_JSONL)
        gold_bytes = Path(GOLD_PARQUET).stat().st_size
        try:
            raw_count = int(
                json.loads(Path(DEDUP_REPORT).read_text(encoding="utf-8"))[
                    "rows_before"
                ]
            )
        except (OSError, ValueError, KeyError):
            raw_count = len(rows)
        write_manifest(
            manifest_path=MANIFEST_JSON,
            inputs={
                GOLD_PARQUET: "sha256:" + file_checksum(GOLD_PARQUET),
                "params.yaml": "sha256:" + file_checksum("params.yaml"),
            },
            params=params,
            rows_before=raw_count,
            rows_after=len(rows),
            dedup_ratio=(raw_count - len(rows)) / raw_count if raw_count else 0.0,
            output_path=GOLD_PARQUET,
            output_bytes=gold_bytes,
            git_sha=_git_sha(),
        )
        return 0
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

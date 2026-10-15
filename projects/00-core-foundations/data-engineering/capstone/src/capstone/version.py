"""Reproducibility record: checksums + manifest writer (reference implementation)."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path


def file_checksum(path: str) -> str:
    """SHA-256 hex digest of a file's bytes (streamed, works at any size)."""
    digest = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def write_manifest(
    *,
    manifest_path: str,
    inputs: dict[str, str],
    params: dict[str, object],
    rows_before: int,
    rows_after: int,
    dedup_ratio: float,
    output_path: str,
    output_bytes: int,
    git_sha: str,
    dataset: str = "gold",
) -> dict[str, object]:
    """Build the manifest dict, write it as JSON to ``manifest_path``, return it.

    Contract: the returned dict (and file) carries exactly these keys:
    ``dataset, git_sha, inputs, params, params_hash, rows_before, rows_after,
    dedup_ratio, output_bytes, output_path`` where ``params_hash`` is the
    sha256 of ``json.dumps(params, sort_keys=True)``. ``output_path`` names the
    dataset artifact the manifest describes (e.g. ``data/gold.parquet``);
    ``manifest_path`` is where this JSON is written. Parent directories of
    ``manifest_path`` are created as needed. Values echo the arguments
    (no recomputation surprises).
    """
    manifest: dict[str, object] = {
        "dataset": dataset,
        "git_sha": git_sha,
        "inputs": inputs,
        "params": params,
        "params_hash": hashlib.sha256(
            json.dumps(params, sort_keys=True).encode("utf-8")
        ).hexdigest(),
        "rows_before": rows_before,
        "rows_after": rows_after,
        "dedup_ratio": dedup_ratio,
        "output_bytes": output_bytes,
        "output_path": output_path,
    }
    target = Path(manifest_path)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(
        json.dumps(manifest, indent=2, ensure_ascii=False) + "\n", encoding="utf-8"
    )
    return manifest

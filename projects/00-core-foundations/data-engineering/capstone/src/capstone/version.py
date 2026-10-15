"""Reproducibility record: checksums + manifest writer. YOUR TURN: implement both."""

from __future__ import annotations

import hashlib  # noqa: F401  (scaffold seam: used once file_checksum is implemented)
import json  # noqa: F401  (scaffold seam: used once write_manifest is implemented)
from pathlib import (
    Path,  # noqa: F401  (scaffold seam: used once write_manifest is implemented)
)


def file_checksum(path: str) -> str:
    """SHA-256 hex digest of a file's bytes (streamed, works at any size)."""
    raise NotImplementedError("YOUR TURN: implement file_checksum (streamed sha256)")


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
    raise NotImplementedError(
        "YOUR TURN: implement write_manifest (keys + file + echo)"
    )

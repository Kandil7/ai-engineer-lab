"""
Data Engineering — 18: DVC and Dataset Versioning
=================================================
Topics: dvc.yaml stage DAG, dvc.lock pinning, .dvcignore, manifest.json,
and the binary-gated honesty rule (ADR-0010, ADR-0013).

Run:      python 18-dvc.py
Verify:   python 18-dvc.py --verify
"""

from __future__ import annotations

import fnmatch
import hashlib
import json
import shutil
import subprocess
import sys
from collections.abc import Sequence

import yaml

SAMPLE_DVC_YAML = """\
stages:
  clean: {cmd: python scripts/clean.py, deps: [raw/customers.csv, scripts/clean.py], params: [{clean: [drop_nulls]}], outs: [data/clean.csv]}
  dedup: {cmd: python scripts/dedup.py, deps: [data/clean.csv, scripts/dedup.py], params: [{dedup: [threshold]}], outs: [data/dedup.csv]}
  export: {cmd: python scripts/export.py, deps: [data/dedup.csv, scripts/export.py], params: [{export: [top_k]}], outs: [data/export.csv]}
"""

SAMPLE_DVC_LOCK = """\
stages:
  clean: {outs: [{path: data/clean.csv, md5: 4a8a08f09d37b73795649038408b5f33, size: 524288}]}
  dedup: {outs: [{path: data/dedup.csv, md5: 8277e0910d750195b448797616e091ad, size: 501232}]}
  export: {outs: [{path: data/export.csv, md5: 5d41402abc4b2a76b9719d911017c592, size: 412340}]}
"""

SAMPLE_DVCIGNORE = """\
*.tmp
raw/scratch/
*.log
"""

SAMPLE_PARAMS_YAML = """\
clean: {drop_nulls: true}
dedup: {threshold: 0.9}
export: {top_k: 100}
"""

SAMPLE_MANIFEST_JSON = """\
{"inputs": {"raw/customers.csv": {"md5": "d41d8cd98f00b204e9800998ecf8427e", "bytes": 1048576}},
"params_hash": "8dcb54da2ea72e997a8d313040f40ef143d3f4276e0a447347491401d55a6847",
"git_sha": "a3c1e5f9b2d84c6a0f7e3d5b9c2a4e6f8d0b1c3d",
"rows_before": 10000, "rows_after": 9732,
"outputs": {"data/export.csv": {"bytes": 412340, "rows": 9732}}}"""


def topo_order(nodes: list[str], edges: list[tuple[str, str]]) -> list[str]:
    order: list[str] = []
    incoming = {n: 0 for n in nodes}
    for _, dst in edges:
        incoming[dst] += 1
    queue = sorted(n for n, d in incoming.items() if d == 0)
    while queue:
        node = queue.pop(0)
        order.append(node)
        for src, dst in edges:
            if src == node:
                incoming[dst] -= 1
                if incoming[dst] == 0:
                    queue.append(dst)
                    queue.sort()
    assert len(order) == len(nodes), "cycle detected in stage DAG"
    return order


def is_ignored(path: str, patterns: Sequence[str]) -> bool:
    for raw in patterns:
        pat = raw.strip()
        if not pat or pat.startswith("#"):
            continue
        if pat.endswith("/"):
            if path.startswith(pat):
                return True
        elif fnmatch.fnmatch(path, pat) or fnmatch.fnmatch(path.split("/")[-1], pat):
            return True
    return False


def main() -> None:
    stages = yaml.safe_load(SAMPLE_DVC_YAML)["stages"]
    lock = yaml.safe_load(SAMPLE_DVC_LOCK)["stages"]
    params = yaml.safe_load(SAMPLE_PARAMS_YAML)
    manifest = json.loads(SAMPLE_MANIFEST_JSON)
    assert set(stages) == {"clean", "dedup", "export"}
    assert set(params) == {"clean", "dedup", "export"}
    producers = {o: n for n, s in stages.items() for o in s["outs"]}
    edges = [
        (producers[d], n)
        for n, s in stages.items()
        for d in s["deps"]
        if producers.get(d, n) != n
    ]
    assert edges == [("clean", "dedup"), ("dedup", "export")]
    assert topo_order(sorted(stages), edges) == ["clean", "dedup", "export"]
    for name, stage in stages.items():
        for out in stage["outs"]:
            pinned = [o for o in lock[name]["outs"] if o["path"] == out]
            assert len(pinned) == 1 and len(pinned[0]["md5"]) == 32, out
    pats = SAMPLE_DVCIGNORE.splitlines()
    assert is_ignored("cache.tmp", pats) and is_ignored("raw/scratch/dump.csv", pats)
    assert not is_ignored("data/clean.csv", pats)
    assert len(manifest["inputs"]["raw/customers.csv"]["md5"]) == 32
    assert (
        manifest["params_hash"]
        == hashlib.sha256(SAMPLE_PARAMS_YAML.encode()).hexdigest()
    )
    assert len(manifest["git_sha"]) == 40
    assert manifest["rows_after"] <= manifest["rows_before"]
    assert manifest["outputs"]["data/export.csv"]["bytes"] > 0
    assert manifest["outputs"]["data/export.csv"]["rows"] == manifest["rows_after"]
    if shutil.which("dvc") is None:
        print("SKIP binary checks: dvc not installed (pip install dvc)")
    else:
        proc = subprocess.run(
            ["dvc", "--version"], capture_output=True, text=True, timeout=60
        )
        assert proc.returncode == 0, "dvc --version failed"
        print(f"dvc binary: {proc.stdout.strip()}")
    print("pipeline: clean -> dedup -> export (acyclic, pinned)")
    print("all asserts passed")


if __name__ == "__main__":
    if "--verify" in sys.argv:
        main()
    else:
        print("Run with --verify to execute the checks.")

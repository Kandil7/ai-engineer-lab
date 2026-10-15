"""Capstone acceptance tests: the definition of D3-done.

Scaffold state: the two structure tests pass; everything else fails with
NotImplementedError (the right reason). A failure for any OTHER reason
(ImportError, SyntaxError, KeyError) is a scaffold bug — report it.

Convention: each test targets ONE stage function with explicit arguments.
MinHash tests assert contract properties (subset, exact-catch, tolerance band),
never a magic pair outcome — estimation has variance and the tests respect it.
See ADR-0012.
"""

from __future__ import annotations

import hashlib
import json
from pathlib import Path

import polars as pl
import pytest
import yaml
from conftest import C5, C6, CORPUS, T1, T4

from capstone.clean import clean_text, frame_from_records
from capstone.dedup import dedup_exact, minhash_dedup
from capstone.export import devmate_doc_id, export_jsonl, export_parquet
from capstone.gates import arabic_ratio, quality_gates
from capstone.profile import profile_parquet
from capstone.version import file_checksum, write_manifest

CAPSTONE_ROOT = Path(__file__).resolve().parents[1]
K, NUM_PERM, BANDS, BAND_ROWS, THRESHOLD, SEED = 5, 128, 16, 8, 0.8, 42
TOLERANCE = 0.25


def _char_shingles(text: str, k: int = 5) -> set[str]:
    """Independent exact-Jaccard helper (test-side, not implementation)."""
    text = " ".join(text.split())
    if len(text) < k:
        return {text} if text else set()
    return {text[i : i + k] for i in range(len(text) - k + 1)}


def _exact_jaccard(a: str, b: str) -> float:
    sa, sb = _char_shingles(a), _char_shingles(b)
    if not sa and not sb:
        return 1.0
    if not sa or not sb:
        return 0.0
    return len(sa & sb) / len(sa | sb)


# ------------------------------------------------------------- structure (green now)

EXPECTED_ORDER = ["clean", "profile", "dedup", "gate", "export"]


def test_dvc_pipeline_structure() -> None:
    """The repo's own dvc.yaml is a valid linear DAG with pinned-style outs."""
    doc = yaml.safe_load((CAPSTONE_ROOT / "dvc.yaml").read_text(encoding="utf-8"))
    stages = doc["stages"]
    assert list(stages) == EXPECTED_ORDER
    produced: set[str] = set()
    for name, stage in stages.items():
        assert stage["cmd"] and stage["deps"] and stage["outs"], name
        for dep in stage["deps"]:
            if dep.endswith((".parquet", ".json")):
                assert dep in produced, f"{name} consumes unproduced {dep}"
        produced.update(str(o) for o in stage["outs"])
    assert any("gold.parquet" in o for o in produced)
    assert any("manifest.json" in o for o in produced)


def test_params_contract() -> None:
    """params.yaml carries every tunable the stage contracts require."""
    params = yaml.safe_load((CAPSTONE_ROOT / "params.yaml").read_text(encoding="utf-8"))
    assert params["dedup"]["shingle_k"] == K
    assert params["dedup"]["num_perm"] == NUM_PERM
    assert params["dedup"]["bands"] == BANDS
    assert params["dedup"]["band_rows"] == BAND_ROWS
    assert params["dedup"]["threshold"] == THRESHOLD
    assert params["dedup"]["seed"] == SEED
    assert params["gates"]["min_chars"] == 20
    assert params["gates"]["max_chars"] == 20000
    assert params["seed"] == SEED


def test_run_rejects_unknown_stage() -> None:
    """Dispatcher errors on unknown stages (harness is implemented)."""
    from capstone.run import main

    with pytest.raises(ValueError, match="unknown stage"):
        main(["bogus-for-test", "--params", str(CAPSTONE_ROOT / "params.yaml")])


# ------------------------------------------------------------------- clean


def test_clean_text_collapses_whitespace() -> None:
    assert clean_text("  العلم   نور\n\nيهدي\tالعقول  ") == "العلم نور يهدي العقول"
    assert clean_text("plain ascii") == "plain ascii"
    assert clean_text("   ") == ""


def test_frame_schema_and_char_count() -> None:
    rows = [
        {"passage_id": "a:1", "text": "short note", "source": "s"},
        {"passage_id": "a:2", "text": "  padded   text ", "source": "s"},
    ]
    frame = frame_from_records(rows)
    assert frame.schema == {
        "passage_id": pl.String,
        "text": pl.String,
        "source": pl.String,
        "char_count": pl.UInt32,
    }
    assert frame["char_count"].to_list() == [10, 11]


# ----------------------------------------------------------------- profile


def test_profile_parquet_measures(tmp_path: Path) -> None:
    frame = pl.DataFrame(
        {
            "passage_id": ["a", "b", "b", "c"],
            "text": ["x", None, "y", "z"],
            "source": ["s", "s", "s", "s"],
        }
    )
    path = str(tmp_path / "mini.parquet")
    frame.write_parquet(path)
    profile = profile_parquet(path)
    assert profile["rows"] == 4
    assert profile["null_rates"] == {"passage_id": 0.0, "text": 0.25, "source": 0.0}
    assert profile["distinct_ids"] == 3
    assert profile["duplicate_ids"] == 1


# ------------------------------------------------------------------- dedup


def test_dedup_exact_keep_first() -> None:
    kept = dedup_exact(CORPUS)
    ids = [r["passage_id"] for r in kept]
    assert len(kept) == 8  # one exact id+text repeat removed
    assert ids.count("b1:p1:0") == 1
    assert kept[0]["text"] == T1  # first occurrence wins


def test_minhash_exact_text_group_collapses() -> None:
    kept, removed_ids, _ratio = minhash_dedup(
        CORPUS,
        k=K,
        num_perm=NUM_PERM,
        bands=BANDS,
        band_rows=BAND_ROWS,
        threshold=THRESHOLD,
        seed=SEED,
    )
    survivors = [r for r in kept if r["text"] == T1]
    assert len(survivors) == 1  # three identical-text rows -> one survivor
    assert {"b1:p1:0", "b1:p9:0"} <= set(removed_ids)  # both repeated ids gone


def test_minhash_unrelated_and_empty_survive() -> None:
    kept, _, _ = minhash_dedup(
        CORPUS,
        k=K,
        num_perm=NUM_PERM,
        bands=BANDS,
        band_rows=BAND_ROWS,
        threshold=THRESHOLD,
        seed=SEED,
    )
    kept_ids = {r["passage_id"] for r in kept}
    assert "b2:c5:0" in kept_ids and "b2:c6:0" in kept_ids  # tiny overlap, never merge
    assert "b3:empty:0" in kept_ids  # empty text skipped, left for the gates


def test_minhash_ratio_arithmetic() -> None:
    kept, removed_ids, ratio = minhash_dedup(
        CORPUS,
        k=K,
        num_perm=NUM_PERM,
        bands=BANDS,
        band_rows=BAND_ROWS,
        threshold=THRESHOLD,
        seed=SEED,
    )
    assert ratio == pytest.approx(len(removed_ids) / len(CORPUS))
    assert len(removed_ids) >= 2  # the certain identical-text removals
    assert len(kept) + len(removed_ids) == len(CORPUS)


def test_minhash_precision_tolerance() -> None:
    """Every removed row must be genuinely similar to an earlier-or-kept row.

    Tolerance band honors estimation variance (ADR-0012): exact Jaccard of the
    removed row against some earlier-or-surviving row must clear
    threshold - 0.25. A removal below that band is a false merge, not variance.
    """
    kept, removed_ids, _ = minhash_dedup(
        CORPUS,
        k=K,
        num_perm=NUM_PERM,
        bands=BANDS,
        band_rows=BAND_ROWS,
        threshold=THRESHOLD,
        seed=SEED,
    )
    kept_texts = {r["text"] for r in kept}
    for i, row in enumerate(CORPUS):
        if row["passage_id"] not in removed_ids or not row["text"].strip():
            continue
        earlier = [r["text"] for r in CORPUS[:i] if r["text"].strip()]
        best = max(
            [_exact_jaccard(row["text"], t) for t in earlier + sorted(kept_texts)]
            or [0.0]
        )
        assert best >= THRESHOLD - TOLERANCE, row["passage_id"]


# ------------------------------------------------------------------- gates


def test_gates_split_with_reasons() -> None:
    rows = [
        {"passage_id": "g1", "text": T1, "source": "s"},
        {"passage_id": "g2", "text": C5, "source": "s"},
        {"passage_id": "g3", "text": "   ", "source": "s"},
        {"passage_id": "g4", "text": "short note", "source": "s"},
        {"passage_id": "g5", "text": "x" * 25000, "source": "s"},
    ]
    result = quality_gates(rows, min_chars=20, max_chars=20000)
    assert [r["passage_id"] for r in result["passed"]] == ["g1", "g2"]
    by_id = {r["passage_id"]: r["reasons"] for r in result["rejected"]}
    assert by_id == {"g3": ["EMPTY"], "g4": ["TOO_SHORT"], "g5": ["TOO_LONG"]}


def test_arabic_ratio_bounds() -> None:
    assert arabic_ratio(T1) > 0.5
    assert arabic_ratio(T4) > 0.5
    assert arabic_ratio(C5) < 0.1
    assert arabic_ratio(C6) < 0.1
    assert arabic_ratio("") == 0.0
    assert arabic_ratio("   ") == 0.0


# ----------------------------------------------------------------- version


def test_manifest_echo_and_file(tmp_path: Path) -> None:
    out = str(tmp_path / "manifest.json")
    manifest = write_manifest(
        manifest_path=out,
        inputs={"raw/corpus.jsonl": "sha256:abc"},
        params={"threshold": 0.8},
        rows_before=9,
        rows_after=6,
        dedup_ratio=3 / 9,
        output_path="data/gold.parquet",
        output_bytes=12345,
        git_sha="abc123",
    )
    assert manifest["rows_before"] == 9
    assert manifest["rows_after"] == 6
    assert manifest["dedup_ratio"] == pytest.approx(3 / 9)
    assert manifest["output_bytes"] == 12345
    assert manifest["git_sha"] == "abc123"
    assert manifest["output_path"] == "data/gold.parquet"
    assert set(manifest) == {
        "dataset",
        "git_sha",
        "inputs",
        "params",
        "params_hash",
        "rows_before",
        "rows_after",
        "dedup_ratio",
        "output_bytes",
        "output_path",
    }
    assert (
        manifest["params_hash"]
        == hashlib.sha256(
            json.dumps({"threshold": 0.8}, sort_keys=True).encode()
        ).hexdigest()
    )
    reloaded = json.loads(Path(out).read_text(encoding="utf-8"))
    assert reloaded == manifest


def test_file_checksum_stable(tmp_path: Path) -> None:
    target = tmp_path / "a.bin"
    target.write_bytes(b"abc" * 1000)
    assert file_checksum(str(target)) == hashlib.sha256(b"abc" * 1000).hexdigest()


# ------------------------------------------------------------------ export


def test_export_doc_id_matches_devmate_formula() -> None:
    expected = hashlib.md5(f"bookA:0:{T1[:100]}".encode()).hexdigest()
    assert devmate_doc_id("bookA", 0, T1) == expected
    assert len(devmate_doc_id("s", 3, "x")) == 32


def test_export_jsonl_roundtrip(tmp_path: Path) -> None:
    rows = [
        {"passage_id": "b1:p1:0", "text": T1, "source": "bookA"},
        {"passage_id": "b2:c5:0", "text": C5, "source": "bookB"},
    ]
    path = str(tmp_path / "gold.jsonl")
    assert export_jsonl(rows, path) == 2
    lines = Path(path).read_text(encoding="utf-8").splitlines()
    assert len(lines) == 2
    first = json.loads(lines[0])
    assert set(first) == {"id", "content", "metadata"}  # Document.to_dict shape
    assert first["id"] == devmate_doc_id("bookA", 0, T1)
    assert first["metadata"] == {"source": "bookA", "passage_id": "b1:p1:0"}


def test_export_parquet_roundtrip(tmp_path: Path) -> None:
    rows = [{"passage_id": "b1:p1:0", "text": T1, "source": "bookA"}]
    path = str(tmp_path / "gold.parquet")
    assert export_parquet(rows, path) == 1
    assert pl.read_parquet(path).height == 1


# -------------------------------------------------------------- integration


def test_full_chain_integration(tmp_path: Path) -> None:
    """Raw fixture -> gold files. Fails at clean_text on scaffold (right reason)."""
    frame = frame_from_records(CORPUS)
    cleaned = [
        {
            "passage_id": r["passage_id"],
            "text": clean_text(r["text"]),
            "source": r["source"],
        }
        for r in CORPUS
    ]
    _ = frame
    exact_kept = dedup_exact(cleaned)
    assert len(exact_kept) == 8
    kept, removed_ids, ratio = minhash_dedup(
        exact_kept,
        k=K,
        num_perm=NUM_PERM,
        bands=BANDS,
        band_rows=BAND_ROWS,
        threshold=THRESHOLD,
        seed=SEED,
    )
    assert ratio == pytest.approx(len(removed_ids) / len(exact_kept))
    gated = quality_gates(kept, min_chars=20, max_chars=20000)
    assert all(
        r["passage_id"] not in {"b3:empty:0", "b3:short:0", "b3:long:0"}
        for r in gated["passed"]
    )
    gold = gated["passed"]
    assert len({r["text"] for r in gold}) == len(gold)  # no exact-text dupes left
    n = export_jsonl(gold, str(tmp_path / "gold.jsonl"))
    assert n == len(gold)
    manifest = write_manifest(
        manifest_path=str(tmp_path / "manifest.json"),
        inputs={"fixture": "corpus"},
        params={"threshold": THRESHOLD},
        rows_before=len(CORPUS),
        rows_after=len(gold),
        dedup_ratio=(len(CORPUS) - len(gold)) / len(CORPUS),
        output_path=str(tmp_path / "gold.parquet"),
        output_bytes=export_parquet(gold, str(tmp_path / "gold.parquet")),
        git_sha="test",
    )
    assert manifest["rows_after"] == len(gold)

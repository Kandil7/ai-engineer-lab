# Data-Engineering Capstone — Corpus Pipeline to DevMate

Build, by hand, the pipeline that turns a raw corpus into a versioned gold
dataset that feeds DevMate retrieval:

```text
raw corpus -> Polars clean -> DuckDB profile -> exact + MinHash dedup
          -> quality gates -> manifest + DVC version -> Parquet + JSONL for DevMate
```

## Contract with DevMate (the anchor — do not modify DevMate)

`projects/04-ai-engineering/devmate/src/devmate/ingest/chunker.py` defines the
record this pipeline must produce:

- `Document.id`: 32-hex string, `md5(f"{source}:{position}:{content[:100]}")`.
  A 16-hex prefix is rejected by Qdrant; the full 32-hex parses as a dashless UUID.
- `Document.to_dict()` shape: `{"id", "content", "metadata"}` (no embedding key).
- `metadata` must carry at least `source`. Chunkers add `chunk_index`,
  `chunker`, and friends downstream.

So `gold.jsonl` carries one record per line:

```json
{"id": "<32-hex>", "content": "...", "metadata": {"source": "...", "passage_id": "..."}}
```

That shape drops straight into `Document(**record)`. Feed path: export cleaned
`.txt`/`.jsonl`, then DevMate's own `DocumentLoader` + `get_chunker("recursive")`
ingests it. A JSONL reader adapter inside DevMate is a future seam, not this task.

## Layout

```text
capstone/
  README.md            # this file
  dvc.yaml             # 5 stages: clean -> profile -> dedup -> gate -> export
  params.yaml          # all tunables; stages read from here, never hardcode
  .dvcignore           # raw/scratch, *.tmp
  src/capstone/        # YOUR code goes here (stubs raise NotImplementedError)
    run.py             # stage dispatcher (implemented): python run.py <stage>
    clean.py           # clean_text, frame_from_records (Polars)
    profile.py         # profile_parquet (DuckDB)
    dedup.py           # dedup_exact, minhash_dedup (stdlib)
    gates.py           # quality_gates, arabic_ratio
    version.py         # write_manifest, file_checksum
    export.py          # devmate_doc_id, export_jsonl, export_parquet
  tests/
    conftest.py        # sys.path seam + shared CORPUS fixture
    test_acceptance.py # acceptance tests (mostly red until you implement)
```

## Run

```bash
cd projects/00-core-foundations/data-engineering/capstone
python -m pytest tests/ -q        # scaffold state: 2 pass, rest fail with NotImplementedError
python -m pytest tests/ -q        # when done: all green
ruff check src tests
mypy src
```

## Scaffold state (right now)

- Green: `test_dvc_pipeline_structure`, `test_params_contract` (file structure is real).
- Red with `NotImplementedError`: everything else. That is the intended start.
- Red for any other reason (ImportError, SyntaxError): a scaffold bug — report it,
  do not work around it.

## Acceptance criteria (D3 done)

1. `pytest tests/ -q` fully green.
2. `ruff check src tests` and `mypy src` clean.
3. Dedup ratio reported by the pipeline on the fixture corpus is arithmetically
   consistent (`removed / total`) and the identical-text group keeps exactly one row.
4. `manifest.json` carries inputs checksums, params hash, git sha, row counts
   before/after, dedup ratio, and output bytes.
5. `dvc.yaml` DAG is acyclic, every stage output is pinned in `dvc.lock` after a
   run, and `dvc repro` rebuilds the dataset from a clean checkout (after you
   `pip install dvc` per ADR-0013).
6. `gold.jsonl` records match the `Document.to_dict()` shape above.

## Rules of the exercise

- Stage functions are pure (frames/rows in, frames/rows out). Only `run.py` and
  `export.py`/`version.py` touch the filesystem.
- Determinism: seed everything (`seed` in params). Same inputs + same params =
  same outputs, byte for byte where formats allow.
- Thresholds live in `params.yaml`, never in code.
- Near-duplicate tests assert contract properties (subset, exact-catch, tolerance
  band), never a magic pair outcome: MinHash estimation has variance, and the
  tests respect that. See ADR-0012.

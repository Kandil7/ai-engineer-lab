# Data Engineering 18: DVC and Dataset Versioning

## Topic Overview

Git versions code beautifully and datasets terribly. A dataset committed to git
bloats the repository forever, because every version of every blob stays in
history. Git also knows nothing about pipelines: it cannot say that
`data/dedup.csv` came from `data/clean.csv` with specific parameters.

DVC (Data Version Control) fills both gaps. Small pointer files go into git;
large data lives in a content-addressable cache and a remote. A `dvc.yaml`
pipeline declares stages, and `dvc repro` re-runs exactly what is stale. A
`dvc.lock` file pins every output checksum so any commit reproduces
byte-identical data.

This lecture covers why git alone fails, `dvc.yaml` stages, `dvc.lock`
pinning, `dvc repro` semantics, remotes, `.dvcignore`, and the `manifest.json`
record this track requires as DVC's mandatory complement. The design follows
ADR-0013 (docs/decisions/0013-choose-dvc-for-dataset-versioning.md) and the
dependency ruling in ADR-0010
(docs/decisions/0010-adopt-duckdb-stdlib-minhash-and-dvc-for-data-engineering.md).

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why git alone fails for datasets (blob bloat, no DAG).
2. Write a `dvc.yaml` stage with cmd, deps, outs, and params.
3. Explain what `dvc.lock` pins and why it is committed to git.
4. Describe `dvc repro` semantics (stale-stage detection).
5. Configure a local remote first and defer cloud remotes.
6. Write the `manifest.json` complement this track requires.

## Prerequisites

- Data Engineering 05 (deduplication) for the row-count checks.
- Data Engineering 06 (provenance) for checksum thinking.
- Data Engineering 14 (data versioning) for the vocabulary.

---

## 1. Why Git Alone Fails for Datasets

### Blob bloat

Git stores full blobs. Commit a 2 GB CSV twice and the repository grows by
roughly 4 GB forever, because history never shrinks. Every contributor pays
the cost of data they never touch.

### No DAG

Git tracks file states, not derivations. Nothing records that `data/dedup.csv`
came from `data/clean.csv` via `scripts/dedup.py` with `threshold: 0.9`.
Reproducing a dataset means trusting memory or a wiki page, and both rot.

### The split DVC introduces

DVC keeps tiny pointer files in git (a checksum, not content) and stores the
bytes in a cache plus a remote. Git stays small; data stays versioned. The
pipeline graph lives in `dvc.yaml`, the pins in `dvc.lock`, both committed.

## 2. dvc.yaml Stages

### The four fields

```yaml
stages:
  dedup:
    cmd: python scripts/dedup.py
    deps:
      - data/clean.csv
      - scripts/dedup.py
    params:
      - dedup:
        - threshold
    outs:
      - data/dedup.csv
```

`cmd` is the exact command to re-run. `deps` are the files it reads; code is
a dependency, because a script change must re-trigger the stage. `params`
names values from `params.yaml` affecting the output. `outs` are the files
DVC then tracks by checksum.

### The DAG rule

Stages connect through files: one stage's `outs` are the next stage's `deps`.
That structure is a directed acyclic graph; cycles are an error, because a
cycle cannot be ordered for execution. The exercise asserts acyclicity with a
topological sort in pure Python.

## 3. dvc.lock Pinning

After a stage runs, DVC records every dep and out checksum in `dvc.lock`,
committed to git alongside `dvc.yaml`. The lock is the ground truth: stage X
at commit Y produced bytes with checksum Z.

Staleness becomes mechanical: a dep whose checksum differs from the lock means
its downstream stages re-run. A reviewer can verify a dataset changed only
when its lock entry changed, which makes data diffs reviewable in a PR.

The exercise asserts every `outs` path in `dvc.yaml` appears in `dvc.lock`
with an `md5` field. An unpinned output is untracked output, and the check
fails loudly rather than letting it slide.

## 4. dvc repro Semantics

`dvc repro` compares current deps and params against `dvc.lock`. Stages whose
inputs match are skipped; changed inputs re-run and cascade downstream.
Unchanged pipelines finish in seconds because nothing executes.

A Makefile also re-runs commands, but pins nothing. `dvc repro` plus the lock
means the same commit yields the same bytes, and a byte change always shows
as a lock diff. That is the property the capstone acceptance test checks.

The `dvc` binary is not installed on this machine (ADR-0010), so the exercise
never pretends to run it. Structural checks always run; binary checks sit
behind `shutil.which("dvc")` with a skip note naming the install step.

## 5. Remotes: Local First, Cloud Later

A remote is where data bytes live: `dvc push` uploads, `dvc pull` downloads.
The first remote should be a local path. It needs no credentials, no billing,
and no network, so the full loop is learnable offline.

Cloud remotes (S3, GCS, Azure Blob) come when a real corpus needs shared
storage. That choice changes credentials, cost, and access control, so
ADR-0013 defers it to a dedicated remote-selection ADR. Do not run a real
corpus through a pipeline whose remote is still undecided.

## 6. .dvcignore

`.dvcignore` lists paths DVC must never track: scratch files, temp outputs,
and raw landing zones. It uses the same pattern style as `.gitignore`.

The fixture ignore file excludes `*.tmp` and `raw/scratch/`. The exercise
asserts a temp path and a scratch path are ignored while a real output is
not. An ignore file swallowing real outputs would silently untrack data, so
the negative half of the check matters.

## 7. manifest.json: The Mandatory Complement

DVC pins bytes but records no pipeline meaning: rows in, rows surviving
dedup, the git commit, the parameters used. ADR-0013 therefore requires every
dataset to ship a `manifest.json` written by the pipeline itself, carrying
input checksums, the params hash, the git sha, row counts before and after
dedup, and output byte sizes.

The exercise asserts all five are present and consistent: rows after dedup
cannot exceed rows before, and output bytes must be positive. The lock answers
"which bytes"; the manifest answers "what happened". Capstone tests assert on
the manifest always, with or without the binary.

## 8. The Real Workflow (Install dvc to Run These)

These commands are the honest workflow and require the binary. They are listed
so real usage is learned, not faked:

```bash
pip install dvc   # one-time install, needs user approval per repo rules
dvc init          # create .dvc/ in a git repository
dvc add raw/customers.csv  # track a dataset; git stores the pointer
dvc repro         # re-run stale stages, update dvc.lock
dvc push          # upload data to the remote
```

Until the install happens, work at the manifest layer: keep `dvc.yaml`,
`dvc.lock`, `.dvcignore`, and `manifest.json` valid so that when the binary
arrives, `dvc repro` has a correct pipeline to execute.

## Real-World Application

- Versioning corpus snapshots so any commit reproduces exact bytes.
- Re-running only the dedup stage when `threshold` changes.
- Pushing reviewed datasets to a local remote before any cloud decision.
- Reading manifest row counts in review to spot a bad ingest at a glance.

## Common Mistakes

1. **Committing datasets to git.** Blob bloat is permanent; track with DVC.
2. **Forgetting code in deps.** A script change must re-trigger its stage.
3. **Leaving an output unpinned in dvc.lock.** Untracked output is untracked data.
4. **Pointing at a cloud remote too early.** Local remote first, per ADR-0013.
5. **Skipping manifest.json.** Bytes without row counts are unauditable.

## Key Takeaways

1. Git fails for datasets: permanent blob bloat and no derivation graph.
2. `dvc.yaml` stages declare cmd, deps, outs, and params; stages form a DAG.
3. `dvc.lock` pins every output checksum and is committed to git.
4. `dvc repro` re-runs only stale stages; the lock makes it reproducible.
5. Local remote first, cloud later; `manifest.json` is the mandatory complement.

## Self-Check Questions

1. Why does committing a 2 GB CSV twice cost roughly 4 GB of history forever?
2. What four fields does a `dvc.yaml` stage declare, and what does each mean?
3. Why is `dvc.lock` committed to git while datasets are not?
4. How does `dvc repro` decide which stages to skip?
5. What five things must `manifest.json` carry, and why is DVC alone not enough?

## Further Reading / Connections

- ADR-0013 (docs/decisions/0013-choose-dvc-for-dataset-versioning.md) — the ruling this topic implements.
- ADR-0010 (docs/decisions/0010-adopt-duckdb-stdlib-minhash-and-dvc-for-data-engineering.md) — why the binary is install-gated.
- Data Engineering 05 (deduplication) and 06 (provenance) — the checks this pipeline encodes.
- Data Engineering 14 (data versioning) — the versioning vocabulary.

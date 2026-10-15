# ADR-0010: Adopt DuckDB stdlib MinHash and DVC for data engineering

- **Status:** Proposed
- **Date:** 2026-10-15
- **Deciders:** Repo owner (AI engineer track)
- **Tags:** data-engineering, dependencies, python

## Context

Topics `01` through `15` under `projects/00-core-foundations/data-engineering/` are
stdlib-only by construction: every `.py` runs with `python <topic>.py --verify` and
no installs. The D2 extension (topics `16-duckdb`, `17-minhash-lsh`, `18-dvc`) and the
D3 capstone need three tools that stdlib cannot honestly provide: SQL profiling over
Parquet, approximate near-duplicate detection, and dataset versioning with
reproducible pipelines.

Machine facts, verified 2026-10-15 on system Python 3.12.10:

- Present: `duckdb` 1.5.5, `polars` 1.44.1, `pytest` 8.4.2, `PyYAML` 6.0.3.
- Absent: `datasketch` (no package), `dvc` (no package and no binary).

Repo safety rules require user approval before any install, so no install happens in
this decision. The decision is which tool is genuinely adopted, which is replaced by
a stdlib equivalent, and which is approved for the user to install later.

## Decision Drivers

- The DE track's zero-install principle: `--verify` must stay runnable offline.
- Honest tool learning: a topic named after a tool must exercise the real tool,
  not a simulation with the tool's name on it.
- Reproducibility of the user's solves: every check must pass on this machine as-is,
  except where an install is explicitly approved and documented.

## Options Considered

### Option A — stdlib-only for all three

- Pros: zero installs; every `--verify` runs everywhere; no approval needed.
- Cons: cannot teach DuckDB profiling or DVC workflows honestly; simulates tools
  instead of using them, which is exactly what the plan forbids ("DVC حقيقي بدل
  DVC-style").

### Option B — pip-install duckdb, datasketch, and dvc now

- Pros: production tools everywhere; 17 uses the real `datasketch` LSH.
- Cons: requires installs this session (approval + network); two of the three are
  absent, so D2 scaffolding would be blocked on provisioning instead of content.

### Option C — mixed adoption per tool reality (chosen)

- Pros: uses what is present for real (DuckDB), teaches the MinHash algorithm in
  stdlib where the library is absent, and approves DVC for user-side install with
  graceful degradation until then. Nothing is simulated under a false name.
- Cons: two code paths to maintain (stdlib MinHash now, `datasketch` noted as the
  production path); DVC checks split into always-run structure checks and
  binary-gated run checks.

## Decision

Option C. `duckdb` is adopted for real use in topic 16 and the capstone profiler
(it is installed, v1.5.5). Topic 17 implements MinHash signatures and LSH banding
in stdlib (`hashlib` shingles, seeded for determinism) and names `datasketch` as the
production replacement, with the lecture showing the mapping. `dvc` is approved for
the user to install when solving topic 18 and the capstone; until then, topic 18
and capstone tests assert on `dvc.yaml` / `dvc.lock` / `.dvcignore` structure and on
a `manifest.json` reproducibility record, and gate binary-dependent asserts behind
`shutil.which("dvc")` with a clear skip message.

## Consequences

- Positive: D2 topics stay runnable offline today; each tool decision is explicit
  and reviewable; the user installs exactly one tool (`dvc`) with a written reason.
- Negative: stdlib MinHash is slower than `datasketch` at scale and must never be
  mistaken for production code; DVC coverage is partial until install.
- Follow-ups / new ADR candidates: ADR-0011 (profiling choice), ADR-0012 (dedup
  choice), ADR-0013 (versioning choice); a future ADR when `dvc` is installed to
  confirm `dvc repro` green on the capstone.

## Links

- Related ADRs: ADR-0011, ADR-0012, ADR-0013.
- Related artifacts (reviews, plans, eval reports):
  `projects/00-core-foundations/data-engineering/16-duckdb/`,
  `17-minhash-lsh/`, `18-dvc/`, `capstone/`.

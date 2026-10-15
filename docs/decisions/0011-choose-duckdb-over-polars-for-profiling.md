# ADR-0011: Choose DuckDB over Polars for profiling

- **Status:** Proposed
- **Date:** 2026-10-15
- **Deciders:** Repo owner (AI engineer track)
- **Tags:** data-engineering, profiling, duckdb, polars

## Context

The D3 capstone pipeline is `Polars clean -> DuckDB profile -> MinHash dedup ->
quality gates -> DVC version -> Parquet feeds DevMate`. Polars (1.44.1) already owns
cleaning and transform: six challenge sets under
`projects/00-core-foundations/python/03-libraries/polars/challenges/`. The open
question is which tool owns the profiling step over Parquet in topic 16 and in
`capstone` (`profile.py`).

## Decision Drivers

- Profile queries must run over Parquet in place, without loading full frames.
- The division between tools must be teachable: one sentence per tool's job.
- Both tools are already installed, so the choice is about fit, not provisioning.

## Options Considered

### Option A — Polars for profiling too

- Pros: single tool across clean and profile; builds directly on the six challenge
  sets the user already solves.
- Cons: profiling becomes extra eager frames held in memory; filtering and
  grouping over Parquet is less expressive than SQL; teaches nothing new about
  predicate pushdown or zero-copy reads.

### Option B — DuckDB owns profiling (chosen)

- Pros: SQL over Parquet in place with predicate pushdown; the industry-standard
  profiling pattern (`SUMMARY`, `PRAGMA show`, approximate quantiles); installed
  v1.5.5 and verified working. Polars keeps clean/transform, DuckDB keeps
  measure/profile: a one-sentence division.
- Cons: a second tool in the track; SQL-in-Python needs `sqlglot`-free discipline
  (plain query strings, parameterized where values vary).

### Option C — pandas-profiling style reports

- Pros: familiar HTML reports.
- Cons: pandas is not installed, is slower and more memory-hungry than both
  options, and is taught nowhere in this repo. Rejected.

## Decision

Option B. Polars owns cleaning and transformation; DuckDB owns profiling and
measurement. Topic 16 teaches `read_parquet` + `SUMMARY` + null/duplicate/distinct
queries and exports the profile as a table the quality gates consume. The capstone
`profile.py` implements the same contract against the gold Parquet.

## Consequences

- Positive: profile step runs in near-constant memory regardless of corpus size;
  the Polars/DuckDB boundary is explicit and tested on both sides.
- Negative: two APIs to learn; DuckDB version pinned by the machine (1.5.5), so
  queries must avoid newer-than-installed syntax.
- Follow-ups / new ADR candidates: none; revisit only if DuckDB is missing on a
  future machine.

## Links

- Related ADRs: ADR-0010 (dependency adoption).
- Related artifacts (reviews, plans, eval reports):
  `projects/00-core-foundations/data-engineering/16-duckdb/`,
  `capstone` (`profile.py`, acceptance tests).

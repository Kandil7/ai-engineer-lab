# ADR-0009: Fix indexing scope before tuning chunk sizes

- **Status:** Accepted
- **Date:** 2026-10-14
- **Deciders:** Workspace owner
- **Tags:** ai, rag, data, eval

## Context

Milestone A3 (`docs/roadmap/active-track-10-week.md`, weeks 2–3) requires a chunking
strategy ADR that **cites measured numbers, not intuition**. Until today the only numbers
in the repo came from offline mode, which scores recorded fixtures rather than a real
index: `devmate.eval.run_ragas --mode offline` reports Hit@5 1.000, but
`src/devmate/eval/run_ragas.py:184` labels that as
"retrieval fixtures used expected_context as top-k (not a live measurement)".

The first live baseline was run on 2026-10-14 against a real index.

**Setup:** Qdrant server v1.8.0 in `infra/docker/docker-compose.yml`, client 1.8.2,
collection `devmate_ollama` with 1363 points at dimension 768, embeddings from
Ollama `nomic-embed-text`. Golden set `evaluations/rag/datasets/devmate-golden.jsonl`,
10 cases. Report: `evaluations/rag/reports/2026-10-14-live-baseline`, commit `445c432`.

**Measured baseline:**

| Metric | Live | Offline (fixtures) |
| --- | --- | --- |
| Hit@1 | 0.800 (8/10) | 1.000 |
| Hit@5 | **0.900 (9/10)** | 1.000 |
| Hit@10 | 0.900 (9/10) | 1.000 |
| MRR | **0.820** | 1.000 |

The offline figure and the live figure differ by a full 0.100 on Hit@5. The offline
number was never a measurement, and the gap between the two is the size of the mistake
that fixture scoring hides.

Two cases fail, and both failures trace to the index, not to the chunker.

**Failure 1, `dev-golden-004`, complete miss (RR 0.000).** The expected source is
`pyproject.toml`. Retrieved instead: `src/devmate/config.py`, `src/devmate/index/vector_store.py`,
`docs/state-audit.md`, `sample_corpus/02-architecture.md`, `docs/deployment-plan.md`.
A Qdrant payload filter probe on `source` matching `pyproject` returns **zero points**.
The file is absent from the index, so no ranking could ever find it. Note that `.toml` is
already in `DocumentLoader.SUPPORTED_EXTENSIONS`
(`src/devmate/ingest/chunker.py:376`), so this is not an extension-filter problem; the
ingest run that produced this collection did not cover the path where the file lives.
A 200-point sample of the collection by extension returned 181 `.py`, 18 `.md`, 1 `.txt`
and no `.toml` at all.

**Failure 2, `dev-golden-007`, Hit@1 miss (RR 0.200).** The expected source is
`src/devmate/guards/guardrails.py`. The top four retrieved sources were
`src/devmate.egg-info/top_level.txt`, `sample_corpus/02-architecture.md`,
`sample_corpus/01-overview.md`, `sample_corpus/06-agents-and-mcp.md`; the expected file
appeared at rank 5. A payload probe confirms `devmate.egg-info/` is genuinely indexed:
`top_level.txt`, `SOURCES.txt`, and `entry_points.txt` are all present as points.
`sample_corpus/` is indexed too.

The cause is in `DocumentLoader.load_directory`
(`src/devmate/ingest/chunker.py:429-440`), whose default `exclude_patterns` lists
`__pycache__`, `.git`, `node_modules`, `.venv`, `venv`, `dist`, `build`, `.next`,
`.cache`, and `target`. It does **not** list `egg-info`, `.ruff_cache`, `.mypy_cache`,
`.pytest_cache`, or `sample_corpus`. Build metadata and the demo corpus are therefore
indexed alongside source code and compete with it on equal footing.

Both defects are indexing-scope defects. Chunk size, overlap, and strategy cannot be
evaluated meaningfully until they are fixed, because any chunker comparison would be
measuring how well each strategy ranks `top_level.txt` against `guardrails.py`.

## Decision Drivers

- **A baseline is only useful if it measures the thing you intend to change.** Comparing
  chunkers on a polluted index produces a ranking that does not transfer to a clean one.
- **The golden set is the contract.** A case whose expected source is not in the index
  fails for a reason no retrieval change can fix, and it will keep failing.
- **Signal-to-noise at the top of the list matters more than recall at large k.** A
  missing file at rank 1 costs a user a round trip; a build artifact at rank 1 costs
  them trust.
- **Ingest scope is a product decision, not a tuning knob.** What counts as "the
  repository" has to be stated before any metric is meaningful.

## Options Considered

### Option A — Tune chunk sizes on the current index

- Pros: produces numbers immediately; requires no re-ingest; appears to close the A3
  deliverable.
- Cons: the numbers would be a property of the pollution, not of the chunker; the one
  complete miss cannot be fixed by any chunking change; a comparison table built on this
  baseline is actively misleading in an interview and in the portfolio.

### Option B — Drop the two failing golden cases and accept the rest

- Pros: Hit@5 becomes 1.000 and the CI gate passes; one-line change.
- Cons: deletes the evidence. The failures are real defects in ingestion. Silencing them
  is the exact failure mode the track's own rule 5 warns about, and it would make the
  offline and live numbers agree for the wrong reason.

### Option C — Fix indexing scope, re-ingest, re-baseline, then compare chunkers

- Pros: the baseline becomes a measurement of retrieval over the intended corpus; the
  golden set stops containing impossible cases; the comparison in the chunking ADR then
  means what it claims; the two defects found here are the deliverable, not a detour.
- Cons: costs a re-ingest and a second baseline run; `sample_corpus/` needs a decision
  that is not purely technical; the numbers will change, so anything already quoting
  Hit@5 1.000 offline has to be restated.

## Decision

Adopt **Option C**.

**Indexing scope is fixed before any chunking comparison runs**, in this order:

1. Extend `DocumentLoader.load_directory`'s default `exclude_patterns`
   (`src/devmate/ingest/chunker.py:429-440`) with at least `egg-info`, `.ruff_cache`,
   `.mypy_cache`, `.pytest_cache`, and `.eggs`. Keep the list in one place and mirror it
   into `RepoAnalyzer.DEFAULT_EXCLUDE_DIRS` (`src/devmate/ingest/repo_reader.py:21`),
   which already claims to mirror it.
2. Decide `sample_corpus/` explicitly. It is demo content shipped in the image for the
   startup ingest in `src/devmate/ingest/sample_corpus.py`, not part of the repository
   being asked about. It is excluded from the repo index and remains available to the
   demo path through its own code path.
3. Re-ingest so the collection covers the full ingest root including `pyproject.toml`,
   and confirm with a payload probe that a known config file now returns points.
4. Re-run the live baseline and commit that report as the number of record.

Only after step 4 does the chunking comparison begin, and it must run against the
re-baselined index. The 2026-10-14 report stays in the repo as the "before" state; it is
evidence of the diagnosis, not the number of record.

**The CI gate is not changed.** `make eval` still gates on Hit@5 at 1.000, and that gate
is currently satisfied only by offline fixture scoring. Live mode is not gated yet, and
this ADR does not pretend otherwise: a live gate should be added at whatever Hit@5 the
re-baselined index actually achieves, with the threshold recorded next to it, not raised
to meet the offline number.

## Consequences

- **Positive:** the next chunking comparison measures chunking; the golden set contains
  only cases the index can answer; build artifacts stop occupying top ranks, which should
  lift Hit@1 (the metric that actually reflects what a user sees); the 0.100 gap between
  offline and live Hit@5 is now explained rather than merely observed.
- **Negative:** everything quoting the offline Hit@5 1.000 has to be restated; the
  collection is rebuilt, so any hand-collected latency or cost number tied to the old
  index is void; `sample_corpus/` exclusion changes what the demo startup ingest sees if
  the two paths are not kept separate, which is a regression risk to test.
- **Watch:** the `sample_corpus/` decision is the one that can silently break the demo.
  `src/devmate/ingest/sample_corpus.py:39` already skips when the store is populated, so
  after a full repo ingest the demo path may never run; that behaviour should be asserted
  rather than assumed.
- **Follow-ups / new ADR candidates:**
  - The chunking-strategy comparison itself, which ADR-0005 listed as the follow-up this
    ADR now unblocks.
  - A live-mode CI gate with a threshold chosen from a measured baseline.
  - Whether `expected_context` in the golden set should store repo-relative paths while
    the index stores absolute ones; the scorer currently matches by suffix, which works
    but is implicit and undocumented.

## Links

- Related ADRs: [0005](0005-vector-db-qdrant-over-chromadb.md) (committed to Qdrant and
  named this chunking ADR as its follow-up), [0004](0004-adopt-10-week-ai-engineer-track.md)
  (defines milestone A3)
- Eval output: `evaluations/rag/reports/2026-10-14-live-baseline`
- Golden set: `evaluations/rag/datasets/devmate-golden.jsonl`
- Code under change: `src/devmate/ingest/chunker.py`,
  `src/devmate/ingest/repo_reader.py`, `src/devmate/ingest/sample_corpus.py`
- Harness: `src/devmate/eval/run_ragas.py`

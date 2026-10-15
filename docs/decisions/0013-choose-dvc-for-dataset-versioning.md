# ADR-0013: Choose DVC for dataset versioning

- **Status:** Proposed
- **Date:** 2026-10-15
- **Deciders:** <names / roles>
- **Tags:** <architecture, backend, ai, infra, ...>

## Context

<!-- What is the issue or force that motivates this decision? State the problem,
constraints, and assumptions. Repo-first: reference real files/paths. No invented scope. -->

## Decision Drivers

- <driver 1, e.g. performance budget>
- <driver 2, e.g. team familiarity>

## Options Considered

### Option A â€” <name>
- Pros:
- Cons:

### Option B â€” <name>
- Pros:
- Cons:

## Decision

Option A, with option C as its mandatory complement. Every dataset ships a
`manifest.json` (input checksums, params hash, git sha, row counts before/after
dedup, output bytes) written by the pipeline itself, plus `dvc.yaml` stages,
`.dvcignore`, and a local remote configuration. Topic 18 and capstone tests assert
on file structure and on the manifest always; asserts that need the binary are
gated behind `shutil.which("dvc")` with a skip message naming the install step.
`dvc repro` green on the capstone is an acceptance criterion for D3, executed after
the user installs DVC.

## Consequences

- Positive: versioning is real from day one at the manifest layer and becomes
  fully reproducible at install time; no throwaway simulation code.
- Negative: partial DVC coverage until install; remote choice (local path first)
  must be revisited before any real corpus goes through the pipeline.
- Follow-ups / new ADR candidates: a confirmation ADR once `dvc repro` passes on
  the capstone; a remote-selection ADR before cloud storage.

## Links

- Related ADRs: ADR-0010 (dependency adoption).
- Related artifacts (reviews, plans, eval reports):
  `projects/00-core-foundations/data-engineering/18-dvc/`,
  `capstone` (`dvc.yaml`, `manifest` writer, acceptance tests).

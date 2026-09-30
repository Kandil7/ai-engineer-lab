# Data Engineering 04: Checkpointing

## Topic Overview

Long pipelines fail. An ingest that takes hours will hit a network drop, a crash, or a bad page, and
without checkpointing every failure restarts the whole job, wasting the work, the cost, and the time.
Checkpointing records progress durably so a failed run resumes where it stopped. For Athar's corpus
ingestion, it is the difference between a job that finishes and one that never does.

This lecture covers why checkpointing matters, what to record, atomic checkpoint writes, correct
resume, and the combination of checkpointing with idempotency that makes resume truly safe.

The subtle property is atomicity: a torn checkpoint (half-written) corrupts the resume position and
causes the pipeline to skip work it never did. Atomic writes via temp-file-and-rename are what
prevent that, and they are a one-line discipline with a large payoff.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why checkpointing matters for long pipelines.
2. Record progress as a durable, atomic checkpoint.
3. Resume from a checkpoint without redoing completed work.
4. Make checkpointing correct under crashes with atomic writes.
5. Combine checkpointing and idempotency for safe resume.
6. Choose what a checkpoint must record to answer "what is done?".

## Prerequisites

- Data Engineering 01 (ETL) and 03 (idempotency) for the pipeline and its safe re-runs.

---

## 1. Why Checkpoint

### The failure is a matter of when

A corpus ingest that takes hours will fail. Without checkpoints, every failure restarts the whole job:
wasted work, wasted cost, delayed data. The longer the job, the more certain the failure and the more
expensive the restart.

### The memory of the pipeline

A checkpoint is the pipeline's memory of what it has completed. With it, the job resumes from the
last completed unit, and the work already done is preserved across failures.

### The scale argument

Checkpointing matters more as the job grows: a ten-minute job can afford to restart, a ten-hour one
cannot. The corpus scale Athar targets makes checkpointing mandatory, not optional.

## 2. What to Record

### The content

A checkpoint records the position of completed work: the last processed page, the last committed
batch, or the set of completed source files. It must be enough to answer "what is done?" unambiguously:

```python
{"book_id": "b1", "last_committed_page": 42, "source_version": "v1"}
```

### The granularity

The granularity is a tradeoff: finer checkpoints lose less work but cost more writes; coarser ones
lose more work but write rarely. A per-page or per-batch checkpoint is the usual choice, tuned to
the cost of re-doing a unit.

### Self-describing

The checkpoint carries its context (book, version) so a resume knows exactly which unit and which
snapshot it is resuming. A checkpoint that is just a number is ambiguous across runs.

## 3. Atomic Checkpoint Writes

### The rule

A checkpoint write must be atomic: either the whole checkpoint is written or none of it is. A torn
write (half a checkpoint) corrupts the resume position:

```python
def save(self, state: dict) -> None:
    tmp = self.path.with_suffix(".tmp")
    tmp.write_text(json.dumps(state), encoding="utf-8")
    os.replace(tmp, self.path)  # atomic on most filesystems
```

### The mechanism

Write to a temp file, then rename. The rename is atomic on most filesystems, so a reader sees either
the old checkpoint or the new one, never a half-written one.

### The anti-pattern

Never append to a checkpoint file. A crash mid-append leaves a corrupt record, and "read the last
line" then fails or, worse, succeeds with garbage. Overwrite atomically instead.

## 4. Resume Correctly

### The rule

On resume, read the checkpoint and start after the last committed unit. The resume must not redo
completed work (that is what the checkpoint prevents) and must not skip uncommitted work (that is
what atomicity prevents).

```python
state = checkpoint.load() or {"last_committed": 0}
for page in pages:
    if page <= state["last_committed"]:
        continue  # already committed: resume skips it
    ...
```

### The boundary

The interesting case is the unit at the boundary: the one that may or may not have committed before
the crash. The checkpoint's atomicity and the idempotency of the load together handle it, because
re-processing that one unit is harmless.

### The test

The checkpoint test simulates a crash mid-run and asserts the resume completes with no work redone
and no work skipped:

```python
assert done == [1, 2, 3, 4, 5], f"resume wrong: {done}"
assert not (cp.path.with_suffix(".tmp")).exists()
```

## 5. Checkpointing Plus Idempotency

### The combination

Checkpointing says "resume here"; idempotency says "even if you redo a little, nothing breaks." A
pipeline with both can resume from a slightly stale checkpoint safely.

### Why stale happens

A checkpoint is written before or after the load commits, so it can be slightly stale relative to
the actual data. Without idempotency, a stale checkpoint means re-processing a committed unit
duplicates it. With idempotency, the re-process is a harmless upsert.

### The production-grade property

This is the production-grade version of the roadmap's exit test: not just "run twice is safe" but
"crash and resume is safe." It is the combination, not either property alone, that delivers it.

## 6. Retention and Cleanup

### Retaining checkpoints

Completed checkpoints can be archived for audit or kept for a short window; stale checkpoints from
abandoned runs should be cleaned up so a new run does not resume from the wrong place.

### The keying

A checkpoint should be keyed by the job and the source version, so a run for one book or one version
does not resume from another's checkpoint. The key is part of the correctness.

## Real-World Application

- Checkpointing the Athar ingest per book and version so a crash at page 400 resumes rather than
  restarting.
- Writing checkpoints atomically so a crash during the checkpoint write does not corrupt the resume
  position.
- Combining the atomic checkpoint with the idempotent upsert so a stale checkpoint is harmless.
- Cleaning up abandoned checkpoints so a new run does not adopt the wrong state.

## Common Mistakes

1. **No checkpoint.** Every failure restarts the whole job.
2. **Non-atomic checkpoint writes.** Torn records corrupt the resume position.
3. **Appending to a checkpoint file.** A crash mid-append corrupts it.
4. **Trusting a stale checkpoint without idempotent loads.** Re-processing duplicates.
5. **Not keying the checkpoint by job and version.** A run resumes from the wrong state.

## Key Takeaways

1. Checkpoints record completed work so failures resume, not restart.
2. The checkpoint is self-describing and keyed by job and source version.
3. Checkpoint writes must be atomic; write to a temp file and rename.
4. Resume starts after the last committed unit and redoes nothing committed.
5. Idempotency makes a stale-checkpoint resume safe; together they deliver crash-and-resume.

## Self-Check Questions

1. Why does checkpointing matter more as a job grows?
2. What must a checkpoint record to answer "what is done?" unambiguously?
3. Why must checkpoint writes be atomic, and how is that achieved?
4. Why is appending to a checkpoint file dangerous?
5. How do checkpointing and idempotency combine to make resume safe?

## Further Reading / Connections

- Data Engineering 03 (idempotency) — the property that makes resume safe.
- Data Engineering 01 (ETL) — the pipeline being checkpointed.
- Embeddings 02 (batch processing) — resumable, async embedding during ingestion.
- `projects/04-ai-engineering/athar-lab/` — the deterministic pipeline a checkpoint front-runs.

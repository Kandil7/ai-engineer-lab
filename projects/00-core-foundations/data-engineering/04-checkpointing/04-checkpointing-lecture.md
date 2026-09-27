# Data Engineering 04: Checkpointing

## 🎯 Topic Overview

Long pipelines fail. Checkpointing records progress so a failed run resumes
where it stopped instead of restarting from zero. For Athar's corpus
ingestion, checkpointing turns a multi-hour job into a resumable one. This
lecture covers what to record, where to store it, and how to make resume
correct.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Explain why checkpointing matters for long pipelines
2. Record progress as a durable, atomic checkpoint
3. Resume from a checkpoint without redoing completed work
4. Make checkpointing correct under crashes (atomic writes)
5. Combine checkpointing with idempotency for safe resume

---

## 1. Why Checkpoint

A corpus ingest that takes hours will fail: a network drop, a crash, a bad
page. Without checkpoints, every failure restarts the whole job — wasted
work, wasted cost, delayed data. With checkpoints, the job resumes from the
last completed unit. The checkpoint is the pipeline's memory of what it has
done.

## 2. What to Record

A checkpoint records the position of completed work: the last processed
page, the last committed batch, the set of completed source files. It must
be enough to answer "what is done?" unambiguously. For Athar: the last
committed page number per book, or the set of committed passage_ids.

```python
# A checkpoint: durable, atomic, self-describing
{"book_id": "b1", "last_committed_page": 42, "source_version": "v1"}
```

## 3. Atomic Checkpoint Writes

A checkpoint write must be atomic: either the whole checkpoint is written
or none of it is. A torn write (half a checkpoint) corrupts the resume
position. Write to a temp file then rename (atomic on most filesystems), or
use a database transaction. Never append to a checkpoint file — a crash
mid-append leaves a corrupt record.

## 4. Resume Correctly

On resume, read the checkpoint and start after the last committed unit.
The resume must not redo completed work (that is what the checkpoint
prevents) and must not skip uncommitted work (that is what atomicity
prevents). The combination of checkpointing plus idempotent loads makes
resume safe even when the checkpoint is slightly stale — re-processing a
committed unit is harmless because the load is idempotent.

## 5. Checkpointing + Idempotency

These two work together. Checkpointing says "resume here"; idempotency says
"even if you redo a little, nothing breaks." A pipeline with both can
resume from a stale checkpoint safely. This is the production-grade version
of the roadmap's exit test: not just "run twice is safe" but "crash and
resume is safe."

## Common Mistakes

- No checkpoint: every failure restarts the whole job.
- Non-atomic checkpoint writes: torn records corrupt the resume position.
- Appending to a checkpoint file (crash mid-append corrupts it).
- Trusting a stale checkpoint without idempotent loads to back it up.

## Key Takeaways

1. Checkpoints record completed work so failures resume, not restart.
2. Checkpoint writes must be atomic.
3. Resume after the last committed unit.
4. Idempotency makes stale-checkpoint resume safe.
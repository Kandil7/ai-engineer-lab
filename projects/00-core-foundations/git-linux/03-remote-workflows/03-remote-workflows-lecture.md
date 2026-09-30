# Git-Linux 03: Remote Workflows

## Topic Overview

A remote is a copy of the repository on another machine, and it is where collaboration happens. Push
sends local commits up; pull brings remote commits down; the pull request is the review gate between
the two. Understanding the remote as "the other copy, with its own history" explains everything about
rejected pushes, divergence, and why you pull before you push.

This lecture covers remotes, the push/pull loop, divergence and its resolution, the pull request as a
review gate, and the workflow that keeps the local and remote in sync without large divergences.

The recurring rule is to pull often and push small. Divergence is a function of time and branch
lifetime, and small, frequent synchronization keeps it small and the merges easy.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Add and inspect a remote.
2. Push local commits to a remote and understand a rejected push.
3. Pull remote changes and resolve divergence.
4. Describe the pull request as a review gate.
5. Keep the local and remote in sync.
6. Explain why small, frequent sync beats a large divergence.

## Prerequisites

- Git-Linux 01 (basics) and 02 (branching and merging).

---

## 1. Remotes

### What a remote is

A remote is a named reference to another copy of the repository. The default is `origin`:

```bash
git remote add origin https://github.com/user/repo.git
git remote -v   # list remotes and their URLs
```

### Why it matters

The remote is where collaboration happens. Pushing and pulling move commits between machines, and the
remote is the shared truth for the team. Your local copy is a working copy of that shared history.

### The source of truth question

For collaboration, the remote is the source of truth for the shared history. For the data in the
system, the source of truth is the database (RAG System 06). The two are different sources of truth
for different things, and neither is the queue.

## 2. Push and Pull

### Push

Push sends local commits to the remote. It succeeds only when the remote's history is an ancestor of
the local history, that is, when the local is strictly ahead:

```python
ok, _ = remote.push(local, last_pushed)
assert ok and remote.commits == ["c1", "c2"]
```

### The rejected push

A push is rejected when the remote has commits the local lacks:

```python
remote.commits.append("c3")  # someone else pushed
ok, _ = remote.push(local, last_pushed)
assert not ok, "push rejected when the remote is ahead"
```

The rejection is a safety feature: it prevents overwriting someone else's work. The resolution is to
pull first.

### Pull

Pull brings the remote's commits down and merges them into the local history:

```python
local = remote.pull(local)
assert "c3" in local
ok, last_pushed = remote.push(local, last_pushed)
assert ok, "after pull, the push succeeds"
```

Pull is the prerequisite for the push that was rejected.

## 3. Divergence

### What it is

Divergence happens when the local and remote both have commits the other lacks. Pulling merges them,
and the merge may conflict (Git-Linux 02).

### Why it grows

Divergence grows with time and branch lifetime. A branch that is not synchronized for a week diverges
heavily and conflicts on many files; a branch synchronized hourly barely diverges at all.

### The discipline

Pull often and push small. Small, frequent synchronization keeps the merges tiny and the conflicts
rare, which is the same principle as short-lived branches (Git-Linux 02) applied to the remote.

### The dependency

Divergence is also why a stale local copy is dangerous: it looks fine until the push is rejected or
the merge conflicts, at which point the drift is discovered all at once. Frequent sync makes the
drift visible continuously.

## 4. The Pull Request

### The gate

A pull request is a review gate: the branch's changes are proposed, reviewed, and merged. It is where
someone else reads the code before it reaches the main line.

```text
feature branch --push--> pull request --review--> merge to main
```

### Why review matters

Review catches bugs, style issues, and design problems before they reach the shared history. It is
also where contract and schema changes are seen by the other side (Data Engineering 02), which is
why a change to a shared contract is a cross-team event.

### The exit test

The roadmap's exit test is that changes are reviewed before merging. The PR is the mechanism: no
change reaches the main line without a second pair of eyes.

## 5. The Workflow

### The daily loop

```text
pull -> branch -> commit -> push -> open a PR -> review -> merge -> delete branch
```

The loop starts with a pull so the local base is current, and it ends with a merge and a cleanup.

### Small pushes

Pushing small and often keeps the remote current and the divergence small. A large, infrequent push
is a large divergence waiting to conflict.

### The branch cleanup

Deleting the merged branch keeps the branch list clean and signals that the work is done.

## 6. The Exercise

### What it models

The exercise models a remote with a list of commits, a push that is rejected when the remote is ahead,
a pull that merges the remote's commits, and a subsequent successful push.

### The assertions

```python
assert ok and remote.commits == ["c1", "c2"]  # push up
assert not ok, "push rejected when the remote is ahead"
local = remote.pull(local)
assert ok, "after pull, the push succeeds"
```

The rejected-then-pulled-then-pushed sequence is the core lesson: the rejection is resolved by pulling,
not by forcing.

### The anti-pattern

Never force-push to resolve a rejected push on a shared branch. Force-pushing overwrites the remote's
history, destroying the commits the local lacked. The correct response is always to pull and merge.

## Real-World Application

- Pulling before starting work so the local base is current and the push will not be rejected.
- Opening a pull request so a change is reviewed before it reaches the main line.
- Resolving a rejected push by pulling and merging, never by force-pushing.
- Pushing small and often so divergence stays tiny and merges stay easy.

## Common Mistakes

1. **Pushing without pulling first.** The push is rejected.
2. **Force-pushing to resolve a rejection.** Other people's commits are destroyed.
3. **Large divergences from infrequent sync.** Conflicts on many files.
4. **Merging without review.** Unreviewed changes reach the main line.
5. **Pushing secrets to a remote.** They are in the shared history.
6. **Never pulling.** The local drifts and the drift is discovered all at once.

## Key Takeaways

1. A remote is a named reference to another copy; it is the shared history for collaboration.
2. Push sends commits up and is rejected when the remote is ahead; pull first, then push.
3. Divergence grows with time; pull often and push small to keep it tiny.
4. The pull request is the review gate before the main line.
5. Never force-push a shared branch; the correct response to a rejection is to pull and merge.

## Self-Check Questions

1. Why is a push rejected when the remote is ahead, and what is the correct response?
2. Why does divergence grow with time, and how is it kept small?
3. What is the pull request's role in the workflow?
4. Why is force-pushing on a shared branch destructive?
5. Why does the daily loop start with a pull?

## Further Reading / Connections

- Git-Linux 01 and 02 — the local model this extends.
- `docs/cheat-sheets/git.md` — remote commands.
- Data Engineering 02 (schemas and contracts) — why a shared-contract change is a cross-team event.

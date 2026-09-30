# Git-Linux 02: Branching and Merging

## Topic Overview

Branches isolate work. A feature branch keeps experiments off the main line until they are ready,
and merging brings them back. The mental model is simple once you have the three areas: a branch is
just a movable pointer to a commit, and switching branches moves the working tree and index to match.
Everything confusing about branching follows from forgetting that branches point at commits, not at
copies of files.

This lecture covers branches, merging (fast-forward and merge commits), conflicts and how to resolve
them deliberately, the merge-versus-rebase choice, and the discipline of short-lived, focused
branches that keep the main line deployable.

The core discipline is that the main line stays working. Feature work happens in isolation, and a
merge is the deliberate moment a change joins the main line, reviewed and understood.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Create and switch branches.
2. Merge a branch back into the main line.
3. Explain fast-forward versus a merge commit.
4. Resolve a merge conflict deliberately.
5. Explain when to merge and when to rebase.
6. Keep branches short-lived and the history readable.

## Prerequisites

- Git-Linux 01 (Git basics) for commits and the three areas.

---

## 1. Branches

### A pointer to a commit

A branch is a movable pointer to a commit. Creating a branch does not copy files; it points at the
current commit and moves forward as new commits are made on it:

```bash
git branch feature-x      # create
git switch -c feature-x   # create and switch
git switch main           # switch back
```

### Why isolation

The main line stays stable while feature work happens in isolation. You can experiment, commit
freely, and abandon the branch without touching the main line. This is the mechanism that lets many
changes proceed without interfering with each other.

### The pointer model

Because a branch is a pointer, switching branches updates the working tree and index to match the
commit the branch points at. Uncommitted changes travel with you or block the switch, which is why
Git refuses to switch when they would be lost.

## 2. Merging

### Fast-forward

A fast-forward merge happens when the branches have not diverged: the feature branch is strictly
ahead, so the main line simply moves its pointer forward to the feature's commit. No merge commit is
created; the history stays linear:

```python
def fast_forward(base, feature):
    """A fast-forward merge: the feature's files become the base's."""
    return Branch(base.name, feature.files)
```

### Merge commit

When the branches have diverged (the main line advanced too), a merge commit joins the two histories.
It records the two parents and a new snapshot, so both histories are preserved.

### The exit test

Merging is the moment a feature becomes part of the main line. Doing it deliberately, after review,
keeps the main line's history meaningful (Git-Linux 03).

## 3. Conflicts

### What a conflict is

A conflict happens when two branches change the same lines differently. Git cannot decide which
version is correct, so it marks the conflict in the file and stops, leaving the resolution to the
developer:

```python
assert conflict_lines(a, b, "app.py"), "same line changed differently"
```

### What it is not

A conflict is not a failure. It is a signal that two changes touched the same place, which is
information worth having. The resolution is a deliberate decision about the correct combined result,
not a blind pick of one side.

### Resolving

Resolve by reading both versions, deciding the correct outcome, editing the file to that outcome, and
staging the resolution. Blindly taking "ours" or "theirs" loses a change and is how subtle bugs enter
after a merge.

### Avoiding them

Conflicts are smaller when branches are short-lived. A branch that lives for weeks diverges from a
moving main line and conflicts on many files; a branch that lives for hours conflicts rarely.

## 4. Merge Versus Rebase

### Merge

Merge preserves the history as it happened: a merge commit records that two histories joined at a
point in time. It is safe on any branch because it does not rewrite commits.

### Rebase

Rebase replays a branch's commits onto a new base, rewriting them as a clean linear sequence. The
history is tidier, but the commits are new (new hashes), so rebasing a shared branch breaks every
other clone that has the old commits.

### The rule

Rebase local branches for tidiness; never rebase a shared branch. The rule exists because rewriting
published history changes the identity of commits other people depend on.

## 5. The Discipline

### Short-lived branches

Feature branches are short-lived and focused: one logical change, merged promptly, deleted after. A
short-lived branch keeps divergence small, keeps review fast, and keeps the main line deployable.

### The workflow

```text
branch -> small commits -> merge back -> delete the branch
```

The main line stays deployable because feature work is off it until the merge, and the merge is
deliberate.

### The history

The history stays readable when commits are focused and merges are deliberate. A tangled history of
long-lived branches is hard to read, hard to bisect, and hard to revert.

## 6. The Exercise

### What it models

The exercise models a branch, a fast-forward merge, and a conflict. A feature branch starts from the
main line's files, edits one, and leaves the main line untouched; a fast-forward merge moves the main
line to the feature's state; and two branches editing the same line are detected as a conflict.

### The assertions

```python
assert main_line.files["app.py"] == "print(1)", "main is untouched"
main_line = fast_forward(main_line, feature)
assert main_line.files["app.py"] == "print(2)"
assert conflict_lines(a, b, "app.py"), "same line changed differently"
```

The first assertion is the isolation: feature work does not touch the main line until the merge.

## Real-World Application

- A feature branch for one logical change, merged after review, so the main line stays deployable.
- Resolving a conflict by reading both changes and choosing the correct combined result.
- Rebasing a local branch to tidy its commits before merging, never rebasing the shared main line.
- Deleting merged branches so the branch list stays clean and the history stays readable.

## Common Mistakes

1. **Committing directly to the main line.** No isolation, no review gate.
2. **Long-lived branches that diverge.** Conflicts on many files.
3. **Resolving conflicts by picking one side blindly.** A change is silently lost.
4. **Rebasing a shared branch.** Other clones break.
5. **Never deleting merged branches.** A cluttered branch list.
6. **Merging without review.** The main line takes unreviewed changes.

## Key Takeaways

1. A branch is a movable pointer to a commit; switching updates the working tree and index.
2. Merging brings work back; fast-forward when undiverged, a merge commit when diverged.
3. A conflict means two changes touched the same lines; resolve it deliberately, never blindly.
4. Rebase rewrites history, so never rebase a shared branch.
5. Feature branches are short-lived and focused, keeping the main line deployable and the history
   readable.

## Self-Check Questions

1. Why does creating a branch not copy files?
2. What is the difference between a fast-forward merge and a merge commit?
3. Why is a conflict a signal rather than a failure, and how should it be resolved?
4. Why must you never rebase a shared branch?
5. How do short-lived branches reduce conflicts and keep the history readable?

## Further Reading / Connections

- Git-Linux 01 (basics) and 03 (remote workflows) — the surrounding model.
- `docs/cheat-sheets/git.md` — branch and merge commands.
- `docs/decisions/` — decisions recorded when structural choices are made.

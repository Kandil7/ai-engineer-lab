# Git-Linux 02: Branching and Merging

## 🎯 Topic Overview

Branches isolate work. A feature branch keeps experiments off the main
line until they are ready; merging brings them back. This lecture covers
branching, merging, conflicts, and the discipline of a clean history.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Create and switch branches
2. Merge a branch back into the main line
3. Resolve a merge conflict
4. Explain merge vs rebase
5. Keep the history readable

---

## 1. Branches

A branch is a movable pointer to a commit. Creating a branch does not copy
files — it points at the current commit and moves as new commits are made.
The main line stays stable while feature work happens in isolation. The
roadmap's exit test: "feature work happens on branches."

```bash
git branch feature-x   # create
git checkout feature-x # switch
git switch -c feature-x  # create and switch
```

## 2. Merging

Merging brings a branch's commits into another branch. A fast-forward
merge moves the pointer forward when the branches have not diverged. A
merge commit joins two divergent histories. The merge is the point where
the feature becomes part of the main line.

## 3. Conflicts

A conflict happens when two branches change the same lines. Git cannot
decide which version is correct — the conflict is marked in the file and
the developer resolves it. A conflict is not a failure; it is a signal
that two changes touched the same place. The resolution is deliberate,
never a blind pick.

## 4. Merge vs Rebase

Merge preserves history as it happened; rebase rewrites it as a clean
sequence. Rebase makes the history linear and readable but rewrites
commits — never rebase a shared branch. The roadmap's rule: "the history
is clean and readable."

## 5. The Discipline

Feature branches are short-lived and focused. A branch that lives for
weeks diverges and conflicts. The workflow: branch, small commits, merge
back, delete the branch. The main line stays deployable.

## Common Mistakes

- Committing directly to the main line.
- Long-lived branches that diverge.
- Resolving conflicts by picking one side blindly.
- Rebasing a shared branch.
- Never deleting merged branches.

## Key Takeaways

1. A branch is a movable pointer to a commit.
2. Merging brings work back to the main line.
3. A conflict means two changes touched the same lines.
4. Rebase rewrites history; never rebase shared branches.
5. Feature branches are short-lived and focused.
# Git-Linux 03: Remote Workflows

## 🎯 Topic Overview

A remote is a copy of the repository on another machine. Push sends local
commits up; pull brings remote commits down. The pull request is the
review gate between the two. This lecture covers remotes, the push/pull
loop, and the PR workflow.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Add and inspect a remote
2. Push local commits to a remote
3. Pull remote changes and resolve divergence
4. Open and review a pull request
5. Keep the remote and local in sync

---

## 1. Remotes

A remote is a named reference to another copy of the repository. The
default remote is `origin`. The remote is where collaboration happens —
pushing and pulling moves commits between machines. The roadmap's exit
test: "the repository is pushed to a remote."

```bash
git remote add origin https://github.com/user/repo.git
git remote -v   # list remotes
```

## 2. Push and Pull

Push sends local commits to the remote; pull brings remote commits down.
A push is rejected when the remote has commits the local does not — the
local must pull first and merge. The push/pull loop keeps the two in sync.
The roadmap's rule: "push after meaningful work."

## 3. Divergence

Divergence happens when local and remote both have commits the other
lacks. Pulling merges them; the merge may conflict. The discipline is to
pull often and push small, so divergence stays small. A large divergence
is a long-lived branch's fault.

## 4. The Pull Request

A pull request is a review gate: the branch's changes are proposed,
reviewed, and merged. The PR is where the code is read by someone else
before it reaches the main line. The roadmap's exit test: "changes are
reviewed before merging."

## 5. The Workflow

The daily loop: pull, branch, commit, push, open a PR, review, merge,
delete the branch. The remote is the source of truth for collaboration;
the local is the working copy.

## Common Mistakes

- Pushing without pulling first (rejected pushes).
- Large divergences from long-lived branches.
- Merging without review.
- Pushing secrets to a remote.
- Never pulling (the local drifts).

## Key Takeaways

1. A remote is a named reference to another copy.
2. Push sends commits up; pull brings them down.
3. Divergence is managed by pulling often and pushing small.
4. The PR is the review gate.
5. The remote is the source of truth for collaboration.
# Git-Linux 01: Git Basics

## Topic Overview

Git is the version control system every project runs on, and the core loop (init, add, commit,
status, log) is the foundation everything else builds on. Understanding it as three distinct areas
rather than as a set of commands is what makes the rest of Git predictable: the same three areas
explain branching, merging, rebasing, and every confusing state you will ever be in.

This lecture covers the working tree, the staging area, and the commit history, why staging is
deliberate rather than a formality, how to read history, and the `.gitignore` discipline that keeps
secrets and artifacts out of the repository permanently.

The single most important habit here is deliberate staging: reviewing what you are about to commit
and staging only that. It is what prevents secrets, debug code, and build artifacts from entering
the history, where they are costly or impossible to remove.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Initialize a repository and read its state.
2. Stage and commit changes, explaining what each command moves between areas.
3. Explain the three areas: working tree, index, HEAD.
4. Read the commit history and diffs.
5. Write a clear commit message.
6. Keep secrets and artifacts out with `.gitignore`.

## Prerequisites

- A terminal and a Git installation.
- Basic file editing.

---

## 1. The Three Areas

### The areas

Git tracks files across three areas:

- **Working tree:** your files on disk, as you edit them.
- **Index (staging area):** the set of changes prepared for the next commit.
- **HEAD:** the last commit, the recorded history.

### The movement

```bash
git init             # create a repository
git status           # show the state of the three areas
git add file.py      # working tree -> index
git commit -m "msg"  # index -> HEAD
```

`git add` moves a change from the working tree to the index; `git commit` moves the index to HEAD
and records it. Once you hold this model, `git status` reads as "what is different between the three
areas", which is the whole point of the command.

### Why the middle area exists

The index is what lets you commit exactly what you intend. Without it, every commit would be "all
current changes", which is how unrelated edits and secrets get bundled into commits. The index is the
review step between editing and committing.

## 2. The Commit

### What it is

A commit is a snapshot of the index with a message. The snapshot is complete: a commit records the
whole tree, not a diff, though Git stores it efficiently.

### The message

The message is the history's documentation: what changed and why. A clear message is imperative,
concise, and specific ("fix: handle empty input in parse_title"), not vague ("fix stuff"). A history
of clear messages is a readable account of how the project evolved.

### The identity

Each commit has a hash, an author, a date, and a message. The hash is the commit's identity and how
the history is addressed; it also makes the history tamper-evident, because changing a commit changes
every hash after it.

## 3. Reading History

### Log and diff

`git log` shows the commit history; `git diff` shows changes not yet staged, and `git diff --staged`
shows what is staged. Reading history and diffs before committing is the review that keeps the history
clean.

### Why read before commit

The habit of running `git status` and `git diff --staged` before every commit catches the accidental
`git add -A` that swept in an untracked file. It is a ten-second check that prevents a costly mistake.

### The exit test

The roadmap's exit test is that the commit history is clean and readable. That is achieved by small,
focused commits with clear messages, which the index makes possible.

## 4. The .gitignore

### What it excludes

Some files never belong in the repository: secrets (`.env`, keys), build artifacts, dependency
directories, and large assets. The `.gitignore` excludes them by pattern.

### The permanence problem

A secret committed once is in the history forever, even after the file is deleted, because the
commit that contains it is still reachable. Removing it requires rewriting history, which is
disruptive. The only reliable fix is prevention: `.gitignore` before the first commit.

### The categories

A good `.gitignore` covers secrets and environment files, build output, caches (`.pytest_cache`,
`__pycache__`, `.mypy_cache`), IDE files, and large generated assets. This repository's `.gitignore`
follows exactly these categories.

## 5. The Workflow

### The daily loop

```text
git status -> edit -> git add <intended files> -> git diff --staged -> git commit -> repeat
```

The loop is small, and its value is the deliberate staging step: you name the files rather than
staging everything.

### Deliberate staging

Staging is deliberate: `git add specific_file.py`, not `git add -A`. Naming the files forces a
moment of review and prevents the accidental inclusion of secrets or unrelated changes.

### The review habit

Review the staged diff before committing. If a file you did not intend is staged, unstage it. If a
secret is staged, unstage and add it to `.gitignore` before it ever enters history.

## 6. The Exercise

### What it models

The exercise models the three areas with a `Repo` class: a working tree, an index, and HEAD. It
stages one intended file, leaves a secret unstaged, commits, and asserts the secret never enters the
history.

### The assertions

```python
repo.add("app.py")
assert "app.py" in repo.index
assert "secret.env" not in repo.index        # only the intended file staged
repo.commit("feat: add app entry point")
assert "secret.env" not in repo.head         # secrets never enter the history
```

The second and third assertions are the ones that matter: deliberate staging and no secrets in
history.

## Real-World Application

- Staging only the files for one logical change so each commit is focused and revertible.
- Running `git diff --staged` before committing to catch an accidental inclusion.
- Adding `.env` to `.gitignore` before the first commit so a secret never enters history.
- Writing messages like "refactor: extract parse_title" so the history explains why, not just what.

## Common Mistakes

1. **Committing secrets.** They live in the history forever.
2. **Blind staging (`git add -A`).** Unrelated changes and secrets get swept in.
3. **Vague commit messages.** "fix stuff" documents nothing.
4. **Committing build artifacts and large assets.** They bloat the repository permanently.
5. **Never checking status before committing.** The accidental inclusion is not caught.
6. **Committing changes that belong to different logical units.** The history becomes unrevertible.

## Key Takeaways

1. Three areas: working tree, index, HEAD; `add` and `commit` move changes between them.
2. A commit is a complete snapshot with a message; the hash is its identity.
3. Read `status` and the staged diff before every commit; it is the review that keeps history clean.
4. `.gitignore` prevents secrets and artifacts from entering history, where removal is costly.
5. Staging is deliberate: name the files, and commit only what you intend.

## Self-Check Questions

1. What are the three areas, and which command moves a change between each pair?
2. Why does the index exist rather than committing all changes directly?
3. Why is a committed secret so hard to remove?
4. What do you gain by running `git diff --staged` before committing?
5. Why is `git add -A` a risky default?

## Further Reading / Connections

- Git-Linux 02 (branching and merging) and 03 (remote workflows) — the next layers on this model.
- `docs/cheat-sheets/git.md` — the command reference.
- `docs/WEEKLY_PROTOCOL.md` — the commit-daily discipline this supports.

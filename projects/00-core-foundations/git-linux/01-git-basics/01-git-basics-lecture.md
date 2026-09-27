# Git-Linux 01: Git Basics

## 🎯 Topic Overview

Git is the version control system every project runs on. The core loop —
init, add, commit, status, log — is the foundation everything else builds
on. This lecture covers the working tree, the staging area, and the commit
history.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Initialize a repository and check its state
2. Stage and commit changes
3. Read the commit history
4. Explain the three areas: working tree, index, HEAD
5. Write a clear commit message

---

## 1. The Three Areas

Git tracks files across three areas. The working tree is your files on
disk. The index (staging area) is the set of changes ready to commit. HEAD
is the last commit. `git add` moves changes from the working tree to the
index; `git commit` moves them from the index to HEAD.

```bash
git init          # create a repository
git status        # show the state of the three areas
git add file.py   # working tree -> index
git commit -m "msg"  # index -> HEAD
```

## 2. The Commit

A commit is a snapshot of the index with a message. The message is the
history's documentation: what changed and why. A clear message is
imperative, concise, and specific. The roadmap's exit test: "the commit
history is clean and readable."

## 3. Reading History

`git log` shows the commit history. Each commit has a hash, an author, a
date, and a message. The hash is the commit's identity — it is how the
history is addressed. `git diff` shows changes before they are committed.

## 4. The .gitignore

Some files never belong in the repository: secrets, build artifacts, and
large assets. The `.gitignore` excludes them. A secret committed once is
in the history forever, even after deletion. The roadmap's rule: "never
commit secrets."

## 5. The Workflow

The daily loop is: check status, make changes, stage the intended files,
commit with a clear message, repeat. Staging is deliberate — only the
intended files are committed, never a blind `git add -A`.

## Common Mistakes

- Committing secrets (they live in history forever).
- Blind staging everything (`git add -A`).
- Vague commit messages ("fix stuff").
- Committing build artifacts and large assets.
- Never checking status before committing.

## Key Takeaways

1. Three areas: working tree, index, HEAD.
2. A commit is a snapshot with a message.
3. The hash is the commit's identity.
4. .gitignore keeps secrets and artifacts out.
5. Staging is deliberate; commit only what is intended.
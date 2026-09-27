# Git-Linux 01: Git Basics — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Working tree | Your files on disk | uncommitted edits |
| Index | The staged changes ready to commit | git add |
| HEAD | The last commit | git log |
| Commit | A snapshot of the index with a message | git commit |
| Commit hash | The commit's identity | a1b2c3d |
| .gitignore | Files excluded from the repository | secrets, artifacts |
| git status | The state of the three areas | what changed |

---

## Alphabetical Glossary

### .gitignore

**Definition:** The file that excludes paths from the repository: secrets,
build artifacts, and large assets. A secret committed once is in history
forever.

**Example:**
```gitignore
.env
*.pyc
outputs/
```

**Related concepts:** Commit

---

### Commit

**Definition:** A snapshot of the index with a message. The message is the
history's documentation: what changed and why.

**Example:**
```bash
git commit -m "docs: add git basics lecture"
```

**Related concepts:** Index, HEAD

---

### Commit hash

**Definition:** The commit's identity, used to address the history. The
hash is how a specific snapshot is referenced.

**Example:**
```bash
git log --oneline  # a1b2c3d docs: add git basics
```

**Related concepts:** Commit

---

### HEAD

**Definition:** The last commit on the current branch. The destination of
`git commit`.

**Example:**
```bash
git log -1  # shows HEAD
```

**Related concepts:** Commit

---

### Index

**Definition:** The staging area: the set of changes ready to commit.
`git add` moves changes from the working tree here.

**Example:**
```bash
git add file.py  # working tree -> index
```

**Related concepts:** Working tree, Commit

---

### Working tree

**Definition:** Your files on disk, as they are. Changes here are not part
of any commit until staged.

**Example:**
```bash
git status  # shows working tree changes
```

**Related concepts:** Index

---

### git status

**Definition:** The command that shows the state of the three areas: what
is modified, staged, or untracked.

**Example:**
```bash
git status --short
```

**Related concepts:** Working tree, Index

---

## Related Concepts

- **Branching**: commits build the branch history (topic 02)
- **Remote workflows**: commits are pushed to remotes (topic 03)
- **Linux**: the shell runs the git commands (topic 04)

## Key Takeaways

1. Three areas: working tree, index, HEAD.
2. A commit is a snapshot with a message.
3. The hash is the commit's identity.
4. .gitignore keeps secrets and artifacts out.
5. Staging is deliberate; commit only what is intended.
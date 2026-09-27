# Git-Linux 02: Branching and Merging — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Branch | A movable pointer to a commit | feature-x |
| Merge | Bringing a branch's commits into another | merge commit |
| Fast-forward | Pointer moves forward, no divergence | linear history |
| Conflict | Two branches changed the same lines | resolve deliberately |
| Rebase | Rewriting commits as a clean sequence | linear history |
| Main line | The stable, deployable branch | main |
| Feature branch | Short-lived isolated work | short-lived, focused |

---

## Alphabetical Glossary

### Branch

**Definition:** A movable pointer to a commit. Creating a branch does not
copy files; it points at the current commit and moves as new commits are
made.

**Example:**
```bash
git switch -c feature-x
```

**Related concepts:** Main line, Feature branch

---

### Conflict

**Definition:** Two branches changed the same lines and git cannot decide
which version is correct. The conflict is marked in the file; the
resolution is deliberate, never a blind pick.

**Example:**
```bash
# <<<<<<< HEAD ... ======= ... >>>>>>> feature-x
```

**Related concepts:** Merge

---

### Fast-forward

**Definition:** A merge that moves the pointer forward because the branches
have not diverged. Produces a linear history.

**Example:**
```bash
git merge feature-x  # fast-forward when main has not moved
```

**Related concepts:** Merge

---

### Feature branch

**Definition:** A short-lived branch isolating one piece of work. Short
lives avoid divergence and conflicts.

**Example:**
```bash
# branch, small commits, merge back, delete
```

**Related concepts:** Branch, Main line

---

### Main line

**Definition:** The stable, deployable branch. Feature work happens
elsewhere and merges back when ready.

**Example:**
```bash
# main stays deployable; features merge in
```

**Related concepts:** Feature branch

---

### Merge

**Definition:** Bringing a branch's commits into another branch. The point
where the feature becomes part of the main line.

**Example:**
```bash
git merge feature-x
```

**Related concepts:** Conflict, Fast-forward

---

### Rebase

**Definition:** Rewriting commits as a clean sequence instead of preserving
the history as it happened. Never rebase a shared branch.

**Example:**
```bash
git rebase main  # linear history, but rewrites commits
```

**Related concepts:** Merge

---

## Related Concepts

- **Git basics**: commits build the branch history (topic 01)
- **Remote workflows**: branches are pushed and merged via PRs (topic 03)
- **Linux**: the shell runs the git commands (topic 04)

## Key Takeaways

1. A branch is a movable pointer to a commit.
2. Merging brings work back to the main line.
3. A conflict means two changes touched the same lines.
4. Rebase rewrites history; never rebase shared branches.
5. Feature branches are short-lived and focused.
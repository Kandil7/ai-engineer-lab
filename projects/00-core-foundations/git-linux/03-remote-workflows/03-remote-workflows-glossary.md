# Git-Linux 03: Remote Workflows — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Remote | A named reference to another copy of the repo | origin |
| Push | Sending local commits to the remote | git push |
| Pull | Bringing remote commits down | git pull |
| Divergence | Local and remote both have commits the other lacks | merge needed |
| Pull request | The review gate for a branch's changes | reviewed before merge |
| origin | The default remote name | git remote add origin |
| Rejected push | Remote has commits the local lacks | pull first |

---

## Alphabetical Glossary

### Divergence

**Definition:** Local and remote both have commits the other lacks. Pulling
merges them; the merge may conflict. Managed by pulling often and pushing
small.

**Example:**
```bash
git pull  # merge the remote's commits
```

**Related concepts:** Push, Pull

---

### origin

**Definition:** The default remote name, added when the repository is
cloned or configured.

**Example:**
```bash
git remote add origin https://github.com/user/repo.git
```

**Related concepts:** Remote

---

### Pull

**Definition:** Bringing remote commits down to the local repository. The
other half of the push/pull loop.

**Example:**
```bash
git pull origin main
```

**Related concepts:** Push, Divergence

---

### Pull request

**Definition:** The review gate: a branch's changes are proposed, reviewed,
and merged. Where the code is read by someone else before the main line.

**Example:**
```bash
# branch -> PR -> review -> merge -> delete branch
```

**Related concepts:** Remote

---

### Push

**Definition:** Sending local commits to the remote. Rejected when the
remote has commits the local lacks.

**Example:**
```bash
git push origin main
```

**Related concepts:** Pull, Rejected push

---

### Rejected push

**Definition:** The remote has commits the local does not. The local must
pull and merge before pushing.

**Example:**
```bash
# ! [rejected] -> git pull, then push again
```

**Related concepts:** Push, Divergence

---

### Remote

**Definition:** A named reference to another copy of the repository. The
default is `origin`. Where collaboration happens.

**Example:**
```bash
git remote -v  # list remotes
```

**Related concepts:** origin, Push

---

## Related Concepts

- **Git basics**: commits are what get pushed (topic 01)
- **Branching**: branches are pushed and merged via PRs (topic 02)
- **Linux**: the shell runs the git commands (topic 04)

## Key Takeaways

1. A remote is a named reference to another copy.
2. Push sends commits up; pull brings them down.
3. Divergence is managed by pulling often and pushing small.
4. The PR is the review gate.
5. The remote is the source of truth for collaboration.
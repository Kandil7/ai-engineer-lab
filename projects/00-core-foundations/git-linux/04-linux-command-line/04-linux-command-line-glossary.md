# Git-Linux 04: Linux Command Line — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| Shell | The program that runs commands | bash |
| Pipe | One command's output into another's input | \| |
| grep | Search file contents | grep "error" |
| Permissions | Read, write, execute per owner/group/others | chmod |
| chmod | Change file permissions | chmod +x |
| Destructive command | Deletes or overwrites without recovery | rm -rf |
| Tab completion | The shell completes names | press Tab |

---

## Alphabetical Glossary

### chmod

**Definition:** The command that changes file permissions. Read, write,
and execute, for the owner, the group, and others.

**Example:**
```bash
chmod +x script.sh  # add execute
```

**Related concepts:** Permissions

---

### Destructive command

**Definition:** A command that deletes or overwrites without recovery.
`rm -rf` is the canonical example. Requires understanding before running.

**Example:**
```bash
rm -rf dir  # deletes without recovery
```

**Related concepts:** Permissions

---

### grep

**Definition:** The command that searches file contents by pattern. The
workhorse of log and text inspection.

**Example:**
```bash
grep "error" app.log
```

**Related concepts:** Pipe

---

### Permissions

**Definition:** Read, write, and execute access, set per owner, group, and
others. Changed with `chmod`, ownership with `chown`.

**Example:**
```bash
ls -l  # shows permissions
```

**Related concepts:** chmod

---

### Pipe

**Definition:** The operator that sends one command's output into another's
input. Composes small tools into powerful one-liners.

**Example:**
```bash
grep "error" log | sort | uniq -c
```

**Related concepts:** grep

---

### Shell

**Definition:** The program that runs commands. The prompt is where you
type; the shell interprets, runs, and returns output.

**Example:**
```bash
pwd; ls; cd dir
```

**Related concepts:** Tab completion

---

### Tab completion

**Definition:** The shell completes file and command names when you press
Tab. Saves typing and prevents typos.

**Example:**
```bash
cd proj<Tab>  # completes the directory name
```

**Related concepts:** Shell

---

## Related Concepts

- **Git basics**: the shell runs the git commands (topic 01)
- **Data engineering**: text processing with pipes (stage 5)
- **DevOps**: the shell drives deployment (stage 6)

## Key Takeaways

1. The shell runs commands; the prompt is where you type.
2. Files and text are the unit of work.
3. Pipes compose small tools into one-liners.
4. Permissions control read, write, and execute.
5. Destructive commands require understanding.
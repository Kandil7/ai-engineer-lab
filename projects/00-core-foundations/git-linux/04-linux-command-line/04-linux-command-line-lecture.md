# Git-Linux 04: Linux Command Line

## Topic Overview

The command line is where the work happens: files, processes, pipes, and permissions. It is faster
than a graphical interface for the tasks a developer repeats all day, and it composes: small tools
chained with pipes do work that would take a program to do otherwise. It is also unforgiving, because
a mistyped destructive command has no undo.

This lecture covers the shell, working with files and text, pipes, file permissions, and the safety
discipline that makes the power usable. The safety part is not an afterthought: the same power that
makes a one-liner efficient makes a mistake expensive.

## Learning Objectives

By the end of this lecture, you will be able to:

1. Navigate and manipulate the filesystem.
2. Read, search, and slice files.
3. Chain commands with pipes.
4. Explain file permissions and change them.
5. Identify destructive commands before running them.
6. Explain why the command line's power demands care.

## Prerequisites

- Git-Linux 01 to 03.
- A terminal.

---

## 1. The Shell

### What it is

The shell is a program that runs commands. The prompt is where you type; the shell interprets the
command, runs it, and returns the output. It has history, tab completion, and variables, which make
it fast for repeated work.

### Navigation

```bash
pwd        # where am I
ls         # what is here
cd dir     # change directory
```

Navigation is the first fluency: knowing where you are and what is there. Most confusion in the shell
is being somewhere unexpected.

### History and completion

Tab completion and command history are not conveniences; they are correctness tools. Tab completion
prevents typos in paths, and history prevents re-typing (and re-typing errors). Use both.

## 2. Files and Text

### The unit of work

Files are the unit of work: reading, searching, and editing. The common tools:

```bash
cat file.txt        # read
grep "error" log    # search
head -20 file.txt   # first lines
tail -f log         # follow a log in real time
```

### Why text

Text processing is where the shell shines, because logs, configs, and data files are text. The
Unix philosophy is small tools that do one thing and compose, and text is the universal interface
between them.

### The search habit

Searching is more reliable than remembering. `grep` for the error, the function, the config key;
the shell answers faster than memory and without a mistake.

## 3. Pipes

### What a pipe does

A pipe sends one command's output into another's input. It composes small tools into a one-liner:

```bash
grep "error" log | sort | uniq -c | sort -rn
```

That chain filters errors, sorts them, counts the unique ones, and sorts by count, all in one line.

### Why composition matters

Each tool does one thing well; the pipe is what lets them cooperate. This is the same composition
principle as modular code, applied to command-line tools.

### The exit test

The roadmap's exit test is that commands are chained with pipes. The skill is knowing the small tools
and how they compose, which comes from use.

## 4. Permissions

### The model

Every file has an owner and a permission set: read, write, and execute, for the owner, the group, and
others.

```bash
chmod +x script.sh    # make executable
chmod 644 file.txt    # owner rw, group/other r
chown user file.txt   # change owner
```

### Why permissions matter

Permissions control who can read, write, and run a file. A secret with world-readable permissions is
a leak; a script without the execute bit does not run. Permissions are a correctness and security
concern, not a formality.

### The link to safety

Permissions interact with destructive commands: a command that can write a file can overwrite it.
Understanding permissions is part of understanding what a command will do.

## 5. Safety

### The unforgiving part

The command line is powerful and unforgiving. `rm -rf` deletes without recovery:

```python
def is_destructive(cmd: str) -> bool:
    """Destructive commands delete or overwrite without recovery."""
    return cmd.startswith("rm -rf") or cmd.startswith("rm -r")
```

### The discipline

Read the command before running it, test on a copy, and never run a destructive command casually. The
flags matter: `rm -r` recurses, `-f` forces, and together they delete a tree without asking.

### Flags before destructive commands

Some tools have a dry-run flag (`--dry-run`, `-n`) that shows what would happen without doing it. Use
it before any command that deletes or overwrites broadly, and never run a recursive delete on a path
you have not verified.

### The link to this repo

The workstation's safety rules forbid the destructive commands (`rm -rf`, `diskpart`, `mkfs`, and so
on) and require approval for the rest. That discipline is this section, enforced.

## 6. The Exercise

### What it models

The exercise models pipes (filter, sort, deduplicate, slice) and the destructive-command check.

### The assertions

```python
result = pipe(["grep-error", "sort", "uniq"], log)
assert result == ["error: retry", "error: timeout"], "filtered, sorted, deduped"
assert is_destructive("rm -rf /tmp/x")
assert not is_destructive("ls -la")
```

The pipe chain shows composition; the destructive check shows the safety rule.

## Real-World Application

- Chaining `grep | sort | uniq -c | sort -rn` to find the most common error in a log.
- Following a service log with `tail -f` while reproducing a bug.
- Using tab completion for paths so a typo cannot delete the wrong directory.
- Checking a command's dry-run before running a broad overwrite.

## Common Mistakes

1. **`rm -rf` without checking the path.** No recovery.
2. **Running commands without understanding them.** Especially copied one-liners.
3. **Never using pipes.** Retyping output by hand.
4. **Ignoring permissions.** Secrets world-readable or scripts not executable.
5. **No tab completion or history.** Avoidable typos and retyping.
6. **Running a destructive command without a dry-run.** The mistake is discovered too late.

## Key Takeaways

1. The shell runs commands; history and tab completion are correctness tools.
2. Files and text are the unit of work; search beats remembering.
3. Pipes compose small tools into one-liners.
4. Permissions control read, write, and execute and are a security concern.
5. Destructive commands require understanding: read, dry-run, and verify the path first.

## Self-Check Questions

1. Why are tab completion and history correctness tools rather than conveniences?
2. What does a pipe do, and why does composition matter?
3. What do file permissions control, and why are they a security concern?
4. Why is `rm -rf` especially dangerous, and what discipline reduces the risk?
5. Why prefer searching with `grep` over relying on memory?

## Further Reading / Connections

- Git-Linux 01 to 03 — the Git model built on the shell.
- `docs/cheat-sheets/git.md` — command reference.
- `AGENTS.md` — the workstation safety rules that enforce this discipline.

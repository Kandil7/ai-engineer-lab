# Git-Linux 04: Linux Command Line

## 🎯 Topic Overview

The command line is where the work happens: files, processes, pipes, and
permissions. This lecture covers the shell, the filesystem, text
processing, and the discipline of safe commands.

## 📚 Learning Objectives

By the end of this lecture, you will be able to:

1. Navigate and manipulate the filesystem
2. Read and search files
3. Chain commands with pipes
4. Understand file permissions
5. Run commands safely

---

## 1. The Shell

The shell is a program that runs commands. The prompt is where you type;
the shell interprets, runs, and returns output. The shell has history,
tab completion, and variables. The roadmap's exit test: "the command line
is used fluently."

```bash
pwd        # where am I
ls         # what is here
cd dir     # change directory
```

## 2. Files and Text

Files are the unit of work. Reading, searching, and editing files is the
daily loop. `cat` reads, `grep` searches, `head`/`tail` slice. Text
processing is where the shell shines — logs, configs, and data are text.

```bash
cat file.txt        # read
grep "error" log    # search
head -20 file.txt   # first lines
tail -f log         # follow a log
```

## 3. Pipes

A pipe sends one command's output into another's input. Pipes compose
small tools into powerful one-liners. The roadmap's exit test: "commands
are chained with pipes."

```bash
grep "error" log | sort | uniq -c | sort -rn
```

## 4. Permissions

Every file has an owner and permissions: read, write, execute, for the
owner, the group, and others. `chmod` changes permissions; `chown` changes
ownership. The roadmap's rule: "never run destructive commands without
understanding them."

## 5. Safety

The command line is powerful and unforgiving. `rm -rf` deletes without
recovery. The discipline: read the command before running it, test on a
copy, and never run destructive commands casually. The roadmap's rule:
"destructive commands require understanding."

## Common Mistakes

- `rm -rf` without checking the path.
- Running commands without understanding them.
- Never using pipes (retyping output by hand).
- Ignoring permissions.
- No tab completion or history.

## Key Takeaways

1. The shell runs commands; the prompt is where you type.
2. Files and text are the unit of work.
3. Pipes compose small tools into one-liners.
4. Permissions control read, write, and execute.
5. Destructive commands require understanding.
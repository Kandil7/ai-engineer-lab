# Python 02: Get Started — Glossary

## Quick Reference Table

| Term | Definition | Example |
|------|-----------|---------|
| PATH | OS search list for executable names | python resolution |
| REPL | Read-eval-print loop: interactive interpreter | probes |
| sys.executable | Absolute path of the running interpreter | which-Python answer |
| Site-packages | Third-party install target of an interpreter | per-env isolation |
| App-execution alias | Store shim intercepting names like `python` | Windows trap |
| `-c` flag | One-liner execution without a file | quick probes |

---

## Alphabetical Glossary

### App-execution alias

**Definition:** Windows Store shim that captures `python` when no real
installation claims PATH first. Opens the Store instead of running code.

**Example:**
```python
# fix: disable the alias, or use the py launcher
```

**Related concepts:** PATH

---

### PATH

**Definition:** The ordered directory list the shell searches for command
names. "Not recognized" always means the entry is missing here.

**Example:**
```bash
# installer checkbox adds Python + Scripts/; new terminal required
```

**Related concepts:** sys.executable, App-execution alias

---

### REPL

**Definition:** Interactive interpreter loop for experiments and probes.
Disposable history — never the home of deliverables.

**Example:**
```bash
python  # >>> 2 + 2 ... then write the script
```

**Related concepts:** `-c` flag

---

### Site-packages

**Definition:** The per-interpreter directory third-party packages install
into. Why `pip install` can "succeed" while `import` fails: two interpreters,
two directories.

**Example:**
```python
python -m pip install X  # binds installer to THIS interpreter, always
```

**Related concepts:** sys.executable

---

### sys.executable

**Definition:** Absolute path of the currently running interpreter. The
ground truth for "which Python" in venvs, tools, CI, and debugging.

**Example:**
```python
import sys

print(sys.executable)
```

**Related concepts:** PATH, Site-packages

---

### `-c` flag

**Definition:** Executes a command string without a file. Probes, version
checks, and one-off inspections — quoting through shells carefully.

**Example:**
```bash
python -c "import sys; print(sys.version)"
```

**Related concepts:** REPL

---

## Related Concepts

- **py launcher**: version-selective Windows entry (`py -3.12`)
- **venv**: per-project interpreters (later topic)
- **Smoke tests**: `run_smoke_tests.py` assumes one explicit interpreter

## Key Takeaways

1. Verify the interpreter before trusting any later error message.
2. `python -m pip` binds installer to interpreter, always.
3. Scripts are deliverables; REPL sessions are scratch.
